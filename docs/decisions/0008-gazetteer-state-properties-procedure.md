# ADR-0008: Procedure for per-state gazetteer properties (G10)

- **Status:** Proposed. Not accepted until the decisions in section 8.1 are
  approved by the maintainer. It defines the "versioned procedure" that
  ADR-0007 §4 step 3 requires, so it is used only once ADR-0007 is accepted.
  ADR-0007 is itself Proposed and cannot be accepted before ADR-0006.
- **Date:** 2026-10-26
- **Deciders:** Project maintainer
- **Relates to:** ADR-0001 §5 and §7, ADR-0004, ADR-0005 (`gazetteer_version`,
  build provenance, sibling-name warnings), ADR-0006 §17 step 1, ADR-0007 §4,
  §8 and O7; research notes G10 and B9

This ADR defines **how** per-state gazetteer properties are computed. It
computes nothing and selects no state. It adds no code, changes no gazetteer
table, manifest or schema, and reports no new count.

## Context

- **ADR-0007 §4 step 3** requires each selection record to list "gazetteer
  properties **computed** from the pinned `gazetteer_version` by a versioned
  procedure, not estimated: districts and sub-districts with no villages in the
  mapping, `same_name_siblings` and `variant_name_siblings` counts, and the
  distribution of villages per PIN". Whether gaps count for or against a state
  is open (O7). No dimension has a threshold.
- **No such procedure exists (G10, B9).** The per-state figures in
  `docs/research/source-inventory.md` ("Candidate-state evidence") and
  `docs/research/focus-state-source-evaluation.md` (O1) came from an ad-hoc
  script that is not in the repository. ADR-0005 §4 records the same problem
  for ADR-0004's "about 11,260": a count whose script is absent cannot be
  checked.
- **What the builder already guarantees** (`src/pata/gazetteer.py`,
  `docs/gazetteer.md`):
  - Tables are written only when the build has no errors. Errors include
    `broken_parent`, `unknown_admin_unit` and `hierarchy_mismatch`, so in a
    written build every non-state unit has a parent of the level above.
  - Village units come only from LGD's "Pincode to Village Mapping", with the
    sub-district as parent. "No villages" therefore means "no villages in that
    mapping".
  - `same_name_siblings` and `variant_name_siblings` records (ADR-0005 §3)
    have `entity_id` set to the sorted, `|`-joined IDs of sibling units, which
    by definition share one parent.
  - `build_info.json` records `status`, `gazetteer_version`, `git_commit`,
    `git_dirty`, the SHA-256 of every output table (`outputs`), row counts and
    issue counts.
- **The local build was checked on 2026-10-26** (read-only, no rebuild):
  `status` "ok", `gazetteer_version`
  `bf4a8b5d35130e7c3b94c6e4de812b3fd6deeb059497af22aac178642c2c2c78`,
  `git_commit` `cb64f6868192e07b163737315eba8654c393c813`, `git_dirty` false.
  The five table files hash to the values in `outputs`. `git diff cb64f68
  e20f26e` shows no change to `src/`, `scripts/`, `data/manifests/`,
  `pyproject.toml` or `uv.lock`.

## Decision

### 1. Scope

- The procedure computes, for each LGD state/UT unit in the pinned gazetteer,
  the properties ADR-0007 §4 step 3 names, plus the unit counts needed to read
  them (section 4). Nothing else.
- It reads only gazetteer output tables. It never reads raw snapshots, address
  sources, address records or the network.
- Its results describe the reference gazetteer. They do not describe any
  address source (section 7).

### 2. Inputs and provenance

Inputs, all from one build directory (by default `data/processed/gazetteer/`):

| File | Used for |
|---|---|
| `build_info.json` | Preconditions and provenance |
| `admin_unit.csv` | Units, levels, parents, published state names |
| `village_pincode.csv` | Village–PIN links |
| `issues.csv` | Sibling-name warning records |

The procedure **stops with an error and writes nothing** unless:
- `build_info.json` has `status` "ok" and `git_dirty` false;
- its `gazetteer_version` equals the version the run is asked for (the pinned
  value, passed explicitly, never read as a default);
- the SHA-256 of each of the three tables equals its value in
  `build_info.json` `outputs`;
- for each of the two sibling codes, the number of `issues.csv` records equals
  the count in `build_info.json` `issues`. The builder writes that field as a
  count of every record it emits, so a code absent from it means zero records,
  not an unknown count.

The provenance file (section 5) records: the procedure version, the
`gazetteer_version`, the three input SHA-256s, the builder's `git_commit` from
`build_info.json`, and the procedure run's own `git_commit` and `git_dirty`
(as ADR-0005 §2 does for the build). As with the build, a dirty run is
allowed for development and recorded as dirty. A selection record cites only a
run whose `git_dirty` is false.

