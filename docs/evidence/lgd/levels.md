# Evidence record: LGD level verification (node E-LGD)

- **Retrieved:** 2026-11-04, from 13:55 UTC, by the agent. Saved responses are in a session
  scratch directory, outside the repository, and are not committed.
- **Standard applied:** ADR-0007 §8 (Proposed): LGD-side evidence is required. Gazetteer counts,
  name patterns, annotator knowledge and third-party summaries are not evidence.
- **Bottom line:** the four levels exist in LGD and are documented as land-region entities. **What
  the sub-district level means in any named state is not established as a configured value for any
  of the 36 states/UTs.** LGD documents that this is configured per state, but no retrieved
  document or file publishes the configured values. **One exception needs your ruling:** the 2017
  manual's help text names Rajasthan with the local term तहसील (claim 6a).
- **Status:** evidence for maintainer review. This record decides nothing. ADR-0006 and ADR-0007
  are unchanged, and `level_mapping_unverified` stays the outcome for sub-district designators.

## Sources

"Manual" below is L5. Its title page restricts reproduction without permission from the Director
General, NIC, so this record cites page numbers and keeps quotes short. The PDF is not committed.

| # | URL | SHA-256 of saved response | What it is |
|---|---|---|---|
| L1 | https://lgdirectory.gov.in/ | `e5b86d2581a34da00775e45601cf6af4e903097a1947d540d42ee768f8dda848` (one saved response; the page embeds a per-session token and live counts, so a re-fetch will differ) | Homepage, also read in the browser pane |
| L2 | https://lgdirectory.gov.in/aboutLGD.do | `1d03a42cfec449cab2ebdde926e5f5b28220df5d26d280ce37f2ba0f98c2efec` | About LGD |
| L3 | https://lgdirectory.gov.in/downloadDirectory.do | `b757e0187f6d672768ece54d985f6d2451ffc72a9d446d5edc612149e7424cc4` | Download Directory entity list |
| L4 | https://lgdirectory.gov.in/copyRightPolicy.do | `073dd98242700fde19afd02cadbebc7c1ff418711dac06013a3c542bc91828b7` | Copyright Policy |
| L5 | https://lgdirectory.gov.in/viewManual.do | `4b4b0e4b8811452c7dadf503cbd6db3df044880f52494ae39fcbca3d3a49574f` | "NICSI-LGD-USER MANUAL V6.0", Land Regions, 1,228 pages, 23,005,173 B, footer release date 03/04/2017 |
| L6 | https://lgdirectory.gov.in/viewPresentation.do | `91304a12fb2ec02e164d5099e17d023e4e429e8680b55d2b429ef786b059d616` | LGD training presentation, 242 slides |
| L7 | https://lgdirectory.gov.in/reportonStatewiseEntityDetails.do | `26aec969f885307e2a121afb98036e48f8f3dcc47627a639b0df47d61f025456` | Report on State wise Administrative Units & Panchayati Raj Institutions |
| L8 | https://lgdirectory.gov.in/globalviewsubdistrictforcitizen.do | `cb270e9eb409e15f2508046abdaee6969f8422ac17a67796c17ecc13493d94e2` | "Local Government Directory (LGD) Codes of Sub-Districts" search form; results not requested (CAPTCHA, see below) |
| L9 | https://lgdirectory.gov.in/globalviewBlockforcitizen.do | `1594c36a6bb0ad39f60820b12874506f108ac178ee27a346c9903ba3cc784d22` | "Local Government Directory (LGD) Codes of Development Blocks" search form; results not requested (CAPTCHA, see below) |
| L10 | https://dev.napix.gov.in/nic/lgd/product/1735 | `f36fdbafcaad4e212e42c4a0c7e418a011f1d3e0be391b5d2fd83edef5edb75e` | NAPIX LGD API product listing |
| L11 | https://dev.napix.gov.in/nic/lgd/product/1723 | `eec084d8a9eb7a9f4d344e37ab2c056c4668bc0f4325eeb6f1829fa213cd7de4` | NAPIX Miscellaneous API product listing |
| L12 | https://lgdirectory.gov.in/rptStatePanchayats.do | `8e5281c0068b485d3dc5073b4810433b60edaf6704741218dbde8b9293f4edbe` (the CAPTCHA page only) | Homepage menu "Report on State Panchayat Set-up"; the CAPTCHA page is headed "Codes of State Panchayats". Report **not read** |
| L13 | Pinned `All_Sub_Districtof_India_2026-10-03_19-56-24.xlsx` (ADR-0004) | `ed0c225a6bdee0b7a94f6ebb06d1b041eebe5dc279f0d13c6e6fb837b6998566` (recomputed 2026-11-04, matches the manifest) | Manually retrieved snapshot; only the header row is used here |
| L14 | https://panchayat.gov.in/lgd/ | `140d324bbc8d5bac583329efe1760d358cad4ab0f195ed93843db586543c4b17` | Ministry page: a text search found no sub-district, tehsil, taluk or mandal wording |

