# Focus-state and source evaluation (O1, O2)

- **Kind:** Research working notes. Not an ADR, not a source assessment under
  ADR-0007 §5, and not a selection record under ADR-0007 §4 step 3. Nothing here
  selects a state, accepts or rejects a source, designates a held-out publisher or
  writes a manifest.
- **Based on:** `docs/research/source-inventory.md` as committed in `a89f609`,
  updated with its third pass (2026-10-05, data.gov.in host and licence
  re-check), fourth pass (2026-10-06, terms of use and retrieval conditions
  for C1–C3), fifth pass (2026-10-06, B6 aggregate and schema inspection,
  offline), sixth pass (2026-10-06, C4 licence and Telangana portal terms),
  seventh pass (2026-10-06, B14 and B15 follow-up), eighth pass
  (2026-10-07, alternative address sources C7–C12) and ninth pass
  (2026-10-07, C9a and C9b assessment evidence), ADR-0001 to ADR-0007,
  and `docs/gazetteer.md`. No retrieval was done for these notes beyond what
  the inventory records. Evidence labels
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
The eighth pass added C7–C12; they have their own table under "Eighth-pass
alternatives (C7–C12)" below. C7 is out of scope for v0 by maintainer
decision (B18, 2026-10-07).

"All India" coverage for C1, C2 and C6 is first-pass evidence only ([MIR] for
C1 and C2, the [PUB] fetch summary for C6). The second pass did not verify any
coverage statement.

| Source | Publisher (as stated) | `source_family` | Declared coverage; state column | Single address string | Licence status | Identifier → likely `record_id_scope` | Status |
|---|---|---|---|---|---|---|---|
| C1a | MoHFW / DoHFW / NIHFW [PUBD] | `government_published` if NIHFW counts as a government body (G4) | All India [MIR, R1]; `State` | `Address_Original_First_Line`, completeness [U] | Basis: site-wide GODL-India, ADR-0002 (2026-10-02); third-pass re-check (2026-10-05): sandbox notice hidden on `www.data.gov.in`, licence text unchanged; no resource-level licence. Fourth pass (2026-10-06): Copyright Policy asks for permission "by sending a mail", unresolved against the footer (B14) | `Hospital_Regis_Number`, stability [U]; otherwise `snapshot` | Not assessable to acceptance |
| C1b | Same as C1a [PUBD] | As C1a | All India [MIR, R1]; `State_Name` | `Address` | **Unresolved** (B15): file hosted only at `info.nhp.gov.in`, not on data.gov.in; host unreachable on 2026-10-06; only National Health Portal terms found (archived 2023, `www.nhp.gov.in`) reserve all rights [ARCH, R58] | None → `snapshot` | Not assessable to acceptance |
| C2 | MoHFW / DoHFW [PUBD] | `government_published` (G4 open) | All India [MIR, R2]; `State Name` | `Facility Address` | As C1a | `Nin_N`, stability [U] | Not assessable to acceptance |
| C3 | MoHFW / DoHFW / CGHS [PUBD] | `government_published` (G4 open) | CGHS cities, not listed by state [U]; **no state column** | `DiagnosticCentreAddress` | As C1a | None → `snapshot` | Not assessable to acceptance |
| C4 | "Health and Medical and Family Welfare" on the Telangana Open Data portal [PUBD] | `government_published` (G4 open) | Telangana only; `State` | **None** (components only) | Publisher label only; licence text [U]. Sixth pass (2026-10-06): no licence text or link found on the portal; portal Copyright Policy asks for permission by mail and footer reserves all rights (B16) [PUBD, R61–R68] | None → `snapshot` | Not assessable to acceptance |
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
  - Seventh pass (2026-10-06): the Copyright Policy is unchanged. The gazette
    notification of GODL-India (MeitY, 10 February 2017) says in its preamble
    that the open licence for data sets published under NDSAP and through the
    OGD Platform had remained unspecified, and its §3 grants the licence for
    shareable non-sensitive data generated with public funds. It does not
    mention the Copyright Policy, so B14 stays open [PUBD, R70, R71].
    The National Health Portal hosts are still unreachable, and NIHFW's own
    website terms do not cover NHP data, so B15 stays open [PUBD, R74, R75].
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
  The diagnostics-centre resource spells its fields `DiagnosticCenter…`, so the
  two are not identically named (inventory, fifth pass) [PUBD, R34].

