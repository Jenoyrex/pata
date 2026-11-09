# Task card — E-LIC: Licence + redistribution evidence (B14–B17)

- **Branch:** `workflow-kit` (maintainer safeguard 2026-11-04: no branch switch, no commit)
- **Started:** 2026-11-04 · **Session(s):** 1
- **Deps confirmed done:** E-INV (see graph)
- **Gate:** none · **Irreversible:** no

## Plan
1. Tabulate licence location, redistribution, attribution and date per candidate.
2. Re-check the texts that can change: data.gov.in policy and footer, Tamil Nadu policy, C4 label.

## Acceptance → proof map
| # | Acceptance criterion (copied verbatim from graph) | How it will be proven | Result |
|---|---|---|---|
| 1 | Per source: licence text location, redistribution terms, attribution terms, retrieval date | `docs/research/source-inventory.md`, "Licence and redistribution (E-LIC, B14–B17)" | see verifier |
| 2 | Unknown stays UNKNOWN; no inferred permission | same section; every open row reads UNKNOWN or "no reuse licence found" | see verifier |

## Scope fence (will NOT do)
- Read B14, B16 or B17 one way or the other. Send a clarification. Accept or reject a source.

## Stop-points
- None for this node. The readings go to G-SRC.

## Discovered work
- None.

## Proof
Hashes R115–R119 and R126–R130 in the inventory.

First verifier run, 2026-11-09: **FAIL** on criterion 1 and UNPROVEN on criterion 2 (C4 attribution
wrong; C5, C6, C12 not fully read; dates overstated; state-instance terms missing). C9c's row was
added before that run. Corrected from recorded evidence and fresh reads of policy pages (R127–R130).

Second verifier run, 2026-11-09: **FAIL** on criterion 1 (C1b date; `/Godl` text wrongly tied to the
Gazette PDF R110), PASS on criterion 2. Both corrected from the recorded rows, with no new retrieval.

## Verifier verdict
Third run, 2026-11-09: **Overall PASS.** The verifier's table, verbatim:

| # | Criterion (verbatim) | Verdict | Evidence (path:line / test id / command) |
|---|---|---|---|
| 1 | Per source: licence text location, redistribution terms, attribution terms, retrieval date | PASS | E:\PATA\docs\research\source-inventory.md:2418-2431 has all four columns for every candidate in the register at :2320-2344 (C1a, C1b, C2-C7, C8, C9a-c, C10-C12). **Dates:** cell dates match the passes holding the cited rows: R38 2026-10-04 (:432, :478); R50, R58 2026-10-06 (:745, :781, :789); R63, R65 2026-10-06 (:1141, :1174-1176); R82-R84, R88 2026-10-07 (:1410, :1453-1459); R99, R100 2026-10-25 (:1963, :2005); R110 2026-10-26 (:2170, :2180); R115-R118 2026-11-04 (:2279, :2296-2299); R126-R130 (:2306-2310). **Terms against recorded text:** GODL §3 (:1478-1485); attribution with DOI, URL or URI (:702); data.gov.in permission and acknowledgement wording (:817-818, :833-835); C4 policy and footer (:1203-1212); state-instance Terms of Use and Copyright Policy (:1487-1499). Both defects from the second verifier run are corrected (C1b date :2421; `/Godl` versus Gazette :2420, :2297). **My live fetch, 2026-11-09:** Dindigul and KVS pages contain the permission-by-mail and acknowledgement wording; the SARAS HTML has 0 licence, copyright or policy hits; `tn.data.gov.in/policies` has no "sending a mail" text and has the NIC IP sentence. **Limits:** I fetched those four pages once each with a generic browser user-agent. `tn.data.gov.in` shares the all-paths-disallowed `robots.txt` (R83 hash equals R49), so that one request went to a disallowed path, like the requests disclosed at :2283-2285. The maintainer should know this. I did not re-fetch the CBSE home page (C12 rests on R130 for that part), did not re-fetch R127-R130 hashes for comparison, and could not check earlier hashes because saved responses are not in the repo. C4's date cell gives no separate footer date; R63 is from the same pass as the policy (2026-10-06). |
| 2 | Unknown stays UNKNOWN; no inferred permission | PASS | E:\PATA\docs\research\source-inventory.md:2415-2416 states permission is not inferred from access. Status is UNKNOWN or "No reuse licence found" on every row (:2420-2431), except C7, which reads B14 and out of v0 scope (:2426). GODL terms are conditional: "if it governs" (:2420), "if GODL-India reaches state data, which is unresolved" (:2427). Unknown values stay explicit: C1b (:2421), C4 label (:2423), C5 CEO attribution (:2424), C11 (:2430), C12 (:2431). Conclusion at :2433-2436 says no candidate has a clear licence and takes no position on B14. No invented licence terms or admin links found. |

Checks: ruff ✓ · format ✓ · pytest 119 passed/0 failed (4 skipped: ADRs already accepted, tests\workflow\test_hooks.py:305) · graph ✓ · diff-check ✓

Overall: PASS (all rows PASS)

## Outcome
- Graph status set to: done. Evidence only: B14, B15, B3, B16, B17 and B4 all stay open for G-SRC.
- Known stale, not fixed after the verifier pass: `docs/research/focus-state-source-evaluation.md:252`
  still describes C10 as "As C1b"; the inventory's C10 row corrects it.
- Commit(s): none yet
