# ADR-0007: Focus states and address-corpus sources for PataBench v0

- **Status:** Proposed. Not accepted until the decisions in section 10.1 are
  approved by the maintainer. **Cannot be accepted before ADR-0006**, which is
  itself still Proposed and on which sections 3 to 7 depend.
- **Date:** 2026-10-04
- **Revision:** 3. Revision 2 followed a read-only adversarial review on
  2026-10-04 (split timing, focus-state membership, out-of-focus records,
  overlapping source families, holdout unit, pre-split exposure of records,
  verification evidence).
  Revision 3 (2026-10-26), alongside ADR-0006 revision 5:
  - unmatched state-column values and state disagreements in sections 3, 4
    and 9;
  - O5 as the only owner of held-out publishers;
  - the held-out publisher list located in sections 6 and E3;
  - format ownership in E3: `docs/schema.md` owns every E3 format, the ADRs
    keep policy and required information, and release ADRs record values;
  - O4 limited to records with no state-column value and no
    `coverage_state`.

  Status unchanged.
- **Deciders:** Project maintainer
- **Relates to:** ADR-0001 §1, §2, §5, §6, §7 (sources, privacy, provenance,
  language and geographic scope), ADR-0002 and ADR-0004 (gazetteer sources),
  ADR-0005 (`gazetteer_version`), ADR-0006 (annotation scope and schema; this is
  the "focus-state and source ADR" its Consequences and L3 refer to)

This ADR decides **how** focus states and address-corpus sources are chosen,
recorded and used. It does **not** name any focus state or any address source.
No address source has been assessed, no address record has been ingested, and no
state has been evaluated against the criteria below. Choosing them before that
evidence exists would be an assumption, so the lists themselves are open
decisions (section 10.2). This ADR creates no tooling, collects no data and
changes no manifest.

## Context

- **ADR-0001 §7** says the gazetteer covers all of India, annotation initially
  focuses on "a smaller, deliberately diverse set of states (chosen and documented
  in a later ADR)", and nothing in the data model or code may assume a fixed set
  of states.
- **ADR-0001 §1** allows only public, non-personal sources: official reference
  data and addresses of institutions or facilities published by their operators
  or by government. A new source category needs a new ADR. §5 requires a
  manifest for every source. §6 puts English and romanized Indian-language text in
  scope and does not build native-script modelling in v0 unless the data or the
  research question requires it.
- **ADR-0006** fixes what happens once records exist:
  - admission screen, `source_context` allowlist and `context_columns` (§12)
  - `record_id` scopes declared per manifest (§2)
  - no synthetic records in v0 (F6)
  - the split key computed at ingestion from allowlisted `source_context`, the
    source manifest, `raw_text` and the pinned gazetteer, with
    `test_source_holdout` for "sources designated as held out" (§17, F5). Before
    the freeze, the split may be recomputed **only** to fix a bug.
  - split ratios, unresolved-group share and holdout feasibility (P6), answered
    from ingestion-time statistics
  - LGD sub-district semantics per selected state, enabling `block` and verifying
    cue-table entries deferred "together with the focus-state ADR" (L3). Since
    ADR-0006 revision 5, L3 points to section 8 (evidence standard) and E1
    (per-state outcomes and `block`) of this ADR.
  - how split assignments carry over between releases is open (L5)

  ADR-0006 does not say who designates held-out sources, how a source is
  accepted, or which states are in focus. Its Consequences list "the
  focus-state and source ADRs (with L3)" as the first follow-up.
- **The pinned gazetteer** (`gazetteer_version`
  `bf4a8b5d35130e7c3b94c6e4de812b3fd6deeb059497af22aac178642c2c2c78`) has 36
  state/UT units. Its known limits bear on state choice:
  - no urban local bodies or localities. Urban roles stay unlinked
    (`urban_deferred`, ADR-0006 §19).
  - India Post is deferred. PINs exist only in `village_pincode`.
  - Chandigarh, 6 districts and 30 sub-districts have no villages in the
    village–PIN mapping (`docs/gazetteer.md`).
  - what LGD records as the sub-district level differs by state and has not been
    verified for any state (ADR-0006 context and §4). No LGD file in the pinned
    snapshots has a column naming the sub-district tier (ADR-0004 headers).
