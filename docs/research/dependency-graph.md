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
| T8 | Blocker 3: withdrawal, denylist, errata | BLOCKED (maintainer: D8.1–D8.4) | T6, Blocker 1, T7 | ADR-0006 §12, §13, §18 | D8.1–D8.4 | a rebuild can't silently re-admit a withdrawn or human-screen-excluded record, or the limitation is documented |
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

**Status:** BLOCKED on D8.1–D8.4. When they are ruled, T9 waits only on T8, which
would then be done.