**C4 (Telangana health centres).**
- *Licence.* The publisher's dataset label "Government Open Data License - India"
  is verified [PUBD, R36]. The licence text it refers to is not. Under ADR-0007
  §5 the licence must be verified from the official text.
  - Sixth pass (2026-10-06): the label is still the same, and it is a free-text
    field with no link or text [PUBD, R61–R63]. No licence page and no Terms
    of Use were found among the portal's routes and 20 probed aliases [PUBD,
    R63, R64].
  - The portal's Copyright Policy says material "may be reproduced free of
    charge after taking proper permission by sending a mail to us" [PUBD, R65].
    Its footer reserves all rights, with no exception for datasets [PUBD, R63].
  - The Telangana State Open Data Policy 2016 commits to adopting an "Open Data
    Use License" but names none and gives no text [PUBD, R68].
  - So whether GODL-India governs C4 is not stated by any Telangana source. The
    label against the Copyright Policy and footer is unresolved (B16).
- *Terms and retrieval.* Licence permission and technical access are separate.
  - No Terms of Use page was found. The Policies page is silent on automated
    access, the API and rate limits [PUBD, R64, R65]. Under ADR-0007 §5 that
    points to manual retrieval; the source ADR records the answer (E5).
  - `robots.txt` disallows only `/search` [PUBD, R60]. That is a technical
    condition, not permission.
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
- The datastore types all 13 columns as `text`. The `state` column's
  description begins with a byte-order mark, which suggests the uploaded CSV
  has one (inference; file not seen) [PUBD, R37].

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

### Eighth-pass alternatives (C7–C12)

Found in the inventory's eighth pass (2026-10-07), from metadata, field lists,
policy pages and scripts only. **None is accepted, rejected or selected.** Rows
C8i and C9c are left out: C8i has no address field, and C9c's file (299 B) is
unlikely to be a station list (inference from size).

| Source | Publisher (as stated) | `source_family` | Declared coverage; state column | Single address string | Licence status | Identifier → likely `record_id_scope` | Status |
|---|---|---|---|---|---|---|---|
| C7 Company Master Data | Ministry of Corporate Affairs [PUBD, R76] | `government_published` (G4 open) | All India [PUBD, R76]; `CompanyStateCode`, scheme [U] | `Registered_Office_Address`, completeness [U] | Site-wide GODL-India statement, as C1–C3; B14 | `CIN`, stability [U] | **Out of scope for v0** (maintainer scope decision B18, 2026-10-07; not a licence rejection). Licence and evidence columns kept as historical context |
| C8a–C8h Karnataka department catalogs | Eight catalogs from seven agencies in six Karnataka departments [PUBD, R79, R80] | `government_published` (G4 open, including the publisher unit) | Karnataka (C8b labelled "All India") [PUBD, R79]; state column [U] | [U]: no field lists | State-instance footer (GODL-India); B14 on `www.data.gov.in`; B17 | [U] → `snapshot` unless a column is found | Not assessable to acceptance; small files |
| C9a CMA ULB offices (TN) | Commissionerate of Municipal Administration [PUBD, R79, R80] | `government_published` (G4 open) | Tamil Nadu [PUBD, R79]; no state column [PUBD, R81] | `address` [PUBD, R81], completeness [U] | As C8 | None → `snapshot` | Not assessable to acceptance; ninth pass below |
| C9b TNOU centres (TN) | Tamil Nadu Open University [PUBD, R79, R80] | Open (G4) | Tamil Nadu [PUBD, R79]; `name_of_the_district` in one list [PUBD, R81] | `address` in one of ten lists [PUBD, R81]; ninth pass: nine of ten [PUBD, R80, R81] | As C8 | [U]; ninth pass: centre code in seven lists [PUBD, R80] | Not assessable to acceptance; ninth pass below |
| C10 Blood Bank Directory | NIHFW [PUBD, R79, R80] | As C1 | All India [PUBD, R79]; `_state`, `_district`, `pincode` [PUBD, R81] | `_address` | As C1b: file at `info.nhp.gov.in`; B14, B15 | [U] | Not assessable to acceptance; no better than C1 |
| C11 AISHE directory | Ministry of Education (mirror label) [MIR, R88] | `government_published` (G4 open) | National [U]; `state`, `district`, `pincode` in the detail view [PUBD, R89] | `address1` [PUBD, R89] | No licence text found; mirror label only | AISHE code [PUBD, R89] | No licence found; interactive search only |
| C12 CBSE SARAS directory | CBSE [PUBD, R91] | Open (G4; whether CBSE operates any listed school is [U]) | State filter [PUBD, R91] | "Address Details" column [PUBD, R91] | None found on the page; policies not checked [U] | Affiliation number / school code [PUBD, R91] | No licence found; interactive search only |