## Evidence by level

| # | Claim | Verdict | Source | Publisher | Retrieved | Exact location | Short quote or "n/a" | Retrieved by |
|---|---|---|---|---|---|---|---|---|
| 1 | LGD treats state, district, sub-district and village as land-region entities | VERIFIED | L5 | NIC for MoPR | 2026-11-04 | Manual p. 13, glossary, "Nodes of GIS map" | "land region entity (State, District, Sub-district, and village)" | agent |
| 2 | The manual's glossary definition of a land-region entity is generic. A term search found no separate definition per level | VERIFIED (the glossary text); the negative is a search result only | L5 | NIC for MoPR | 2026-11-04 | Manual p. 12, glossary; two-column extraction, alignment read by term order | "A geographic area with a well-defined boundary." | agent |
| 3 | **State:** LGD publishes a coded state/UT level; 36 units live and in the pinned snapshot. No definition beyond claims 1–2 was found | VERIFIED (level); definition UNVERIFIED | L1, L3, ADR-0004 | MoPR | 2026-11-04 | Homepage counts; entity "All States of India"; pinned header | `State or UT` | agent |
| 4 | **District:** LGD publishes a coded district level under the state. No definition beyond claims 1–2 was found | VERIFIED (level); definition UNVERIFIED | L1, L3, L5, ADR-0004 | MoPR | 2026-11-04 | Entity "All Districts of India"; pinned header; Manual p. 83 describes the form only | `District Name(In English)` | agent |
| 5 | **Sub-district:** the local name is configured per state, in a Nomenclature of Sub District form | VERIFIED | L5 | NIC for MoPR | 2026-11-04 | Manual p. 45, §5.1.17.1 | "the name by which a sub-district within his state is called" | agent |
| 6 | The English-field help text gives Tehsil as an example and names no state | VERIFIED | L5 | NIC for MoPR | 2026-11-04 | Manual pp. 46, 49, 51, field 1 | "Sub district in some state is called Tehsil" | agent |
| 6a | The local-language help text, in the next row, names one state. It is a 2017 help example, not a shown configured value, and gives no block-equivalence value | VERIFIED (the text exists; seen on the rendered page). **Whether it verifies Rajasthan under ADR-0007 §8: maintainer ruling** | L5 | NIC for MoPR | 2026-11-04 | Manual pp. 46, 49, 51, field 2 | "called तहसील in local language in Rajasthan" | agent |
| 6b | The form's sample screenshots show other sample values with no state named, so they verify nothing per state | VERIFIED by a verifier's reading of rendered pages; the agent viewed only the p. 46 crop | L5 | NIC for MoPR | 2026-11-04 (read 2026-11-05) | Figs 5.1.17.1.1, 5.1.17.1.2, 5.1.17.2.1–3: Tehsil/Tehsil/No; SubDistrict/Upzilla/No | n/a | agent |
| 7 | Each state records whether blocks exist and whether block and sub-district share a definition; if so they are treated as one | VERIFIED (the mechanism) | L5 | NIC for MoPR | 2026-11-04 | Manual pp. 45–48, §5.1.17.1 | "Is definition of the block and sub-district is same?" | agent |
| 8 | Sub-district and Development Block are separate published entities | VERIFIED | L1, L3, L8, L9 | MoPR | 2026-11-04 | Entity lists; homepage counts 7,112 and 7,328 | n/a | agent |
| 9 | LGD's own report labels the level with several generic names | VERIFIED; maps no state to a tier | L7 | MoPR | 2026-11-04 | Column header | "No. of Sub-Districts/ Tehsils/ Mandals" | agent |
| 10 | NAPIX describes the hierarchy with a generic gloss | VERIFIED; maps no state to a tier | L10 | NIC / MoPR | 2026-11-04 | "State–District–Subdistrict–Block–Village API" description | "Subdistrict (Tehsil/Taluk)" | agent |
| 11 | **The configured nomenclature and block-equivalence value for any named state** | **UNVERIFIED, all 36 states/UTs** (for Rajasthan see 6a) | L3, L5, L8, L10, L11, L13 | — | 2026-11-04 | No such column in the pinned header (L13); no such output in the NAPIX listings read. `nomenclatureEnglish` in L11 belongs to `activeLocalGovernmentSetupOfState`, whose other outputs concern local-body types. That it is a different field is an inference: the API was not called | n/a | agent |
| 12 | **Village:** LGD publishes a coded village level under the sub-district, with name and census code fields | VERIFIED (level) | L3, L5 | NIC for MoPR | 2026-11-04 | Manual p. 188, "Create Village"; entity "All Villages of India" | "name of village, census code, GIS node" | agent |
| 12a | The Create Village form has a Village Status field defined by "MDDS", which the manual does not expand and this record has not read | VERIFIED (the field); what MDDS says UNVERIFIED | L5 | NIC for MoPR | 2026-11-04 (read 2026-11-05) | Manual p. 191; the Village Status field recurs elsewhere, for example pp. 196, 216, without the term | "according to the MDDS of Land Region entities" | agent |
| 13 | LGD's village count combines rural and urbanised villages; the homepage also splits inhabited, un-inhabited and forest villages | VERIFIED | L1, L7 | MoPR | 2026-11-04 | L7 footnote to "* No. of Villages" | "cumulative total of Rural and Urbanised villages" | agent |
| 14 | Whether an LGD village is a revenue village, and which categories the pinned Pincode to Village file includes | UNVERIFIED | L5, L13 | — | 2026-11-04 | The phrase "Revenue Village" has 0 hits in the manual's extracted text. The file has no category column (ADR-0004) | n/a | agent |

