# Changelog

## 1.0.0 (2026-11-10): gazetteer toolkit

The first release, scoped by [ADR-0009](docs/decisions/0009-version-1-gazetteer-toolkit.md).
Version 1.0.0 is not PataBench 1.0, and it delivers a small part of the project's stated aim.

Distributed as a tagged source release on GitHub. The Python package alone holds only
`src/pata`; the build script, source inspection tool, manifests and guide are in the source tree.

### Included

- A deterministic all-India gazetteer build from Local Government Directory (LGD) snapshots,
  with quality checks and build provenance.
- `pata.normalize.name_key`, a script-agnostic comparison key for names.
- `scripts/source_stats.py`, which reports a CSV's header and aggregate statistics only.
- Provenance manifests, a [user guide](docs/toolkit.md) and the recorded source research.

### Not included

- Any data file. Users download LGD reports themselves and re-pin the manifests. A user's build
  is the maintainer's build only if they hold the same LGD files.
- Any address dataset, parser, resolver, geocoder, model, benchmark or metric. PataBench moves
  to version 2.
- Urban localities or towns, India Post data, local-language names, and LGD history.

### Known limits

- The toolkit is checked by its tests and the build's quality checks, not by PataBench.
- `source_stats.py` has run on synthetic test files only.
- The documented re-pinning path is tested on synthetic fixtures. It has not been run on a
  fresh LGD download.
- Sub-district meaning per state stays unverified.
