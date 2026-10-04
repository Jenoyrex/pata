# ADR-0005: Gazetteer version, build provenance, sibling-name warnings, record corrections

- **Status:** Accepted
- **Date:** 2026-10-04
- **Deciders:** Project maintainer

## Context

A read-only audit of the LGD ingestion (commit e8a6420, 2026-10-04) found the four
pinned snapshots internally consistent: checksums and row counts match, every
parent exists, the village file agrees exactly with the level files, every
village has one valid PIN, and a rebuild is byte-identical. It also found gaps that
would hurt anything built on top of the gazetteer:

- **No gazetteer version.** A table row or a future annotation could cite
  `lgd:village:…`, but nothing named the snapshot set it came from.
- **Build provenance was unreliable.** `build_info.json` recorded only `git rev-parse
  HEAD`. The processed tables on the maintainer's machine say `git_commit:
  07ee461…`, a commit with no XLSX reader: they were built from uncommitted changes
  that later became e8a6420, and nothing recorded that.
- **One warning code covered two different findings.** All 11,382 build warnings
  were `name_key_collision` (sibling units whose `name_key` is equal). Recounting
  from the raw files, 11,250 of those groups have byte-identical published names
  and 132 have names that differ as published but coincide after `name_key`
  (`Haripura` / `Haripura.`, `Melopara Pt-Ii` / `Melopara Pt-II`).
- **Stale or incomplete records** in ADR-0002, ADR-0003, ADR-0004 and the README.

## Decision

### 1. Gazetteer version

`build_info.json` gets `gazetteer_version`: the SHA-256 (hex) of the SHA-256 values
of the built, non-deferred source snapshots, sorted and joined with `\n`. It depends
only on the pinned source files, not on code, build time or machine, and changes
whenever any snapshot changes. For the 2026-10-03 LGD snapshots it is
`bf4a8b5d35130e7c3b94c6e4de812b3fd6deeb059497af22aac178642c2c2c78`.

The version names the inputs. The code that turned them into tables is named by
`git_commit` and `git_dirty`, below. Both are needed to reproduce a build.

### 2. Honest build provenance

- `git_commit` stays `HEAD` (or `unknown`).
- New `git_dirty`: `true` if `git status --porcelain` shows tracked changes or
  untracked, non-ignored files; `false` if clean; `null` if git state can't be read.
  A dirty or unknown state also prints a warning to stderr. A dirty build is not
  refused, because development needs it, but it is never recorded as if it came
  from a clean commit.
- New `outputs`: the SHA-256 of every file the build writes (`admin_unit.csv`,
  `post_office.csv`, `pincode.csv`, `village_pincode.csv`, `issues.csv`; only
  `issues.csv` when the build fails).

ADR-0001 section 5 asks for "the transformations applied (script path + git
commit)". This is recorded per build in `build_info.json`, not in the manifests,
because the commit is a property of a build, not of a source.

### 3. Sibling-name warnings

`name_key_collision` for administrative units is replaced by two warning codes.
Siblings are units of the same level under the same parent whose `name_key` is
equal:

- `same_name_siblings`: two or more siblings with **byte-identical** published
  names. One warning per identical name.
- `variant_name_siblings`: a sibling group whose published names **differ** but
  share one `name_key`. One warning per group, listing every member and every
  spelling.

A group such as {`Salaiya`, `Salaiya`, `Salaiya.`} gets both: the identical pair is
a `same_name_siblings` warning, and the whole group is a `variant_name_siblings`
warning. Nothing is dropped, and the published names are not changed.

Both stay warnings. LGD allows distinct villages with one name. Whether a variant
pair is two villages or one village entered twice cannot be decided from the
source, so it is reported, not resolved. The post-office `name_key_collision`
**error** (India Post, deferred) is a different check and is unchanged.

On the pinned snapshots this gives 11,390 warning records, all at village level:
11,258 `same_name_siblings` and 132 `variant_name_siblings`. They cover the same
11,382 distinct name collision groups that `name_key_collision` reported: 11,250
groups whose names are all identical, plus 132 variant groups. 8 of the variant
groups also contain an identical pair, so each of them gets one record of each
code. That adds 8 `same_name_siblings` records (11,250 + 8 = 11,258), and it is
why there are 8 more records than groups (11,390 − 11,382).

### 4. The 11,260 vs 11,382 discrepancy

ADR-0004 expected "about 11,260" `name_key_collision` warnings. The build reported
11,382. ADR-0004's figure came from a read-only inspection whose script is not in
the repository, so how it counted cannot be checked. What can be checked is that
11,382 = 11,250 groups of identical names + 132 groups that only coincide after
`name_key`. The estimate is close to the first number, which is consistent with
counting identical names only, but that is an inference, not a record. The
build's count, 11,382 groups, is the correct count of the check as it was defined.
"About 11,260" stays in ADR-0004 as a historical, approximate expectation. It is
not a measured result and must not be quoted as the current count; the current
counts are in section 3.

### 5. Record corrections

Historical decisions are not rewritten. These header notes and wording fixes are
made, each pointing here:

- **ADR-0002:** its "Amended by" note now says that ADR-0004 also changes, for the
  four LGD sources, decision 5 (column mappings filled from the real files) and
  decision 8 (LGD acknowledgement and portal timestamps instead of a GODL
  attribution and data.gov.in dates). This also makes its first Consequence moot.
  Decision 8 still governs the deferred India Post manifest.
- **ADR-0003:** stays *Proposed, PERMISSION PENDING*. The NAPIX request is still
  unanswered, and NAPIX is not an approved source. A header note marks it as
  superseded in part by ADR-0004 for acquiring the v0 LGD snapshots, so its
  "stays blocked" consequence no longer holds.
- **ADR-0004:** section 3 and its Consequences said the ingestion change was still to
  come. It landed in the same commit (e8a6420). The wording now says so. The
  11,260 estimate is kept, with a pointer here.
- **README:** "build cleanly" is replaced by the actual result (no errors, and these
  warnings).

### 6. Unchanged scope

Still deferred: India Post data, NAPIX acquisition, LGD urban/local-body
integration, a PIN entity table, `name_local` beyond what ADR-0004 allows, the
address corpus, annotation, and model work.

## Consequences

- `gazetteer_version` is what later datasets and annotations cite to name the
  reference data they were built against.
- Processed tables built before this change have no `gazetteer_version`, no
  `outputs` hashes, and the old warning code. They must be rebuilt (`uv run
  scripts/build_gazetteer.py`) from a clean checkout of the commit that adds this ADR,
  so that `git_dirty` is `false`. The table files other than `issues.csv` come
  out byte-identical, because the change only touches warnings and `build_info.json`.
- `build_info.json` now differs between a clean and a dirty build of the same
  code. The tables do not, so they remain byte-reproducible from the same snapshot.
- Any tooling that filtered `issues.csv` on `name_key_collision` for admin units
  has to use the two new codes.
