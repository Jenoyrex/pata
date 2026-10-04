# Reference gazetteer (v0)

The gazetteer is Pata's reference data for administrative and postal geography.
Parsers, resolvers and benchmarks are checked against it. Sources and the reasons
for each choice are in [ADR-0002](decisions/0002-gazetteer-sources-and-schema.md),
amended by [ADR-0004](decisions/0004-lgd-portal-xlsx-snapshots.md) for the LGD
sources. Build provenance and warning codes are in
[ADR-0005](decisions/0005-gazetteer-version-and-warning-taxonomy.md). The data
policy is in [ADR-0001](decisions/0001-data-privacy-licensing-scope.md).

## Sources

| Manifest | Publisher | Provides | Snapshot | Data rows |
|---|---|---|---|---|
| `lgd_states` | Ministry of Panchayati Raj (LGD) | states/UTs | LGD portal report "All States of India", generated 2026-10-03 19:54:11 IST | 36 |
| `lgd_districts` | Ministry of Panchayati Raj (LGD) | districts | "All Districts of India", 2026-10-03 19:55:41 IST | 784 |
| `lgd_subdistricts` | Ministry of Panchayati Raj (LGD) | sub-districts (tehsil/taluk/mandal …) | "All Sub-Districts of India", 2026-10-03 19:56:24 IST | 7,092 |
| `lgd_villages_pincode` | Ministry of Panchayati Raj (LGD) | state → district → sub-district → village codes and names, village → PIN | "Pincode to Village Mapping", 2026-10-03 19:57:07 IST | 672,619 |
| `dop_pincode_directory` | Department of Posts | post offices, PIN codes, India Post circle/region/division, district/state labels, lat/lon | **deferred** (not built; see below) | – |

The four LGD snapshots were downloaded manually from
https://lgdirectory.gov.in/downloadDirectory.do on 2026-10-03. Their SHA-256
checksums are pinned in the manifests and in ADR-0004. The portal timestamp in each
file name is the only version information the reports carry.

**Deferred.** The India Post PIN directory could not be retrieved from data.gov.in,
its only openly licensed first-party source. Its manifest stays for provenance but
carries `deferred = "…"`. The build skips it, writes `post_office.csv` and
`pincode.csv` with headers only, and does not run `pincode_not_in_dop`. LGD's
"Pincode to Urban Mapping" report is also deferred (ADR-0004 section 7). It has no
manifest.