How they compare with C4, C5 and C6, on the evidence only:
- **Licence evidence.** C7, C8, C9 and C10 sit under a site-wide licence
  statement, and the GODL-India text it names was read directly (R82,
  identical to R47). C4 has a
  label with no text (B3, B16); C5 and C6 offer reuse only on request (B4).
  That is a difference in the evidence, not a resolved licence: C7 and C10
  carry B14, and C8 and C9 carry B17.
- **Address strings.** C7, C9a, C9b (one list) and C10 publish a single address
  field, which C4 does not (G2). Ninth pass: C9b lists an `Address` column in
  nine of ten resources [PUBD, R80, R81].
- **Publishers.** C8 and C9 add state-department publishers in Karnataka and
  Tamil Nadu, distinct from C5's election authorities. Whether each department
  is a separate `publisher` (ADR-0007 §6) is G4.
- **Weaknesses.** C8 and C9 files are small, and most have no field list. Some
  of C7's registered offices may be residences [U] (B18). C11 and C12 are no
  stronger than C6: interactive searches with no licence found.
- These are differences in the evidence gathered so far. They rank no
  source and prefer none.
- **C7 after B18.** The points above about C7 are historical assessment
  context. C7 is no longer a v0 candidate (B18).

### C9a and C9b (ninth pass, 2026-10-07)

Detail in the inventory, "C9a and C9b assessment evidence". **Neither is
accepted, rejected or selected**, and Tamil Nadu is not selected.

