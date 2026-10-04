# ADR-0004: LGD portal XLSX downloads as the v0 LGD source

- **Status:** Accepted
- **Date:** 2026-10-03
- **Deciders:** Project maintainer
- **Amends:** ADR-0002 (decision 1 for the four LGD sources; decision 7, standard library only).
  ADR-0005 records that it also amends ADR-0002 decisions 5 and 8 for these sources.
- **Corrected:** 2026-10-04 (ADR-0005). Wording only: section 3 and the Consequences
  described the ingestion change as pending although it landed in the same commit
  (e8a6420). The decisions are unchanged.

## Context

ADR-0002 chose four Ministry of Panchayati Raj (LGD) resources on data.gov.in as
v0 sources. None could be acquired:

- `api.data.gov.in` refuses TCP connections on ports 443 and 80 (checked 2026-10-03
  from an Indian ISP and from an overseas network, so the cause is server-side).
- `www.data.gov.in` file URLs sit behind an Akamai bot challenge, and its download
  form's CAPTCHA did not render for the maintainer.
- NAPIX needs LGD's prior approval (ADR-0003, still pending).

The primary publisher's portal, lgdirectory.gov.in, offers the same entities from
its Download Directory page (`downloadDirectory.do`) as PDF, HTML, XLS or ODT
reports behind a human CAPTCHA. On 2026-10-03 the maintainer downloaded five
reports manually in a browser:

| Report (portal entity) | File | Bytes | SHA-256 | Data rows |
|---|---|---|---|---|
| All States of India | `All_Stateof_India_2026-10-03_19-54-11.xlsx` | 5,651 | `0343bd004bf6d45992d658501dfde61be9185813d7f7d7ffaa6cf10ab4a0173c` | 36 |
| All Districts of India | `All_Districtof_India_2026-10-03_19-55-41.xlsx` | 34,834 | `59bb5756c9c4666da232edd1a5484c9e397f48c32d62ef1fab69021ddc06dc83` | 784 |
| All Sub-Districts of India | `All_Sub_Districtof_India_2026-10-03_19-56-24.xlsx` | 410,582 | `ed0c225a6bdee0b7a94f6ebb06d1b041eebe5dc279f0d13c6e6fb837b6998566` | 7,092 |
| Pincode to Village Mapping | `Pincodeto_Village_Mapping_2026-10-03_19-57-07.xlsx` | 31,941,542 | `dd9f901c7e521368f7872e1408217b91d1868038ea461f72f2173da3054503ef` | 672,619 |
| Pincode to Urban Mapping | `Pincodeto_Urban_Mapping_2026-10-03_19-58-00.xlsx` | 281,128 | `a4f9c3511698550627ce559fc83134a831388ea6b0af9f6862dd47c38576e811` | 7,238 |

A read-only inspection (2026-10-03) found:

- **Layout.** Each file is an XLSX workbook with one sheet. Row 1 holds the report
  title (e.g. `All Districts of India`) in column A, row 2 holds the headers, and
  data starts at row 3. There are no footer rows, empty rows, empty columns or
  ragged rows, and `S.No.` runs 1…n without gaps.
- **Numbers.** Every code and PIN is a numeric cell. All values are whole numbers,
  but they are read back as floats (`35.0`, `744301.0`).
- **No version inside the files.** The only report timestamp is the one in the
  filename, which is the portal's generation time (IST).
- **Headers** (exact, as published):
  - States: `S.No.`, `State Code`, `State Version`, `State Name (In English)`,
    `State Name (In Local)`, `Census 2001 Code`, `Census 2011 Code`, `State or UT`
  - Districts: `S.No.`, `State Code`, `State Name (In English)`, `District Code`,
    `District Name(In English)`, `Census 2001 Code`, `Census 2011 Code`
  - Sub-Districts: `S.No.`, `State Code`, `State Name`, `District Code`,
    `District Name`, `Sub-district Code`, `Sub-district Version`,
    `Sub-district Name`, `Census 2001 Code`, `Census 2011 Code`
  - Pincode to Village: `S.No.`, `State Code`, `State Name`, `District Code`,
    `District Name`, `SubDistrict Code`, `SubDistrict Name`, `Village Code`,
    `Village Name`, `Pincode`
  - Pincode to Urban: `S.No.`, `State Code`, `State Name`, `Localbody Code`,
    `Localbody Name`, `Localbody Type Name`, `Pincode`
