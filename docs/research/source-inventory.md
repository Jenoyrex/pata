# Address-source and focus-state inventory

- **Kind:** Research working notes; not a decision record and not yet sufficient
  for source acceptance. Input to ADR-0007 O1 (focus states) and O2 (address
  sources). Nothing here selects a state, accepts a source or writes a manifest.
- **Gathered:** 2026-10-04, by web search, page fetches and one local computation
  on the pinned gazetteer (`gazetteer_version`
  `bf4a8b5d35130e7c3b94c6e4de812b3fd6deeb059497af22aac178642c2c2c78`).
- **Not exhaustive.** Only the sources and categories listed below were looked
  at. Categories identified but not researched are listed separately.

## How the evidence was gathered

- **Two tools were used.** A web search tool returned a list of result links plus
  a model-generated summary of those results. A page-fetch tool retrieved a single
  page and returned a model-generated summary of it. No page text was saved, and
  no page was read directly by a person. Every external claim below therefore
  rests on one of these summaries, and none is a directly inspected quotation.
  Other claims rest on this repository's ADRs [ADR] or on the local gazetteer
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
3. `government_published`.
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
    data.gov.in blocked from this machine [ADR, ADR-0004].
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
3. `government_published`.
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
3. `government_published`.
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
3. `government_published`.
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
3. `government_published`.
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
3. `government_published`.
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
| All other states | Only national sources C1–C3, C6; per-state coverage [U] | [U] | Not yet verified | Gazetteer gaps in the table below [CALC] | C1–C3 via data.gov.in, blocked from this machine [ADR]; not yet verified |

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

## Evidence status

- **Checked at the publisher (fetch summary, not directly inspected):** RBI
  terms (R7, R8); KVS homepage facts (R10).
- **Official metadata only (mirror):** everything about C1–C4 and AISHE except
  the data.gov.in site-wide licence, which ADR-0002 checked on 2026-10-02.
- **Search-derived only:** C1 content description; all C5 facts; UDISE+
  (aggregates, API); PMJAY; ABDM; oil outlets; bank locators.
- **Community or third-party:** C1 attribute names and quality notes (R6);
  IFSC compilation (R9); PMJAY guide (R23).
- **Calculated:** the gazetteer table, and the KVS India count of 1,364
  (conditional).
- **Still needs publisher or header verification before any source ADR:**
  every licence except the data.gov.in site-wide statement; every header row;
  C1 and C2 publisher strings and currency; C5 licence and statewide coverage;
  the AISHE `Location` field; the UDISE+ API terms; and the RBI disclaimer text.

## Evidence gaps

- **G1. Licences.** Known only for data.gov.in site-wide (C1–C3, via ADR-0002) and
  as mirror labels (C4, AISHE). C5 and C6 have none found; RBI grants none.
- **G2. `raw_text`.** C4 documents components only; C1 is unknown. Whether a
  concatenation counts as published `raw_text` under ADR-0006 is not decided.
- **G3. Headers.** No header row has been seen for any source.
- **G4. Publisher identity.** C1–C3 all sit under MoHFW (NIHFW, DoHFW, CGHS).
  Whether they are one `publisher` for ADR-0007 §6 is open. So is whether
  autonomous and statutory bodies (KVS, NIHFW, NHA, RBI) and public-sector
  companies count as "a government body" for `source_family`.
- **G5. Retrieval.** data.gov.in is blocked from this machine (ADR-0004).
- **G6. Currency.** C1 ("Static" against "updated till last month") and C2
  ("Monthly" against a 2016 snapshot) have conflicting metadata.
- **G7. Per-state counts.** No ingestion-time aggregates exist (ADR-0007 §4
  step 3).
- **G8. Language.** Only C5 in Tamil Nadu has any language evidence, and it is
  search-derived.
- **G9. Operators.** No `operator_published` source with a licence was found.
- **G10. Reproducibility.** The gazetteer table came from an ad-hoc script that is
  not in the repository. ADR-0007 §4 requires a versioned procedure.
- **G11. Coverage of this inventory.** Not exhaustive; see "Identified but not
  researched".
