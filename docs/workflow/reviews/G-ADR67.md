# Gate review packet — G-ADR67: T11 + D10.1, joint acceptance of ADR-0006 rev 6 and ADR-0007 rev 4

Prepared by Claude on 2026-11-05 from an `adr-reviewer` report. **Review only: nothing was modified,
committed, merged, pushed or accepted while preparing this packet.**

Read the diff itself. Line numbers (`l.`) refer to `adr-0006-rev6` unless a row says main. Section 3
quotes the changed wording only, so it departs from the template's full old-and-new columns. See both
versions with `git diff main..adr-0006-rev6 -- docs/decisions/`.

## 1. What you are being asked to decide

Whether to accept ADR-0006 revision 6 and ADR-0007 revision 4 together, by explicit dated
acceptance in both files, and merge the branch. **This gate unblocks D-SCHEMA, U-UNICODE and G-ADR8,
and through them all pipeline code.** The approval in principle of F1–F13 does not cover the revised
text (D10.1), so the changed items need approval by name.

## 2. Scope of change

```
$ git diff --stat main..adr-0006-rev6
 PROGRESS.md                                        |  35 +
 docs/decisions/0006-annotation-scope-and-schema.md | 703 ++++++++++++++++-----
 docs/decisions/0007-focus-states-and-sources.md    | 213 +++++--
 docs/research/dependency-graph.md                  |   2 +-
 4 files changed, 756 insertions(+), 197 deletions(-)
```

Refs per the reviewer: `main` `0d1c570`, branch `0513447`, commits `099fdb6` and `0513447`. Both ADRs
still say Proposed; nothing in the draft claims acceptance. ADR-0008 is also Proposed and unchanged.

## 3. Decision by decision

| ID | What changes (new wording quoted) | Open edge per the reviewer [assumption] | Deviation from the edit map |
|---|---|---|---|
| F1 | Adds: "A withdrawal or human-screen failure excludes the record's whole duplicate class; a failure caused only by `source_context` stays per record" | Denylist re-match of a `source_context`-only exclusion (I6); whether a rules-screen failure cascades | None |
| F3 | Adds the valid-PIN rule, `pincode_role` cases, ordered `not_checkable` causes. "A PIN never sets verification scope." | A village linked only by an addition after an empty name stage: role `not_applicable`, yet §9 could still compute consistency | None |
| F5 | "frozen in staging before the first human exposure of any record" replaces "frozen before experiments" | How a recompute keeps an exposed record out of test when the bucket hashes the class key: no mechanism stated | None |
| F9 | Adds a fixed `basis` precedence, gate-rejected designators, "Gated or invalidated candidate lists never feed D." | An F10 role with no `pending_level` falling to `not_specified` is only implicit | None |
| F10 | Adds `place_unspecified`; "Their `pending_level` is named only on a cited source" | The only revised F row with no "(Revision 6 adds...)" note | None |
| F12 | Adds staged screening: rules-only screen, split frozen in staging, role-restricted human screen, then `data/processed/` | No eligible screener; staging content limit against needed identifiers (I10) | Staging sits in F12, which the map allows |
| F14 (new) | Layer A records roles as written; a level mapping is verified only under ADR-0007 §8; generation and reconciliation gates | Known limitation is in §7, not §21 (D1) | None |
| F15 (new) | Private denylist as a versioned screen rule; exposure log in the same store; append-only errata | Retention and access control of the private store | None |
| S6 | Adds distinct-value lists to the evidence limit, plus column roles, aliases, tokens and `raw_text` scope in the manifest | A distinct-value list that itself contains personal data | Decoding is absent from §5 (D2) |
| S9 | Extends verification from sub-district to all four LGD levels, national or per state | Who resolves a conflict: "until it is resolved" has no owner | None |

## 4. Points that deserve your attention

These are text facts from the reviewer. Whether each matters is your call. I recommend deciding I6,
I10 and the O/E wording before accepting, because they affect later code or the acceptance itself.

**Deferred items: the claim is only partly documented.**

- P and L: ADR-0006 l.12 says items deferred in §21.2 and §21.3 do not block acceptance.
- O and E: **ADR-0007 has no such sentence.** The statement exists only in
  `docs/research/dependency-graph.md` l.1227–1228 and the graph node. O1–O7 sit under "10.2 Open",
  not "Deferred". The G-ADR67 criterion asks you to confirm these are "non-blocking and documented".

Later constraints recorded: P1–P5, P7 by the pilot; P6 before the split; L1, E2 at the release ADR;
L3, E1 before the guidelines freeze; L5, E4 before a second release; L6 by new ADR; O1–O2 after
assessments and selection records; O3–O5 before the split; O6–O7 after inventory and selection
records; E3 in `docs/schema.md`; E5 in a source ADR.

**Inconsistencies.**

