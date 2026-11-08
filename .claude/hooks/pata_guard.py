#!/usr/bin/env python3
"""Pata guard hooks for Claude Code.

One script, four modes (wired in .claude/settings.json):
  pre-bash       PreToolUse  Bash                -> block forbidden commands
  pre-edit       PreToolUse  Edit|Write|MultiEdit|NotebookEdit
                                                 -> block forbidden writes
  post-edit      PostToolUse Edit|Write|MultiEdit
                                                 -> re-validate graph.toml
  session-start  SessionStart                    -> inject LOOP reminder + state

Exit 2 = block (stderr is shown to Claude as the reason).
Pre-* modes FAIL CLOSED: any internal error blocks the action.
Stdlib only.

ADR protection works on the *result* of an edit, not just the new text:
the edit is applied to the current file in memory and the ADR status is
compared before vs. after. A transition to "accepted", or any newly added
acceptance record, is blocked.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path, PurePosixPath

# ---------------------------------------------------------------- policy
# Folders holding decision records (relative, POSIX). Pata uses docs/decisions/.
ADR_DIRS = ("docs/decisions/", "docs/adr/")

# Paths Claude must never write to by hand (relative to project root, POSIX).
PROTECTED_WRITE = [
    "data/raw/",
    "private/",
    "staging/",
    ".claude/hooks/",
    ".claude/settings.json",
    "vendor/unicode/Scripts.txt",
]
# Paths that must never be staged into git.
PROTECTED_GIT_ADD = ["data/raw", "private", "staging", "denylist", "exposure"]

BASH_RULES: list[tuple[str, str]] = [
    (
        r"\bgit\s+push\b",
        ("Pushing is maintainer-only. Report the branch/commit and ask the maintainer to push."),
    ),
    (
        r"\bgit\s+merge\b",
        ("Merging is maintainer-only (ADR branches especially). Prepare a review packet instead."),
    ),
    (r"\bgit\s+rebase\b", "Rewriting history needs explicit maintainer approval."),
    (
        r"\bgit\s+reset\s+--hard\b",
        "Destructive reset is blocked. Use `git stash` or a new branch.",
    ),
    (
        r"\bgit\s+clean\s+-[a-z]*f",
        "`git clean -f` deletes untracked work (may include staging data).",
    ),
    (r"\bgit\s+branch\s+-D\b", "Force-deleting branches is maintainer-only."),
    (r"\bgit\s+(commit|push)\b.*--no-verify", "Skipping checks is not allowed."),
    (
        r"\bgit\s+add\b.*\s(-f|--force)\b",
        "Force-adding ignored files is blocked (raw/private data stays out of Git).",
    ),
    (
        r"\bgh\s+(pr\s+merge|repo\s+(edit|create|delete)|release\s+create)\b",
        "Remote repo/PR/release actions are maintainer-only.",
    ),
    (
        r"graph\.py\b.*\bapprove\b",
        "Approvals are recorded by the maintainer in their own terminal.",
    ),
    (
        (
            r"\brm\s+-[a-z]*r[a-z]*\s+.*\b(data|private|staging|releases|"
            r"docs/decisions|docs/adr)\b"
        ),
        "Recursive delete of project data/decision folders is blocked.",
    ),
]

# "Status: Accepted", "**Status:** Accepted", "- status: accepted",
# "| Status | Accepted |", YAML front matter "status: accepted".
STATUS_LINE = re.compile(
    r"(?im)^[\s>*\-|]*\**\s*status\s*\**\s*[:|\-–]+\s*\**\s*([A-Za-z][^\n|*]*)"
)
# "## Status" heading followed by the value on the next non-empty line.
STATUS_HEADING = re.compile(r"(?im)^\s*#{1,6}\s*status\s*:?\s*$\n+\s*[*_]*\s*([^\n]+)")
# Acceptance records anywhere in the document.
ACCEPT_RECORD = re.compile(
    r"(?i)\baccepted\s+(on|by)\b|\baccepted\s*\(\s*\d{4}-\d{2}-\d{2}"
    r"|\bmaintainer\s+acceptance\s*:"
)
APPROVAL_TEXT = re.compile(r"\[\[\s*approval\s*\]\]|^\s*approved_by\s*=", re.MULTILINE)


# ---------------------------------------------------------------- helpers
def project_root(event: dict) -> Path:
    raw = os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or "."
    return Path(raw).resolve()


def rel_posix(path_str: str, root: Path) -> str:
    p = Path(path_str)
    if not p.is_absolute():
        p = root / p
    try:
        rel = p.resolve().relative_to(root)
    except ValueError:
        return PurePosixPath(path_str.replace("\\", "/")).as_posix()
    out = rel.as_posix()
    return out.lower() if os.name == "nt" else out


def block(msg: str) -> None:
    print(f"[pata-guard] BLOCKED: {msg}", file=sys.stderr)
    sys.exit(2)


def edit_texts(tool: str, ti: dict) -> list[str]:
    if tool == "Write":
        return [ti.get("content", "")]
    if tool == "Edit":
        return [ti.get("new_string", "")]
    if tool == "MultiEdit":
        return [e.get("new_string", "") for e in ti.get("edits", [])]
    if tool == "NotebookEdit":
        return [ti.get("new_source", "")]
    return []


def _apply(text: str, old: str, new: str, replace_all: bool) -> str:
    if not old or old not in text:
        # Unknown anchor: be conservative and judge the new text on its own.
        return text + "\n" + new
    return text.replace(old, new) if replace_all else text.replace(old, new, 1)


def simulate(tool: str, ti: dict, before: str) -> str:
    """Return the file content the tool call would produce."""
    if tool == "Write":
        return ti.get("content", "")
    if tool == "Edit":
        return _apply(
            before,
            ti.get("old_string", ""),
            ti.get("new_string", ""),
            bool(ti.get("replace_all")),
        )
    if tool == "MultiEdit":
        after = before
        for e in ti.get("edits", []):
            after = _apply(
                after,
                e.get("old_string", ""),
                e.get("new_string", ""),
                bool(e.get("replace_all")),
            )
        return after
    return before + "\n".join(edit_texts(tool, ti))


def adr_status(text: str) -> str | None:
    """First declared status value, lower-cased, or None if none found."""
    found = []
    for rx in (STATUS_LINE, STATUS_HEADING):
        m = rx.search(text)
        if m:
            found.append((m.start(), m.group(1).strip().strip("*_ ").lower()))
    return min(found)[1] if found else None


def is_accepted(text: str) -> bool:
    st = adr_status(text)
    return bool(st) and st.startswith("accepted")


def is_adr_path(rel: str) -> bool:
    return rel.endswith(".md") and any(rel.startswith(d) for d in ADR_DIRS)


def run_validate(root: Path) -> tuple[bool, str]:
    script = root / "scripts" / "graph.py"
    if not script.exists():
        return True, ""
    proc = subprocess.run(
        [sys.executable, str(script), "validate"],
        capture_output=True,
        text=True,
        cwd=root,
        timeout=60,
        check=False,
    )
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip()


# ---------------------------------------------------------------- modes
def pre_bash(event: dict) -> None:
    cmd = event.get("tool_input", {}).get("command", "")
    flat = " ".join(cmd.split())
    for pattern, reason in BASH_RULES:
        if re.search(pattern, flat):
            block(reason)
    # git add of protected paths (keep .gitignore right for `git add .`)
    for m in re.finditer(r"\bgit\s+add\b([^;&|]*)", flat):
        try:
            args = shlex.split(m.group(1))
        except ValueError:
            args = m.group(1).split()
        for a in args:
            low = a.replace("\\", "/").lower()
            if any(p in low for p in PROTECTED_GIT_ADD):
                block(f"`git add {a}` would stage raw/private/staging data.")
    # commits require a valid graph
    if re.search(r"\bgit\s+commit\b", flat):
        ok, out = run_validate(project_root(event))
        if not ok:
            block("workflow/graph.toml is invalid — fix before committing:\n" + out)


def check_adr(tool: str, ti: dict, path: Path) -> None:
    before = path.read_text(encoding="utf-8") if path.exists() else ""
    after = simulate(tool, ti, before)
    reason = None
    if is_accepted(after) and not is_accepted(before):
        reason = "this edit would change the decision status to Accepted"
    elif len(ACCEPT_RECORD.findall(after)) > len(ACCEPT_RECORD.findall(before)):
        reason = "this edit adds an acceptance record"
    if reason:
        block(
            f"{reason}. Accepting a decision record is the maintainer's act. "
            "Leave the status as Proposed and list the acceptance step in your "
            "report."
        )


def pre_edit(event: dict) -> None:
    tool = event.get("tool_name", "")
    ti = event.get("tool_input", {})
    path_str = ti.get("file_path") or ti.get("notebook_path") or ""
    root = project_root(event)
    rel = rel_posix(path_str, root)
    for prefix in PROTECTED_WRITE:
        if rel == prefix.rstrip("/") or rel.startswith(prefix):
            block(
                f"'{rel}' is protected (raw/private/staging data, vendored "
                "files or the guard itself). Generate such files with project "
                "scripts, or ask the maintainer."
            )
    if is_adr_path(rel):
        p = Path(path_str)
        check_adr(tool, ti, p if p.is_absolute() else root / p)
    if rel == "workflow/graph.toml":
        for t in edit_texts(tool, ti):
            if APPROVAL_TEXT.search(t):
                block(
                    "Approval records are append-only and maintainer-written "
                    "(`uv run python scripts/graph.py approve ...`)."
                )


def post_edit(event: dict) -> None:
    ti = event.get("tool_input", {})
    root = project_root(event)
    rel = rel_posix(ti.get("file_path", ""), root)
    if rel != "workflow/graph.toml":
        return
    ok, out = run_validate(root)
    if not ok:
        print(
            "[pata-guard] graph.toml is now INVALID — fix it before doing anything else:\n" + out,
            file=sys.stderr,
        )
        sys.exit(2)


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        cwd=root,
        timeout=10,
        check=False,
    )
    return proc.stdout


def session_start(event: dict) -> None:
    root = project_root(event)
    lines = [
        "PATA SESSION START — follow docs/workflow/LOOP.md.",
        (
            "Hard rules: no push/merge/ADR-acceptance/approvals by Claude; "
            "no fabricated data, licences or results;"
        ),
        ("raw/private/staging data never enters Git; ask before any node marked IRREVERSIBLE."),
    ]
    script = root / "scripts" / "graph.py"
    if script.exists():
        proc = subprocess.run(
            [sys.executable, str(script), "next"],
            capture_output=True,
            text=True,
            cwd=root,
            timeout=60,
            check=False,
        )
        state = proc.stdout.strip() or proc.stderr.strip()
        lines += ["", "Graph state (scripts/graph.py next):", state]
    try:
        branch = _git(root, "branch", "--show-current").strip()
        status = _git(root, "status", "--short")
        dirty = len([x for x in status.splitlines() if x.strip()])
        lines.append(f"\nGit: branch '{branch}', {dirty} uncommitted path(s).")
    except (OSError, subprocess.SubprocessError):
        pass
    print("\n".join(lines))


MODES = {
    "pre-bash": pre_bash,
    "pre-edit": pre_edit,
    "post-edit": post_edit,
    "session-start": session_start,
}


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode not in MODES:
        print(f"[pata-guard] unknown mode {mode!r}", file=sys.stderr)
        sys.exit(2)
    try:
        raw = sys.stdin.read()
        event = json.loads(raw) if raw.strip() else {}
        MODES[mode](event)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 — fail closed for guards
        if mode.startswith("pre"):
            block(
                f"guard error ({type(exc).__name__}: {exc}); failing closed. Tell the maintainer."
            )
        print(f"[pata-guard] non-blocking error: {exc}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
