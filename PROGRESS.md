# Progress

Update at every checkpoint. Record only commands that actually ran and their observed
results.

## Current objective

Make ADR-0006 (rev 5) and ADR-0007 (rev 3) acceptable. Blocker decisions are taken
one at a time, then written into one coordinated revision (ADR-0006 rev 6,
ADR-0007 rev 4). Tasks, edges and the ruling ledger:
[`docs/research/dependency-graph.md`](docs/research/dependency-graph.md).

## Repository state (2026-10-28)

- Branch `main`, tracking `origin/main`. At the last fetch, `origin/main` was
  `f5c5473`.
- Local commits not yet pushed before this checkpoint:
  - `114c54e` (ADR-0006 rev 5 / ADR-0007 rev 3)
  - `f18c35a` (T0)
  - `359b339` (T1 ledger)
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

## Failed attempts

- T2: a shell `node -e` edit script failed on quoting (bash syntax error) before
  writing anything. The edits were redone with the Edit tool.

## Open decisions

Each needs maintainer input. Accepting Blocker 8 resolves none of them.

- Blocker 9 (T3, READY)
- Blocker 5 (T4, READY)
- Blocker 4 (T5, READY)
- Blocker 6 (T6, READY)
- Blocker 10 (T7, READY)
- Blocker 3 (T8, BLOCKED on T6)
- Blocker 7 (T9, BLOCKED on T3–T8)
- Blocker 11 (T10). Its ordering part is BLOCKED on T9. The acceptance condition
  can be ruled at any time.

## Next action

**T3:** maintainer rulings on Blocker 9, the Layer D reliability method. No ADR
edits until T1–T10 are decided.
