# Dependency graph: ADR-0006 / ADR-0007 acceptance work

Working note, not a decision record. It tracks the acceptance-readiness review of
ADR-0006 revision 5 and ADR-0007 revision 3, and the maintainer rulings made so
far. Rulings listed here are **not yet written into the ADRs**. The ADR text stays
authoritative until a revision incorporates them.

"Blocker N" means a blocker from that review. These are unrelated to the source
blockers B1, B2, ... in `focus-state-source-evaluation.md`.

Statuses: BLOCKED, READY, IN PROGRESS, VERIFIED, ACCEPTED. A decision task is
READY when its prerequisites are resolved and its options are written up. The
maintainer's ruling is the work.

## Edges

`A → B`: B can't proceed until A is resolved.

```
T0 ─────────────────────────────────────────────┐
T1 (Blocker 2 rest) → T2 (Blocker 8) → T3 (Blocker 9)
T4 (Blocker 5) ── same §17 text, edit together ── T5 (Blocker 4)
T6 (Blocker 6) → T8 (Blocker 3) ← Blocker 1 (decided)
T7 (Blocker 10)
T1..T8 → T9 (Blocker 7) → T10 (Blocker 11 ordering)
T1..T10 → T11 (ADR-0006 rev 6 + ADR-0007 rev 4) → maintainer acceptance → T12
```

- T1 → T2: R1f (anchor invalidation) overlaps Blocker 8's "multiple higher-level
  anchors", and both edit ADR-0006 §7–§9.
- T2 → T3: Blocker 9's per-annotator Layer D needs settled Layer C statuses and sets.
- T6 → T8: a withdrawal denylist keys on `raw_text_sha256`, which depends on
  decoding.
- T4, T5, T6, T7 have no prerequisites. The order below is a recommendation, not a
  dependency.
- T11 waits for every decision. The maintainer asked for one coordinated
  revision, not piecemeal edits.

## Tasks

| ID | Task | Status | Prerequisites | Affected text | Needs from maintainer | Done when |
|---|---|---|---|---|---|---|
| T0 | Workflow files (`CLAUDE.md`, `PROGRESS.md`, this note) | VERIFIED | — | these files | — | CI checks and `git diff --check` pass. Committed. |
| T1 | Close Blocker 2 | VERIFIED (2026-10-28) | — | ADR-0006 §3, §4, §7–§9, §14, F9, F10; ADR-0007 §8, S9 | — (R1f, R1g, R8b ruled) | every item ruled. The R1f procedure details that depend on Blocker 8 moved to T2 (items 8.6–8.9). |
| T2 | Blocker 8: PIN, `basis` and anchor semantics | READY | T1 | ADR-0006 §7–§9 | items 8.1–8.10 below | every case has exactly one outcome |
| T3 | Blocker 9: Layer D reliability method | BLOCKED (T2) | T2 | ADR-0006 §1, §14, §15 | derivation inputs; independent C set for `ambiguous`; meaning of `merge` | method computable from stored documents |
| T4 | Blocker 5: split-key inputs | READY | — | ADR-0006 §17 steps 1–2; ADR-0007 §5 | alias table and its evidence; one state column; district-column rules | two engineers derive the same step-1/2 result |
| T5 | Blocker 4: freeze point, salt, bucket mapping | READY | — (edit with T4) | ADR-0006 §17, F5 | freeze at first human exposure; salt provenance | mapping fully specified; freeze point testable |
| T6 | Blocker 6: `raw_text` eligibility and decoding | READY | — | ADR-0006 §2, §11, L6 | whether documented partial address lines qualify | eligibility decidable from documentation alone |
| T7 | Blocker 10: screening before the split | READY | — | ADR-0006 §12, §14; ADR-0007 §5 | option (a), (b) or (c); dev-only guideline examples | no unrecorded pre-split exposure |
| T8 | Blocker 3: withdrawal, denylist, errata | BLOCKED (T6) | T6, Blocker 1 | ADR-0006 §12, §13, §18 | denylist (a), (b) or (c); cascade to duplicate class; errata location | a rebuild can't silently re-admit a withdrawn record, or the limitation is documented |
| T9 | Blocker 7: release-manifest fields | BLOCKED (T1–T8) | T1–T8 | ADR-0006 §18 | `benchmark_version` major/minor rules | every version input is listed |
| T10 | Blocker 11: acceptance condition and ordering | BLOCKED (T9) for ordering. The acceptance condition can be ruled any time. | T9 | ADR-0006 status line, Consequences; ADR-0007 Consequences | what counts as acceptance | both ADRs give one consistent order |
| T11 | Coordinated revision: ADR-0006 rev 6, ADR-0007 rev 4 | BLOCKED (T1–T10) | T1–T10 | as above | approval of the drafted diff | full diff reviewed; cross-references checked |
| T12 | Follow-up implementation (`docs/schema.md`, procedures, validator) | BLOCKED (acceptance) | ADR acceptance | per ADR-0006 Consequences | — | per ADR |