| Item | C9a (CMA offices) | C9b (TNOU centres) |
|---|---|---|
| Publisher (G4) | CMA, under the Municipal Administration and Water Supply Department, Tamil Nadu [PUBD, R93]; unit open | TNOU, under the Higher Education Department, Tamil Nadu [PUBD, R94]; legal status [U]; unit open |
| Licence statement | Site footer only; no `license` metadata element [PUBD, R80, R83, R93, R95]. The catalog page says "Released Under: NDSAP", a policy, not a licence [PUBD, R95] | Site footer only; no `license` metadata element [PUBD, R80, R83, R94]. No C9b page obtained, so any "Released Under" statement is [U] |
| Licence status | **Unresolved:** B17, with B14 | **Unresolved:** B17, with B14 |
| Publisher website | "All rights reserved" footer; about the website, not the dataset [PUBD, R97] | Same [PUBD, R96] |
| Retrieval (technical) | Terms silent; `robots.txt` disallows all [PUBD, R83]; download-modal CAPTCHA styles on the resource page (inference) [PUBD, R95]; manual (B19) | Terms and `robots.txt` as C9a (instance-wide) [PUBD, R83]; download form not checked (no C9b page obtained) [U]; `is_api_available` "0" [PUBD, R80]; manual (B19) |
| Columns | Platform field list: `Address`, office and ULB names, contact columns, `No.of Wards` [PUBD, R81] | Nine address-bearing resources: eight with declared `meta_field` lists [PUBD, R80], one (B.Ed Study Centres) from the platform field list [PUBD, R81]; one aggregate resource [PUBD, R81] |
| Header row | Not obtained | Not obtained |
| State and district | No state or district column [PUBD, R81] | No state column; `Name of the District` in six lists [PUBD, R80, R81] |
| Declared coverage → LGD | "Tamil Nadu" [PUBD, R93] → `lgd:state:33` by exact `name_key` [CALC, R98]; declared label only, records unverified [U] | Same [PUBD, R94; CALC, R98] |
| Identifier → `record_id_scope` | None → `snapshot` [PUBD, R81] | Centre code in seven lists [PUBD, R80] (stability [U]) → possibly `native`; B.Ed lists `snapshot` |
| Privacy | Contact columns (not ingestible) [PUBD, R81]; address content [U] | `Contact Person` column; contact columns [PUBD, R80]; address content [U]; B20 (Partner Institutions `Name of the Company`) |
| Currency | Last changed 2017-12-29 [PUBD, R80] | 2020–2021 period; last changed 2021-08-13 [PUBD, R80] |

**Readiness.** Neither can go to a formal §5 assessment yet with a result other
than "licence unclear", which §5 treats as rejection. The order of what is
missing:
1. B17 (and B14): a licence basis for state-department data on the platform.
2. Header rows and scripted aggregate statistics (B6), from a manual download
   through the form (B19), after maintainer approval.
3. G4 (publisher unit) and, for C9b, B20.

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
  - header rows and file-level aggregate statistics (B6; schema-level part
    gathered in the fifth pass, file-level part not)
  - their personal-data questions settled
- **C4** depends on its licence text (B3), the conflict with the portal's
  Copyright Policy and footer (B16), and G2 (B5). Its retrieval terms were
  gathered in the sixth pass (B8, Telangana part).
- **C5 and C6:** no reuse licence was found, and the outcome depends on B4.
- **C7–C12 (eighth pass):** none is ready either, and C7 is no longer a v0
  candidate.
  - C7: out of scope for v0 (B18, maintainer scope decision, 2026-10-07).
    Its B14 status and missing evidence are not pursued for v0.
  - C8 and C9 need B14 and B17, and header rows for every file-only resource
    (B6, G12). Ninth pass: C9a and C9b evidence gathered as far as metadata
    allows; still B17, B6, G4 and (C9b) B20.
  - C10 needs B14 and B15, as C1b does.
  - C11 and C12 have no licence text.
- No `operator_published` source with a licence has been found, so that family
  is empty (ADR-0007 Consequences anticipates this).

### B6 aggregate inspection (fifth pass, 2026-10-06)

Structural evidence only. It changes no licence status and no outcome above. The
detail is in the inventory, "B6 aggregate and schema inspection".

- **Gathered, offline from saved responses** [PUBD, CALC]:
  - platform field counts and types for C1a (48 fields), C1b (16), C2 (13) and
    C3 (3);
  - C4's 13 all-`text` datastore columns and its platform count of 7,001;
  - the publisher's missing-value notes for C1–C3 ("NA/Blank: Not Available"
    for C1a and C1b; "NA: Not Available" for C2 and C3);
  - file sizes and hosting for C1–C3;
  - a correction to the inventory's C3 field-name comparison.
- **Not gathered:** file header rows; row counts for C1a, C1b, C2, C3, C5 and
  C6; any empty-value rate; value distributions; per-state counts; language or
  script.
