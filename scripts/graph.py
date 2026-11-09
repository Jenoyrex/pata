#!/usr/bin/env python3
"""Pata dependency-graph engine.

Stdlib only (Python >= 3.11, uses tomllib). Reads workflow/graph.toml.

Commands
  validate [--check-outputs]   structural + status + gate checks (exit 1 on error)
  next                         what can be worked on now, what waits on whom
  show ID                      one node, its deps, dependents and approval
  status                       per-phase overview
  critical                     longest remaining dependency chain to the release
  mermaid [--out FILE]         Mermaid flowchart (status-coloured)
  progress [--write FILE]      Markdown progress block (writes between markers)
  approve ID --by NAME --ref EVIDENCE [--date YYYY-MM-DD]
                               MAINTAINER ONLY: interactive, needs a real TTY
"""

from __future__ import annotations

import argparse
import datetime as dt
import glob
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

STATUSES = {"todo", "in_progress", "review", "blocked", "done", "dropped"}
KINDS = {"decision", "evidence", "spec", "impl", "human", "infra", "release"}
GATES = {"none", "maintainer"}
OWNERS = {"agent", "maintainer", "screener", "annotator"}
REQUIRED = ("id", "title", "phase", "kind", "status", "deps", "gate", "owner", "acceptance")
STARTED = {"in_progress", "review", "done"}
WIP_LIMIT_AGENT = 2

BEGIN = "<!-- graph:progress:begin -->"
END = "<!-- graph:progress:end -->"


def _today() -> dt.date:
    return dt.datetime.now().astimezone().date()


DEFAULT_GRAPH = Path(__file__).resolve().parent.parent / "workflow" / "graph.toml"


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


