# ADR-0006: PataBench v0 annotation scope and schema

- **Status:** Proposed. Not accepted until the decisions in section 21.1 are
  approved by the maintainer.
  - It is accepted **together with ADR-0007 revision 4**, by an explicit, dated
    maintainer acceptance recorded in both status lines.
  - Acceptance comes after the maintainer has reviewed the complete revision diff,
    has re-approved by name every decision item whose text changed, and the
    cross-reference checks pass.
  - F1 to F13 were approved in principle on 2026-10-26, for the text of revision
    5. That approval is **not** approval of revised text.
  - Items explicitly deferred in sections 21.2 and 21.3 do not block acceptance.
- **Date:** 2026-10-04
- **Revision:** 6 (2026-10-28), alongside ADR-0007 revision 4, from the
  maintainer's acceptance-readiness rulings of 2026-10-27 and 2026-10-28:
  - Layer A records roles as written. Designator verification covers all four LGD
    levels, gates only Layer C and Layer D, and is checked by a deterministic gate
    that human additions can't bypass (§1, §3, §4, §7).
  - §7 adds anchor invalidation (`anchor_invalidated`) and a fixed precedence.
  - §8 and §9 settle `basis` precedence, PIN validity, `pincode_role` and the
    `not_checkable` causes.
  - Duplicate classes replace merged groups (§17 step 4).
  - §17 specifies split-key column roles, aliases, missing-value tokens, district
    rules, the bucket mapping, the salt and the freeze point.
  - Ingestion is staged: a rules-only screen, then the split frozen in staging,
    then a role-restricted human screen, before `data/processed/` (§12).
  - A private denylist, duplicate-class cascade and an append-only errata log
    (§12, §13, §18).
  - Layer D reliability and adjudication `merge` are defined (§14, §15).
  - The release manifest gains fields, plus `benchmark_version` rules (§18).
  - The Consequences list is the single implementation order shared with
    ADR-0007.
- **Revision 5 and earlier:** Revision 2 followed a read-only design review on 2026-10-04
  that found circular split assignment, PIN circularity, an insufficient Layer D
  vocabulary and gaps in candidate reproducibility. Revision 3 (2026-10-04)
  narrows Layer D `deferred_coverage` to `pending_level`, fixes the
  pre-annotation boundary and removes remaining contradictions. Revision 4
  (2026-10-04), from the ADR-0007 review: P6 is answered from ingestion-time
  statistics, and cross-release split stability is recorded as open (L5).
  Revision 5 (2026-10-26), from a review against ADR-0007:
  - §17 step 1 takes the state from the column first and otherwise from the
    manifest's `coverage_state`. An unmatched column value, or a disagreement
    between the two, excludes the record under its own reason. Exclusions are
    resolved only by a documented, evidence-based correction or disposition.
  - §17 step 5 and §18 point to the held-out publisher list in the versioned
    split configuration (ADR-0007 §6, E3).
  - §17 and §18 say what the split file and release manifest must record.
    `docs/schema.md` defines their exact field names, structures, types and
    serialization, and each release ADR records the values.
  - `raw_text` stays strict, and text not published as one string is deferred
    (L6, new).
  - L3 now points to ADR-0007 §8 and E1.
  - P6 no longer asks which publishers are held out (ADR-0007 O5).
- **Deciders:** Project maintainer
- **Relates to:** ADR-0001 (data, privacy, licensing, scope), ADR-0002 and ADR-0004
  (gazetteer sources and IDs), ADR-0005 (`gazetteer_version`), ADR-0007 (focus
  states and address sources)

This ADR decides **what** is annotated, **how** labels are represented, **what
annotators and systems may see**, and **how splits and releases are built**. It
creates no tooling, collects no data and writes no `docs/schema.md`. No
annotation, corpus or result exists. Every number that depends on data (pilot
size, agreement thresholds, split ratios) is left open on purpose (section 21).

## Context

PataBench needs gold data for four research questions:
- where the components of an address are
- how they are written canonically
- which real-world unit each one refers to
- where the address as a whole points

Merging these into one label would hide which step a system got wrong.

Constraints already in force:

- **ADR-0001.**
  - Only public, non-personal sources and clearly flagged synthetic data. No
    scraped personal or user addresses.
  - Personal data is removed at ingestion. Residential-looking records are
    excluded, not anonymized.
  - Labels are on character offsets. Every record has a script and a language
    field.
  - Synthetic data is never a headline result.
  - Focus states are chosen in a later ADR, and nothing may assume a fixed set of
    states.
  - No UI, API server or deployment infrastructure.
- **Gazetteer (ADR-0002, ADR-0004, ADR-0005, `docs/gazetteer.md`).**
  - Linkable units are LGD units `lgd:{level}:{lgd_code}`, at the levels `state`,
    `district`, `subdistrict` and `village`.
  - Each build is identified by `gazetteer_version`. The current one is
    `bf4a8b5d35130e7c3b94c6e4de812b3fd6deeb059497af22aac178642c2c2c78`.
  - There are no urban local bodies or localities. India Post is deferred. There
    is no PIN entity table: PINs exist only as values in `village_pincode`.
    `name_local` is empty. LGD history is not modelled.
- **The gazetteer is ambiguous by nature.**
  - 11,258 `same_name_siblings` records: identical village names under one
    sub-district.
  - One PIN covers a median of 19 villages, and 1,889 PINs span more than one
    district.
  - Suffixes such as `(Ct)`, `(Og)` and `(Part)` appear in village names. What
    LGD means by them, and whether they are ordinary villages, is not assumed
    (ADR-0007 §8).
- **The meaning of LGD's sub-district level varies by state.**
  - In the pinned snapshot, 115 sub-district names contain "Circle".
  - West Bengal has 346 sub-districts, Bihar 537 and Jharkhand 264.
  - These counts alone do not establish which local tier (tehsil, circle, block,
    or another) LGD records as the sub-district in a given state. That has to be
    verified, not assumed.
- **No level mapping is verified yet.** A designator's mapping to the state,
  district, sub-district or village level needs LGD-side evidence, national or per
  state (ADR-0007 §8). None has been recorded.

## Decision

### 1. Four layers, three of them human-judged

| Layer | Question | How the gold is produced |
|---|---|---|
| **A. Extraction** | Which character spans are address components, in which roles? | Human annotation of `raw_text` |
| **B. Normalization** | What is each span's canonical written form? | **Generated** by a versioned procedure. Humans decide only the ambiguous cases the procedure flags (section 6). |
| **C. Entity linking** | Which gazetteer unit does each span role denote? | Deterministic candidate generation, plus a human decision that is recorded in structured form (section 7) |
| **D. Address resolution** | Which unit does the record point to, at each LGD level? | **Derived** by a versioned procedure from gold A and C and the pinned gazetteer (section 8). Not annotated. |

- Each layer has its own fields and provenance. No label encodes two layers.
- **Layer A records each role as written.** Whether a designator's mapping to an
  LGD level is verified never changes a Layer A label. It decides only Layer C
  linking and Layer D gold (sections 3, 7 and 8).
- **Staged gold.** A is adjudicated first. B and C work on the gold spans, and D
  is derived from gold A and C. So a boundary disagreement cannot appear as a
  linking disagreement.
- Each layer can be evaluated on its own:
  - A on `raw_text`
  - B and C with gold spans (oracle) or end to end
  - D end to end
- D is derived rather than annotated, so its gold can be reproduced exactly from
  gold A and C. Its reliability is measured by deriving D from each annotator's
  independent A and C and comparing the results (section 14).

### 2. The record

A **record** is one address string for one place or institution, exactly as one
admissible source published it (section 12). Records are created by ingestion
under a source manifest, never typed in by annotators.

**`record_id` rules.** Every source manifest must declare one of two scopes:

- **`native`**: the source publishes a stable identifier for the place or
  institution.
  - `record_id` is `rec:` + the first 32 hex characters of SHA-256 over
    `native\n{source_id}\n{native_id}`.
  - It persists across snapshots for as long as the publisher keeps the
    identifier.
  - The text may change between snapshots. Annotations are bound to
    `raw_text_sha256`, so annotations made on old text are detected as stale and
    are never reused silently.
- **`snapshot`**: no stable identifier exists, only a row reference.
  - `record_id` is `rec:` + the first 32 hex characters of SHA-256 over
    `snapshot\n{source_id}\n{source_snapshot_sha256}\n{row_ref}`.
  - It is valid **only within that snapshot**. A refresh creates new IDs.
  - Carrying annotations to a new snapshot would need a separately versioned
    matching procedure. None is defined in v0, and snapshot-scoped IDs are never
    described as persistent.
- **Duplicate native IDs.** If two or more rows of one snapshot share a
  `native_id`, every one of them is excluded as `duplicate_native_id` and
  counted. None gets a `record_id`.

| Field | Required | Allowed values / format | Purpose and scientific use |
|---|---|---|---|
| `record_id` | yes | as above | Identity. Its stability is explicit, not assumed. |
| `record_id_scope` | yes | `native` or `snapshot` | Says how far the identity can be trusted across refreshes. |
| `source_id` | yes | an `id` from `data/manifests/` | Provenance and licence (ADR-0001 §5). Used for source holdout (section 17). |
| `source_snapshot_sha256` | yes | 64 hex | The pinned snapshot the text came from, so the corpus can be rebuilt. |
| `source_record_ref` | yes | the native identifier, or the row reference inside the snapshot | Lets anyone find the record in the source again. |
| `source_type` | yes | `real` (the only allowed value in v0; section 21.1, F6) | ADR-0001 §3 source classification. Kept so that any synthetic data added later stays separable. |
| `raw_text` | yes | Unicode string exactly as published. No trimming, Unicode normalization, case change or redaction. | The only text input to annotators and systems. All offsets refer to it. |
| `raw_text_sha256` | yes | SHA-256 of the UTF-8 bytes of `raw_text` | Integrity check. Binds annotations to one text. Supports stand-off distribution (section 21.3, L1). |
| `scripts` | yes, derived | sorted ISO 15924 codes from the Unicode Script property of letters, read from the Unicode Character Database `Scripts.txt` of the same Unicode version as the build's `unicodedata.unidata_version`. A build fails if the two versions differ. | ADR-0001 §6 script field. Computed, so it is reproducible. The file's SHA-256 is recorded in the release manifest (section 18). |
| `source_context` | optional | object whose keys come only from the manifest's `context_columns` allowlist (section 12) | Used only to compute split keys and for audits. Never gold. Never shown to annotators or systems. |
| `admission.screen_version` | yes | version of the written privacy screen | Screening can be reproduced. |
| `admission.screened_by` | yes | the `rule:{name}` screen applied before the split and the pseudonymous ID of the human screener after it (section 12) | Accountability for each stage of the privacy decision. |

