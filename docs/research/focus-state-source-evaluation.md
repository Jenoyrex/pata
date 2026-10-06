# Focus-state and source evaluation (O1, O2)

- **Kind:** Research working notes. Not an ADR, not a source assessment under
  ADR-0007 §5, and not a selection record under ADR-0007 §4 step 3. Nothing here
  selects a state, accepts or rejects a source, designates a held-out publisher or
  writes a manifest.
- **Based on:** `docs/research/source-inventory.md` as committed in `a89f609`,
  updated with its third pass (2026-10-05, data.gov.in host and licence
  re-check) and fourth pass (2026-10-06, terms of use and retrieval conditions
  for C1–C3), ADR-0001 to ADR-0007, and `docs/gazetteer.md`. No retrieval was
  done for these notes beyond what the inventory records. Evidence labels
  ([PUBD], [ARCH], [MIR], [SRCH], [ADR], [CALC], [U]) and source numbers
  (C1–C6, R#) are those of the inventory.
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
| C1a | MoHFW / DoHFW / NIHFW [PUBD] | `government_published` if NIHFW counts as a government body (G4) | All India [MIR, R1]; `State` | `Address_Original_First_Line`, completeness [U] | Basis: site-wide GODL-India, ADR-0002 (2026-10-02); third-pass re-check (2026-10-05): sandbox notice hidden on `www.data.gov.in`, licence text unchanged; no resource-level licence. Fourth pass (2026-10-06): Copyright Policy asks for permission "by sending a mail", unresolved against the footer (B14) | `Hospital_Regis_Number`, stability [U]; otherwise `snapshot` | Not assessable to acceptance |
| C1b | Same as C1a [PUBD] | As C1a | All India [MIR, R1]; `State_Name` | `Address` | **Unresolved** (B15): file hosted only at `info.nhp.gov.in`, not on data.gov.in; host unreachable on 2026-10-06; only National Health Portal terms found (archived 2023, `www.nhp.gov.in`) reserve all rights [ARCH, R58] | None → `snapshot` | Not assessable to acceptance |
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
  2026-10-02. The second-pass re-check was inconclusive because the footer
  markup served on 2026-10-04 contains a sandbox notice. The third pass
  (2026-10-05) found that notice hidden on `www.data.gov.in`. The site's script
  shows it only on `sandbox.data.gov.in`. The GODL-India text is unchanged since
  2026-10-02 [PUBD, R44–R47]. No resource-level licence field exists [PUBD, R48].
  GODL-India exempts personal information from the licence (ADR-0002), so
  any personal information in these files is outside the licence in any case.
  - Fourth pass (2026-10-06): the Terms of Use say catalogs and information are
    available under the "license" metadata element of each record "except
    where otherwise noted". The metadata has no such element [PUBD, R48, R50,
    R55].
  - The Copyright Policy says material "may be reproduced free of charge after
    taking proper permission by sending a mail to us" [PUBD, R52]. Whether that
    covers published datasets, against the GODL-India footer, is unresolved
    (B14).
  - **C1b differs from C1a.** Its only file location is `info.nhp.gov.in`, not
    data.gov.in [PUBD, R55]. The footer licenses "the content published on
    data.gov.in", and no inspected page says whether that reaches a file hosted
    elsewhere. C1b's licence is therefore unresolved (B15).
- *Terms and retrieval.* Licence permission and technical access are separate;
  nothing below limits the licence.
  - The data.gov.in Terms of Use are silent on automated access [PUBD, R50].
    `robots.txt` disallows all paths for all user agents [PUBD, R49]. Downloads
    go through a form asking name, e-mail, usage type and purpose, with an image
    CAPTCHA [PUBD, R54]. `api.data.gov.in` refused connections [PUBD, R57].
  - ADR-0007 §5: where the terms are silent, retrieval is manual. On
    data.gov.in's terms as inspected, that rule points to manual retrieval for
    C1a, C2 and C3. The answer is recorded in the source ADR (E5), not here.
  - `HEAD` requests (no body) to the file URLs got `405`, or `200 text/csv` for
    C1a's legacy path. No `GET` was sent, so ADR-0004's record of a bot
    challenge on file URLs is neither confirmed nor contradicted [PUBD, R56].
  - C1b: `info.nhp.gov.in` did not accept connections on 2026-10-06, and no
    current terms could be read. The only National Health Portal terms found
    (archived 2023, `www.nhp.gov.in`, a sibling host) say nothing on automated
    access; they reserve all rights and describe the site as for individual
    and professional, non-commercial use [ARCH, R58].
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
- Licence, terms and retrieval are as for C1a (not C1b, whose file is hosted
  elsewhere).
- `Facility Address` is a single address string. In the inspected schemas, C2
  and C3 show no person or contact fields.
- Possible `context_columns`: `State Name`, `District Name`, `Subdistrict Name`,
  `Facility Type`, `Type Of Facility`. `Location Type`, `ActiveFlag_C` and
  `NOTIONAL_PHYSICAL` have unknown meanings and cannot be approved until they are
  known.
- `Nin_N` could support `native` IDs if it is stable, which is [U].
- The data is fixed at 7 October 2016, against a "Monthly" frequency (G6).