| # | Where | Finding |
|---|---|---|
| I1 | ADR-0007 l.82–83 | Quotes ADR-0006 Consequences text that rev 6 removed |
| I2 | ADR-0007 l.71 | Quotes "sources designated as held out"; rev 6 §17 says "held-out publisher" |
| I3 | ADR-0007 l.71–72, l.375 | Says a recompute is allowed "before the freeze"; rev 6 §17 says "only to fix a bug", with an exposed-record limit |
| I4 | Status lines | ADR-0007 lacks the cross-reference check and deferred-items rule that ADR-0006 states |
| I5 | ADR-0008 l.6 | Says ADR-0007 "cannot be accepted before ADR-0006"; the drafts say "together" |
| I6 | ADR-0006 §12, F1 | A `source_context`-only failure stays per record, but a denylist match excludes the whole class, with no carve-out |
| I7 | ADR-0006 §19 l.1271 | Narrower than F9 and §8 on `deferred_coverage` |
| I8 | F5, §17 l.1000 | "any record" against "any admitted record" |
| I9 | ADR-0006 §4 l.326–327 | "for each selected state"; §3, F14 and ADR-0007 §8 allow national scope |
| I10 | ADR-0006 §12 l.730 | Staging "holds only `raw_text` and allowlisted `source_context`", yet per-record assignments and denylist fields need more unless held elsewhere [assumption] |
| I11 | §18 and §12 | Denylist entry described for the record and class, against per record |

**Deviations from the T11 edit map.** D1 limitations placed in §7, §8, §12, not §21. D2 decoding
absent from ADR-0007 §5 (ADR-0006 §2 fixes it per source). D3 `district` and `state` rows of §4 also
changed. D4 §2 adds the Decoding block. D5 `admission.screened_by` row changed. D6 ADR-0007 §2 l.127
changes `focus_state_version`. D7 the 13 D10.2 steps are present in order but lightly paraphrased,
against "in the maintainer's wording". D8 L5 reworded. D9 §10 wording differs from the ruling summary.

Stale on the branch: its `PROGRESS.md` "Next action" still says to draft T11.

**New evidence bearing on this gate.** ADR-0007 §8's standard is what E-LGD applied. See
`docs/evidence/lgd/levels.md`, including the Rajasthan question.

## 4a. Alternatives

| Option | What it means | Evidence for | Cost |
|---|---|---|---|
| A. Accept as drafted | Dated acceptance in both ADRs, named re-approval, merge | All ten decisions located; no acceptance claimed; no gap filled; §17 vectors recomputed and matched | D10.1 requires cross-reference checks to pass, and I1–I3 are stale cross-references, so this needs you to rule them acceptable. They and the I6, I10 gaps become permanent: accepted ADRs are never rewritten (`CLAUDE.md`), so fixes need a new ADR |
| B. One more draft, then accept (**recommended**) | ADR-0006 rev 7 and ADR-0007 rev 5: fix I1–I3, I5 if ADR-0008 is included, I6, I10, the O/E sentence; then named approval | The same reports. Section 4b corrects this row: I1–I5 and the O/E sentence are text fixes, while I6 and I10 need rulings | Another review, and any changed decision row needs re-approval. Needs your go to edit that branch |
| C. Change a decision | Reject or reword a row such as F5, F12, F14 | Open edges in section 3 | Larger re-review; may reopen rulings |
| D. Hold | No decision now | Nothing further is needed from evidence | D-SCHEMA, U-UNICODE, G-ADR8 and all pipeline work stay blocked |

## 4b. Option B draft and two decision requests (2026-11-05)

**Draft:** `docs/workflow/reviews/G-ADR67-rev7-rev5.patch`. It is proposed text, not applied to any
branch. It makes ADR-0006 rev 7, ADR-0007 rev 5 and ADR-0008 rev 3. It covers I1, I2, I3, I4, I5 and
the O/E sentence. It changes no decision row and all three ADRs stay Proposed. Applying it also
needs your ruling on two points outside this list: D10.1 names rev 6 and rev 4, and ADR-0008 was
outside the T11 edit map. If applied, the G-ADR67 title, criteria and this packet need the new
revision numbers.

An `adr-reviewer` run found that an earlier version also made new decisions on I6 and I10, and
missed one I2 occurrence. I removed the I6 and I10 text and fixed I2. **The reduced patch has
mechanical checks only and no second reviewer run:** it applies to `adr-0006-rev6` in a temporary
index, all 28 and 22 decision rows are unchanged, and each status line says Proposed.

Check the patch against the branch without touching this checkout:

```bash
git worktree add ../pata-adr-rev7 adr-0006-rev6
git -C ../pata-adr-rev7 apply --check E:/PATA/docs/workflow/reviews/G-ADR67-rev7-rev5.patch
```

**Decision 1: I6, what a denylist match does after a failure caused only by `source_context`.**
D8.2 keeps that failure per record. The derived matching rule, marked overridable, excludes the
whole class with no exception. A per-record drop before split-key step 4 on a rebuild can change the
class key of the remaining members, or take a class out of holdout, which conflicts with fixed
assignments [assumption on ordering; no text fixes it].

