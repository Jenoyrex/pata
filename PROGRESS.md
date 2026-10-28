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
- T9 decision requests D9.1–D9.2 prepared. Commit `32deeb4`.
- **T9 rulings (2026-10-28).**
  - D9.1 accepted. §20 is to be revised in T11.
  - D9.2 (a) accepted subject to verification, then **verified**: UCD 15.0.0
    `Scripts.txt`, which matches `unidata_version` 15.0.0.
    - official URL, HTTP 200 retrieved 2026-10-28T14:20:02Z
    - SHA-256 `cca85d83…ea4b0`
    - the code-point set matches Python's assigned characters exactly
    - Unicode License v3 (`copyright.html` §2.2/§3.3, `license.txt`), retrieved
      2026-10-28
  - Kept explicit:
    - no publisher-published checksum was found or checked
    - the file is in scratch only (not vendored or committed)
    - using it needs a `data/manifests/` entry
  - **T9 VERIFIED.**
- T10 decision requests D10.1 and D10.2 prepared. Commit `5c71642`.
- **T10 rulings (2026-10-28).**
  - D10.1 accepted: joint, explicit, dated acceptance after T11; re-approval of
    changed items by name. The approval in principle doesn't cover revised text.
  - D10.2 accepted in the maintainer's 13-step wording.
  - No conflicts. **T10 VERIFIED.**
- **T11 READY.**
  - Section-by-section edit map prepared in the graph, mapping every ADR-0006 and
    ADR-0007 section to the rulings it must incorporate.
  - Also prepared: a re-approval list and the preserved gaps.
  - No ADR text drafted yet.
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
| 2026-10-28, T9 rulings + T10 requests | `uv run python -I -c` (versions) | Python 3.12.14, `unidata_version` 15.0.0 |
| | `curl` Scripts.txt to scratch | HTTP 200, exit 0, 2026-10-28T14:20:02Z; `sha256sum` `cca85d830f46aece2e7c1459ef1249993dca8f2e46d51e869255be140d7ea4b0` |
| | `uv run python -I` (scratch version-match script) | listed 149,251 = assigned 149,251; asserts ok, exit 0 |
| | `git diff --check` | no output, exit 0 |
| | `uv run ruff format --check .` | 23 files already formatted, exit 0 |
| | `uv run ruff check .` | All checks passed, exit 0 |
| | status audit | T0–T9 VERIFIED, T10 BLOCKED (D10.1, D10.2), T11–T12 BLOCKED; no stale lines |
| | `uv run pytest` | not rerun (docs-only change) |
| 2026-10-28, T10 rulings + T11 edit map | `git diff --check` | no output, exit 0 |
| | `uv run ruff format --check .` | 23 files already formatted, exit 0 |
| | `uv run ruff check .` | All checks passed, exit 0 |
| | `git diff --stat -- docs/decisions src scripts tests` | empty (no ADR or code changes) |
| | status audit | T0–T10 VERIFIED, T11 READY, T12 BLOCKED |
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

- No blocker decisions open. Remaining: reviewing the T11 draft, then acceptance of
  ADR-0006, ADR-0007 and ADR-0008 by the maintainer.
- Evidence gaps preserved: no source accepted; B6, B14–B17; the C1a field
  documentation; reason categories; L1; the `Scripts.txt` manifest; P1–P7.

## Next action

**T11: draft ADR-0007 rev 4 and ADR-0006 rev 6** from the graph's "T11 edit map".
- Commit them as one reviewable batch with status Proposed.
- Don't accept them. Acceptance follows D10.1.
- Start from a fresh session if context is low: read `CLAUDE.md`, this file and the
  graph first.
