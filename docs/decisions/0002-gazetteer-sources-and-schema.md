# ADR-0002: Reference gazetteer v0 sources and schema

- **Status:** Accepted
- **Date:** 2026-10-02
- **Deciders:** Project maintainer

## Context

M0 needs an India-wide reference gazetteer covering administrative units (LGD)
and postal geography (PIN codes, post offices), built under ADR-0001: first-party
public sources, explicit provenance and licence, no raw data in git, no invented data.

Findings from source research (2026-10-02):

- **Department of Posts** publishes the *All India Pincode Directory till last month*
  on data.gov.in (resource `5c2f62fe-5afa-4119-a499-fec9d604d5bd`). The metadata
  lists the fields: circlename, regionname, divisionname, officename, pincode,
  officetype, delivery, district, statename, latitude, longitude. It is updated
  monthly. The file has no stable post-office identifier.
- **Ministry of Panchayati Raj (LGD)** publishes four relevant resources on data.gov.in:
  - States (`a71e60f0-…`)
  - Districts (`37231365-…`)
  - Sub-Districts (`6be51a29-…`)
  - Villages with PIN Codes (`f17a1608-…`), with fields stateCode, stateNameEnglish,
    districtCode, districtNameEnglish, subdistrictCode, subdistrictNameEnglish,
    villageCode, villageNameEnglish, pincode
  
  The resource notes say they are updated monthly. data.gov.in publishes **no field
  list** for the States, Districts and Sub-Districts files.
- **lgdirectory.gov.in** (the primary LGD site) offers downloads behind a CAPTCHA
  and shows no reuse licence on its download page. The data.gov.in copies come with
  a clear licence and are the same publisher's data, so they are preferred.
- **Licence:** data.gov.in content is under the Government Open Data License – India
  (GODL-India), which allows use, adaptation and redistribution with attribution.
  The per-resource licence fields are empty, so the licence applies through platform
  policy. The GODL page is rendered client-side and could not be machine-verified,
  so its terms here come from secondary summaries.
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

## Consequences

- The gazetteer cannot be built until a maintainer downloads the five files, pins
  them, and maps the LGD level-file columns. Doing that is the first M0 follow-up.
- Rural geography is detailed down to village level. Urban localities are **not**
  covered (no LGD urban bodies, no town directory), which is a known gap.
- Post-office coordinates are kept as published and are only sanity-checked against
  a rough bounding box. Their accuracy is unknown and must not be treated as
  ground truth for geocoding.
- LGD entity versions and change history (splits, renames) are not modelled in v0.
