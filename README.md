# Pata

**An open-source benchmark and ML toolkit for Indian address intelligence.**

Pata studies how noisy, multilingual, inconsistent Indian addresses can be

- **parsed** into structured components,
- **normalized**,
- **resolved** to administrative and geographic entities,
- **geocoded**, and
- assigned **calibrated confidence**.

The project has two parts:

- **PataBench** is the credibility layer: dataset, annotation schema, data documentation,
  task definitions, metrics, baselines, reproducible experiments and error analysis.
- **Pata** is the reusable toolkit. Each of its components is built and validated against PataBench.

## Status

**Pre-alpha (version 0.1.0). There is no address dataset, model or benchmark result yet.**
Any number that appears in this repository will be produced by committed code and a
recorded experiment.

| Area | State |
|---|---|
| Reference gazetteer | Built from pinned LGD snapshots: 680,531 administrative units and 672,619 village-to-PIN rows ([docs/gazetteer.md](docs/gazetteer.md)). The snapshots are not in this repository |
| Source research | Candidate inventory and licence evidence recorded in [docs/research/source-inventory.md](docs/research/source-inventory.md). No address source is accepted, and no candidate has a clear licence yet |
| Annotation scope and sources | [ADR-0006](docs/decisions/0006-annotation-scope-and-schema.md) and [ADR-0007](docs/decisions/0007-focus-states-and-sources.md) are drafted for version 2 and awaiting maintainer acceptance |
| Tooling | Aggregate-only source inspection (`scripts/source_stats.py`) and the workflow graph (`scripts/graph.py`). The inspection tool has run on synthetic fixtures only |
| Not started | Ingestion, split generation, privacy screening, annotation, evaluation and baselines |

**Version 1 is a gazetteer toolkit**
([ADR-0009](docs/decisions/0009-version-1-gazetteer-toolkit.md); see the
[user guide](docs/toolkit.md)). It has no address dataset, model, benchmark or metric.
PataBench moves to version 2, and until then the toolkit is checked by its tests and the
build's quality checks. Version 1 uses pinned data snapshots; live data is left to later
versions.

Work is ordered by the dependency graph in
[workflow/graph.toml](workflow/graph.toml), and
[PROGRESS.md](PROGRESS.md) records its current state.

Current milestone, **M0 "Know the data"**:

- [x] Repository, tooling, CI, data/privacy policy
- [ ] All-India reference gazetteer (with quality audit). The LGD administrative
      hierarchy and village → PIN mapping are pinned and build with no errors.
      It reports 11,390 warning records, all about same-named villages under one
      sub-district: 11,258 `same_name_siblings` (identical names, which LGD allows)
      and 132 `variant_name_siblings` (spellings that differ only in case,
      punctuation, spacing or Unicode form; the source can't say whether they are
      distinct villages). They cover 11,382 name collision groups; 8 groups hold
      both an identical pair and a variant spelling, hence 8 more records than
      groups ([docs/gazetteer.md](docs/gazetteer.md)). The India Post directory and
      urban PIN mapping are deferred.
- [ ] Annotation schema v0.1 and pilot annotation (with inter-annotator agreement)
- [ ] Evaluation harness and trivial baselines

## Principles

1. Data quality and evaluation come before model sophistication.
2. Reproducibility is mandatory.
3. Every ML claim is backed by a measurable evaluation.
4. Strong, simple baselines come first.
5. Assumptions and limitations are documented.
6. Privacy and licence compliance are non-negotiable. See
   [ADR-0001](docs/decisions/0001-data-privacy-licensing-scope.md).

## Data policy (summary)

- Only public, non-personal sources and clearly flagged synthetic data.
  No scraped personal or user addresses.
- Each dataset keeps its source's licence. OSM-derived data is kept separate under ODbL.
- Data is redistributed only where its licence permits. Every source has a manifest
  with provenance, licence and checksums.
- Data files are never committed to git.

## Development

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync                    # create .venv and install pinned deps
uv run pytest              # tests
uv run ruff check .        # lint
uv run ruff format .       # format
uv run python scripts/graph.py next   # what the workflow graph says is ready
```

To build the gazetteer from your own LGD files, follow the
[user guide](docs/toolkit.md).

## Repository layout

```
src/pata/        toolkit (library code)
scripts/         build, inspection and workflow entry points
tests/           tests
docs/            documentation, decision records, research and workflow
workflow/        dependency graph of the project's work
data/manifests/  dataset provenance manifests (data itself is not committed)
```

More directories (`bench/`, `experiments/`) are added when they get content.

## License

Code: [Apache-2.0](LICENSE). Datasets keep their original licences (see ADR-0001).
