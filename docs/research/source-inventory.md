# Address-source and focus-state inventory

- **Kind:** Research working notes; not a decision record and not yet sufficient
  for source acceptance. Input to ADR-0007 O1 (focus states) and O2 (address
  sources). Nothing here selects a state, accepts a source or writes a manifest.
- **Gathered:** 2026-10-04. First pass: web search, page fetches and one local
  computation on the pinned gazetteer (`gazetteer_version`
  `bf4a8b5d35130e7c3b94c6e4de812b3fd6deeb059497af22aac178642c2c2c78`). Second
  pass: publisher pages and publisher-platform metadata APIs retrieved with
  `curl` and inspected directly (see "Licence and header verification"). Third
  pass, 2026-10-05: data.gov.in host and licence re-check for C1–C3 only.
- **Not exhaustive.** Only the sources and categories listed below were looked
  at. Categories identified but not researched are listed separately.
- **Three passes.** The sections up to "Candidate-state evidence" record the
  first pass. "Licence and header verification" records a second pass on C1–C6.
  "data.gov.in host and licence re-check" records a third pass on the C1–C3
  licence only. Where they differ, the later pass is the current evidence; the
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

Listed so the gap is visible. None is claimed to be suitable.

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
  `document_id` and `resource_uuid`, and file headers were not read.

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
  mislabelled [U].
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
answered by the third pass ("data.gov.in host and licence re-check").

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
    differ from data.gov.in's [U].
  - The GODL-India exemptions (section 6) exclude personal information and
    identity documents from the licence. That bears on C1a's `Nodal_Person_*`
    and contact fields, which the record-level screen and context-column rules
    already exclude.
  - Terms of use and automated retrieval (E5), header rows, G4 and the source
    ADR itself.

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
  - for C1–C3, the remaining items listed under "Effect on the second pass"
    (third pass); the sandbox question itself is answered there;
  - the licence text behind C4's label;
  - C5 licence (all rights reserved at CEO Tamil Nadu, R38; district sites allow
    reuse on request, R39, R40) and schema;
  - C6 licence (reuse on request, R42) and schema;
  - downloadable file header rows for C1–C4 (only platform schemas were read);
  - C1 and C2 currency;
  - CEO versus district publisher for C5;
  - C5 statewide coverage;
  - the AISHE `Location` field, the UDISE+ API terms and the RBI disclaimer text.

## Evidence gaps

- **G1. Licences.**
  - C1–C3: ADR-0002 verified data.gov.in's site-wide GODL-India statement on
    2026-10-02. The second pass's re-check was inconclusive because of the
    sandbox notice. The third pass (2026-10-05) found that notice hidden on
    `www.data.gov.in` and the licence text unchanged [PUBD, R44–R47]. No
    resource-level licence field exists.
  - C4: the publisher's dataset label "Government Open Data License - India" was
    verified directly [PUBD, R36]; the applicable licence text is not verified.
  - AISHE: mirror label only [MIR, R5].
  - C5: all rights reserved at CEO Tamil Nadu (R38); district sites allow reuse
    on request (R39, R40).
  - C6: reuse on request (R42).
  - C5 and C6: no reuse licence found. RBI grants none.
- **G2. `raw_text`.** C1a has `Address_Original_First_Line`, C1b has `Address`,
  C2 has `Facility Address` and C3 has `DiagnosticCentreAddress`. Whether these
  are complete enough to serve as `raw_text` is unverified (C1a's field is named
  a first line). C4 publishes components only. Whether a concatenation counts as
  published `raw_text` under ADR-0006 is not decided.
- **G3. Headers.** Publisher/platform schema fields for C1–C4 were inspected
  directly [PUBD, R32–R34, R37]. No downloadable file was opened, so actual file
  header rows remain unverified. C5 and C6 record-bearing schemas are
  unresolved.
- **G4. Publisher identity.** C1–C3 all sit under MoHFW (NIHFW, DoHFW, CGHS).
  Whether they are one `publisher` for ADR-0007 §6 is open. So is whether
  autonomous and statutory bodies (KVS, NIHFW, NHA, RBI) and public-sector
  companies count as "a government body" for `source_family`.
- **G5. Retrieval.** The first pass's fetch tool got HTTP 403 from data.gov.in,
  consistent with the bot challenge recorded in ADR-0004. In the second pass,
  `curl` got HTTP 200 for the catalog pages and metadata APIs (R26–R34). File
  downloads were not attempted, so whether data files are retrievable is
  untested.
- **G6. Currency.** C1a's frequency is "One-time" (granularity "Monthly") while
  its title says "updated till last month"; C1b's is "Monthly" [PUBD, R29].
  Whether either file is actually refreshed is unknown. C2 ("Monthly" against a
  2016 snapshot) and C4 (8 February 2023 against 8 November 2022) also have
  conflicting metadata.
- **G7. Per-state counts.** No ingestion-time aggregates exist (ADR-0007 §4
  step 3).
- **G8. Language.** Only C5 in Tamil Nadu has any language evidence, and it is
  search-derived.
- **G9. Operators.** No `operator_published` source with a licence was found.
- **G10. Reproducibility.** The gazetteer table came from an ad-hoc script that is
  not in the repository. ADR-0007 §4 requires a versioned procedure.
- **G11. Coverage of this inventory.** Not exhaustive; see "Identified but not
  researched".