**`raw_text` is strict in v0.** It is one string the source publishes as an
address. A concatenation of separately published components, and text
extracted from a PDF or another document, are **not** `raw_text` in v0. A
future documented decision may permit them (section 21.3, L6). Until then, a
source that does not publish its addresses as such strings supplies no
records.

**Which field is `raw_text`.**
- A field is eligible only if the publisher's documentation presents it as the
  facility's address or as an address line. This is never judged from the values.
- The manifest records the field and its `raw_text_scope` (ADR-0007 §5):
  - `full_address`
  - `address_line`: a documented single line of the address
- `address_line` records are reported as their own stratum. Their Layer D levels
  will often be `not_specified`.

**Decoding**, fixed per source in its source ADR under a versioned
`ingestion_procedure_version`:
- **Encoding** is declared from the publisher's documentation or the file's own
  declaration, never guessed.
  - Decoding is strict, with no replacement characters.
  - A row that fails to decode is excluded as `undecodable`.
- **BOM.** One leading U+FEFF at the start of a *file* is file encoding and is
  removed before parsing. A U+FEFF inside a field is kept as published.
- **CSV:** RFC 4180, with the delimiter and quote character declared.
  - A quoted embedded newline is part of the value and stays in `raw_text`.
  - A row with the wrong number of fields is excluded as `malformed_row`.
- **XLSX:** the `raw_text` cell must be a text cell. A numeric, date or formula
  cell is excluded as `non_text_cell`, because formatting it would invent text.
  - In a context column, an integer-valued numeric cell becomes its decimal
    string. Any other numeric value counts as no value.
- **Missing values.** Missing-value tokens that the publisher documents for the
  `raw_text` field (ADR-0007 §5) are recognized first.
  - A matching value is excluded as `missing_value_token`.
  - Then `raw_text` that is empty or entirely whitespace (`str.isspace()`) is
    excluded as `empty_raw_text`.
  - Nothing is trimmed.
- **Counts.** Each reason is counted per source at ingestion, alongside the
  section 17 reasons. Counts for different reasons are never added together.

Removed from revision 1: `synthetic_generator` (synthetic data is excluded from v0)
and `admission.result` (it was always `admitted`).

### 3. Visibility and the outside-knowledge rule

**Annotators must not use personal or world knowledge in any layer.** That
includes knowing the place, maps, web search and memory of district names. They
may use only:

| Pass | Annotators see | Never shown |
|---|---|---|
| A (independent) | `raw_text`, the guidelines, the **reference name list**, the **cue table** | `source_context`, `source_id`, split membership, other annotators' work, system output, model labels and any other generated suggestion (section 13) |
| B (ambiguity decisions) | `raw_text`, gold spans, the cases the procedure flagged with their listed expansions (none preselected, in an order that does not depend on the record), the normalization table | same as A |
| C (independent) | `raw_text`, gold spans, the cue table, **lookups they start themselves** in the pinned gazetteer (section 13) | same as A, including generated candidate lists |
| C (reconciliation, after the independent C labels are frozen) | everything in C (independent), plus the complete generated candidate lists | `source_context`, `source_id`, split membership, other annotators' work, system output, model labels |
| Adjudication (after reconciliation) | `raw_text`, gold spans (for B and C), the independent and reconciliation annotations shown without annotator identities, the complete generated candidate lists | `source_context`, `source_id`, split membership, system output, model labels |

- **Reference name list.** All `state` and `district` names in `admin_unit.csv` of
  the pinned `gazetteer_version`, produced by a versioned procedure
  (`reference_list_version`).
  - This replaces revision 1's "general knowledge of state and district names".
  - Village and sub-district names are not in the list. Recognizing them requires
    a designator from the cue table, or the span is labelled `place_unspecified`.
- **Cue table.** A versioned table (`cue_table_version`) of designators and
  relational cue words. Each designator entry carries:
  - the **written role**: the section 4 label the designator gives a span, as
    written. The guidelines and cue table own this mapping from written words to
    labels, based on observed address usage.
  - the **claimed level**: the LGD level that role names, if any
  - the **verified scope** of the claimed level's mapping:
    - national, or a list of `lgd:state:` IDs
    - with any states excepted from a national mapping
    - or none
  - a reference to the evidence (ADR-0007 §8)
  - `pending_level`, if any (below)

  **Verification gates only linking.**
  - A designator unverified for a state never yields a gold link at its claimed
    level for units in that state (the gate, section 7).
  - It never falls back to the no-designator route.
  - It never changes the Layer A label.

  **`pending_level`** is the single LGD level whose mapping to the designator is
  pending verification.
  - **Written role is an LGD level label:** `pending_level` is that level.
  - **Written role is `place_unspecified`** (the F10 designators "Block" and
    "Sub-division"): it is named only on a cited source of a kind ADR-0007 §8
    allows, state-government material included, with URL and retrieval date.
    - Such a source supports "pending" only, never "verified".
    - Without one, no `pending_level` is named.
  - `pending_level` must not drive annotation, candidate generation, ranking or
    linking. It is used only by the derived Layer D status `deferred_coverage`
    (section 8).

  This ADR does not define the table's contents. They come from dev-pool
  observation, LGD documentation and, for `pending_level` only, the cited sources
  above.

Everything an annotator may use is also available to systems (section 16). So the
gold never relies on information systems cannot have.

### 4. Span labels (v0)

Labels name the **role a span plays as written**, decided by the rules in
section 3. Whether the designator's LGD mapping is verified never changes the
label. It only gates Layer C and Layer D (sections 3, 7 and 8).

| Label | Covers | Default Layer C status |
|---|---|---|
| `organization` | The institution or facility that occupies the address | `not_applicable` |
| `premise_name` | The name of a building, complex or campus as a physical structure | `not_applicable` |
| `premise_number` | House, door, plot, shop, survey or building number | `not_applicable` |
| `unit` | A part inside a building: floor, flat, room, wing, or a lettered or numbered building "block" | `not_applicable` |
| `street` | Road, street, lane, cross, main, marg | `not_in_gazetteer` / `entity_type_not_modelled` |
| `landmark` | Another place used as a reference ("near X"), without the cue word | `not_in_gazetteer` / `entity_type_not_modelled` |
| `locality` | Colony, nagar, sector, ward, mohalla, area, layout | `not_in_gazetteer` / `entity_type_not_modelled` |
| `village` | A place marked as a village by a designator whose written role in the cue table is `village` | linkable (`lgd:village:`) where the mapping is verified; otherwise `not_in_gazetteer` / `level_mapping_unverified` (section 7) |
| `post_office` | A place marked as a post office ("P.O.", "Post") | `not_in_gazetteer` / `source_deferred` |
| `subdistrict` | A place marked by a designator whose written role in the cue table is `subdistrict` | linkable (`lgd:subdistrict:`) where the mapping is verified; otherwise `not_in_gazetteer` / `level_mapping_unverified` (section 7) |
| `city` | A place marked as a city, town or urban local body | `not_in_gazetteer` / `urban_deferred` |
| `district` | A place marked as a district, or a bare name matching the reference name list (rules: section 21.2, P5) | linkable (`lgd:district:`). A designated role is gated (section 7). |
| `state` | A state or union territory: designator or reference-list match | linkable (`lgd:state:`). A designated role is gated (section 7). |
| `pincode` | A Postal Index Number as written | `not_in_gazetteer` / `entity_type_not_modelled` |
| `country` | A country name | `not_applicable` |
| `place_unspecified` | A named place whose level the text does not reveal under these rules, including places whose designator's written role is `place_unspecified` ("Block X", "Sub-division X"; F10) | Without a designator: linkable at all four levels. With an F10 designator: `not_in_gazetteer` / `level_mapping_unverified`. |

**Overlapping labels and how they are told apart.** Whether any of these should be
merged is a pilot question (section 21.2, P3).

| Pair | Distinguishing test |
|---|---|
| `organization` / `premise_name` | `organization` names who occupies the address. `premise_name` names the structure. Test: would the name change if the occupant moved out? If yes, it is `organization`. Government buildings named after their function ("Collectorate") are the hard case the pilot must measure. |
| `organization` / `landmark` | `organization` is the occupant of **this** address. `landmark` is another place, introduced by a relational cue. |
| `unit` / `premise_number` | `unit` is inside a building. `premise_number` identifies the building or plot. |
| `locality` / `village` / `city` / `place_unspecified` | Decided only by designators and cue words, by their written role in the cue table, never by LGD verification status. Without one, the label is `place_unspecified`. The pilot measures whether `place_unspecified` takes over most of the label distribution. |
| `street` / `locality` | Decided by the designator: "Road" and "Lane" mean `street`; "Nagar" and "Colony" mean `locality`. |

**Candidates for removal**, kept in v0 pending pilot evidence:
- `premise_name`: merge into `organization` if they can't be told apart reliably
- `country`: trivial while scope is India
- `unit`: drop if rare in admissible sources

**`block` is not a v0 label.** Revision 1 had it. It is withdrawn because whether
LGD's sub-district level corresponds to development blocks, revenue circles,
tehsils or something else must be checked for each selected state before the label
can be defined (section 21.3, L3). Revision 1 also listed "sub-division" under
`subdistrict`. That was wrong: a sub-division may be a separate tier, so it too
counts as an unverified designator. Text that names a block or sub-division is
labelled `place_unspecified` and left unlinked (`level_mapping_unverified`).
These F10 exceptions stay unless a separately justified decision changes them.

### 5. Spans, offsets and spans with two roles (Layer A)

**Offsets:**
- 0-based and half-open (`[start, end)`), counted in Unicode **code points** of
  `raw_text` (Python `str` indexing).
- Not bytes, not UTF-16 code units, not grapheme clusters.
- `raw_text[start:end]` must equal the span's `text`.

