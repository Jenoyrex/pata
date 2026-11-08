"""Smoke tests for .claude/hooks/pata_guard.py.

Feed real hook payloads, check exit codes.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
GUARD = ROOT / ".claude" / "hooks" / "pata_guard.py"


def run(mode: str, event: dict) -> subprocess.CompletedProcess:
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(ROOT)}
    return subprocess.run(
        [sys.executable, str(GUARD), mode],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
        check=False,
    )


def bash(cmd: str) -> dict:
    return {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": cmd},
        "cwd": str(ROOT),
    }


def edit(tool: str, path: str, text: str) -> dict:
    ti = {"file_path": str(ROOT / path)}
    if tool == "Write":
        ti["content"] = text
    else:
        ti["old_string"], ti["new_string"] = "x", text
    return {
        "hook_event_name": "PreToolUse",
        "tool_name": tool,
        "tool_input": ti,
        "cwd": str(ROOT),
    }


@pytest.mark.parametrize(
    "cmd",
    [
        "git push origin main",
        "git push",
        "git merge adr-0006-rev6",
        "git reset --hard HEAD~1",
        "git clean -fd",
        "git add -f data/raw/source.csv",
        "git add private/denylist.csv",
        "git add staging/split/frozen.manifest",
        "git commit --no-verify -m x",
        "gh pr merge 12",
        "uv run python scripts/graph.py approve G-ADR67 --by me --ref x",
        "rm -rf staging/split",
    ],
)
def test_bash_blocked(cmd):
    r = run("pre-bash", bash(cmd))
    assert r.returncode == 2, (cmd, r.stderr)
    assert "BLOCKED" in r.stderr


@pytest.mark.parametrize(
    "cmd",
    [
        "uv run pytest -q",
        "git status",
        "git diff main..adr-0006-rev6",
        "git add src/pata/ingest/decode.py tests/ingest/test_decode.py",
        "git commit -m 'feat(ingest): strict decoder'",
        "uv run python scripts/graph.py next",
        "ls data",
    ],
)
def test_bash_allowed(cmd):
    r = run("pre-bash", bash(cmd))
    assert r.returncode == 0, (cmd, r.stderr)


@pytest.mark.parametrize(
    "tool,path,text",
    [
        ("Write", "data/raw/x.csv", "a,b"),
        ("Write", "private/denylist.csv", "x"),
        ("Edit", ".claude/settings.json", "{}"),
        ("Edit", ".claude/hooks/pata_guard.py", "pass"),
        ("Edit", "docs/adr/0006-annotation.md", "Status: Accepted"),
        ("Edit", "docs/adr/0006-annotation.md", "**Status:** Accepted (2026-10-29)"),
        ("Edit", "docs/adr/0007-split.md", "- Status: accepted"),
        ("Edit", "workflow/graph.toml", '[[approval]]\nnode = "G-ADR67"'),
    ],
)
def test_edit_blocked(tool, path, text):
    r = run("pre-edit", edit(tool, path, text))
    assert r.returncode == 2, (path, text, r.stderr)


@pytest.mark.parametrize(
    "tool,path,text",
    [
        ("Edit", "docs/adr/0006-annotation.md", "Status: Proposed (rev 6)"),
        ("Edit", "workflow/graph.toml", 'status = "in_progress"'),
        ("Write", "docs/evidence/lgd/levels.md", "# LGD levels\nstate: UNVERIFIED"),
        ("Write", "src/pata/ingest/decode.py", "def decode(): ..."),
    ],
)
def test_edit_allowed(tool, path, text):
    r = run("pre-edit", edit(tool, path, text))
    assert r.returncode == 0, (path, r.stderr)


def test_post_edit_valid_graph_passes():
    ev = {
        "hook_event_name": "PostToolUse",
        "tool_name": "Edit",
        "tool_input": {"file_path": str(ROOT / "workflow" / "graph.toml")},
        "cwd": str(ROOT),
    }
    assert run("post-edit", ev).returncode == 0


def test_session_start_injects_context():
    r = run(
        "session-start",
        {"hook_event_name": "SessionStart", "source": "startup", "cwd": str(ROOT)},
    )
    assert r.returncode == 0
    assert "LOOP" in r.stdout and "READY" in r.stdout


def test_garbage_input_fails_closed():
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(ROOT)}
    r = subprocess.run(
        [sys.executable, str(GUARD), "pre-bash"],
        input="{not json",
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert r.returncode == 2


# ---------------------------------------------------------------- ADR protection
# Pata keeps decision records in docs/decisions/. The guard must judge the RESULT
# of an edit (status before vs after), not just the inserted text.

_gspec = importlib.util.spec_from_file_location("pata_guard", GUARD)
guard = importlib.util.module_from_spec(_gspec)
sys.modules["pata_guard"] = guard
_gspec.loader.exec_module(guard)

ADR_FORMATS = {
    "colon": "# ADR-0006\n\nStatus: Proposed\n\nBody.\n",
    "bold": "# ADR-0006\n\n**Status:** Proposed (rev 6)\n\nBody.\n",
    "bullet": "# ADR-0006\n\n- Status: Proposed\n\nBody.\n",
    "table": "# ADR-0006\n\n| Field | Value |\n|---|---|\n| Status | Proposed |\n",
    "heading": "# ADR-0006\n\n## Status\n\nProposed\n\n## Context\n\nAccepted ideas.\n",
    "frontmatter": "---\nid: 6\nstatus: proposed\n---\n# ADR-0006\n",
}


def adr_project(tmp_path: Path, text: str) -> Path:
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    f = d / "0006-annotation.md"
    f.write_text(text, encoding="utf-8")
    return f


def run_in(root: Path, mode: str, event: dict) -> subprocess.CompletedProcess:
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(root)}
    return subprocess.run(
        [sys.executable, str(GUARD), mode],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
        check=False,
    )


def ev(tool: str, path: Path, **ti) -> dict:
    return {"tool_name": tool, "tool_input": {"file_path": str(path), **ti}}


@pytest.mark.parametrize("fmt", sorted(ADR_FORMATS))
def test_word_only_edit_to_accepted_is_blocked(tmp_path, fmt):
    """The hole in v1: replacing just 'Proposed' with 'Accepted'."""
    text = ADR_FORMATS[fmt]
    f = adr_project(tmp_path, text)
    old = "proposed" if fmt == "frontmatter" else "Proposed"
    r = run_in(tmp_path, "pre-edit", ev("Edit", f, old_string=old, new_string="Accepted"))
    assert r.returncode == 2, (fmt, r.stderr)


@pytest.mark.parametrize("fmt", sorted(ADR_FORMATS))
def test_full_rewrite_to_accepted_is_blocked(tmp_path, fmt):
    text = ADR_FORMATS[fmt]
    f = adr_project(tmp_path, text)
    new = text.replace("Proposed", "Accepted").replace("proposed", "accepted")
    assert run_in(tmp_path, "pre-edit", ev("Write", f, content=new)).returncode == 2


def test_multiedit_to_accepted_is_blocked(tmp_path):
    f = adr_project(tmp_path, ADR_FORMATS["heading"])
    edits = [
        {"old_string": "Body", "new_string": "Body"},
        {"old_string": "Proposed", "new_string": "Accepted"},
    ]
    r = run_in(tmp_path, "pre-edit", ev("MultiEdit", f, edits=edits))
    assert r.returncode == 2


def test_adding_acceptance_record_is_blocked(tmp_path):
    f = adr_project(tmp_path, ADR_FORMATS["colon"])
    r = run_in(
        tmp_path,
        "pre-edit",
        ev(
            "Edit",
            f,
            old_string="Body.",
            new_string="Body.\n\nAccepted by Jenoy on 2026-10-29.",
        ),
    )
    assert r.returncode == 2


def test_new_adr_created_as_accepted_is_blocked(tmp_path):
    (tmp_path / "docs" / "decisions").mkdir(parents=True)
    f = tmp_path / "docs" / "decisions" / "0009-new.md"
    r = run_in(tmp_path, "pre-edit", ev("Write", f, content="# ADR-0009\n\nStatus: Accepted\n"))
    assert r.returncode == 2


@pytest.mark.parametrize(
    "old,new",
    [
        ("Body.", "Body, clarified. Reviewers accepted the wording change."),
        ("Proposed", "Proposed (rev 7)"),
    ],
)
def test_normal_adr_edits_allowed(tmp_path, old, new):
    f = adr_project(tmp_path, ADR_FORMATS["colon"])
    r = run_in(tmp_path, "pre-edit", ev("Edit", f, old_string=old, new_string=new))
    assert r.returncode == 0, r.stderr


def test_heading_format_body_mentioning_accepted_is_allowed(tmp_path):
    f = adr_project(tmp_path, ADR_FORMATS["heading"])
    r = run_in(
        tmp_path,
        "pre-edit",
        ev(
            "Edit",
            f,
            old_string="Accepted ideas.",
            new_string="Accepted ideas, revised.",
        ),
    )
    assert r.returncode == 0, r.stderr


def test_rm_decisions_folder_blocked():
    assert run("pre-bash", bash("rm -rf docs/decisions")).returncode == 2


# ---------------------------------------------------------------- real repository ADRs
REAL_ADRS = sorted(
    p
    for d in ("docs/decisions", "docs/adr")
    for p in (ROOT / d).glob("*.md")
    if p.name[:4].isdigit() or p.name.lower().startswith("adr")
)


@pytest.mark.skipif(not REAL_ADRS, reason="no decision records in this checkout")
@pytest.mark.parametrize("adr", REAL_ADRS, ids=lambda p: p.name)
def test_real_adr_status_is_understood_and_protected(adr):
    """Every real decision record must have a status the guard can read, and
    flipping a not-yet-accepted one to Accepted must be blocked."""
    text = adr.read_text(encoding="utf-8")
    status = guard.adr_status(text)
    assert status, f"guard cannot find a status line in {adr.name}; update STATUS_* regexes"
    if status.startswith("accepted"):
        pytest.skip(f"{adr.name} is already accepted")
    m = guard.STATUS_LINE.search(text) or guard.STATUS_HEADING.search(text)
    flipped = text[: m.start(1)] + "Accepted" + text[m.end(1) :]
    r = run(
        "pre-edit",
        {
            "tool_name": "Write",
            "tool_input": {"file_path": str(adr), "content": flipped},
        },
    )
    assert r.returncode == 2, f"{adr.name}: status flip was NOT blocked"
    old = m.group(1)
    r = run(
        "pre-edit",
        {
            "tool_name": "Edit",
            "tool_input": {
                "file_path": str(adr),
                "old_string": old,
                "new_string": "Accepted",
            },
        },
    )
    assert r.returncode == 2, f"{adr.name}: word-only status edit was NOT blocked"