### Limits of this evidence

- **The manual is dated.** It was released on 03/04/2017, so the current form may differ. Apart
  from the Rajasthan help example (claim 6a), no per-state value was found in the text searched.
- **Text search, not a full read.** The 1,228-page manual was searched for level terms, and the
  cited pages were read. A definition elsewhere under other wording would have been missed.
  Screenshots are not searchable. `pdftotext` also dropped Devanagari on these pages, which is why
  the first version of this record missed claim 6a. A verifier caught it with PyMuPDF. Other
  Indic-script text may have been missed the same way.
- **Live counts differ from the pin.** On 2026-11-04 the homepage shows 790 districts, 7,112
  sub-districts and 677,662 villages. The pinned snapshots of 2026-10-03 have 784, 7,092 and
  672,619. The pin stands (ADR-0004). This is recorded, not corrected. The village figures may
  also differ in scope (claim 14).
- **Counts are not used as evidence of meaning**, as ADR-0007 §8 requires.

## Access problems

| URL | Problem | Date | Action requested from maintainer |
|---|---|---|---|
| https://lgdirectory.gov.in/rptStatePanchayats.do | CAPTCHA. Not attempted. Whether this report holds sub-district nomenclature is UNKNOWN; its title suggests panchayat set-up only | 2026-11-04 | Open it in a browser and say whether a per-state sub-district name or block-equivalence value appears |
| https://lgdirectory.gov.in/globalviewsubdistrictforcitizen.do, `globalviewBlockforcitizen.do`, `globalviewdistrictforcitizen.do` and `globalviewvillageforcitizen.do` | The search forms ask for a CAPTCHA. No search was submitted, so per-unit detail pages were not seen. Whether they show a tier, type or definition is UNKNOWN | 2026-11-04 | Search one unit per level, for each state of interest, and say whether a type or nomenclature appears |
| https://lgdirectory.gov.in/downloadDirectory.do, entity "All Villages of India With Village Category" | Downloads need a CAPTCHA (`lgd_subdistricts.toml`). Not attempted. This is the direct lead on claim 14 | 2026-11-04 | Download it to `data/raw/lgdirectory.gov.in/`, not committed, if village categories matter |
| "User Manual for Revenue Department" and "LGD SOPs", homepage panel "SUPPORTING DOCUMENTS" | Not obtained, so their content is UNKNOWN. The direct guess `viewManualRevenue.do` returned 404, the `cbt.htm` links returned "Session Timed Out" to a script, and the panel could not be reopened in the browser pane | 2026-11-04 | Download both from the panel and share them |
| https://lgdirectory.gov.in/downLoadCBT.do | The training file is larger than 135 MB and the transfer hit a 40 s limit. The partial file was deleted and not read | 2026-11-04 | None, unless the two documents above are silent |
| `lgdDwrInitialService` (the portal's internal call) | A scripted call was refused by the session's permission check. It was not retried by other means. Only visible menu items and plain links were used after that | 2026-11-04 | None |

`viewManual.do` and `viewPresentation.do` were found by pattern from the `viewManualGIS.do` link
the portal shows. They need no CAPTCHA or login. The documents' own title pages identify them.

## Open questions for the maintainer

Your decision at this gate is one of these. They can be combined, and none is taken here.

1. **Freeze as unverified.** The node's notes allow this. Every sub-district designator stays
   `level_mapping_unverified` until a state has evidence. This costs nothing now and limits
   `subdistrict` linking later.
2. **Fetch the blocked documents** listed above, then re-run this node for the states of interest.
3. **Ask LGD.** The draft below is not sent. Nothing is recorded as answered until a reply is
   received and cited.

Also rule on two ADR-0007 §8 readings:

- Whether the Rajasthan help example (claim 6a) counts as LGD documentation for Rajasthan. Until
  you rule, this record treats it as not verifying Rajasthan, because it is an example rather than
  a shown configured value.
- Whether the manual's mechanism (claims 5 and 7) may count as LGD-side evidence once per-state
  values are obtained. This record assumes it may.

### Draft request to LGD: not sent

- To: lgdirectory@gov.in (the contact recorded in ADR-0003)
- Drafted: 2026-11-04. Status: draft, not sent. The project description is the maintainer's to
  confirm.

> **Subject:** State-wise nomenclature of sub-districts in the Local Government Directory
>
> Dear LGD team,
>
> I maintain Pata, an open-source research project on Indian addresses that uses LGD's published
> directory as its reference gazetteer, with acknowledgement under the LGD Copyright Policy.
>
> The LGD User Manual (Land Regions, V6.0, §5.1.17) describes a "Nomenclature of Sub District"
> setting for each State, with the fields "Is Block Exist" and "Is definition of the block and
> sub-district is same?".
>
> Could you please tell me:
>
> 1. Whether the configured values of these fields are published for each State/UT, and where.
> 2. If they are not published, whether you could share them for research use, and on what terms.
> 3. Whether an LGD "village" always means a revenue village, or how it should be understood.
>
> Thank you for your time.
>
> Regards,
> [Name]
> [Project link and contact details]
