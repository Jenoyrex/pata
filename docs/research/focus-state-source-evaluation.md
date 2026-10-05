# Focus-state and source evaluation (O1, O2)

- **Kind:** Research working notes. Not an ADR, not a source assessment under
  ADR-0007 §5, and not a selection record under ADR-0007 §4 step 3. Nothing here
  selects a state, accepts or rejects a source, designates a held-out publisher or
  writes a manifest.
- **Based on:** `docs/research/source-inventory.md` as committed in `a89f609`,
  ADR-0001 to ADR-0007, and `docs/gazetteer.md`. No new retrieval or research was
  done for these notes. Evidence labels ([PUBD], [MIR], [SRCH], [ADR], [CALC],
  [U]) and source numbers (C1–C6, R#) are those of the inventory.
- **Gazetteer:** `gazetteer_version`
  `bf4a8b5d35130e7c3b94c6e4de812b3fd6deeb059497af22aac178642c2c2c78`.

## Procedural position

- ADR-0006 and ADR-0007 are both **Proposed**. ADR-0007 cannot be accepted before
  ADR-0006, and its Consequences fix the order: source assessments, a source ADR
  accepting sources (O2), ingestion-time aggregate statistics and selection
  records, then a focus-state ADR (O1).
- **Candidacy (§4 step 2)** requires an accepted source that covers the state,
  and the state must exist in the pinned gazetteer. Coverage here is the
  **declared coverage** taken from source documentation during the §5
  assessment. **Per-state record counts** belong to the selection record (§4
  step 3) and are produced from accepted source files. They are not a
  precondition for candidacy.
- **No source has been accepted, so there are no candidate states today.** The
  state table below records pre-candidate evidence only.
- The written §5 assessments do not exist yet. The inventory is their input. This
  document maps the inventory onto the §5 assessment items and the §4 diversity
  dimensions, and lists what is missing.
- ADR-0007 §5 limits pre-split assessment evidence to the publisher's
  documentation, licence text and terms, the header row of a downloaded file, and
  scripted aggregate column statistics.
  - The inventory's field lists (R32–R34 from data.gov.in, R37 from the Telangana
    portal) come from platform APIs. They are not header rows.
  - Because a platform serves them rather than the publisher, **treating them as
    "the publisher's documentation" under §5 is an interpretation that needs the
    maintainer's confirmation.** They are used below as schema evidence on that
    provisional basis only.

## O2: sources against the ADR-0007 §5 assessment items

ADR-0007 §5: "An unclear or missing licence means the source is rejected." C5 and
C6 offer reuse only on request. Whether that is a missing licence or a possible
licence basis is open (B4). **No source is recorded as rejected in these notes.**

### Overview

The inventory has seven candidate rows (C1a, C1b, C2, C3, C4, C5, C6) for six
numbered sources (C1–C6). C1, C2 and C3 are the three data.gov.in health sources.

"All India" coverage for C1, C2 and C6 is first-pass evidence only ([MIR] for
C1 and C2, the [PUB] fetch summary for C6). The second pass did not verify any
coverage statement.