Other open records outside this graph: ADR-0003 (NAPIX permission pending), ADR-0008
(Proposed), and the source blockers in `focus-state-source-evaluation.md`.

## Ruling ledger (maintainer, 2026-10-27 and 2026-10-28; not yet in the ADRs)

**Blocker 1: decided.**
- Merge only records with identical `name_key(raw_text)`.
- The class key is the lexicographically smallest member key.
- If any member is from a held-out publisher, the whole class goes to `test_source_holdout`.
- No district-level transitive grouping.
- Drop "union-find" from ADR-0006 §17 step 4 and ADR-0007 §3 and §6.

**Blocker 2: decided so far.**
- **Evidence standard (C).** LGD-side evidence, with URL and retrieval date, for all
  four levels, national or per state as the evidence supports.
  - State-government material only corroborates (S9).
  - Name patterns, counts and annotator knowledge are not evidence.
- **Layer A (4).** Layer A records the role as written. Verification gates only
  Layer C and Layer D.
  - The guidelines and cue table own the word-to-label mapping.
  - The F10 exceptions (`Block`, `Sub-division` → `place_unspecified`) stay (R6).
- **Unverified designators (1, R3).** An unverified designator removes its claimed
  level, and never falls back to the no-designator route.
  - The inversion with bare names is documented as a known limitation.
- **Gate (R1a, R1b, R1c).** Runs after the hierarchy stage and before the PIN stage,
  on generated sets only.
  - If any candidate is outside the verified scope, the role becomes
    `not_in_gazetteer` / `level_mapping_unverified`.
  - Its lists are kept for audit, `final_set` is `[]`, and it anchors nothing.
  - A new stage flag, `level_mapping_unverified`, records the outcome.
  - A PIN never establishes verification scope.
- **Reconciliation additions (R1d).** An addition outside the scope is recorded, and
  the role becomes `level_mapping_unverified` with `final_set` `[]`. Additions can't
  bypass the gate.
- **Empty name stage (R1e).** `no_match_in_snapshot`, kept distinct from a gate failure.
- **`pending_level` (R2).** A rejected designator whose written role is an LGD label
  records that level as its `pending_level`.
- **F10 designators (R8).** `pending_level` only where evidence supports it.
  Otherwise Layer D stays `not_specified`, with no guessed level.
- **`not_checkable` (R4).** Causes are ordered: no valid PIN, then
  `deferred_coverage`, then any other reason.
  - The PIN stage filters only the village members of a mixed-level
    `place_unspecified` role.
- **Conflicting evidence (3, R5, R5b).** Compatible state LGD evidence narrows a
  national mapping.
  - Contradicting state LGD evidence leaves the mapping unverified for that state.
  - Contradicting national LGD evidence leaves it unverified nationally.
  - State-government material can't demote a national mapping.
- **PIN stage not run (R7).** `pincode_role` `not_applicable` also covers "the PIN
  stage did not run", stated as meaning no PIN was checked.
- **Agreement (R9).** Mechanically derived Layer C statuses are excluded from status
  kappa and counted separately.
  - Excluded: non-linkable defaults, designators unverified everywhere, failures at
    the generation gate.
  - Not excluded: R1d failures.
- **Timing (5).** Verification is complete, or frozen as unverified, before the
  guidelines freeze. A later change means a new `cue_table_version` and
  re-annotation.
- **Village records (V).** They cover `(Ct)`, `(Og)` and `(Part)` where evidence
  permits, with nothing assumed.
- **Out of scope here.** Bare-name state/district matching (P5).

**Blocker 2: ruled 2026-10-28.**
- **R1f, option (a).** If a higher-level role's final outcome no longer supports
  the unit it anchored, every lower role that depended on that anchor becomes
  `not_in_gazetteer` / `anchor_invalidated`.
  - No link that depends on the anchor survives.
  - The count is recorded and reported.
  - Determinism, timing, multiple anchors and the Blocker 8 interactions are
    checked under T2, items 8.6–8.9.
- **R1g: yes.** For roles that fail either gate, additions and prunings are recorded
  for audit only.
  - They never change the effective set or bypass verification.
  - The gated outcome stays terminal.
- **R8b: accepted.** Any S9-permitted source with a URL and retrieval date may
  support an F10 `pending_level`, including state-government material.
  - It supports "pending" only, never "verified".
  - Names, gazetteer counts, name patterns, annotator knowledge and intuition never
    qualify.
  - `pending_level`, `not_specified` and a verified mapping stay distinct.

**Consistency check of the 2026-10-28 rulings against the ADR text**
(findings; the ADRs are unchanged):
- **R8b vs. S9 (ADR-0007 §8, l.378).**
  - No conflict: S9 governs verification only, and R8b assigns no verification.
  - ADR-0006 §3 l.187–188 says cue-table contents "come from dev-pool observation
    and LGD documentation". R8b adds cited S9 sources for `pending_level`. That
    sentence needs a wording change in T11.
  - F10 (l.924) is unchanged: those spans stay `level_mapping_unverified`.
