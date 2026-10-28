# Progress

Update at every checkpoint. Record only commands that actually ran and their observed
results.

## Current objective

Make ADR-0006 (rev 5) and ADR-0007 (rev 3) acceptable. Blocker decisions are taken
one at a time, then written into one coordinated revision (ADR-0006 rev 6,
ADR-0007 rev 4). Tasks, edges and the ruling ledger:
[`docs/research/dependency-graph.md`](docs/research/dependency-graph.md).

## Repository state (2026-10-28)

- Branch `main`. Before this checkpoint: HEAD `114c54e`, one commit ahead of
  `origin/main` (ADR-0006 rev 5 / ADR-0007 rev 3, not pushed). Working tree clean.
- Accepted ADRs: 0001, 0002, 0004, 0005. Proposed: 0003 (permission pending), 0006,
  0007, 0008.
- No address source accepted. No datasets, models or benchmark results.

## Completed

- **T0, workflow setup.** Added `CLAUDE.md`, this file, and the dependency graph.
  No ADR or code changes.

## Verification (2026-10-28, before the T0 commit)

| Command | Result |
|---|---|
| `uv sync --locked` | resolved and checked 10 packages, exit 0 |
| `uv run ruff check .` | All checks passed |
| `uv run ruff format --check .` | 20 files already formatted |
| `uv run pytest` | 26 passed in 79 s |
| `git diff --cached --check` (T0 files staged) | no output, exit 0 |

## Failed attempts

None.

## Open decisions

- Blocker 2: R1f, R1g, R8b (T1).
- Blockers 3–11 (T2–T10).

Details are in the graph.

## Next action

**T1:** maintainer rulings on R1f, R1g and R8b. Once ruled, T2 (Blocker 8) becomes
READY. T4–T7 are also READY and need maintainer input. No ADR edits until T1–T10
are decided.
