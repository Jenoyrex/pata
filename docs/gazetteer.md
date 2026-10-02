# Reference gazetteer (v0)

The gazetteer is Pata's reference data for administrative and postal geography.
Parsers, resolvers and benchmarks are checked against it. Sources and the reasons
for each choice are in [ADR-0002](decisions/0002-gazetteer-sources-and-schema.md).
The data policy is in [ADR-0001](decisions/0001-data-privacy-licensing-scope.md).

## Sources

| Manifest | Publisher | Provides | Field list | Resource last updated* |
|---|---|---|---|---|
| `dop_pincode_directory` | Department of Posts | post offices, PIN codes, India Post circle/region/division, district/state labels, lat/lon | from data.gov.in metadata | **03/10/2025** (stale; see below) |
| `lgd_villages_pincode` | Ministry of Panchayati Raj (LGD) | state → district → sub-district → village codes and names, village → PIN | from data.gov.in metadata | 01/09/2026 |
| `lgd_states` | Ministry of Panchayati Raj (LGD) | states/UTs | **not published; map after download** | 25/09/2026 |
| `lgd_districts` | Ministry of Panchayati Raj (LGD) | districts | **not published; map after download** | 25/09/2026 |
| `lgd_subdistricts` | Ministry of Panchayati Raj (LGD) | sub-districts (tehsil/taluk/mandal …) | **not published; map after download** | 25/09/2026 |

\* As shown in data.gov.in resource metadata, checked 2026-10-02.

**Freshness.** The PIN directory's resource note says "Data will be updated on
monthly basis", but it was last updated 03/10/2025. Do not treat it as monthly or
current.

**Two kinds of date.** Each manifest records the publisher's dates for the
resource (`resource_published`, `resource_last_updated`, and `metadata_checked`,
the day we looked) separately from Pata's download date (`snapshot.retrieved`).
These are different facts. The resource can change after we download it.

**Licence.** All five are distributed by data.gov.in. The site states that its
content is licensed under the Government Open Data License – India (GODL-India).
This was verified 2026-10-02 from the official text at https://www.data.gov.in/Godl
(details in ADR-0002). GODL allows use, adaptation, redistribution and derivative
works for lawful purposes. Its conditions:
- an attribution statement in the GODL section 5 format: *Name of Data Provider,
  Year of Publication, Name of Data, Name of Data Repository/Website, Version
  Number and/or Date of Publication, DOI/URL/URI. Published under Name of License:
  URL of License.*
- non-endorsement
- no warranty
- section 6 exemptions, including personal information

Each manifest's `attribution` follows that template, using the resource's
publication year and its last-updated date. Re-check both when a snapshot is
pinned. Pata never commits the data.

The LGD portal (lgdirectory.gov.in) has its own Copyright Policy. It allows free
reproduction with prominent acknowledgement of the source, provided the material
is reproduced accurately and not used in a derogatory or misleading way. Its
downloads are PDF/HTML/XLS/ODT behind a CAPTCHA, and v0 does not use them.

## Building

1. Download each file as described in its manifest's `retrieval` field and save it
   under `data/raw/` at the manifest's `raw_file` path.
2. Print checksums, row counts and headers:
   ```bash
   uv run scripts/build_gazetteer.py --snapshot-info
   ```
3. Paste the `[snapshot]` values into each manifest. For the three LGD level files,
   fill `[columns]` from the printed header. Header matching ignores case and
   surrounding whitespace.
4. Build:
   ```bash
   uv run scripts/build_gazetteer.py        # writes data/processed/gazetteer/
   ```

Exit codes:
- `0`: built.
- `1`: quality errors were found; see `issues.csv`. No tables are written.
- `2`: a source is unusable (missing, checksum or row-count mismatch, unmapped column).

A downloaded file that differs from the pinned snapshot is refused. Updating a
snapshot is always an explicit manifest change in git.

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

**`build_info.json`**: build status, pata version, git commit, source snapshots
(checksum, rows, retrieval date, licence), table row counts and issue counts.

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
| `name_key_collision` (admin) | warning | Sibling units have the same normalized name. This can be legitimate. |
| `cross_source_name_mismatch` | warning | The same LGD code is named differently in two LGD files |
| `unparseable_coordinate` | warning | Coordinate couldn't be parsed and was blanked |
| `coordinate_outside_india_bbox` | warning | Point lies outside a rough lat/lon box around India (not a boundary) |
| `pincode_not_in_dop` | warning | A PIN that LGD lists for a village doesn't appear in the India Post directory |
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
only for duplicate and collision detection and for post-office IDs. Published names
are never overwritten.

## Known limitations

- No urban localities or towns (LGD urban local bodies are not ingested).
- LGD entity versions and history (splits, renames) are not modelled.
- India Post district/state labels are not resolved to LGD. That is a future,
  measured task.
- Post-office coordinates are unverified and not suitable as geocoding ground truth.
- The India Post PIN directory was last updated 03/10/2025 (per data.gov.in
  metadata, checked 2026-10-02). Offices and PIN codes created or changed since
  then may be missing or out of date.