| Source | Publisher (as stated) | `source_family` | Declared coverage; state column | Single address string | Licence status | Identifier → likely `record_id_scope` | Status |
|---|---|---|---|---|---|---|---|
| C1a | MoHFW / DoHFW / NIHFW [PUBD] | `government_published` if NIHFW counts as a government body (G4) | All India [MIR, R1]; `State` | `Address_Original_First_Line`, completeness [U] | Basis: ADR-0002 (2026-10-02); this pass's re-check inconclusive (sandbox) | `Hospital_Regis_Number`, stability [U]; otherwise `snapshot` | Not assessable to acceptance |
| C1b | Same as C1a [PUBD] | As C1a | All India [MIR, R1]; `State_Name` | `Address` | As C1a; file hosted at `info.nhp.gov.in`, whose terms are [U] | None → `snapshot` | Not assessable to acceptance |
| C2 | MoHFW / DoHFW [PUBD] | `government_published` (G4 open) | All India [MIR, R2]; `State Name` | `Facility Address` | As C1a | `Nin_N`, stability [U] | Not assessable to acceptance |
| C3 | MoHFW / DoHFW / CGHS [PUBD] | `government_published` (G4 open) | CGHS cities, not listed by state [U]; **no state column** | `DiagnosticCentreAddress` | As C1a | None → `snapshot` | Not assessable to acceptance |
| C4 | "Health and Medical and Family Welfare" on the Telangana Open Data portal [PUBD] | `government_published` (G4 open) | Telangana only; `State` | **None** (components only) | Publisher label only; licence text [U] | None → `snapshot` | Not assessable to acceptance |
| C5 | CEO Tamil Nadu; district administrations [PUBD] | Open (G4; CEO vs district publisher) | Per constituency (TN); statewide [U] | [U] (PDFs, not opened) | All rights reserved (CEO TN); district sites reuse on request | PS number within constituency [SRCH], stability [U] | No reuse licence found; outcome depends on B4 |
| C6 | Kendriya Vidyalaya Sangathan [PUBD] | Open (legal status not verified) | All India [PUB, R10]; 1,364 schools in India [CALC]; state filter in the search form [PUBD, R43] | [U] (search form) | Reuse on request (R42) | UDISE code searchable; stability [U] | No reuse licence found; outcome depends on B4 |

The rest of the inventory (AISHE, UDISE+, PMJAY, ABDM, oil outlets, bank locators)
is unresolved or not assessable. RBI IFSC, IFSC compilations and OpenStreetMap
are recorded there as rejected. Nothing here changes those entries.

### Per-source notes

**C1a, C1b (National Health Portal directories).**
- *Licence.* ADR-0002 verified data.gov.in's site-wide GODL-India statement on
  2026-10-02. The second-pass re-check is inconclusive because the footer served
  on 2026-10-04 carries a sandbox notice. No resource-level licence field
  exists. GODL-India exempts personal information from the licence (ADR-0002), so
  any personal information in these files is outside the licence in any case.
- *Terms and retrieval.* Whether automated retrieval is allowed is [U] (E5).
  ADR-0004 records a bot challenge on data.gov.in file URLs. The second pass
  retrieved metadata with HTTP 200 but attempted no file download. C1b's data file
  is on `info.nhp.gov.in`, whose terms were not checked.
- *Personal-data risk.* C1a's schema has `Nodal_Person_Info`,
  `Nodal_Person_Tele` and `Nodal_Person_Email_Id`, plus phone, mobile, fax and
  email fields. C1b has `landline_number`. Under ADR-0006 §12 none of these can be
  a context column. Whether person names or phone numbers also appear inside the
  address fields is [U] and is left to the record-level screen.
- *Possible `context_columns`*, as far as ADR-0006 §12 allows (administrative
  geography and facility category). Inclusion is subject to the screen and to
  aggregate statistics:
  - C1a: `State`, `District`, `Subdistrict`, `Town`, `Subtown`, `Village`,
    `Pincode`, `Hospital_Category`, `Hospital_Care_Type`
  - C1b: `State_Name`, `District_Name`, `Taluka_Name`, `Block_Name`, `pincode`,
    `Facility Type`

  Free-text fields (`Specialties`, `Facilities`, `Miscellaneous_Facilities`) and
  coordinates are not of the allowed kinds.
- *Use for annotation.* As far as the platform schema shows, C1a publishes a
  single string, `Address_Original_First_Line`, so the ADR-0006 §2 "exactly as
  published" question does not arise as it does for C4. No file header or record
  has been inspected. Whether the field is complete enough to be useful for
  Layers C and D is open (G2).
  - That can be judged only from scripted aggregate statistics, never from
    reading records.
  - Examples: the distribution of token counts per value, and the share of
    empty values, compared with the component columns.