- **Repository convention** (`docs/README.md`): ADRs are never rewritten once
  accepted. Later decisions are new ADRs, as ADR-0004 amends ADR-0002.

## Decision

### 1. Scope of this ADR

- This ADR covers the **address corpus**: the records annotated under ADR-0006.
- The **gazetteer** sources stay governed by ADR-0002, ADR-0004 and ADR-0005.
  Nothing here changes them.
- **Gazetteer sources are never address-corpus sources.** That covers any source
  with a gazetteer manifest (entity `admin_unit`, `lgd_village_pincode` or
  `post_office`) and any data derived from one. The gazetteer is reference data
  that systems receive (ADR-0006 §16). Records built from it would make the gold
  depend on the reference it is scored against.

### 2. Focus states: definition

- A **focus state** is a state or union territory in which v0 annotation effort is
  concentrated. It is identified by its `lgd:state:{code}` ID at the pinned
  `gazetteer_version`, never by a name string.
- The focus states for a release form the **focus-state list**, versioned as
  `focus_state_version`. Each entry records the `lgd:state:` ID and a reference to
  its selection record (section 4).
- The list is **benchmark configuration**, not provenance. It is never stored in
  source manifests. Code and procedures read it and never hard-code states
  (ADR-0001 §7).
- The list is decided in a **new ADR** that cites the selection records (section
  4). This ADR is not amended to add it.
- Recording `focus_state_version` in the release manifest (ADR-0006 §18) is a
  follow-up. `docs/schema.md` defines the field, and each release ADR records
  its value (section 10.3, E3).
- The list is fixed before the split is first computed. Any later change is a new
  `split_version` and a new release (section 7).

### 3. Focus-state membership of a record

- A record's **focus-state membership** is its own **step-1 state** from the
  versioned split key procedure (ADR-0006 §17, `split_key_procedure_version`),
  computed for that record before any merge:
  - the allowlisted state column takes precedence, matched by exact `name_key` as
    ADR-0006 §17 step 1 says
  - otherwise the manifest's `coverage_state` (section 5), which is already an
    `lgd:state:` ID and needs no name matching
  - a column value that matches no state never falls back to `coverage_state`
  - two cases give the record no step-1 state and no membership. Both are
    excluded and counted per source, each under its own reason (ADR-0006 §17
    step 1, revision 5):
    - `state_column_unmatched`: the column value matches no state;
    - `state_coverage_disagreement`: the column's state differs from
      `coverage_state`.

    Such a record is resolved only as ADR-0006 §17 step 1 allows.
- A district found from `raw_text` in step 2 **never** assigns a focus state. A
  merged group's key never changes a record's membership.
- Membership never uses gold labels, annotator judgement or model output. It is
  reproducible from the procedure version, the manifest and the pinned gazetteer.
  Recording it as a split-file field is a follow-up for `docs/schema.md` (E3).
- **Out-of-focus records.** Records whose step-1 state is known and is not a focus
  state are **counted** per state and per source, and then **dropped** before
  split-key steps 2 to 5. They never take part in the duplicate merge
  (union-find), get no `record_id` or split, and are never written to
  `data/processed/`. So the choice of focus states cannot change the group key or
  split of any retained record.
- **Unknown state.** Whether records whose step-1 state is unknown are retained is
  open (section 10.2, O4). O4 covers only records with no state-column value
  and no `coverage_state`. A `state_column_unmatched` record is excluded
  whatever O4 decides.
- **Exclusivity is a new decision.** ADR-0001 §7 says annotation "initially
  focuses" on a set of states. It does not require annotation to be limited to
  them. Limiting v0 annotation to focus-state records is decided here (S3), for
  the maintainer to approve, and is not presented as derived from ADR-0001.
- The records that remain form the **annotation pool**. ADR-0006's "dev pool" is
  the part of it assigned to `dev`.
