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
T6 (Blocker 6) → T8 (Blocker 3) ← Blocker 1 (decided), T7 (Blocker 10)
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
- T5 ↔ T7: D5.1 (freeze point) and D7.1′ (staging) are both approved and
  consistent. Human screening comes after the freeze and before
  `data/processed/`.
- T7 → T8: human-screen exclusions aren't deterministic, so the D8.1 denylist must
  cover them.
- T4 ↔ T6: D4.4 (publisher missing-value tokens) applies both to split-key columns
  and to `raw_text`.
- T11 waits for every decision. The maintainer asked for one coordinated
  revision, not piecemeal edits.

## Tasks

| ID | Task | Status | Prerequisites | Affected text | Needs from maintainer | Done when |
|---|---|---|---|---|---|---|
| T0 | Workflow files (`CLAUDE.md`, `PROGRESS.md`, this note) | VERIFIED | — | these files | — | CI checks and `git diff --check` pass. Committed. |
| T1 | Close Blocker 2 | VERIFIED (2026-10-28) | — | ADR-0006 §3, §4, §7–§9, §14, F9, F10; ADR-0007 §8, S9 | — (all ruled) | every item ruled. The R1f details were settled with T2 (8.6, 8.9). |
| T2 | Blocker 8: PIN, `basis` and anchor semantics | VERIFIED (2026-10-28) | T1 | ADR-0006 §7–§9, §14 | — (8.1–8.10 ruled) | every case has exactly one outcome (consistency check below) |
| T3 | Blocker 9: Layer D reliability method | VERIFIED (2026-10-28) | T2 | ADR-0006 §1, §14, §15 | — (D3.1–D3.3 ruled) | method computable from stored documents |
| T4 | Blocker 5: split-key inputs | VERIFIED (2026-10-28) | — | ADR-0006 §17 steps 1–2; ADR-0007 §5 | — (D4.1–D4.5 ruled) | two engineers derive the same step-1/2 result |
| T5 | Blocker 4: freeze point, salt, bucket mapping | VERIFIED (2026-10-28) | — | ADR-0006 §17, F5 | — (D5.1, D5.2 ruled) | mapping fully specified; freeze point testable |
| T6 | Blocker 6: `raw_text` eligibility and decoding | VERIFIED (2026-10-28) | — | ADR-0006 §2, §11, L6 | — (D6.1, D6.2, D4.4 ruled) | eligibility decidable from documentation alone |
| T7 | Blocker 10: screening before the split | VERIFIED (2026-10-28) | — | ADR-0006 §12, §14; ADR-0007 §5; ADR-0001 §2 | — (D7.1′ (a) ruled) | no unrecorded pre-split exposure |
| T8 | Blocker 3: withdrawal, denylist, errata | VERIFIED (2026-10-28) | T6, Blocker 1, T7 | ADR-0006 §12, §13, §18 | — (D8.1–D8.4 ruled) | a rebuild can't silently re-admit a withdrawn or human-screen-excluded record, or the limitation is documented |
| T9 | Blocker 7: release-manifest fields | VERIFIED (2026-10-28) | T1–T8 (met) | ADR-0006 §2, §18, §20 | — (D9.1, D9.2 ruled; D9.2 evidence verified) | every version input is listed |
| T10 | Blocker 11: acceptance condition and ordering | VERIFIED (2026-10-28) | T9 (met) | ADR-0006 status line, Consequences; ADR-0007 status line, Consequences; ADR-0008 | — (D10.1, D10.2 ruled) | both ADRs give one consistent order, and acceptance is defined |
| T11 | Coordinated revision: ADR-0006 rev 6, ADR-0007 rev 4 | IN PROGRESS (drafted on branch `adr-0006-rev6`, 2026-10-28; awaiting maintainer review; both ADRs Proposed) | T1–T10 (met) | see "T11 edit map" | review of the drafted diff; acceptance per D10.1 | every ruling incorporated; full diff reviewed; changed decision items re-approved by name; cross-references checked |
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

**Blocker 2: decided (2026-10-27 and 2026-10-28).**
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

- **R1f, option (a).** If a higher-level role's final outcome no longer supports
  the unit it anchored, every lower role that depended on that anchor becomes
  `not_in_gazetteer` / `anchor_invalidated`.
  - No link that depends on the anchor survives.
  - The count is recorded and reported.
  - Procedure: Blocker 8 items 8.5, 8.6, 8.8 and 8.9, and Layer C step 9 below.
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

**Findings from checking the R1f/R1g/R8b rulings against the ADR text**
(the ADRs are unchanged; each gap is closed by the Blocker 8 item named):
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
  kappa, was unruled. → T2 item 8.10.

**Layer C precedence for one linkable role** (decided; still to be written into
ADR-0006 §7 in T11):
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
9. (R1f) Anchor invalidation, run on the adjudicated Layer C (and on each
   annotator's reconciliation C; see 8.10).
   - One pass from the top level down. Every anchor is at a higher level and has
     already been settled, so cascades resolve in one deterministic pass.
   - Part of the Layer C derivation (`candidate_procedure_version`).
   - Anchor A, whose single generated candidate is u, "supports" its anchor only if
     A's final status is `linked` with `entity_id` u.
   - Every role that depends on an unsupporting A (8.6) becomes `not_in_gazetteer` /
     `anchor_invalidated` with `final_set` `[]`. That includes `linked`,
     `ambiguous` and `no_supported_match` roles.
   - Exception: roles that failed either gate keep `level_mapping_unverified`,
     because a gated outcome is terminal (R1g).

Gated lists never feed Layer D.

**Blocker 8: decided 2026-10-28** (all ten defaults accepted as specified):
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

**Consistency check of the Blocker 8 rulings with R1f, Layer D and §14.**
These are consequences of rulings already made, not new decisions.
- **8.5 + 8.6:** removing a redundant anchor (a state whose district also anchors)
  leaves the intersection unchanged, so nothing depends on it.
  - When the last anchor is removed, the comparison is with `candidates.name`.
  - Removing a constraint only grows the intersection, so a dependence test can
    never turn a stage into a skip.
- **R1f + 8.7:** an `anchor_invalidated` `place_unspecified` role has an empty
  `final_set`, so it is a role at no level.
  - Layer D treats it like any other unlinked `place_unspecified` role
    (`not_specified` unless something else constrains L).
  - It still appears in the R1f count.
  - 8.8 applies to labelled roles at L.
- **8.8 + §8 order:** `not_in_gazetteer` (now including `anchor_invalidated`) still
  comes before `deferred_coverage` in the existing first-match order. No existing
  precedence changes.
- **R1f audit:** the set a role had before invalidation isn't stored, because the
  `not_in_gazetteer` invariant requires an empty `final_set`. It can be rebuilt
  from the stored stages, additions and prunings, so no new field is needed.
- **8.10 + step 9:** the final-set Jaccard compares each annotator's
  reconciliation `final_set` after invalidation has been applied to that
  annotator's C.
  - Generation-gate failures are identical for every annotator, so they're excluded
    and counted.
  - R9's status kappa uses the independent round, which comes before invalidation,
    so it's unaffected.
- **8.1 + 8.3 + 8.4:** a valid PIN absent from `village_pincode` gives
  `pincode_conflict`. A linked village then gives `inconsistent`, and no village
  link gives `not_checkable` (R4 cause 2 if the village level is
  `deferred_coverage`, otherwise cause 3).
  - The PIN never anchors and never sets verification scope.

## T3–T7 workstream (2026-10-28)

Labels:
- **Spec** is derived from approved rules or existing ADR text. It's recorded under
  existing authority, and the maintainer may override it.
- **D** is a decision request. Rulings are in "T3–T7 rulings" at the end of this
  section. Every D was accepted. D7.1 was superseded by D7.1′ (a), staging.
- Nothing here is in the ADRs yet (T11).

### T3: Blocker 9, Layer D reliability (ADR-0006 §1, §13, §14, §15)

**Facts.**
- §14 says to "derive D from each annotator's independent A and C".
- Independent C is done on **gold** spans (§3, §7). An annotator's own A spans can't
  be joined to their C entries, so the A half of that sentence can't be computed.
- Independent C sees no generated lists (§13, F13), and `final_set` exists only
  after reconciliation. So `ambiguous` has no stored set per annotator today.

**Spec.**
- Entries that R9 classes as mechanical take the generated outcome, identical for
  both annotators, wherever per-annotator C is assembled:
  - non-linkable defaults
  - designators unverified everywhere
  - generation-gate failures
- R1f (anchor invalidation) does not apply to independent C. Anchors are a property
  of generation, and independent annotators never see generated lists.
  - So per-annotator D can differ from gold D for that reason. That is acceptable,
    because the agreement compares annotators with each other, not with gold.

**D3.1 Inputs.**
- *Recommended:* gold A + each annotator's independent C (with the substitutions
  above), the cue table and the pinned gazetteer. The §8 procedure is run once per
  annotator.