- *Holdout.* C1a and C1b have one publisher string, so ADR-0007 §6 gives them one
  designation.

**C2 (All India Health Centres Directory).**
- Licence, terms and retrieval are as for C1.
- `Facility Address` is a single address string. In the inspected schemas, C2
  and C3 show no person or contact fields.
- Possible `context_columns`: `State Name`, `District Name`, `Subdistrict Name`,
  `Facility Type`, `Type Of Facility`. `Location Type`, `ActiveFlag_C` and
  `NOTIONAL_PHYSICAL` have unknown meanings and cannot be approved until they are
  known.
- `Nin_N` could support `native` IDs if it is stable, which is [U].
- The data is fixed at 7 October 2016, against a "Monthly" frequency (G6).

**C3 (CGHS empanelled hospitals).**
- Licence, terms and retrieval are as for C1.
- **No state or district column, and it does not cover a single state**, so it
  cannot have a `coverage_state`. Every record's step-1 state is therefore
  unknown (ADR-0006 §17 step 1), and **no C3 record can currently be attributed
  to a focus state**.
- C3 records would enter the annotation pool only if unknown-state records are
  retained (O4). If they are not, C3 contributes no records.
- The fields are named `DiagnosticCentre…` in the hospital resource (unresolved).

**C4 (Telangana health centres).**
- *Licence.* The publisher's dataset label "Government Open Data License - India"
  is verified [PUBD, R36]. The licence text it refers to is not. Under ADR-0007
  §5 the licence must be verified from the official text.
- *`raw_text`.* No single address string is published. ADR-0006 §2 defines
  `raw_text` as the string "exactly as published". Whether a concatenation of
  `Street`, `Landmark` and `Locality` can meet that definition is an open
  decision (G2), not one for an assessment.
- `coverage_state` would be `lgd:state:36`, and a `State` column exists.
- Possible `context_columns`: `State`, `District`, `Taluka`, `Facility Type`.
  `Region Indicator` has an unknown meaning. Whether `Ownership Authority` counts
  as a facility category is for the assessment.
- The datastore reports 7,001 rows. It is a single publisher, distinct from the
  central ministry.

**C5 (polling-station lists).**
- *Licence.* CEO Tamil Nadu: "All rights reserved", with no policy page linked
  (R38). The district sites allow reuse after permission requested by email
  (R39, R40). No reuse licence was found; the outcome depends on B4.
- *Further issues, independent of the licence:*
  - The lists are PDFs. How text extracted from a PDF would meet "exactly as
    published" is undefined.
  - The lists include "polling areas" describing residential areas served, which
    bears on ADR-0006 §12 rule 4. This is [SRCH]: the inventory notes that the
    summary was probably generated from the PDFs themselves.
  - The CEO site links to electoral rolls [PUBD, R38], which must never be
    retrieved.

**C6 (KVS directory).**
- *Licence.* Reuse is allowed on request by email (R42), and framing is
  disallowed. No reuse licence was found; the outcome depends on B4.
- No static schema and no bulk file were found. The directory found is a search
  form, and results load only on search.
- Whether KVS counts as "a government body" is open (G4).

### O2 result

**No source can be accepted now, and none is ready for a source ADR.**
- **C1, C2 and C3** (rows C1a, C1b, C2, C3) share one **licence** blocker:
  whether the data.gov.in sandbox notice affects the GODL-India basis recorded in
  ADR-0002. Separately, they each still need:
  - header rows (B6)
  - terms of use, including automated retrieval (B8)
  - their personal-data questions settled
- **C4** depends on its licence text (B3) and on G2 (B5).
- **C5 and C6:** no reuse licence was found, and the outcome depends on B4.
- No `operator_published` source with a licence has been found, so that family
  is empty (ADR-0007 Consequences anticipates this).

## O1: pre-candidate state evidence

**No state is a candidate** (ADR-0007 §4 step 2). Columns follow the §4 diversity
dimensions.

