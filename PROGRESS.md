# Progress

Update at every checkpoint. Record only commands that actually ran and their observed
results.

## Current objective

Make ADR-0006 (rev 5) and ADR-0007 (rev 3) acceptable. Blocker decisions are taken
one at a time, then written into one coordinated revision (ADR-0006 rev 6,
ADR-0007 rev 4). Tasks, edges and the ruling ledger:
[`docs/research/dependency-graph.md`](docs/research/dependency-graph.md).

## Repository state (2026-10-28)

- Branch `main`, tracking `origin/main`. Pushed 2026-10-28: `origin/main` =
  `067aad3` (it includes `114c54e`, `f18c35a`, `359b339`). Verified by fetch at the
  start of the T3–T7 run.
- Accepted ADRs: 0001, 0002, 0004, 0005. Proposed: 0003 (permission pending), 0006,
  0007, 0008.
- No address source accepted. No datasets, models or benchmark results.

## Completed

- **T0, workflow setup.** Added `CLAUDE.md`, this file, and the dependency graph.
  Commit `f18c35a`.
- **T1, Blocker 2: VERIFIED.** All Blocker 2 rulings are recorded in the graph
  ledger, including R1f (a), R1g (yes) and R8b (accepted), with a check against the
  ADR text. Commit `359b339`.
- **T2, Blocker 8: VERIFIED.** All ten defaults (8.1–8.10) were accepted and
  recorded.
  - The consistency check with R1f, Layer D and §14 found no contradiction.
  - The derived consequences are listed in the graph.
- None of the Blocker 1, 2 or 8 rulings is **incorporated into the ADRs** yet. That
  happens in T11, after every blocker is decided.
- **T3–T7 analysis.** Commit `2858a73`: facts, specs and decision requests
  D3.1–D7.3.
- **T3–T7 rulings (2026-10-28).**
  - The maintainer accepted every D, with explicit wording for D4.4.
  - Checking against the ADR text found one conflict. D7.1 (human screening after
    the split) contradicts **ADR-0001 §2 (Accepted)**: personal identifiers "are
    removed during ingestion, before anything is written to `data/processed/`".
    D7.1 is therefore **not recorded**. Options are listed as D7.1′.
  - **T3, T4, T5, T6 VERIFIED** against their criteria.
  - **T7 BLOCKED** on D7.1′.
  - **T8 READY**: its prerequisites, T6 and Blocker 1, are met.
  - No file-level evidence exists for any source field (B6), so per-source
    eligibility stays pending. This isn't a T6 criterion.

## Verification

| Date / checkpoint | Command | Result |
|---|---|---|
| 2026-10-28, T0 | `uv sync --locked` | 10 packages checked, exit 0 |
| | `uv run ruff check .` | All checks passed |
| | `uv run ruff format --check .` | 20 files already formatted |
| | `uv run pytest` | 26 passed in 79 s |
| | `git diff --cached --check` | no output, exit 0 |
| 2026-10-28, T1 | `git diff --check` | no output, exit 0 |
| 2026-10-28, T2 | `uv sync --locked` | 10 packages checked, exit 0 |
| | `uv run ruff check .` | All checks passed, exit 0 |
| | `uv run ruff format --check .` | 23 files already formatted, exit 0. Ruff includes `.md` files; the 3 workflow files account for 20 → 23. |
| | `uv run pytest` | 26 passed in 78.9 s, exit 0 |
| 2026-10-28, T3–T7 | `uv run python -I` (scratch vector script) | 6 vectors + 6 boundaries printed; asserts ok, exit 0 |
| | `git diff --check` | no output, exit 0 |
| | `uv run ruff format --check .` | 23 files already formatted, exit 0 |
| | `uv run ruff check .` | All checks passed, exit 0 |
| | `uv run pytest` | not rerun (docs-only change) |
| 2026-10-28, T3–T7 rulings | `git diff --check` | no output, exit 0 |
| | `uv run ruff format --check .` | 23 files already formatted, exit 0 |
| | `uv run ruff check .` | All checks passed, exit 0 |
| | status audit (grep of the graph table and per-task status lines) | T0–T6 VERIFIED, T7 BLOCKED, T8 READY, T9–T12 BLOCKED; no stale or contradictory lines |

## Failed attempts

- T2: a shell `node -e` edit script failed on quoting (bash syntax error) before
  writing anything. The edits were redone with the Edit tool.
- T3–T7, three shell problems:
  - A stray `cat >` waited on stdin and hung the vector command. It was stopped,
    and the script was rewritten with the Write tool.
  - A long `cat >> ... <<'EOF'` append failed with a bash quoting error and wrote
    nothing.
  - Both appends were redone with the Edit tool.
  - Lesson: write file content with Write or Edit, never shell heredocs, in this
    environment.

## Open decisions

Each needs maintainer input.

- Blocker 10 (T7, BLOCKED: D7.1′, the conflict with ADR-0001 §2; staging
  recommended)
- Blocker 3 (T8, READY: denylist option, cascade to the duplicate class, errata
  location; coordinate with D7.1′)
- Blocker 7 (T9, BLOCKED on T7 and T8)
- Blocker 11 (T10). Its ordering part is BLOCKED on T9. The acceptance condition
  can be ruled at any time.

## Next action

**Maintainer ruling on D7.1′** (graph, "T3–T7 rulings"). T8 is READY to be written
up as a decision request; whether withdrawals happen inside the staging area
depends on D7.1′. No ADR edits until T1–T10 are decided.