class Graph:
    def __init__(self, data: dict, root: Path):
        self.root = root
        self.raw = data
        self.nodes: dict[str, dict] = {}
        self.order: list[str] = []
        self._dupes: list[str] = []
        for n in data.get("node", []):
            nid = n.get("id", "<missing id>")
            if nid in self.nodes:
                self._dupes.append(nid)
            self.nodes[nid] = n
            self.order.append(nid)
        self.approvals: list[dict] = list(data.get("approval", []))

    # ------------------------------------------------------------ loading
    @classmethod
    def load(cls, path: Path) -> Graph:
        with path.open("rb") as fh:
            data = tomllib.load(fh)
        return cls(data, path.resolve().parent.parent)

    # ------------------------------------------------------------ queries
    def deps(self, nid: str) -> list[str]:
        return list(self.nodes[nid].get("deps", []))

    def dependents(self, nid: str) -> list[str]:
        return [o for o in self.order if nid in self.nodes[o].get("deps", [])]

    def status(self, nid: str) -> str:
        return self.nodes[nid]["status"]

    def approval_for(self, nid: str) -> dict | None:
        for a in self.approvals:
            if a.get("node") == nid:
                return a
        return None

    def deps_done(self, nid: str) -> bool:
        return all(self.nodes.get(d, {}).get("status") == "done" for d in self.deps(nid))

    def ready(self) -> list[str]:
        return [n for n in self.order if self.status(n) == "todo" and self.deps_done(n)]

    def waiting(self) -> list[tuple[str, list[str]]]:
        out = []
        for n in self.order:
            if self.status(n) in {"todo", "blocked"} and not self.deps_done(n):
                missing = [d for d in self.deps(n) if self.nodes.get(d, {}).get("status") != "done"]
                out.append((n, missing))
        return out

    def topo(self) -> list[str]:
        indeg = {n: 0 for n in self.order}
        for n in self.order:
            for d in self.deps(n):
                if d in indeg:
                    indeg[n] += 1
        queue = [n for n in self.order if indeg[n] == 0]
        out: list[str] = []
        while queue:
            n = queue.pop(0)
            out.append(n)
            for m in self.dependents(n):
                indeg[m] -= 1
                if indeg[m] == 0:
                    queue.append(m)
        return out

    def find_cycle(self) -> list[str] | None:
        WHITE, GREY, BLACK = 0, 1, 2
        color = {n: WHITE for n in self.order}
        stack: list[str] = []

        def dfs(n: str) -> list[str] | None:
            color[n] = GREY
            stack.append(n)
            for d in self.deps(n):
                if d not in color:
                    continue
                if color[d] == GREY:
                    return stack[stack.index(d) :] + [d]
                if color[d] == WHITE:
                    found = dfs(d)
                    if found:
                        return found
            stack.pop()
            color[n] = BLACK
            return None

        for n in self.order:
            if color[n] == WHITE:
                found = dfs(n)
                if found:
                    return found
        return None

    def critical_path(self) -> list[str]:
        """Longest chain of not-done nodes (by count) ending anywhere."""
        open_nodes = [n for n in self.topo() if self.status(n) not in {"done", "dropped"}]
        best: dict[str, list[str]] = {}
        for n in open_nodes:
            prev = [best[d] for d in self.deps(n) if d in best]
            chain = max(prev, key=len) if prev else []
            best[n] = chain + [n]
        return max(best.values(), key=len) if best else []

    # ------------------------------------------------------------ validation
    def validate(self, check_outputs: bool = False) -> Report:
        r = Report()
        for d in self._dupes:
            r.errors.append(f"duplicate node id: {d}")
        for nid in self.order:
            n = self.nodes[nid]
            for key in REQUIRED:
                if key not in n:
                    r.errors.append(f"{nid}: missing field '{key}'")
            if n.get("status") not in STATUSES:
                r.errors.append(f"{nid}: bad status {n.get('status')!r}")
            if n.get("kind") not in KINDS:
                r.errors.append(f"{nid}: bad kind {n.get('kind')!r}")
            if n.get("gate") not in GATES:
                r.errors.append(f"{nid}: bad gate {n.get('gate')!r}")
            if n.get("owner") not in OWNERS:
                r.errors.append(f"{nid}: bad owner {n.get('owner')!r}")
            if not n.get("acceptance"):
                r.errors.append(f"{nid}: acceptance criteria must not be empty")
            for d in n.get("deps", []):
                if d == nid:
                    r.errors.append(f"{nid}: depends on itself")
                elif d not in self.nodes:
                    r.errors.append(f"{nid}: unknown dep '{d}'")
            if n.get("status") == "blocked" and not n.get("blocker"):
                r.errors.append(f"{nid}: status 'blocked' needs a 'blocker' explanation")
            if n.get("irreversible") and n.get("gate") != "maintainer":
                r.errors.append(f"{nid}: irreversible nodes must have gate = 'maintainer'")

        cyc = self.find_cycle()
        if cyc:
            r.errors.append("dependency cycle: " + " -> ".join(cyc))

        if r.errors:  # status checks assume structure is sane
            return r

        for nid in self.order:
            n = self.nodes[nid]
            st = n["status"]
            if st in STARTED and not self.deps_done(nid):
                missing = [d for d in self.deps(nid) if self.status(d) != "done"]
                r.errors.append(f"{nid}: status '{st}' but deps not done: {', '.join(missing)}")
            if n["gate"] == "maintainer" and st == "done" and not self.approval_for(nid):
                r.errors.append(
                    f"{nid}: maintainer-gated node is 'done' without an [[approval]] entry"
                )

        seen: set[str] = set()
        for a in self.approvals:
            node = a.get("node")
            if node not in self.nodes:
                r.errors.append(f"approval for unknown node {node!r}")
                continue
            if node in seen:
                r.errors.append(f"duplicate approval for {node}")
            seen.add(node)
            if self.nodes[node]["gate"] != "maintainer":
                r.warnings.append(f"approval recorded for non-gated node {node}")
            for key in ("by", "date", "ref"):
                if not a.get(key):
                    r.errors.append(f"approval for {node}: missing '{key}'")
            try:
                dt.date.fromisoformat(str(a.get("date", "")))
            except ValueError:
                r.errors.append(f"approval for {node}: date must be YYYY-MM-DD")

        wip = [
            n
            for n in self.order
            if self.status(n) == "in_progress" and self.nodes[n]["owner"] == "agent"
        ]
        if len(wip) > WIP_LIMIT_AGENT:
            r.warnings.append(
                f"{len(wip)} agent tasks in progress (limit {WIP_LIMIT_AGENT}): {', '.join(wip)}"
            )

        if check_outputs:
            for nid in self.order:
                n = self.nodes[nid]
                if n["status"] != "done":
                    continue
                for out in n.get("outputs", []):
                    path = out.split(" (", 1)[0]  # "path (note)" still declares a path
                    if "outside Git" in out or " " in path:
                        continue
                    if not glob.glob(str(self.root / path)):
                        r.warnings.append(f"{nid}: declared output not found: {out}")
        return r

    # ------------------------------------------------------------ rendering
    def progress_markdown(self) -> str:
        total = [n for n in self.order if self.status(n) != "dropped"]
        done = [n for n in total if self.status(n) == "done"]
        lines = [
            BEGIN,
            f"_Generated from `workflow/graph.toml` on {_today().isoformat()}"
            " — do not edit by hand._",
            "",
            (
                f"**Graph nodes done:** {len(done)}/{len(total)} "
                "(node count, not effort; design nodes ≠ implementation)."
            ),
            "",
            "| Phase | Node | Status | Gate | Waiting on |",
            "|---|---|---|---|---|",
        ]
        for nid in self.order:
            n = self.nodes[nid]
            waiting = ", ".join(d for d in self.deps(nid) if self.status(d) != "done") or "—"
            gate = (
                "maintainer" + (" · irreversible" if n.get("irreversible") else "")
                if n["gate"] == "maintainer"
                else "—"
            )
            lines.append(
                f"| {n['phase']} | **{nid}** {n['title']} | {n['status']} | {gate} | {waiting} |"
            )
        ready = self.ready()
        lines += [
            "",
            "**Ready now:** "
            + (", ".join(ready) if ready else "nothing — see gates awaiting the maintainer"),
        ]
        reviews = [n for n in self.order if self.status(n) == "review"]
        if reviews:
            lines.append("**Awaiting maintainer:** " + ", ".join(reviews))
        lines.append(END)
        return "\n".join(lines)

    def mermaid(self) -> str:
        cls = {
            "done": "done",
            "in_progress": "doing",
            "review": "review",
            "blocked": "blocked",
            "todo": "todo",
            "dropped": "dropped",
        }
        out = ["flowchart LR"]
        phases: dict[str, list[str]] = {}
        for nid in self.order:
            phases.setdefault(self.nodes[nid]["phase"], []).append(nid)
        for ph, ids in phases.items():
            out.append(f'  subgraph {ph.replace("-", "_")}["{ph}"]')
            for nid in ids:
                n = self.nodes[nid]
                label = n["title"].replace('"', "'")
                if len(label) > 48:
                    label = label[:45] + "..."
                shape = ('{{"', '"}}') if n["gate"] == "maintainer" else ('["', '"]')
                safe = nid.replace("-", "_")
                out.append(f"    {safe}{shape[0]}{nid}<br/>{label}{shape[1]}:::{cls[n['status']]}")
            out.append("  end")
        for nid in self.order:
            for d in self.deps(nid):
                out.append(f"  {d.replace('-', '_')} --> {nid.replace('-', '_')}")
        out += [
            "  classDef done fill:#e8f7ef,stroke:#177245,color:#0b3d24",
            "  classDef doing fill:#eaf1ff,stroke:#244b8f,color:#10264d",
            "  classDef review fill:#fff4d8,stroke:#8a5700,color:#4a2f00",
            "  classDef blocked fill:#fff0f0,stroke:#9f2f2f,color:#5a1414",
            "  classDef todo fill:#ffffff,stroke:#8a96a8,color:#172033",
            "  classDef dropped fill:#eeeeee,stroke:#aaaaaa,color:#777777",
        ]
        return "\n".join(out)