**Boundary rules**, all checkable with the standard library:
- A span starts and ends on a non-whitespace character.
- No boundary falls before a combining mark (`Mn`, `Mc`, `Me`), on either side of
  U+200C or U+200D, or directly after a virama (canonical combining class 9).
- Spans are contiguous, flat and non-overlapping.
- Relational cue words from the cue table are **outside** spans and unlabelled.
- Whether a designator attached to a name is inside the span ("Gonda Dist.") is
  deferred to the pilot (section 21.2, P2). The draft guidelines put it inside.

**Spans with two roles.** Sometimes one stretch of text explicitly carries two
roles, signalled by two designators: "Vill & PO Rampur" or "Distt. & Tehsil Gonda".
Such a span is annotated **once**:
- `label` is its primary role: the first applicable entry in this order: `village`,
  `subdistrict`, `district`, `state`, `city`, `post_office`, `locality`, `street`,
  `landmark`, `premise_name`, `organization`, `premise_number`, `unit`, `pincode`,
  `country`.
- `also_labels` lists the other roles.
- Two roles are recorded only when the text states both. They are never inferred.
- Layer C links each role separately (section 7).

This keeps spans flat. Nested spans are not needed for this case. Whether the
precedence order works in practice is checked in the pilot (section 21.2, P3).

| Field | Required | Allowed values / format | Purpose and scientific use |
|---|---|---|---|
| `span_id` | yes | `"{start}:{end}"` | Deterministic and independent of tooling. Spans are flat, so offsets identify them. |
| `start`, `end` | yes | integers, `0 ≤ start < end ≤ len(raw_text)` | Character-offset labels (ADR-0001 §6). |
| `text` | yes | equals `raw_text[start:end]` | Catches offset and encoding errors. |
| `label` | yes | one label from section 4 | The primary extraction target. Single-label metrics use it. |
| `also_labels` | optional | non-empty list of other labels from section 4, excluding `place_unspecified` | Lets a span carry two stated roles without nested spans. Scored as its own extraction sub-task. |

Record-level fields set in pass A:

| Field | Required | Allowed values / format | Purpose and scientific use |
|---|---|---|---|
| `scope` | yes | `in_scope`, `not_an_address`, `multiple_addresses`, `outside_india`, `unreadable` | Out-of-scope records are counted and excluded from metrics, never silently dropped. Layers B to D apply only to `in_scope`. |
| `languages` | yes | BCP 47 tags with a script subtag for romanized text (`hi-Latn`). `und` is allowed. | ADR-0001 §6 language field. Used to stratify results. |
| `code_mixed` | derived | `true` if `languages` has more than one language other than `und` | Code-mixed stratum. |

### 6. Normalization (Layer B): generated, with human decisions only where it is ambiguous

Layer B is produced by a **versioned normalization procedure** using a **versioned
normalization table** (`normalization_table_version`). The table lists generic
address abbreviations and their expansions. This ADR defines **none** of its
entries: they come from dev-pool observation, never from guesses.

What the procedure does:
- It is deterministic: separators inside digit sequences are removed, digits are
  converted to ASCII, and table entries with **one** expansion are expanded.
- When a match is ambiguous, it **flags** it instead of choosing. A match is
  ambiguous when its table entry lists several expansions, or when the entry is
  marked as also usable inside proper names.
- It never corrects the spelling of proper names, transliterates or translates.

**The only human decision in Layer B:** for each flagged match, choose one of the
listed expansions or `not_an_abbreviation`.

| Field | Required | Allowed values / format | Purpose and scientific use |
|---|---|---|---|
| `span_id` | yes | an existing gold `span_id` | Joins B to A. |
| `normalized` | generated | string, or `null` when `status` is `not_normalizable` | The normalization gold. |
| `status` | generated | `normalized`, `unchanged`, `not_normalizable` | Separates "nothing to change" from "cannot be made canonical" (e.g. a `pincode` span that is not six digits after normalization). |
| `ops` | generated | subset of `separator_removed`, `digits_ascii`, `abbreviation_expanded` | Error analysis by kind of operation. |
| `decisions` | if any match was flagged | list of `{start, end, choice}`. `choice` is one of the listed expansions or `not_an_abbreviation`. | The only part of B that is judged by a person. Agreement is measured on it (section 14). |

Whether Layer B is a **v0 evaluation task** or only a convenience field depends on
how often ambiguous matches occur. That is deferred to the pilot (section 21.2, P4).

### 7. Entity linking (Layer C)

There is one entry per (`span_id`, role) for every role of every gold span: the
`label` and each of the `also_labels`.

**Statuses:**

| `status` | Meaning | Invariants |
|---|---|---|
| `linked` | The final candidate set has exactly one unit, and the text supports it | `entity_id` equals the only member of `final_set` |
| `ambiguous` | The final candidate set has two or more units, and the text can't decide between them | `final_set` has at least 2 members. No `entity_id`. |
| `not_in_gazetteer` | The role denotes a geographic unit that the pinned gazetteer can't represent, no candidate is supported, the verification gate rejected it, or its anchor was invalidated | `reason` is given. `final_set` is empty, or absent for roles that are not linkable. No `entity_id`. Generated candidate lists may be present for audit; they never feed Layer D. |
| `not_applicable` | The role never denotes a geographic unit (section 4) | Has no candidates, `entity_id` or `reason` |

`reason` takes one of these values:
- `entity_type_not_modelled`
- `urban_deferred`
- `source_deferred`
- `level_mapping_unverified`
- `no_match_in_snapshot`: name generation found nothing
- `no_supported_match`: candidates existed, but each was pruned as not supported by
  the text
- `anchor_invalidated`: the role's candidates were narrowed by a higher-level
  anchor whose final outcome no longer supports it (step 9)

**Deterministic candidate generation**, versioned as
`candidate_procedure_version` and uses only `raw_text`, gold spans, the cue table
and the pinned gazetteer.
- It never uses split metadata, the step-1 state or a PIN to decide verification
  scope.
- It runs for linkable roles in level order: state, district, sub-district,
  village, then `place_unspecified`.

**Precedence for one linkable role** (the steps are checked in order; a terminal
step fixes the status):

0. **Not linkable.** A label that is not linkable gets its section 4 default.
1. **Designator unverified everywhere** (no verified scope at all, including the
   F10 designators).
   - The role never enters generation. Lists are `null` and no stage flag is set.
   - Status `not_in_gazetteer` / `level_mapping_unverified`. *Terminal.*
2. **Name stage.**
   - Strip the cue-table designators from the span text.
   - Collect every unit whose `name_key` equals the `name_key` of the remainder, at
     the role's claimed level. A `place_unspecified` role without a designator
     uses all four levels.
   - Output: `candidates.name`.
   - If it is empty, the status is `not_in_gazetteer` / `no_match_in_snapshot`.
     The gate is not checked. A reconciliation addition can still widen the
     set (step 6), and step 7 checks it.
3. **Hierarchy stage.**
   - The **anchors** are the higher-level roles in the record that have exactly
     one candidate after their own stages, including the gate (step 4).
   - With several anchors, keep the intersection of their descendant sets.
   - Skip this stage if the result would be empty, and record
     `hierarchy_conflict`.
   - Output: `candidates.hierarchy`.
   - A role **depends on** anchor A if removing A from the anchor set changes
     `candidates.hierarchy` (compared with `candidates.name` when no anchor
     remains). A skipped stage depends on no anchor.
4. **Generation gate**, for a role with a designator.
   - It is checked on the last generated set: `candidates.hierarchy`, or
     `candidates.name` if the hierarchy stage did not run or was skipped.
   - Each unit is checked against the designator's verified scope, through its
     state ancestor (`parent_id`).
   - If **any** unit lies outside the scope:
     - status `not_in_gazetteer` / `level_mapping_unverified`
     - stage flag `level_mapping_unverified`
     - `candidates.name` and `candidates.hierarchy` kept for audit
     - `candidates.pincode` is `null`
     - `final_set` is `[]`
     - the role anchors nothing
     - *Terminal.*
   - Candidates in unverified states are never silently dropped, because dropping
     them could leave a false unique match.
5. **PIN stage**, only for roles that passed the gate, and only on village-level
   candidates.
   - If the record has a valid PIN (section 9), keep only the villages
     `village_pincode` lists under that PIN.
   - For a `place_unspecified` role with candidates at several levels, only its
     village members are filtered. Other levels are left as they are.
   - Skip this stage if it would leave no village, and record `pincode_conflict`.
   - Output: `candidates.pincode`.
6. **Human decision.**
   1. Annotators first link **independently**, using only lookups they start
      themselves (section 13).
   2. In **reconciliation** they see the generated lists and record, in structured
      form, every difference between their decision and the last generated stage:
      - an **addition**: `{entity_id, reason: spelling_variant, evidence_span_id}`,
        for a unit that name matching missed
      - a **pruning**: `{entity_id, reason, evidence_span_id, guideline_section}`.
        `reason` comes from a closed, versioned list in the guidelines (section
        21.2, P7). It includes `outside_annotated_ancestor` (an ancestor the
        annotator linked as a spelling variant excludes this unit) and
        `text_does_not_support`.
7. **Reconciliation gate.**
   - An addition outside the designator's verified scope is recorded.
   - The role then gets the same outcome as a step-4 failure: status
     `level_mapping_unverified`, the flag set, `final_set` `[]`, and it anchors
     nothing. *Terminal.*
   - Human additions can't bypass verification.
8. **`final_set`** is the last generated stage, plus additions, minus prunings.
   - It is derived, never typed in.
   - Exception: when either gate failed, `final_set` is `[]`. Additions and
     prunings on such a role are recorded for audit only and have no effect.
   - One unit gives `linked`; two or more give `ambiguous`; none gives
     `not_in_gazetteer` / `no_supported_match`.
9. **Anchor invalidation**, on the adjudicated Layer C (and on each annotator's
   reconciliation C, section 14).
   - It is one pass from the top level down. Every anchor is at a higher level
     and has already been settled, so cascades resolve in one deterministic pass.
   - Anchor A, whose single generated candidate is u, still supports its anchor
     only if A's final status is `linked` with `entity_id` u.
   - Otherwise, every role that depends on A becomes `not_in_gazetteer` /
     `anchor_invalidated`, with `final_set` `[]`.
     - This includes roles that were `linked`, `ambiguous` or
       `no_supported_match`, and roles that passed the gate only because the
       anchor narrowed them. There is no re-gating.
     - Roles that failed either gate keep `level_mapping_unverified`.
   - The number of invalidated roles is recorded and reported.

