# ADR-0002: Reference gazetteer v0 sources and schema

- **Status:** Accepted
- **Date:** 2026-10-02
- **Deciders:** Project maintainer
- **Corrected:** 2026-10-02, after a provenance verification pass. Factual context
  only: GODL-India terms verified from the official text, LGD portal reuse terms,
  PIN directory freshness, attribution format. The decisions are unchanged.
- **Amended by:** ADR-0004 (LGD portal sources; XLSX reader). For the four LGD
  sources this also covers decision 5 (their column mappings are now filled from
  the real files) and decision 8 (their manifests carry the LGD Copyright Policy
  acknowledgement and portal report timestamps instead of a GODL attribution and
  data.gov.in resource dates), and makes the first Consequence moot. Recorded by
  ADR-0005; decision 8 still applies to the deferred India Post manifest.

## Context

M0 needs an India-wide reference gazetteer covering administrative units (LGD)
and postal geography (PIN codes, post offices), built under ADR-0001: first-party
public sources, explicit provenance and licence, no raw data in git, no invented data.

Findings from source research (2026-10-02):

- **Department of Posts** publishes the *All India Pincode Directory till last month*
  on data.gov.in (resource `5c2f62fe-5afa-4119-a499-fec9d604d5bd`). The metadata
  lists the fields: circlename, regionname, divisionname, officename, pincode,
  officetype, delivery, district, statename, latitude, longitude. Its resource note
  says "Data will be updated on monthly basis", but the metadata shows it was
  published 04/12/2020 and **last updated 03/10/2025** (checked 2026-10-02). It must
  not be described as monthly or current. The file has no stable post-office identifier.
- **Ministry of Panchayati Raj (LGD)** publishes four relevant resources on data.gov.in:
  - States (`a71e60f0-…`)
  - Districts (`37231365-…`)
  - Sub-Districts (`6be51a29-…`)
  - Villages with PIN Codes (`f17a1608-…`), with fields stateCode, stateNameEnglish,
    districtCode, districtNameEnglish, subdistrictCode, subdistrictNameEnglish,
    villageCode, villageNameEnglish, pincode
  
  The resource notes say they are updated on the 1st of every month. Their metadata
  (checked 2026-10-02) shows last updates of 25/09/2026 for States, Districts and
  Sub-Districts, and 01/09/2026 for Villages with PIN Codes. data.gov.in publishes
  **no field list** for the States, Districts and Sub-Districts files.
- **lgdirectory.gov.in** (the primary LGD site) offers downloads in PDF, HTML, XLS and
  ODT only (no CSV), behind a CAPTCHA. Its Copyright Policy (`copyRightPolicy.do`)
  states that material "may be reproduced free of charge in any format or media
  without requiring specific permission", subject to accurate reproduction, no
  derogatory or misleading use, and prominent acknowledgement of the source when it
  is published. The data.gov.in copies are preferred because they are CSV and carry
  GODL-India terms. They are the same publisher's data.
- **Licence (verified 2026-10-02 from the official GODL-India text served by
  data.gov.in at `/Godl`):** data.gov.in states that "the content published on
  data.gov.in is owned by the respective Ministry/State/Department/Organization and
  licensed under the Government Open Data License - India". The per-resource licence
  fields are empty, so this site-wide statement is what applies. GODL-India grants a
  worldwide, royalty-free, non-exclusive licence to use, adapt, publish, translate,
  display, add value to, and create derivative works from the data, for lawful
  commercial and non-commercial purposes. Its conditions:
  - **Attribution:** the user must acknowledge the provider, source and licence by
    publishing an attribution statement that includes the DOI, URL or URI of the
    data. The section 5 template is: *Name of Data Provider, Year of Publication,
    Name of Data, Name of Data Repository/Website, Version Number and/or Date of
    Publication, DOI/URL/URI. Published under Name of License: URL of License.*
    When many datasets are combined, a link to a separate attribution page is allowed.
  - **Non-endorsement:** the user must not suggest the provider endorses them or their use.
  - **No warranty**, and no guarantee that updated data will keep being supplied.
  - **Exemptions** (section 6): personal information; data the provider isn't
    authorised to license; names, crests, logos and official symbols; data under other
    IP rights; data that shouldn't have been disclosed under RTI Act section 8.
  - **Termination:** rights end automatically on breach and are reinstated if the
    breach is cured within 30 days. The provider may withdraw the licence for a specific dataset.
- **Access:** direct file URLs returned HTTP 403/301 to scripted requests, and
  `api.data.gov.in` was unreachable from the development machine. Every source
  currently has to be **downloaded manually**.

Considered and deferred:

- **Third-party mirrors** (GitHub LGD dumps, India Data Portal): not first-party.
- **Census 2011 village/town directories:** older vintage, different code system.
- **India Post PIN boundary polygons:** a geocoding-phase concern.
- **OSM:** ODbL, a separate bundle under ADR-0001.
- **LGD local bodies and urban units:** wait until rural coverage is understood.

## Decision

1. **v0 sources:** the five data.gov.in resources above, one manifest each in
   `data/manifests/`.
2. **No cross-publisher merging.** LGD units and India Post offices are separate
   tables. India Post's `district`/`state` strings are kept raw and are not linked
   to LGD codes. Linking them is a resolution task to be measured later, not a
   build step. The only cross-publisher link is the one LGD itself states (village → PIN).
3. **IDs** are namespaced by publisher and level:
   - LGD units: `lgd:{level}:{lgd_code}`, with levels state, district, subdistrict
     and village. Sub-district covers taluk, tehsil, mandal and similar units, as LGD
     defines them.
   - Post offices: `dop:po:{pincode}:{name_key(office_name)}`. This is derived,
     because India Post provides no office ID.
4. **Pinned snapshots.** Each manifest records the SHA-256 checksum and row count of
   the exact file. The build refuses files that don't match, so a new snapshot is
   always an explicit, reviewable manifest diff.
5. **Explicit column mappings.** Canonical columns map to source headers in each
   manifest. Mappings for the three LGD level files stay **empty until checked
   against a real file**, and the build refuses to run until they're filled. This
   avoids guessing between, for example, LGD and Census code columns.
6. **Quality gates.** Errors fail the build and no tables are written. Warnings
   and info items are written to `issues.csv`. See `docs/gazetteer.md`.
7. **Standard library only** (csv, tomllib, hashlib). The outputs are sorted CSV
   files, so they are byte-reproducible from the same snapshot.
8. **Attribution and dates.** Each manifest carries a GODL section 5 attribution
   string. It also records the resource's own dates as shown on data.gov.in
   (`resource_published`, `resource_last_updated`, `metadata_checked`), kept separate
   from Pata's download date (`snapshot.retrieved`). The attribution date is
   re-checked whenever a snapshot is pinned.

## Consequences

- The gazetteer cannot be built until a maintainer downloads the five files, pins
  them, and maps the LGD level-file columns. Doing that is the first M0 follow-up.
- Rural geography is detailed down to village level. Urban localities are **not**
  covered (no LGD urban bodies, no town directory), which is a known gap.
- Post-office coordinates are kept as published and are only sanity-checked against
  a rough bounding box. Their accuracy is unknown and must not be treated as
  ground truth for geocoding.
- LGD entity versions and change history (splits, renames) are not modelled in v0.