- **Consistency of the four core files.** LGD codes are unique at every level.
  Every parent exists. The village file's state, district and sub-district codes
  and names agree exactly with the level files. There are no exact duplicate rows
  and all PINs are 6 digits with a non-zero first digit.
- **Village → PIN.** Each village code appears exactly once, so this snapshot gives
  one PIN per village. One PIN covers many villages (median 19, maximum 1,308 for
  834001). 1,889 PINs span more than one district and 27 span two states.
  Chandigarh, 6 districts and 30 sub-districts (mostly city tehsils) have no villages.
- **Local names.** Only the States file has a local-name column. In it, 28 of 36
  values are the English name in capitals, one (Ladakh) is English, and 7 are in an
  Indic script.
- **Urban mapping.** Urban local bodies carry only a state code (no district), and
  4,958 local-body codes are numerically equal to village codes. Several PINs look
  like data-entry placeholders: 313325 is mapped to 214 Rajasthan municipalities
  across the state, and 328024 and 328027 to 184 each. Names and types have
  trailing spaces and tabs and inconsistent casing.

**Licence.** The LGD portal's Copyright Policy (`copyRightPolicy.do`, read
2026-10-03) states: "Material featured on this site may be reproduced free of
charge in any format or media without requiring specific permission. This is
subject to the material being reproduced accurately and not being used in a
derogatory manner or in a misleading context. Where the material is being
published or issued to others, the source must be prominently acknowledged."
Material identified as third-party copyright is excluded. The policy prescribes no
acknowledgement wording. These reports are LGD's own directory data, so the
third-party exclusion does not apply.

## Decision

### 1. Source

The four core v0 LGD sources are the LGD portal reports **All States of India**,
**All Districts of India**, **All Sub-Districts of India** and **Pincode to Village
Mapping**, downloaded from https://lgdirectory.gov.in/downloadDirectory.do. They
replace the data.gov.in resources named in ADR-0002 for these four manifests. The
publisher is unchanged: Ministry of Panchayati Raj, Government of India (Local
Government Directory).

Retrieval is manual: a person downloads each report as XLS (the portal delivers
`.xlsx`) and solves the CAPTCHA. Pata does not automate the portal.

### 2. Licence and acknowledgement

The basis for reuse is the LGD Copyright Policy quoted above, not GODL-India.
Pata must:

- reproduce the data accurately. Derived tables keep published values. Every
  derivation is documented, and quality findings are reported, never silently fixed.
- not use it in a derogatory or misleading way, and not imply endorsement by LGD
  or the Ministry.