| State | Sources with state-specific evidence (status) | Source families documented | Publishers documented for the state | Sub-district verification (§8) | Language/script per documentation | Gazetteer properties [CALC, ad hoc] |
|---|---|---|---|---|---|---|
| Telangana (`lgd:state:36`) | C4 (licence text [U]; G2) | `government_published` only (G4 open) | 1 state department. C1, C2 and C6 declare all-India coverage (first pass: [MIR] C1, C2; [PUB] C6) | Unverified | [U] | 33 districts, 621 sub-districts, 3 sub-districts without villages, 41 same-name, 0 variant-name, median 16 villages/PIN, 0 of its PINs also map villages in another state |
| Tamil Nadu (`lgd:state:33`) | C5 (no reuse licence found; B4) | Open (C5 family not classified) | CEO TN, or one or more district administrations (unresolved). C1, C2 and C6 declare all-India coverage (first pass: [MIR] C1, C2; [PUB] C6) | Unverified | Tamil and English [SRCH, R20]; whether native-script lists are admissible is O6 | 38 districts, 317 sub-districts, 0 / 0 without villages, 88 same-name, 2 variant-name, median 7 villages/PIN, 17 of its PINs also map villages in another state |
| Karnataka (`lgd:state:29`) | C5, one district page only (no reuse licence found; B4) | Open | One district administration. C1, C2 and C6 declare all-India coverage (first pass: [MIR] C1, C2; [PUB] C6) | Unverified | [U] | 31 districts, 240 sub-districts, 0 / 0 without villages, 646 same-name, 16 variant-name, median 17 villages/PIN, 0 of its PINs also map villages in another state |
| The other 33 states/UTs | No state-specific source. C1, C2 and C6 declare all-India coverage (first pass: [MIR] C1, C2; [PUB] C6) | `government_published` (G4 open) | MoHFW (one or several publishers, G4); KVS | Unverified | [U] | In the inventory's table |

C3 is not in the table: it has no state column, its declared coverage (CGHS
cities) is not listed by state, and its records cannot currently be attributed to
any state (O4).

Observations, none of them a selection criterion:
- **Region.** ADR-0007 sets the evidence for region as the LGD state unit and
  defines no regional grouping.
  - The three states with state-specific evidence are all in southern India. That
    is general geographic context, not repository evidence and not an ADR
    dimension.
  - Ease of access is not one of the ADR-0007 §4 selection dimensions. Having
    state-specific evidence is not by itself a reason to prefer these states.
- **What would create candidates.** Among sources with a documented licence
  basis, C1 and C2 could potentially provide multi-state coverage.
  - If C1 or C2 were accepted, that could meet the §4 step 2 source condition
    for whichever states its declared coverage maps to.
  - That mapping, from "All India" [MIR] to `lgd:state:` IDs at the pinned
    `gazetteer_version`, is established during the §5 assessment and is
    currently [U]. It is not assumed to cover all 36 pinned units.
  - C3 could not, for the reasons above.
  - Other national sources (C6, AISHE, UDISE+) are unresolved, not excluded.
  - Per-state record counts come afterwards, in the selection records (§4 step
    3), from accepted source files.
- **Gazetteer properties.** The figures above come from an ad-hoc script, not
  the versioned procedure §4 step 3 requires (G10), so they cannot go into a
  selection record as they stand. Whether gaps count for or against a state is
  open (O7).
- **Language.** No candidate source documents the language or script of its
  addresses except C5 [SRCH]. For every state this dimension is currently
  unknown, and it is recorded as unknown, not guessed.
- **Holdout.**
  - For Telangana, the documented state-specific publisher is one state
    department.
  - For Tamil Nadu, it may be CEO TN or several district administrations; this is
    unresolved, so no single Tamil Nadu publisher is assumed.
  - Whether a state keeps a non-held-out publisher (§6) cannot be judged until
    sources are accepted and O5 is decided.

