# Task card — E-INV: Candidate source inventory (exact files/snapshots, publishers)

- **Branch:** `workflow-kit` (maintainer safeguard 2026-11-04: no branch switch, no commit)
- **Started:** 2026-11-04 · **Session(s):** 1
- **Deps confirmed done:** none (E-INV has no deps)
- **Gate:** none · **Irreversible:** no

## Plan
1. Consolidate C1–C12 from the ten earlier passes into one register.
2. Re-check C1–C4 metadata and the hosts that were failing.
3. Say plainly that no candidate data file has been retrieved.

## Acceptance → proof map
| # | Acceptance criterion (copied verbatim from graph) | How it will be proven | Result |
|---|---|---|---|
| 1 | Every candidate lists publisher, exact file/snapshot, URL, retrieval date or 'not retrieved' | `docs/research/source-inventory.md`, "Candidate register (E-INV)" | see verifier |
| 2 | No raw data committed to Git | `git ls-files data/raw` empty; `git status --short` shows no data path | see verifier |

## Scope fence (will NOT do)
- Accept, reject or rank a source. Download a candidate data file. Research every unresearched
  category (G11 stays open and is stated).

## Stop-points
- None for this node. Retrieving any candidate file is a maintainer step (G-SRC packet).

## Discovered work
- E-B6: scripted aggregate inspection, added to the graph.

## Proof
Metadata hashes are in the inventory, R111–R125.

## Verifier verdict
First run, 2026-11-04: **FAIL** on criterion 1 (C5, C8a–C8i, C9b, C9c had no exact file or URL);
criterion 2 PASS; no fabrication found. The rows were re-researched from metadata on 2026-11-05.

Second run, 2026-11-05: **FAIL**, narrowly. C10 had gaps, since corrected from R125. C9c's URL is
unknown and its "not a candidate" label had no ruling behind it. All R120–R124 hashes and 22 file
entries matched; C8d and C8i judged legitimate. Criterion 2 PASS.

**Blocked on the maintainer:** C9c needs a ruling or a URL. The criterion is not reinterpreted here.

## Outcome
- Graph status set to: blocked (C9c)
- Commit(s): none (maintainer safeguard)