- **Why:** no candidate file is held locally, and no permitted scripted route
  to one is established.
  - data.gov.in: retrieval points to manual (B8), and B14 is open.
  - C1b: the host was unreachable (B15).
  - C4: the portal's terms (B3, B8) were unchecked at the time. (Sixth pass:
    B8 evidence gathered; B3 open, with B16.)
  - C5, C6: depend on B4.
- **Not an ADR-0007 dimension.** How easy a source is to inspect is not one of
  the §4 selection dimensions and is not used to rank states.

## O1: pre-candidate state evidence

**No state is a candidate** (ADR-0007 §4 step 2). Columns follow the §4 diversity
dimensions.

| State | Sources with state-specific evidence (status) | Source families documented | Publishers documented for the state | Sub-district verification (§8) | Language/script per documentation | Gazetteer properties [CALC, ad hoc] |
|---|---|---|---|---|---|---|
| Telangana (`lgd:state:36`) | C4 (licence unresolved, B3 and B16; G2) | `government_published` only (G4 open) | 1 state department. C1, C2 and C6 declare all-India coverage (first pass: [MIR] C1, C2; [PUB] C6) | Unverified | [U] | 33 districts, 621 sub-districts, 3 sub-districts without villages, 41 same-name, 0 variant-name, median 16 villages/PIN, 0 of its PINs also map villages in another state |
| Tamil Nadu (`lgd:state:33`) | C5 (no reuse licence found; B4). Eighth pass: C9a, C9b (site-wide licence statement; B14, B17; schemas partly [U]) | Open (C5 family not classified); C9 `government_published` (G4 open) | CEO TN, or one or more district administrations (unresolved); eighth pass: CMA and TNOU. C1, C2 and C6 declare all-India coverage (first pass: [MIR] C1, C2; [PUB] C6) | Unverified | Tamil and English [SRCH, R20]; whether native-script lists are admissible is O6 | 38 districts, 317 sub-districts, 0 / 0 without villages, 88 same-name, 2 variant-name, median 7 villages/PIN, 17 of its PINs also map villages in another state |
| Karnataka (`lgd:state:29`) | C5, one district page only (no reuse licence found; B4). Eighth pass: C8a–C8h (site-wide licence statement; B14, B17; no field lists) | Open; C8 `government_published` (G4 open) | One district administration; eighth pass: seven agencies in six state departments (whether each is a `publisher` is G4). C1, C2 and C6 declare all-India coverage (first pass: [MIR] C1, C2; [PUB] C6) | Unverified | [U] | 31 districts, 240 sub-districts, 0 / 0 without villages, 646 same-name, 16 variant-name, median 17 villages/PIN, 0 of its PINs also map villages in another state |
| The other 33 states/UTs | No state-specific source. C1, C2 and C6 declare all-India coverage (first pass: [MIR] C1, C2; [PUB] C6) | `government_published` (G4 open) | MoHFW (one or several publishers, G4); KVS | Unverified | [U] | In the inventory's table |

C3 is not in the table: it has no state column, its declared coverage (CGHS
cities) is not listed by state, and its records cannot currently be attributed to
any state (O4).

Eighth pass: C7 declares "All India" [PUBD, R76] but is out of v0 scope
(B18); C10, C11 and C12 are national. Like C1, C2 and C6, they add no state-specific evidence: how their
state columns map to `lgd:state:` IDs is [U]. Nothing in the eighth pass
changes the Telangana row.

Observations, none of them a selection criterion:
- **Region.** ADR-0007 sets the evidence for region as the LGD state unit and
  defines no regional grouping.
  - The three states with state-specific evidence are all in southern India. That
    is general geographic context, not repository evidence and not an ADR
    dimension.
  - Ease of access is not one of the ADR-0007 §4 selection dimensions. Having
    state-specific evidence is not by itself a reason to prefer these states.
  - The eighth pass also found address catalogs by title for Maharashtra,
    Mizoram and Meghalaya, not assessed. The southern concentration reflects
    what was searched and assessed, not where sources exist.
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
  - Eighth pass: C8 and C9 could each meet the source condition only for
    their own state, subject to B14 and B17. C7 is out of v0 scope (B18)
    and is not counted here.
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
  - For Karnataka and Tamil Nadu, the eighth pass documents several state
    departments or agencies. Whether they count as separate publishers is G4.
  - Whether a state keeps a non-held-out publisher (§6) cannot be judged until
    sources are accepted and O5 is decided.

