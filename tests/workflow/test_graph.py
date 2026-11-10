"""Tests for scripts/graph.py — the workflow graph is code, so it gets tests."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("pata_graph", ROOT / "scripts" / "graph.py")
graph = importlib.util.module_from_spec(_spec)
sys.modules["pata_graph"] = graph  # dataclasses need the module registered
_spec.loader.exec_module(graph)


def node(nid, deps=(), status="todo", gate="none", **extra):
    base = {
        "id": nid,
        "title": nid,
        "phase": "P0",
        "kind": "impl",
        "status": status,
        "deps": list(deps),
        "gate": gate,
        "owner": "agent",
        "acceptance": ["x"],
    }
    base.update(extra)
    return base


def make(nodes, approvals=()):
    return graph.Graph({"node": nodes, "approval": list(approvals)}, ROOT)


# ------------------------------------------------------------ real graph
def test_project_graph_is_valid():
    g = graph.Graph.load(ROOT / "workflow" / "graph.toml")
    r = g.validate()
    assert r.ok, r.errors


def test_project_graph_toml_parses():
    with (ROOT / "workflow" / "graph.toml").open("rb") as fh:
        assert tomllib.load(fh)["project"] == "pata"


def test_project_graph_t12_waits_on_adr_gate():
    g = graph.Graph.load(ROOT / "workflow" / "graph.toml")
    assert "G-ADR67" in g.deps("T12")
    assert "T12" not in g.ready()


def ancestors(g, nid, skip=()):
    seen, stack = set(), [nid]
    while stack:
        for d in g.deps(stack.pop()):
            if d not in seen and d not in skip:
                seen.add(d)
                stack.append(d)
    return seen


# Legacy T12 ("follow-up implementation") was dropped in W0; these nodes carry its scope.
T12_SCOPE = (
    "D-SCHEMA",
    "U-UNICODE",
    "I-INGEST",
    "I-SPLITKEY",
    "I-RULESCREEN",
    "H-SCREEN",
    "I-TABLES",
    "I-RESOLVE",
    "I-VALIDATOR",
)


def test_t12_scope_waits_on_adr_gate_without_t12():
    g = graph.Graph.load(ROOT / "workflow" / "graph.toml")
    for nid in T12_SCOPE:
        assert "G-ADR67" in ancestors(g, nid, skip={"T12"}), nid


def test_t12_dropped_and_blocks_nothing():
    g = graph.Graph.load(ROOT / "workflow" / "graph.toml")
    assert g.status("T12") == "dropped"
    assert g.dependents("T12") == []


def test_validator_after_guidelines_freeze():
    g = graph.Graph.load(ROOT / "workflow" / "graph.toml")
    assert {"D-GUIDE", "D-SCHEMA", "X-FREEZE"} <= ancestors(g, "I-VALIDATOR")


def test_adr_outputs_point_at_real_decision_records():
    g = graph.Graph.load(ROOT / "workflow" / "graph.toml")
    outs = [o for nid in g.order for o in g.nodes[nid].get("outputs", [])]
    assert not [o for o in outs if o.startswith("docs/adr")]
    for nid in ("G-ADR67", "G-ADR8"):
        for out in g.nodes[nid]["outputs"]:
            assert (ROOT / out).is_file(), out


def test_selection_records_wait_on_adr0008():
    g = graph.Graph.load(ROOT / "workflow" / "graph.toml")
    assert "G-ADR8" in g.deps("I-SPLITKEY")


def test_freeze_before_human_screen_and_irreversible():
    g = graph.Graph.load(ROOT / "workflow" / "graph.toml")
    assert "X-FREEZE" in g.deps("H-SCREEN")
    assert g.nodes["X-FREEZE"].get("irreversible") is True


# ------------------------------------------------------------ structure
def test_cycle_detected():
    r = make([node("A", ["B"]), node("B", ["A"])]).validate()
    assert any("cycle" in e for e in r.errors)


def test_unknown_dep():
    r = make([node("A", ["NOPE"])]).validate()
    assert any("unknown dep" in e for e in r.errors)


def test_duplicate_id():
    r = make([node("A"), node("A")]).validate()
    assert any("duplicate node id" in e for e in r.errors)


def test_empty_acceptance_rejected():
    r = make([node("A", acceptance=[])]).validate()
    assert any("acceptance" in e for e in r.errors)


def test_bad_enum_rejected():
    r = make([node("A", status="finished")]).validate()
    assert any("bad status" in e for e in r.errors)


# ------------------------------------------------------------ status rules
@pytest.mark.parametrize("st", ["in_progress", "review", "done"])
def test_cannot_start_before_deps_done(st):
    r = make([node("A"), node("B", ["A"], status=st)]).validate()
    assert any("deps not done" in e for e in r.errors)


def test_blocked_needs_reason():
    r = make([node("A", status="blocked")]).validate()
    assert any("blocker" in e for e in r.errors)


def test_irreversible_requires_gate():
    r = make([node("A", irreversible=True)]).validate()
    assert any("irreversible" in e for e in r.errors)


# ------------------------------------------------------------ gates
def test_gated_done_without_approval_fails():
    r = make([node("G", gate="maintainer", status="done")]).validate()
    assert any("without an [[approval]]" in e for e in r.errors)


def test_gated_done_with_approval_passes():
    ap = {"node": "G", "by": "maint", "date": "2026-10-29", "ref": "ADR §Status"}
    r = make([node("G", gate="maintainer", status="done")], [ap]).validate()
    assert r.ok, r.errors


def test_approval_bad_date():
    ap = {"node": "G", "by": "m", "date": "29/10/2026", "ref": "r"}
    r = make([node("G", gate="maintainer", status="done")], [ap]).validate()
    assert any("YYYY-MM-DD" in e for e in r.errors)


def test_approve_refuses_without_tty(tmp_path, monkeypatch):
    p = tmp_path / "workflow" / "graph.toml"
    p.parent.mkdir()
    p.write_text(
        'schema_version = 1\nproject = "t"\n[[node]]\nid = "G"\ntitle = "g"\nphase = "P0"\n'
        'kind = "decision"\nstatus = "review"\ndeps = []\n'
        'gate = "maintainer"\nowner = "maintainer"\n'
        'acceptance = ["x"]\n',
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.stdin.isatty", lambda: False)
    rc = graph.main(["--graph", str(p), "approve", "G", "--by", "agent", "--ref", "fake"])
    assert rc == 2
    assert "[[approval]]" not in p.read_text(encoding="utf-8")


# ------------------------------------------------------------ scheduling
def test_ready_and_critical_path():
    g = make(
        [
            node("A", status="done"),
            node("B", ["A"]),
            node("C", ["B"]),
            node("D", ["A"]),
        ]
    )
    assert g.ready() == ["B", "D"]
    assert g.critical_path() == ["B", "C"]


def test_progress_block_is_replaced_in_place(tmp_path):
    g = make([node("A")])
    f = tmp_path / "PROGRESS.md"
    f.write_text(f"# Log\nkeep me\n{graph.BEGIN}\nold\n{graph.END}\ntail\n", encoding="utf-8")
    graph.cmd_progress(g, str(f))
    text = f.read_text(encoding="utf-8")
    assert "keep me" in text and "tail" in text and "old" not in text
    assert text.count(graph.BEGIN) == 1


def test_progress_write_uses_lf_line_endings(tmp_path):
    f = tmp_path / "PROGRESS.md"
    f.write_text(f"{graph.BEGIN}\nold\n{graph.END}\n", encoding="utf-8")
    graph.cmd_progress(make([node("A")]), str(f))
    assert b"\r\n" not in f.read_bytes()


def test_cli_survives_stdout_that_cannot_encode_its_symbols():
    env = {**os.environ, "PYTHONIOENCODING": "cp1252"}
    run = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "graph.py"), "progress"],
        capture_output=True,
        env=env,
        cwd=ROOT,
    )
    assert run.returncode == 0, run.stderr.decode("utf-8", "replace")


def test_check_outputs_sees_a_path_with_a_note():
    g = make([node("A", status="done", outputs=["no/such/file.txt (git-ignored; a note)"])])
    assert any("no/such/file.txt" in w for w in g.validate(check_outputs=True).warnings)


def test_check_outputs_ignores_prose_and_outside_git_outputs():
    outputs = ["a manifest under no/such/ (name UNDECIDED)", "private/denylist (outside Git)"]
    g = make([node("A", status="done", outputs=outputs)])
    assert g.validate(check_outputs=True).warnings == []


@pytest.mark.parametrize(
    ("nid", "ruled_item"),
    [("G-SRC", "eligibility"), ("D-SRCADR", "raw_text_scope"), ("D-SRCADR", "record_id_scope")]
    + [("X-FREEZE", "D4.5"), ("X-FREEZE", "steps 2-5"), ("X-FREEZE", "after step 5")]
    + [("I-SPLITKEY", "newly place"), ("I-SPLITKEY-CODE", "newly place")]
    + [("H-SCREEN", "source_record_ref"), ("H-SCREENER", "must not annotate")]
    + [("G-ADR67", "S7,S8"), ("E-FIELD", "ADR-0006 section 2 exception")],
)
def test_ruled_obligations_have_an_acceptance_row(nid, ruled_item):
    g = graph.Graph.load(ROOT / "workflow" / "graph.toml")
    assert any(ruled_item in a for a in g.nodes[nid]["acceptance"])
