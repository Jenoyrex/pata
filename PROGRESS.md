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
  - T7 was blocked on D7.1′. Commit `0f3dc19`.
- **D7.1′ (a), staging, approved (2026-10-28).**
  - Order: rules-only screen, then the split frozen in an ignored staging area
    (`data/interim/`), then a role-restricted human screen, then only passing
    records written to `data/processed/`.
  - Checked against ADR-0001 §2, ADR-0006 §12 and §17, ADR-0007 §3 and §5, D5.1,
    D7.3, Blocker 1 and Blockers 2/8: no conflicts.
  - **T7 VERIFIED.**
  - New coupling: human-screen exclusions aren't reproducible on rebuild, so T8's
    denylist must cover them.
- T8 decision requests D8.1–D8.4 prepared. Commit `6ae0221`.
- **T8 rulings (2026-10-28): D8.1–D8.4 accepted as recorded.**
  - Checked against ADR-0001–0008, Blockers 1, 2 and 8, D5.1, D7.1′ and fixed
    assignment: no conflicts.
  - Derived:
    - the §13 deletion exception
    - denylist matching on all three fields
    - a documented limitation for new snapshots and duplicates across sources
    - the reason-category list left to `docs/schema.md` (gap)
  - **T8 VERIFIED.**
- **T9 decision requests D9.1–D9.2 prepared.**
  - The required manifest fields are specified from approved rules.
  - T9 is BLOCKED on the two decisions.
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
| 2026-10-28, D7.1′ + T8 requests | `git diff --check` | no output, exit 0 |
| | `uv run ruff format --check .` | 23 files already formatted, exit 0 |
| | `uv run ruff check .` | All checks passed, exit 0 |
| | status audit | T0–T7 VERIFIED, T8 BLOCKED (D8.1–D8.4), T9–T12 BLOCKED |
| | `uv run pytest` | not rerun (docs-only change) |
| 2026-10-28, T8 rulings + T9 requests | `git diff --check` | no output, exit 0 |
| | `uv run ruff format --check .` | 23 files already formatted, exit 0 |
| | `uv run ruff check .` | All checks passed, exit 0 |
| | status audit | T0–T8 VERIFIED, T9 BLOCKED (D9.1, D9.2), T10–T12 BLOCKED; no stale lines |
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

Each needs maintainer input.

- Blocker 7 (T9, BLOCKED: D9.1 `benchmark_version` rules, D9.2 data source for
  `scripts`)
- Blocker 11 (T10). Its ordering part is BLOCKED on T9. The acceptance condition
  can be ruled at any time.

## Next action

**Maintainer rulings on D9.1–D9.2** (graph, "T9 ... decision requests"). Then T10
becomes READY. No ADR edits until T1–T10 are decided.