### 3. State identity and assignment

- A state is an `admin_unit` row with `level` "state". It is identified by its
  `id` (`lgd:state:{lgd_code}`), as ADR-0007 §2 requires. The number of states
  is read from the table, never assumed (ADR-0001 §7).
- Every other unit is assigned to a state by following `parent_id` up the
  levels (village → sub-district → district → state). **No name is matched at
  any step.**
- The output carries the state's published `name` exactly as in
  `admin_unit.csv`, for reading only. It is never a key.
- Mapping a publisher's state label (for example "Tamil Nadu") to an
  `lgd:state:` ID is **not** part of this procedure. That is ADR-0006 §17
  step 1 and the ADR-0007 §5 coverage assessment.
- **Missing or ambiguous mapping.** If a chain does not end at exactly one
  state unit (missing parent, wrong parent level, a cycle), or a sibling
  warning names an ID absent from `admin_unit.csv`, or its member IDs resolve
  to more than one state, or a `village_pincode.csv` row names a `village_id`
  that is not a village unit in `admin_unit.csv`, the procedure stops with an
  error and writes nothing. An unresolved unit is never counted as zero or
  skipped. There is no "unknown state" bucket. A sibling warning among state
  units themselves (empty parent) is counted on a separate `(state level)`
  line of the provenance file and in no state's row.

### 4. Property definitions

All counts are of distinct unit IDs, distinct PINs or distinct warning
records, per state `S`.

| Column | Definition | Counting unit |
|---|---|---|
| `districts` | District units assigned to `S` | units |
| `subdistricts` | Sub-district units assigned to `S` | units |
| `villages` | Village units assigned to `S` | units |
| `districts_without_villages` | Districts in `S` with no village unit below them | units |
| `subdistricts_without_villages` | Sub-districts in `S` with no village child | units |
| `same_name_siblings_{level}` | `issues.csv` records with code `same_name_siblings` whose members are units of `{level}` in `S` | warning records |
| `variant_name_siblings_{level}` | Same, for `variant_name_siblings` | warning records |
| `pins` | Distinct PINs linked to at least one village in `S` | PINs |
| `villages_without_pin` | Villages in `S` with no row in `village_pincode.csv` | units |
| `pins_shared_with_other_states` | PINs counted in `pins` that are also linked to a village in another state | PINs |

Rules:
- **Levels.** `{level}` is `district`, `subdistrict` and `village`, in that
  order: three `same_name_siblings_*` columns, then three
  `variant_name_siblings_*` columns. Each is present even when zero, so the
  column set does not depend on the snapshot. Zero means the build emitted no
  such record (section 2), not that the count is unknown.
- **No villages.** A sub-district inside a district without villages is
  counted in both columns. Each level is counted on its own.
- **Warning records are counted as records,** as `issues.csv` and
  `build_info.json` count them. They are not converted to groups or units, and
  a group with both codes counts once under each (ADR-0005 §3). They are never
  deduplicated across the two codes.
- **Villages per PIN.** For each PIN `p` counted in `pins`, `n_S(p)` is the
  number of distinct village IDs in `S` linked to `p`. A village linked to
  several PINs counts once for each. The **distribution** is the full
  frequency table of `n_S(p)`: for each value, the number of PINs with it. For
  a PIN shared with another state, `n_S(p)` counts only the villages in `S`;
  `pins_shared_with_other_states` says how many PINs that affects. Counting
  within the state is a choice made here. ADR-0007 says only "the
  distribution of villages per PIN". The alternative, counting all of a PIN's
  villages wherever they lie, is not used.
- `villages_without_pin` and `pins_shared_with_other_states` are not new
  properties. They state the coverage of the villages-per-PIN distribution
  above and are needed to read it.
- A state with no villages still has a row. Its village, PIN and
  villages-per-PIN columns are zero, and it has no lines in
  `villages_per_pin.csv`. Its district and sub-district columns are counted as
  usual.

### 5. Output format and order

Three files, written together, or none:

- `state_properties.csv`: one row per state. Columns `state_id`, `lgd_code`,
  `name`, then the section 4 columns in the order of that table.
- `villages_per_pin.csv`: columns `state_id`, `villages_in_state`,
  `pin_count`, one row per state and distinct value of `n_S(p)`.
- `state_properties_info.json`: the provenance of section 2, the output
  SHA-256s, the `(state level)` line, and the procedure version.

Format: UTF-8, LF line endings, a header row, integers in plain decimal with no
separators. CSV rows are sorted by the integer value of `lgd_code`, then by
`state_id` as a string (a tie-breaker, in case two codes differ only in
leading zeros), then, in `villages_per_pin.csv`, by the integer value of
`villages_in_state`. JSON keys are sorted, as in `build_info.json`. Output
goes under `data/processed/`, which is not committed, like the gazetteer.

