# Address-source and focus-state inventory

- **Kind:** Research working notes; not a decision record and not yet sufficient
  for source acceptance. Input to ADR-0007 O1 (focus states) and O2 (address
  sources). Nothing here selects a state, accepts a source or writes a manifest.
- **Gathered:** 2026-10-04. First pass: web search, page fetches and one local
  computation on the pinned gazetteer (`gazetteer_version`
  `bf4a8b5d35130e7c3b94c6e4de812b3fd6deeb059497af22aac178642c2c2c78`). Second
  pass: publisher pages and publisher-platform metadata APIs retrieved with
  `curl` and inspected directly (see "Licence and header verification"). Third
  pass, 2026-10-05: data.gov.in host and licence re-check for C1–C3 only. Fourth
  pass, 2026-10-06: terms of use and retrieval conditions for C1–C3, including
  C1b's file host `info.nhp.gov.in`. Fifth pass, 2026-10-06: B6 aggregate and
  schema inspection for C1–C6, offline, from responses already saved. Sixth
  pass, 2026-10-06: C4 licence and Telangana portal retrieval terms (B3, B8).
  Seventh pass, 2026-10-06: B14 and B15 follow-up for C1–C3. Eighth pass,
  2026-10-07: alternative address sources (C7–C12), metadata only.
- **Not exhaustive.** Only the sources and categories listed below were looked
  at. Categories identified but not researched are listed separately.
- **Eight passes.** The sections up to "Candidate-state evidence" record the
  first pass. "Licence and header verification" records a second pass on C1–C6.
  "data.gov.in host and licence re-check" records a third pass on the C1–C3
  licence only. "Terms of use and retrieval conditions" records a fourth pass on
  C1–C3 only. "B6 aggregate and schema inspection" records a fifth pass on
  C1–C6. "C4 licence and retrieval terms" records a sixth pass on C4 only.
  "B14 and B15 follow-up" records a seventh pass on C1–C3 only. "Alternative
  address sources" records an eighth pass on new candidates C7–C12. Where they
  differ, the later pass is the current evidence; the
  earlier text is kept as the record of what was known then.

## How the evidence was gathered

- **First pass: two tools were used.** A web search tool returned a list of
  result links plus a model-generated summary of those results. A page-fetch tool
  retrieved a single page and returned a model-generated summary of it. No page
  text was saved, and no page was read directly by a person. Every first-pass
  external claim therefore rests on one of these summaries, and none is a directly
  inspected quotation.
- **Second pass:** publisher pages and publisher-platform metadata APIs were
  retrieved with `curl` and the responses inspected directly. Those claims carry
  the label [PUBD]; the method is described under "Licence and header
  verification".
- **Third pass:** the same method, on data.gov.in pages, site scripts and
  metadata only; described under "data.gov.in host and licence re-check".
- **Fourth pass:** the same method, on data.gov.in terms, policy pages,
  `robots.txt`, site scripts, metadata and response headers, plus one Internet
  Archive copy of a National Health Portal page [ARCH]; described under "Terms
  of use and retrieval conditions".
- **Fifth pass:** no new retrieval. Responses saved by the second and fourth
  passes were re-read offline; described under "B6 aggregate and schema
  inspection".
- **Sixth pass:** Telangana portal pages, metadata, scripts and policy, and the
  ITE&C Department's open-data policy, retrieved with `curl` and read directly
  [PUBD]; described under "C4 licence and retrieval terms".
- **Seventh pass:** data.gov.in Policies page, the GODL-India gazette
  notification, NDSAP guidelines, National Health Portal host checks and
  NIHFW's website terms, retrieved with `curl` and read directly [PUBD];
  described under "B14 and B15 follow-up".
- **Eighth pass:** web search and data.gov.in catalog searches for discovery
  only; then data.gov.in and state-instance metadata APIs, policy pages and
  site scripts, and the AISHE, UDISE+, CBSE and AIKosh sites, retrieved with
  `curl` and read directly [PUBD]; described under "Alternative address
  sources".
- Other claims rest on this repository's ADRs [ADR] or on the local gazetteer
  computation [CALC].
- **Page fetches** were made with an instruction to report only metadata,
  licence and terms, and column names, and not to reproduce records. **Web
  searches** carried no such instruction, so their summaries could describe the
  content of pages they found.
- **No dataset was downloaded** and no individual address record was
  intentionally inspected for benchmark admission. One exception in kind, not in
  intent: the structure of the Tamil Nadu polling-station lists (C5) comes from a
  search summary that was very likely generated from the PDF lists themselves, or
  from pages describing them. No PDF was opened.
- **data.gov.in** returned HTTP 403 to the three page fetches attempted,
  consistent with the bot challenge recorded in ADR-0004. Its metadata comes from
  search summaries and from AIKosh, an official government mirror.

## Evidence labels

| Label | Meaning |
|---|---|
| [PUB] | Official publisher page, fetched; content known from the fetch summary |
| [MIR] | Official government mirror or metadata page (AIKosh, IndiaAI/MeitY), fetched; content known from the fetch summary |
| [SRCH] | Search-result summary only; the underlying page was not fetched |
| [3P] | Third-party (commercial or non-official) source |
| [COMM] | Volunteer or community source |
| [ADR] | Already recorded in this repository's ADRs |
| [CALC] | Calculated here |
| [U] | Unknown or not yet verified |

[PUBD] (publisher page or platform API, retrieved directly and inspected) is
defined under "Licence and header verification". [ARCH] (Internet Archive copy
of a publisher page, retrieved directly and inspected; evidence of the page on
the capture date only) is defined under "Terms of use and retrieval
conditions".

Labels can combine, for example [SRCH, 3P].

## Cited sources

All retrieved or searched on **2026-10-04**. "Fetched" means the page-fetch tool
returned content; "search result" means the URL appeared in search results and
was not fetched.

| # | URL | Kind | How used | Supports |
|---|---|---|---|---|
| R1 | https://aikosh.indiaai.gov.in/home/datasets/details/national_hospital_directory_with_geo_code_and_additional_parameters_updated_till_last_month.html | [MIR] | fetched | C1 publisher, format, upload date, frequency, licence label |
| R2 | https://aikosh.indiaai.gov.in/home/datasets/details/all_india_health_centres_directory_till_october_2016.html | [MIR] | fetched | C2 publisher, snapshot date, fields, format, frequency, licence label |
| R3 | https://aikosh.indiaai.gov.in/home/datasets/details/list_of_hospitals_empaneled_under_cghs_all_over_india.html | [MIR] | fetched | C3 publisher, fields, dates, frequency, licence label |
| R4 | https://aikosh.indiaai.gov.in/home/datasets/details/telangana_health_centres_geolocation_and_facility_details.html | [MIR] | fetched | C4 publisher, fields, date, frequency, licence label |
| R5 | https://aikosh.indiaai.gov.in/home/datasets/details/all_colleges_as_per_aishe_dashboard_3.html | [MIR] | fetched | AISHE publisher, column names, licence label |
| R6 | https://wiki.openstreetmap.org/wiki/India_Health_Facilities_Import | [COMM] | fetched | C1: OSM import's attributes, exclusions and quality notes |
| R7 | https://rbi.org.in/Scripts/Disclaimer.aspx | [PUB] | fetched | RBI copyright, caching and licence statements |
| R8 | https://www.rbi.org.in/Scripts/IFSCMICRDetails.aspx | [PUB] | fetched | RBI IFSC/MICR is an interactive search |
| R9 | https://github.com/razorpay/ifsc | [3P] | fetched | IFSC compilation sources and its data-licence claim |
| R10 | https://kvsangathan.nic.in/ | [PUB] | fetched | C6 school count, search features, ownership statement |
| R11 | https://data.telangana.gov.in/ | [PUB] | fetched; only the title was returned | C4 portal exists; terms not obtained |
| R12 | https://nhpr.abdm.gov.in/ (redirect from https://facility.abdm.gov.in) | [PUB] | fetched; only the title was returned | ABDM terms not obtained |
| R13 | https://data.gov.in/catalog/hospital-directory-national-health-portal | [PUB] | fetch returned 403 | C1 catalog location only |
| R14 | https://data.gov.in/resource/nin-health-faclities-geo-code-and-additional-parameters-updated-till-last-month | [PUB] | fetch returned 403 | C1 resource location only |
| R15 | https://data.gov.in/catalog/all-india-health-centres-directory | [PUB] | fetch returned 403 | C2 catalog location only |
| R16 | https://ckandev.indiadataportal.com/dataset/udise/resource/457fddf1-982f-4c85-855d-5095578accc1 | [3P] | fetch returned 403 | UDISE+ third-party copy exists |
| R17 | https://community.data.gov.in/?p=113814 | [SRCH] | search result | UDISE+ on data.gov.in is aggregates up to 2019-20 |
| R18 | https://api.udiseplus.gov.in | [SRCH] | search result | An official UDISE+ API exists |
| R19 | https://data.opencity.in/dataset/delhi-udise-2024-25 | [SRCH, 3P] | search result | UDISE+ third-party copy exists |
| R20 | https://dindigul.nic.in/?p=39324 | [SRCH] | search result | C5: Tamil Nadu district page offering polling-station lists in Tamil and English |
| R21 | https://www.elections.tn.gov.in/PSLIST_09112022/dt4/English/AC040.pdf, https://www.elections.tn.gov.in/PSLIST_27102023/dt28/English/AC217.pdf, https://www.elections.tn.gov.in/PSLIST_27102023/dt8/English/AC071.pdf | [SRCH] | search results; **not opened** | C5: per-constituency PDF lists on the CEO Tamil Nadu site, English editions, dated directories |
| R22 | https://chikkaballapur.nic.in/en/election/eln_citizensinfo_en/ | [SRCH] | search result | C5 Karnataka: one district page with notices of polling-station list publication |
| R23 | https://bajajfinserv.in/insurance/ayushman-bharat-hospital-list | [SRCH, 3P] | search result | PMJAY: dashboard PDF download (third-party description) |
| R24 | https://abdm.gov.in/strapicms/uploads/HFR_SOP_for_verifiers_2697480f8a_2_fc7c967615_4_51f1289d5c.pdf | [SRCH] | search result | ABDM HFR: registration collects facility contact-person details |
| R25 | https://www.data.gov.in/resource/statepsu-oil-marketing-companies-omcs-wise-details-petrol-pumps-set-country-2016-17-2019 | [SRCH] | search result | Oil outlets: counts, not addresses |

Claims for which no specific page could be established are marked [U] in place.

**Attribution of [SRCH] claims.** Search summaries did not say which result URL
supported which statement. Where a [SRCH] claim cites an R#, linking it to that
URL is an inference from the results returned, not an attribution made by the
search tool.

These search-derived claims rest on the summary of a whole query and cite no
R#:
- the C1 content description (C1 item 4)
- the C5 Tamil Nadu list structure (C5 items 4, 6 and 8, and "polling areas" in
  item 11)
- the bank/ATM locator finding, which records only that one search returned no
  download or reuse terms

## Excluded by ADR-0007 S1

LGD gazetteer files and the India Post PIN directory, and anything derived from
them, are not address-corpus sources and were not inventoried.

## Candidate address sources

Field numbers follow the requested checklist: (1) publisher, (2) URL,
(3) family, (4) contents, (5) coverage, (6) address fields, (7) language/script,
(8) stable ID, (9) dates, (10) licence/terms, (11) privacy/scope fit,
(12) limitations, (13) held-out-publisher potential.

C1–C6 are the first-pass candidates. C7–C12 were found in the eighth pass and
are recorded under "Alternative address sources".

### C1. Hospital Directory / NIN Health Facilities (National Health Portal)

1. AIKosh names the National Institute of Health and Family Welfare (NIHFW)
   [MIR, R1]. The OSM page names MoHFW, Department of Health and Family Welfare,
   NIHFW [COMM, R6]. Exact publisher string [U].
2. R13, R14 (403); mirror R1.
3. `government_published` (first-pass reading; classification open, G4).
4. State-wise list of hospitals with location, category, systems of medicine,
   contact details, PIN, email, website, specialities [SRCH]. An ownership
   (government/private) attribute [MIR, R1].
5. All India per metadata [MIR, R1]. Per-state counts [U].
6. **The actual header of the C1 files has not been seen [U].** R6 lists the
   attributes the OSM import kept, after combining three directories (hospital,
   NIN health facilities, blood banks) and converting values for OSM. Those
   attributes (`Address`, `Street`, `Locality`, `Pincode`, `State_Name`,
   `District_Name`, `Taluka_Name`, `Block_Name` and others) may be renamed or
   merged, so they **do not establish C1's source columns** [COMM, R6].
7. [U].
8. R6 says the import excluded a `Hospital_Reg_No` field [COMM]. Whether C1 has a
   stable per-record identifier [U].
9. CSV, 9.86 MB, uploaded 2017-08-10, frequency "Static" [MIR, R1], while the
   title says "updated till last month". Unresolved metadata conflict.
10. data.gov.in site-wide GODL-India statement [ADR, ADR-0002, checked
    2026-10-02]; licence label "GODL" [MIR, R1]. Per-resource licence [U].
    data.gov.in blocked the first-pass fetch tool [ADR, ADR-0004]; see G5.
11. Institutional facilities. Among the attributes the OSM import **kept**, R6
    lists `Mobile_Number` and `Hospital_Primary_Email_Id`. Among those it
    **excluded**, R6 lists a field described as "personal information" [COMM].
    So the import's inputs carried phone, email and personal-information fields.
    **Open verification question:** which of these C1 actually has, and whether
    they identify people. This needs the real header row.
12. R6 reports geocodes within about 150–200 m, invalid placeholder values and
    duplicates [COMM]. **Open verification question:** whether C1 publishes a
    single address string usable as `raw_text`, or only components (G2).
13. One national publisher. Publisher diversity and per-state source availability
    are unknown, so whether holding it out is workable cannot be judged yet.

### C2. All India Health Centres Directory

1. MoHFW, Department of Health and Family Welfare [MIR, R2].
2. R15 (403); mirror R2.
3. `government_published` (first-pass reading; classification open, G4).
4. Sub-centres, PHCs, CHCs, district and state hospitals [MIR, R2].
5. All India [MIR, R2].
6. State, district, sub-district, facility name, address, coordinates [MIR, R2].
   Header row not seen [U].
7. [U]. 8. [U].
9. Snapshot "as on 7th October, 2016", uploaded 2017-09-21, CSV 20 MB [MIR, R2].
   The same page gives the update frequency as "Monthly" [MIR, R2]. **Unresolved
   metadata conflict:** a monthly frequency against a dated 2016 snapshot.
10. Licence label "GODL" [MIR, R2]; data.gov.in site-wide statement [ADR].
11. Public facilities; personal columns [U].
12. Possibly ten years old. The facility types suggest mostly rural public
    facilities, which is an inference, not a finding [U].
13. Same ministry as C1. Whether C1 and C2 are one `publisher` [U] (G4).

### C3. CGHS empanelled hospitals

1. Central Government Health Scheme, MoHFW [MIR, R3].
2. Mirror R3; data.gov.in original URL [U].
3. `government_published` (first-pass reading; classification open, G4).
4. Hospitals, diagnostic centres and eye-care facilities empanelled under CGHS
   [MIR, R3].
5. CGHS cities [MIR, R3]. Which cities [U].
6. "City Names, hospital names, address details" [MIR, R3]. Exact columns [U].
7. [U]. 8. [U].
9. Uploaded 2019-04-08, half-yearly, last deployed 2026-09-30 [MIR, R3].
10. Licence label "GODL" [MIR, R3].
11. Institutional; personal columns [U].
12. City-based, so likely urban [U]. Size [U].
13. Publisher identity versus C1 [U] (G4).

### C4. Telangana health centres

1. Telangana Health, Medical and Family Welfare Department, via Open Data
   Telangana [MIR, R4].
2. R11 (portal title only); mirror R4.
3. `government_published` (first-pass reading; classification open, G4).
4. Health centres with facility type, ownership (government, private, NGO) and
   operational status [MIR, R4].
5. Telangana [MIR, R4].
6. `State`, `District`, `Taluka`, `Street`, `Landmark`, `Locality`, region
   indicator, latitude, longitude, as listed on R4 [MIR]. Header row not seen [U].