**Licence.** The LGD sources are reused under the LGD portal's Copyright Policy
(https://lgdirectory.gov.in/copyRightPolicy.do), not GODL-India. Material "may be
reproduced free of charge in any format or media without requiring specific
permission", provided that:
- it is reproduced accurately
- it is not used in a derogatory manner or a misleading context
- the source is prominently acknowledged where the material is published or
  issued to others

Each LGD manifest's `attribution` holds the acknowledgement in the interim wording
of ADR-0004 section 2. Pata never commits the data. The deferred India Post
manifest still records data.gov.in's GODL-India terms (details in ADR-0002).

## Building

1. Download each LGD report as described in its manifest's `retrieval` field. Keep
   the portal's file name and save it under `data/raw/` at the manifest's
   `raw_file` path (`data/raw/lgdirectory.gov.in/…`). Do not open and re-save it in
   a spreadsheet program, because that changes the checksum.
2. Print checksums, row counts, titles and headers:
   ```bash
   uv run scripts/build_gazetteer.py --snapshot-info
   ```
3. A new snapshot is pinned by updating `[snapshot]`, `title`, `header` and the
   report fields in the manifest, together with the ADR that records it.
4. Build (about two minutes for the village file):
   ```bash
   uv run scripts/build_gazetteer.py        # writes data/processed/gazetteer/
   ```

Exit codes:
- `0`: built.
- `1`: quality errors were found; see `issues.csv`. No tables are written.
- `2`: a source is unusable (missing, checksum, row-count, title or header mismatch,
  unmapped column, undecodable cell).

A downloaded file that differs from the pinned snapshot is refused. Updating a
snapshot is always an explicit manifest change in git.

### Reading XLSX sources

LGD portal reports are XLSX workbooks (read with openpyxl, ADR-0004 section 5).
Only the first worksheet is read:
- row 1 is the report title and must equal the manifest's `title`
- row 2 is the header and must equal the manifest's `header` exactly
- data starts at row 3, and `[columns]` maps canonical names to exact header names

Cells are **decoded, not normalized** (ADR-0004 section 4):
- A numeric cell holding a whole number becomes its integer string (`35.0` → `"35"`).
- Any other number, and any non-text, non-numeric cell, stops the build. Nothing
  is rounded.
- Text cells are kept exactly as stored, including surrounding whitespace and
  non-ASCII characters.
- Empty cells become `""`.

CSV sources (India Post, when it is built) are read as UTF-8, and their values are
stripped of surrounding whitespace.

## Output tables

All tables are UTF-8 CSV, sorted, with LF line endings, so the same snapshot
produces the same bytes. Empty string means "not provided by the source".

**`admin_unit.csv`** (LGD only)

| Column | Meaning |
|---|---|
| `id` | `lgd:{level}:{lgd_code}` |
| `level` | `state`, `district`, `subdistrict`, `village` |
| `lgd_code` | LGD code as published (digits) |
| `name` | English name as published |
| `name_local` | Local-language name, if the level file provides one |
| `parent_id` | `id` of the parent unit (empty for states) |
| `source` | Manifest id that provided the row |

**`post_office.csv`** (India Post only)

| Column | Meaning |
|---|---|
| `id` | `dop:po:{pincode}:{name_key(office_name)}`, a derived ID because India Post publishes none |
| `pincode`, `office_name`, `office_type`, `delivery` | As published |
| `circle`, `region`, `division` | India Post's own postal hierarchy, which is not administrative |
| `district_name`, `state_name` | India Post's labels as raw strings, **not linked to LGD** |
| `latitude`, `longitude` | As published. Unparseable values are blanked and logged. Accuracy unknown. |
| `source` | Manifest id |

**`pincode.csv`**: one row per PIN code, derived from `post_office`, with
`office_count` and the distinct `district_names` / `state_names` (pipe-separated, raw).

**`village_pincode.csv`**: the village → PIN links stated by LGD
(`village_id`, `pincode`, `source`). A village can have more than one PIN.

**`issues.csv`**: every quality finding (`severity`, `code`, `entity_id`, `message`).

**`build_info.json`** (ADR-0005):
- `status`, `pata_version`, table row counts and issue counts
- `sources`: each source snapshot's checksum, rows, retrieval date and licence
- `gazetteer_version`: SHA-256 of the sorted SHA-256s of the built source
  snapshots. It identifies the exact input snapshots, independent of code and
  build time. Cite it whenever data is derived from the gazetteer.
- `git_commit` and `git_dirty`: the code that ran. `git_dirty` is `true` when the
  tree has uncommitted changes or untracked, non-ignored files, so the tables
  can't be attributed to `git_commit` alone. It is `null` when git state can't be
  read. A dirty or unknown state also prints a warning.
- `outputs`: the SHA-256 of every file written in this build

## Quality checks

| Code | Severity | Meaning |
|---|---|---|
| `missing_required` | error | Required field (code, name, parent, office name) is empty |
| `invalid_lgd_code` | error | LGD code is not all digits |
| `invalid_pincode` | error | Not a 6-digit PIN with a non-zero first digit |
| `conflicting_duplicate_id` | error | Two rows share an ID but differ |
| `name_key_collision` (post office) | error | Two differently written office names in one PIN normalize to the same key |
| `broken_parent` | error | Parent unit doesn't exist |
| `unknown_admin_unit` | error | The village file names a state, district or sub-district that is missing from its level file |
| `hierarchy_mismatch` | error | The village file and a level file disagree about a unit's parent |
| `exact_duplicate_row` | warning | Identical row repeated; one copy is kept |
| `same_name_siblings` | warning | Sibling units (same level, same parent) have byte-identical published names. LGD allows this. One warning per repeated name. |
| `variant_name_siblings` | warning | Sibling units whose published names differ but share one `name_key` (e.g. `Haripura` / `Haripura.`). They may be distinct units or one unit entered twice; the source can't tell. One warning per group. |
| `cross_source_name_mismatch` | warning | The same LGD code is named differently in two LGD files |
| `unparseable_coordinate` | warning | Coordinate couldn't be parsed and was blanked |
| `coordinate_outside_india_bbox` | warning | Point lies outside a rough lat/lon box around India (not a boundary) |
| `pincode_not_in_dop` | warning | A PIN that LGD lists for a village doesn't appear in the India Post directory. Skipped while India Post is deferred |
| `missing_coordinate`, `village_row_without_pincode` | info | Aggregate counts |
| `pincode_spans_states` | info | One PIN's offices carry more than one state label |

Checks that happen before any tables are built (exit code 2):
- the file matches its pinned SHA-256 checksum
- the parsed row count equals the pinned count
- every required column is mapped and present in the header
- the manifest has every provenance field required by ADR-0001

## Normalization

`pata.normalize.name_key` is the only normalization step:
- Unicode NFKC, then casefold
- punctuation, symbols and whitespace collapsed to single spaces
- format characters such as ZWJ removed

It is script-agnostic, and Indic combining marks are preserved. It does no
abbreviation expansion, transliteration or spelling correction. The key is used
only for duplicate and sibling-name detection and for post-office IDs. Published names
are never overwritten.

## Known limitations

- No urban localities or towns. LGD urban local bodies and the "Pincode to Urban
  Mapping" report are not ingested (deferred by ADR-0004).
- No India Post data in v0: `post_office.csv` and `pincode.csv` are empty and PINs
  are not cross-checked against India Post.
- LGD entity versions and history (splits, renames) are not modelled. Census codes
  are not ingested.
- No local-language names. `name_local` is empty: the only candidate, the States
  file's "State Name (In Local)", is mostly English in capitals.
- Snapshot refreshes are manual, because the LGD portal requires a CAPTCHA.
- India Post district/state labels are not resolved to LGD. That is a future,
  measured task.
- Post-office coordinates are unverified and not suitable as geocoding ground truth.
- The India Post PIN directory was last updated 03/10/2025 (per data.gov.in
  metadata, checked 2026-10-02). If it is built later, offices and PIN codes created
  or changed since then may be missing or out of date.

## v0 snapshot quality (2026-10-03)

The build of the pinned snapshots exits `0` with no errors.
`gazetteer_version` is `bf4a8b5d35130e7c3b94c6e4de812b3fd6deeb059497af22aac178642c2c2c78`.

- `admin_unit`: 680,531 rows (36 states, 784 districts, 7,092 sub-districts,
  672,619 villages). `village_pincode`: 672,619 rows. Every village has exactly one
  PIN in this snapshot.
- 11,390 warning records, all at village level, all about siblings under one
  sub-district. No errors. The names are not changed.
  - 11,258 `same_name_siblings` records: one per name shared by distinct
    village codes under one sub-district. LGD allows this.
  - 132 `variant_name_siblings` records: one per group whose spellings differ
    only in case, punctuation, spacing or Unicode form.
  - The records cover 11,382 distinct name collision groups (equal `name_key`
    under one parent). 8 groups contain both an identical pair and a variant
    spelling, so they get one record of each code: 11,390 − 11,382 = 8 (ADR-0005).
  - ADR-0004's "about 11,260" was a pre-build estimate. It is historical and not
    a measured result.
- Processed tables built before ADR-0005 lack `gazetteer_version`, `git_dirty`
  and `outputs`, and use the old warning code. Rebuild them from a clean checkout.
- Not flagged by a check, but visible in the data:
  - one PIN can cover many villages (median 19, maximum 1,308 for 834001)
  - 1,889 PINs span more than one district and 27 span two states
  - 113 village names end in an undocumented `*`
  - some names carry census-style suffixes (`(Ct)`, `(Og)`, `(Part)`) or non-ASCII
    punctuation and diacritics
  - Chandigarh, 6 districts (including Mumbai, Kolkata and three Delhi districts)
    and 30 sub-districts have no villages in the mapping
