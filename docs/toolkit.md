# Pata gazetteer toolkit: user guide (version 1)

Version 1 of Pata is a toolkit for building an all-India reference gazetteer from the Local
Government Directory (LGD), under [ADR-0009](decisions/0009-version-1-gazetteer-toolkit.md).

It contains **no address dataset, model, benchmark or metric**. It does not parse, resolve or
geocode addresses, and it is not PataBench, which moves to version 2. The toolkit is checked
by its tests and by the build's quality checks.

## Install

You need [uv](https://docs.astral.sh/uv/) and Python 3.12.

```bash
git clone https://github.com/Jenoyrex/pata.git
cd pata
uv sync
```

## Build from your own LGD snapshot

No data ships with Pata. The manifests in `data/manifests/` pin the maintainer's exact LGD
files, and a build refuses any file that differs. A new download will differ, so you re-pin
the four LGD manifests to your own files first: `lgd_states`, `lgd_districts`,
`lgd_subdistricts` and `lgd_villages_pincode`.

1. Download each report as its manifest's `retrieval` field describes. The portal uses a
   CAPTCHA, so this is manual. Keep the portal's file name, save it under
   `data/raw/lgdirectory.gov.in/`, and do not open and re-save it in a spreadsheet program.
2. In each manifest, set `raw_file` to `lgdirectory.gov.in/<your file name>`. The path is
   relative to `data/raw/`, so a bare file name is not found.
3. Print the values to pin:
   ```bash
   uv run scripts/build_gazetteer.py --snapshot-info
   ```
4. In each manifest, copy the printed `[snapshot]` values (`retrieved`, `sha256`, `rows`). If
   the printed title or header differs, update `title` and `header`, and check that `[columns]`
   still names the right headers. Update `report_generated` and `attribution` to match.
5. Commit your manifest changes. Otherwise the build records `git_dirty = true`.
6. Build, which takes about two minutes for the village file:
   ```bash
   uv run scripts/build_gazetteer.py
   ```

Exit codes: `0` built; `1` quality errors were found, see `issues.csv`, and no tables were
written; `2` a source is unusable, such as a missing file or a checksum mismatch.

Your build is deterministic for your snapshot: the same files give the same bytes. It is not
the maintainer's build unless you hold the same LGD files.

## Output tables

Written to `data/processed/gazetteer/` as sorted UTF-8 CSV. An empty string means the source
did not provide the value. [gazetteer.md](gazetteer.md) defines every column.

| File | Contents |
|---|---|
| `admin_unit.csv` | LGD states, districts, sub-districts and villages, with parent links |
| `village_pincode.csv` | Village-to-PIN links as LGD states them. A village can have more than one PIN |
| `post_office.csv`, `pincode.csv` | Empty in version 1, because India Post is deferred |
| `issues.csv` | Every quality finding |
| `build_info.json` | Source checksums, `gazetteer_version`, row and issue counts, code commit |

Cite `gazetteer_version` whenever you derive data from the gazetteer.

## Compare names with `name_key`

```python
from pata.normalize import name_key

name_key("Mahatma  Gandhi Rd.")  # "mahatma gandhi rd"
```

`name_key` applies NFKC, casefolds, and collapses punctuation, symbols and spaces. It keeps
combining marks, so native-script names stay intact. It does not expand abbreviations,
transliterate or correct spelling. It is a comparison key: keep the published name for display.

## Inspect a source file with `source_stats`

`scripts/source_stats.py` reports a CSV's header row and aggregate column statistics, never a
cell value. It refuses a file that does not match the checksum you give it.

```bash
uv run python scripts/source_stats.py FILE.csv --sha256 CHECKSUM --missing-token NA --expected-column "Column Name"
```

Always pass `--expected-column` with a column you know should exist. Without it, a file with no
header row prints its first record as the header. So far this tool has only been run on
synthetic test files.

## Limits

- No address dataset, parsing, resolution, geocoding, model or metric.
- No urban localities or towns, and no India Post data.
- No local-language names, and no LGD history of splits or renames.
- What an LGD sub-district is called varies by state, and that meaning stays unverified. See
  [evidence/lgd/levels.md](evidence/lgd/levels.md).
- 11,390 sibling-name warnings in the maintainer's snapshot are reported, not resolved.
- Refreshing a snapshot is manual.
- Pata does not publish the derived tables. Doing so needs its own decision (ADR-0009 §4).

## Acknowledging LGD

If you publish data or derived tables, acknowledge the source prominently, reproduce it
accurately, do not use it in a misleading way, and do not imply endorsement by LGD or the
Ministry (ADR-0004 §2). Use this wording with your own report details:

> Source: Local Government Directory (LGD), Ministry of Panchayati Raj, Government of India,
> https://lgdirectory.gov.in/. Report "{report name}", generated {portal timestamp}, retrieved
> {retrieval date}. Reproduced under the LGD Copyright Policy
> (https://lgdirectory.gov.in/copyRightPolicy.do).