7. [U]. 8. [U].
9. Uploaded 2025-02-19, annual [MIR, R4].
10. "Open Government License, India" [MIR, R4]. Portal terms not obtained (R11) [U].
    (Sixth pass: portal terms and licence evidence recorded under "C4 licence
    and retrieval terms".)
11. Institutional; personal columns [U].
12. Address documented as components, not one string. Whether components can
    form `raw_text` is open (G2).
13. A state publisher distinct from the central ministry, covering one state.

### C5. Polling-station lists (State Chief Electoral Officers)

1. Office of the Chief Electoral Officer of each state.
2. Tamil Nadu: per-constituency PDFs on `elections.tn.gov.in` (R21, not opened);
   Dindigul district page (R20). Karnataka: R22.
3. `government_published` (first-pass reading; classification open, G4).
4. Tamil Nadu: polling-station number, building, locality, polling areas, and
   whether a station serves all voters [SRCH]. This came from a search summary
   that was probably generated from the PDFs or pages describing them; no PDF
   was opened.
5. **Tamil Nadu:** per-constituency lists on the state CEO site [SRCH, R21];
   statewide completeness [U]. **Karnataka:** only one district-level page (R22)
   was found, describing notices of list publication [SRCH]. **Statewide
   coverage in Karnataka is unknown**, and so is any other state's.
6. See 4 [SRCH].
7. Tamil Nadu: Tamil and English [SRCH, R20]; English path segments in R21
   [SRCH]. Other states [U].
8. Polling-station number within a constituency, from the same whole-query
   summary as item 4 [SRCH]; stability [U].
9. Dated directory names (`PSLIST_09112022`, `PSLIST_27102023`) [SRCH, R21].
10. **[U].** No licence or copyright statement found.
11. Whether the listed buildings are institutional is not verified; this
    inventory infers it from polling stations usually being public buildings
    (inference, not a finding). "Polling areas" describe the residential areas
    served [SRCH]. **Flag:** electoral rolls are personal data and must never be
    retrieved. Whether CEO sites host them alongside the polling-station lists
    was not verified [U]; any retrieval must be limited to the lists.
12. The lists found are PDFs [SRCH, R21]. Whether other formats exist [U].
13. One publisher per state, so structurally suited to per-publisher holdout.
    Blocked by the unknown licence.

### C6. Kendriya Vidyalaya directory

1. Kendriya Vidyalaya Sangathan [PUB, R10].
2. R10 (directory and "Know Your School" search).
3. `government_published` (first-pass reading; classification open, G4).
4. Kendriya Vidyalaya schools. The page summary reports **1,367** schools,
   listing Moscow, Tehran and Kathmandu (one each) alongside India [PUB, R10].
   If those three are included in 1,367, the India count would be 1,364 [CALC];
   **the India split is not directly verified.**
5. All India; per-state counts [U].
6. Search by UDISE code, school name or PIN [PUB, R10]. Downloadable fields [U].
7. Address language and script [U].
8. Schools are searchable by UDISE code [PUB, R10]. Whether that code is stable
   is not verified [U].
9. [U].
10. Footer states content ownership by KVS; no reuse licence on the homepage
    [PUB, R10]. "Website Policies" page not read [U].
11. Institutional.
12. Database search rather than a file; whether bulk retrieval is allowed [U].
13. Small per state [U].

### Not usable as found, or not assessable

| Source | Publisher | Finding |
|---|---|---|
| AISHE college/university directory | Dept. of Higher Education, MoE | **Unresolved.** Columns per R5: AISHE Code, Name of the Institution, State, District, Year of Establishment, Location, College Type, Management, Affiliated University Name and Type [MIR]. Whether `Location` holds address text was not inspected [U]. Address suitability unverified. Licence label "Open Government License, India" [MIR, R5]. |
| UDISE+ school data | Dept. of School Education & Literacy, MoE | data.gov.in releases are aggregates up to 2019-20 [SRCH, R17]. **An official API was identified** (R18) [SRCH]; its access conditions, terms and suitability are not verified [U]. Copies at R16 and R19 are third-party [3P] and would be a new source category (ADR-0007 §5). |
| RBI IFSC/MICR branch lists | Reserve Bank of India | Interactive search [PUB, R8]. Disclaimer, per the fetch summary (not directly inspected) [PUB, R7]: "All Rights Reserved"; caching prohibited; framing prohibited; linking to the homepage requires notifying RBI in writing, and linking to internal pages requires RBI's prior permission; the page grants no reuse licence. **Rejected under ADR-0007 §5: no licence found.** To be re-checked against the page text before any source ADR cites it. |
| `razorpay/ifsc` and similar compilations | Third parties | Compiled from RBI and NPCI files; claims "public domain" data [3P, R9], which is not RBI's statement. **Rejected:** aggregator, a new source category. |
| PMJAY empanelled hospitals | National Health Authority | Public dashboard PDF download, per a **third-party** guide [SRCH, 3P, R23]. Terms [U]. Not assessable. |
| ABDM Health Facility Registry | National Health Authority | Public facility search; registration collects facility contact-person details [SRCH, R24]. Fetch returned only a title (R12). Bulk download and terms [U]. Not assessable. |
| Oil-company retail outlets | MoPNG / OMCs | data.gov.in resources found are counts, not addresses [SRCH, R25]. |
| Bank/ATM locators (e.g. SBI) | Operators | One search returned no download or reuse terms; no page was fetched [SRCH, no R#]. Not assessable. |
| OpenStreetMap | Contributors | Not published by an operator or government; ODbL. **Rejected for v0:** new source category (ADR-0001 §4, ADR-0007 §5). |

### Identified but not researched

Listed so the gap is visible. None is claimed to be suitable. (Eighth pass:
AISHE, UDISE+, CBSE and seven state open-data instances were looked at; see
"Alternative address sources". UGC, eCourts and NIC district pages remain
unresearched.)

- CBSE affiliated-school directory
- UGC list of universities
- "Public utilities" pages on NIC district websites
- eCourts court-complex information
- State open-data portals other than Telangana
- The UDISE+ API (R18), beyond noting that it exists

**Flagged for personal-data risk, not assessed:** fair-price-shop (PDS) dealer
lists, Common Service Centre lists, Anganwadi centre lists, drug or food licence
registers. The listed operator is commonly a named individual and the premises
may be a residence. **This is an assumption to verify from documentation, not a
finding.**

**`operator_published` family:** no candidate with a known licence was found.
(Eighth pass: still none.)

## Candidate-state evidence

**No state meets ADR-0007 §4 step 2 today,** because no source has been accepted.
This is input for later selection records, not a ranking.

| State | Source evidence specific to the state | Language/script per documentation | Region | Urban/rural coverage observable | Acquisition feasibility |
|---|---|---|---|---|---|
| Telangana (`lgd:state:36`) | C4 [MIR, R4] | [U] | Not yet verified | C4 includes urban health centres as a facility type [MIR, R4]; gazetteer: 3 sub-districts without villages [CALC] | Portal terms not obtained (R11); mirror lists the dataset; not yet verified |
| Tamil Nadu (`lgd:state:33`) | C5 lists on the CEO site [SRCH, R20, R21] | Tamil and English [SRCH, R20] | Not yet verified | Not yet verified | PDFs; licence unknown; not yet verified |
| Karnataka (`lgd:state:29`) | One district-level page only [SRCH, R22]; statewide coverage unknown | [U] | Not yet verified | Not yet verified | Not yet verified |
| All other states | Only national sources C1–C3, C6; per-state coverage [U] | [U] | Not yet verified | Gazetteer gaps in the table below [CALC] | C1–C3 via data.gov.in; first-pass fetches blocked [ADR], second-pass metadata retrieved (G5); not yet verified |

The gazetteer has no urban units, so it cannot show urban coverage. It only shows
where villages are missing ("Districts/Sub-districts w/o villages" below).

Gazetteer properties [CALC], computed with an ad-hoc script from
`data/processed/gazetteer/` (not the versioned procedure ADR-0007 §4 requires).
Totals reproduce `docs/gazetteer.md`: 784 districts, 7,092 sub-districts, 672,619
villages, 6 districts and 30 sub-districts without villages, 11,258
`same_name_siblings` and 132 `variant_name_siblings` records. "Same-name" and
"Variant-name" count warning records; "Villages/PIN" is the median number of
villages per PIN within the state; "PINs > 1 state" counts that state's PINs that
also map villages in another state.

| State/UT | LGD ID | Districts | Sub-districts | Villages | Districts w/o villages | Sub-districts w/o villages | Same-name | Variant-name | PINs | Villages/PIN | PINs > 1 state |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Andaman And Nicobar Islands | 35 | 3 | 9 | 559 | 0 | 0 | 3 | 0 | 18 | 20 | 0 |
| Andhra Pradesh | 28 | 28 | 688 | 17,954 | 0 | 0 | 132 | 0 | 1,149 | 10 | 0 |
| Arunachal Pradesh | 12 | 27 | 209 | 5,485 | 0 | 0 | 16 | 0 | 47 | 59 | 0 |
| Assam | 18 | 35 | 161 | 28,723 | 0 | 1 | 438 | 9 | 517 | 37 | 2 |
| Bihar | 10 | 38 | 537 | 48,927 | 0 | 0 | 2,949 | 3 | 794 | 41 | 0 |
| Chandigarh | 4 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | – | 0 |
| Chhattisgarh | 22 | 33 | 252 | 20,630 | 0 | 0 | 327 | 0 | 258 | 68 | 0 |
| Delhi | 7 | 13 | 39 | 208 | 3 | 13 | 0 | 0 | 38 | 3 | 0 |
| Goa | 30 | 3 | 12 | 429 | 0 | 0 | 0 | 0 | 75 | 3 | 0 |
| Gujarat | 24 | 34 | 306 | 19,057 | 0 | 7 | 15 | 1 | 918 | 13 | 5 |
| Haryana | 6 | 23 | 143 | 7,082 | 0 | 0 | 3 | 0 | 280 | 17 | 0 |
| Himachal Pradesh | 2 | 12 | 193 | 21,592 | 0 | 0 | 5 | 0 | 430 | 33 | 2 |
| Jammu And Kashmir | 1 | 20 | 208 | 6,857 | 0 | 0 | 4 | 6 | 177 | 32 | 0 |
| Jharkhand | 20 | 24 | 264 | 32,737 | 0 | 1 | 1,007 | 63 | 254 | 76 | 0 |
| Karnataka | 29 | 31 | 240 | 29,900 | 0 | 0 | 646 | 16 | 1,220 | 17 | 0 |
| Kerala | 32 | 14 | 78 | 1,666 | 0 | 0 | 0 | 0 | 1,020 | 1 | 0 |
| Ladakh | 37 | 2 | 15 | 248 | 0 | 0 | 0 | 0 | 13 | 19 | 0 |
| Lakshadweep | 31 | 1 | 10 | 27 | 0 | 0 | 0 | 0 | 9 | 2 | 0 |
| Madhya Pradesh | 23 | 55 | 445 | 57,478 | 0 | 0 | 1,125 | 0 | 724 | 68 | 0 |
| Maharashtra | 27 | 36 | 358 | 44,805 | 1 | 0 | 1 | 0 | 1,465 | 17 | 0 |
| Manipur | 14 | 16 | 65 | 3,850 | 0 | 0 | 15 | 2 | 49 | 45 | 0 |
| Meghalaya | 17 | 12 | 56 | 7,107 | 0 | 0 | 52 | 2 | 65 | 65 | 2 |
| Mizoram | 15 | 11 | 28 | 887 | 0 | 0 | 0 | 0 | 34 | 16 | 0 |
| Nagaland | 13 | 17 | 120 | 1,570 | 0 | 0 | 17 | 0 | 42 | 26.5 | 0 |
| Odisha | 21 | 30 | 317 | 50,217 | 0 | 2 | 1,041 | 2 | 809 | 46 | 0 |
| Puducherry | 34 | 2 | 8 | 123 | 0 | 1 | 0 | 0 | 29 | 3 | 17 |
| Punjab | 3 | 23 | 97 | 13,006 | 0 | 0 | 0 | 1 | 507 | 18 | 1 |
| Rajasthan | 8 | 41 | 425 | 51,448 | 0 | 0 | 512 | 23 | 975 | 35 | 0 |
| Sikkim | 11 | 6 | 19 | 485 | 0 | 0 | 5 | 0 | 18 | 15.5 | 0 |
| Tamil Nadu | 33 | 38 | 317 | 18,652 | 0 | 0 | 88 | 2 | 1,866 | 7 | 17 |
| Telangana | 36 | 33 | 621 | 11,296 | 0 | 3 | 41 | 0 | 612 | 16 | 0 |
| The Dadra And Nagar Haveli And Daman And Diu | 38 | 3 | 3 | 101 | 0 | 0 | 0 | 0 | 9 | 8 | 5 |
| Tripura | 16 | 8 | 23 | 898 | 0 | 0 | 3 | 0 | 73 | 10 | 0 |
| Uttar Pradesh | 9 | 75 | 350 | 110,268 | 0 | 0 | 2,038 | 1 | 1,583 | 51 | 2 |
| Uttarakhand | 5 | 13 | 129 | 17,342 | 0 | 0 | 273 | 0 | 276 | 45.5 | 1 |
| West Bengal | 19 | 23 | 346 | 41,005 | 1 | 1 | 502 | 1 | 871 | 29 | 0 |

These counts describe the gazetteer, not address sources. They are not evidence
of what LGD's sub-district tier means in any state (ADR-0007 §8).

## Licence and header verification (second pass, 2026-10-04)

Evidence status only. **No source is accepted** and no manifest is written.

### Method

- Publisher pages and publisher-platform metadata APIs were retrieved with
  `curl` from the development machine and the saved responses were read
  directly. This differs from the first pass, which relied on model summaries.
  New label: **[PUBD]** = publisher page or publisher-platform API, retrieved
  directly and inspected.
- Only metadata was requested:
  - data.gov.in: catalog and resource metadata (`backend/dmspublic/v1`) and API
    descriptors with field lists (`backend/dataapi/v1/lists`). Neither returns
    data rows.
  - Telangana portal (DKAN): dataset metadata and a datastore query with
    `limit=0&results=false&schema=true`, which returns the schema and a row
    count but no rows.
- **No data file was downloaded, no PDF was opened and no address record was
  retrieved.** Saved responses are in a scratch directory outside the
  repository and are not committed.
- data.gov.in pages, which returned 403 to the first pass's fetch tool, returned
  200 to `curl`.
- A field list from a platform API is the publisher's schema for the resource.
  It is not byte-for-byte the downloadable file's header row: data.gov.in adds
  `document_id` and `resource_uuid`, and file headers were not read. (Fifth
  pass: C3's list has neither field.)

### Sources for this pass

All retrieved on **2026-10-04**.

| # | URL | Kind | Supports |
|---|---|---|---|
| R26 | https://www.data.gov.in/catalog/hospital-directory-national-health-portal | [PUBD] | C1 catalog metadata; data.gov.in footer licence text |
| R27 | https://data.gov.in/catalog/all-india-health-centres-directory | [PUBD] | C2 catalog page; same footer |
| R28 | https://www.data.gov.in/backend/dmspublic/v1/catalogs?filters[node_alias]=/catalog/hospital-directory-national-health-portal (and the same query for `/catalog/all-india-health-centres-directory`) | [PUBD] | C1 and C2 catalog metadata |
| R29 | https://www.data.gov.in/backend/dmspublic/v1/resources?filters[catalog_reference]=323881 | [PUBD] | C1 resource metadata |
| R30 | https://www.data.gov.in/backend/dmspublic/v1/resources?filters[catalog_reference]=3786581 | [PUBD] | C2 resource metadata |
| R31 | https://www.data.gov.in/backend/dmspublic/v1/resources?filters[node_alias]=/resource/list-hospitals-empaneled-under-cghs-all-over-india | [PUBD] | C3 resource metadata |
| R32 | https://www.data.gov.in/backend/dataapi/v1/lists?format=json&filters[catalog_uuid]=e48a8bcf-ff56-4f39-839d-095827ba2a18 | [PUBD] | C1 field lists |
| R33 | https://www.data.gov.in/backend/dataapi/v1/lists?format=json&filters[catalog_uuid]=09ef97dd-3b9f-4b2c-bd3d-c24a0e084463 | [PUBD] | C2 field list |
| R34 | https://www.data.gov.in/backend/dataapi/v1/lists?format=json&filters[catalog_uuid]=624753e6-6052-4ef0-8a25-631f22739ebb | [PUBD] | C3 field list |
| R35 | https://data.telangana.gov.in/api/1/search?fulltext=health%20centres | [PUBD] | C4 dataset identified; per-dataset licence labels |
| R36 | https://data.telangana.gov.in/api/1/metastore/schemas/dataset/items/44935575-631b-4116-b278-41f4c507b95b | [PUBD] | C4 metadata and licence |
| R37 | https://data.telangana.gov.in/api/1/datastore/query/44935575-631b-4116-b278-41f4c507b95b/0?limit=0&results=false&schema=true&count=true | [PUBD] | C4 schema and row count |
| R38 | https://www.elections.tn.gov.in/ | [PUBD] | C5 Tamil Nadu: footer and links |
| R39 | https://dindigul.nic.in/website-policies/ | [PUBD] | C5: Dindigul district copyright policy |
| R40 | https://chikkaballapur.nic.in/en/website-policies/ | [PUBD] | C5: Chikkaballapur district copyright policy |
| R41 | http://kvsangathan.nic.in/ (HTTPS timed out; HTTP answered) | [PUBD] | C6: school counter, footer |
| R42 | http://kvsangathan.nic.in/वेबसाइट-नीतियां/ (percent-encoded in the site's link) | [PUBD] | C6: copyright policy |
| R43 | http://kvsangathan.nic.in/के-वि-की-निर्देशिका/ (percent-encoded in the site's link) | [PUBD] | C6: directory page structure |

### Licence findings

Categories: (a) explicit reuse licence for the dataset; (b) site-wide licence;
(c) copyright statement without reuse permission, or reuse only on request;
(d) terms of use; (e) unknown.

- **data.gov.in (C1, C2, C3).** Category **(b)**. Three separate facts:
  - **(i) Licence basis, previously verified.** data.gov.in's site-wide
    statement that its content is "licensed under the Government Open Data
    License - India", and the GODL-India text, were verified on 2026-10-02 and
    recorded in ADR-0002 [ADR]. This remains the licence basis for C1–C3.
  - **(ii) No resource-level licence.** The current resource metadata has no
    licence field (R29, R30, R31) [PUBD]. Nothing at resource level confirms or
    contradicts (i). The catalog pages for C1 and C2 also say "Released Under:
    National Data Sharing and Accessibility Policy (NDSAP)" [PUBD, R26, R27].
  - **(iii) Unresolved sandbox notice.** The footer served on 2026-10-04 at R26
    and R27 repeats the site-wide GODL-India statement, and adds "All rights
    reserved except published datasets/resources and metadata." It also says
    "This is a sandbox environment created for testing and demonstration
    purposes only. The content, data, and functionality may be incomplete or
    inaccurate." [PUBD, R26, R27]. Whether the pages retrieved were the
    production site is unverified, so **this pass's re-check of (i) is
    inconclusive**. It neither confirms nor withdraws the ADR-0002 finding.
- **Telangana portal (C4).** Category **(a)** by publisher label only: the
  dataset names a licence, but the licence text itself has not been verified, so
  this does not yet meet (a) in substance.
  - **Verified:** the dataset's `license` field reads "Government Open Data
    License - India" [PUBD, R36]. Other health datasets on the portal read
    "License Not Specified" [PUBD, R35], so the field varies by dataset.
  - **Not verified:** the metadata gives no URL or text for that licence, so
    which licence text applies, and whether it is the same instrument as the
    GODL-India text verified for data.gov.in in ADR-0002, is not independently
    verified [U].
  - (Sixth pass: no licence text was found on the portal, and its Copyright Policy
    and footer conflict with the label; see "C4 licence and retrieval
    terms".)
- **CEO Tamil Nadu (C5).** Category **(c)**.
  - Footer: "© 2021 Public (Elections) Department, Tamil Nadu. All rights
    reserved." [PUBD, R38]. No copyright, terms or policy page is linked from
    the homepage [PUBD, R38].
- **District sites (C5 district evidence).** Category **(c)**, reuse on request.
  - Dindigul and Chikkaballapur both state: "Material featured on this website
    may be reproduced free of charge after taking proper permission by sending a
    mail to us." [PUBD, R39, R40]. These are district administrations, not the
    CEO.
- **KVS (C6).** Category **(c)**, reuse on request.
  - Copyright policy (Hindi): "इस पोर्टल पर प्रदर्शित सामग्री को हमें एक मेल भेजकर
    उचित अनुमति लेने के बाद नि:शुल्क पुन: प्रस्तुत किया जा सकता है।" [PUBD, R42].
    Translation by this inventory: material on the portal may be reproduced free
    of charge after obtaining proper permission by sending a mail. The same page
    disallows loading its pages in frames.

### Header and schema findings

| Candidate | Resource verified | Fields (exact names from the publisher's schema) | Single address string | Components | Identifier field | Language/script field | Person or contact fields |
|---|---|---|---|---|---|---|---|
| C1a | "National Hospital Directory with Geo Code and additional parameters (updated till last month)" [PUBD, R29, R32] | Sr_No, Location_Coordinates, Location, Hospital_Name, Hospital_Category, Hospital_Care_Type, Discipline_Systems_of_Medicine, Address_Original_First_Line, State, District, Subdistrict, Pincode, Telephone, Mobile_Number, Emergency_Num, Ambulance_Phone_No, Bloodbank_Phone_No, Foreign_pcare, Tollfree, Helpline, Hospital_Fax, Hospital_Primary_Email_Id, Hospital_Secondary_Email_Id, Website, Specialties, Facilities, Accreditation, Hospital_Regis_Number, Registeration_Number_Scan, Nodal_Person_Info, Nodal_Person_Tele, Nodal_Person_Email_Id, Town, Subtown, Village, Establised_Year, Ayush, Miscellaneous_Facilities, Number_Doctor, Num_Mediconsultant_or_Expert, Total_Num_Beds, Number_Private_Wards, Num_Bed_for_Eco_Weaker_Sec, Empanelment_or_Collaboration_with, Emergency_Services, Tariff_Range, State_ID, District_ID | `Address_Original_First_Line` (named a first line; whether it holds a full address [U]) | Location, Town, Subtown, Village, State, District, Subdistrict, Pincode | Hospital_Regis_Number, Sr_No; stability [U]. State_ID and District_ID scheme [U] | None | **Nodal_Person_Info, Nodal_Person_Tele, Nodal_Person_Email_Id** (named as a person's details); Mobile_Number, Telephone and email fields (whose numbers is not documented) |
| C1b | "NIN Health Faclities with Geo Code and additional parameters (updated till last month)" [PUBD, R29, R32] | SrNo, Health Facility Name, Address, street, landmark, locality, pincode, landline_number, latitude, longitude, altitude, Facility Type, State_Name, District_Name, Taluka_Name, Block_Name | `Address` | street, landmark, locality, pincode, State_Name, District_Name, Taluka_Name, Block_Name | None in the schema, although the resource note defines "NIN: National Identification Number" [PUBD, R29] | None | landline_number |
| C2 | "All India Health Centres Directory as on 7th October, 2016" [PUBD, R30, R33] | State Name, District Name, Subdistrict Name, Facility Type, Facility Name, Facility Address, Latitude, Longitude, ActiveFlag_C, NOTIONAL_PHYSICAL, Location Type, Type Of Facility, Nin_N | `Facility Address` | State Name, District Name, Subdistrict Name | `Nin_N`; stability [U] | None | None |
| C3 | "List of Hospitals empaneled under CGHS all over India" [PUBD, R31, R34] | DiagnosticCentreName, DiagnosticCentreAddress, CityName | `DiagnosticCentreAddress` | CityName only; **no state or district field** | None | None | None |
| C4 | "Details of Health centres latitude and longitude in Telangana" [PUBD, R36, R37] | State, District, Taluka, Facility Name, Facility Type, Latitude, Longitude, Street, Landmark, Locality, Region Indicator, Operational Status, Ownership Authority | **None** | Street, Landmark, Locality, Taluka, District, State | None | None | None |
| C5 | CEO Tamil Nadu lists; Karnataka district evidence | **[U].** The lists are PDFs (R21). Reading their columns means opening a file that contains records, which this pass did not do. | [U] | [U] | [U] | [U] | [U] |
| C6 | KVS directory [PUBD, R43] | **[U].** The directory is a search form filtered by state (राज्य) and region (संभाग); no table or field names are in the page's HTML. Results load only on search. | [U] | [U] | [U] | [U] | [U] |

Notes:
- **C1** catalog: contributor "Ministry of Health and Family Welfare; Department
  of Health and Family Welfare; National Institute of Health and Family Welfare
  (NIHFW), New Delhi"; published 2015-08-13 [PUBD, R26]. The catalog holds six
  resources, including dated 2015 and 2016 snapshots and a dispensaries
  directory [PUBD, R32]. C1a has frequency "One-time" and granularity "Monthly";
  C1b has frequency "Monthly" and its data file is hosted at `info.nhp.gov.in`
  [PUBD, R29]. Both resource nodes were last changed 2026-08-11 [PUBD, R29];
  whether the data changed then [U]. Field names keep the publisher's spelling
  ("Faclities", "Establised", "Registeration").
- **C2**: frequency "Monthly", granularity "Others", file 20,967,450 bytes,
  resource published 2017-09-20 [PUBD, R30], while the title fixes the data at
  7 October 2016. The first-pass conflict stands.
- **C3**: catalog "Central Government Health Scheme", resource frequency "Half
  yearly", file 80,196 bytes, resource last changed 2026-07-31 [PUBD, R31].
  The hospital resource's fields are named `DiagnosticCentre…`, the same as the
  diagnostics-centre resource in that catalog [PUBD, R34]. Whether they are
  mislabelled [U]. (Fifth pass: "the same as" is corrected under "B6 aggregate
  and schema inspection"; the two resources' field names differ in spelling.)
- **C4**: publisher "Health and Medical and Family Welfare", author "The Health,
  Medical & Family Welfare", contact "Telangana Open Data Unit"; modified
  2023-02-15 [PUBD, R36]. Its description says "Data available As on 8th
  February 2023" while its distribution title says "as on 8th November 2022"
  [PUBD, R36]: unresolved. Datastore row count **7,001** (source-reported)
  [PUBD, R37]. The column set matches the AIKosh record R4, but that R4 is this
  dataset is not verified (titles and dates differ). Meaning of `Region
  Indicator` [U].

### Publisher identity (ADR-0007 §5, §6)

Recorded as the publisher states it. Whether each counts as "a government body"
for `source_family`, and how `publisher` strings are normalized for holdout,
stays open (G4).

| Candidate | Publisher as stated | Note |
|---|---|---|
| C1 | Ministry of Health and Family Welfare / Department of Health and Family Welfare / National Institute of Health and Family Welfare (NIHFW), New Delhi [PUBD, R26, R29] | Three-level string |
| C2 | Ministry of Health and Family Welfare / Department of Health and Family Welfare [PUBD, R30] | Shares two levels with C1 |
| C3 | Ministry of Health and Family Welfare / Department of Health and Family Welfare / Central Government Health Scheme (CGHS) [PUBD, R31] | Shares two levels with C1 |
| C4 | "Health and Medical and Family Welfare" on the Telangana Open Data portal [PUBD, R36] | A state department |
| C5 | "Public (Elections) Department, Tamil Nadu" in the CEO site footer [PUBD, R38]; district pages are published by district administrations [PUBD, R39, R40] | CEO versus district publisher is unresolved |
| C6 | "केन्द्रीय विद्यालय संगठन" (Kendriya Vidyalaya Sangathan) as content owner; the page title adds "भारत सरकार" (Government of India) [PUBD, R41] | Legal status not verified here; classification open. The first pass's `government_published` for C6 is therefore not confirmed. |

### Other second-pass facts

- **C5:** the CEO Tamil Nadu homepage links to an `ElectoralRolls.aspx` page and
  to `voters.eci.gov.in/download-eroll` [PUBD, R38]. Neither was opened. This
  confirms the first pass's flag: retrieval from this site must be limited to
  polling-station lists.
- **C6:** the homepage counter reads "1,367", labelled "भारत और दुनिया भर में
  के. वि." (KVs in India and around the world), with "मास्को - 01, तेहरान - 01,
  काठमांडू - 01" [PUBD, R41]. The 1,367 therefore includes the three abroad, and
  1,364 are in India [CALC]. This settles the first pass's open point.

### Evidence status per candidate

Evidence status only, **not source acceptance**.

| Candidate | Licence | Schema | Status | What blocks further progress |
|---|---|---|---|---|
| C1a, C1b | (b) Basis: site-wide GODL-India, verified 2026-10-02 (ADR-0002). This pass: no resource-level field; re-check inconclusive (sandbox notice) | Verified (platform schema) | **licence_unverified in this pass**; ADR-0002 basis stands, pending the sandbox question | Sandbox notice; person fields `Nodal_Person_*` must stay out of `context_columns`; `Address_Original_First_Line` completeness [U] |
| C2 | (b) as C1 | Verified (platform schema) | **licence_unverified in this pass**; ADR-0002 basis stands, pending the sandbox question | Sandbox notice; 2016 data; frequency conflict |
| C3 | (b) as C1 | Verified (platform schema) | **licence_unverified in this pass**; ADR-0002 basis stands, pending the sandbox question | Sandbox notice; no state or district field; field naming [U] |
| C4 | (a) publisher licence label "Government Open Data License - India"; no licence text or URL | Verified (datastore schema) | **licence_unverified**: publisher licence label verified; applicable licence text not independently verified. Not rejected. | Licence text; no single address string (G2); date conflict; identity with R4 [U] |
| C5 | (c) all rights reserved (CEO TN); reuse on request (district sites) | Not verified | **both_unverified** | No reuse licence found; schema needs opening record-bearing PDFs |
| C6 | (c) reuse on request by email | Not verified | **both_unverified** | No reuse licence without a request; no static schema |

This table records the second pass. For C1–C3, the sandbox question in it is
answered by the third pass ("data.gov.in host and licence re-check"). The
fourth pass ("Terms of use and retrieval conditions") found C1b's file hosted
outside data.gov.in, so C1b's licence is unresolved rather than "as C1a". The
sixth pass ("C4 licence and retrieval terms") found no licence text for C4 and
a conflicting portal Copyright Policy; C4 stays licence_unverified.

### Still unresolved after the second pass

- Whether the data.gov.in sandbox notice applies to the production site.
  (Answered by the third pass, 2026-10-05.)
- The licence text behind C4's "Government Open Data License - India" label.
- Whether C1a's `Address_Original_First_Line` holds a full address; what
  `State_ID`, `District_ID`, `Region Indicator`, `Location Type` and
  `NOTIONAL_PHYSICAL` mean.
- Stability of `Hospital_Regis_Number` and `Nin_N`.
- Any language or script information: no schema has such a field.
- C5 and C6 schemas, and whether either publisher would grant permission.
- Whether concatenated components can serve as `raw_text` (G2). Not decided
  here.

## data.gov.in host and licence re-check (third pass, 2026-10-05)

Evidence status only. **No source is accepted** and no manifest is written. This
pass addresses only the second pass's sandbox question for C1–C3.

### Method

- Pages, site scripts and metadata APIs were retrieved with `curl` on
  2026-10-05 (from 14:04 UTC) and the saved responses were read directly [PUBD].
- No data file was downloaded and no dataset record was retrieved. The metadata
  APIs are the same `backend/dmspublic/v1` endpoints as R28–R31.
- The licence body on `/Godl` is not in the server-rendered HTML. The page loads
  it from a route script (R47), and the text was read from that script, not from
  a rendered browser page.
- For comparison, copies saved locally during the ADR-0002 work on 2026-10-02
  and during the second pass on 2026-10-04 were read. They are outside the
  repository and are cited as local saved copies, not as publisher retrievals.

### Sources for this pass

| # | URL | Kind | SHA-256 of saved response | Supports |
|---|---|---|---|---|
| R44 | https://data.gov.in/ and https://www.data.gov.in/ | [PUBD] | `e8972bf1d36fed1745b5be80950424475f021e4bd2d6a773763001ebb19b2f0b` (www homepage) | Redirect; footer markup; canonical link |
| R45 | https://www.data.gov.in/Godl | [PUBD] | `251aee4b5cadaacb48fde9d7de7d2e43f28cd23f88af0360729a778fc7323511` | Licence page; footer markup; scripts it loads |
| R46 | https://www.data.gov.in/_nuxt/fabd03c.js | [PUBD] | `8da0ada885d65f8edee54a3d37f60ea6ce8d8c1bf5e172254705de53e849a493` | Site build configuration; sandbox-notice condition |
| R47 | https://www.data.gov.in/_nuxt/36aab54.js | [PUBD] | `45fc26bc7b8d0b25fa746c168d1c37bd6be28dfae91b5e09b45f72ce2ad23458` | GODL-India licence text served by `/Godl` |
| R48 | The R29, R30 and R31 resource queries, and the two R28 catalog queries | [PUBD] | not recorded here | C1–C3 resource and catalog metadata keys |

### Findings

- **Host.** `https://data.gov.in/` answers `301 Moved Permanently` with
  `Location: https://www.data.gov.in/`. Every page in this pass was served by
  `www.data.gov.in`. The homepage's canonical link is `https://data.gov.in`
  [PUBD, R44].
- **The sandbox notice is a hidden template element, not a statement about this
  host.**
  - In the HTML of R44 and R45, the sandbox sentence sits in
    `<p style="display:none;">`, so it is not displayed [PUBD].
  - The site script shows that paragraph only under the condition
    `['sandbox.data.gov.in'].includes(DOMAIN_NAME)` [PUBD, R46].
  - The same script's build configuration sets
    `VUE_APP_DOMAIN_NAME: "www.data.gov.in"`, and its context sets
    `isDev: false` [PUBD, R46].
  - So the notice is displayed only on a host named `sandbox.data.gov.in`, and
    on `www.data.gov.in` it is present in the markup but hidden.
  - The local saved copies from 2026-10-02 (`/Godl`) and 2026-10-04 (C1 and C2
    catalog pages) have the same hidden `display:none` paragraph.
- **What this establishes about "production".** The site states no explicit
  "production" label. What is established from the site itself:
  - `www.data.gov.in` is the host `data.gov.in` redirects to.
  - It is configured with its own domain name, not as the sandbox, and the
    sandbox notice is inactive there.
  - The second pass's pages came from this host.

  An attempt to reach `https://sandbox.data.gov.in/` ended in a connection
  reset, so nothing about that host is established.
- **Licence statement.** The footer of R44 and R45 still states that "The
  content published on data.gov.in is owned by the respective
  Ministry/State/Department/Organization and licensed under the Government Open
  Data License - India", linking to `/Godl` [PUBD].
- **Licence text.** The `/Godl` route script (R47) contains the GODL-India text
  [PUBD]. Every element ADR-0002 relied on is present:
  - the worldwide, royalty-free, non-exclusive licence to use, adapt, publish,
    translate, display, add value and create derivative works, for lawful
    commercial and non-commercial purposes (section 3)
  - attribution with DOI, URL or URI; a separate attribution page for multiple
    data; non-endorsement; no warranty; continuity of provision (section 4)
  - the attribution template (section 5)
  - exemptions (section 6): personal information; data the provider is not
    authorized to license; names, crests, logos and official symbols; data under
    other IP rights; military insignia; identity documents; data that should not
    have been disclosed under RTI Act section 8
  - termination on breach, reinstated if cured within 30 days; the provider may
    terminate the licence for a data set found to include section 6 data (section
    7)
- **Unchanged since 2026-10-02.** The licence text extracted from R47 is
  identical to the text extracted from the copy of the then-current route script
  saved on 2026-10-02 (`542bb31.js`, local saved copy). That script is still
  served unchanged.
- **Resource level (C1–C3).** The resource and catalog metadata keys (R48)
  include no licence field of any name [PUBD]. The licence basis for C1–C3 is
  therefore the site-wide footer statement, as ADR-0002 found for its own
  data.gov.in resources. The resources show `is_priced` 0 and `field_public` 1
  [PUBD, R48]. The second pass's "Released Under: NDSAP" on the catalog pages
  (R26, R27) names the National Data Sharing and Accessibility Policy. The
  licence's preamble presents GODL-India as the open licence for data sets
  published under that policy [PUBD, R47]. No other licence is named for C1–C3.

### Effect on the second pass

- The second pass's sandbox question (Licence findings, (iii)) is answered: the
  notice is hidden on `www.data.gov.in` and shown only on `sandbox.data.gov.in`.
  It does not affect the ADR-0002 basis.
- The current evidence for C1–C3 is a site-wide GODL-India statement on the
  non-sandbox host with an unchanged licence text, and no resource-level
  licence. This is licence evidence, **not source acceptance**.
- Still open for C1–C3 after this pass:
  - C1b's data file is hosted at `info.nhp.gov.in`. Whether that host's terms
    differ from data.gov.in's [U]. (Fourth pass: still [U]; see there.)
  - The GODL-India exemptions (section 6) exclude personal information and
    identity documents from the licence. That bears on C1a's `Nodal_Person_*`
    and contact fields, which the record-level screen and context-column rules
    already exclude.
  - Terms of use and automated retrieval (E5), header rows, G4 and the source
    ADR itself.

  The first and third of these were taken up by the fourth pass (next section).

## Terms of use and retrieval conditions (fourth pass, 2026-10-06)

Evidence status only. **No source is accepted, rejected or selected**, and no
manifest is written. This pass covers C1a, C1b, C2 and C3 only. It addresses the
third pass's open items on `info.nhp.gov.in` and on terms of use and automated
retrieval (E5). C4–C6 were not revisited.

### Method

- Pages, `robots.txt`, site scripts and metadata APIs were retrieved with `curl`
  on 2026-10-06 between 14:48 and 15:05 UTC, and the saved responses were read
  directly [PUBD]. The saved responses are in a scratch directory outside the
  repository and are not committed.
- data.gov.in renders most page text in the browser. Where the text was not in
  the server-rendered HTML, it was read from the route script that carries it,
  as in the third pass.
- **Response headers only for file URLs.** HTTP `HEAD` requests, which return
  headers and no body, were sent to the C1a, C2 and C3 file URLs on
  `www.data.gov.in`, and to C1a's legacy `data.gov.in` path. No `GET` was sent
  to any data-file URL, and no data file was downloaded or opened. The C3
  `datafile_url` (an `api.data.gov.in` data query) was not requested.
- `info.nhp.gov.in` and `nhp.gov.in` could not be reached (below). For the
  National Health Portal's terms, one Internet Archive copy of a publisher page
  was read. New label: **[ARCH]** = Internet Archive copy of a publisher page,
  retrieved directly and inspected. It shows the page as captured on that date,
  not the current terms, and is not a publisher retrieval.
- **Disclosure.** `www.data.gov.in/robots.txt` (R49) disallows all paths for all
  user agents. The second and third passes record no robots-exclusion check.
  Those passes and this one made a small number of scripted requests, for
  metadata, pages and scripts, to paths it covers.

### Sources for this pass

| # | URL | Kind | SHA-256 of saved response | Supports |
|---|---|---|---|---|
| R49 | https://www.data.gov.in/robots.txt (`https://data.gov.in/robots.txt` redirects here) | [PUBD] | `efdb5938a9736727f5cce2b60355588e4fa541d19d022d222d8a09b8efd5dcce` | Robots exclusion |
| R50 | https://www.data.gov.in/terms-of-use | [PUBD] | `cf4a7695928d418aaef2bd3aaf65f0e7b8b7ec53f380187e85de359af686adb1` | Terms of Use, server-rendered |
| R51 | https://www.data.gov.in/_nuxt/92f8eeb.js | [PUBD] | `562f14cbc4f2c0ab5cda0d560f6afbb9bcf82ac115a2bf617ccb98bf7480074b` | Terms of Use component source |
| R52 | https://www.data.gov.in/policies | [PUBD] | `0e1ef1afd34980873c056e859b0350e13666f0a7a5e0809f3f958b0c1bf7d500` | Hyperlinking, Copyright and Privacy policies, server-rendered |
| R53 | https://www.data.gov.in/help and https://www.data.gov.in/apis/ | [PUBD] | `a98c3590235a006d3ffcf1c52385a9bf08d850aabaf003fcc23ee9cfb6b1bfb4` (help); `3db255c151fa290dbab416ce05aaa7738d1e0b183aeb03e4e3e344262eea8774` (apis) | API key for registered users |
| R54 | https://www.data.gov.in/_nuxt/d96b352.js and https://www.data.gov.in/_nuxt/6f8a3d9.js, loaded by the C2 resource page https://www.data.gov.in/resource/all-india-health-centres-directory-7th-october-2016 and its catalog page | [PUBD] | `ba21f2c841c3e6e6df34090c360086f942f7efb3501db6b4728ad1b1b72c022a` (d96b352); `e0b7500449581c51b2ea6525efa35df6a803d46b8c7292d78e01174578909077` (6f8a3d9); resource page `ba28bf6eaa5fb8236d9fa18c7207f34ce45d800954ee973d941037d6009684ba` | Download form and CAPTCHA |
| R55 | The R29, R30 and R31 resource queries, re-retrieved | [PUBD] | `1450e9c8b5e4d391a2cbbc924833e1b0fc8f218146456f7b193004768dfe92ab` (C1); `37a900a4d8b3d3281300b42ade38a3181eb040d93a877f39b051c17d80d77d52` (C2); `0ab5f8139b12c498267bc4c697ed1f295f4a902c04ede009a664aa014e428547` (C3) | File locations per resource |
| R56 | `HEAD` requests to the C1a, C2 and C3 file-store URLs on `www.data.gov.in`, and to C1a's legacy `data.gov.in` path (followed through its redirect), listed under "Retrieval conditions" | [PUBD] | headers only, not saved | File-URL response to a scripted request |
| R57 | Connection attempts: `api.data.gov.in`, `info.nhp.gov.in`, `nhp.gov.in`, `www.nhp.gov.in` | [PUBD] | none | Reachability from the development machine |
| R58 | https://web.archive.org/web/20230404002716/https://www.nhp.gov.in/terms-of-use_pg (raw capture) | [ARCH] | `7fd841fce7e81bae09f2be7ce9b8a3d41b0dd8f268476c3f8a80f075406a6275` | National Health Portal terms of use, as captured 2023-04-04 |
| R59 | https://web.archive.org/cdx/search/cdx?url=info.nhp.gov.in&matchType=host | [ARCH] | not saved | Index of archived `info.nhp.gov.in` URLs; no capture opened |

### File locations (C1–C3)

From the resource metadata (R55) [PUBD]:

| Row | `datafile` (file on data.gov.in) | `datafile_url` | `reference_url` |
|---|---|---|---|
| C1a | `https://www.data.gov.in/files/ogdpv2dms/s3fs-public/datafile/hospital_directory.csv` | `https://data.gov.in/sites/default/files/datafile/hospital_directory.csv` | `http://www.nhp.gov.in/` |
| C1b | **none** | `https://info.nhp.gov.in/api/nin-health-facilities.csv` | none |
| C2 | `https://www.data.gov.in/files/ogdpv2dms/s3fs-public/dataurl14092017/geocode_health_centre.csv` | `http://data.gov.in/sites/default/files/dataurl14092017/geocode_health_centre.csv` | none |
| C3 | `https://www.data.gov.in/files/ogdpv2dms/s3fs-public/datafile/2_empanelledHospitals_1.csv` | an `api.data.gov.in/resource/de59e770-…` query that embeds an `api-key` parameter (value not recorded here) | none |

So C1a, C2 and C3 each have a file on data.gov.in's own file store. **C1b has
none**: its only listed file is on `info.nhp.gov.in`.

### Terms and policies: data.gov.in (C1a, C1b, C2, C3)

- **Terms of Use (R50, R51)** [PUBD]. The server-rendered page states, in
  substance:
  - the portal is designed, developed and hosted by NIC;
  - no responsibility for accuracy or completeness, and no liability for loss
    from use of data;
  - "Catalog and Links to other websites that have been published through the
    OGD Platform are provided for public convenience only", and the portal is
    not responsible for linked websites;
  - catalogs, "if reproduced, have to be accurate and are not to be used in a
    derogatory manner or in a misleading context"; the source "must be
    prominently acknowledged"; the permission to reproduce does not extend to
    material identified as third-party copyright;
  - Indian law and the courts of India govern;
  - "The catalog and information available through the Portal are available
    under terms described in the “license” metadata element of individual
    dataset records except where otherwise noted."

  **The Terms of Use say nothing about automated access, crawling, rate limits
  or bulk download.** They contain no clause restricting research use.
- **Licence pointer.** The Terms of Use defer to a per-record "license"
  metadata element. The C1–C3 resource and catalog metadata have no licence
  field (third pass, R48; unchanged in R55). The site-wide footer names
  GODL-India (third pass). Whether the footer is the "otherwise noted" case is a
  reading, not a statement made by the site. The ADR-0002 basis is not changed
  by this pass.
- **Copyright Policy (R52)** [PUBD]: "Material featured on this Portal may be
  reproduced free of charge after taking proper permission by sending a mail to
  us." The same accuracy, acknowledgement and third-party conditions follow.
  - This wording asks for permission. GODL-India grants permission without a
    request. The footer reads "All rights reserved except published
    datasets/resources and metadata."
  - The policy does not say whether "material" includes published datasets.
    **This tension is unresolved here.** It is recorded, not settled. It does
    not withdraw the ADR-0002 basis. It is a question for the maintainer or for
    data.gov.in.
- **Hyperlinking Policy (R52)** [PUBD]: direct links need no prior permission,
  though the portal asks to be informed. Framing is not permitted.
- **Privacy Policy (R52)** [PUBD]: the portal logs IP address, browser, date,
  time and pages visited for statistical purposes.

### Retrieval conditions: data.gov.in (technical, not licence terms)

These are technical access conditions. **None of them is stated as a licence
term or as a condition of the licence.** A file that is hard to retrieve by
script may still be licensed for reuse.

- **`robots.txt` (R49)** [PUBD]: `User-agent: *` / `Disallow: /`. It asks all
  automated crawlers to stay off every path. It is a machine-readable request,
  not a term in the Terms of Use, which are silent on automated access.
- **Download form (R54)** [PUBD]. The resource page's download component asks
  for:
  - name and e-mail (marked required); mobile is optional, judged by its
    validation rules (format and length only);
  - a usage type and a purpose (both required). The option labels in the
    component are Commercial, Non Commercial, Academia, Business, Govt Use,
    Journalistic, R&D and Other. Which labels belong to which field was not
    traced.
  - an image CAPTCHA, requested from `ogdp/captcha/refresh/image/download_purpose`
    when the component mounts.

  The form is posted to `/ogdp/download_purpose`, and the download URL comes
  back in the response. This is consistent with ADR-0004's record of a CAPTCHA
  on the download form (2026-10-03).
- **API (R53)** [PUBD]: the help page lists "API Key generation and access of
  API URLs using API Key" as a service for registered users. `api.data.gov.in`
  refused a TCP connection on port 443 on 2026-10-06 (R57), as ADR-0004
  recorded on 2026-10-03.
- **File URLs, `HEAD` only (R56)** [PUBD], 2026-10-06 14:53 UTC, browser-style
  user agent:
  - the `www.data.gov.in/files/ogdpv2dms/…` file-store URLs for C1a, C2 and C3:
    `405 Method Not Allowed`;
  - C1a's `datafile_url` on `data.gov.in`: `301` to
    `https://www.data.gov.in/sites/default/files/datafile/hospital_directory.csv`,
    which answered `200 OK`, `Content-Type: text/csv`.
- **What the `HEAD` results do and do not show.**
  - They show that a scripted `HEAD` request for C1a's legacy file path got
    `200` with a CSV content type, not a challenge or error status, on that
    date.
  - They do not show what a `GET` would return, so they neither confirm nor
    contradict ADR-0004's record of an Akamai bot challenge on file URLs and
    ADR-0002's "HTTP 403/301 to scripted requests".
  - The header lines inspected (status, `Server`, `Location`, content type and
    length, `X-*`, `Set-Cookie`) named no CDN or bot-management product; most
    were absent.
  - A `405` to `HEAD` says nothing about `GET`.
- **First-pass 403s.** The first pass's fetch tool got 403 from data.gov.in
  pages (R13–R15), which `curl` retrieved with 200 in the second to fourth
  passes. The cause of the difference was not determined.

### `info.nhp.gov.in` and the National Health Portal (C1b)

- **Host relationship, as evidenced.**
  - data.gov.in lists C1b under the catalog "Hospital Directory (National
    Health Portal)", contributed by MoHFW / DoHFW / NIHFW (R26, R29) [PUBD]. Its
    only file location is `https://info.nhp.gov.in/api/nin-health-facilities.csv`
    (R55) [PUBD].
  - C1a's `reference_url` is `http://www.nhp.gov.in/` (R55) [PUBD].
  - The archived National Health Portal terms (R58) [ARCH] say the portal "is
    designed, developed and hosted by Centre for Health Informatics (CHI) of the
    National Health Portal (NHP), set up at National Institute of Health and
    Family Welfare (NIHFW), by the Ministry of Health and Family Welfare
    (MoHFW)". This is from `www.nhp.gov.in`, captured 2023-04-04, with a page
    date of 30 April 2015.
  - `info.nhp.gov.in` is a subdomain of `nhp.gov.in`. **That it is operated by
    CHI/NIHFW under the same terms is an inference from the domain name, not a
    finding [U].**
- **Reachability (R57)**, 2026-10-06 from the development machine [PUBD]:
  - `info.nhp.gov.in` resolves to 117.239.178.13; TCP connections to ports 80
    and 443 timed out (attempts at 14:48 and 14:58 UTC);
  - `nhp.gov.in` resolves to 172.239.183.210; connections to ports 80 and 443
    failed;
  - `www.nhp.gov.in` did not resolve.

  No current terms, policy page or `robots.txt` could be obtained from these
  hosts. Whether they are down, decommissioned or blocked for this network is
  unknown [U].
- **Archived National Health Portal terms (R58)** [ARCH], `www.nhp.gov.in`,
  captured 2023-04-04. In substance:
  - "All the copyright of NHP belongs to the Ministry of Health and Family
    Welfare, Government of India and will be governed by their guidelines, as
    issued from time to time."
  - "The site is meant for individual and professional use only"; "This is a
    non-commercial web-site funded by MoHFW".
  - Linking without prior permission is allowed; framing is not.
  - Footer: "© 2016 MoHFW, Government of India, All rights reserved."
  - **No reuse licence, no redistribution permission, and nothing on automated
    access.**

  These are the 2023 terms of `www.nhp.gov.in`. Whether they applied to
  `info.nhp.gov.in`, and whether they are current, is [U].
- **Archive index (R59)** [ARCH]. It lists captures of
  `info.nhp.gov.in/api/nin-health-facilities.csv` (2019) and
  `info.nhp.gov.in/api/hospital-directory.csv` (2021). **Neither capture was
  opened.** The index shows only that the URLs existed then.

### Findings per row

Licence (legal permission) and retrieval (technical access) are kept apart.

- **C1a.**
  - *Licence:* unchanged. Site-wide GODL-India statement, no resource-level
    licence (third pass). The Copyright Policy tension above applies.
  - *Terms:* the data.gov.in Terms of Use (R50) apply as for any data.gov.in
    resource; they are silent on automated retrieval.
  - *Retrieval:* the file is on data.gov.in's own store. `robots.txt`
    disallows crawling; the download form needs a CAPTCHA. A scripted `HEAD`
    to the legacy path got `200 text/csv` (R56); `GET` untested.
  - *Linked site:* `reference_url` points to `www.nhp.gov.in`, unreachable on
    2026-10-06.
- **C1b.**
  - *Licence:* **unresolved [U].** The data.gov.in footer licenses "the content
    published on data.gov.in". C1b's file is not on data.gov.in: its only
    location is `info.nhp.gov.in`. The Terms of Use treat "Links to other
    websites" published through the platform as provided for convenience only.
    Whether GODL-India reaches a file hosted elsewhere is not stated anywhere
    inspected. The only National Health Portal terms found (R58, archived, a
    different subdomain) reserve all rights, grant no reuse licence and
    describe the site as for individual and professional, non-commercial use.
  - *Terms of the file host:* not obtainable; host unreachable [U].
  - *Retrieval:* the host accepted no connections on 2026-10-06, so nothing
    could be retrieved from it from this machine then. The file URL itself was
    not requested. That is a technical fact, not evidence about permission.
- **C2.**
  - *Licence:* as C1a.
  - *Terms:* as C1a.
  - *Retrieval:* the file is on data.gov.in's own store; `HEAD` got `405`; same
    `robots.txt` and form conditions.
- **C3.**
  - *Licence:* as C1a.
  - *Terms:* as C1a.
  - *Retrieval:* the file is on data.gov.in's own store (`HEAD`: `405`). Its
    `datafile_url` is an `api.data.gov.in` query, and that host refused
    connections. Same `robots.txt` and form conditions.

### Effect on the open items

- **Third pass, "`info.nhp.gov.in` terms":** not resolved. The host is
  unreachable. The only terms found are archived and from a sibling host, and
  they reserve rights. C1b's licence basis is now **unresolved**, not "as C1a".
- **Third pass, "terms of use and automated retrieval (E5)", data.gov.in:** the
  evidence is gathered.
  - The Terms of Use are silent on automated retrieval.
  - `robots.txt` disallows all crawling.
  - Downloads go through a form with an image CAPTCHA.
  - Under ADR-0007 §5, where the terms are silent, retrieval is manual. Which
    method applies is recorded in a source ADR, not here.
- **New, unresolved:** the data.gov.in Copyright Policy's "after taking proper
  permission" wording against the GODL-India footer (R52).
- **Not addressed in this pass:** C4's licence text and the Telangana portal's
  retrieval terms; header rows; G4.

## B6 aggregate and schema inspection (fifth pass, 2026-10-06)

Evidence status only. **No source is accepted, rejected or selected**, no state
is selected, and no manifest or selection record is written. This pass collects
the schema and aggregate evidence that can be had now without reading records.
It is structural evidence. It says nothing about licences or terms, which stay
as the earlier passes left them (B14, B15 and C4's B3/B8 open).

### Method

- **No new retrieval.** Every finding below comes from responses already saved
  by the second pass (2026-10-04) and the fourth pass (2026-10-06), re-read
  offline on 2026-10-06. No request was sent to any publisher or platform.
- **No record content.** The saved responses are metadata: platform field
  lists, resource and dataset metadata, and a datastore schema query that
  returned a count and no rows (`limit=0`, `results=false`). The data.gov.in
  field-list responses contain an array named `records`. Its entries are API
  descriptors, one per resource, holding field lists, not data rows.
- **No local candidate file.** `data/raw/data.gov.in/` is empty, and no C1–C6
  file exists elsewhere in `data/`. So no header row was read, and no column
  statistic was computed from a file.
- **Why nothing new was retrieved.**
  - data.gov.in: the Terms of Use are silent on automated access, so under
    ADR-0007 §5 retrieval points to manual (fourth pass). Separately, as
    technical conditions, `robots.txt` disallows all paths and downloads go
    through a form with a CAPTCHA.
  - C1b: `info.nhp.gov.in` was unreachable (fourth pass).
  - C4: the Telangana portal's retrieval terms (B8) have not been checked, so
    its datastore API was not queried again for column statistics. Whether it
    supports such queries was not checked [U].
  - C5, C6: no licence and no bulk mechanism was found.
- **No per-state counts.** Under ADR-0007 §4 step 3, record counts per source
  and per step-1 state come from accepted source files, in selection records.
  None were computed.
- New label: none. [PUBD] marks the saved publisher or platform responses;
  [CALC] marks counts derived here from those responses (field counts and type
  tallies), never from records.

### Saved responses re-read

The second pass did not record hashes. These are the hashes of the local saved
copies re-read in this pass.

| Ref | Saved response | Retrieved | SHA-256 of local saved copy |
|---|---|---|---|
| R32 | data.gov.in field lists, catalog "Hospital Directory (National Health Portal)" | 2026-10-04 | `6308ca533937b70a1a44cd13ddb5f42d32a6552af2309f25e4e31db592f8e50d` |
| R33 | data.gov.in field list, catalog "All India Health Centres Directory" | 2026-10-04 | `14e90785c995c5959175bca1ba08711d5caf6760bc1cfd1915b4d01d6f43db71` |
| R34 | data.gov.in field lists, catalog "Central Government Health Scheme" | 2026-10-04 | `7cdce8aaa44e9a85f833b96540d9b96be808534433781ec63b408d48dc986d57` |
| R36 | Telangana portal dataset metadata (C4) | 2026-10-04 | `602efd63ba4748f10f121b3de88e934e7d9ed25d24d48beac54bc53b3a1f2a2e` |
| R37 | Telangana datastore schema and count query (C4) | 2026-10-04 | `91f6ca720803446017cbfbc98f1dd2a790bdde03d179fa2d0fed7145ab690dc6` |
| R55 | data.gov.in resource metadata, C1–C3 | 2026-10-06 | as listed under the fourth pass |

### Aggregate and schema findings per source

| Row | Publisher fields; platform type tally [CALC from PUBD] | Row count | Declared coverage; state field | Address fields | Missing-value convention | File structure |
|---|---|---|---|---|---|---|
| C1a | 48 (the platform list has 50, adding `document_id` and `resource_uuid`); 32 `keyword`, 16 `double` [R32] | **[U]**: no row count in resource metadata (R55), field lists (R32) or pages seen | "All India" from the first-pass mirror only [MIR, R1]; `State` field; no `lgd:state:` mapping | `Address_Original_First_Line` plus components `Location`, `Town`, `Subtown`, `Village`, `State`, `District`, `Subdistrict`, `Pincode` [R32] | Note: "NA/Blank: Not Available" [PUBD, R55] | CSV, 10,341,256 bytes, on data.gov.in's file store [PUBD, R55] |
| C1b | 16 (platform 18); 10 `keyword`, 5 `double`, 1 `text` [R32] | **[U]** | As C1a [MIR, R1]; `State_Name` field | `Address` plus `street`, `landmark`, `locality`, `pincode`, `State_Name`, `District_Name`, `Taluka_Name`, `Block_Name` [R32] | Note: "NA/Blank: Not Available"; "NIN: National Identification Number" [PUBD, R55] | CSV, 26,644,508 bytes, hosted only at `info.nhp.gov.in` [PUBD, R55] |
| C2 | 13 (platform 15); 12 `keyword`, 1 `double` [R33] | **[U]** | "All India" from the first-pass mirror only [MIR, R2]; `State Name` field | `Facility Address` plus `State Name`, `District Name`, `Subdistrict Name` [R33] | Note: "NA: Not Available" [PUBD, R55] | CSV, 20,967,450 bytes, on data.gov.in's file store [PUBD, R55] |
| C3 | 3 (platform 3; no `document_id` or `resource_uuid`); 3 `keyword` [R34] | **[U]** | CGHS cities, not listed [U]; **no state field** | `DiagnosticCentreAddress`; `CityName` only as a component [R34] | Note: "NA: Not Available." [PUBD, R55] | CSV, 80,196 bytes, on data.gov.in's file store; metadata flag `field_from_api` is 1, meaning not documented [PUBD, R55] |
| C4 | 13; all `text` in the datastore [R37] | **7,001**, the platform datastore's count (source-reported, not a file row count) [PUBD, R37] | Telangana (dataset title); `State` field; `lgd:state:36` mapping not made here | No single address string; components `Street`, `Landmark`, `Locality`, `Taluka`, `District`, `State` [R37] | Not documented [U] | One CSV distribution; no checksum given (`checksum` null) [PUBD, R36] |
| C5 | **[U]**: lists are PDFs, not opened | [U] | Tamil Nadu per constituency [SRCH]; statewide [U] | [U] | [U] | PDFs per constituency [SRCH, R21] |
| C6 | **[U]**: search form, no static schema | [U]; the homepage counter of 1,367 schools (1,364 in India [CALC]) counts institutions, not rows of any file | All India [PUB, R10]; state filter in the search form [PUBD, R43] | [U] | [U] | Search form; no bulk file found [PUBD, R43] |

Field counts and type tallies are counted here from the platform's field lists
[CALC]. They match the field names recorded in the second pass (48 for C1a, 16
for C1b).

### Observations from the platform field types

These are types assigned by the platform's search index. How the platform
assigns them is not documented, so **what a type implies about the values is
[U].** They are recorded as signals for a later aggregate script to check, not
as findings about the data.

- **C1a.** The 16 `double` fields include two address components, `subtown`
  and `village`, and also `hospital_regis_number`, `registeration_number_scan`,
  `accreditation`, `miscellaneous_facilities`, `empanelment_or_collaboration_with`
  and `tariff_range`. Fields named as text being typed numeric may mean they hold
  only numbers or no values, but that is not established. In the May-2016
  snapshot's index in the same catalog, the matching `_subtown`, `_village` and
  `_hospital_regis_number` are `keyword` [PUBD, R32].
- **C1b.** `pincode`, `latitude`, `longitude` and `altitude` are `double`;
  `street` is `text`; `Address` is `keyword` [PUBD, R32].
- **C2.** Only `nin_n` is `double`; `_latitude` and `_longitude` are `keyword`
  [PUBD, R33].
- **C3.** Its index has no `document_id` or `resource_uuid`, unlike C1 and C2.
  So the second pass's note that data.gov.in adds those two fields does not
  hold for C3 [PUBD, R34].
- **C4.** All 13 datastore columns are `text`. The datastore description of
  `state` begins with a byte-order mark (U+FEFF). That suggests the uploaded
  CSV's header starts with a UTF-8 byte-order mark; the file itself has not
  been seen, so this is an inference [PUBD, R37].

### Corrections and other metadata

- **C3 field names (corrects the second pass).** The hospital resource's fields
  are `DiagnosticCentreName`, `DiagnosticCentreAddress`, `CityName`. The
  diagnostics-centre resource in the same catalog has `DiagnosticCenterAddr`,
  `DiagnosticCenterName`, `CityName` [PUBD, R34]. Both use a diagnostic-centre
  prefix, but the names are spelt differently, so they are not "the same". Whether
  the hospital resource is mislabelled stays [U].
- **C4 dataset metadata** [PUBD, R36]: `accrualPeriodicity` is the code "3",
  whose meaning the response does not give [U]; `granularity` "Area level";
  `geospatial` "Yes"; `accessLevel` "public". The first pass's "annual" came
  from the mirror [MIR, R4] and is not confirmed by this code.
- **data.gov.in counts that are not row counts.** The field-list responses'
  `total` and `count` (6, 1 and 6 for R32, R33 and R34) count API descriptors in
  each catalog, not rows. The resource metadata's `download_count` and
  `view_count` count downloads and views.

### What B6 does not establish

- No header row of any downloaded file (G3 stands).
- No row count for C1a, C1b, C2, C3, C5 or C6. C4's 7,001 is a platform count,
  not a count of rows in the downloadable file.
- No empty-value or missing-value rate for any column of any source.
- No value distribution, token count or address completeness (G2 stands).
- No per-state or per-source record counts (ADR-0007 §4 step 3; G7 stands).
- No language or script evidence (G8 stands).
- Nothing on whether values contain people's names, phone numbers or emails
  beyond what the field names already show.
- Nothing on identifier stability (`Hospital_Regis_Number`, `Nin_N`).
- Nothing about licences, terms or permission to retrieve.

### Still unresolved after this pass

- File-level aggregate statistics for every source. They need a file obtained
  through a permitted route, then a script that prints only the header row, row
  count, per-column empty rates and value-shape statistics.
  - data.gov.in (C1a, C2, C3): manual download through the site's form, a
    maintainer action. B14 stays open.
  - C1b: the host must be reachable first, and B15 stays open.
  - C4: B3 and B8 first; a datastore query for column statistics is an option
    only if the datastore supports it [U] and the portal's terms allow it.
  - C5, C6: no route without a licence decision (B4).
- What the platform's `double` typing of C1a's `subtown`, `village` and
  `hospital_regis_number` means.
- The meaning of C4's `accrualPeriodicity` code "3". (Sixth pass: answered;
  see "C4 licence and retrieval terms".)
- Whether C3's hospital resource is mislabelled.

## C4 licence and retrieval terms (sixth pass, 2026-10-06)

Evidence status only. **C4 is not accepted or rejected**, Telangana is not
selected, and no manifest or selection record is written. This pass covers C4
only: the licence text behind its label (B3) and the Telangana portal's
retrieval terms (B8). No dataset file was downloaded, no datastore query was
run, and no record was read.

### Method

- Portal pages, the dataset metadata, the portal's metadata schema, its content
  pages and `robots.txt` were retrieved with `curl` on 2026-10-06 between 15:55
  and 16:03 UTC, and read directly [PUBD].
- The portal is a single-page application. Its route list, footer and metadata
  display were read from its main script. The copy saved on 2026-10-04 was read
  offline, and the copy served on 2026-10-06 is byte-identical to it.
- Content pages outside the coded routes are looked up through
  `/local-path?alias=…`. Twenty likely aliases were probed, such as
  `/terms-of-use`, `/copyright-policy`, `/license` and `/open-data-policy`.
  Each lookup returns a small JSON object naming a page or echoing the alias.
- The Telangana State Open Data Policy 2016 was downloaded from the ITE&C
  Department site. It is a scanned PDF with no text layer. Its pages were
  read as images, and the quotations below are transcribed from them.
- Third-party commentary on the 2016 draft policy turned up in a web search
  (CIS, DataMeet). It is not used as evidence.

### Sources for this pass

| # | URL | Kind | SHA-256 of saved response | Supports |
|---|---|---|---|---|
| R60 | https://data.telangana.gov.in/robots.txt | [PUBD] | `bceb8401bd93df40acb8dc657648f9557bc0ee3f07ebc1717ac7780511a41df8` | Robots exclusion |
| R61 | https://data.telangana.gov.in/api/1/metastore/schemas/dataset/items/44935575-631b-4116-b278-41f4c507b95b | [PUBD] | `e112a96fdcbf0e14788075e5512ccac507e000a2c4d39ef7a03e535ce1eed9dd` | C4 licence value, 2026-10-06 |
| R62 | https://data.telangana.gov.in/api/1/metastore/schemas/dataset | [PUBD] | `ae61dcb077cbfc23ffea19c9583608f2b4beed0d1d6ce35e62d4eb47778878d7` | Definition of the portal's `license` field |
| R63 | https://data.telangana.gov.in/frontend/build/static/js/main.8f3435a2.chunk.js, loaded by https://data.telangana.gov.in/ | [PUBD] | `0a28865933e5da46c285bd1e06ea36e6cdb732f363ca3706ce7cc94280a20e2c` (homepage `c3196b483b6d0cec610fb350eb78a85720188257dd87deca8487083b58ca5093`) | Routes, footer, licence display, periodicity codes |
| R64 | https://data.telangana.gov.in/local-path?alias=… (20 aliases) | [PUBD] | not saved | Which content pages exist |
| R65 | https://data.telangana.gov.in/node/2258?_format=json (alias `/policies`) | [PUBD] | `7f9cab1c21cd432367e2ed237559064c13176e017f409b2d3d9a5df8658d380e` | Hyperlinking, Privacy and Copyright policies |
| R66 | https://data.telangana.gov.in/node/2257?_format=json (alias `/contact-us`) | [PUBD] | `ae944c5c9eb21a27dd7f8b5ed5857dd24dc0c14d3dcc4e553c0fbadaede9b0ab` | Contact for clarifications |
| R67 | https://it.telangana.gov.in/initiatives/open-data/ | [PUBD] | `908de29aff860e0918ad53d2cb0a6fb25d295a15f68bdf640ace776874d20ddf` | ITE&C Department open-data page; link to the policy |
| R68 | https://it.telangana.gov.in/wp-content/uploads/2016/10/Telangana-Open-Data-Policy1.pdf | [PUBD] | `5143e676152a4d981dfe802ed37a5ad3df753b000a054435f2430e123804dd54` | Telangana State Open Data Policy 2016 |
| R69 | https://data.telangana.gov.in/api/1 | [PUBD] | none | API documentation: **not obtained**, timed out twice with no bytes received |

### Licence findings (B3)

- **Dataset licence value (R61)** [PUBD]: `license` is "Government Open Data
  License - India". This is unchanged from 2026-10-04 (R36); the two saved
  copies differ only in how they are serialized. There is no `rights` field,
  and no licence URL or text.
- **What the field is (R62)** [PUBD]. The portal's metadata schema defines
  `license` as a free-text string. Its description points to a US federal page
  of open licences, which is the platform's default wording. The schema does
  not tie the value to any licence text.
- **How the portal shows it (R63)** [PUBD]: as a plain "License" row in the
  dataset's metadata table. There is no link.
- **No licence page and no Terms of Use found (R63, R64)** [PUBD].
  - The coded routes are `/`, `/about`, `/publishers`, `/search`, `/api`, the
    dataset and collection pages, `/featured/…` and `/frontend/login`.
  - Of the 20 aliases probed, only `/policies` and `/contact-us` resolve to a
    page. No licence, terms-of-use, copyright, disclaimer or open-data-policy
    page exists under those names.
  - The `/about` route shows the platform's placeholder text ("This is the
    default state of the DKAN data catalog. … Update this about page before
    publishing.").
- **Copyright Policy (R65)** [PUBD]. The Policies page (created 2022-05-21)
  says: "Material featured on this Portal may be reproduced free of charge
  after taking proper permission by sending a mail to us." Accuracy,
  non-derogatory use, prominent acknowledgement and a third-party exclusion
  follow, under Indian law. **The page does not mention GODL-India or any other
  licence.**
- **Footer (R63)** [PUBD]: "© Copyright @ {year}. Open Data Unit, Information
  Technology, Electronics & Communication Department (IT E&C), Government Of
  Telangana. All rights reserved." Unlike the data.gov.in footer, it has **no
  exception for published datasets** and names no licence.
- **State policy (R68)** [PUBD]. The Telangana State Open Data Policy 2016
  applies to public authorities within the state.
  - Its preamble aims to share data "under open license".
  - §8 says GoI e-governance initiatives will be adopted, "including but not
    limited to Adoption of Open Source Software, Open APIs, Open Standards &
    Open Data Use License".
  - Its definition of metadata says it "will also include license type".
  - §9 promises detailed implementation guidelines within six months. Whether
    they were issued, and what they say, is [U].
  - **The policy names no licence and contains no licence text.** It does not
    say that "Open Data Use License" means GODL-India.
- **ITE&C open-data page (R67)** [PUBD]: gives a general definition of open
  data ("freely used, reused and redistributed – subject only, at the most, to
  the requirement of attribution"). It is a description, not a licence grant
  for any dataset.
- **Contact (R66)** [PUBD]: clarifications about datasets go to the Open Data
  Unit, Department of ITE&C, at opendata[at]telangana[dot]gov[dot]in.

**What this establishes about B3.**
- The label is the only licence statement attached to C4. The portal, the
  department and the state policy were searched, and no linked or published
  licence text was found.
- The portal's own Copyright Policy asks for permission by mail, and its footer
  reserves all rights without exception.
- Whether the label means the GODL-India instrument verified on data.gov.in
  (third pass, R47) is **not stated by any Telangana source** [U]. Whether that
  label prevails over the portal's Copyright Policy and footer is also [U].
- B3 therefore stays **open**, now with a documented conflict (B16 in the
  evaluation notes). This pass does not infer permission from the label.

### Retrieval findings (B8)

These are terms and technical conditions. They say nothing about the licence.

- **Terms:** no Terms of Use page was found (R64). The Policies page (R65)
  covers hyperlinking, links out, privacy, copyright and blogs. **It is silent
  on automated access, the API, bulk download and rate limits.**
  - Its Hyperlinking Policy allows direct links without prior permission,
    asks to be informed, and does not permit framing.
  - Under ADR-0007 §5, silent terms point to manual retrieval. Which method
    applies is recorded in a source ADR, not here.
- **Technical conditions (not terms):**
  - `robots.txt` (R60) disallows only `/search` for all user agents. It names
    `/sitemap.xml`, which returned 404.
  - The portal publishes an API under `/api/1`, which the second pass used for
    metadata (R35–R37). Its documentation endpoint (R69) did not respond on
    2026-10-06.
  - The dataset lists one CSV file under `/sites/default/files/`. It was not
    requested.
- The 2016 policy's commitment to open APIs (§6.6, for real-time data) is a
  policy aim, not a term of use.

### Other corrections and facts

- **C4 periodicity (answers a B6 open item).** The portal's display script maps
  `accrualPeriodicity` codes to labels, and code 3 is "Annually" (R63). That
  agrees with the first pass's "annual" from the mirror [MIR, R4]. The fifth
  pass's "meaning [U]" is superseded.
- **Publisher identity.** The footer and contact page name the Open Data Unit,
  Department of ITE&C, as the portal's operator (R63, R66). The dataset's
  publisher remains "Health and Medical and Family Welfare" (R61). The portal
  operator and the dataset publisher are named differently; how they relate,
  and G4, stay open.

### Effect on the open items

- **B3 (C4 licence text): not resolved.** No licence text was found on the
  portal. The label is free text. The portal's Copyright Policy and footer
  point the other way. **New: B16**, the C4 label against the portal's
  Copyright Policy and footer. Like B14, it is for the maintainer or the
  publisher to clarify; the Open Data Unit contact (R66) is the documented
  route.
- **B8 (Telangana portal): evidence gathered.** The terms are silent on
  automated retrieval, and `robots.txt` excludes only `/search`. That is not
  permission for automated retrieval.
- **Unchanged:** the C4 schema and the 7,001 platform count (fifth pass), G2 (no
  single address string), G4, and the absence of a header row.

## B14 and B15 follow-up (seventh pass, 2026-10-06)

Evidence status only. **No source is accepted, rejected or selected**, and no
manifest is written. This pass covers B14 (the data.gov.in Copyright Policy
against GODL-India, for C1a, C2 and C3) and B15 (C1b's file host
`info.nhp.gov.in`). C4 was not revisited. No dataset file was requested and no
record was read.

### Method

- Pages and official PDFs were retrieved with `curl` on 2026-10-06 between
  16:27 and 16:32 UTC and read directly [PUBD]. A saved fourth-pass site
  script was re-read offline.
- The two data.gov.in PDFs are policy documents linked from the portal's
  Policies page. They sit under a path that the portal's `robots.txt` disallows
  (fourth pass, R49); two requests were made, one per document.
- A web search was used only to find NIHFW's official site. Search results are
  not used as evidence.

### Sources for this pass

| # | URL | Kind | SHA-256 of saved response | Supports |
|---|---|---|---|---|
| R70 | https://www.data.gov.in/policies, re-retrieved 16:28 UTC | [PUBD] | `0e1ef1afd34980873c056e859b0350e13666f0a7a5e0809f3f958b0c1bf7d500` (identical to R52) | Copyright Policy unchanged; its link to the GODL-India notification |
| R71 | https://data.gov.in/sites/default/files/Gazette_Notification_OGDL.pdf (served from `www.data.gov.in`) | [PUBD] | `b338e0cfacc9cdc83a40950feaaf5ac9d2396b43d3105f99f7d494921c7e3ebe` | GODL-India as notified in the Gazette of India |
| R72 | https://data.gov.in/sites/default/files/NDSAP%20Implementation%20Guidelines%202.4.pdf | [PUBD] | `5de555da05f9c725246ac1b73ff7fad94b4b9e38df0ca707e5b2a034ae8215a5` | NDSAP guidelines before GODL-India |
| R73 | https://www.data.gov.in/_nuxt/4499f47.js (saved 2026-10-06, fourth pass) | [PUBD] | `2e6adbbe6036de8fd185ff42295bda4642b3fd903c3aad33a226d9edda04bd9d` | The two Policies components and their copyright texts |
| R74 | Connection attempts, 16:29 UTC: `info.nhp.gov.in`, `nhp.gov.in`, `www.nhp.gov.in` | [PUBD] | none | Reachability (repeat of R57) |
| R75 | https://nihfw.ac.in/, https://nihfw.ac.in/cms/website-policy.php, https://nihfw.ac.in/cms/terms--and-conditions.php | [PUBD] | `bf4dc6c568fdd649870383ce4d5d65846ab5eaeb6c3266c8ad407aaa3aeee0d1` (home); `baa7fcc2782db5b7d7dcab17b27d5049b591d5424047580c862bc249cbd77539` (policy); `b707426bf4373ca682428c481172e1122acd20d4c9059485424ad989c2ba4571` (terms) | NIHFW's own website terms |

### B14: data.gov.in Copyright Policy and GODL-India

- **Copyright Policy unchanged (R70)** [PUBD]. The Policies page is
  byte-identical to the copy read earlier on 2026-10-06 (R52). It still says:
  "Material featured on this Portal may be reproduced free of charge after
  taking proper permission by sending a mail to us." The footer still reads
  "All rights reserved except published datasets/resources and metadata."
- **The same page lists GODL-India (R70)** [PUBD]. Among its policy documents is
  "Govt Open Data License - India", linked to the gazette notification (R71).
  The page gives no text relating that document to the Copyright Policy.
- **GODL-India as notified (R71)** [PUBD]: MeitY Notification F.No.
  8(2)/2013-EG-I, New Delhi, 10 February 2017, titled "Government Open Data
  License - India".
  - Its preamble says that "the open license for data sets published under
    NDSAP and through the OGD Platform remained unspecified till now".
  - Section 3 grants the licence "Following the mandate of the National Data
    Sharing and Accessibility Policy (NDSAP) … that applies to all shareable
    non-sensitive data … generated using public funds by various agencies of
    the Government of India", subject to sections 4 and 7.
  - Sections 4 to 9 cover attribution, non-endorsement, the attribution
    template, exemptions, termination, dispute redress and governing law. They
    were not compared clause by clause with the `/Godl` text (R47) recorded in
    the third pass.
  - **The notification does not mention the portal's Copyright Policy.**
- **NDSAP Implementation Guidelines 2.4 (R72)** [PUBD], dated 18 November 2015,
  before the notification. They record a Task Force decision of 10 September
  2015 to form a committee to "review and recommend the license to be
  associated with the data being published on the OGD Platform". They contain
  no licence text and do not mention the Copyright Policy.
- **A second copyright text in the site script (R73)** [PUBD]. The script holds
  two "Policies" components.
  - The one served on `/policies` carries the "proper permission" text.
  - The other carries a different "Copyright Policy": "The content available on
    the portal is the intellectual property of NIC and its various content
    providers from Government of India."
  - Which page or host shows the second component was not determined [U].
  - Neither text mentions published datasets.
- **What this establishes about B14.**
  - The notified text says the open licence for data sets published "under
    NDSAP and through the OGD Platform" had remained unspecified, and grants
    GODL-India for shareable non-sensitive data generated with public funds
    (R71). It does not name C1a, C2 or C3. The portal's footer excepts
    published datasets from "All rights reserved" (R70).
  - No official text found explains how the Copyright Policy's permission
    requirement relates to published datasets, or which statement governs where
    they differ [U].
  - B14 stays **open**. This pass does not decide precedence, and it does not
    withdraw or strengthen the ADR-0002 basis.

### B15: C1b and `info.nhp.gov.in`

- **Hosts still unreachable (R74)** [PUBD], 16:29 UTC.
  - `info.nhp.gov.in` (117.239.178.13) and `nhp.gov.in` (172.239.183.210)
    refused or timed out on ports 80 and 443.
  - `www.nhp.gov.in` did not resolve.
  - No current terms, licence or `robots.txt` could be read [U].
- **NIHFW's own site (R75)** [PUBD]. NIHFW is the contributor named for the C1
  catalog (R26).
  - Its Website Policy (last updated 03-08-2023) is a disclaimer and a privacy
    note.
  - Its "Terms & Conditions" page holds only "Content Provided By Department"
    (last updated 24-03-2025), with no terms.
  - Its footer reads "Contents on this website is published and managed by The
    National Institute of Health & Family Welfare. Copyright © 2017. All rights
    reserved."
  - Neither page mentions the National Health Portal, `info.nhp.gov.in` or the
    reuse of NHP data. These terms cover NIHFW's own website; **they are not
    evidence about C1b's file host.**
- **Historical evidence unchanged.** The 2023 National Health Portal terms
  (fourth pass, R58) remain [ARCH], historical, from `www.nhp.gov.in`. They are
  not current evidence and not evidence about `info.nhp.gov.in`.
- **Relevant, not decisive.**
  - The GODL-India notification frames its grant by NDSAP data generated
    with public funds and does not address where a file is hosted (R71).
  - The C1 catalog page says "Released Under: National Data Sharing and
    Accessibility Policy (NDSAP)" (second pass, R26).
  - No inspected source says whether that catalog-level statement covers C1b's
    externally hosted file. B15 stays **open** [U].

### Effect on the open items

- **B14:** open. GODL-India's notified wording is now cited from the
  Gazette text (R71). The Copyright Policy's relation to datasets remains
  unexplained.
- **B15:** open; unchanged in substance. The hosts are still unreachable, and
  NIHFW's site has no terms for NHP data.
- **Unchanged:** technical retrieval conditions (fourth pass), C4 (sixth pass),
  B6, G2 and G4.

## Alternative address sources (eighth pass, 2026-10-07)

Evidence status only. **No source is accepted, rejected or selected**, no state
is selected, and no manifest or selection record is written. This pass looked
for address-bearing public sources that could replace or complement C1–C6. No
dataset file was downloaded, no datastore or record API was queried, and no
record was read.

### Method

- Discovery used web search [SRCH] and keyword searches of the data.gov.in
  catalog metadata API. Search results located pages; they are not used as
  evidence for any claim below.
- Publisher pages, platform metadata APIs and site scripts were retrieved with
  `curl` on 2026-10-07, between about 14:40 and 15:00 UTC, and read directly
  [PUBD]. Field lists come from the platform's list API, which returns field
  names and types, not records.
- **Requests to hosts whose `robots.txt` disallows all paths.** Roughly 120
  metadata and page requests went to data.gov.in hosts: `www.data.gov.in`
  (R49) and the state instances, whose `robots.txt` is byte-identical to R49
  (R83, R84). Earlier passes did the same. Eighteen field-list requests
  failed locally because of a script error (a trailing carriage return in
  the identifier) and were repeated.
- **Incidental record exposure.** One discovery search (Jan Aushadhi Kendras)
  returned a third-party site's summary that quoted a few individual outlet
  addresses. They are not recorded here, were not used, and the source was not
  pursued; it is third-party [SRCH, 3P]. As with the first pass's C5 summary,
  this was not intentional inspection, but it is disclosed because ADR-0007 §5
  keeps record text out of assessment.
- The first reachability probe of the state instances failed on DNS. A retry
  minutes later reached seven of them (R92). The failures were resolver
  timeouts, not evidence that the hosts are absent.

### Sources for this pass

| # | URL | Kind | SHA-256 of saved response | Supports |
|---|---|---|---|---|
| R76 | https://www.data.gov.in/backend/dmspublic/v1/catalogs?filters[node_alias]=/catalog/company-master-data | [PUBD] | `8169d9e8fa6a746cdde0139c8641f3b4c38cb861caac83ef90cfc00755f484c6` | C7 catalog metadata |
| R77 | https://www.data.gov.in/backend/dmspublic/v1/resources?filters[catalog_reference]=354261 | [PUBD] | `d4a7a40997a0d9444fcd81337206d0edd86b5ed07cf0d0a8231f55888f4d04fe` | C7 resource metadata |
| R78 | https://www.data.gov.in/backend/dataapi/v1/lists?format=json&filters[catalog_uuid]=ec58dab7-d891-4abb-936e-d5d274a6ce9b (offsets 0 and 100) | [PUBD] | `e9922ba043c31d8bbdf69895d051d3a344cc459ec3b0a9fcc7c6894f73270f7f`; `f5554c4193be137908532e455100a7f38039a533c5c177094da152a16599a76c` | C7 field lists (128 lists) |
| R79 | https://www.data.gov.in/backend/dmspublic/v1/catalogs?query=… (18 keyword searches, such as "address", "directory", "contact details", "police station") | [PUBD] | saved; not individually hashed | Discovery only |
| R80 | https://www.data.gov.in/backend/dmspublic/v1/resources?filters[catalog_reference]=… for the catalogs in C8–C10 and "Not assessable or not pursued" | [PUBD] | listed per catalog below | Resource metadata |
| R81 | https://www.data.gov.in/backend/dataapi/v1/lists?format=json&filters[catalog_uuid]=… for the same catalogs | [PUBD] | listed per catalog below | Field lists, where they exist |
| R82 | https://www.data.gov.in/_nuxt/36aab54.js, re-retrieved | [PUBD] | `45fc26bc7b8d0b25fa746c168d1c37bd6be28dfae91b5e09b45f72ce2ad23458` (identical to R47) | GODL-India text unchanged; grant wording |
| R83 | https://tn.data.gov.in/ (home, `/terms-of-use`, `/policies`, `/robots.txt`) | [PUBD] | home `f88ef1c0df63628e411db1ea4aa5b958fa7a3a0fdfb682e8a9e896120e95dc0e`; terms `7665ee9f366f956606c7dab60865493f2ee27c574952fd4f98541e56798436a0`; policies `a5d2f7cf837c5002c48e66ced8ff63c95485688981f7737e17355c1d25a15e83`; robots `efdb5938a9736727f5cce2b60355588e4fa541d19d022d222d8a09b8efd5dcce` | Tamil Nadu instance footer, terms, policies |
| R84 | https://karnataka.data.gov.in/ (the same four paths) | [PUBD] | home `f0b8f416b6e5c46e55d12c89486150f390ed3781349cb9f34962122206a5011e`; terms `0ebcd7eb5d045b0375f7606795b062670953cf432ec5ea216961aa638ac7613f`; policies `040d01b9e127470e702b2eefa959a00aa9186d04a99dfba2c66122481b359425`; robots as R83 | Karnataka instance footer, terms, policies |
| R85 | `/policies` on `odisha`, `sikkim`, `punjab`, `kerala` and `ap.data.gov.in` | [PUBD] | `de65554c1ce0ba35cebda51e354d45f758d0008bbade4ed081a024e51fcd7e0d`; `824ca0a3de4217b1604a483590f3dfe370e2e475ef179eeb5e9ea77bdd939b65`; `2347f0f2660a5b7249d7d999918f6665f2b157c6335a803c917c4bcfcfaaa278`; `50c02115ef5e6ad5250439e11278d304e3b4ebbdefd6f7545a161b5be2a119af`; `bd7361f1d488c6ca37c920e6708fe2e8bf4a1893d88c2d026a871f099ca08251` | Same footer and Copyright Policy on five more state instances |
| R86 | https://smartcities.data.gov.in/policies | [PUBD] | `09160cc0d750bc0c1c4c1cc026e1be51006b875d87388eda180941fe2c13e659` | Smart Cities instance policies |
| R87 | https://aikosh.indiaai.gov.in/ and its scripts; https://aikosha-api.indiaai.gov.in/ad/idp/api/v1/admin/content/detail/terms_and_conditions | [PUBD] | home `887995cb32885b1fa0cdf49a194625796693364270a7235f49f6e2eb0d12139c`; main script `9c5df858153fba5cfd40d3e65a13c26dd01428d4e93c5a6c8ae66420f756f48f`; terms API `12a22880bc2e59f8278b4a5e547567f0aa14d020ea456598267fa00208cfebc5` (a `403 Forbidden` body) | AIKosh footer; terms **not obtained** |
| R88 | https://aikosh.indiaai.gov.in/home/datasets/details/all_colleges_as_per_aishe_dashboard_3.html | [MIR] | `cdc26da2b9850ad70fc991255023894b39b5c3ba6d04b94f576bfac7a6cdf29a` | AISHE mirror metadata, read directly this time (R5 was a fetch summary) |
| R89 | https://dashboard.aishe.gov.in/hedirectory/ and its scripts `main.6a3f3221b4aecf63.js`, `337.52e2d3e8e3776afe.js` | [PUBD] | page `7689ede8a68ffc9e5e5fabd9c345357b063bb401f3962a63e4b4ecdff27f7f3c`; main `7ed241f7cdfbfc4e626d0b479754d7e5d69e5e3c1b10b8a25e38cc5f8c810149`; module `37add94d3048733a5c8cd2b51644e0efd03a54d6f3161463335415f61dd574e3` | C11 directory fields and query handling |
| R90 | https://udiseplus.gov.in/ and `main-KGJ6AKF7.js`; https://data.udiseplus.gov.in/archive; `kys.udiseplus.gov.in`, `microdata.udiseplus.gov.in` | [PUBD] | home `002f6499d0b8df10274e366b94d67f8f505955d591de6af0ad721a7acc873661`; script `c4db55841d3c9ac04637ffa7450d74ec493f073068715f7fa96c353317cdfee7`; archive `b722f328a12a68931951cc61c379b87af6e8c74e9d5a955f5af38c26fe2214fe` | UDISE+ sub-portals; archive behind a login; two hosts did not respond |
| R91 | https://saras.cbse.gov.in/SARAS/AffiliatedList/ListOfSchdirReport | [PUBD] | `7c672f1463abc2d17019e61bf18c1353d191b0be01d335db18fb1bc0d6408ca1` | C12 directory page |
| R92 | Reachability of state open-data hosts, 2026-10-07 | [PUBD] | none | Seven state instances reachable on retry; `rajasthan`, `delhi` and `surat.data.gov.in`, `data.karnataka.gov.in` and `opendata.maharashtra.gov.in` did not answer |

### The GODL-India basis for state-department data (B17)

C8 and C9 are published by state departments through NIC's state instances of
the Open Government Data Platform. C7 and C10 are central and sit on
`www.data.gov.in`, like C1–C3.

- **Footer, on every state instance read (R83–R85)** [PUBD]: "© 2012-2022
  GOVERNMENT OF INDIA All rights reserved except published datasets/resources
  and metadata." and "The content published on data.gov.in are owned by the
  respective Ministry/State/Department/Organization licensed under the
  Government Open Data License - India." It is the same footer as on
  `www.data.gov.in` (R26, R70), and it names state owners.
- **GODL-India text unchanged (R82)** [PUBD]. The script is byte-identical to
  R47. Its grant (section 3) reads: "Following the mandate of the National Data
  Sharing and Accessibility Policy (NDSAP) of Government of India that applies
  to all shareable non-sensitive data … generated using public funds by various
  agencies of the Government of India, … all users are provided a worldwide,
  royalty-free, non-exclusive license to use, adapt, publish (either in
  original, or in adapted and/or derivative forms), translate, display, add
  value, and create derivative works (including products and services), for
  all lawful commercial and non-commercial purposes". A search of the
  licence text strings in the script found no "State" or "States".
- **Terms of Use on the state instances (R83, R84)** [PUBD]. Like the
  `www.data.gov.in` terms recorded in the fourth pass (R50), they defer to
  "the 'license' metadata element of individual dataset records", require
  accuracy and prominent acknowledgement, and are silent on automated
  access. They were not compared with R50 word for word.
- **The Copyright Policy differs by host** [PUBD].
  - Seven state instances (R83–R85) carry: "The content available on the
    portal is the intellectual property of NIC and its various content
    providers from Government of India. NIC shall not be liable for any delays
    in content updation …". It matches the second "Policies" component found
    in the data.gov.in script in the seventh pass (R73), which was not then
    placed on any page. **It has no permission requirement and does not mention
    datasets or a licence.**
  - `www.data.gov.in` (R70) and `smartcities.data.gov.in` (R86) carry the
    "proper permission by sending a mail to us" text (B14).
- **Same files, two portals.** The C8 and C9 catalogs are returned by the
  `www.data.gov.in` catalog API with their state instance as domain name, and
  their files sit on the `www.data.gov.in` file store (R79, R80). So the same
  files can be reached through portals whose Copyright Policies differ.
  Whether `www.data.gov.in` presents them as its own content was not checked
  [U].
- **What this establishes.**
  - The platform footer extends GODL-India to state-owned content in so many
    words. The licence's own grant sentence refers to agencies of the
    Government of India and does not mention state governments. No inspected
    text says whether that sentence limits the footer for state data [U].
  - On the state instances the B14 permission sentence is absent; on
    `www.data.gov.in`, through which the same files are reached, it is
    present. No inspected text says which portal's policy governs such a
    file [U].
  - **New B17** (evaluation notes). Like B14, it is not resolved here, and this
    pass decides no precedence.

### Candidates found

Numbered on from C6. "Family" is a first-look classification only; G4 applies
to every one.

#### C7. Company Master Data (Ministry of Corporate Affairs, data.gov.in)

1. **Publisher:** Ministry of Corporate Affairs (R76) [PUBD].
2. **Title and URL:** catalog "Company Master Data",
   https://www.data.gov.in/catalog/company-master-data; active resource
   "Registrars of Companies (RoC)-wise Company Master Data",
   `/resource/registrars-companies-roc-wise-company-master-data` (R76, R77).
3. **Family:** `government_published` (G4 open).
4. **Licence:** the site-wide GODL-India statement, as for C1–C3 (R70, R82).
   No resource-level licence field. **B14 applies.**
5. **Redistribution and commercial use:** if GODL-India governs, its text
   grants publication "in original, or in adapted and/or derivative forms" for
   "all lawful commercial and non-commercial purposes", subject to its sections
   4 and 7. Whether it governs is B14.
6. **Retrieval:** catalog `is_webservice` 1 and resource `is_api_available` 1
   (R76, R77). `api.data.gov.in` refused connections in the fourth pass and was
   not re-tested. The platform's download form and CAPTCHA (R54, recorded for
   C2) were not re-checked for this resource. Silent terms point to manual
   retrieval (B8).
7. **Coverage:** jurisdiction "All India" [PUBD, R76]. Mapping to `lgd:state:`
   IDs [U].
8. **Fields (R78)** [PUBD]. The active list (updated 2026-07-22) has 16 fields:
   `CIN`, `CompanyName`, `CompanyROCcode`, `CompanyCategory`,
   `CompanySubCategory`, `CompanyClass`, `AuthorizedCapital`, `PaidupCapital`,
   `CompanyRegistrationdate_date`, `Registered_Office_Address`,
   `Listingstatus`, `CompanyStatus`, `CompanyStateCode`,
   `CompanyIndian/Foreign Company`, `nic_code`,
   `CompanyIndustrialClassification`.
   - The other 127 lists (state-wise snapshots to 2015, 2018, 2019 and 2021)
     are inactive. 93 of them also have `email_addr`.
   - **Address:** one string, `Registered_Office_Address`. Completeness [U]
     (G2).
   - **State:** `CompanyStateCode`. Its code scheme is [U], so its mapping to
     `lgd:state:` is [U]. `CompanyROCcode` names a Registrar of Companies,
     which is not a state. No district or PIN column.
9. **Identifier:** `CIN` ("Corporate Identification Number", per the
   catalog description, R76), which could support `record_id_scope`
   `native`. Stability across snapshots [U].
10. **Currency:** frequency "Monthly"; the resource note says "The data upto
    3rd November 2023"; the resource's `datafile_url` points to a 2015 Goa file
    (R77). The metadata conflicts (G6).
11. **Privacy and scope:**
    - The active list has no person or contact field. The inactive lists'
      `email_addr` would be removed at ingestion (ADR-0001 §2) if they were
      ever used.
    - Registered offices of small companies may be residences [U]. ADR-0001 §2
      excludes residential-looking records, and only the record-level screen
      can tell how many (ADR-0006 §12).
    - Company names can contain names of individuals [U].
    - Whether a company's registered office is an address "of
      institutions/facilities" under ADR-0001 §1 is a maintainer decision
      (**B18**).
12. **Schema observation (not a preference):** its field list shows national
    declared coverage, one address string, a company identifier and a state
    code. It is also the furthest from the facility types of C1–C6, and its
    residential share is unknown.

#### C8. Karnataka state-department address catalogs (karnataka.data.gov.in)

Each catalog is a separate candidate; C8a and C8b share a publisher. Licence
for all:
the footer and terms above, with B14 and B17. Retrieval for all: a
`robots.txt` that disallows all paths (R84) and silent terms (B8); whether the
state instances use the download form recorded for `www.data.gov.in` (R54) was
not checked [U].
Department and jurisdiction come from the catalog records returned by R79;
agency, frequency, dates and file sizes from R80 [PUBD]. Sizes are file sizes
from metadata, not row counts.

| Row | Catalog (resources) | Publisher (department / agency) | Jurisdiction | Frequency; published | File size | Field list (R81) | SHA-256 (R80; R81) |
|---|---|---|---|---|---|---|---|
| C8a | List of Karnataka one centers address and contact details (1) | DPAR, Electronic Delivery of Citizen Services (EDCS) | Karnataka | Annual; 2021-10-27 | 8,347 B | none | `3616cc23dacc191cb5a2a63d7843c093e0fb7417b40d94c45b8a2ffc9cebc1ea`; `6f546342c197bf25d28c15ae22d71cdc0e2bf2393b60d44a0ed70e9fa249a3d4` |
| C8b | List of Grama One centers details (2, same title and size) | DPAR, EDCS | "All India" | Biannual; 2021-11-18 | 32,064 B | none | `b3f8f083d1548b9eae4f0c933a63f0a02eaf16baebf7773e3b76ba6a31c7bdc9`; `613cde457d419c455beeaaa8b8439d9898c43a38b9466cdb15450d3046f6b932` |
| C8c | FIRE STATION DETAILS (1) | Home Dept, Karnataka State Fire and Emergency Services | Bangalore Urban | Annual; 2025-07-15 | 11,640 B; file name "DETAILS_OF_FIRE_STATIONS_WITH_PHONE_NUMBERS" | none | `2b88620533726bf960f0aaef1df3b4f349682b235d0c481ba571d3920f2fbee8`; `9c0fe89feb17339656f72d59e5383f10d19661a4873030253899c5d23a6a3ea8` |
| C8d | List of Prisons in Karnataka State (5) | Home Dept, Prisons and Correctional Services | Karnataka | Annual; 2022 | 234–1,637 B each | none | `f1a3ca33919a6dc3f84e4e19127f18a8c7bf033ae8ae53f914a00f806aeb8514`; `a571f0624d5a0f1e2d851f67dac52ac577c37a9b4165690b402bd2479afae528` |
| C8e | List of APMCs (1) | Agricultural Marketing Department | Karnataka | Annual; 2021-10-12 | 19,566 B | none | `8783befc7e9c23dd1c9766db38189aaa3bcdbfa0869572462cddba6ab50e6457`; `5c8d82024cb377ab032c9a047556ee1c1162c56be50c02ed79a543321b5bf0f3` |
| C8f | Fisheries Office Contact Details (3) | Animal Husbandry and Fisheries Department | Karnataka | One-time; 2021–2022 | 597–4,238 B each | none | `3520d87f7726758cfbd81d1b9a5a62d1f0cc83a8d126b20eb025c2c26f89c023`; `39f01b7f684415ee054a0ef22002fb653a4b4121209890334303490c1964d11a` |
| C8g | List of training center in Karnataka skill development center (1) | Karnataka Vocational Training and Skill Development Corporation | Karnataka | Half yearly; 2022-01-07 | 644 B | none | `f566c436298374fa79c9209b049337bcacf1b20b23ae6d79580c6ef595ba1c34`; `bf96a0efc52b38498ef1a4c23a3918ea8d491770825b167511613a1a5382b1f0` |
| C8h | Registrar of Cooperative Societies - List of Societies (KSC Act 1959) (1) | Co-operative Department | Karnataka | Annual; 2021-10-12 | 1,147 B | none | `03d0b110755bf7e3bc3973f32bf0dd8e8881786c38c7d076806a78d0cc7429ef`; `2155253a27fb431afb7404f6673af3abc80be462a39d18452a0cb91d5174a019` |
| (C8i) | List of Museums (1) | Directorate of Tourism | Karnataka | Annual; 2021-12-01 | 1,784 B | `district_`, `museum_name_`, `fee`, `museum_incharge_head`, `contact_numbers`, `email_id` | `5ff804320ad791b77d9628bf447ce3dc5f2179dd5e6154dade3107317604d206`; `2ab2f946e17b21b6384d943dca73bba5dd97e7951dc93b23e044023dd62561b9` |

- **Address fields:** [U] for C8a–C8h. They have no platform field list, so
  only a header row could show them (B6). The titles of C8a and C8f name
  "address" or "contact details"; a title is not schema evidence.
- **C8i has no address field** in its field list. It is listed so that it is
  not re-checked; it is **not an address-bearing candidate**. It has a
  person-related column (`museum_incharge_head`) and contact columns.
- **Coverage:** one state each. `coverage_state` would be `lgd:state:29` only
  if a file holds Karnataka records alone [U]. C8b's jurisdiction label "All
  India" conflicts with its state publisher.
- **Identifier, state, district and PIN columns:** [U].
- **Size:** the files are small (234 B to 32 KB). C8d, C8g and C8h are under
  2 KB each, so they can hold only a few dozen short rows at most
  (inference from size). What each holds is [U].
- **Privacy:** contact columns are likely, from the titles [U]. Who operates
  Karnataka One and Grama One centres, and whether any are run by individuals,
  is [U]. C8h (societies) may include residential addresses [U].
- **Why it matters:** several Karnataka departments publish separately. If G4
  treats them as distinct publishers, that bears on ADR-0007 §6 (holdout) and
  on the publisher-count dimension. Neither is decided here.

#### C9. Tamil Nadu state-department address catalogs (tn.data.gov.in)

Licence and retrieval as for C8 (R83 for the instance).

| Row | Catalog (resources) | Publisher | Frequency; published | File size | Field list (R81) | SHA-256 (R80; R81) |
|---|---|---|---|---|---|---|
| C9a | Commissionerate of Municipal Administration (CMA): Regional Offices and ULBs Address Details (1) | Municipal Administration and Water Supply Dept, CMA | Annual; 2017-12-29 | 23,541 B | `sl_no`, `name_of_the_regional_office`, `name_of_the_ulb_rdma`, `address`, `telephone_no__with_std_code`, `fax_number_`, `email_id`, `no_of_wards` | `ba882adfa6f1e22009bf230383a5dcdc5a7dc2f07399bcc4ba65860edc6bc23f`; `da459cf4c2e68fd57cd99dc2554f9bb0e5fa827721ddbe95d8beb2c681be9360` |
| C9b | List of Study Centres under Tamil Nadu Open University in 2020 (10) | Higher Education Dept, Tamil Nadu Open University (TNOU) | Annual; 2021-08-12 | 976 B–31 KB each; the enrolment-count resource 152 KB | Two of ten lists: B.Ed study centres (`name_of_the_region`, `name_of_the_district`, `name_of_the_institute`, `address`, `phone_number`, `mobile_number_`, `mail_id`); enrolment counts (no address) | `5ce4f79e57ad0c2b013d1bdb7216778872f0aa8e873eaa878ffd5f1508887df7`; `287b1f78714278c4d228f5e0c8329ae0d072e5718133f51244804c78f4b88649` |
| C9c | Details of State, District Offices of the Fire and Rescue Services department and fire stations (1) | Home, Prohibition and Excise Dept, TN Fire and Rescue Services | Annual; 2019-06-04 | 299 B | none | `e74dcc5876ad375389f875a9efccd05fd06ae375b54bf5dda9289eac6d4d52a0`; `53abc76a0650d932cf3f1d641c866df7f5ea87ffb2edece50d1b335a142a1d35` |

- **C9a:** its field list shows one `address` string per regional office or
  urban local body. It has no district, PIN or
  identifier column. Its contact columns would be removed at ingestion
  (ADR-0001 §2); whether they are office or personal contacts is [U]. The
  gazetteer has no urban units, so ULB offices could not link below district
  level (ADR-0006 §19).
- **C9b:** one list shows `address` and `name_of_the_district`. Its
  `mobile_number_` may be a person's number [U]. The other eight lists'
  schemas are [U]. Apart from the enrolment counts, the resources are lists of
  institutions (centres, partner institutions).
- **C9c:** 299 B, file name `office_infrastructure_details.csv` (R80). It can
  hold only a few short rows, so it is unlikely to be a list of fire stations
  (inference from size); what it holds is [U]. Weak.
- **Coverage:** jurisdiction "Tamil Nadu" for all three; `lgd:state:33` [U].
- The publishers differ from C5's (CEO Tamil Nadu or district
  administrations), and unlike C5 these catalogs carry a site-wide licence
  statement.

#### C10. Blood Bank Directory (National Health Portal, data.gov.in)

- Publisher NIHFW, as for C1. Two resources (R80, R81) [PUBD]:
  - "Blood Bank Directory (updated till last month)", Monthly, published
    2017-08-10, `datafile_url` `https://info.nhp.gov.in/api/blood-banks.csv`.
    That is C1b's file host, so **B15 applies**.
  - "Blood Bank Directory as on September 2015", 2015-09-18.
- Fields include `_state`, `_district`, `_city`, `_address`, `pincode`,
  latitude and longitude. They also include `_nodal_officer_`,
  `_contact_nodal_officer`, `_mobile_nodal_officer`, `_email_nodal_officer` and
  `_qualification_nodal_officer`, which are personal data and would be removed
  at ingestion (ADR-0001 §2).
- SHA-256: resources
  `37d9612bc8333bbf5d3123c4da3a9fdb63182abbc9b49cc5eee7e98bd0382a9d`; lists
  `b07771e75be20bdbc53cf1db50d2ea5a9024a65ef4c40018514da5b8dc334797`.
- No evidence advantage over C1: same publisher, same file host, B14 and
  B15.

#### C11. AISHE higher-education directory (Ministry of Education)

- **Directory (R89)** [PUBD]: https://dashboard.aishe.gov.in/hedirectory/. Its
  institution detail view shows `name`, `address1`, `state`, `district`,
  `pincode` and `website`, loaded from `institutionDirectory` endpoints by an
  `id` parameter. The scripts also handle an AISHE code, which the mirror
  lists as a column (R88).
- **Access:** an interactive search. The client encrypts search text and AISHE
  codes before sending them. No bulk file was found in the directory.
- **Licence:** no licence, terms or copyright text was found in the directory
  page or scripts. The only licence statement is the mirror label "Open
  Government License, India" (R88) [MIR]; a label alone is not verified licence
  text. The mirror copy lists "Location", not an address column.
- **Outcome:** no licence text found; not assessable to acceptance. Whether
  `aishe.gov.in` has terms was not checked [U].

#### C12. CBSE affiliated-school directory (SARAS)

- **Page (R91)** [PUBD]: "CBSE SCHOOLS DIRECTORY", "Total No. of Schools
  affiliated with CBSE : 33169". It filters by state, district, region, keyword
  ("any word from School Name or Address"), affiliation number and level.
  Result columns: "Aff. No & School Code", "State & District", "Status",
  "School & Head Name", "Address Details".
- **Licence:** none on the page; CBSE's website policies were not checked [U].
- **Privacy:** "Head Name" is a person's name and would be removed (ADR-0001
  §2). What "Address Details" holds besides the address is [U].
- **Family:** CBSE publishes as the affiliating board. Whether it operates any
  of the listed schools is not stated on the page [U]. G4 open.
- **Outcome:** not assessable to acceptance. Like C6, a search form with no
  licence found.

### Not assessable or not pursued

| Source | Finding |
|---|---|
| UDISE+ school directory (R90) | The archive needs a login; `kys.udiseplus.gov.in` and `microdata.udiseplus.gov.in` did not respond; `api.udiseplus.gov.in` returns 404 at its root. Terms [U]. Not assessable. |
| AIKosh terms (R87) | The terms API returned `403 Forbidden`; the footer reads "Copyright AIKosh. All rights reserved." AIKosh is a mirror, so its terms would not be the publisher's licence. |
| Maharashtra Labour Department and Allied Offices (data.gov.in; published 2025-09-25; 66,199 B) | Address-bearing by title; no field list; schema [U]. Found late; not assessed. |
| Mizoram police stations (data.gov.in; 2022-07-20; 1,783 B); Meghalaya Rural Bank branches (2014, One-time) | Address-bearing by title; schema [U]; not assessed. |
| MoHUA Smart Cities city catalogs (police and fire stations for several cities; Agra hospitals and nursing homes) | City-level. The one checked (Chennai police stations) is on `smartcities.data.gov.in`, whose Copyright Policy carries the B14 text (R86). Not assessed. |
| MSME Udyog Aadhaar registrations; Karnataka Udyam registrations | **Flagged for personal-data risk, not assessed:** enterprise registrations commonly include sole proprietors. An assumption to verify from documentation, not a finding. |
| State-wise list of notaries (Ministry of Law and Justice) | By its title, a list of appointed individuals; out of scope under ADR-0001 §2. Not a candidate. |
| Punjab "Banking Offices" | District counts, not addresses. |
| Jan Aushadhi Kendras (PMBI) | Discovery returned only a third-party site [SRCH, 3P]; the official site was not checked. Not assessed. |
| NDAP (`ndap.niti.gov.in`), Navodaya Vidyalaya Samiti, UGC, eCourts | Reachable; not researched in this pass. |

### Effect on the open items

- **No source is ready for a source ADR.** None of C7–C12 has file header rows
  or file-level statistics (B6).
- **New B17:** the GODL-India basis for state-department data, and which
  Copyright Policy governs files listed on both a state instance and
  `www.data.gov.in`.
- **New B18:** whether company registered offices (C7) fall within ADR-0001 §1,
  and how residential registered offices are handled.
- **B14** now also covers C7 and C10, and bears on C8 and C9 through B17.
- **B15** now also covers C10.
- **Seventh-pass [U] answered in part:** the second data.gov.in Copyright
  Policy text (R73) is the one shown on the state instances (R83–R85).
- **Unchanged:** C1–C6 and their open items.

## Evidence status

- **Publisher or publisher-platform, retrieved and inspected directly (second
  pass) [PUBD]:** C1–C3 catalog and resource metadata, field lists, publisher
  strings and the data.gov.in footer (R26–R34); C4 metadata, licence label,
  schema and row count (R35–R37); C5 CEO Tamil Nadu footer and electoral-roll
  links, and the Dindigul and Chikkaballapur copyright policies (R38–R40); C6
  homepage counter, footer, copyright policy and directory page (R41–R43).
- **Publisher or publisher-platform, retrieved and inspected directly (third
  pass) [PUBD]:** data.gov.in redirect, footer markup, site build configuration,
  GODL-India text, and C1–C3 resource and catalog metadata keys (R44–R48).
- **Publisher or publisher-platform, retrieved and inspected directly (fourth
  pass) [PUBD]:** data.gov.in `robots.txt`, Terms of Use, policies, help and
  API pages, download-form scripts, C1–C3 file locations, file-URL response
  headers, and reachability of `api.data.gov.in` and the National Health Portal
  hosts (R49–R57).
- **Saved responses re-read offline (fifth pass):** platform field types and
  counts for C1–C3 (R32–R34) and C4's datastore schema, count and dataset
  metadata (R36, R37); C1–C3 resource-metadata notes and file facts (R55). No
  new retrieval; no file or record read.
- **Publisher or publisher-platform, retrieved and inspected directly (sixth
  pass) [PUBD]:** Telangana portal `robots.txt`, C4 metadata, metadata schema,
  routes, footer, content-page lookups, Policies and Contact pages; ITE&C
  open-data page and the Telangana State Open Data Policy 2016 (R60–R68). The
  portal's API documentation was not obtained (R69).
- **Publisher or publisher-platform, retrieved and inspected directly (seventh
  pass) [PUBD]:** data.gov.in Policies page re-check, the GODL-India gazette
  notification and NDSAP Implementation Guidelines 2.4, the two Policies
  components in the site script, National Health Portal host checks and
  NIHFW's website terms (R70–R75).
- **Publisher or publisher-platform, retrieved and inspected directly (eighth
  pass) [PUBD]:** C7 catalog, resource and field-list metadata (R76–R78);
  catalog searches used for discovery (R79); C8–C10 and other resource and
  field-list metadata (R80, R81); GODL-India text re-check (R82); footer and
  policies of seven state instances, terms and `robots.txt` of two of them,
  and the Smart Cities instance's policies (R83–R86); AIKosh, AISHE directory, UDISE+ and CBSE SARAS pages and
  scripts (R87, R89–R91); host reachability (R92). AISHE mirror metadata read
  directly [MIR, R88]. AIKosh terms not obtained.
- **Internet Archive copy, inspected directly (fourth pass) [ARCH]:** National
  Health Portal terms of use as captured 2023-04-04 (R58); archive index for
  `info.nhp.gov.in` (R59).
- **Checked at the publisher (first-pass fetch summary, not directly
  inspected):** RBI terms (R7, R8). The first-pass KVS facts (R10) are
  superseded by R41–R43.
- **Official metadata only (mirror, first pass):** AISHE (R5). The first-pass
  mirror records R1–R4 for C1–C4 are superseded by the [PUBD] evidence above
  where they differ.
- **Search-derived only:** C1 content description; the C5 list structure,
  languages, polling-station numbering, Tamil Nadu list locations (R20, R21) and
  Karnataka district evidence (R22); UDISE+ (aggregates, API); PMJAY; ABDM; oil
  outlets; bank locators.
- **Community or third-party:** C1 attribute names and quality notes (R6);
  IFSC compilation (R9); PMJAY guide (R23).
- **Calculated:** the gazetteer table, and the KVS India count of 1,364
  [CALC], derived from the source-reported 1,367 "in India and around the
  world" minus one school each in Moscow, Tehran and Kathmandu [PUBD, R41].
- **Still needs verification before any source ADR:**
  - for C1–C3, the items still open under "Effect on the open items" (fourth
    and seventh passes): C1b's licence and file-host terms (B15), and the
    data.gov.in Copyright Policy wording (B14); plus header rows and G4;
  - the licence text behind C4's label, and the conflict with the portal's
    Copyright Policy and footer (sixth pass);
  - C5 licence (all rights reserved at CEO Tamil Nadu, R38; district sites allow
    reuse on request, R39, R40) and schema;
  - C6 licence (reuse on request, R42) and schema;
  - downloadable file header rows for C1–C4 (only platform schemas were read);
  - C1 and C2 currency;
  - CEO versus district publisher for C5;
  - C5 statewide coverage;
  - the AISHE `Location` field, the UDISE+ API terms and the RBI disclaimer text;
  - for C7–C12 (eighth pass): B14, B17 and B18 as they apply, header rows for
    every file-only resource, the C7 state-code scheme, and licence text for
    C11 and C12.

## Evidence gaps

- **G1. Licences.**
  - C1–C3: ADR-0002 verified data.gov.in's site-wide GODL-India statement on
    2026-10-02. The second pass's re-check was inconclusive because of the
    sandbox notice. The third pass (2026-10-05) found that notice hidden on
    `www.data.gov.in` and the licence text unchanged [PUBD, R44–R47]. No
    resource-level licence field exists.
  - C1–C3, fourth pass (2026-10-06): the Terms of Use defer to a per-record
    "license" element that the metadata lacks; the Copyright Policy asks for
    permission "by sending a mail", against the GODL-India footer (unresolved)
    [PUBD, R50–R52]. Seventh pass: the Copyright Policy is unchanged; the
    gazette notification addresses the licence for data sets published under
    NDSAP and through the OGD Platform and does not mention the Copyright
    Policy (unresolved, B14) [PUBD, R70, R71].
  - C1b: its file is hosted only at `info.nhp.gov.in`, outside data.gov.in.
    Whether GODL-India reaches it is unresolved; the host was unreachable, and
    the only National Health Portal terms found (archived 2023, `www.nhp.gov.in`)
    reserve all rights [PUBD, R55, R57; ARCH, R58]. Seventh pass: the hosts are
    still unreachable, and NIHFW's own website terms do not cover NHP data
    (unresolved, B15) [PUBD, R74, R75].
  - C4: the publisher's dataset label "Government Open Data License - India" was
    verified directly [PUBD, R36]; the applicable licence text is not verified.
    Sixth pass (2026-10-06): no licence text or link was found on the portal; the
    portal's Copyright Policy asks for permission by mail and its footer
    reserves all rights; the 2016 state policy names no licence [PUBD,
    R61–R68]. Unresolved.
  - AISHE: mirror label only [MIR, R5].
  - C5: all rights reserved at CEO Tamil Nadu (R38); district sites allow reuse
    on request (R39, R40).
  - C6: reuse on request (R42).
  - C5 and C6: no reuse licence found. RBI grants none.
  - Eighth pass (2026-10-07): C7 and C10 rest on the same site-wide statement
    as C1–C3 (B14; C10 also B15). C8 and C9 rest on the same footer on the
    state instances, whose Copyright Policy lacks the B14 permission sentence;
    whether GODL-India's grant reaches state-department data, and which host's
    policy governs, is unresolved (B17) [PUBD, R82–R85]. C11 and C12: no
    licence text found [PUBD, R89, R91; MIR, R88].
- **G2. `raw_text`.** C1a has `Address_Original_First_Line`, C1b has `Address`,
  C2 has `Facility Address` and C3 has `DiagnosticCentreAddress`. Whether these
  are complete enough to serve as `raw_text` is unverified (C1a's field is named
  a first line). C4 publishes components only. Whether a concatenation counts as
  published `raw_text` under ADR-0006 is not decided. Eighth pass: C7 has
  `Registered_Office_Address`, C9a and C9b's B.Ed list have `address`, C10 has
  `_address`; their completeness is equally unverified.
- **G3. Headers.** Publisher/platform schema fields for C1–C4 were inspected
  directly [PUBD, R32–R34, R37]. No downloadable file was opened, so actual file
  header rows remain unverified. The fifth pass (B6) added platform field types
  and counts, not header rows. C5 and C6 record-bearing schemas are
  unresolved.
- **G4. Publisher identity.** C1–C3 all sit under MoHFW (NIHFW, DoHFW, CGHS).
  Whether they are one `publisher` for ADR-0007 §6 is open. So is whether
  autonomous and statutory bodies (KVS, NIHFW, NHA, RBI) and public-sector
  companies count as "a government body" for `source_family`. Eighth pass: the
  same questions arise for MCA (C7), for each Karnataka and Tamil Nadu
  department or agency in C8 and C9 (department, agency or state government as
  the `publisher` unit), for TNOU and for CBSE (C12).
- **G5. Retrieval.** The first pass's fetch tool got HTTP 403 from data.gov.in,
  consistent with the bot challenge recorded in ADR-0004. In the second pass,
  `curl` got HTTP 200 for the catalog pages and metadata APIs (R26–R34). File
  downloads were not attempted, so whether data files are retrievable is
  untested. Fourth pass (2026-10-06): `robots.txt` disallows all paths; the
  download form needs an image CAPTCHA; the Terms of Use are silent on
  automated access; `api.data.gov.in` refused connections; `HEAD` requests to
  file URLs got `405` (file store) or `200 text/csv` (C1a legacy path), with no
  `GET` sent; `info.nhp.gov.in` (C1b) was unreachable [PUBD, R49–R57]. These
  are technical access conditions, not licence terms. Sixth pass (2026-10-06),
  Telangana portal (C4): no Terms of Use page found; the Policies page is silent on
  automated access; `robots.txt` disallows only `/search`; the API
  documentation endpoint did not respond [PUBD, R60–R69].
- **G6. Currency.** C1a's frequency is "One-time" (granularity "Monthly") while
  its title says "updated till last month"; C1b's is "Monthly" [PUBD, R29].
  Whether either file is actually refreshed is unknown. C2 ("Monthly" against a
  2016 snapshot) and C4 (8 February 2023 against 8 November 2022) also have
  conflicting metadata. So does C7 ("Monthly", data "upto 3rd November 2023",
  and a 2015 file URL) [PUBD, R77].
- **G7. Per-state counts.** No ingestion-time aggregates exist (ADR-0007 §4
  step 3).
- **G8. Language.** Only C5 in Tamil Nadu has any language evidence, and it is
  search-derived.
- **G9. Operators.** No `operator_published` source with a licence was found.
- **G10. Reproducibility.** The gazetteer table came from an ad-hoc script that is
  not in the repository. ADR-0007 §4 requires a versioned procedure.
- **G11. Coverage of this inventory.** Not exhaustive; see "Identified but not
  researched" and, for the eighth pass, "Not assessable or not pursued".
- **G12. Schemas of state-instance files.** Most C8 and C9 resources have no
  platform field list, so their address, state, district, PIN and identifier
  columns are unknown until a header row is read (B6).
