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

**Pre-alpha. There are no datasets, models or benchmark results yet.** Any number
that appears in this repository will be produced by committed code and a recorded
experiment.

Current milestone, **M0 "Know the data"**:

- [x] Repository, tooling, CI, data/privacy policy
- [ ] All-India reference gazetteer (with quality audit). The LGD administrative
      hierarchy and village → PIN mapping are pinned and build cleanly
      ([docs/gazetteer.md](docs/gazetteer.md)). The India Post directory and urban
      PIN mapping are deferred.
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
```

## Repository layout

```
src/pata/        toolkit (library code)
scripts/         build entry points (e.g. build_gazetteer.py)
tests/           tests
docs/            documentation and decision records
data/manifests/  dataset provenance manifests (data itself is not committed)
```

More directories (`bench/`, `experiments/`) are added when they get content.

## License

Code: [Apache-2.0](LICENSE). Datasets keep their original licences (see ADR-0001).