# ---------------------------------------------------------------- CLI
def _print_report(r: Report) -> None:
    for e in r.errors:
        print(f"ERROR   {e}")
    for w in r.warnings:
        print(f"WARN    {w}")
    print("graph OK" if r.ok else f"graph INVALID ({len(r.errors)} error(s))")


def cmd_next(g: Graph) -> None:
    def line(nid: str) -> str:
        n = g.nodes[nid]
        tags = [n["owner"]]
        if n["gate"] == "maintainer":
            tags.append("gate")
        if n.get("irreversible"):
            tags.append("IRREVERSIBLE: ask before running")
        return f"  {nid:<12} {n['title']}  [{', '.join(tags)}]"

    sections = [
        ("IN PROGRESS", [n for n in g.order if g.status(n) == "in_progress"]),
        ("AWAITING MAINTAINER (review)", [n for n in g.order if g.status(n) == "review"]),
        ("READY (all deps done)", g.ready()),
    ]
    for title, ids in sections:
        print(f"{title}:")
        print("\n".join(line(n) for n in ids) if ids else "  —")
    blocked = [n for n in g.order if g.status(n) == "blocked"]
    if blocked:
        print("BLOCKED:")
        for n in blocked:
            print(f"  {n:<12} {g.nodes[n].get('blocker', '')}")
    agent_ready = [n for n in g.ready() if g.nodes[n]["owner"] == "agent"]
    print()
    if agent_ready:
        print(f"Suggested next agent task: {agent_ready[0]}  (run /loop {agent_ready[0]})")
    else:
        print("No agent task is ready. Progress depends on maintainer/human nodes above.")