- acknowledge the source prominently wherever data or derived tables are published.
  Until LGD supplies wording, the acknowledgement is:

  > Source: Local Government Directory (LGD), Ministry of Panchayati Raj,
  > Government of India, https://lgdirectory.gov.in/. Report "{report name}",
  > generated {portal timestamp}, retrieved {retrieval date}. Reproduced under the
  > LGD Copyright Policy (https://lgdirectory.gov.in/copyRightPolicy.do).

Raw files stay out of git (ADR-0001).

### 3. Pinned snapshots

The SHA-256 and data-row counts in the table above are the pinned v0 snapshots for
States, Districts, Sub-Districts and Pincode to Village Mapping. Row counts exclude
the title and header rows. `retrieved` is 2026-10-03. Each manifest also records the
portal report name, its generation timestamp (from the filename) and the title text
in row 1. The build refuses a file whose checksum, row count, row-1 title or row-2
header differs.

The raw files keep their original portal filenames and live under
`data/raw/lgdirectory.gov.in/`.

### 4. Reading XLSX: decoding, not normalization

- The first worksheet is read. Row 1 must equal the recorded report title. Row 2 is
  the header and must match the manifest's column mapping exactly. Data starts at row 3.
- A numeric cell holding a whole number is decoded to its integer string
  (`35.0` → `"35"`, `744301.0` → `"744301"`).
- A numeric cell holding a non-integral value in a code or PIN column is an error.
  It is never rounded. None exist in the pinned snapshots.
- Text cells are passed through exactly as stored, including surrounding
  whitespace, tabs and non-ASCII characters. An empty cell becomes `""`.

This step undoes the storage format so that values equal what LGD published. It
is not normalization. `pata.normalize.name_key` remains the only normalization,
used only for keys and collision checks (ADR-0002).

### 5. XLSX reader: openpyxl

The ingestion change adds **openpyxl** (`>=3.1,<4`, MIT licence) as a runtime
dependency, read with `load_workbook(read_only=True, data_only=True)`. This amends
ADR-0002 decision 7 ("standard library only") for this one purpose.

Reasons:

- It is the de facto Python XLSX reader, mature and maintained. Version 3.1.5
  streamed the 672,619-row village file without problems during inspection.
- A standard-library reader (`zipfile` plus `xml.etree`) would have to reimplement
  shared strings, inline strings, sparse cell references and cell types. That is
  more code for Pata to own and test, for a format detail.
- It is used only to read cells. CSV writing, hashing and manifest parsing stay on
  the standard library, and output is still byte-reproducible.

openpyxl warns that these workbooks have "no default style". This is harmless for
reading values.

### 6. Column use

The level files map to the canonical `admin_unit` columns: `code`, `name`,
`parent_code`. `name_local` stays **unmapped** in v0. The States file's
`State Name (In Local)` is mostly English in capitals, and mapping it would
misrepresent it as a local-language name.

`State Version`, `Sub-district Version`, `Census 2001 Code`, `Census 2011 Code`
and `State or UT` are not ingested in v0. Versions and history are already out of
scope (ADR-0002), and a Census code of `0` means "none".

### 7. Deferred

- **Pincode to Urban Mapping** is not part of the v0 gazetteer. Its file is
  recorded above for provenance only. It is deferred because:
  - it contains placeholder-like PIN assignments (one PIN mapped to hundreds of
    municipalities), which need a dedicated quality check before use.
  - urban local bodies need their own ID namespace (their codes overlap village
    codes) and a hierarchy decision, since the file gives no district parent.

  Including it needs a new ADR.
- **India Post** (`dop_pincode_directory`) stays deferred. data.gov.in is still
  its only openly licensed first-party source.
- **NAPIX** (ADR-0003) is no longer needed to acquire the v0 LGD snapshots. ADR-0003
  stays open for possible automated refreshes later.

## Consequences

- The four LGD manifests, the gazetteer loader, `docs/gazetteer.md` and the tests
  were changed to these sources in the same commit as this ADR (e8a6420).
- Refreshing a snapshot is a manual browser download followed by an explicit
  manifest diff. Pata cannot fetch these reports unattended.
- Quality output expected from these snapshots:
  - about 11,260 `name_key_collision` warnings (distinct villages that share a
    name within one sub-district, which LGD allows). This was an approximate
    expectation, kept here as history. The first build (e8a6420) measured 11,382
    groups. ADR-0005 explains the difference, splits the warning into two codes
    and gives the current counts.
  - village names with an undocumented trailing `*` (113), census-style suffixes
    such as `(Ct)` and `(Og)`, and non-ASCII punctuation, kept as published.
  - very large PIN fan-outs (e.g. 834001 → 1,308 villages), reported, not corrected.
- `pincode_not_in_dop` cannot run while India Post is deferred.
- Urban coverage remains the known gap stated in ADR-0002.
- If LGD gives its own acknowledgement wording, it replaces the interim wording in §2.
