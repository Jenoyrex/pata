# ADR-0001: Data, privacy, licensing and v0 scope policy

- **Status:** Accepted
- **Date:** 2026-10-02
- **Deciders:** Project maintainer

## Context

Pata studies how noisy, multilingual, inconsistent Indian addresses can be parsed,
normalized, resolved to administrative/geographic entities, geocoded, and assigned
calibrated confidence. PataBench (dataset, schema, tasks, metrics, baselines) is the
project's credibility layer; the Pata toolkit is built and validated against it.

Real addresses are personal data. No public, openly licensed, labelled corpus of
real Indian user-written addresses is known to us. How we source, label, license and
release data therefore determines whether the project is legitimate and whether its
results mean anything. These rules are decided before any data is collected.

## Decision

### 1. Allowed data sources

v0 uses only:

- **Public, non-personal sources:** official/open reference data (for example
  administrative code directories and postal directories) and addresses of
  institutions/facilities published by their operators or by government.
- **Synthetic data**, under the rules in §3.

Not allowed:

- Scraped personal or user-entered addresses (e-commerce, classifieds, social media,
  delivery data, leaked or breached datasets).
- Any dataset with unclear licence, unclear provenance, or unclear consent.
- Sources whose terms of service forbid the intended use.

Adding a new source category (for example consented partner data) needs a new ADR.

### 2. Privacy

- No data that identifies a natural person is collected. Names of individuals,
  phone numbers, emails and ID numbers are out of scope. If a public source contains
  them, they are removed during ingestion, before anything is written to `data/processed/`.
- Institutional addresses are not personal data, but residential-looking records
  found in any source are excluded rather than "anonymized".
- Data files are never committed to git. Only provenance manifests (`data/manifests/`)
  are tracked.

### 3. Synthetic data

- Every synthetic record carries an explicit provenance flag (e.g. `source_type = "synthetic"`)
  and the generator version/seed that produced it.
- Synthetic data is never presented as real-world ground truth. Reported metrics
  are always broken down by real vs synthetic. A headline benchmark number is never
  computed on synthetic data alone.
- Generator code is versioned in the repository so synthetic sets are reproducible
  from a seed.

### 4. Licensing and redistribution

- **Code:** Apache-2.0.
- **Data:** each dataset keeps the licence of its original source. Pata does not
  relicense data.
- **OSM-derived data** (ODbL) is kept in a clearly separated location and
  release bundle, with ODbL attribution and share-alike obligations met. It is never
  mixed into non-ODbL bundles.
- Data is **redistributed only if its licence explicitly permits it.** Otherwise
  Pata ships a deterministic download-and-build script and the user fetches the
  source themselves.

### 5. Provenance (mandatory for every dataset)

Every source has a manifest in `data/manifests/` recording at least:

- source name and URL
- publisher
- licence (SPDX identifier where one exists) and a link to the licence text
- retrieval date
- SHA-256 checksum of each retrieved file
- whether redistribution is permitted
- the transformations applied (script path + git commit)

No dataset enters the pipeline without a manifest.

### 6. Language scope (v0)

- In scope: English and romanized Indian-language text, including code-mixed text.
- The annotation schema and data model are **script-agnostic from day one**: Unicode
  text throughout, labels defined on character offsets (not on English tokens), and
  a script/language field per record.
- Native-script modelling is not built in v0 unless the data or the research
  question requires it.

### 7. Geographic scope

- The reference gazetteer covers **all of India**.
- Annotation initially focuses on a smaller, deliberately diverse set of states
  (chosen and documented in a later ADR).
- Nothing in the data model or code may assume a fixed set of states.

### 8. Out of scope for now

No UI, API server, Docker or other deployment infrastructure until the underlying
data science has been validated on PataBench.

## Consequences

- Real data in v0 will skew towards institutional addresses, which are cleaner than
  user-typed residential addresses. This **distribution shift is a known limitation**
  and must be stated in the datasheet and in every reported result.
- Synthetic data can cover noise patterns that real public data lacks, but it risks
  models learning the generator. Hence the mandatory real/synthetic split in reporting.
- Some datasets cannot be redistributed. Reproducing them depends on upstream
  availability, which checksums let us detect but not prevent.
- Character-offset labels add some engineering cost now, so that native scripts
  don't require a schema migration later.