| Option | Effect | Cost |
|---|---|---|
| A. Carve-out, applied after step 4 (**recommended**) | The entry says the failure was context-only. The record still counts toward the class key and holdout, then it alone is dropped. A rebuild reproduces the first split | Two new rules, and a constraint on the reason categories, a gap `docs/schema.md` was to fill |
| B. Carve-out, applied before step 4 | Simpler to implement | Rebuilds can move other records; needs a further rule to stop it |
| C. Make context-only failures cascade | Removes the conflict; no new mechanism | Reverses D8.2 and changes F1. Records with clean context are lost |

**Decision 2: I10, what staging may hold.** D7.1′'s derived note says only `raw_text` and allowlisted
`source_context`. The denylist needs `source_record_ref` and `raw_text_sha256`, and the split needs
`record_id`, `group_key` and the assignment. §2 also requires other fields, such as
`admission.screened_by`.

| Option | Effect | Cost |
|---|---|---|
| A. Limit source columns only (**recommended**) | Of a source's columns, staging holds only the `raw_text` source, allowlisted `source_context` and any native `source_record_ref`. Values ingestion computes may sit beside them | Reads the derived note as being about source columns [assumption]. §12's "Nothing outside the list is ingested" needs a matching exception for a native ID |
| B. Keep the note literally | Identifiers and assignments sit in a separate file keyed to each record | The same data on the same local disk, with more to keep in step |

Either answer needs its own wording and review, and F1, F12 or F15 re-approval as affected. I7, I8,
I9 and I11 also stay open after the patch, and I11 depends on Decision 1.

**Rulings, 2026-11-05: Option A for both** (recorded in `docs/research/dependency-graph.md`, "G-ADR67
rulings"). The patch now carries that wording in ADR-0006 §12 and §17. This is not acceptance.

**Second `adr-reviewer` run, 2026-11-05.** Both rulings are implemented with no added rule; I1–I5 and
the O/E sentence are fixed; no decision row changes; all status lines say Proposed. The revision note
failed narrowly and was then corrected, so that one note has no reviewer run. The patch is not ready
for acceptance. Still open:

| Item | Where (patched ADR-0006) | Why it matters | Recommendation (not a decision) |
|---|---|---|---|
| I9 | l.338 "for each selected state" | Fails the cross-reference test: L3 says national or per state | Text fix |
| I11 | §18 withdrawal, "the record and its duplicate class" | Fails the test against §12, and has no context-only branch | Text fix following the I6 ruling |
| I7 | §19 `deferred_coverage` | Narrower than F9 and §8; fails only if the check covers consistency | Text fix |
| I8 | §17 "any admitted record", F5 "any record" | First exposure is on staged records, not yet admitted | Fix §17 and leave the F5 row alone |
| Native `source_record_ref` | §2, §12 | **New.** No text puts an individual value through the privacy screen, and it now sits in staging. The gap predates the patch | Needs a ruling: same screen as `source_context` |
| N1 | §17 split table | **New.** "No key appears in two splits" can fail when a held-out and a non-held class share a `group_key`. Predates the patch; whether data reaches it is an assumption | Needs a ruling |
| Rebuild scope | §12 and §17 | §17 says "in a rebuild"; whether a bug-fix recompute counts is not stated | Decide with N1 |
| Revision numbers, ADR-0008 rev 3 | D10.1, graph | No ruling yet | Approve both |

## 5. Checks

See `PROGRESS.md`, session entry of 2026-11-05. The reviewer recomputed the §17 salt, four vectors
and four boundaries with the standard library, and all matched. It did not run ruff or pytest on the
branch, and I did not switch branches to do so (maintainer safeguard).

## 6. Facts vs. assumptions

- **Verified from the repository, by the reviewer:** the diff, status lines, rows and line numbers.
- **Assumptions:** items marked [assumption]. The reviewer did not trace every sentence to a ruling.
- **Recommendation (mine, not a decision):** rule on section 4b, apply the patch, then accept. The
  earlier idea that I6 and I10 were small text fixes was wrong: both need a ruling. I have made no
  edits to any ADR or to the branch.

## 7. Maintainer checklist

- [ ] Every approved ruling is incorporated (D10.1). The reviewer did not trace every sentence
- [ ] Cross-reference checks pass (D10.1). I1, I2, I3 and I5 are open against this today
- [ ] I read the full diff, not only this packet
- [ ] Every changed decision is acceptable as written: F1, F3, F5, F9, F10, F12, F14, F15, S6, S9
- [ ] Deferred P, L, O and E items are genuinely non-blocking, and that is documented
- [ ] I decided what to do about I1–I11
- [ ] I wrote dated acceptance in each document myself
- [ ] I merged the branch myself
- [ ] I ran `uv run python scripts/graph.py approve G-ADR67 --by <me> --ref "<doc § + merge sha>"`
