# Task card — E-LGD: LGD level verification: state / district / sub-district / village

- **Branch:** `workflow-kit` (maintainer safeguard 2026-11-04: no branch switch, no commit)
- **Started:** 2026-11-04 · **Session(s):** 1
- **Deps confirmed done:** none (E-LGD has no deps)
- **Gate:** maintainer · **Irreversible:** no

## Plan
1. Search LGD's own portal and documents for level definitions.
2. Record each level with URL, date, location, short quote and hash; unknown stays UNVERIFIED.
3. Log CAPTCHA and access problems; ask the maintainer to fetch.

## Acceptance → proof map
| # | Acceptance criterion (copied verbatim from graph) | How it will be proven | Result |
|---|---|---|---|
| 1 | Each level has LGD-side evidence: URL, retrieval date, quoted field definition, file hash if downloaded | `docs/evidence/lgd/levels.md`, "Sources" and "Evidence by level" | see verifier |
| 2 | Any level without evidence is explicitly marked UNVERIFIED (never guessed) | same file, claims 4, 11, 14 | see verifier |
| 3 | CAPTCHA/403 blocks are logged, not bypassed; maintainer asked to fetch manually | same file, "Access problems" | see verifier |

## Scope fence (will NOT do)
- Solve a CAPTCHA, or call the portal's internal services from a script.
- Decide any state's sub-district outcome (ADR-0007 E1), or edit an ADR or the cue table.
- Commit the manual or any LGD document.

## Stop-points
- Gate: the maintainer reviews this record and chooses among the options in it.

## Discovered work
- None added as nodes. The Revenue manual and SOPs are a maintainer fetch, recorded in the evidence file.

## Proof
Hashes were computed with `sha256sum` on saved responses; see the evidence file. L13 recomputed:
`ed0c225a6bdee0b7a94f6ebb06d1b041eebe5dc279f0d13c6e6fb837b6998566`, equal to
`data/manifests/lgd_subdistricts.toml`. The saved responses stay in the session scratch directory,
so a checker can confirm the hashes only by re-retrieving the pages; live pages may change.

## Verifier verdict
First run, 2026-11-04: **FAIL.** Criterion 1 FAIL (missed Rajasthan example; no level-specific
quotes; L1 unhashed), criterion 2 PASS with caveat, criterion 3 UNPROVEN (CAPTCHAs on L3, L8, L9
unlogged). All 12 recomputed hashes matched. The record was corrected on 2026-11-05.

Scope-fence note: one scripted call to the portal's internal service was attempted before this
fence was written, and the session's permission check refused it. It is logged in the evidence file.

Second run, 2026-11-05: **FAIL** on criterion 3 only (district and village search forms unlogged);
criteria 1–2 PASS with small corrections (claims 6b, 12a; UNKNOWN to UNVERIFIED). A full-text sweep
of all 1,228 pages found no other per-state value. All corrected on 2026-11-05.

Third run, 2026-11-05, scoped to those fixes: criteria 1–3 **PASS**, Overall PASS. It did not repeat
the full hash and quote sweep (done in run two). Its two non-blocking corrections (retrieval dates
on claims 6b and 12a, "for example" on the page list) were applied after that run.

## Outcome
- Graph status set to: review (gate = maintainer; awaits your choice among the record's options)
- Commit(s): none (maintainer safeguard)
