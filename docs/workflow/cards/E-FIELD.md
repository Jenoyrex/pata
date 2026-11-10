# Task card — E-FIELD: Field semantics evidence (incl. C1a Address_Original_First_Line)

- **Branch:** `workflow-kit` (maintainer safeguard 2026-11-04: no branch switch, no commit)
- **Started:** 2026-11-04 · **Session(s):** 1
- **Deps confirmed done:** E-INV (see graph)
- **Gate:** none · **Irreversible:** no

## Plan
1. Read every publisher-side descriptor for each candidate raw-text field.
2. Record what is documented; a column name counts for nothing.
3. State the C1a outcome.

## Acceptance → proof map
| # | Acceptance criterion (copied verbatim from graph) | How it will be proven | Result |
|---|---|---|---|
| 1 | Each candidate proposed for acceptance has its raw-text field backed by publisher documentation, not column names, or falls under the ADR-0006 section 2 exception (maintainer ruling 2026-11-10) | `docs/research/source-inventory.md`, "Field semantics (E-FIELD)" | **Not met: no publisher definition found for any field.** The 2026-11-09 verifier judged the earlier wording |
| 2 | C1a outcome stated: qualifies / does not qualify / undetermined, with evidence | same section | Undetermined, with evidence |

## Scope fence (will NOT do)
- Reword criterion 1 to pass it. Infer meaning from names. Read records.

## Stop-points
- Criterion 1 is the stop-point. Ask the publishers, or a maintainer ruling on what suffices.

## Discovered work
- E-B6 can add shape statistics once a file exists. Those are not publisher documentation.

## Proof
Hashes R111–R114 in the inventory. Checked per C1–C3 list: `id`, `name`, `type`, `desc`, and the
resource `note`. Each `desc` repeats the title; each `note` covers missing values and, for C1,
update timing.

## Verifier verdict
2026-11-09: **Overall FAIL**, on criterion 1 only. The verifier's table, verbatim:

| # | Criterion (verbatim) | Verdict | Evidence (path:line / test id / command) |
|---|---|---|---|
| 1 | Each candidate raw-text field backed by publisher documentation, not column names | FAIL | E:\PATA\docs\research\source-inventory.md:2380 states that no publisher documentation defining any candidate field was found. In the table at :2387-2400, every row says "None found". :2413-2416 says the criterion "cannot be met on available evidence". I re-fetched R32 on 2026-11-09: `Address_Original_First_Line` has only `id`, `name` and `type: keyword`, and each `desc` shown repeats a title. R131 (MDDS p.51, "Address of Facility") and R132 (manual p.1) define no candidate column, as :2421-2427 says. |
| 2 | C1a outcome stated: qualifies / does not qualify / undetermined, with evidence | PASS | Stated as undetermined at source-inventory.md:2387 and :2402-2411, and at E:\PATA\docs\research\focus-state-source-evaluation.md:370-371. The evidence is R111-R114 plus the live re-fetch: the R29 note reads "NA/Blank: Not Available; data will be updated on regular interval", and the R32 field descriptor matches. The row does not infer meaning from the column name (:2405-2406). |

Checks: ruff ✓ · format ✓ · pytest 138 passed/0 failed (4 skipped: ADRs already accepted, tests/workflow/test_hooks.py:305) · graph ✓ · diff-check ✓

Overall: FAIL

It found no sign of fabrication. It did not re-check R111–R114 hashes (live content compared instead),
R133, the C2 and C3 notes, or rows C5–C7 and C9–C12 beyond their "None found" entries.

Further search, 2026-11-09: rows C7 and C9c added; R131–R133 read. No candidate field gained a
publisher definition.

## Outcome
- Started 2026-11-09, after E-INV closed. Graph status set to: blocked. The maintainer reworded criterion 1
  on 2026-11-10; it is still unmet until a publisher answers or the §2 exception applies.
- Commit(s): none