- Agreement per level L:
  - kappa on `levels.L.status`
  - exact `entity_id` agreement where both are `linked`
  - Jaccard on `candidates` where both are `ambiguous` or both `conflicting`
  - `basis` agreement where both are `linked`
- *Alternative:* reconciliation C (after invalidation). It is complete, but it was
  made after exposure to the generated lists, so it isn't independent (F13).
- *Risk:* the change in wording drops "independent A" from §14. A's own reliability
  is still measured by span F1 (§14).

**D3.2 What independent C stores.**
- *Recommended:* when the status is `ambiguous`, the annotator records
  `independent_set`, the complete sorted list of units found by their own lookups,
  with at least 2 members.
- `linked` stores only `entity_id`. `not_in_gazetteer` stores only `reason`.
- That is the minimum data needed to rerun D3.1.
- *Burden:* listing every sibling. Lookups already show all matches, so this is
  recording, not search.
- *Schema:* a new field in independent C documents (`docs/schema.md`, T12).
- *Alternative:* no set, which leaves per-annotator `ambiguous` uncomputable.

**D3.3 Adjudication `merge` for candidate sets.** No default has been approved yet.
- **Union**, defined on edits: generated stage + (A₁ ∪ A₂ additions) − (P₁ ∩ P₂
  prunings). This equals the union of the two `final_set`s for roles that pass the
  gate.
  - It keeps any unit either annotator supported.
  - Over-inclusion tends to produce `ambiguous`, never a false `linked`.
- **Intersection:** a unit kept by only one annotator is dropped. That can collapse
  {a, b} ∩ {a} to {a}, a **false unique link**. Not recommended.
- **Explicit:** the adjudicator decides each disputed member with a P7 reason. That's
  already available as `replace`.
- *Recommended:*
  - `merge` = union on edits, followed by the reconciliation gate (R1d) and anchor
    invalidation (step 9). The adjudicator may then apply `replace` with structured
    prunings or additions.
  - Defined behaviour:
    - both empty → `[]`
    - {a} and {b} → {a, b} → `ambiguous`, unless a reasoned pruning follows
    - an out-of-scope addition by either annotator → R1d failure
    - a missing annotation → `merge` is not available; only `accept` or `replace`
  - Gated roles are never adjudicated, because they are terminal.
- This changes adjudication semantics, so it **needs the maintainer**.

**Status:** VERIFIED 2026-10-28 (see "T3–T7 rulings"). No dependency on T4–T7.

### T4: Blocker 5, split-key inputs (ADR-0006 §17 steps 1–2, ADR-0007 §5, §12)

**Facts.**
- `context_columns` lists names only. Nothing assigns a column to a role (state,
  district).
- The research notes list *possible* context columns from platform field lists, not
  file headers:
  - C1a `State`/`District`; C1b `State_Name`/`District_Name`; C2 `State Name`/
    `District Name`; C4 `State`/`District`
  - no file has been inspected (B6)
  - whether platform field lists count as publisher documentation is unconfirmed
    (`focus-state-source-evaluation.md`, "Procedural position")