def cmd_show(g: Graph, nid: str) -> int:
    if nid not in g.nodes:
        print(f"unknown node {nid}")
        return 1
    n = g.nodes[nid]
    print(f"{nid} — {n['title']}")
    for key in ("phase", "kind", "status", "gate", "owner", "irreversible", "blocker"):
        if key in n:
            print(f"  {key:<12} {n[key]}")
    print("  deps        " + (", ".join(f"{d}({g.status(d)})" for d in g.deps(nid)) or "—"))
    print("  unblocks    " + (", ".join(g.dependents(nid)) or "—"))
    print("  outputs:")
    for o in n.get("outputs", []):
        print(f"    - {o}")
    print("  acceptance:")
    for a in n["acceptance"]:
        print(f"    [ ] {a}")
    for v in n.get("verify", []):
        print(f"  verify      {v}")
    if n.get("notes"):
        print(f"  notes       {n['notes']}")
    ap = g.approval_for(nid)
    if ap:
        print(f"  APPROVED    by {ap['by']} on {ap['date']} — {ap['ref']}")
    return 0


def cmd_status(g: Graph) -> None:
    phases: dict[str, dict[str, int]] = {}
    for nid in g.order:
        n = g.nodes[nid]
        phases.setdefault(n["phase"], {}).setdefault(n["status"], 0)
        phases[n["phase"]][n["status"]] += 1
    for ph, counts in sorted(phases.items()):
        total = sum(counts.values())
        done = counts.get("done", 0)
        bar = "#" * done + "." * (total - done)
        detail = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
        print(f"{ph:<16} [{bar}] {done}/{total}  ({detail})")


def cmd_progress(g: Graph, write: str | None) -> None:
    block = g.progress_markdown()
    if not write:
        print(block)
        return
    path = Path(write)
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if BEGIN in text and END in text:
        head, rest = text.split(BEGIN, 1)
        _, tail = rest.split(END, 1)
        text = head + block + tail
    else:
        text = (
            (text.rstrip() + "\n\n" if text else "")
            + "## Dependency graph status\n\n"
            + block
            + "\n"
        )
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"updated {path}")


