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
- **T3–T7 analysis (2026-10-28), none VERIFIED.**
  - For each task the graph now records facts, specs derived from approved rules,
    and decision requests D3.1–D7.3. All five are BLOCKED on maintainer decisions.
  - The T5 bucket mapping is fully specified, with synthetic test vectors.
  - The T6 decoding rules are specified.
  - Finding: the publishers' documented "NA" markers conflict with the "has a
    value" rule (D4.4).
  - No file-level evidence exists for any source field (B6), so T6 eligibility stays
    pending per source.

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

Each needs maintainer input. Accepting Blocker 8 resolves none of them.

- Blocker 9 (T3, BLOCKED: D3.1–D3.3)
- Blocker 5 (T4, BLOCKED: D4.1–D4.5)
- Blocker 4 (T5, BLOCKED: D5.1, D5.2; decide D5.1 with D7.1)
- Blocker 6 (T6, BLOCKED: D6.1, D6.2, D4.4)
- Blocker 10 (T7, BLOCKED: D7.1–D7.3)
- Blocker 3 (T8, BLOCKED on T6)
- Blocker 7 (T9, BLOCKED on T3–T8)
- Blocker 11 (T10). Its ordering part is BLOCKED on T9. The acceptance condition
  can be ruled at any time.

## Next action

**Maintainer rulings on D3.1–D7.3**, in the graph's "T3–T7 workstream" section.
No task is READY for agent work until then. No ADR edits until T1–T10 are decided.