- The publishers document missing-value markers ("NA/Blank: Not Available" for C1a
  and C1b; "NA: Not Available" for C2 and C3; same file, "B6 aggregate
  inspection").
  - `name_key("NA")` is `"na"`, so under the rule "has a value ⇔ `name_key(v) != ""`"
    an `NA` state cell counts as a value. It is then excluded as
    `state_column_unmatched` instead of being treated as missing.
  - **This conflicts with the publisher's own semantics.** → D4.4
- `name_key` maps punctuation and symbols to spaces (`src/pata/normalize.py`). So a
  source value written with "&" never equals a gazetteer name written with "and".
  Exact matching rejects such spelling variants. → D4.1

**Spec.**
- The manifest declares each split-key column's role: `state_column` and
  `district_column`, at most one column per role, each listed in `context_columns`.
  - That's required information. Field names belong to `docs/schema.md` (E3).
  - Without a declared role a column is not used by the split key, whatever its name.
- Tokens are `name_key(raw_text).split(" ")`. A whole-token sequence matches when
  the district's `name_key` tokens occur contiguously.
- Step 2 rule order decides between column and text: a matching district column
  wins. Disagreements between column and text are counted per source and never
  change the key.
- Text rule 2 needs exactly one district. Zero, or two or more distinct districts,
  means no district from text.
- Repeated runs give the same key. Every input is pinned: the manifest content, the
  alias table (if any), the gazetteer, `split_key_procedure_version` and the
  `name_key` code with its Unicode version (T9).
- Missing districts don't put unrelated records in a new kind of group.
  - They fall into `unresolved:lgd:state:{code}` or `unresolved:unknown` by
    existing design. That is one group per state, which P6 already has to bound.
  - The earlier non-blocking note recommends a maximum share for a single group.

**D4.1 Alias table.**
- *Recommended:* allowed, per source and versioned, for state and district columns
  only.
- Each entry is: exact `name_key` of a source value → one `lgd:` ID.
- Evidence:
  - a scripted distinct-value list with counts for that column (an aggregate
    statistic, allowed under ADR-0007 §5)
  - the LGD unit's name
- Every entry is approved by the maintainer and recorded with the source
  assessment. No fuzzy matching.
- A change after the first split is a change to the source set (ADR-0007 §7).
- *Alternative:* no aliases. Every spelling variant is then excluded as
  `state_column_unmatched`, which loses coverage silently by source style.

**D4.2 Evidence for assigning a column role.**
- *Recommended:* publisher documentation naming the field's content, plus a
  scripted aggregate exact-match rate against LGD names (reported, no threshold).
- Platform field lists count as documentation only once the maintainer confirms the
  pending "Procedural position" question.
- A column name alone is never enough.

**D4.3 Several state-like columns.**
- *Recommended:* exactly one declared `state_column`. Other state-like columns are
  not used for split keys.

**D4.4 Missing values.**
- *Recommended:* a value is present if `name_key(v) != ""` **and** `name_key(v)`
  isn't in the source's declared `missing_value_tokens`.
  - The tokens must be cited from publisher documentation (for example `na`,
    `blank`).
  - Tokens apply to split-key columns and to `raw_text` (T6).
- This amends the earlier mechanical rule, so it **needs the maintainer**.

**D4.5 District-column rules.**
- (a) The column has a value and matches nothing within the known state.
  - *Recommended:* the district is unknown, with **no fall-through to text**. It's
    counted as `district_column_unmatched`, and the record is kept with key
    `unresolved:lgd:state:X`.
  - *Alternative:* the current text implies falling through to text matching. That
    lets text override the publisher's own field.
- (b) The state is known.
  - *Recommended:* match only within that state, never across India.
  - Matching across India "if the match is unique" applies only when the state is
    unknown.
  - Otherwise a cross-state district would contradict step 1.

**Status:** VERIFIED 2026-10-28 (see "T3–T7 rulings", including the D4.4 wording).

### T5: Blocker 4, freeze point, salt, bucket mapping (ADR-0006 §17, F5)

**Facts.**
- §17 says the split is "frozen before any model experiment", and a recompute is
  allowed "only to fix a bug".
- Annotation and the pilot happen before any model experiment.
- The salt has no provenance rule.

**Spec: bucket mapping**, complete. The ratio values stay P6.
1. Step-5 holdout assignment happens first (existing order). Hashing applies only to
   the remaining classes, keyed by the class key (Blocker 1).
2. Message: `group_key + "\n" + split_salt`, encoded UTF-8, with no BOM and no
   trailing newline. `split_salt` is its 64-character lowercase hex string.
3. `h` = the first 8 bytes of SHA-256(message), read as an unsigned big-endian
   integer, 0 ≤ h < 2⁶⁴.
4. Ratios are positive integer weights `w_train`, `w_dev`, `w_test`, with W =
   their sum.
5. `b = (h × W) >> 64`, exact integer arithmetic with no floats, so 0 ≤ b < W.
6. Intervals are half-open, in the fixed order train, dev, test:
   - `train` if b < w_train
   - `dev` if b < w_train + w_dev
   - otherwise `test`
7. A zero weight is not allowed (configuration error).

**Synthetic test vectors**, computed 2026-10-28 with `uv run python -I` on a
scratch script. These are not benchmark data.
- Salt = SHA-256 hex of the ASCII bytes `pata synthetic test-vector salt` =
  `c2486d9637f8cc990bec2ea16a39999692387fdddd099c55df427bc6c8745b2a`.
- Weights 8/1/1 (synthetic, not P6).

| key | h (hex) | bucket |
|---|---|---|
| `synthetic:a` | `63b6c9c4c2b75d54` | train |
| `synthetic:b` | `f5f0f6a861bb0d63` | test |
| `synthetic:c` | `53526df4c6a3e805` | train |
| `synthetic:d` | `8c1fd55acbb2aebd` | train |
| `synthetic:e` | `82e0dbc2971e8e64` | train |
| `synthetic:f` | `f818bbf49755ac7b` | test |

Boundaries (weights 8/1/1):

| h | bucket |
|---|---|
| `0000000000000000` | train |
| `cccccccccccccccc` | train |
| `cccccccccccccccd` | dev |
| `e666666666666666` | dev |
| `e666666666666667` | test |
| `ffffffffffffffff` | test |

The script asserted all four boundary transitions. A future implementation must
reproduce this table (T12).

**Spec: consequence of Blocker 1 and the freeze.**
- A record removed after the split (by a later screen or withdrawal) can change its
  duplicate class's smallest key, and so the bucket of the other members.
- Freeze rule: assignments are fixed per `record_id` at first computation. Removing
  a record never recomputes another record's key or split.
- This matches "never moves records after the split is frozen".

**D5.1 Freeze point.**
- *Recommended:* the split is computed and frozen **before the first human exposure**
  of any admitted record's text. Exposure means screening, pilot, guideline work or
  annotation.
- An exposure log is kept from then on: record or class, person pseudonym, purpose,
  date.
- A later bug-fix recompute (new `split_version`) may never move an exposed record
  into `test` or `test_source_holdout`.
- Must be decided with D7.1.
- *Alternative:* the current "before any model experiment". It allows recomputes
  after people have read records.

**D5.2 Salt.**
- *Recommended:*
  - 32 bytes from the operating system's cryptographic random generator, generated
    once, before the first ingestion run that computes splits
  - committed to the versioned split configuration before that run
  - immutable for that `split_version`
  - published with the release (it isn't secret; test gold is protected separately)
  - never regenerated after any split result has been seen
- A new salt means a new `split_version`, and it is recorded with its reason.
- *Alternative:* a salt derived from a public value (for example, a commit hash).
  That is reproducible but predictable before commitment.

**Status:** VERIFIED 2026-10-28 (see "T3–T7 rulings").

### T6: Blocker 6, `raw_text` eligibility and decoding (ADR-0006 §2, §11, L6)

**Facts.**
- No candidate source file is held locally (B6). So no field's eligibility can be
  verified at file level now, for any source.
- Per-candidate state, from documentation only:

| Source | Field (documented) | Eligibility now | Evidence gap |
|---|---|---|---|
| C1a | `Address_Original_First_Line` | can qualify as `address_line` (D6.1); pending | publisher documentation ("Procedural position"); file header; licence (B14) |
| C1b | `Address` | single string per schema; pending | licence (B15); file |
| C2 | `Facility Address` | single string per schema; pending | licence (B14); file |
| C3 | `DiagnosticCentreAddress` | single string per schema; pending | licence (B14); file; no state (O4) |
| C4 | none (components only) | not `raw_text` under rev 5 strict rule (L6) | L6 |
| C5 | PDF lists | not `raw_text` under rev 5 (L6) | L6; licence (B4) |
| C6 | search form, field [U] | pending | licence (B4); no bulk file |
| C8–C12 | [U] | pending | per inventory |

  None of these is accepted, and none is rejected here.

**Spec: decoding.** Each source ADR fixes these per source, under a new
`ingestion_procedure_version` (recorded in the release manifest, T9).
- **Encoding** is declared from publisher documentation or the file's own
  declaration. No guessing.
  - Decoding is strict, with no replacement characters.
  - A row that fails to decode is excluded as `undecodable`.
- **BOM:** one leading U+FEFF at the start of the *file* is removed before parsing.
  It is file encoding, not field content. U+FEFF inside a field stays as published.
- **CSV:** the RFC 4180 dialect, with the delimiter and quote character declared.
  - Quoted embedded newlines are part of the value, and `raw_text` keeps them.
  - A row with the wrong field count is excluded as `malformed_row`.
- **XLSX:** a `raw_text` cell must be a text cell. A numeric, date or formula cell
  is excluded as `non_text_cell`, because formatting it would invent text.
  - Context columns: an integer-valued numeric cell becomes its decimal string.
    Any other numeric value counts as no value.
- **Empty values:** `raw_text` that is empty or entirely whitespace (`str.isspace()`)
  is excluded as `empty_raw_text`.
  - A value matching a declared missing token (D4.4) is excluded as
    `missing_value_token`.
  - No trimming otherwise (§2).
- **Counts:** each reason is counted per source at ingestion, alongside the §17
  reasons, and never summed across reasons.

**D6.1 Partial address lines.**
- *Recommended:* a field qualifies when publisher documentation presents it as the
  facility's address or an address line.
  - The manifest records `raw_text_scope: full_address | address_line`.
  - `address_line` is reported as its own stratum.
  - Layer D for such records will often be `not_specified`, which is honest.
- *Alternative:* only fields documented as the full address qualify. C1a then
  contributes nothing.
- Never decided from the values themselves.

**D6.2 Duplicate native IDs within one snapshot.**
- A `record_id` collision.
- *Recommended:* exclude every row that shares the ID, as `duplicate_native_id`,
  counted.
- *Alternative:* demote the whole source to `snapshot` scope.

**Status:** VERIFIED 2026-10-28 (see "T3–T7 rulings"). File-level checks wait for B6 and
the licences, not for T6.

### T7: Blocker 10, screening and test exposure (ADR-0006 §12, §14; ADR-0007 §5)

**Facts.**
- ADR-0007 §5 says no person reads records before the split, because the maintainer
  writes the guidelines and cue table, and reading would expose future test records.
- ADR-0006 §12 says the screen runs "before anything reaches `data/processed/`", so
  before the split. A person may screen (`screened_by`, §14).
- ADR-0006 §14 allows guideline examples "from admitted records", which includes
  test.
- ADR-0006 §3 already says the cue table comes from **dev-pool** observation.
- Test records must be read by their annotators (§15, double annotation).
- So the goal can't be "nobody sees test". It is: nothing *derived from* test
  reaches the guidelines, the cue table or model choices.

**Controls that actually protect test**, as opposed to logging:
- freezing the guidelines and cue table before any test record is annotated
  (§14 already freezes the guidelines before gold annotation)
- dev-only examples and observations
- assigning splits before anyone reads records
- reporting under the frozen versions

The exposure log only makes breaches visible.

**D7.1 When humans screen.**
- *Recommended (a):*
  1. A rules-only screen (`rule:{name}`) before the split.
  2. The split is computed and frozen (D5.1).
  3. Human screening happens after the split. For dev and train it can be done by
     anyone. For test and `test_source_holdout` it's done only by people who don't
     write or change the guidelines or cue table.
  4. A record failing the human screen is excluded after the split, without moving
     other records (T5 spec).
- *Alternative (b):* allow human screening before the split, log it, and report the
  exposure.
- *Alternative (c):* screeners may never write the guidelines or cue table.
- (a) changes the §12 order ("before `data/processed/`") for the human part, so it
  is a semantic change.

**D7.2 Guideline examples.**
- *Recommended:* dev pool only.
- Amends §14 "from admitted records". This matches §3 for the cue table.

**D7.3 Accidental exposure.** A test or holdout record seen by someone who writes
guidelines or the cue table, outside test annotation.
- *Recommended:*
  - log it
  - keep the record in place (no moves after the freeze)
  - flag its duplicate class as `exposed`
  - report test metrics with and without exposed classes
  - any guideline or cue-table change made after an exposure, by the exposed person,
    must cite only dev or train evidence
- *Alternative:* drop exposed classes from test scoring altogether.

**Interactions:**
- Duplicate classes: exposure is tracked per class, because members share text.
- Publisher holdout: `test_source_holdout` is treated like `test`.
- Withdrawal: T8, not started.

**Status:** VERIFIED 2026-10-28. D7.1′ (a), staging, was ruled; D7.2 and D7.3 are
accepted (see "T3–T7 rulings").

### Cross-task consistency (checked 2026-10-28)

- Decided together: D5.1 + D7.1 (freeze vs. screening order), D4.4 (T4 and T6),
  and Blocker 1 + the T5 spec (fixed per-record assignment).
- T3 needs nothing from T4–T7.
- No T3–T7 item touches the Blocker 2 or Blocker 8 rulings, except D3.3, which reuses
  R1d and step 9 unchanged.
- No ADR, code, dataset or split was changed or created.

### T3–T7 rulings (maintainer, 2026-10-28; not yet in the ADRs)

**Accepted as recommended above:** D3.1, D3.2, D3.3, D4.1, D4.2, D4.3, D4.5, D5.1,
D5.2, D6.1, D6.2, D7.2, D7.3.

**D4.4, accepted with explicit wording:**
- Publisher-documented missing-value tokens are recognized **before** the generic
  presence rule `name_key(v) != ""`.
- The token list is per source and per column, cited from publisher documentation,
  and versioned with the manifest.
  - It applies to split-key columns, and to `raw_text` only where the publisher
    documents the token for that field.
- `NA` is not a value where the publisher defines it as "Not Available".
- Source values are never rewritten. `source_context` keeps the value as published,
  and presence is derived.

**D7.1: not recorded; it conflicted with ADR-0001 §2 (Accepted).** Resolved by the
D7.1′ (a) ruling below. This paragraph is kept as the record of the conflict.
- ADR-0001 §2: "If a public source contains them [names of individuals, phone
  numbers, emails, ID numbers], they are removed during ingestion, before anything
  is written to `data/processed/`."
- D7.1 puts human screening *after* the split. But the split step writes retained
  records to `data/processed/` (ADR-0006 §17 step 1, ADR-0007 §3).
  - So an identifier that only a human would catch is in `data/processed/` *by
    design* before the human screen runs.
- ADR-0006 §12's withdrawal mechanism already tolerates *accidental* misses. D7.1
  would make it planned.
- Options (**D7.1′**, needs the maintainer):
  - (a) **Staging, recommended.**
    1. Rules-only screen.
    2. Split computed and frozen in a staging area outside `data/processed/` (for
       example `data/interim/`, ignored by git like `data/*`).
    3. Role-restricted human screen on the staged records (D7.1 restrictions
       unchanged).
    4. Only records that pass are written to `data/processed/`.
    - This satisfies ADR-0001 §2 literally, keeps D5.1, and makes "ingestion" end
      at the write to `data/processed/`.
  - (b) A new ADR superseding ADR-0001 §2's timing. Accepted ADRs are never
    rewritten.
  - (c) Human screening before the split. **Contradicts the approved D5.1**, so not
    viable without reopening D5.1.

**Derived consequences** (no new decisions; recorded for T11, overridable):
- **T3, metric scope.**
  - Agreement uses only records with two independent C documents (dev pool, §14).
  - A status disagreement at L is counted only by the status kappa.
  - `entity_id`, Jaccard and `basis` comparisons apply only to pairs with the same
    status.
  - `reason` agreement is reported for pairs that are both `not_in_gazetteer` or
    both `deferred_coverage`.
- **T4, order inside a column.**
  1. Missing token (D4.4).
  2. Alias (D4.1).
  3. Exact LGD `name_key` match.
  - An alias entry for a value that already matches LGD exactly is invalid.
- **T4, ambiguous district column.** A district column that matches **more than
  one** district (state unknown, India-wide not unique) is handled like D4.5(a).
  - The district is unknown, with no fall-through to text, counted as
    `district_column_ambiguous`.
  - Same rationale as D4.5: text must not override the publisher's field.
- **T5, what "first human exposure" means:** a person viewing `raw_text` or
  `source_context` values of an individual record.
  - Scripted aggregate statistics and the D4.1 distinct-value lists for state and
    district columns are not exposure (ADR-0007 §5).
  - So aliases can be approved before the split.
- **T5 + D7.1:** whatever D7.1′ decides must keep human exposure after the split
  (D5.1 is approved).
- **T6, C1a.** `Address_Original_First_Line` can qualify as `address_line` (D6.1),
  but only on publisher documentation, which needs the pending "Procedural
  position" confirmation or other documentation.
  - It is still pending, with that gap and B6/B14 named.
- **T8 readiness.** Its listed prerequisites (T6, Blocker 1, and T7 since D7.1′)
  are met. Decision requests D8.1–D8.4 have been prepared, below.
  - Post-split exclusion of a withdrawn record uses the T5 fixed-assignment spec.
  - Where withdrawals happen relative to `data/processed/` should be decided
    together with D7.1′.

**Acceptance criteria re-check:**
- **T3 VERIFIED.**
  - Inputs are defined (D3.1).
  - The minimum stored data is defined (D3.2), with the schema field deferred to
    T12.
  - Merge is deterministic (D3.3).
  - Every status pair and set comparison is defined (derived above).
  - It is recomputable from stored documents.
- **T4 VERIFIED.**
  - Every step-1 and step-2 case has one outcome: state column present, missing
    token, alias, unmatched, disagreement with `coverage_state`, absent; district
    column matched, missing token, unmatched, ambiguous, absent; text matching
    0, 1 or more districts.
  - The inputs are pinned.
- **T5 VERIFIED.**
  - The freeze point is observable (exposure defined, log kept).
  - Salt provenance and immutability are defined.
  - The mapping is complete, with boundaries and vectors.
- **T6 VERIFIED.**
  - Every candidate field has a decision or a named gap.
  - Decoding is versioned.
  - Malformed, missing and empty inputs are handled explicitly.
  - Counts are per reason.
  - No source is accepted.
- **T7 VERIFIED** (after D7.1′, below).
  - Screening stages and who may access what are defined.
  - Exposure is logged from the first human screen.
  - Guideline and cue-table contamination is controlled (D7.2, the §14 freeze, §3
    dev-pool observation).
  - Accidental exposure has a disposition (D7.3).
  - It is consistent with T4 and T5.
  - No split was generated.

### D7.1′ ruling: staging (maintainer, 2026-10-28)

**Approved: option (a).** The ingestion order is:
1. **Rules-only privacy screen** (`screened_by: rule:{name}`), in its versioned
   form.
2. The split is **computed and frozen in an ignored staging area outside
   `data/processed/`**, such as `data/interim/`.
   - `data/*` is already in `.gitignore`, so staging is never committed.
3. **Role-restricted human screen** on the staged records, after the freeze. The
   D5.1 exposure rules apply, and the exposure log starts here.
   - Dev and train can be screened by anyone.
   - Test and `test_source_holdout` are screened only by people who don't write or
     change the guidelines or cue table (D7.1).
4. **Only records that pass** are written to `data/processed/`.
5. A failed record is excluded. No other record's frozen assignment is recomputed
   or moved (T5 spec).
   - Withdrawal and duplicate-class handling follow the existing rules, and T8.
6. Personal identifiers are therefore removed before any record enters
   `data/processed/` (ADR-0001 §2).

**Consistency check (no conflicts found):**
- **ADR-0001 §2 (Accepted):** satisfied as written. Nothing that fails a screen
  reaches `data/processed/`.
  - Staging holds rules-screened records on local disk, like the pinned raw
    snapshots already do (ADR-0004). It is never committed and never released.
  - Derived: staging holds only `raw_text` and allowlisted `source_context`
    (ADR-0006 §12: "Nothing outside the list is ingested").
- **ADR-0006 §12:** the human screen still runs "before anything reaches
  `data/processed/`".
  - "Excluded records are not stored": derived, a failed record is deleted from
    staging after the screen and only per-rule counts are kept.
  - The §12 withdrawal mechanism stays for records the human screen also misses.
- **ADR-0006 §17 and ADR-0007 §3:**
  - the split is still computed at ingestion, before annotation
  - step-1 and out-of-focus exclusions are still never written to
    `data/processed/`
  - the split file in `data/processed/` lists only records that passed
- **ADR-0007 §5:** no person reads records before the split.
- **D5.1:** the first human exposure, the human screen, comes after the freeze.
  - A later bug-fix recompute can't move a screened (exposed) record into `test` or
    `test_source_holdout`.
- **D7.3:** screening of test by non-authors is logged exposure, not "accidental
  exposure", which D7.3 defines as exposure of a guideline or cue-table author.
- **Blocker 1:**
  - Removing a failed member leaves the frozen assignments of the other class
    members unchanged.
  - Whether a failure cascades to the whole duplicate class is D8.2. Until it is
    ruled, only the failing record is excluded.
- **Blocker 2 and Blocker 8:** no interaction. Annotation layers start only on
  records in `data/processed/`.
- **Practical constraint** (a consequence, not a decision): test and holdout records
  can be screened only by someone who doesn't write the guidelines or cue table.
  Until such a person is available, those records can't be written to
  `data/processed/`.
- **New coupling to T8.** A human screening decision isn't deterministic.
  - A rebuild from the same snapshot and `screen_version` would re-admit records
    that failed the human screen, just as it would re-admit withdrawals.
  - Recording human-screen exclusions is therefore part of D8.1.

### T8: Blocker 3, withdrawal, denylist, errata (ADR-0006 §12, §13, §18) — decision requests

**Facts.**
- §12, withdrawal before release: the record and all its annotations are deleted.
  "Only the count of withdrawals is logged, because `record_id` is derived from
  source data."
- §13: annotation documents are immutable ("nothing is overwritten"), and
  withdrawal deletes them. The exception isn't stated.
- §18:
  - a release is immutable
  - the manifest has an `errata` field ("errata entries that affect this
    release")
  - errata entries never contain text, `record_id` or hashes
  - withdrawal makes a new release without the affected records
- **The gap.** Rebuilding from the pinned snapshot with the same `screen_version`
  re-admits:
  - withdrawn records
  - D7.1′ human-screen exclusions
  - textual duplicates of a withdrawn record, whatever their source
- L1 (stand-off or shipping `raw_text`) is undecided.

**Derived** (no ruling needed; overridable):
- §13 gets an explicit exception: withdrawal is the only deletion of annotation
  documents.
- A withdrawal after the freeze never moves another record (T5 spec, D7.1′ step 5).

**D8.1 Durable record of exclusions (denylist).**
- *(a) Recommended: an internal, unreleased denylist.*
  - Each entry: `source_id`, `source_record_ref`, `raw_text_sha256`, a reason
    category, the date.
  - It is applied as a screen rule, so every change bumps `screen_version`.
  - It covers withdrawals and human-screen exclusions.
  - It is kept in private maintainer storage: never in git, never released.
  - External stand-off rebuilds are protected another way: a release lists its
    member records, so a withdrawn record is absent from the next release's list.
    That depends on L1.
  - This **changes §12's** "only the count ... is logged".
- *(b) A published keyed-hash denylist.*
  - With a public key, anyone holding the source can identify the record. That
    defeats §18's no-hashes rule.
  - With a secret key, outsiders can't apply it.
- *(c) No denylist, with the limitation documented.* Rebuilds silently re-admit
  excluded records, and human-screen decisions can't be reproduced.

**D8.2 Cascade to the duplicate class.**
- *Recommended:* a withdrawal or human-screen failure excludes the record's whole
  duplicate class (identical `name_key(raw_text)`, Blocker 1).
  - `name_key` keeps letters and digits, so a personal name or phone number in one
    member's text is in every member's.
  - It is counted separately.
  - A failure caused only by `source_context` stays per record, because context
    differs between members.
- *Alternative:* per record only, with the class flagged for re-screening.

**D8.3 Where errata live.**
- *Recommended:* an append-only errata log outside releases (for example
  `docs/errata.md` in git).
  - Entry: date, affected release versions, reason category, number of records
    removed. No text, `record_id` or hashes (§18).
  - The `errata` field of a release manifest lists only the entries known at
    publication, meaning the ones that release fixes. The log, not the manifest,
    says which earlier releases an entry affects. Releases stay immutable.
- *Alternative:* a mutable manifest field, which breaks immutability.
- *Alternative:* release notes only, which give no single place to look.

**D8.4 Exposure-log entries of excluded records.** The D5.1 exposure log holds
record or class identifiers.
- *Recommended:* the entries are kept in the same private store as the D8.1
  denylist and are released only as counts.
- *Alternative:* replace them with counts at exclusion, which loses the exposure
  audit for those classes.

**Status:** VERIFIED 2026-10-28 (see "T8 rulings").

### T8 rulings (maintainer, 2026-10-28; not yet in the ADRs)

**Accepted exactly as recommended:** D8.1 (a), D8.2, D8.3, D8.4.
- **D8.1 denylist.**
  - Internal and unreleased, in private maintainer storage. Never committed, never
    released.
  - It covers withdrawals and D7.1′ human-screen exclusions.
  - Fields: `source_id`, `source_record_ref`, `raw_text_sha256`, a reason category,
    the date.
  - It is applied as a versioned screen rule, and every change bumps
    `screen_version`.
- **D8.2.** Withdrawals and human-screen failures exclude the whole Blocker 1
  duplicate class, counted separately. A failure caused only by `source_context`
  stays per record.
- **D8.3.** An append-only errata log outside releases (for example
  `docs/errata.md`).
  - Entries have no raw text, record IDs or hashes.
  - Each release manifest lists only the entries it incorporates.
- **D8.4.** Individual exposure-log entries are kept in the same private store as
  the denylist. Only aggregate counts are published.

**Consistency check** (ADR-0001 to ADR-0008, Blockers 1, 2 and 8, D5.1, D7.1′, the
fixed-assignment rule): **no conflicts found.**
- **ADR-0001 §2:** the denylist and exposure log are data and are never committed
  (§2, last bullet).
  - An entry points to a row in a public source snapshot that is already held
    locally. It adds no personal data beyond that snapshot, and it holds no text.
- **ADR-0002 l.70** (a GODL-India provider may withdraw the licence for a dataset):
  a different kind of withdrawal, which errata could record. See the gap below.
- **ADR-0003, ADR-0004, ADR-0005, ADR-0008:** nothing on withdrawal, errata,
  screening or exposure.
- **ADR-0006 §12** ("only the count of withdrawals is logged"): changed by D8.1, as
  the request stated. Wording change in T11.
- **ADR-0006 §18:** errata without text, IDs or hashes is unchanged.
  - The manifest's `errata` field changes from "entries that affect this release"
    to "entries this release incorporates". Wording change in T11.
- **Fixed assignment and Blocker 1:** every member of a class shares the class key
  and so the same split. A cascade removes the whole class and moves no one else.
- **D7.1′:** a human-screen failure in staging deletes the whole class from staging
  (D8.2) and adds denylist entries. Only passing records reach `data/processed/`.
- **D5.1, D7.3:** "with and without exposed classes" reporting uses the counts
  D8.4 allows.
- **Blockers 2 and 8:** anchors and Layer D are per record, so deleting a record's
  annotations changes no other record's gold.

**Derived** (no new decisions; recorded for T11, overridable):
- **§13 exception:** withdrawal is the only case where annotation documents are
  deleted.
- **Matching.**
  - A denylist entry matches a record when `source_id`, `source_record_ref` and
    `raw_text_sha256` are all equal (the recorded fields, read as one key).
  - D8.2 then excludes the matched record's whole duplicate class in that build.
  - Rebuilds from the same pinned snapshots are therefore deterministic.
- **Limitation (documented, not solved):**
  - A new snapshot can drop the original row or change its text (a `native` ID
    with new text). A duplicate of a withdrawn text may also appear in another
    source while the original row has gone.
  - In those cases no entry matches. Such records are caught only by the human
    screen, which every new ingestion runs (D7.1′).
  - External stand-off rebuilds depend on release membership lists (L1).
- **Gap: the reason-category list isn't defined.** The values are a format for
  `docs/schema.md` (T12). Candidates include personal data, licence withdrawn
  (ADR-0002 l.70) and source error. Nothing is chosen here.

**T8 acceptance check:**
- A same-snapshot rebuild can't re-admit a withdrawn or human-screen-excluded record:
  the denylist runs as a screen rule, and the class cascades.
- The cases that remain are documented as limitations.
- The cascade, the errata location and the exposure-log retention are each defined.
- **VERIFIED.**

### T9: Blocker 7, release-manifest fields (ADR-0006 §2, §18, §20) — decision requests

**Facts.** The §18 table lacks:
- the source manifest content
- `normalization_procedure_version` (§6 calls the procedure "versioned", but there
  is no field)
- an ingestion procedure version
- `focus_state_version` (ADR-0007 §2: "recording ... is a follow-up")
- the code and Unicode versions that `name_key` depends on
- a data source for `scripts`
- rules for `benchmark_version`

**Spec: required fields, derived from approved rules.** Field names and format
belong to `docs/schema.md` (E3).
- `sources`: for each source, the SHA-256 of its **manifest content** next to the
  snapshot SHA-256.
  - The manifest carries everything that changes splits: `coverage_state`,
    `context_columns`, column roles (T4), the alias table (D4.1),
    `missing_value_tokens` (D4.4), `raw_text_scope` (D6.1), `record_id_scope`.
- `ingestion_procedure_version` (T6 decoding).
- `normalization_procedure_version` (§6).
- `focus_state_version` (ADR-0007 §2).
- The split configuration: `split_version`, `split_salt` (D5.2), the held-out
  publisher list, and the **ratio weights** (P6 values, T5 mapping).
- Code provenance:
  - the Pata git commit
  - the Python version
  - `unicodedata.unidata_version`, because `name_key` and the Script property
    depend on it (T4: repeated runs give the same key)
- `screen_version` (exists). It already identifies the denylist state (D8.1); no
  denylist hash or contents are published.
- `errata`: the entries this release incorporates (D8.3).
- Published aggregate counts go in a release report listed in `files` with its
  SHA-256, not in the manifest:
  - exclusions per reason (T6, §17)
  - cascades (D8.2)
  - exposure (D7.3, D8.4)
  - `anchor_invalidated` (R1f)
  - mechanical statuses (R9, 8.10)
- Unchanged: L1 (`licence`, `attribution`) stays with the release ADR.

**D9.1 `benchmark_version` rules.**
- *Recommended:*
  - **MAJOR** for anything that makes scores not directly comparable (§18 point
    4): any change to records (additions, withdrawals), to splits (`split_version`),
    to `gazetteer_version` (§10 migration), or to gold semantics (labels, statuses
    including a new Layer D status, procedures that change gold).
  - **MINOR** for additive release content that changes no gold, split or record
    (for example a new derived stratification field, or new report counts).
  - **PATCH** for documentation or packaging fixes where every gold and split file
    keeps the same SHA-256.
- This **conflicts with §20's current wording**, which allows a new Layer D status
  as a minor version. The earlier non-blocking note flagged this. Changed in T11 if
  accepted.
- *Alternative:* keep §20 and define MAJOR only for removals and incompatible schema
  changes. Then score comparability across minor versions isn't guaranteed.

**D9.2 Data source for `scripts`** (§2: "sorted ISO 15924 codes from the Unicode
Script property of letters"; Python's standard library has no Script property).
- *Recommended (a):* pin the Unicode Character Database file `Scripts.txt` for the
  same Unicode version as `unicodedata.unidata_version`.
  - Its SHA-256 goes in the manifest.
  - It needs a provenance manifest and a licence check (Unicode's data licence)
    before use.
  - No new Python dependency.
- *(b)* a pinned third-party dependency exposing `\p{Script}` (for example
  `regex`), locked in `uv.lock`. Its Unicode version must match, or both must be
  recorded.
- *(c)* derive the script from character names. That's a heuristic, and not
  recommended.
- **Evidence gap:** neither the licence nor a specific UCD version was checked
  in this run.

**Status:** VERIFIED 2026-10-28 (see "T9 rulings").

### T9 rulings (maintainer, 2026-10-28; not yet in the ADRs)

- **D9.1 accepted as recommended.**
  - MAJOR for any change that makes scores not directly comparable: records,
    splits, `gazetteer_version`, or gold semantics (labels, statuses, procedures
    that change gold).
  - MINOR for additive content that changes no record, split or gold.
  - PATCH only when every gold and split file keeps its SHA-256.
  - **ADR-0006 §20 needs a matching revision in T11.** Today it allows a new
    Layer D status as a minor version.
- **D9.2 option (a), accepted in principle, subject to verification. Verified
  2026-10-28:**

| Item | Evidence |
|---|---|
| Version to match | `unicodedata.unidata_version` = `15.0.0` under the locked Python 3.12.14 (`uv run python -I`, 2026-10-28) |
| Official source URL | `https://www.unicode.org/Public/15.0.0/ucd/Scripts.txt`. Retrieved 2026-10-28T14:20:02Z: HTTP 200, `text/plain; charset=utf-8`, `Last-Modified: Wed, 27 Apr 2022 15:40:26 GMT` |
| Exact version | File header `# Scripts-15.0.0.txt`, `# Date: 2022-04-26, 23:15:02 GMT` |
| Version match, independent check | The code points listed in the file (149,251) equal exactly the code points that Python's `unicodedata` 15.0.0 assigns, excluding categories Cn, Co and Cs (scratch script, asserts passed) |
| Integrity | SHA-256 `cca85d830f46aece2e7c1459ef1249993dca8f2e46d51e869255be140d7ea4b0`, 184,112 bytes, 3,031 lines |
| Licence | Unicode Terms of Use (`https://www.unicode.org/copyright.html`, retrieved 2026-10-28). §2.2: "Data Files" include all computer data files under `https://www.unicode.org/Public/`. §3.3: they are governed by the Unicode License v3 unless otherwise indicated at release. The file names no other licence; its header points to `https://www.unicode.org/terms_of_use.html`, retrieved 2026-10-28, which also names the Unicode License v3 in §3.3. |
| Licence terms | `https://www.unicode.org/license.txt` (retrieved 2026-10-28): "UNICODE LICENSE V3". Free permission to use, copy, modify, merge, publish and distribute, provided the copyright and permission notice appears with all copies. |

**Limits and conditions, kept explicit:**
- No publisher-published checksum was found or checked. Integrity rests on HTTPS
  from the official host plus the independent code-point match. The SHA-256 above
  is ours, taken at retrieval.
- The file was fetched only to a session scratch directory, to hash and check it.
  It wasn't vendored, committed or used by any code.
- Using it later (T12) needs a provenance manifest under `data/manifests/`
  (ADR-0001 §5), with the URL, retrieval date, SHA-256 and licence above.
- Any redistributed copy must carry the Unicode copyright and permission notice.
- **Derived:** a build fails if `unicodedata.unidata_version` differs from the
  `Scripts.txt` version. The release manifest records the `Scripts.txt` SHA-256
  next to `unidata_version`.
- If the Python minor version changes, the bundled Unicode version can change too.
  That would be a new pin and, under D9.1, a MAJOR release if gold changes.

**T9 manifest-field check** against ADR-0001 to ADR-0008 and the approved rulings:
- **ADR-0001 §5:** every data source has a manifest, so `Scripts.txt` needs one
  (above).
- **ADR-0002, ADR-0004, ADR-0005:** `gazetteer_version` and the table hashes are
  already in §18.
- **ADR-0007:** `focus_state_version` (§2), the held-out publisher list (§6) and
  the E3 format owner are listed.
- **ADR-0008:** its procedure version belongs to selection records, not the release
  manifest. ADR-0008 is still Proposed.
- **ADR-0003:** no field (no NAPIX source).
- **Approved rulings:** each is covered by an existing version field or by the T9
  spec list:
  - cue-table scope → `cue_table_version`
  - the gate and anchor invalidation → `candidate_procedure_version`
  - the denylist → `screen_version`
  - errata (D8.3)
  - aliases, missing tokens, column roles and `raw_text_scope` → the
    source-manifest hash
  - decoding → `ingestion_procedure_version`
  - salt and weights → the split configuration
  - counts → the release report
- **Result:** every version input is listed. **T9 VERIFIED.**

### T10: Blocker 11, acceptance condition and ordering — decision requests

**Facts.**
- **ADR-0006's status line:** "Not accepted until the decisions in section 21.1
  are approved ... F1 to F13 were approved in principle on 2026-10-26. The ADR
  stays Proposed until revision 5 is reviewed."
  - The approval date is the rev 5 date, so it isn't recorded whether it covered
    rev 5's rewritten §17.
  - Rev 6 will change the text behind F3, F5, F9 and F10, and add rules (R1f, the
    gate, staging).
- **ADR-0007's status line:** it can't be accepted before ADR-0006. Its 10.1
  decisions S1–S10 need approval.
- **ADR-0006 Consequences order:**
  1. focus-state and source ADRs
  2. `docs/schema.md`
  3. the table procedures
  4. the candidate and resolution procedures
  5. the split key procedure
  6. the guidelines
  7. the validator
  8. the pilot
- **ADR-0007 Consequences order:**
  1. inventory and assessments
  2. source ADR
  3. ingestion-time statistics and selection records
  4. focus-state ADR
  5. ingestion, screening and the first split
  6. sub-district verification
  7. ADR-0006's list from `docs/schema.md` onward
- **Contradictions:**
  - ADR-0007 runs the first split (step 5) before `docs/schema.md` and the split
    key procedure (step 7), but the split file and configuration formats belong to
    `docs/schema.md` (E3).
  - ADR-0007 step 3 needs split-key step 1 implemented (counts per step-1 state)
    and the ADR-0008 procedure (selection records).
  - Neither order has a place for the D5.2 salt, the D8.1 denylist (an empty
    initial state), the D7.1′ staging steps, or decision C's verification for all
    levels before the guidelines freeze.

**D10.1 What counts as acceptance.**
- *Recommended:*
  - ADR-0006 rev 6 and ADR-0007 rev 4 are accepted **together**, by an explicit,
    dated maintainer acceptance recorded in each status line.
  - Acceptance comes only after:
    1. T11 has incorporated every ruling in this graph
    2. the maintainer has reviewed the full diff
    3. every 21.1 item whose text changed (F3, F5, F9, F10 and new items such as
       F14) has been re-approved by name, along with S1–S10
    4. a cross-reference check passes
  - Items deferred by design (P1–P7, L1–L6, O1–O7, E1–E5) don't block acceptance.
  - ADR-0008 is accepted separately, on its own 8.1 decisions. It must be accepted
    before the selection records are computed.
- *Alternatives:*
  - Accept ADR-0006 alone first. ADR-0007 already allows that order, but the
    shared rulings would sit in one accepted ADR and one Proposed ADR.
  - Treat the 2026-10-26 approval in principle as carrying over. That doesn't
    cover the changed F-items.

**D10.2 One implementation order** (derived from dependencies; replaces both
Consequences lists in T11):
1. Accept ADR-0006 rev 6 and ADR-0007 rev 4 (D10.1). Accept ADR-0008 when ready.
2. **LGD level verification** for all four levels (decision C, ADR-0007 §8, E1).
   - It needs no address records, so it can start now and run in parallel.
   - It must be complete or frozen as unverified before step 11.
3. **Source inventory and assessments**: documentation, headers, scripted aggregate
   statistics. This includes column-role evidence (D4.2), missing-token
   documentation (D4.4) and alias distinct-value lists (D4.1).
4. **`docs/schema.md`**: every E3 format, plus the new fields:
   - the independent C set (D3.2)
   - the stage flag (R1c)
   - the reasons `anchor_invalidated`, `district_column_ambiguous` and the T6 ones
   - the errata and denylist entry formats
   - the reason categories
   - release-manifest fields (T9)
5. **Source ADR(s)** accepting sources, with manifests: column roles, aliases,
   tokens, `raw_text_scope`, decoding, `record_id_scope`.
6. **Ingestion procedure** (T6) and **split-key step 1**, then the ingestion-time
   aggregate statistics (O3, O4, O5, P6 inputs) and the ADR-0008 gazetteer
   properties, which give the **selection records**.
7. **Focus-state ADR** (O1, O3, O4, O5). Then the **split configuration**:
   - the salt generated and committed (D5.2)
   - the held-out publishers
   - the P6 weights
8. **Rules screen** (`screen_version`, empty denylist), then **split-key steps
   2–5**. The first split is computed and frozen in staging (D7.1′). The exposure
   log starts.
9. **Role-restricted human screen**. Passing records go to `data/processed/`;
   failures go to the denylist with the class cascade (D8.1, D8.2).
10. **Reference list, normalization table, and cue table procedures.** The cue
    table comes from dev-pool observation (§3), so it needs step 9.
11. **Candidate and resolution procedures**, then the **guidelines** (dev-only
    examples, D7.2), then the **freeze** of the guidelines and cue table.
12. **Validator.**
13. **Pilot** on dev (P1–P5, P7), then gold annotation.

- *Choices inside this order that the maintainer may change:*
  - `docs/schema.md` comes before the source ADRs, because manifests need its
    field format. ADR-0006 put it second, after the source ADRs.
  - Verification runs in parallel instead of after the first split (ADR-0007
    step 6).

**Status:** VERIFIED 2026-10-28 (see "T10 rulings").

### T10 rulings (maintainer, 2026-10-28; not yet in the ADRs)

**D10.1 accepted.**
- ADR-0006 rev 6 and ADR-0007 rev 4 are accepted **together**, by explicit, dated
  maintainer acceptance recorded in both status lines.
- Before acceptance:
  - T11 incorporates every approved ruling
  - the maintainer reviews the complete diff
  - every changed decision item is re-approved **by name**
  - cross-reference checks pass
- Deferred P, L, O and E items don't block acceptance where the ADRs explicitly
  defer them.
- ADR-0008 is a separate acceptance decision. It must be accepted before selection
  records are computed.
- The 2026-10-26 approval in principle is **not** approval of revised decision text.

**D10.2 accepted, in the maintainer's wording** (this order replaces both
Consequences lists in T11):
1. Complete and review the coordinated ADR revisions and acceptance.
2. Start LGD verification in parallel where possible. Finish it, or explicitly
   freeze unresolved levels as unverified, before the guidelines are finalized.
3. Complete the source inventory, eligibility, documentation and licence
   assessments before accepting any source.
4. Define `docs/schema.md` before implementing procedures that depend on its
   formats.
5. Complete source ADRs and provenance manifests before ingesting their data.
6. Implement ingestion, split-key step 1 and the required statistics. Accept
   ADR-0008 before computing selection records.
7. Finalize the focus-state ADR and the split configuration: salt, held-out
   publishers, ratio weights.
8. Run the rules-only privacy screen, then compute and freeze the split in staging.
9. Conduct the role-restricted human screen, applying the approved denylist and
   duplicate-class rules.
10. Build the reference list, normalization table and cue table under the approved
    data and dev-pool restrictions.
11. Implement the candidate and resolution procedures, then finalize and freeze the
    guidelines.
12. Implement and run the validator.
13. Conduct the dev-pool pilot and resolve the pilot decisions. Only then proceed to
    gold annotation.

**Derived:**
- Source-ADR manifests use `docs/schema.md`'s manifest format, so step 4 precedes
  the manifests in step 5.

**Consistency:**
- D10.2 keeps:
  - verification-before-freeze (decision 5)
  - the salt before the first split (D5.2)
  - staging (D7.1′)
  - the denylist and cascade (D8.1, D8.2)
  - dev-only guidance (D7.2)
  - ADR-0007 §5's no-reading-before-the-split
- No conflicts found.

**T10 acceptance check:** acceptance is defined (D10.1), and one consistent order is
decided (D10.2). Writing them into the ADRs is T11. **VERIFIED.**

### T11 edit map: ADR-0006 rev 6 and ADR-0007 rev 4 (prepared 2026-10-28; nothing drafted yet)

Each entry maps an ADR section to the rulings it must incorporate. The draft must
add no rule beyond these. Wording changes listed as "derived" in this graph are
included.

**ADR-0006 rev 6**

| Section | Incorporate |
|---|---|
| Status, Revision | rev 6 note; stays Proposed; acceptance per D10.1 |
| Context l.75–81 | verification of all four levels (C); suffixes `(Ct)`, `(Og)`, `(Part)` without assumed meaning (V) |
| §1 l.94–97 | Layer A records the role as written; verification gates only C and D (4) |
| §2 | `raw_text_scope` (D6.1); duplicate native IDs (D6.2); missing tokens for `raw_text` (D4.4); the `scripts` source, pinned `Scripts.txt` matching `unidata_version` (D9.2) |
| §3 l.170–188 | cue-table entry: written role, claimed level, verified scope (national, or states with exceptions), evidence reference, `pending_level` (R2, R8, R8b, R5, R5b); drop "for the state concerned"; l.187–188 sources for `pending_level` (R8b) |
| §4 | labels as written (4, R6); rows l.207, l.209, l.215; overlap table l.225; the block paragraph l.233–239 (F10 exceptions kept) |
| §7 | precedence steps 0–9: gate after hierarchy and before PIN (R1a–R1c); R1e; reconciliation gate (R1d); edits audit-only on gated roles (R1g); anchors (8.5, 8.6) and invalidation (R1f, 8.9); stage flag `level_mapping_unverified`; reason `anchor_invalidated`; the l.328 invariant; the l.379 `final_set` exception; l.345 rewritten; R3 limitation |
| §8 | role at L requires a non-empty `final_set` (8.7); `basis` precedence and what `conflicting` counts (8.2); `not_in_gazetteer` reasons include `anchor_invalidated` (8.8); `deferred_coverage` via `pending_level` (R2); gated lists never feed D; l.407 verified-designator wording |
| §9 | `pincode_role`: `not_applicable` includes "PIN stage did not run" (R7); `decisive` and `narrowing` (8.3); valid PIN (8.4); drop "a conflict always gives inconsistent" (8.1); `not_checkable` cause order (R4); the mixed-level PIN stage (R4a) |
| §10 | a verification change after the guidelines freeze is handled as a migration with a new `cue_table_version` (5) |
| §12 | staging order (D7.1′); human screen role restrictions (D7.1); denylist replaces "only the count" (D8.1); class cascade (D8.2); exposure log retention (D8.4) |
| §13 | the deletion exception for withdrawal (T8 derived); `visible_inputs` unchanged |
| §14 | agreement table: R9 exclusions, 8.10 Jaccard, D row (D3.1 and its derived scope); dev-only guideline examples (D7.2); verification before the freeze (5); independent C set (D3.2) |
| §15 | adjudication `merge` = union on edits, then the gates and invalidation (D3.3) |
| §16 | no change expected; confirm that the cue-table scope and the gate stay reproducible from system inputs |
| §17 | step 1: column roles, missing tokens, aliases, one state column (D4.1–D4.4); step 2: district rules and the ambiguous case (D4.5 and derived); step 4: Blocker 1 wording (drop "union-find"); step 5: bucket mapping and test vectors (T5); freeze at first exposure and the exposure log (D5.1); salt (D5.2); fixed per-record assignment; staging (D7.1′) |
| §18 | manifest fields (T9); the `errata` field = entries incorporated, plus the append-only log (D8.3); `benchmark_version` rules (D9.1) |
| §19 | suffix handling follows the village verification record (V) |
| §20 | versioning per D9.1 (a new Layer D status is MAJOR) |
| §21 | revised F1, F3, F5, F9, F10, F12; new item(s) for the verification gate and staging/denylist (numbering at drafting); L3 extended to all levels; known limitations (R3 inversion, 8.7 multi-level, T8 rebuild limits) |
| Consequences | the D10.2 order |

**ADR-0007 rev 4**

| Section | Incorporate |
|---|---|
| Status, Revision | rev 4 note; acceptance together with ADR-0006 (D10.1) |
| Context l.58–61 | verification of all four levels (C) |
| §3 l.139 | Blocker 1 wording; step-1 state is never an input to verification (R1) |
| §4 step 3 l.184, table l.202 | verification status for all levels (C) |
| §5 | manifest fields: column roles, aliases, missing tokens, `raw_text_scope`, decoding (D4.1–D4.4, D6.1, T6); evidence for column roles (D4.2); distinct-value lists count as aggregate statistics, not exposure (T5 derived) |
| §6 l.301 | duplicate classes (Blocker 1) |
| §8 | evidence standard for all levels, national or per-state scope, the conflict rules (R5, R5b), the village record (V), evidence for `pending_level` (R8b) |
| §10.1 | revised S6, S9 |
| §10.3 | E1 extended to all levels; the E3 format list extended |
| Consequences | the D10.2 order |

**Re-approval list (D10.1):** the decision items whose text changes. Expected:
ADR-0006 F1, F3, F5, F9, F10, F12 and the new items; ADR-0007 S6, S9. The final
list is taken from the actual diff, not from this plan.

**Preserved gaps** (must not be filled while drafting):
- no source accepted (B1–B20 open as recorded)
- B6 (no files)
- B14–B17 (licences)
- `Address_Original_First_Line` documentation
- the reason-category list (`docs/schema.md`)
- L1 stand-off
- the `Scripts.txt` provenance manifest (T12)
- P1–P7 data-dependent values

### G-ADR67 rulings (maintainer, 2026-11-05; drafted, not in the ADRs on any branch)

Option A for both requests in `docs/workflow/reviews/G-ADR67.md` section 4b. These rulings are not
acceptance of any ADR, and they do not settle the revision numbers or ADR-0008 revision 3.
- **I6.** A denylist entry for a failure caused only by `source_context` drops only the matched
  record, after split-key step 5. The record still counts toward its duplicate class, class key and
  holdout. The reason categories must identify such a failure. This overrides the derived matching
  rule in "T8 rulings" for those entries only.
- **I10.** The D7.1′ derived staging note limits source columns: the `raw_text` field, allowlisted
  `source_context` and a native `source_record_ref`. Values computed for each record may be held with
  them. §12's "Nothing outside the list is ingested" gets a matching exception.

### Maintainer rulings, 2026-11-09 (none of these accepts an ADR)

- **Revision numbers:** ADR-0006 rev 7, ADR-0007 rev 5 and ADR-0008 rev 3 approved.
- **Native `source_record_ref`:** gets the `source_context` screen (ADR-0006 §12).
- **N1:** the whole `group_key` group goes to `test_source_holdout` (ADR-0006 §17 step 5, ADR-0007 §6).
- **Rebuild scope:** a bug-fix recompute counts as a rebuild (ADR-0006 §17).
- **E-FIELD (G-SRC decision 3):** ask the publishers, with a deadline. If there is no reply, the
  platform field list for C2 is used as a recorded limitation (ADR-0006 §2). Deadline: 2026-11-23.
- **Screener and annotation:** a screener must not annotate records they screened (ADR-0006 §12).
- **D10.2:** orders real-data work only. Code built and tested on labelled synthetic fixtures is outside
  it. Graph change approved: `I-INGEST-CODE`, `I-SPLITKEY-CODE`, `I-RULESCREEN-CODE`, `I-VALIDATOR-CODE`.
- **OSM:** stays out of v1 for now. If B14 is not cleared by 2026-11-23, prepare an ADR proposing OSM as
  a fallback source. That ADR stays Proposed.
- **E-LGD:** accepted as unverified. The drafted query is to be sent without waiting for a reply. The
  Rajasthan help text is not verification.
- **B14:** write first. C1a and C2 stay unclear until a reply.
- **W0:** approved by the maintainer. The `graph.py approve` record is still to be run.

### Maintainer rulings, 2026-11-10 (none of these accepts an ADR)

Options as set out from the fourth `adr-reviewer` run (`docs/workflow/reviews/G-ADR67.md`, section 6a).
- **X3 (option a):** a failure caused only by a native `source_record_ref` value is treated as one caused
  only by a `source_context` value, so it stays per record (ADR-0006 §12).
- **X4 (option a):** every denylist exclusion takes effect after split-key step 5. This also settles X6,
  the stage at which the denylist applies (ADR-0006 §12, §17).
- **E2 (option c):** an exposed class that collides with a held-out `group_key` is excluded from that
  build, so no exposed record enters test and no key appears in two splits (ADR-0006 §17).
- **X5 (option a):** the ADR says that the implementation order governs real-data work, and that code
  built and tested on labelled synthetic fixtures is outside it (ADR-0006 Consequences).

Later on 2026-11-10, from the fifth `adr-reviewer` run (packet section 6b):
- **C1 and C2 (option a for both):** one rule replaces the E2 wording. If a recompute would newly place an
  exposed class in `test` or `test_source_holdout`, that class is excluded from the build. A class is
  exposed when any member is in the exposure log (ADR-0006 §17).
- **Lead source columns (option a):** the C2 exception also covers its state and district columns, with the
  same deadline and recorded limitation (ADR-0006 §2, ADR-0007 §5). This widens the 2026-11-09 ruling.
- **S7 and S8 (option a):** added to the G-ADR67 re-approval list.

Last on 2026-11-10, from the sixth `adr-reviewer` run (packet section 6c):
- **N1:** the definition of an exposed class applies to the recompute rule only (ADR-0006 §17).
- **N2:** E-FIELD's first criterion is reworded by the maintainer: each candidate proposed for acceptance
  has its raw-text field backed by publisher documentation, or falls under the ADR-0006 §2 exception.
- **R1:** the exposed-class exclusion applies after step 5 and does not feed back into steps 4 and 5.
- **R2:** "newly" is measured against the immediately preceding `split_version`. A class already in
  `test` or `test_source_holdout` is not newly placed.
- **R3:** the exposure-log state used is recorded with each new `split_version`.

Final on 2026-11-10, from the seventh `adr-reviewer` run (packet section 6d):
- **M1 and M2 (option A):** a class is newly placed when any of its exposed members was in neither test
  split under the immediately preceding `split_version`, and a move between those two splits is not a
  move into test in ADR-0006 or ADR-0007 (ADR-0006 §17). This replaces the R2 baseline wording.

**Version 1 scope (maintainer direction, 2026-11-10):** version 1 is a gazetteer toolkit and PataBench
moves to version 2. Drafted as ADR-0009, Proposed. This is not acceptance of any ADR.