**Known limitation.** An unverified designator removes its claimed level.
- "Vill. Rampur" with an unverified `village` mapping therefore has no candidates.
- A bare "Rampur" (`place_unspecified`, no designator) can still be linked at any
  level under the rules above.
- This inversion is documented, not worked around. An unverified designator is
  never treated as absent.

| Field | Required | Allowed values / format | Purpose and scientific use |
|---|---|---|---|
| `span_id`, `role` | yes | gold `span_id`. `role` is the label or one of the `also_labels`. | One link per stated role. |
| `status` | yes | the four statuses above | Systems are scored on correct abstention, not only on choosing an ID. |
| `entity_id` | if `linked` | `lgd:{level}:{code}`, present in the pinned `admin_unit.csv` at the role's level (or an allowed level) | The linking target. |
| `candidates.name`, `candidates.hierarchy`, `candidates.pincode` | for linkable roles | complete sorted lists of `entity_id`s. `null` if the stage did not run. Stage flags `hierarchy_conflict`, `level_mapping_unverified` and `pincode_conflict`. | Every candidate set can be reproduced from the pinned gazetteer. Nothing is truncated. |
| `additions`, `prunings` | if any | structured lists as above | Every human change to a generated set is recorded and can be audited. |
| `final_set` | derived | sorted list; `[]` after a gate failure or anchor invalidation | The decision set, reproducible from the stages plus additions and prunings. |
| `reason` | if `not_in_gazetteer` | the reason values above | Says why the role can't be linked, and marks which spans to re-link when coverage grows. |
| `pincode_role` | derived | `not_applicable`, `not_used`, `narrowing`, `decisive`, `conflict` (section 9) | Separates links that the PIN decided from links that are independent of it. |

Revision 1's candidate cap K, `candidate_count` and `candidate_query` are removed.
`candidate_query` could not express the PIN constraint, several ancestor
constraints, or `place_unspecified` across levels. Complete lists can express all
of these.

### 8. Address resolution (Layer D): its own status vocabulary, derived

Layer D is computed for each in-scope record and each level `L` (state, district,
sub-district, village) by a **versioned resolution procedure**
(`resolution_procedure_version`). Its inputs are gold A, gold C, the cue table
and the pinned gazetteer. It is not annotated.

A **role at `L`** is either of these:
- a role whose label is `L`'s label (`state`, `district`, `subdistrict`,
  `village`)
- a `place_unspecified` role that is linked to a unit at `L`, or whose `final_set`
  is **non-empty** and lies entirely at `L`

A `place_unspecified` role with an empty `final_set` is a role at no level. So is
one whose `final_set` spans several levels; that is a documented limitation.

Generated candidate lists of a role that is `not_in_gazetteer` (gated, invalidated
or unmatched) never feed any Layer D status or `basis`. Roles with no LGD level (`city`, `post_office`, `locality`,
`street`, `landmark`, `pincode` and the `not_applicable` labels) are never roles at
any `L`. Their Layer C status and reason (section 7) already record that the
gazetteer cannot represent them, and they do not change any Layer D status.

**Layer D statuses, checked in this order (the first that applies wins):**

| `status` | Meaning |
|---|---|
| `conflicting` | The units supported at `L` disagree. They come only from linked roles at `L` (`stated`), ancestors of linked units below `L` (`inferred_from_descendant`), or both. PIN and descendant-candidate inference never count. `candidates` lists them. A source error is recorded, not repaired. |
| `linked` | Exactly one unit at `L` is supported. `basis` says how (see below). |
| `ambiguous` | Units at `L` come only from an `ambiguous` role at `L`, there are two or more after keeping descendants of linked ancestors, and no `basis` gives a single unit. `candidates` lists them. |
| `not_in_gazetteer` | A role at `L` is `not_in_gazetteer` with reason `no_match_in_snapshot`, `no_supported_match` or `anchor_invalidated`. `anchor_invalidated` is scored only as abstention and reported separately. |
| `deferred_coverage` | The record has a role that is `not_in_gazetteer` / `level_mapping_unverified` (unverified everywhere, or rejected by a gate) whose designator's cue-table entry names `L` as its `pending_level` (section 3; this is the only use of `pending_level`). `reason` is `level_mapping_unverified`. It never fires because of a `city` or other role with no LGD level. A level for which the record has no such role is never `deferred_coverage`. |
| `no_such_level` | The pinned gazetteer has no units at `L` below the deepest linked ancestor. This is computed, and is relative to the gazetteer version. |
| `not_specified` | Nothing in the record constrains `L` beyond its ancestors. This includes records whose only other place roles have no LGD level, such as `city`. |

**`basis`** is required when the status is `linked`. When several apply, the first
in this order wins: `stated`, `inferred_from_descendant`,
`inferred_from_descendant_candidates`, `inferred_from_pincode`.
- `stated`: a role at `L` is linked.
- `inferred_from_descendant`: `L` is an ancestor of a linked unit below it.
- `inferred_from_descendant_candidates`: every unit in an `ambiguous` set below `L`
  shares this one ancestor at `L`.
- `inferred_from_pincode`: `L` is `state`, `district` or `subdistrict`, and the
  record's valid PIN (section 9) maps, in `village_pincode`, only to villages under one unit
  at `L`, consistent with the linked ancestors. This basis is never used at
  village level, because picking a village from a PIN alone would be downward
  inference, and never to produce an `ambiguous` status.

Inference only goes **upward**. Choosing a unit because it is the only plausible
child is not allowed.

| Field | Required | Allowed values / format | Purpose and scientific use |
|---|---|---|---|
| `levels.<L>.status` | derived | the seven statuses above | Per-level gold that keeps "not stated", "not covered", "doesn't exist in this gazetteer" and "contradictory source" apart. |
| `levels.<L>.entity_id` | if `linked` | `lgd:` ID at level `L` | Target of hierarchical resolution. |
| `levels.<L>.candidates` | if `ambiguous` or `conflicting` | complete sorted list | Set-based scoring. Conflict auditing. |
| `levels.<L>.basis` | if `linked` | the four values above | Separates what the record states from what is inferred, and which inference was used. |
| `levels.<L>.reason` | if `not_in_gazetteer` or `deferred_coverage` | as in section 7 | Targets for re-resolution when coverage grows. |
| `settlement_signal` | derived | `rural_signal` (a village-level role is `linked` or `ambiguous`, and no `city` role), `urban_signal` (a `city` role, and no village-level role), `mixed_signal`, `no_signal` | Used **only to stratify results**. It is computed from the text's roles, so it is not a subjective judgment, and it never affects gold. It replaces revision 1's annotated `settlement_context`. |

**Evaluation semantics for D**, fixed now. Metric formulas belong to the
task-definition document (section 21.3, L2).
- **Primary per-level score:** over levels whose gold is `linked` with basis
  `stated` or `inferred_from_descendant`.
- **Reported separately:**
  - basis `inferred_from_descendant_candidates`
  - basis `inferred_from_pincode`
  - `ambiguous` (scored against the set)
  - `conflicting`
  - abstention correctness for `not_in_gazetteer`, `deferred_coverage`,
    `no_such_level` and `not_specified`, with `anchor_invalidated` counted
    separately

### 9. PIN as evidence versus PIN consistency

A PIN plays two roles that must not be mixed: **evidence** that helps choose a
village, and an **independent check** of the source against LGD.

**Valid PIN.** A record has a valid PIN when its `pincode` spans give exactly one
distinct value that normalizes (Layer B) to 6 ASCII digits with a non-zero first
digit (`docs/gazetteer.md`, `invalid_pincode`).
- Repeats of one value count once.
- Several distinct values mean the record has no valid PIN.
- A valid PIN that `village_pincode` doesn't list leads to `pincode_conflict`. It
  is not invalid.
- The PIN never anchors and never establishes verification scope (section 7).

**`pincode_role`** is derived for each village-level link in Layer C. For a
mixed-level `place_unspecified` role it is computed on the village subset, and the
role counts as village-level only if it ends up linked to a village.
- `not_applicable`: the record has no valid PIN, the role is not village-level, or
  **the PIN stage did not run** (for example after a gate failure).
  `not_applicable` never means that a PIN was checked.
- `not_used`: the PIN stage did not change the candidate list.
- `narrowing`: the PIN stage shrank the list in any way other than `decisive`.
- `decisive`: the last stage that ran before the PIN stage (hierarchy, or name if
  hierarchy did not run) had two or more candidates, and the PIN stage left
  exactly the final linked unit.
- `conflict`: the PIN stage would have left nothing, so it was skipped.

**`pincode_consistency`** is derived for each in-scope record:
- `consistent` or `inconsistent`: the village level is `linked` (its basis is
  always `stated`; section 8), `pincode_role` is not `decisive`, and the stated
  PIN is, or is not, listed for that village in `village_pincode`. A `conflict`
  with a linked village is therefore `inconsistent`.
- `not_independent`: the PIN decided the village (`pincode_role` is `decisive`).
  Agreement between the PIN and the village is then true by construction, so it
  is **excluded**.
- `not_checkable`: otherwise. It is reported by its first applicable cause, in
  this order:
  1. no valid PIN
  2. the village level is `deferred_coverage` (verification missing)
  3. no village-level link for any other reason

  The causes are derived from existing fields, and no field is added.

**Evaluation semantics:**
- The source-versus-LGD PIN disagreement rate is `inconsistent / (consistent +
  inconsistent)`. It is never computed over `not_independent`.
- Linking results (C) are reported separately for each `pincode_role`.
- In D, `inferred_from_pincode` levels are kept out of the primary score
  (section 8).

### 10. Pinning the gazetteer version

- Layer C entries and the derived Layer D record `gazetteer_version`. A gold
  release has exactly one.
- A validator, to be built later, rejects:
  - an `entity_id` that is missing or at the wrong level
  - candidate stages that don't reproduce from the gazetteer
  - a `final_set` that doesn't follow from the stages, additions and prunings