- If gold Layer D later places a record in a different state, that is reported
  alongside the leakage audit (ADR-0006 §17). It never moves the record after the
  split is computed.

### 4. Focus-state selection procedure and criteria

**What selection may never use.** Choosing focus states and accepting sources never
uses annotations, gold labels, pilot results, model or baseline outputs on
candidate data, or individual address records. It may use only the evidence named
in this section and in section 5.

Selection happens before any address record is stored in `data/processed/` or
assigned a split, in this order:

1. **Source inventory.** Candidate address sources are identified and assessed
   under section 5.
2. **Candidate states.** A state is a candidate only if it meets every
   **required condition**:
   - at least one source covering it has been accepted under section 5
   - the state exists as an `lgd:state:` unit in the pinned gazetteer
3. **Selection record.** For each candidate state, a written record lists:
   - the accepted sources covering it, with their source family and publisher
     (section 5)
   - gazetteer properties **computed** from the pinned `gazetteer_version` by a
     versioned procedure, not estimated: districts and sub-districts with no
     villages in the mapping, `same_name_siblings` and `variant_name_siblings`
     counts, and the distribution of villages per PIN
   - ingestion-time aggregate statistics produced by a script from the accepted
     source files: record counts per source and per step-1 state, the count
     whose step-1 state is unknown, and, kept separate, the counts excluded
     as `state_column_unmatched` and as `state_coverage_disagreement` (section
     3). No record is read by a person or stored.
   - the status of sub-district semantics verification for that state (section 8),
     which will usually be "unverified" at this point
   - the diversity dimensions below, as far as source documentation shows them.
     Anything not documented is recorded as unknown, not guessed.

   Selection records are published with the ADR that decides the list, so the
   choice can be audited, including any effect of gazetteer properties on
   benchmark difficulty.
4. **Choice.** The focus-state list is chosen from the candidates to cover the
   diversity dimensions and is recorded in a new ADR (section 2).

**Diversity dimensions** (what "deliberately diverse" in ADR-0001 §7 means for
Pata):

| Dimension | Why it matters for PataBench | Evidence allowed before the split |
|---|---|---|
| Source families available | Avoids gold that reflects one publisher template | Source assessments (section 5) |
| Number of independent publishers | `test_source_holdout` holds out publishers, and needs some left for `train`, `dev` and `test` (section 6) | Source assessments |
| Sub-district verification status | ADR-0006 L3: tiers differ by state, and this drives `subdistrict` and `place_unspecified` outcomes | Verification records (section 8). Usually unverified at selection time. |
| Gazetteer coverage properties | Districts without villages, sibling-name density and PIN fan-out change how much can be linked | Computed from the pinned gazetteer |
| Language and script of published addresses | ADR-0001 §6 scope; code-mixed and romanized strata | Source documentation only. Measurements from the dev pool are reported later and never revise the selection within a release. |
| Region | Address conventions are not assumed to be national | LGD state unit |

How many focus states, and how the dimensions are weighed against each other, are
open (section 10.2, O1 and O3). No dimension has a threshold in this ADR.

### 5. Address sources: families, assessment and manifest

**Source families** are defined by who publishes. ADR-0006 §12 admits only
addresses "published by its operator or a government body". Every address source
belongs to exactly one family:

| `source_family` | Meaning |
|---|---|
| `government_published` | The publisher is a government body, whether or not it operates the institutions or facilities |
| `operator_published` | The publisher is a non-government operator of the institutions or facilities |

Any other publisher, including a third-party aggregator, is a new source category
and needs its own ADR (ADR-0001 §1).

**Source assessment.** Before a manifest is written, each candidate source is
assessed in writing.

*Evidence limit.* Before the split is first computed, an assessment may use only:
- the publisher's documentation, licence text and terms
- the header row of a downloaded file
- aggregate column statistics produced by a script

No person reads individual records or readable address text, and assessment
documents never quote record text. The reason is that the maintainer also writes
the guidelines and the cue table from dev-pool observation (ADR-0006 §3, §6).
Reading records before the split would expose future test records. This limit
applies to source assessment and selection. The record-level admission screen of
ADR-0006 §12 is unchanged.