## Blockers, gaps and dependencies

### A. Blockers

| # | Blocker | Blocks | Owner / route |
|---|---|---|---|
| B1 | ADR-0006 and ADR-0007 are Proposed | Formal assessments, source ADR, selection records | Maintainer decision |
| B2 | **Resolved 2026-10-05.** The data.gov.in sandbox notice is hidden on `www.data.gov.in` and shown only on `sandbox.data.gov.in`; the GODL-India text is unchanged since ADR-0002 (inventory, third pass) | — | — |
| B3 | Licence text behind C4's label. **Sixth pass (2026-10-06):** none found on the portal; the 2016 state policy names no licence (inventory, sixth pass) | C4 licence | The Telangana Open Data Unit (opendata[at]telangana[dot]gov[dot]in, R66) |
| B4 | Whether permission or reuse on request can count as an acceptable licence basis (ADR-0001 §1, §4; ADR-0007 §5) | C5, C6 | Maintainer decision; it would be a new decision, not an assessment finding |
| B5 | G2. **C4:** components only, so whether a concatenation can be `raw_text` "exactly as published". **C1a:** a single string is published, but whether `Address_Original_First_Line` is complete enough is unknown | C4; usefulness of C1a | Maintainer decision (C4); scripted aggregate statistics (C1a) |
| B6 | No header rows and no scripted aggregate statistics from files. **Fifth pass (2026-10-06):** schema-level part gathered offline (platform field types and counts, C4 platform count, missing-value notes); file-level part not done, as no candidate file is held and no permitted scripted route is established | §5 assessment items (personal-data risk, context-column approval) | A script within the §5 evidence limit, run on a file obtained through a permitted route. Per-state counts for §4 step 3 come later, from accepted source files. |
| B7 | G4: publisher identity of C1–C3; whether NIHFW, CGHS and KVS count as "a government body" | `source_family`, publisher count, holdout unit | Publisher documentation; maintainer decision |
| B9 | No versioned procedure for gazetteer properties (G10) | Selection records (§4 step 3) | Code, after approval |
| B14 | data.gov.in Copyright Policy: "may be reproduced free of charge after taking proper permission by sending a mail to us" [PUBD, R52], against the footer's GODL-India statement and "All rights reserved except published datasets/resources and metadata" | Licence basis of C1a, C2, C3 (not withdrawn; unresolved). **Seventh pass (2026-10-06):** policy unchanged (R70); the gazette notification's preamble says the open licence for data sets published under NDSAP and through the OGD Platform had remained unspecified, and its §3 grants GODL-India for shareable non-sensitive data generated with public funds; it does not mention the Copyright Policy (R71); no official text relating the two was found | data.gov.in (NIC) clarification; maintainer decision on how to read it |
| B15 | C1b's file is hosted only at `info.nhp.gov.in`; whether GODL-India reaches it, and that host's terms. Host unreachable on 2026-10-06; only archived National Health Portal terms (2023) found, reserving all rights. **Seventh pass (2026-10-06):** hosts still unreachable (R74); NIHFW's own website terms do not cover NHP data (R75) | C1b licence | National Health Portal / NIHFW documentation, if the host returns; otherwise C1b stays unresolved |
| B16 | C4's label "Government Open Data License - India" against the Telangana portal's Copyright Policy ("may be reproduced free of charge after taking proper permission by sending a mail to us") and its footer ("All rights reserved", no exception for datasets) [PUBD, R61, R63, R65] | C4 licence (unresolved; the label is not withdrawn) | The Open Data Unit or the publisher to clarify; maintainer decision on how to read it |
| B17 | State-department data on the data.gov.in state instances. The footer says content "owned by the respective Ministry/State/Department/Organization" is licensed under GODL-India; the GODL-India grant refers to data "generated using public funds by various agencies of the Government of India" and does not mention states. The state instances' Copyright Policy has no permission requirement, while `www.data.gov.in`, through which the same files are reached, carries the B14 text [PUBD, R79–R85] | Licence basis of C8 and C9 (unresolved) | data.gov.in (NIC) or the publishing departments to clarify; maintainer decision on how to read it |
| B18 | **Decided 2026-10-07 (maintainer scope decision): Option B. C7 (MCA Company Master Data) is out of scope for v0 and is no longer a v0 candidate.** Under the existing wording of ADR-0001 §1 and ADR-0006 §12 rule 2, a company registered office is not clearly the address of an institution, facility or public place; including it would require expanding or reinterpreting the source category. This is a scope decision, not a licence rejection: C7's licence status (B14) and evidence status are unchanged and kept as historical assessment context. It does not claim that company addresses are invalid or unsafe. Option C, a separate organization/company-address track, remains possible later and would need a new ADR with its own reporting and privacy rules. | — (C7 out of v0 scope) | — |
| B20 | Whether TNOU partner-company premises (C9b, "Partner Institutions", declared column `Name of the Company`) are the address of an institution, facility or public place (ADR-0006 §12 rule 2). Related to, but not decided by, B18 [PUBD, R80] | That C9b resource | Maintainer decision |