- **Moving to a new gazetteer version is a migration, not an edit.**
  1. Candidates are generated again and D is derived again.
  2. Changed links are reviewed.
  3. A new gold release is produced (section 18). The old release is kept.
- **A verification change after the guidelines freeze** (a new or revised level
  mapping, ADR-0007 §8) is also a migration.
  - It needs a new `cue_table_version`.
  - Candidates are regenerated, new Layer C work is done for affected roles, and
    D is derived again.
  - Layer A is unchanged, because it records roles as written.

### 11. Raw text versus normalized text

- `raw_text` is immutable and is the only text input.
- No Unicode normalization is applied before offsets are computed.
- Normalized forms exist only in Layer B and never replace `raw_text`.
- `name_key` is used only for matching (candidate generation, duplicate
  detection). It is not stored as gold.

### 12. Admissible sources and privacy

A record is admitted only if **all** of these hold under the written, versioned
screen, checked before anything reaches `data/processed/`:

1. Its source has a manifest whose licence permits the intended use (ADR-0001 §1,
   §5).
2. It is the address of an institution, facility or public place, published by its
   operator or a government body.
3. It contains no identifier of a natural person: names of addressees or occupants
   ("c/o", "s/o", "w/o", "d/o" plus a name), phone numbers, email addresses or
   government ID numbers.
4. It is not residential-looking.
5. It is not personal data under ADR-0001 by any other route, for example a
   beneficiary list.

**Staged screening.** The screen runs in two stages, so that no person reads a
record before its split is frozen (ADR-0007 §5) and nothing that fails reaches
`data/processed/` (ADR-0001 §2):
1. **Rules-only screen** (`admission.screened_by: rule:{name}`), before the split.
2. The split is **computed and frozen in a staging area** outside
   `data/processed/` (for example `data/interim/`, ignored by git like all of
   `data/`). Staging holds only `raw_text` and allowlisted `source_context`.
3. **Human screen** on the staged records, after the freeze. It is the first human
   exposure (section 17).
   - Dev and train records may be screened by anyone.
   - Test and `test_source_holdout` records are screened only by people who don't
     write or change the guidelines or the cue table.
4. **Only records that pass** are written to `data/processed/`.

A record that fails the human screen is excluded without recomputing or moving any
other record's frozen split assignment (section 17).

**Failure handling:**
- A record that fails is **excluded whole, never redacted**. Redaction would
  change the published text and teach models the placeholders.
- **Duplicate classes.** A withdrawal or human-screen failure excludes the
  record's whole duplicate class (section 17 step 4). `name_key` keeps letters and
  digits, so an identifier in one member's text is in every member's.
  - Such cascades are counted separately.
  - A failure caused only by a `source_context` value stays a per-record
    exclusion.
- Excluded records are not stored. Failed staged records are deleted from staging.
  Only aggregate counts per rule are kept, plus the denylist below.
- **Denylist.** Withdrawals and human-screen exclusions are recorded in an
  internal denylist.
  - Entry: `source_id`, `source_record_ref`, `raw_text_sha256`, a reason
    category, the date.
  - It is kept in private maintainer storage. It is never committed and never
    released.
  - It is applied as a versioned screen rule, and every change bumps
    `screen_version`.
  - An entry matches a record when all three identifiers are equal. The record's
    whole duplicate class is then excluded in that build.
  - Rebuilds from the same pinned snapshots are therefore deterministic.
  - **Limitation:** a new snapshot that drops the original row or changes its
    text, and a duplicate that appears in another source after the original row
    has gone, match no entry. These are caught only by the human screen of the
    new ingestion.
  - The reason categories are a format question for `docs/schema.md`.
- Names that honour public figures ("Mahatma Gandhi Road") are admissible.
- Businesses named after a private person are excluded.
- **When in doubt, the record is excluded** (section 21.1, F1).

**`source_context` allowlist:**
- A source's manifest lists its approved `context_columns`. Nothing outside the
  list is ingested.
- Only administrative-geography and facility-category columns can be approved,
  such as state, district, sub-district, village, PIN and facility type.
- Columns holding names of people, phone numbers, email addresses, identifiers of
  people or free-text remarks are never approved.
- `source_context` values pass **the same screen** as `raw_text`. If any value
  fails, the whole record is excluded.

**Annotator notes:**
- Released data contains only `comment_codes` from a closed list:
  `guideline_gap`, `privacy_flag`, `unreadable`, `boundary_uncertain`,
  `other_see_internal`.
- Any free-text `internal_note` stays internal and is **never released**.

**Withdrawal before release.** An annotator who finds personal data the screen
missed sets `privacy_flag`.
- The record's duplicate class and all its annotations are then deleted from the
  working data.
- The record is added to the denylist above.
- Published logs carry only counts, because `record_id` is derived from source
  data. Revision 5 kept only the count. The denylist is private, so a rebuild
  can't silently re-admit the record.
- Exposure-log entries (section 17) for withdrawn or excluded records are kept in
  the same private store as the denylist. Only aggregate counts are published.

**Withdrawal after release** is covered in section 18.

### 13. Annotation protocol: no pre-annotation, blinding, provenance

**No pre-annotation (a hard v0 rule).** Until an annotator's independent labels for
a layer are stored and frozen (the `independent` annotation document is immutable;
nothing is overwritten), the tool and every other system must not present:
- generated candidate recommendations or generated candidate lists
- ranked candidates
- suggested entities, spans or labels, from a gazetteer or any other source
- labels generated by a model, and any other system output
- prior annotations of the same layer: other annotators' work, or labels carried
  over from earlier rounds

Adjudicated gold of an earlier layer (gold spans in passes B and C) is an input,
not a prior annotation. Complete generated candidate lists appear only after the
independent C labels are stored and frozen. They are then shown in the
reconciliation round and in the adjudication that follows it, because the
adjudicator must be able to audit how `final_set` was derived (section 3). Both
rounds come after the freeze, so this is within the no-pre-annotation rule, not
an exception to it.

*Why:* a person who is shown a suggestion tends to accept it (anchoring and
confirmation bias). The gold would then measure agreement with the suggesting
system, inherit its errors, and favour systems like it in evaluation. Independent
labels made first are also the only valid input for agreement statistics.

*What does not count as pre-annotation:* in pass C, a **lookup the annotator
starts** in the pinned gazetteer (searching for a name they typed, or browsing the
hierarchy) is a reference, not a suggestion. It must not be started or prefilled
automatically from the span, and it must not rank, preselect or highlight results.
Results are shown in an order that does not depend on the record (section 21.1,
F2 and F13).

**Blinding:**
- Independent annotators don't see each other's work or know whether a record is
  annotated twice.
- No one in passes A to C knows a record's split.
- The adjudicator sees the independent annotations (and, for C, the
  reconciliation annotations) without annotator identities.

**Annotation documents:** one per record, per layer (A, B decisions, C), per
annotator, per round. They are never overwritten. The only deletion is a
withdrawal (section 12), which removes a withdrawn record's documents.

| Field | Required | Allowed values / format | Purpose and scientific use |
|---|---|---|---|
| `annotation_id` | yes | `ann:` + UUID | Unique handle. Nothing is overwritten. |
| `record_id`, `raw_text_sha256` | yes | as in section 2 | Binds the work to one exact text. |
| `layer` | yes | `A`, `B`, `C` | Keeps layers apart. D is derived. |
| `round` | yes | `independent`, `reconciliation` (C only), `adjudication`, `review` | Agreement statistics use only `independent`. |
| `annotator_id` | yes | pseudonym `annotator:{nn}`. The key to real identities is private to the maintainer. | Per-annotator analysis without personal data. |
| `role` | yes | `annotator`, `adjudicator` | Separates labelling from deciding. |
| `schema_version`, `guidelines_version` | yes | version strings | Traceability. |
| `reference_list_version`, `cue_table_version` | yes for A and C | version strings | Pass A and C decisions depend on them. |
| `normalization_table_version` | for B | version string | B decisions depend on it. |
| `gazetteer_version` | for C | as in section 10 | Section 10. |
| `visible_inputs` | yes | subset of `raw_text`, `guidelines`, `reference_name_list`, `cue_table`, `normalization_table`, `gold_spans`, `annotator_lookup`, `generated_candidates`, `blinded_independent_annotations`, `blinded_reconciliation_annotations` | Checks that the section 3 visibility rules were followed. |
| `tool`, `tool_version` | yes | strings | Effects of the tool can be traced. |
| `created_at` | yes | ISO 8601, UTC | Ordering and auditing. Not released (section 18). |
| `comment_codes` | optional | the closed list in section 12 | Structured, releasable notes. |
| `internal_note` | optional | free text, never released | Working notes. |

Adjudicated gold documents also record `source_annotation_ids` and, for each
disputed item, a `decision` (`accept:{annotation_id}`, `merge`, `replace`) and a
`rationale` that names a guideline section.

Deferred out of v0: `annotator_profile` and `time_spent_seconds`. They are
personal data about a very small group of annotators and are not needed for v0
evaluation.

### 14. Guidelines and agreement

The guidelines are versioned and frozen before gold annotation starts.
- Before that freeze, every level mapping in the cue table is verified, or is
  explicitly frozen as unverified (ADR-0007 §8).
- Guideline examples come only from the dev pool, or are clearly marked as
  invented.

They need these sections:

1. scope tests
2. the privacy screen and flagging
3. a definition of each label, with examples from dev-pool records or clearly
   marked as invented
4. how to use the cue table and the reference name list
5. boundary rules, with Indic-script examples
6. spans with two roles
7. language and script tags
8. the procedure for normalization decisions
9. the linking procedure, including reconciliation, additions and the pruning
   reason list
10. adjudication and rationale codes

**Agreement is measured for every decision a person makes**, on the dev pool:

| Human decision | Agreement measure |
|---|---|
| Privacy screen (if done by a person) | percentage agreement and kappa on admit/exclude, computed at screening time as counts only, because excluded records are not kept. Every exclusion stands, whichever screener made it. |
| A: `scope` | kappa |
| A: spans and `label` | pairwise span F1, exact and overlap; kappa on labels of matched spans |
| A: `also_labels` | F1 on the role sets of matched spans |
| A: `languages` | exact set agreement and Jaccard |
| B: `decisions` | kappa on the choices for flagged matches |
| C: independent `status` and `entity_id` | kappa on status; agreement on `entity_id` where both annotators linked. Statuses fixed mechanically (non-linkable defaults, designators unverified everywhere, generation-gate failures) are excluded and counted separately. Reconciliation-gate failures stay in. |
| C: reconciliation prunings and additions | agreement on the resulting `final_set` (Jaccard), after anchor invalidation is applied to each annotator's C. Generation-gate failures are excluded and counted. Reconciliation-gate failures and `anchor_invalidated` roles stay in. |
| D | not annotated. Derived once per annotator from **gold A plus that annotator's independent C**, the cue table and the pinned gazetteer, with mechanically fixed entries taken from generation. Anchor invalidation doesn't apply to independent C. Only records with two independent C documents count. Per level: kappa on status; `entity_id` agreement where both are `linked`; Jaccard on `candidates` where both are `ambiguous` or both `conflicting`; `basis` agreement where both are `linked`; `reason` agreement where both are `not_in_gazetteer` or both `deferred_coverage`. A status disagreement is counted only by the kappa. |

**Independent C stores a set for `ambiguous`.**
- When an annotator's independent status is `ambiguous`, they record
  `independent_set`: the complete sorted list of units their own lookups found
  (at least 2).
- `linked` stores only `entity_id`; `not_in_gazetteer` stores only `reason`.
- This is the minimum needed to derive D per annotator.

Thresholds for freezing the guidelines come from the pilot (section 21.2, P1).
After the freeze, any change creates a new `guidelines_version` together with an
assessment of which labels it affects.

**Pilot records** are taken from the dev pool. If they later become gold, they are
annotated again under the frozen guidelines.

### 15. Ambiguity and adjudication

- **Referential ambiguity is gold.** A record that doesn't identify one unit gets
  `ambiguous`. Disagreement between annotators goes to adjudication. A guideline
  gap is recorded as `rationale: guideline_gap` and fixed in a later guideline
  version.
- **Who annotates what:**
  - Records in `dev`, `test` and `test_source_holdout` are annotated
    independently by two annotators, layer by layer.
  - Records in train get one annotator plus a sampled review. The rate is set in
    the pilot (P1).
  - The record's split is known before annotation starts (section 17), so this can
    be applied.
- **Adjudication.** The adjudicator works blinded (section 13), chooses, merges or
  replaces, and never records a guess as `linked`. If neither link is supported by
  the text, the result is `ambiguous` or `not_in_gazetteer` / `no_supported_match`.
- **`merge` for candidate sets** is the union on edits: the generated stage, plus
  every addition either annotator made, minus only the prunings both made.
  - The reconciliation gate (section 7 step 7) and anchor invalidation (step 9)
    then apply.
  - The adjudicator may afterwards `replace`, with structured additions and
    prunings.
  - Defined cases:
    - two empty sets give `[]`
    - {a} and {b} give {a, b}, so `ambiguous` unless a reasoned pruning follows
    - an out-of-scope addition by either annotator fails the gate
    - if one annotation is missing, `merge` isn't available; only `accept` or
      `replace`
  - Roles that failed the generation gate are never adjudicated: the outcome is
    fixed before any human decision. A reconciliation-gate failure comes from one
    annotator's addition, so it is adjudicated like any other disagreement.
  - Intersection is never used: it can turn {a, b} and {a} into a false unique
    link.
- Independent annotations are kept unchanged.

### 16. What systems receive

| Evaluated layer | System receives | Notes |
|---|---|---|
| A | `raw_text` | — |
| B | `raw_text`; gold spans (oracle setting) or its own spans | — |
| C | `raw_text`; gold spans (oracle setting) or its own spans | — |
| D | `raw_text` | — |