*What is assessed:*
- **Licence**, verified from the official text on a recorded date, as ADR-0002 and
  ADR-0004 did. An unclear or missing licence means the source is rejected.
- **Terms of use**, including whether automated retrieval is allowed. Where it is
  not, or the terms are silent, retrieval is manual (as in ADR-0004). The answer
  is recorded per source in its source ADR.
- **Redistribution**: whether `raw_text` may be redistributed. This feeds the
  release decision (ADR-0006 L1). It does not block ingestion.
- **Personal-data risk**: whether the documented columns, or the scripted column
  statistics, show names of people, phone numbers, emails, person identifiers or
  residential records. What cannot be told from this evidence is recorded as
  unknown, and the record-level screen decides (ADR-0006 §12).
- **Declared coverage**: the states the publisher says it covers, as `lgd:state:`
  IDs, and whether a state column exists for the allowlist.
- **Identifier**: whether the publisher gives a stable per-record identifier, which
  decides `record_id_scope` (ADR-0006 §2).

A rejected source is recorded with its reason, so it is not reassessed without
cause.

**Acceptance.** Address sources are accepted by a **source ADR**, which may cover
several sources and cites their assessments, as ADR-0002 and ADR-0004 do for the
gazetteer. An address source manifest carries the ADR-0001 §5 fields (including
`publisher`) plus:

| Field | Required | Values | Use |
|---|---|---|---|
| `source_family` | yes | the two values above | Stratification and diversity reporting |
| `record_id_scope` | yes | `native` or `snapshot` | ADR-0006 §2 |
| `context_columns` | yes, may be empty | allowlisted column names | ADR-0006 §12 |
| `coverage_state` | if the whole source covers exactly one state | `lgd:state:{code}` at the pinned `gazetteer_version` | Split-key step 1 and focus-state membership (section 3) |

Manifests describe sources only. Holdout designation and the focus-state list are
benchmark configuration and never go in a manifest (sections 2 and 6). Adding
these fields to the manifest format is a follow-up (E3). The table above fixes
the required information; exact field names, types and serialization are
defined in `docs/schema.md`. This ADR changes no manifest.

### 6. Held-out publishers and grouped splits

ADR-0006 §17 sends every merged group that contains a record from a held-out
source to `test_source_holdout`. This ADR decides how that designation is made:

- **The unit is the publisher.** Every address source manifest with the same
  `publisher` gets the same designation. Holding out one manifest of a publisher
  while keeping another would put the same publisher's template in `train`, which
  defeats the purpose of `test_source_holdout` ("to measure template effects",
  ADR-0006 §17).
- **Where it is stored.** The list of held-out publishers is part of a **versioned
  split configuration**, together with `split_salt`, and is versioned with
  `split_version`. It is not stored in source manifests. Each release manifest
  records it (ADR-0006 §18). Its format is defined in `docs/schema.md` (E3).
  This section sets only the policy.
- **When.** It is fixed before the split is first computed. It is never set or
  changed on the basis of gold labels, annotations, pilot results or model
  results. Any later change is a new `split_version` and a new release (section
  7).
- The selection record of each focus state reports which of its publishers are held
  out and whether any non-held-out publisher remains for that state.
- Holding out every publisher of a state would remove that state from `train`,
  `dev` and `test`. That is reported as a property of the release. It is **not** an
  unseen-state split: v0 has no such split (ADR-0006 §17).
- Because duplicate groups merge across sources (ADR-0006 §17 step 4), a held-out
  publisher can also pull records of other publishers into `test_source_holdout`.
  The number of such records is reported per release.

Which publishers are held out is open (O5, its only owner). Whether
`test_source_holdout` is feasible at all is ADR-0006 P6, and O5 uses that
answer.

### 7. Fixing scope before the split is first computed

- The focus-state list, the set of accepted address sources and the held-out
  publishers for a release are fixed **before its split is first computed**
  (ADR-0006 §17, F5).
