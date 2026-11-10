# ADR-0009: Version 1 is a gazetteer toolkit; PataBench moves to version 2

- **Status:** Proposed. Not in force until the maintainer records a dated acceptance here.
- **Date:** 2026-11-10
- **Deciders:** Project maintainer
- **Relates to:** ADR-0001 (context, §4, §5, §8), ADR-0002, ADR-0004 §2, ADR-0005, ADR-0006,
  ADR-0007, ADR-0008

## Context

The project's plan has one first release: PataBench and the toolkit together. That release
needs an accepted address source, a human privacy screen and human gold annotation. As of
this ADR no candidate has a clear licence, no candidate address file is held, and those
human roles are unfilled.

What exists and works is the reference gazetteer: pinned LGD snapshots, a deterministic
build, quality checks and name normalization. The maintainer directed on 2026-11-10 that
version 1 be released from what is available, and that real address data wait for later
versions.

ADR-0001 says the toolkit is built and validated against PataBench. Version 1 cannot meet
that, so this ADR records a limited exception. ADR-0001 itself is unchanged.

## Decision

### 1. What version 1 is

Version 1 is the **Pata gazetteer toolkit**:

- the LGD gazetteer build (`scripts/build_gazetteer.py`, `src/pata/gazetteer.py`);
- name normalization (`pata.normalize.name_key`);
- aggregate source inspection (`scripts/source_stats.py`);
- provenance manifests, documentation and the recorded source research.

### 2. What version 1 is not

Version 1 contains no address dataset, parser, resolver, geocoder, model, benchmark or
metric. It is not PataBench and is never described as a benchmark. It makes no claim about
address parsing, resolution or geocoding quality.

### 3. Validation

Exception to ADR-0001's context statement, for version 1 only: the gazetteer toolkit is
validated by its tests and by the build's own quality checks (`docs/gazetteer.md`), not by
PataBench. Any later component that makes an address-intelligence claim is validated against
PataBench as ADR-0001 says.

### 4. Data distribution

Version 1 ships code and manifests only. Data files stay out of the release and out of git
(ADR-0001 §2, §4).

- A freshly downloaded LGD report differs from the pinned snapshot, and the build refuses
  it. A user re-pins their manifests as `docs/gazetteer.md` describes, so their build is
  deterministic for their snapshot, but is not the maintainer's build.
- Publishing derived tables is out of scope here and needs its own decision.
- LGD is acknowledged as ADR-0004 §2 requires wherever derived data is published.

### 5. PataBench moves to version 2

The benchmark plan is deferred, not abandoned. ADR-0006, ADR-0007 and ADR-0008 stay Proposed
and keep their text. Their acceptance is not required for version 1. Graph nodes that serve
only the benchmark carry `release = "v2"` and keep their dependencies.

The source research stays as recorded. No source is accepted or rejected by this ADR, and
no licence question (B3, B4, B14 to B17) is resolved by it.

### 6. Release

The release is a maintainer-gated, irreversible graph node (`R-V1`). The maintainer tags and
publishes it.

## Consequences

- A finished, honest first release is reachable without an address corpus or human
  annotators.
- Version 1 delivers a small part of the project's stated aim. The README and release notes
  must say so.
- The package version moves to 1.0.0 for a toolkit that has no benchmark behind it. Users
  must not read 1.0 as PataBench 1.0.
- Users cannot reproduce the maintainer's exact gazetteer unless they hold the same LGD
  files.