**C3 (CGHS empanelled hospitals).**
- Licence, terms and retrieval are as for C1a (not C1b, whose file is hosted
  elsewhere).
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
- **C1, C2 and C3** (rows C1a, C1b, C2, C3): the shared sandbox question (B2)
  is resolved by the third pass. Their licence evidence is the site-wide
  GODL-India statement on `www.data.gov.in`, the host `data.gov.in` redirects
  to, with an unchanged licence text. This is
  evidence, not acceptance. The fourth pass (2026-10-06) gathered data.gov.in's
  terms and retrieval conditions (B8, data.gov.in part). They each still need:
  - the data.gov.in Copyright Policy wording settled against the footer (B14)
  - for C1b, a licence basis for a file hosted only at `info.nhp.gov.in` (B15),
    and that host's terms [U]
  - header rows (B6)
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
  basis, C1 (row C1a; C1b's licence is unresolved, B15) and C2 could
  potentially provide multi-state coverage.
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
| B2 | **Resolved 2026-10-05.** The data.gov.in sandbox notice is hidden on `www.data.gov.in` and shown only on `sandbox.data.gov.in`; the GODL-India text is unchanged since ADR-0002 (inventory, third pass) | — | — |
| B3 | Licence text behind C4's label | C4 licence | Telangana portal documentation or the Telangana Open Data Unit |
| B4 | Whether permission or reuse on request can count as an acceptable licence basis (ADR-0001 §1, §4; ADR-0007 §5) | C5, C6 | Maintainer decision; it would be a new decision, not an assessment finding |
| B5 | G2. **C4:** components only, so whether a concatenation can be `raw_text` "exactly as published". **C1a:** a single string is published, but whether `Address_Original_First_Line` is complete enough is unknown | C4; usefulness of C1a | Maintainer decision (C4); scripted aggregate statistics (C1a) |
| B6 | No header rows and no scripted aggregate statistics | §5 assessment items (personal-data risk, context-column approval) | A script within the §5 evidence limit. Per-state counts for §4 step 3 come later, from accepted source files. |
| B7 | G4: publisher identity of C1–C3; whether NIHFW, CGHS and KVS count as "a government body" | `source_family`, publisher count, holdout unit | Publisher documentation; maintainer decision |
| B9 | No versioned procedure for gazetteer properties (G10) | Selection records (§4 step 3) | Code, after approval |
| B14 | data.gov.in Copyright Policy: "may be reproduced free of charge after taking proper permission by sending a mail to us" [PUBD, R52], against the footer's GODL-India statement and "All rights reserved except published datasets/resources and metadata" | Licence basis of C1a, C2, C3 (not withdrawn; unresolved) | data.gov.in (NIC) clarification; maintainer decision on how to read it |
| B15 | C1b's file is hosted only at `info.nhp.gov.in`; whether GODL-India reaches it, and that host's terms. Host unreachable on 2026-10-06; only archived National Health Portal terms (2023) found, reserving all rights | C1b licence | National Health Portal / NIHFW documentation, if the host returns; otherwise C1b stays unresolved |

The treatment of platform field lists as publisher documentation (see
"Procedural position") also needs the maintainer's confirmation.

### B. Recorded gaps and dependencies

| # | Item | Meaning |
|---|---|---|
| B8 | Whether automated retrieval is allowed: data.gov.in, `info.nhp.gov.in`, Telangana DKAN (E5) | Decides the retrieval method, not acceptance. Where terms are silent, retrieval is manual (ADR-0007 §5). **data.gov.in, evidence gathered 2026-10-06:** Terms of Use silent; `robots.txt` disallows all paths; download form with image CAPTCHA; API host refused connections. **`info.nhp.gov.in`:** unreachable, terms [U]. **Telangana DKAN:** not checked. |
| B10 | C3 has no state column | Dependency on O4 (retention of unknown-state records) |
| B11 | No `operator_published` source with a licence | A recorded absence. Reported, not worked around (ADR-0007 Consequences). |
| B12 | Sub-district semantics unverified for every state (§8) | Expected to be "unverified" at selection time (§4 step 3). Recorded in each selection record. |
| B13 | Address language/script undocumented for every source except C5 [SRCH] | Recorded as unknown, not guessed (§4 step 3). Bears on O6. |

## Recommended next evidence step

1. **B2: done (2026-10-05).** It affected C1, C2 and C3 (three of the six
   numbered sources, four of the seven inventory rows). C1 and C2 are also the
   only sources with a documented licence basis that could cover several
   states; C3 cannot, because it has no state attribution. The steps were:
   - determine the host: `data.gov.in` redirects to `www.data.gov.in`, which is
     not configured as the sandbox;
   - retrieve the GODL-India text from that host;
   - compare it with ADR-0002.

   The inventory's third pass records the evidence. It used licence text, terms
   and metadata only, within the §5 evidence limit.
2. **B3 and B8** are the same kind of documentation retrieval, for C4 and the
   three hosts.
   - B8 for data.gov.in: evidence gathered (fourth pass, 2026-10-06). It found
     B14 and B15.
   - B8 for `info.nhp.gov.in`: blocked; the host was unreachable.
   - B8 for Telangana DKAN, and B3 (C4's licence text): not yet done.
3. **Then B6**, after maintainer approval: a script that downloads a candidate
   file to `data/raw/` (never committed) and checks it against a recorded
   SHA-256.
   - It prints only the header row, the row count, per-column null rates and
     value-shape statistics (for example token-count distributions).
   - It prints no record text, and no person reads the file.
   - This is §5 assessment evidence. Per-state record counts for selection
     records are produced later (§4 step 3), from accepted source files.
4. **B1, B4, B5 (for C4), B7 and the reading of B14 are maintainer
   decisions,** as is the platform-field-list interpretation. No further
   evidence resolves them.