- ADR-0006 §17 allows a recompute before the freeze only to fix a bug. Changing
  any of these three is not a bug fix. It means a new ingestion, a new
  `split_version` and a new release, built under ADR-0006 §17.
- How split assignments carry over from one release to the next is not decided
  here. It is ADR-0006 L5.

### 8. Sub-district semantics verification (ADR-0006 L3)

This ADR fixes the evidence standard. The outcome for each state is open (section
10.3, E1).

- Verification establishes what local tier (for example tehsil, circle, block or
  another) LGD records as the sub-district level in one state.
- **LGD-side evidence is required**: LGD documentation, or information LGD itself
  publishes about the type of its sub-district units. Each piece is cited by URL
  and retrieval date.
- An official publication of the state government describing its administrative
  tiers may **corroborate** LGD-side evidence. On its own it cannot verify what
  LGD records.
- Not evidence: counts or name patterns in the gazetteer (such as names containing
  "Circle"), annotator knowledge, or third-party summaries.
- **If no LGD-side evidence exists, the mapping stays unverified.** The designator
  stays unverified in the cue table and may name a `pending_level` (ADR-0006 §3,
  §8).
- A verified mapping is recorded in the cue table as a verified designator with a
  reference to its evidence (ADR-0006 §3). The per-state outcome is recorded in a
  new ADR or in the relevant source ADR, never by amending this ADR.
- Whether to enable a `block` label stays with ADR-0006 L3.

### 9. Reporting

- Every reported result is broken down by **focus state** and by **source family**,
  in addition to the strata in ADR-0006 (`settlement_signal`, `pincode_role`,
  languages, D `basis`).
- Each release reports, per focus state and per source: records admitted,
  excluded by screen rule (as counts only, ADR-0006 §12), in the annotation pool,
  and per split.
- Dropped out-of-focus records are reported as counts per state and per source
  (section 3).
- Records excluded at split-key step 1 are reported per source, separately as
  `state_column_unmatched` and `state_coverage_disagreement` (section 3), with
  a reference to each recorded resolution (ADR-0006 §17 step 1).
  - These counts equal the ingestion-time counts of the ingestion the release
    was built from (section 4, step 3).
  - A change in these counts between releases is traced to a recorded
    resolution or to another section 7 change of the source set.
- The ADR-0001 distribution-shift limitation (institutional addresses only) is
  repeated for every focus state, because no source family in section 5 covers
  user-typed residential addresses.

### 10. Decisions

#### 10.1 To approve with this ADR (freeze now)

| # | Decision | Section |
|---|---|---|
| S1 | ADR-0007 governs address-corpus sources and focus states only. Sources with a gazetteer manifest, and data derived from them, are never address-corpus sources. | 1 |
| S2 | Focus states are identified by `lgd:state:` ID. The focus-state list is versioned benchmark configuration, decided in a new ADR, never stored in manifests and never hard-coded. | 2 |
| S3 | Membership is each record's own step-1 state from the versioned split key procedure. Known out-of-focus records are counted and dropped before split-key steps 2 to 5. Limiting v0 annotation to focus-state records is a new decision, not derived from ADR-0001. | 3 |
| S4 | Selection follows the four-step procedure, with the two required conditions, the computed selection record and the diversity dimensions, and never uses annotations, gold, pilot results, model outputs or individual records. No thresholds are set here. | 4 |
| S5 | Two publisher-based source families, `government_published` and `operator_published`. Anything else needs a new ADR. | 5 |
| S6 | Written source assessment limited to documentation, headers and scripted aggregate statistics before the split; acceptance by a source ADR; the added manifest fields. | 5 |
| S7 | Holdout is designated per publisher, in the versioned split configuration, before the split is first computed, and never from results. | 6 |
| S8 | The focus-state list, the accepted source set and the held-out publishers are fixed before the split is first computed. Any later change is a new `split_version` and a new release. | 7 |
| S9 | Sub-district verification needs LGD-side evidence. State-government evidence only corroborates. Without LGD-side evidence the mapping stays unverified. | 8 |
| S10 | Results are reported by focus state and source family, with per-state and per-source counts. | 9 |