The procedure version is a single integer, recorded as
`state_properties_procedure_version`. Any change to sections 2 to 5 is a new
version. Version 1 is assigned when this ADR is accepted.

### 6. Validation

A run fails, and writes nothing, unless all of these hold:
- the preconditions of section 2;
- every state unit appears in exactly one row;
- the sums of `districts`, `subdistricts` and `villages` over all rows equal
  the number of `admin_unit.csv` rows at each level;
- the sums of the sibling-record columns, plus the `(state level)` line, equal
  the issue counts in `build_info.json` for each code;
- the sum of `villages_in_state` × `pin_count` over all rows of
  `villages_per_pin.csv` equals the number of `village_pincode.csv` rows;
- for each state, the sum of `pin_count` in `villages_per_pin.csv` equals
  its `pins` in `state_properties.csv`.

Reproducibility: two runs on the same inputs at the same procedure version
produce byte-identical files. When implemented, the code gets a small
synthetic-fixture test in `tests/`, as the builder has, covering a shared
PIN, a village without a PIN, a district without villages and both sibling
codes.

These checks use only builder outputs. For the pinned version, the national
totals are also **compared**, as a separate review step and not a gate, with
the figures in `docs/gazetteer.md` (784 districts, 7,092 sub-districts,
672,619 villages, 6 districts and 30 sub-districts without villages, 11,258
and 132 warning records). The builder does not compute the "without villages"
figures, so they are documentation, not reference values. A mismatch is
recorded and investigated, and neither side is adjusted to match.

### 7. Use in selection, and limits

- A selection record quotes the values together with
  `state_properties_procedure_version`, `gazetteer_version` and the SHA-256s
  of `state_properties.csv` and `villages_per_pin.csv`.
- The values feed only the ADR-0007 §4 dimension "Gazetteer coverage
  properties". They set no threshold, rank no state and do not decide O7.
- **They do not measure** address-source availability, record counts, address
  quality or completeness, urban coverage, language or script, or the
  publisher count. A state with many villages per PIN or many sibling names is
  not thereby a better or worse source of addresses.
- "Without villages" means without villages **in LGD's village–PIN
  mapping**. It does not show that a district or sub-district has no villages,
  or no addresses.
- They are **not** evidence for sub-district semantics. ADR-0007 §8 excludes
  counts and name patterns in the gazetteer.
- **Not derivable from the pinned gazetteer**, so not computed:
  - urban local bodies, towns or localities (not ingested, ADR-0004);
  - post-office facts, PIN-to-district or PIN-to-state labels from India Post
    (deferred; `post_office.csv` and `pincode.csv` are empty);
  - what tier LGD records as a state's sub-district (no such column, ADR-0004,
    ADR-0007 §8);
  - local-language names (`name_local` is empty);
  - LGD history, splits and renames;
  - regional groupings, population, area or any census figure;
  - anything about address sources.
- The ad-hoc figures in the research notes stay marked as ad hoc. They are
  replaced only by output of the implemented procedure, never edited to
  match it.

### 8. Decisions

#### 8.1 To approve with this ADR

| # | Decision | Section |
|---|---|---|
| G10-1 | Inputs are the built gazetteer tables, admitted only through the `build_info.json` checks; no raw or address data | 2 |
| G10-2 | States by `lgd:state:` ID; assignment by parent chain only; no name matching; stop on any unresolved chain | 3 |
| G10-3 | The property definitions, counting units and no-deduplication rule | 4 |
| G10-4 | The output files, format, order and integer procedure version | 5 |
| G10-5 | The validation checks and byte-identical reruns | 6 |
| G10-6 | The values are descriptive inputs to one ADR-0007 dimension and measure nothing about address sources | 7 |

#### 8.2 Open

| # | Question |
|---|---|
| Q1 | Which summary of the villages-per-PIN distribution a selection record shows besides the full table (for example `pins`, minimum, median by a named rule, maximum). The ad-hoc notes used a median whose rule is not recorded. |
| Q2 | Whether the unit counts and the two coverage columns of section 4 are quoted in selection records or kept only in the output files. |
| Q3 | Where the implementation lives (a module beside `pata.gazetteer` and a script beside `scripts/build_gazetteer.py` is the existing pattern). |

## Consequences

- After approval, the procedure is implemented as code with its fixture test,
  run on the pinned build, and cited by selection records. Until then B9 stays
  open and no gazetteer property can go into a selection record.
- The gazetteer builder, its tables and `build_info.json` are unchanged.
- A new gazetteer snapshot changes `gazetteer_version` and so every output;
  a definition change changes the procedure version. Either is visible in the
  provenance file.
- The procedure fails closed. A hierarchy problem that the builder would
  already have refused stops it too, rather than producing partial counts.