- **R1g vs. Layer D (ADR-0006 §8).** Confirmed from the text.
  - Layer D reads only linked roles, `ambiguous` roles' sets, ancestors of linked
    units, and the record's PIN (`inferred_from_pincode`).
  - No status or `basis` reads `candidates.*` of a `not_in_gazetteer` role.
  - T11 should state this explicitly.
- **Pre-existing defect, ADR-0006 §8 l.407.**
  - "a `place_unspecified` role ... whose `final_set` lies entirely at `L`" is
    vacuously true for an empty `final_set`.
  - So every unlinked `place_unspecified` role (gated, `no_match_in_snapshot`,
    `anchor_invalidated`) is a role at all four levels.
  - With `no_match_in_snapshot` that gives Layer D `not_in_gazetteer` at every
    level. → T2 item 8.7.
- **R1f vs. Layer D.** §8's `not_in_gazetteer` row accepts only
  `no_match_in_snapshot` and `no_supported_match`.
  - An `anchor_invalidated` role at L would fall through to `not_specified`. That
    contradicts the row's own meaning, "nothing in the record constrains L".
  - → T2 item 8.8.
- **R1f vs. the gate.** A role can pass the generation gate only because an anchor
  narrowed its set.
  - The name stage is a superset of the hierarchy stage, so a role that failed the
    gate would still fail without the anchor. Gate failures therefore stay terminal.
  - A role that passed with that anchor's help, when the anchor is later invalidated,
    needs a precedence rule. → T2 item 8.9.
- **R1g vs. §14 agreement.** A generation-gate failure always has `final_set` `[]`.
  Whether it is excluded from the final-set Jaccard, as R9 excludes it from status
  kappa, isn't ruled. → T2 item 8.10.

**Proposed Layer C precedence**, one linkable role (to confirm with T2):
0. A non-linkable label gets the §4 default.
1. A designator unverified everywhere gets `level_mapping_unverified`, with lists
   `null` and no flag.
2. An empty name stage gives `no_match_in_snapshot`.
3. The hierarchy stage runs.
4. The generation gate runs.
5. The PIN stage runs.
6. Independent annotation, then reconciliation.
7. The reconciliation gate.
8. `final_set` = stage + additions − prunings, unless a gate failed, in which case
   it's `[]`. Its size then gives `linked`, `ambiguous` or `no_supported_match`.
9. (R1f) Anchor invalidation, after the Layer C gold is adjudicated.
   - One pass from the top level down, so cascades resolve in one direction.
   - Also run on each annotator's C, for Blocker 9.
   - Part of the Layer C derivation (`candidate_procedure_version`).
   - The dependence test and precedence are open: T2 items 8.6 and 8.9.

Gated lists never feed Layer D.

**T2 / Blocker 8 items** (recommended defaults; the maintainer rules):
- 8.1 `pincode_consistency`: drop "a `conflict` always gives `inconsistent`".
  - A `conflict` with a linked village is already `inconsistent` (the linked unit
    isn't under the PIN).
  - With no village link, it's `not_checkable` by the R4 cause order.
- 8.2 `basis` precedence: `stated` > `inferred_from_descendant` >
  `inferred_from_descendant_candidates` > `inferred_from_pincode`.
  - `conflicting` counts only units from `stated` and `inferred_from_descendant`.
- 8.3 `pincode_role` gap: `decisive` = the previous stage had 2 or more, and the PIN
  stage left exactly the final linked unit. `narrowing` = the PIN stage shrank the
  list in any other way.
- 8.4 A "valid PIN" is exactly one distinct value in the record that normalizes to 6
  ASCII digits with a non-zero first digit (`docs/gazetteer.md` `invalid_pincode`).
  - Repeats of one value count once.
  - Several distinct values mean no valid PIN (R4 cause 1).
  - A valid PIN absent from `village_pincode` is a `pincode_conflict`, not invalid.
- 8.5 Several single-candidate higher roles: the hierarchy stage keeps the
  intersection of their descendant sets.
  - An empty intersection is skipped with `hierarchy_conflict` (existing rule).
- 8.6 (R1f) A role depends on anchor A if removing A from the anchor set changes
  `candidates.hierarchy`.
  - It's computable from generation alone, so no new field is needed.
  - A skipped hierarchy stage depends on no anchor.
- 8.7 A `place_unspecified` role is at L only if `final_set` is non-empty and lies
  entirely at L.
  - A non-empty `final_set` spanning several levels constrains no level, documented
    as a limitation.
  - Effect: a `place_unspecified` role with `no_match_in_snapshot` constrains no
    level, so Layer D gives `not_specified`. `deferred_coverage` is unaffected,
    because it doesn't need a role at L (§8 l.421).
- 8.8 Layer D: `anchor_invalidated` is added to the reasons that give
  `not_in_gazetteer` at L.
  - It's scored only as abstention and reported separately.
- 8.9 A role that passed the gate with an anchor that is later invalidated becomes
  `anchor_invalidated`, with no re-gating (one pass).
- 8.10 Generation-gate failures are excluded from the final-set Jaccard and counted.
  - R1d failures and `anchor_invalidated` roles stay in, because they come from human
    decisions.