#### 10.2 Open

O3, O4 and O5 are decided from ingestion-time aggregate statistics (section 4,
step 3) before the split is first computed, and never from pilot annotations.

| # | Question | Depends on |
|---|---|---|
| O1 | Which states are focus states | Source inventory and selection records (section 4) |
| O2 | Which address sources are accepted | Source assessments (section 5) |
| O3 | How many focus states; minimum number of publishers per focus state; any cap on one source's, publisher's or family's share of a split | Source inventory and ingestion-time aggregate statistics |
| O4 | Whether records whose step-1 state is unknown are retained in the annotation pool. Only records with no state-column value and no `coverage_state`; `state_column_unmatched` records are always excluded (section 3). | Ingestion-time aggregate statistics (unknown-state counts) |
| O5 | Which publishers are held out. O5 is the only owner of this question. (Revision 2 also asked here whether `test_source_holdout` is feasible; that is ADR-0006 P6.) | Ingestion-time aggregate statistics; the feasibility answer from ADR-0006 P6 |
| O6 | Whether sources publishing native-script addresses are admitted in v0 | ADR-0001 §6; source inventory |
| O7 | Whether gazetteer coverage gaps (urban-heavy states, districts without villages) count for or against a candidate state | Selection records |

Revision 1's O8 (automated retrieval per source) is a fact about each source, not a
benchmark decision. It is recorded in the source ADR (section 5; E5).

#### 10.3 Deferred to another ADR or document

| # | Question | Where |
|---|---|---|
| E1 | Per-state outcome of sub-district semantics verification; enabling `block` | A new ADR or the relevant source ADR, together with ADR-0006 L3 |
| E2 | Redistribution of address text, and licence of the annotations | Release ADR (ADR-0006 L1) |
| E3 | Formats: address-source manifest fields (section 5), split configuration (section 6) including the held-out publisher list with `split_salt`, focus-state list file, `focus_state_version` and the held-out publisher list in the release manifest, focus-state field in the split file | `docs/schema.md` is the normative owner of every format in this row: exact field names, structures, types and serialization. This ADR and ADR-0006 keep the policy, procedures, invariants and required information (here sections 2, 5, 6, 7 and 9), and reference the schema. Each release ADR records that release's values, such as its held-out publisher list, and references the schema; it never redefines a format. (Revision 2 said "`docs/schema.md` and the release ADR".) |
| E4 | How split assignments carry over between releases when sources or states change | ADR-0006 L5 |
| E5 | Whether each source permits automated retrieval | That source's source ADR |

## Consequences

- Accepting this ADR selects no state and no source. ADR-0006 must be accepted
  first. The next steps are, in order:
  1. the source inventory and assessments (documentation, headers and scripted
     aggregate statistics only)
  2. a source ADR accepting the address sources (O2), with their manifests
  3. ingestion-time aggregate statistics and the selection records, computed by
     script from the accepted sources and the pinned gazetteer
  4. a new ADR recording the focus-state list (O1) and deciding O3, O4 and O5
  5. ingestion, screening and the first split computation under ADR-0006 §17
  6. sub-district verification for each focus state (E1)
  7. the steps listed in ADR-0006's Consequences, from `docs/schema.md` onward
- Requiring a written assessment and a source ADR makes adding sources slower.
  In exchange, every source in the benchmark has a recorded licence, terms and
  personal-data assessment.
- Requiring a verified licence may leave the `operator_published` family empty in
  practice, if operators publish addresses without one. That is reported, not
  worked around.
- Holding out by publisher cannot detect two publishers that share one template.
  That remains a known limit of `test_source_holdout`.
- The v0 benchmark will under-represent urban addresses wherever focus states are
  urban-heavy, because the gazetteer has no urban units (ADR-0002, ADR-0004). This
  is reported per focus state, not hidden.
- Fixing scope before the split is first computed keeps one release's splits
  reproducible. Extending coverage always means a new release, and whether such
  releases are split-compatible depends on ADR-0006 L5.