For every layer a system may also use the **pinned gazetteer** (`admin_unit.csv`
and `village_pincode.csv` at the release's `gazetteer_version`), the published
**reference name list**, **cue table** and **normalization table**, and the
**train** split with its gold.

Systems **never** receive:
- `source_context`, `source_id` or other source metadata (no metadata is approved
  for systems in v0)
- split keys
- dev or test gold
- anything else not listed above

Adding any input requires a schema version change that updates **both** this table
and the annotator visibility rules in section 3.

The visibility rules are aligned: everything annotators may use is available to
systems, so the gold never depends on information systems lack. Systems evaluated
on Layer A may use the whole pinned gazetteer, while pass-A annotators had only
the reference list.
That gives systems more, not less, and does not leak gold. The generated
candidate lists that annotators see after the independent C freeze (section 13)
are not a separate input: they are reproducible from the pinned gazetteer, the
cue table and the spans that systems already receive (section 7).

Whether there is also an "open" track allowing external resources and pretrained
models, and how its results are labelled, is decided by the task-definition
document (section 21.3, L2). The contract above defines the **closed** setting.

### 17. Train, dev and test splits

The split is computed **at ingestion, before any annotation**. It never uses gold
labels. It decides which records get double annotation (section 15). It is
versioned (`split_version`).

**Freeze point.** The split is computed and frozen in staging **before the first
human exposure** of any admitted record (section 12).
- Human exposure means a person viewing an individual record's `raw_text` or
  `source_context`, for screening, pilot, guideline work or annotation.
- Scripted aggregate statistics, and the distinct-value lists used for value
  aliases (ADR-0007 §5), are not exposure.
- **Exposure log.** From the first exposure on, an exposure log records the record
  or duplicate class, the person's pseudonym, the purpose and the date.
  - It is kept with the denylist in private storage (section 12).
  - Only aggregate counts are published.
- **Exposed records never enter test.** A later bug-fix recompute (a new
  `split_version`) may never move an exposed record into `test` or
  `test_source_holdout`.
- **Assignments are fixed per `record_id`** when the split is first computed.
  Removing a record later (a failed human screen, a withdrawal) never recomputes
  or moves another record's key or split.
- **Accidental exposure.** If a person who writes or changes the guidelines or the
  cue table sees a `test` or `test_source_holdout` record outside test annotation:
  - It is logged.
  - The record stays in place, and its duplicate class is flagged `exposed`.
  - Test metrics are reported with and without exposed classes.
  - Any later guideline or cue-table change by that person must cite only dev or
    train evidence.

Revision 5 froze the split "before any model experiment", which allowed recomputes
after people had read records.

**Split key procedure**, versioned as `split_key_procedure_version`, uses only
allowlisted `source_context`, the source manifest, `raw_text` and the pinned
gazetteer. Neither the resulting key nor `source_context` is ever shown to
annotators.

**Column values (steps 1 and 2).**
- Only the column the manifest declares as `state_column` or `district_column`
  is used (ADR-0007 §5). A column's name alone never makes it one.
- A value "has a value" only if, in this order:
  1. its `name_key` is not one of that column's cited missing-value tokens. A
     token such as "NA" that the publisher defines as "Not Available" is treated
     as missing.
  2. `name_key(v) != ""`
- A present value is then matched by its exact `name_key`:
  1. first against the column's maintainer-approved value aliases
  2. then against LGD names
- No fuzzy matching. Stored values are never rewritten.

1. **State.**
   - If the record has a value in the declared state column, match it to an
     LGD state as above.
   - Otherwise, if the manifest declares `coverage_state` (ADR-0007 §5), use
     that `lgd:state:` ID directly. It is not name-matched.
   - Otherwise the state is unknown. Whether such records are retained is
     ADR-0007 O4.
   - **Two exclusion reasons.** Neither value is ever chosen over the other,
     and `coverage_state` is never a fallback for a column value:
     - `state_column_unmatched`: the column has a value and nothing matches
       it. The state is unknown even if `coverage_state` exists.
     - `state_coverage_disagreement`: the column value matches a state, and
       the manifest declares a different `coverage_state`.

     A record with either reason is **excluded** from the annotation pool
     pending resolution. It takes no part in steps 2 to 5, gets no
     `record_id` or split, and is not written to `data/processed/`. Records
     are counted per source and per reason at ingestion, and the two reasons
     are never added together into one count.
   - **Resolution.** An exclusion is resolved only by a documented,
     evidence-based correction or disposition:
     - correcting the manifest's `coverage_state` or the source's
       state-column mapping;
     - or rejecting the affected records, or the source.

     Evidence is limited, before and after the split, to the kinds ADR-0007
     §5 allows for source assessment: publisher documentation, the header row
     and scripted aggregate statistics. Never model predictions, gold labels,
     annotations or a person reading records. The record of a resolution
     states:
     - the source and the reason;
     - the number of records affected;
     - the evidence, cited by URL and retrieval date or by script and output
       hash;
     - the outcome, the date and who decided.

     It is kept with the source's assessment or source ADR. A correction made
     after the split is first computed is a change to the source set and
     follows ADR-0007 §7.
   - Revision 4 used "or", name-matched both inputs and had no rule for an
     unmatched value or a disagreement.
2. **District.**
   1. **District column.** If the record has a value in the declared district
      column, match it as above:
      - within the known state, if there is one. A district in another state is
        never matched.
      - across India, only if the state is unknown
      - Exactly one district: use it.
      - No match: the district is unknown, counted as `district_column_unmatched`.
      - Several matches: the district is unknown, counted as
        `district_column_ambiguous`.
      - In both of those cases there is **no fall-through to text**. The record is
        kept, with the step 3 key for an unknown district.
   2. **Text.** Only if the record has no district-column value: district names
      from the reference list that appear as whole-token sequences in
      `name_key(raw_text)`, within the known state if there is one.
      - Tokens are `name_key(raw_text).split(" ")`.
      - Exactly one district: use it. None, or two or more: no district from text.
   - A district column that matches is used even when the text names another
     district. Such disagreements are counted per source and never change the key.
3. **Group key.** `lgd:district:{code}` if a district was found. Otherwise
   `unresolved:lgd:state:{code}`, or `unresolved:unknown`. The source is **not** part
   of the key. In revision 1 it was, which let the same place, published by two
   sources, end up in different groups.
4. **Duplicate classes.**
   - Records whose `name_key(raw_text)` values are identical, across all sources,
     form one **duplicate class**. Only identical values join a class. Districts
     or step-3 groups are never merged, and nothing is grouped transitively.
   - The class key is the lexicographically smallest step-3 key of its members.
     Every member gets the class key as its `group_key`.
5. **Assignment.**
   - **Held out.** A duplicate class with any record from a held-out publisher goes
     wholly to `test_source_holdout`.
     - The designation is per publisher, listed in the versioned split
       configuration (ADR-0007 §6).
   - **Bucket mapping.** Every other class goes to `train`, `dev` or `test`:
     1. Message: `group_key + "\n" + split_salt`, encoded UTF-8, with no BOM and
        no trailing newline. `split_salt` is its 64-character lowercase hex
        string.
     2. `h` = the first 8 bytes of SHA-256(message), read as an unsigned
        big-endian integer, 0 ≤ h < 2⁶⁴.
     3. Ratios are positive integer weights `w_train`, `w_dev`, `w_test`, with W =
        their sum. A zero weight is a configuration error.
     4. `b = (h × W) >> 64`, in exact integer arithmetic.
     5. Half-open intervals, in the fixed order train, dev, test:
        - `train` if b < w_train
        - `dev` if b < w_train + w_dev
        - otherwise `test`
   - The weight values are deferred (section 21.2, P6).
   - **Synthetic test vectors.** These are not benchmark data. An implementation
     must reproduce them.
     - Salt: the SHA-256 hex of the ASCII bytes `pata synthetic test-vector salt`
       = `c2486d9637f8cc990bec2ea16a39999692387fdddd099c55df427bc6c8745b2a`.
     - Weights: 8/1/1.

     | `group_key` | h (hex) | split |
     |---|---|---|
     | `synthetic:a` | `63b6c9c4c2b75d54` | train |
     | `synthetic:b` | `f5f0f6a861bb0d63` | test |
     | `synthetic:c` | `53526df4c6a3e805` | train |
     | `synthetic:d` | `8c1fd55acbb2aebd` | train |

     Boundaries (weights 8/1/1):
     - h = `cccccccccccccccc` → train
     - h = `cccccccccccccccd` → dev
     - h = `e666666666666666` → dev
     - h = `e666666666666667` → test
   - **Salt.**
     - 32 bytes from the operating system's cryptographic random generator,
       generated once, before the first split computation.
     - Committed to the versioned split configuration before that run, and
       published with the release.
     - Immutable for its `split_version`, and never regenerated after any split
       result has been seen.
     - A new salt means a new `split_version`, recorded with its reason.

**Split names:**
- `test` holds out **whole groups**. It is **not** an i.i.d. sample. Revision 1's
  "in-distribution test" was wrong.
- `test_source_holdout` holds out whole sources, to measure template effects.

**Known limits, measured rather than assumed:**
- A key derived from source columns or text matching can be wrong. After gold
  exists, a **leakage audit** reports:
  - the share of test records whose gold Layer D district differs from their split
    key
  - the share of test records whose gold district also appears in train
  - the share of test gold `entity_id`s that also appear in train

  The audit is reported. It never moves records after the split is frozen.
- Unresolved groups can be large. How many records end up unresolved is counted
  at ingestion, before the split is first computed (P6).
- Adding sources or records in a later release can add members to a duplicate
  class (step 4) and so change the `group_key`, and the split, of records already
  assigned. How assignments carry over between releases is open (section 21.3,
  L5).
- A recompute is allowed **only** to fix a bug in the procedure.
  - It is a new `split_version`, and it never uses gold.
  - It never moves an exposed record into `test` or `test_source_holdout`.

The table below fixes **what** the split file must record. Its exact field
names, structure, types and serialization are defined in `docs/schema.md`
(ADR-0007 E3).

| Split-file field | Required | Allowed values / format | Purpose and scientific use |
|---|---|---|---|
| `record_id` | yes | as in section 2 | Joins the split to the record. |
| `split` | yes | `train`, `dev`, `test`, `test_source_holdout` | Evaluation partition. |
| `group_key` | yes | the duplicate-class key (step 4) | Leakage audit: no key appears in two splits. |
| `split_version` | yes | version string | Reproducibility, and protection against silent re-splitting. |

### 18. Release manifest and withdrawal after publication

Every gold release has a **release manifest**. A release is immutable. Any change
makes a new release.

The table below fixes **what** a release manifest must record. The normative
field names, structure, types and serialization of the release manifest and
the split configuration are defined in `docs/schema.md` (ADR-0007 E3). Each
release ADR records that release's values and references the schema; it
does not redefine the format.

| Field | Purpose |
|---|---|
| `benchmark_version` | Identity of the release (semantic versioning, rules below). |
| `release_date` | When it was published. |
| `schema_version`, `guidelines_version` | The rules the labels follow. |
| `gazetteer_version` and the SHA-256 of `admin_unit.csv` and `village_pincode.csv` | The exact reference data. |
| `sources`: `source_id`, snapshot SHA-256 and the SHA-256 of the source manifest's content for each source | The exact input snapshots. The manifest hash covers everything a manifest adds that changes records or splits: `coverage_state`, `context_columns`, column roles, value aliases, missing-value tokens, the `raw_text` field and scope, `record_id_scope`. |
| `screen_version` | The privacy rules applied, including the state of the private denylist (section 12). Neither the denylist nor its hash is published. |
| `reference_list_version`, `cue_table_version`, `normalization_table_version` | Tables that annotation and generation depend on. |
| `ingestion_procedure_version`, `normalization_procedure_version` | Decoding (section 2) and the Layer B procedure (section 6). |
| `candidate_procedure_version`, `resolution_procedure_version`, `split_key_procedure_version` | Procedures that generate or derive gold and splits. |
| `focus_state_version` | The focus-state list (ADR-0007 §2). |
| `split_version`, `split_salt`, ratio weights | The salt and weights are published with the release, so splits can be regenerated. |
| Code provenance: Pata git commit, Python version, `unicodedata.unidata_version`, and the SHA-256 of the pinned `Scripts.txt` (section 2) | `name_key`, decoding and `scripts` depend on them. |
| Release report: path and SHA-256, listed in `files` | Published aggregate counts: exclusions per reason (sections 2, 12 and 17), duplicate-class cascades, exposure, `anchor_invalidated` roles, and mechanically fixed statuses (section 14). |
| Held-out publisher list | Which publishers form `test_source_holdout`, as fixed in the versioned split configuration (ADR-0007 §6). Its field name and format are defined in `docs/schema.md` (ADR-0007 E3), not here. The release ADR records the list for that release. |
| `files`: path and SHA-256 for each file | Integrity of every file in the release. |
| `errata` | References to the errata entries this release incorporates. Entries found later are recorded in the errata log, not in this manifest. |
| `licence`, `attribution` | Deferred to the release ADR (section 21.3, L1). |

Not released: `annotator_id` mappings, `internal_note`, `created_at` and other
timing data, the denylist and the exposure log.

**`benchmark_version` rules:**
- **MAJOR:** any change that makes scores not directly comparable. That means
  changes to records (additions or withdrawals), to splits (`split_version`), to
  `gazetteer_version`, or to gold semantics (labels, statuses, procedures that
  change gold).
- **MINOR:** additive release content that changes no record, split or gold.
- **PATCH:** documentation or packaging fixes, only when every gold and split file
  keeps its SHA-256.

**Errata log.** Errata live in an append-only log outside releases (for example
`docs/errata.md`).
- An entry records the date, the affected release versions, a reason category
  and the number of records removed.
- It never contains raw text, `record_id`s or hashes.
- Releases stay immutable. A release manifest lists only the entries it
  incorporates.

**Withdrawal after publication.** A copy that has been published cannot be
recalled. When personal data, or any other reason for withdrawal, is found in a
release:

1. A new release is made without the affected records.
2. An **errata entry** is appended to the errata log. It contains the date, the
   affected release versions, a reason category and the number of records
   removed. It never contains the record's text, `record_id` or hashes. The
   record and its duplicate class are added to the denylist (section 12).
3. Pata stops distributing the affected releases wherever it controls
   distribution.
4. Scores on different releases are marked as not directly comparable.

Stand-off distribution (L1) reduces this exposure, because the text stays with
its source.

### 19. Urban coverage

Urban addresses are in scope for A and B, and for C wherever a role is linkable
(for example state and district). How urban coverage appears in each layer:
- `city` roles: `not_in_gazetteer` / `urban_deferred`.
- `locality`: always `entity_type_not_modelled`, because LGD has no locality level
  at all.
- Layer D: a `city` role is not a role at any LGD level, so it changes no Layer D
  status. A level the record does not otherwise state stays `not_specified`.
  `deferred_coverage` is used only for a role with an unverified designator whose
  cue-table `pending_level` (section 3) is that level, and `no_such_level` only
  where the gazetteer has no units below the deepest linked ancestor (section 8).
- Results: always reported by `settlement_signal`. A headline linking number must
  state which share of roles was linkable.
- Village names with suffixes such as `(Ct)`, `(Og)` or `(Part)` are matched and
  linked only as the village-level verification record establishes (ADR-0007 §8).
  - Their meaning and their matching behaviour, including whether the name stage
    strips the suffix, are not assumed.
  - Revision 5 linked `(Ct)` units as villages without evidence.

### 20. Extending the schema beyond v0

- **`schema_version` uses semantic versioning.**
  - Minor: new labels, reasons, statuses, optional fields, ID namespaces or
    approved inputs (updating sections 3 and 16 together).
  - Major: splitting, merging or redefining a label, or changing offsets. Existing
    gold is migrated, not edited.
  - A label's meaning is never reused.
  - `schema_version` versions the format. The release identity, `benchmark_version`
    (section 18), is versioned separately.
    - A schema change that changes any gold makes the next release MAJOR, even
      when it is only a minor schema version.
    - A new status is one example.
- **New gazetteer content uses new ID namespaces:** `lgd:localbody:` (local-body
  codes overlap village codes), `dop:po:`, `pin:`.
- **Reasons mark what to re-link when coverage grows:**
  `urban_deferred`, `source_deferred`, `level_mapping_unverified`.
- **`block`** can be added once LGD semantics are verified for the selected
  geography (L3).
- **Nested spans** can be added with an optional `parent_span_id` if a case
  appears that two roles on one span can't express.
- **Synthetic data** needs `source_type: synthetic` plus generator fields in a
  minor version, and must follow the ADR-0001 §3 reporting rules.

### 21. Decisions

#### 21.1 To approve with this ADR (freeze now)

| # | Was | Proposal | Why it must be frozen before any annotation |
|---|---|---|---|
| F1 | U7 | Exclude whole records, never redact. Names honouring public figures are allowed. Businesses named after private persons are excluded. When in doubt, exclude. A withdrawal or human-screen failure excludes the record's whole duplicate class; a failure caused only by `source_context` stays per record (section 12). (Revision 6 adds the class cascade.) | Decides what may enter `data/processed/` at all. |
| F2 | U8 | No personal or world knowledge in any layer. Only the inputs in the section 3 visibility table: the reference name list and cue table and, in pass C, gazetteer lookups the annotator starts themselves (not prefilled, ranked or preselected). Independent passes never include generated candidates (F13). | Defines what the gold measures and how the visibility rules match the system inputs. |
| F3 | U9 | PIN semantics as in section 9: the valid-PIN rule, `pincode_role` (including "PIN stage did not run" under `not_applicable`), exclusion of `not_independent`, the ordered `not_checkable` causes, D strata, and `inferred_from_pincode` only above village level. A PIN never sets verification scope. (Revision 6 adds the valid-PIN rule, the `pincode_role` cases and the `not_checkable` causes.) | The PIN circularity would otherwise corrupt both linking gold and the consistency statistic. |
| F4 | U10 | A city named like its district does not imply that district. | Upward-only inference; changes district-level gold. |
| F5 | U13 (principle) | The split is computed at ingestion from the split key procedure in section 17, never from gold, and frozen in staging before the first human exposure of any record. Exposure is logged, assignments are fixed per record, and exposed records never move into test. (Revision 5: "frozen before experiments".) | Double annotation and pilot sampling depend on the split. |
| F6 | U14 | No synthetic records in v0. `source_type` is kept and is always `real`. | Scope, and ADR-0001 §3 reporting. |
| F7 | U15 | Flat spans, with spans carrying two stated roles via `also_labels`. | Representation. Changing it later is a major version. |
| F8 | U16 | `record_id` scopes as in section 2. | Identity. Revision 1's stability claim was false for row references. |
| F9 | new | Layer D is derived, with its own seven-status vocabulary and `basis` values, applied in a fixed `basis` precedence. `deferred_coverage` fires only through the cue-table `pending_level` of a designator that is unverified, or that a gate rejected (the single LGD level whose mapping is pending verification), never because of a `city` or other role with no LGD level. `pending_level` drives no annotation, candidate generation, ranking or linking. Gated or invalidated candidate lists never feed D. Layer B is generated, with human decisions only for flagged matches. (Revision 6 adds the `basis` precedence, gate-rejected designators and the rule on candidate lists.) | Gold that can be reproduced; no subjective D labels. |
| F10 | U18 | No `block` label in v0. Block and sub-division designators count as unverified, and those spans are labelled `place_unspecified` and unlinked (`level_mapping_unverified`). Their `pending_level` is named only on a cited source (section 3). | Avoids assuming LGD semantics that haven't been verified. |
| F11 | U17 (replaced) | `settlement_signal` is derived and used only for stratification. | Removes a subjective field that drove gold. |
| F12 | new | `source_context` allowlist and screening. Screening is staged: a rules-only screen, then the split frozen in staging, then a role-restricted human screen, then `data/processed/`. Only structured comment codes are released. (Revision 6 adds the staging.) | Privacy (ADR-0001 §2) and no pre-split exposure (ADR-0007 §5). |
| F13 | new | No pre-annotation (section 13): until independent labels are frozen, no generated candidate recommendations or lists, ranked candidates, suggested entities, model labels or prior annotations of the same layer are presented. Complete generated candidate lists become available only after the independent C labels are stored and frozen, and are then shown in C reconciliation and the adjudication that follows it, so that the derivation of `final_set` can be audited. Annotators are blinded to each other. The adjudicator is blinded to annotator identities. | Protects the gold against confirmation bias. |
| F14 | new (revision 6) | Layer A records roles as written. A designator's LGD level mapping is verified only under ADR-0007 §8, national or per state. It gates only Layer C and Layer D: through the generation gate (any candidate outside the verified scope makes the role `level_mapping_unverified`, lists kept for audit, `final_set` empty) and the reconciliation gate (human additions can't bypass it). An unverified designator never falls back to the no-designator route. Anchor invalidation (`anchor_invalidated`) follows the section 7 precedence. | Gold links never rest on unverified LGD semantics, and the gate is reproducible from system inputs. |
| F15 | new (revision 6) | A private, unreleased denylist of withdrawals and human-screen exclusions is applied as a versioned screen rule. The exposure log is kept in the same private store. Errata go in an append-only log outside releases. | A rebuild from the same snapshots can't silently re-admit an excluded record; releases stay immutable. |