def cmd_approve(g: Graph, graph_path: Path, nid: str, by: str, ref: str, date: str | None) -> int:
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        print("approve must be run by the maintainer in an interactive terminal.", file=sys.stderr)
        return 2
    if nid not in g.nodes:
        print(f"unknown node {nid}", file=sys.stderr)
        return 1
    n = g.nodes[nid]
    if n["gate"] != "maintainer":
        print(f"{nid} is not maintainer-gated; nothing to approve.", file=sys.stderr)
        return 1
    if g.approval_for(nid):
        print(f"{nid} already approved.", file=sys.stderr)
        return 1
    if not g.deps_done(nid):
        print(f"{nid}: deps not done — cannot approve yet.", file=sys.stderr)
        return 1
    date = date or _today().isoformat()
    dt.date.fromisoformat(date)
    print(f"{nid}: {n['title']}")
    for a in n["acceptance"]:
        print(f"  [ ] {a}")
    typed = input(f"Type 'APPROVE {nid}' to record approval by {by} on {date}: ")
    if typed.strip() != f"APPROVE {nid}":
        print("not approved.")
        return 1

    def esc(s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"')

    block = (
        f'\n[[approval]]\nnode = "{nid}"\nby = "{esc(by)}"\ndate = "{date}"\nref = "{esc(ref)}"\n'
    )
    with graph_path.open("a", encoding="utf-8") as fh:
        fh.write(block)
    print(f'approval recorded. Now set {nid} status = "done" (or ask Claude to) and run validate.')
    return 0


def main(argv: list[str] | None = None) -> int:
    # A Windows console or pipe may be cp1252, which cannot encode symbols such as "≠".
    sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser(
        prog="graph.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--graph", default=str(DEFAULT_GRAPH))
    sub = p.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate")
    v.add_argument("--check-outputs", action="store_true")
    sub.add_parser("next")
    s = sub.add_parser("show")
    s.add_argument("id")
    sub.add_parser("status")
    sub.add_parser("critical")
    m = sub.add_parser("mermaid")
    m.add_argument("--out")
    pr = sub.add_parser("progress")
    pr.add_argument("--write")
    a = sub.add_parser("approve")
    a.add_argument("id")
    a.add_argument("--by", required=True)
    a.add_argument("--ref", required=True)
    a.add_argument("--date")
    args = p.parse_args(argv)

    graph_path = Path(args.graph)
    try:
        g = Graph.load(graph_path)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        print(f"ERROR   cannot load {graph_path}: {exc}")
        return 1

    if args.cmd == "validate":
        r = g.validate(check_outputs=args.check_outputs)
        _print_report(r)
        return 0 if r.ok else 1
    # every other command refuses to reason over an invalid graph
    r = g.validate()
    if not r.ok:
        _print_report(r)
        return 1
    if args.cmd == "next":
        cmd_next(g)
    elif args.cmd == "show":
        return cmd_show(g, args.id)
    elif args.cmd == "status":
        cmd_status(g)
    elif args.cmd == "critical":
        chain = g.critical_path()
        print(f"{len(chain)} open nodes on the longest chain:")
        print("  " + "\n  -> ".join(f"{c} ({g.status(c)})" for c in chain))
    elif args.cmd == "mermaid":
        text = g.mermaid()
        if args.out:
            Path(args.out).write_text(text + "\n", encoding="utf-8")
            print(f"wrote {args.out}")
        else:
            print(text)
    elif args.cmd == "progress":
        cmd_progress(g, args.write)
    elif args.cmd == "approve":
        return cmd_approve(g, graph_path, args.id, args.by, args.ref, args.date)
    return 0


if __name__ == "__main__":
    sys.exit(main())