## Blockers, gaps and dependencies

### A. Blockers

| # | Blocker | Blocks | Owner / route |
|---|---|---|---|
| B1 | ADR-0006 and ADR-0007 are Proposed | Formal assessments, source ADR, selection records | Maintainer decision |
| B2 | data.gov.in sandbox notice vs the ADR-0002 GODL-India basis | C1, C2 and C3 licence | Documentation retrieval (see next steps) |
| B3 | Licence text behind C4's label | C4 licence | Telangana portal documentation or the Telangana Open Data Unit |
| B4 | Whether permission or reuse on request can count as an acceptable licence basis (ADR-0001 §1, §4; ADR-0007 §5) | C5, C6 | Maintainer decision; it would be a new decision, not an assessment finding |
| B5 | G2. **C4:** components only, so whether a concatenation can be `raw_text` "exactly as published". **C1a:** a single string is published, but whether `Address_Original_First_Line` is complete enough is unknown | C4; usefulness of C1a | Maintainer decision (C4); scripted aggregate statistics (C1a) |
| B6 | No header rows and no scripted aggregate statistics | §5 assessment items (personal-data risk, context-column approval) | A script within the §5 evidence limit. Per-state counts for §4 step 3 come later, from accepted source files. |
| B7 | G4: publisher identity of C1–C3; whether NIHFW, CGHS and KVS count as "a government body" | `source_family`, publisher count, holdout unit | Publisher documentation; maintainer decision |
| B9 | No versioned procedure for gazetteer properties (G10) | Selection records (§4 step 3) | Code, after approval |

The treatment of platform field lists as publisher documentation (see
"Procedural position") also needs the maintainer's confirmation.

### B. Recorded gaps and dependencies

| # | Item | Meaning |
|---|---|---|
| B8 | Whether automated retrieval is allowed: data.gov.in, `info.nhp.gov.in`, Telangana DKAN (E5) | Decides the retrieval method, not acceptance. Where terms are silent, retrieval is manual (ADR-0007 §5). |
| B10 | C3 has no state column | Dependency on O4 (retention of unknown-state records) |
| B11 | No `operator_published` source with a licence | A recorded absence. Reported, not worked around (ADR-0007 Consequences). |
| B12 | Sub-district semantics unverified for every state (§8) | Expected to be "unverified" at selection time (§4 step 3). Recorded in each selection record. |
| B13 | Address language/script undocumented for every source except C5 [SRCH] | Recorded as unknown, not guessed (§4 step 3). Bears on O6. |

## Recommended next evidence step

1. **Resolve B2 first.** C1, C2 and C3 (three of the six numbered sources, four
   of the seven inventory rows) share this licence blocker. C1 and C2 are also
   the only sources with a documented licence basis that could cover several
   states. C3 cannot, because it has no state attribution.
   1. **Determine which host is production.** Check whether `www.data.gov.in` and
      `data.gov.in`, as retrieved on 2026-10-04, are the production site or a
      sandbox, and record the evidence and date.
   2. Only then retrieve the GODL-India text (`/Godl`) and the footer from the
      confirmed production host, on a recorded date.
   3. Compare with ADR-0002.

   This uses licence text and terms only, within the §5 evidence limit.
2. **B3 and B8** are the same kind of documentation retrieval, for C4 and the
   three hosts.
3. **Then B6**, after maintainer approval: a script that downloads a candidate
   file to `data/raw/` (never committed) and checks it against a recorded
   SHA-256.
   - It prints only the header row, the row count, per-column null rates and
     value-shape statistics (for example token-count distributions).
   - It prints no record text, and no person reads the file.
   - This is §5 assessment evidence. Per-state record counts for selection
     records are produced later (§4 step 3), from accepted source files.
4. **B1, B4, B5 (for C4) and B7 are maintainer decisions,** as is the
   platform-field-list interpretation. No further evidence resolves them.
