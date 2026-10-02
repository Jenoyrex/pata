# Reference gazetteer (v0)

The gazetteer is Pata's reference data for administrative and postal geography.
Parsers, resolvers and benchmarks are checked against it. Sources and the reasons
for each choice are in [ADR-0002](decisions/0002-gazetteer-sources-and-schema.md).
The data policy is in [ADR-0001](decisions/0001-data-privacy-licensing-scope.md).

## Sources

| Manifest | Publisher | Provides | Field list |
|---|---|---|---|
| `dop_pincode_directory` | Department of Posts | post offices, PIN codes, India Post circle/region/division, district/state labels, lat/lon | from data.gov.in metadata |
| `lgd_villages_pincode` | Ministry of Panchayati Raj (LGD) | state → district → sub-district → village codes and names, village → PIN | from data.gov.in metadata |
| `lgd_states` | Ministry of Panchayati Raj (LGD) | states/UTs | **not published; map after download** |
| `lgd_districts` | Ministry of Panchayati Raj (LGD) | districts | **not published; map after download** |
| `lgd_subdistricts` | Ministry of Panchayati Raj (LGD) | sub-districts (tehsil/taluk/mandal …) | **not published; map after download** |

All five are distributed by data.gov.in under GODL-India, which allows reuse with
attribution. Each manifest holds the attribution text. Pata never commits the data.

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
- The GODL-India terms were taken from secondary summaries. The official page
  couldn't be machine-read (see ADR-0002).
