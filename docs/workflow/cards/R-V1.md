# Task card — R-V1: Release Pata gazetteer toolkit 1.0.0

- **Branch:** `workflow-kit` (maintainer's working branch)
- **Started:** 2026-11-10 · **Session(s):** 1
- **Deps confirmed done:** G-V1SCOPE, I-V1KIT, W0, E-LGD
- **Gate:** maintainer · **Irreversible:** yes (maintainer "go R-V1" given in chat on 2026-11-10)

## Plan
1. Set the package and lock versions to 1.0.0; update the version test.
2. Write `CHANGELOG.md`; make the README and package description match ADR-0009.
3. Run the gates. The maintainer tags, pushes and publishes.

## Acceptance → proof map
| # | Acceptance criterion (copied verbatim from graph) | How it will be proven | Result |
|---|---|---|---|
| 1 | Package version is 1.0.0 and the changelog lists what is and is not included | `pyproject.toml`, `uv.lock`, `tests/test_package.py`, `CHANGELOG.md` | see verifier |
| 2 | All project gates pass on the release commit | The documented gates, on the release tree; rerun on the commit by CI after the maintainer pushes | see verifier |
| 3 | No data file is in the release or in git | `git ls-files data` lists only `data/manifests/` | see verifier |
| 4 | Tag, push and publication done by the maintainer | Maintainer step; not done by Claude | Pending the maintainer |

## Scope fence (will NOT do)
- Tag, push, publish or record the approval. Publish derived tables.

## Stop-points
- Criterion 4 is the maintainer's. The node stays `review` until they approve it.

## Discovered work
- None.

## Proof
`uv lock --check` exit 0; ruff passed; format 59 files; `uv run pytest -q` 160 passed, 5 skipped;
`graph.py validate --check-outputs` OK; `git diff --check` exit 0.

## Verifier verdict
2026-11-10, before the release commit: **Overall FAIL**, expected at this stage. Criterion 2 needs the
commit to exist; criterion 4 is the maintainer's step. No defect found. The verifier's table, verbatim:

| # | Criterion (verbatim) | Verdict | Evidence (path:line / test id / command) |
|---|---|---|---|
| 1 | Package version is 1.0.0 and the changelog lists what is and is not included | PASS | E:\PATA\pyproject.toml:3; `uv.lock` diff shows `pata` at 1.0.0; `uv lock --check` exit 0; `uv run python -c "import pata; print(pata.__version__)"` prints 1.0.0; `tests/test_package.py::test_version_is_exposed` fails on any other version; `uv build` produced `pata-1.0.0`. E:\PATA\CHANGELOG.md:8 "Included", :16 "Not included". The not-included list matches ADR-0009 §2 and §4. No test covers the changelog; the evidence is the file itself. See warnings 1 and 2. |
| 2 | All project gates pass on the release commit | UNPROVEN | No release commit exists. HEAD `bb7c772` is still version 0.1.0, and the release changes are uncommitted (`git status`). All gates pass on the working tree only (Checks line below). CI has not run on this content. |
| 3 | No data file is in the release or in git | PASS | `git ls-files data` returns 5 files, all `data/manifests/*.toml`. Tracked file types are md, py, toml, yml, json, lock, patch, mmd and config only. A search of `git log --all --diff-filter=A` for data extensions and `data/`, `report data/`, raw, private and staging paths finds only `data/manifests/` entries. The 2 untracked files are `CHANGELOG.md` and the card. `uv build` to the scratchpad: the sdist and wheel hold only `src/pata/*`, LICENSE, README and metadata. Checked on the working tree; recheck on the release commit. |
| 4 | Tag, push and publication done by the maintainer | FAIL (not yet done) | `git tag --list` returns 0 tags; `git ls-remote --tags origin` returns 0 lines; the release changes are uncommitted. This is the maintainer's step and the card says so (E:\PATA\docs\workflow\cards\R-V1.md:19). |

Checks: ruff ✓ · format ✓ (60 files) · pytest 160 passed/0 failed (5 skipped) · graph ✓ · diff-check ✓

Overall: FAIL

Its warnings 1 and 2 were then fixed: the changelog names the tagged source release, and the changelog
and README say version 1 delivers a small part of the project's aim. CI runs on a push to `main`.

## Outcome
- Graph status stays `in_progress` until the maintainer pushes, tags, publishes and approves.
- Commit(s): the release commit.
