---
description: Run one full LOOP (Load → Outline → Operate → Prove → Record) on one graph node
argument-hint: "[NODE-ID]  (omit to take the next ready agent node)"
---

Run exactly one LOOP iteration following `docs/workflow/LOOP.md`. Target node: `$ARGUMENTS`
(if empty, pick per LOOP §L step 3).

**L — Load**
1. Run `uv run python scripts/graph.py next`, `git status --short`, `git branch --show-current`.
2. Read the last entry of `PROGRESS.md`.
3. Run `uv run python scripts/graph.py show <ID>`.
4. STOP and report instead of continuing if: any dep is not done; owner is not `agent`;
   node is `irreversible` and I have not said "go <ID>" in this conversation.

**O — Outline**
5. Create `docs/workflow/cards/<ID>.md` from `docs/workflow/templates/task-card.md`.
   Map every acceptance criterion (verbatim) to a concrete proof.
6. Create branch `node/<ID>-<short-slug>` and set the node `status = "in_progress"` in `workflow/graph.toml`.
7. Show me the plan + acceptance→proof map in 10 lines or fewer. If it touches ADR meaning,
   sources, split config or schema vocabulary, WAIT for my reply; otherwise continue.

**O — Operate**
8. Do the work in small commits-worth of steps. impl: test first. evidence: use
   `docs/workflow/templates/evidence-record.md`, every claim sourced and dated; CAPTCHA/403 → log + ask me.
9. New work found → `/add-node`, don't expand scope.

**P — Prove**
10. Run the node's `verify` commands and the standard checks (ruff check, ruff format --check,
    pytest, `graph.py validate --check-outputs`, `git diff --check`). Paste real output into the card.
11. Invoke the `verifier` subagent with the node ID and card path. Any FAIL/UNPROVEN → fix and re-prove.

**⟲ Record**
12. Set status: `done` (gate none + all PASS) / `review` (maintainer gate) / `blocked` (+ blocker).
13. `uv run python scripts/graph.py progress --write PROGRESS.md`; append a session entry
    (`docs/workflow/templates/session-log.md`).
14. Commit on the node branch. Do not push or merge.
15. Final report to me: result, proof summary, verifier verdict, what's ready now, what needs me.