#### 21.2 Deferred until data exists (not to be decided without it)

P1 to P5 and P7 are answered by the pilot. P6 is answered from ingestion-time
aggregate statistics before the split is first computed, never from pilot
annotations.

| # | Was | Question |
|---|---|---|
| P1 | U5 | Pilot size, train review rate, agreement thresholds for freezing the guidelines. |
| P2 | U12 | Whether designators sit inside spans or outside. |
| P3 | new | Merging or removing `premise_name`, `country`, `unit`; whether the two-role precedence order works; how often `place_unspecified` is used. |
| P4 | new | The contents of the normalization table; whether Layer B is a v0 evaluation task. |
| P5 | new | Rules for labelling a bare name as `state` or `district` from the reference list when the same name is also a village or other place. |
| P6 | U13 (rest) | Split ratios; acceptable share of unresolved groups; whether `test_source_holdout` is feasible. Answered from ingestion-time aggregate statistics before the split is first computed, never from pilot annotations, because pilot records come from the dev split. Which publishers are held out is decided only under ADR-0007 O5, which uses this feasibility answer (revision 5; revision 4 also asked "with which publishers of the approved sources"). |
| P7 | new | The closed list of pruning reasons. |

#### 21.3 Deferred to another ADR or document

| # | Was | Question | Where |
|---|---|---|---|
| L1 | U3 | Licence of the annotations; shipping `raw_text` or stand-off | A release ADR, before the first publication |
| L2 | new | Task and metric definitions; whether an "open" track exists | A task-definition document |
| L3 | U18 (rest) | LGD semantics of the state, district, sub-district and village levels, national or per state; whether to enable `block`; verifying cue-table entries | Evidence standard: ADR-0007 §8 (S9). Outcomes and enabling `block`: a new ADR or the relevant source ADR (ADR-0007 E1). Must be completed, or frozen as unverified, before the guidelines freeze (section 14). Revision 4 said "together with the focus-state ADR"; revision 5 covered the sub-district level only. |
| L4 | U4 | Annotator recruitment, consent, compensation. Consent is required either way. | An annotation-protocol document |
| L5 | new | How split assignments carry over between releases when new sources or records change duplicate merges (section 17, step 4). Unresolved; no policy is chosen here. Must be decided before any second release, or any change to the source set after a split is first computed. | An ADR amending section 17 (or a revision of this ADR while it is Proposed) |
| L6 | G2/B5 (revision 5) | Whether text not published as one address string (a concatenation of published components, or text extracted from a PDF or other document) can ever be `raw_text`, and by which versioned procedure. Until decided, it cannot (section 2). | A new ADR, or a revision of this ADR while it is Proposed |

#### 21.4 Removed from ADR-0006

- **U1** (focus states): ADR-0001 §7 gives this its own ADR.
- **U2** (sources): source ADRs and manifests. Section 12 sets the admission rules.
- **U6** (annotation tool): protocol. The tool must follow ADR-0001 §8 and
  section 13.
- **U11** (candidate cap K): eliminated, because complete candidate lists replace
  it.

U17 (`settlement_context`) is not removed: it is replaced by F11.

## Consequences

- Each layer has gold that can be evaluated alone. B is mostly generated and D is
  fully derived, so most of the gold can be reproduced from human decisions that
  are few and explicitly recorded.
- Ambiguity, conflicts, gaps in coverage and missing levels are distinct, labelled
  outcomes. Systems are scored on abstaining correctly.
- PIN-based decisions can be traced, and the PIN consistency statistic excludes
  cases that are true by construction.
- Splits exist before annotation and are never derived from gold. Leakage that the
  ingestion-time split key misses is measured and reported, not hidden.
- The rules are conservative: unverified designators, no `block`, no world
  knowledge, exclusion when in doubt. More records stay unlinked or out of the
  corpus. That is accepted in exchange for gold that doesn't rest on assumptions.
- Generated candidates and derived D need versioned procedures before annotation
  starts. They are part of the follow-up work.
- **Implementation order.** This is the single order shared with ADR-0007. It
  replaces both ADRs' revision 5 and revision 3 lists, which contradicted each
  other.
  1. Complete and review the coordinated ADR revisions and acceptance (this ADR
     with ADR-0007).
  2. Start LGD verification (ADR-0007 §8, E1) in parallel where possible. Finish
     it, or explicitly freeze unresolved levels as unverified, before the
     guidelines are finalized.
  3. Complete the source inventory, eligibility, documentation and licence
     assessments before accepting any source.
  4. Define `docs/schema.md` before implementing procedures that depend on its
     formats. Source manifests use its manifest format.
  5. Complete source ADRs and provenance manifests before ingesting their data.
  6. Implement ingestion (section 2), split-key step 1 and the required
     ingestion-time statistics. ADR-0008 is accepted before selection records are
     computed.
  7. Finalize the focus-state ADR and the split configuration: the salt, the
     held-out publishers, the ratio weights (P6).
  8. Run the rules-only privacy screen, then compute and freeze the split in
     staging (sections 12 and 17).
  9. Conduct the role-restricted human screen, applying the denylist and
     duplicate-class rules (section 12).
  10. Build the reference list, normalization table and cue table under the dev-pool
      restrictions (sections 3 and 6).
  11. Implement the candidate and resolution procedures, then finalize and freeze
      the guidelines (section 14).
  12. Implement and run the validator.
  13. Conduct the dev-pool pilot (P1 to P5, P7) and resolve its decisions. Only
      then proceed to gold annotation.

  None of this produces results until real admitted records exist.