The treatment of platform field lists as publisher documentation (see
"Procedural position") also needs the maintainer's confirmation.

### B. Recorded gaps and dependencies

| # | Item | Meaning |
|---|---|---|
| B8 | Whether automated retrieval is allowed: data.gov.in, `info.nhp.gov.in`, Telangana DKAN (E5) | Decides the retrieval method, not acceptance. Where terms are silent, retrieval is manual (ADR-0007 §5). **data.gov.in, evidence gathered 2026-10-06:** Terms of Use silent; `robots.txt` disallows all paths; download form with image CAPTCHA; API host refused connections. **`info.nhp.gov.in`:** unreachable, terms [U]. **Telangana portal, evidence gathered 2026-10-06:** no Terms of Use page found; Policies page silent on automated access; `robots.txt` disallows only `/search`; API documentation endpoint did not respond. |
| B10 | C3 has no state column | Dependency on O4 (retention of unknown-state records) |
| B11 | No `operator_published` source with a licence | A recorded absence. Reported, not worked around (ADR-0007 Consequences). |
| B12 | Sub-district semantics unverified for every state (§8) | Expected to be "unverified" at selection time (§4 step 3). Recorded in each selection record. |
| B13 | Address language/script undocumented for every source except C5 [SRCH] | Recorded as unknown, not guessed (§4 step 3). Bears on O6. Eighth pass: also undocumented for C7–C12. |
| B19 | State instances (C8, C9): retrieval conditions | Same as data.gov.in (B8): Terms of Use silent; `robots.txt` disallows all paths; files on the `www.data.gov.in` file store [PUBD, R80, R83, R84]; whether the state instances use the same download form was not checked [U]. Silent terms point to manual retrieval. **Ninth pass:** the C9a resource page on `tn.data.gov.in` carries `#download-modal` CAPTCHA styles, which points to the same form (inference; component not traced) [PUBD, R95]. |

### C. Pending external clarification requests

These are **requests, not evidence and not licence decisions.** Nothing is
recorded as sent until the maintainer sends it, and nothing is recorded as
answered until a reply is received and cited. No permission is assumed in the
meantime.

**C4 (B3, B16): draft to the Telangana Open Data Unit. Not sent.**

- To: Open Data Unit, Department of ITE&C, Government of Telangana,
  opendata[at]telangana[dot]gov[dot]in (the contact on the portal, R66)
