# Task card — I-V1KIT: Toolkit v1 readiness: user guide, re-pinning path, honest claims

- **Branch:** `workflow-kit` (maintainer's working branch)
- **Started:** 2026-11-10 · **Session(s):** 1
- **Deps confirmed done:** G-V1SCOPE (approved by the maintainer, 2026-11-10)
- **Gate:** none · **Irreversible:** no

## Plan
1. Tests first: a new snapshot is refused, re-pinned as the guide says, then builds deterministically.
2. Write `docs/toolkit.md`.
3. Say in the README that version 1 is a gazetteer toolkit under ADR-0009.

## Acceptance → proof map
| # | Acceptance criterion (copied verbatim from graph) | How it will be proven | Result |
|---|---|---|---|
| 1 | docs/toolkit.md covers install, building from a user's own LGD snapshot, the output tables, name_key, source_stats and the limits in ADR-0009 | The guide's sections, read against ADR-0009 | see verifier |
| 2 | A test re-pins a manifest to a synthetic fixture snapshot through the documented path and builds deterministically; the fixture is labelled synthetic | `test_new_snapshot_is_refused_until_repinned`, `test_repinned_build_is_deterministic` | see verifier |
| 3 | README and docs state version 1 has no address dataset, model, benchmark or metric | `test_docs_state_what_version_1_is_not` | see verifier |
| 4 | LGD acknowledgement wording from ADR-0004 section 2 appears in the user guide | `test_guide_carries_the_lgd_acknowledgement` | see verifier |

## Scope fence (will NOT do)
- Bump the version, tag or publish (R-V1). Run on or publish LGD data. Add a re-pinning command:
  the documented manual path works and is tested.

## Stop-points
- None for this node. R-V1 needs an explicit maintainer "go".

## Discovered work
- None.

## Proof
`uv run pytest tests/test_toolkit_v1.py -q`: 8 passed. Before the guide existed, 3 tests failed as expected.

## Verifier verdict
First run, 2026-11-10: **FAIL.** Guide step 2 gave a bare `raw_file`, which is not found, and the test did
not exercise that step. Fixed: the guide gives the working form, and the test now uses a renamed LGD-style
workbook through the real command line.

Second run, 2026-11-10: **Overall PASS.** The verifier's table, verbatim:

| # | Criterion (verbatim) | Verdict | Evidence (path:line / test id / command) |
|---|---|---|---|
| 1 | docs/toolkit.md covers install, building from a user's own LGD snapshot, the output tables, name_key, source_stats and the limits in ADR-0009 | PASS | Read against E:\PATA\docs\decisions\0009-version-1-gazetteer-toolkit.md §2-§4. E:\PATA\docs\toolkit.md: install :10-18; own snapshot :20-49; output tables :51-64; name_key :66-76; source_stats :78-89; limits :6-8, :48-49, :91-100. Claims checked against code: exit codes 0/1/2 and no tables on exit 1 (E:\PATA\src\pata\gazetteer.py:519-552, E:\PATA\scripts\build_gazetteer.py:28-30); name_key example (`test_guide_name_key_example_is_correct`); Python 3.12 (pyproject.toml:11); 11,390 warnings (E:\PATA\docs\gazetteer.md:205). Scratch-copy walk of steps 2-6 on the real manifest format with synthetic workbooks: refused rc 2, re-pinned, built rc 0, all six output files present. The guide's source_stats command ran rc 0, and rc 2 on a wrong checksum. Step 1 (manual portal download) was not run. |
| 2 | A test re-pins a manifest to a synthetic fixture snapshot through the documented path and builds deterministically; the fixture is labelled synthetic | PASS | `tests/test_toolkit_v1.py::test_new_snapshot_is_refused_until_repinned`, `::test_repinned_build_is_deterministic`, helper E:\PATA\tests\test_toolkit_v1.py:50-65; synthetic label at :1. Mutations on a scratch copy, each caught: nonce added to build_info fails the determinism test; sha check disabled fails the refusal test; wrong sha printed by --snapshot-info fails both. Limits: the test does not exercise the guide's conditional title/header update (step 4), and it compares only the files in output a (the walk confirmed identical file sets and bytes). |
| 3 | README and docs state version 1 has no address dataset, model, benchmark or metric | PASS | E:\PATA\README.md:35; E:\PATA\docs\toolkit.md:6; E:\PATA\docs\decisions\0009-version-1-gazetteer-toolkit.md:37. `test_docs_state_what_version_1_is_not[doc0]` and `[doc1]`: removing the sentence from either file fails the matching case on the scratch copy. |
| 4 | LGD acknowledgement wording from ADR-0004 section 2 appears in the user guide | PASS | E:\PATA\docs\toolkit.md:108-111 matches E:\PATA\docs\decisions\0004-lgd-portal-xlsx-snapshots.md:112-115 verbatim after whitespace normalisation (direct script comparison returned True). This comparison is the evidence. `test_guide_carries_the_lgd_acknowledgement` checks only the opening phrase: deleting the "Reproduced under the LGD Copyright Policy (...)" tail still gave 8 passed, so the test would not catch a partial loss of the wording. |

Checks: ruff ✓ · format ✓ · pytest 160 passed/0 failed (5 skipped; node verify command `uv run pytest tests/test_toolkit_v1.py -q`: 8 passed) · graph ✓ · diff-check ✓

Overall: PASS (all rows PASS)

## Outcome
- Graph status set to: done. Synthetic fixtures only; no real LGD re-pin was run.
- Commit(s): none yet