- Drafted: 2026-10-06
- Status: draft, not sent
- The project description in the draft ("non-commercial", "academic") is the
  maintainer's to confirm before sending; the ADRs do not record it.

> **Subject:** Licence and reuse terms for "Details of Health centres latitude
> and longitude in Telangana" (data.telangana.gov.in)
>
> Dear Open Data Unit,
>
> I maintain Pata, a non-commercial, open-source academic research project on
> the parsing and resolution of Indian addresses. Before using any dataset, I
> check its licence and terms of use, and I would be grateful for your
> clarification about the following dataset on the Telangana Open Data portal:
>
> - Title: Details of Health centres latitude and longitude in Telangana
> - Dataset identifier: 44935575-631b-4116-b278-41f4c507b95b
> - Publisher shown: Health and Medical and Family Welfare
>
> The dataset's metadata lists its licence as "Government Open Data License -
> India". The portal's Policies page also contains a Copyright Policy stating
> that material "may be reproduced free of charge after taking proper
> permission by sending a mail to us".
>
> Could you please confirm:
>
> 1. Whether this dataset is licensed under the Government Open Data License -
>    India (GODL-India).
> 2. If it is, the official licence text or reference that applies (for
>    example, a link to the licence text).
> 3. Whether the Copyright Policy's requirement to obtain permission by email
>    applies to published open datasets such as this one.
> 4. Whether downloading, reusing and redistributing this dataset is permitted
>    for non-commercial academic research, including as part of an open-source
>    research benchmark, and if so under what conditions (for example, the
>    required attribution).
>
> Thank you for your time.
>
> Regards,
> [Name]
> [Project link and contact details]

Until a reply is received and recorded, B3 and B16 stay open and C4 stays
unresolved, unaccepted and unselected.

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
   - B8 for the Telangana portal: evidence gathered (sixth pass, 2026-10-06).
   - B3 (C4's licence text): searched in the sixth pass; no licence text was
     found and a conflict was recorded (B16). Still open. A clarification
     request to the Telangana Open Data Unit is drafted, not sent (section C
     above).
   - B14 and B15: followed up in the seventh pass (2026-10-06). Both stay
     open; B14 needs data.gov.in (NIC) to clarify, B15 needs a reachable
     National Health Portal host or NIHFW documentation.
3. **Then B6, file-level part**, after maintainer approval. Its schema-level
   part was gathered in the fifth pass (above). A candidate file is placed in
   `data/raw/` (never committed) through a permitted route, and a script checks
   it against a recorded SHA-256. For data.gov.in that route is a manual
   download, as B8 points to manual retrieval.
   - It prints only the header row, the row count, per-column null rates and
     value-shape statistics (for example token-count distributions).
   - It prints no record text, and no person reads the file.
   - This is §5 assessment evidence. Per-state record counts for selection
     records are produced later (§4 step 3), from accepted source files.
4. **B1, B4, B5 (for C4), B7 and the readings of B14 and B16 are maintainer
   decisions,** as is the platform-field-list interpretation. No further
   evidence resolves them. The eighth pass adds the reading of B17. B18 was
   decided by the maintainer on 2026-10-07 (Option B).
5. **Alternatives (eighth pass, 2026-10-07).** If the maintainer wants to
   pursue them, the evidence still missing per candidate is (listed in no
   order of preference):
   - C7: none for v0; it is out of scope (B18). A future organization/
     company-address track (Option C) would need a new ADR first.
   - C9a and C9b, then C8: header rows for the file-only resources (B6, G12),
     which needs a permitted manual route (B19). Ninth pass: C9a and C9b
     metadata evidence is gathered (see "C9a and C9b (ninth pass)"); B17 is
     the first blocker, then B6, G4 and B20.
   - C8, C9 and C10 inherit B14; C8 and C9 also need B17.
   - C11 and C12: publisher terms (`aishe.gov.in`, CBSE website policies)
     before anything else.

   Search results were used for discovery only, and no new clarification
   request is drafted.
