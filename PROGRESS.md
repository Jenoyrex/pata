# Progress

Update at every checkpoint. Record only commands that actually ran and their observed
results.

## Current objective

Version 1.0.0 (gazetteer toolkit) is released. Next is version 2, PataBench: G-ADR67, then E-FIELD. What to
work on is decided by `workflow/graph.toml` (`uv run python scripts/graph.py next`). Legacy tasks and
the ruling ledger: [`docs/research/dependency-graph.md`](docs/research/dependency-graph.md).

## Repository state (2026-11-10)

- Tag `v1.0.0` is at `718549d`, published on GitHub by the maintainer on 2026-11-10. `origin/main` and
  `origin/workflow-kit` were at `718549d` then; the closing record for R-V1 follows on `workflow-kit`.
- Local `main` is still at `0d1c570`, behind `origin/main`.
- The ADR-0006 rev 6 and ADR-0007 rev 4 text is now on `origin/main`, **still Proposed**. Merging it
  is not acceptance: G-ADR67 stays in `review` and D10.1 still needs an explicit, dated acceptance.
- Accepted ADRs: 0001, 0002, 0004, 0005. Proposed: 0003 (permission pending), 0006,
  0007, 0008 (status lines read on `origin/main`, 2026-11-09).
- No address source accepted. No datasets, models or benchmark results.

## Completed

- **T0, workflow setup.** Added `CLAUDE.md`, this file, and the dependency graph.
  Commit `f18c35a`.
- **T1, Blocker 2: VERIFIED.** All Blocker 2 rulings are recorded in the graph
  ledger, including R1f (a), R1g (yes) and R8b (accepted), with a check against the
  ADR text. Commit `359b339`.
- **T2, Blocker 8: VERIFIED.** All ten defaults (8.1–8.10) were accepted and
  recorded.
  - The consistency check with R1f, Layer D and §14 found no contradiction.
  - The derived consequences are listed in the graph.
- None of the Blocker 1, 2 or 8 rulings is **incorporated into the ADRs** yet. That
  happens in T11, after every blocker is decided.
- **T3–T7 analysis.** Commit `2858a73`: facts, specs and decision requests
  D3.1–D7.3.
- **T3–T7 rulings (2026-10-28).**
  - The maintainer accepted every D, with explicit wording for D4.4.
  - Checking against the ADR text found one conflict. D7.1 (human screening after
    the split) contradicts **ADR-0001 §2 (Accepted)**: personal identifiers "are
    removed during ingestion, before anything is written to `data/processed/`".
    D7.1 is therefore **not recorded**. Options are listed as D7.1′.
  - **T3, T4, T5, T6 VERIFIED** against their criteria.
  - T7 was blocked on D7.1′. Commit `0f3dc19`.
- **D7.1′ (a), staging, approved (2026-10-28).**
  - Order: rules-only screen, then the split frozen in an ignored staging area
    (`data/interim/`), then a role-restricted human screen, then only passing
    records written to `data/processed/`.
  - Checked against ADR-0001 §2, ADR-0006 §12 and §17, ADR-0007 §3 and §5, D5.1,
    D7.3, Blocker 1 and Blockers 2/8: no conflicts.
  - **T7 VERIFIED.**
  - New coupling: human-screen exclusions aren't reproducible on rebuild, so T8's
    denylist must cover them.
- T8 decision requests D8.1–D8.4 prepared. Commit `6ae0221`.
- **T8 rulings (2026-10-28): D8.1–D8.4 accepted as recorded.**
  - Checked against ADR-0001–0008, Blockers 1, 2 and 8, D5.1, D7.1′ and fixed
    assignment: no conflicts.
  - Derived:
    - the §13 deletion exception
    - denylist matching on all three fields
    - a documented limitation for new snapshots and duplicates across sources
    - the reason-category list left to `docs/schema.md` (gap)
  - **T8 VERIFIED.**
- T9 decision requests D9.1–D9.2 prepared. Commit `32deeb4`.
- **T9 rulings (2026-10-28).**
  - D9.1 accepted. §20 is to be revised in T11.
  - D9.2 (a) accepted subject to verification, then **verified**: UCD 15.0.0
    `Scripts.txt`, which matches `unidata_version` 15.0.0.
    - official URL, HTTP 200 retrieved 2026-10-28T14:20:02Z
    - SHA-256 `cca85d83…ea4b0`
    - the code-point set matches Python's assigned characters exactly
    - Unicode License v3 (`copyright.html` §2.2/§3.3, `license.txt`), retrieved
      2026-10-28
  - Kept explicit:
    - no publisher-published checksum was found or checked
    - the file is in scratch only (not vendored or committed)
    - using it needs a `data/manifests/` entry
  - **T9 VERIFIED.**
- T10 decision requests D10.1 and D10.2 prepared. Commit `5c71642`.
- **T10 rulings (2026-10-28).**
  - D10.1 accepted: joint, explicit, dated acceptance after T11; re-approval of
    changed items by name. The approval in principle doesn't cover revised text.
  - D10.2 accepted in the maintainer's 13-step wording.
  - No conflicts. **T10 VERIFIED.**
- **T11 READY.**
  - Section-by-section edit map prepared in the graph, mapping every ADR-0006 and
    ADR-0007 section to the rulings it must incorporate.
  - Also prepared: a re-approval list and the preserved gaps.
  - No ADR text drafted yet.
  - No file-level evidence exists for any source field (B6), so per-source
    eligibility stays pending. This isn't a T6 criterion.

## Verification

| Date / checkpoint | Command | Result |
|---|---|---|
| 2026-10-28, T0 | `uv sync --locked` | 10 packages checked, exit 0 |
| | `uv run ruff check .` | All checks passed |
| | `uv run ruff format --check .` | 20 files already formatted |
| | `uv run pytest` | 26 passed in 79 s |
| | `git diff --cached --check` | no output, exit 0 |
| 2026-10-28, T1 | `git diff --check` | no output, exit 0 |
| 2026-10-28, T2 | `uv sync --locked` | 10 packages checked, exit 0 |
| | `uv run ruff check .` | All checks passed, exit 0 |
| | `uv run ruff format --check .` | 23 files already formatted, exit 0. Ruff includes `.md` files; the 3 workflow files account for 20 → 23. |
| | `uv run pytest` | 26 passed in 78.9 s, exit 0 |
| 2026-10-28, T3–T7 | `uv run python -I` (scratch vector script) | 6 vectors + 6 boundaries printed; asserts ok, exit 0 |
| | `git diff --check` | no output, exit 0 |
| | `uv run ruff format --check .` | 23 files already formatted, exit 0 |
| | `uv run ruff check .` | All checks passed, exit 0 |
| | `uv run pytest` | not rerun (docs-only change) |
| 2026-10-28, T3–T7 rulings | `git diff --check` | no output, exit 0 |
| | `uv run ruff format --check .` | 23 files already formatted, exit 0 |
| | `uv run ruff check .` | All checks passed, exit 0 |
| | status audit (grep of the graph table and per-task status lines) | T0–T6 VERIFIED, T7 BLOCKED, T8 READY, T9–T12 BLOCKED; no stale or contradictory lines |
| 2026-10-28, D7.1′ + T8 requests | `git diff --check` | no output, exit 0 |
| | `uv run ruff format --check .` | 23 files already formatted, exit 0 |
| | `uv run ruff check .` | All checks passed, exit 0 |
| | status audit | T0–T7 VERIFIED, T8 BLOCKED (D8.1–D8.4), T9–T12 BLOCKED |
| | `uv run pytest` | not rerun (docs-only change) |
| 2026-10-28, T8 rulings + T9 requests | `git diff --check` | no output, exit 0 |
| | `uv run ruff format --check .` | 23 files already formatted, exit 0 |
| | `uv run ruff check .` | All checks passed, exit 0 |
| | status audit | T0–T8 VERIFIED, T9 BLOCKED (D9.1, D9.2), T10–T12 BLOCKED; no stale lines |
| | `uv run pytest` | not rerun (docs-only change) |
| 2026-10-28, T9 rulings + T10 requests | `uv run python -I -c` (versions) | Python 3.12.14, `unidata_version` 15.0.0 |
| | `curl` Scripts.txt to scratch | HTTP 200, exit 0, 2026-10-28T14:20:02Z; `sha256sum` `cca85d830f46aece2e7c1459ef1249993dca8f2e46d51e869255be140d7ea4b0` |
| | `uv run python -I` (scratch version-match script) | listed 149,251 = assigned 149,251; asserts ok, exit 0 |
| | `git diff --check` | no output, exit 0 |
| | `uv run ruff format --check .` | 23 files already formatted, exit 0 |
| | `uv run ruff check .` | All checks passed, exit 0 |
| | status audit | T0–T9 VERIFIED, T10 BLOCKED (D10.1, D10.2), T11–T12 BLOCKED; no stale lines |
| | `uv run pytest` | not rerun (docs-only change) |
| 2026-10-28, T10 rulings + T11 edit map | `git diff --check` | no output, exit 0 |
| | `uv run ruff format --check .` | 23 files already formatted, exit 0 |
| | `uv run ruff check .` | All checks passed, exit 0 |
| | `git diff --stat -- docs/decisions src scripts tests` | empty (no ADR or code changes) |
| | status audit | T0–T10 VERIFIED, T11 READY, T12 BLOCKED |
| | `uv run pytest` | not rerun (docs-only change) |

## Failed attempts

- T2: a shell `node -e` edit script failed on quoting (bash syntax error) before
  writing anything. The edits were redone with the Edit tool.
- T3–T7, three shell problems:
  - A stray `cat >` waited on stdin and hung the vector command. It was stopped,
    and the script was rewritten with the Write tool.
  - A long `cat >> ... <<'EOF'` append failed with a bash quoting error and wrote
    nothing.
  - Both appends were redone with the Edit tool.
  - Lesson: write file content with Write or Edit, never shell heredocs, in this
    environment.

## Open decisions

Each needs maintainer input.

- W0: review and approval.
- G-ADR67: the open items in `docs/workflow/reviews/G-ADR67.md` section 4b (I7, I8, I9, I11, native
  `source_record_ref` screening, N1, rebuild scope, revision numbers, ADR-0008 rev 3), then
  acceptance of ADR-0006, ADR-0007 and ADR-0008 by the maintainer.
- E-LGD: the options in `docs/workflow/cards/E-LGD.md`.
- G-SRC: B14, retrieval and what counts as field evidence (same packet).
- H-SCREENER: assign the screener.
- Evidence gaps preserved: no source accepted; B6, B14–B17; the C1a field
  documentation; reason categories; L1; the `Scripts.txt` manifest; P1–P7.

## T11 draft (2026-10-28, branch `adr-0006-rev6`)

- ADR-0007 rev 4 and ADR-0006 rev 6 were drafted from the edit map. Both stay
  Proposed.
- Decision rows changed in the actual diff:
  - ADR-0006: F1, F3, F5, F9, F10, F12, new F14 and F15, and L3
  - ADR-0007: S6, S9, E1, E3
- Checks: `git diff --check` exit 0; ruff check passed; ruff format: 23 files
  already formatted; pytest 26 passed (84.8 s).
- Derived edits beyond the map:
  - `admission.screened_by` records both screen stages
  - the T5 test vectors are copied into §17
  - §20 clarifies that `schema_version` and `benchmark_version` are separate
- **Review completed** (2026-10-28, second checkpoint on the branch). Both diffs
  were read in full against the edit map and the rulings. Fixes:
  - ADR-0007 §3 still said "allowlisted state column" and "before any merge".
    Now: the declared column, matched after tokens and aliases, before duplicate
    classes are formed.
  - ADR-0006 §7 step 2: the level of a role without a designator was undefined.
    Now: its label's level.
  - ADR-0006 §7 step 8: an empty result could override `no_match_in_snapshot`.
    It is now kept.
  - ADR-0006 §8: a paragraph that had run into the next one was split.
  - ADR-0006 L5: outdated "duplicate merges" wording.
  - ADR-0006 §19: the history note on revision 5 is now factual.
- Cross-reference check:
  - Every cited section exists: ADR-0006 §2, §3, §7, §10, §12, §14, §17, §18;
    ADR-0007 §2, §5, §6, §8.
  - The only remaining "merged group" text is in the revision notes.
  - ADR-0006, ADR-0007 and ADR-0008 are all Proposed. ADR-0008 is unchanged.
- **Re-approval list**, from the diff:
  - ADR-0006: F1, F3, F5, F9, F10, F12, new F14, new F15. Deferred rows reworded:
    L3, L5.
  - ADR-0007: S6, S9. Deferred rows reworded: E1, E3.

## Next action

**Version 1.0.0 is released; version 2 waits on the maintainer, and no agent task is ready.** E-FIELD's first criterion needs
publisher documentation that was not found for any candidate, so it depends on G-SRC decision 3.
The other maintainer decisions are listed above.

## Session log

### 2026-10-29 — W0 — blocked

- **Did:** Reconciled `workflow/graph.toml` with `docs/research/dependency-graph.md`.
  - Real ADR paths are now `docs/decisions/`.
  - Legacy T11 maps to G-ADR67. Its draft exists only on the local branch `adr-0006-rev6`;
    this branch still says T11 is READY.
  - T12 is `dropped`, with its scope mapped to implementation nodes and removed from
    I-INGEST's deps.
  - I-VALIDATOR now waits on D-GUIDE (D10.2).
  - Acceptance criteria added for the T5 vectors, `docs/schema.md` formats, `Scripts.txt`
    provenance, the ADR-0001 §5 manifest fields and screening.
  - Diagram regenerated. Task card: `docs/workflow/cards/W0.md`.
- **Proof:** `ruff check` passed; `ruff format --check` **failed** (1 file:
  `.claude/hooks/pata_guard.py`, protected); `pytest -q` 108 passed, 4 skipped;
  `graph.py validate --check-outputs` OK; `git diff --check` exit 0.
  - Verifier: criteria 1–3 PASS, criterion 4 FAIL on one sub-check (a missing ADR-0001 §5
    field), since fixed. The verifier has not re-run since the fix.
- **Branch / commit:** `workflow-kit`, uncommitted (maintainer instruction). Not pushed, not
  merged.
- **Now ready:** E-LGD, E-INV, H-SCREENER (Phase 1 and 2 work is on hold until W0 is reviewed).
- **Needs maintainer:**
  - approve and run the formatting-only change to `pata_guard.py`
  - decide the `Scripts.txt` storage path and the staging path
  - review W0
- **New nodes added:** none. Candidates are listed in the task card.
- **Open risks:** none new.

### 2026-11-04 to 2026-11-05 — W0, E-LGD, E-INV, E-B6 — evidence and verification

- **Did:**
  - W0: `pata_guard.py` was found unformatted on disk; the maintainer authorised
    `uv run ruff format .claude/hooks/pata_guard.py`. Three G-ADR67 acceptance gaps against D10.1 were
    fixed; all tighten the gate. `Scripts.txt` path and `staging/` recorded per maintainer instruction.
  - E-LGD: `docs/evidence/lgd/levels.md`. Levels exist; per-state sub-district meaning stays UNVERIFIED.
  - E-INV: eleventh pass in `docs/research/source-inventory.md`, R111–R125.
  - E-B6: `scripts/source_stats.py`, tests on synthetic fixtures only. Never run on a real file.
  - E-FIELD and E-LIC evidence drafted. Packets: `docs/workflow/reviews/G-ADR67.md`, `G-SRC.md`.
- **Process slip:** E-FIELD, E-LIC and E-B6 work was drafted before E-INV closed, against "one node at a
  time". The guard caught E-B6's status. E-FIELD and E-LIC stay `todo` and need their own verifier run.
  E-B6's dep on E-INV was removed as wrong; a verifier judged that sound.
- **Proof:** verifier results are in each task card.
  - W0: four runs; Overall PASS on the fourth. `uv run pytest -q` 119 passed, 4 skipped;
    `ruff format --check` 54 files already formatted; `graph.py validate --check-outputs` OK.
  - E-LGD: three runs; Overall PASS on the third. E-B6: Overall PASS, with test gaps listed in its card.
  - E-INV: two runs; FAIL, blocked on C9c only. A later C10 correction has not been re-verified.
- **Data:** no candidate address file retrieved. `data/raw/data.gov.in/` is empty.
- **Branch / commit:** `workflow-kit`, uncommitted (maintainer safeguard). Not pushed, not merged.
- **Needs maintainer:** W0 review; E-LGD options; C9c ruling; G-ADR67 decision; G-SRC readings;
  H-SCREENER.
- **Obligations with no acceptance row (from the W0 verifier; not added as nodes):** eligibility
  assessment before source acceptance (D10.2 step 3; the sharpest gap, since G-SRC can close without
  it); split-key step 2, D4.5 district rules; `raw_text_scope` and `record_id_scope` in D-SRCADR;
  running E-B6 on a real file.
- **Tool defects seen, not fixed:** `graph.py show` and `progress` crash with `UnicodeEncodeError` on
  a cp1252 stdout; `validate --check-outputs` skips outputs containing `(`.
- **G-ADR67 option B draft (maintainer go, 2026-11-05):** `docs/workflow/reviews/G-ADR67-rev7-rev5.patch`,
  not applied to any branch. It covers I1–I5 and the O/E sentence. `adr-reviewer` found the first
  version also made new decisions on I6 and I10 and missed one I2 occurrence. Those hunks were removed
  and I2 fixed; both are now decision requests in the packet, section 4b. The reduced patch has
  mechanical checks only (`git apply --cached --check` on a temporary index of `adr-0006-rev6` exit 0;
  28 and 22 decision rows unchanged; status lines Proposed) and no second reviewer run. G-ADR67 stays
  `review`.
- **G-ADR67 rulings (maintainer, 2026-11-05):** Option A for I6 and I10, recorded in
  `docs/research/dependency-graph.md` and added to the patch. A second `adr-reviewer` run found them
  implemented with no added rule; one revision note was then corrected and has no reviewer run. Not
  ready for acceptance: I7, I8, I9, I11, native `source_record_ref` screening, N1, rebuild scope,
  revision numbers and ADR-0008 rev 3 remain open (packet section 4b).

### 2026-11-08 — no node — state audit of the uncommitted work

- **Did:** Audited the uncommitted changes against the graph. Removed the kit's install markers from
  `CLAUDE.md` and `.gitignore` (comments only). Updated this file's objective, repository state, open
  decisions and next action, which still described 2026-10-28. No node status changed.
- **Proof, before those edits:** `uv sync --locked` exit 0; `uv run pytest -q` 119 passed, 4 skipped.
  `git apply --cached --check` of `G-ADR67-rev7-rev5.patch` on a temporary index of `adr-0006-rev6`
  exit 0.
- **Proof, after those edits:** `ruff check` passed; `ruff format --check` 54 files already formatted;
  `uv run pytest tests/workflow -q` 82 passed, 4 skipped; `graph.py validate --check-outputs` OK;
  `git diff --check` exit 0.
- **Verifier, W0, before commit:** criteria 1–4 PASS, Overall PASS; `uv run pytest -q` 119 passed,
  4 skipped. Table in `docs/workflow/cards/W0.md`. No node changed status.
- **Verifier caveats, new:** the guard blocks the read-only `git merge-base --is-ancestor`, so
  `099fdb6` and `0513447` being on `adr-0006-rev6` was not checked by it. G-SRC has no G-ADR67
  ancestor, so a source decision can be recorded before ADR acceptance, although D10.2 numbers
  acceptance first. "Required statistics" and "selection records" appear only in the I-SPLITKEY
  title, with no acceptance row. None is fixed here.
- **Branch / commit:** `workflow-kit`, committed on maintainer instruction, split by node group. Not
  pushed, not merged.
- **Graph edit after those commits (maintainer instruction, 2026-11-08):** G-SRC now depends on G-ADR67,
  closing the verifier's gate-order caveat. A second W0 verifier run, on the tree with this edit,
  gave criteria 1–4 PASS, Overall PASS; `uv run pytest -q` 119 passed, 4 skipped.
- **Not done:** the `graph.py` defects listed above are still present; `progress` was reproduced
  crashing on cp1252 stdout on 2026-11-08. Fixing them changes W0 after its verifier pass.
- **W0 verifier, later on 2026-11-08 (at `17540a2`): Overall FAIL.** Criteria 1–3 PASS. Criterion 4
  FAIL: no node gating G-SRC carries the eligibility assessment of D10.2 step 3. The table is in the
  W0 card (`714bb4d`). W0 stays in `review`; it needs a new acceptance row or a maintainer ruling.
- **G-ADR67 patch (maintainer go, 2026-11-08):** text fixes I7, I8, I9 and I11 added to
  `docs/workflow/reviews/G-ADR67-rev7-rev5.patch`, not applied to any branch. `git apply --cached` on
  `adr-0006-rev6` in a temporary index exits 0. Third `adr-reviewer` run: all four fixes PASS, no table
  row changed, status lines still Proposed; UNPROVEN on §20's "selected geography" wording and two
  points in the rev 7 note (packet section 4b). §20 was then aligned on maintainer go, with
  mechanical checks only and no further reviewer run. Native `source_record_ref`, N1, rebuild scope
  and revision numbers still need rulings.
- **Gate checks, 2026-11-08 at `714bb4d`:** ruff and format pass (54 files); `uv run pytest -q` 119
  passed, 4 skipped; `git diff --check` exit 0; graph OK. On an export of `adr-0006-rev6` (`0513447`):
  ruff and format pass (23 files); pytest 25 passed, 1 skipped.
- **Recheck, 2026-11-08, uncommitted tree over `714bb4d`:** two blank context lines added to the
  G-ADR67 patch failed `git diff --check`; their single trailing space was removed. The patch produces
  the same tree before and after (`008a412`) and its index hashes match. Ruff and format pass (54
  files); `uv run pytest -q` 119 passed, 4 skipped; `git diff --check` exit 0; graph OK. On a temporary
  export of `adr-0006-rev6` plus the patch: ruff and format pass (24 files, temporary virtualenv
  excluded); pytest 25 passed, 1 skipped. Packet sections 5–7 brought up to date. Patch still unapplied.
- **E-INV done, 2026-11-08.** C9c's catalog and file URL found from page metadata (R126); the file was
  not downloaded and C9c was not ruled on. Third verifier run: PASS on both criteria, including the
  C10 correction; ruff, format, `git diff --check` and graph pass; pytest 119 passed, 4 skipped.
  Caveat: today's metadata gives a different file path for C10's first URL and two C9b files, and
  whether the old paths resolve is UNKNOWN (card `docs/workflow/cards/E-INV.md`).

### 2026-11-09 — E-LIC — done

- **Did:** Finished the licence table in `docs/research/source-inventory.md`: added C9c, corrected C4's
  attribution and the state-instance terms, split "last read" dates by source, and read the C5, C6 and
  C12 policy pages (R127–R130). KVS's policy page has moved to `kvs.gov.in`. Evidence only; B14, B15,
  B3, B16, B17 and B4 stay open, and no source was accepted or rejected.
- **Proof:** verifier run 1 FAIL, run 2 FAIL (criterion 1 only), run 3 Overall PASS, both criteria
  (table in `docs/workflow/cards/E-LIC.md`). ruff and format pass; `uv run pytest -q` 119 passed,
  4 skipped; graph OK; `git diff --check` clean.
- **Branch / commit:** `workflow-kit`, uncommitted. Not pushed, not merged.
- **Data:** no candidate data file requested. Only policy, home and directory pages were fetched.
- **Needs maintainer:** the G-SRC readings. Note that the verifier's spot-check sent one request to
  `tn.data.gov.in/policies`, a path that host's `robots.txt` disallows, with a generic browser
  user-agent. For R127–R130, `robots.txt` was checked only for `saras.cbse.gov.in` (HTML 404).
- **New nodes added:** none.
- **Open risks:** `focus-state-source-evaluation.md:252` still describes C10 as "As C1b"; the inventory
  corrects it, and it was left unedited to keep the verified tree unchanged.
- **Commit, after this entry:** E-LIC was committed as `7947461`.

### 2026-11-09 — no node — push and merge recorded

- **Did:** Recorded the maintainer's push and the merges of PR 1 and PR 2 in this file. No node status
  changed. Claude's own push attempt was blocked by the guard hook; the maintainer pushed.
- **Proof:** `git fetch origin`; `origin/main` at `0c72e75`; `gh pr list` shows both PRs merged;
  ADR status lines read from `origin/main`.
- **Not checked:** whether `docs/workflow/reviews/G-ADR67-rev7-rev5.patch`, prepared against
  `adr-0006-rev6`, still applies to `origin/main`.
- **Branch / commit:** `workflow-kit`, this update uncommitted. Not pushed.
- **Needs maintainer:** update local `main`; the open reviews listed above.

### 2026-11-09 — W0, E-B6, E-FIELD — sprint on eligible nodes

- **Did:** W0: added the eligibility, D4.5 and manifest-scope acceptance rows the verifier asked for;
  fixed the `graph.py` cp1252 crash, the `--check-outputs` skip on `(`, and CRLF from `progress --write`.
  E-B6: added the missing leak and per-process tests, non-CSV detection and `--expected-column`.
  E-FIELD: added rows C7 and C9c and read R131–R133; no field gained a publisher definition.
  No Phase 2–7 node was started: each waits, directly or indirectly, on a maintainer gate.
- **Proof:** W0 verifier Overall PASS (after one FAIL on criterion 4). E-B6 verifier Overall PASS.
  E-FIELD verifier Overall FAIL on criterion 1, PASS on criterion 2. Final gates: `uv lock --check`
  exit 0; `uv sync --locked` exit 0; ruff passed; format 54 files; `uv run pytest -q` 142 passed,
  4 skipped; `graph.py validate --check-outputs` OK; `git diff --check` exit 0.
- **Status:** W0 stays `review`. E-B6 stays `done`. E-FIELD is `blocked`. Graph: 4 of 29 done, unchanged.
- **Real-file validation of E-B6:** not done; no candidate file is held. Synthetic fixtures only.
- **Branch / commit:** `workflow-kit`, committed by node group on the maintainer's instruction, after
  W0 and E-B6 verifier reruns (both Overall PASS, tables in their cards).
- **Needs maintainer:** G-ADR67; W0 approval; E-LGD option; G-SRC decision 3; H-SCREENER.
- **New nodes added:** none.
- **Open risks:** D-SPLITCFG can close without the focus-state ADR named in its title (no acceptance row).

### 2026-11-09 — G-ADR67 — rulings applied, awaiting acceptance

- **Did:** The maintainer fast-forwarded `workflow-kit` to `origin/main` (`aeb13b8`); Claude's attempt was
  blocked by the guard. Applied `docs/workflow/reviews/G-ADR67-rev7-rev5.patch` to the working tree and
  added the 2026-11-09 rulings to ADR-0006 rev 7 and ADR-0007 rev 5. Rulings recorded in
  `docs/research/dependency-graph.md`.
- **Proof:** `uv lock --check` exit 0; ruff passed; format 54 files; `graph.py validate --check-outputs`
  OK; `git diff --check` exit 0; all 56 ADR decision and open-item rows byte-identical to `aeb13b8`; all
  three status lines Proposed. `uv run pytest` equivalent, no cache: 142 passed, 4 skipped. A first run
  failed one hook test only because the shell had `PYTHONIOENCODING=utf-8` set; it passes without it.
  No `adr-reviewer` run on the 2026-11-09 text.
- **Status:** G-ADR67 stays `review`. No ADR accepted.
- **Later the same day, maintainer rulings:** E-FIELD deadline 2026-11-23; a screener must not annotate
  records they screened (ADR-0006 §12); D10.2 orders real-data work only; four `-CODE` nodes added to the
  graph on the maintainer's approval (29 to 33 live nodes). OSM stays out of v1; if B14 is not cleared by
  2026-11-23, prepare a Proposed ADR for OSM as a fallback.
- **Graph approvals:** W0 and E-LGD have no `[[approval]]` entry in `workflow/graph.toml`, checked
  2026-11-09. Both stay `review`.
- **Branch / commit:** `workflow-kit`, uncommitted. Not pushed.
- **Needs maintainer:** send the B14 and LGD emails (not sent); run `graph.py approve` for W0 and E-LGD;
  review the diff and accept.
- **Open risks:** N1 can move a whole district key into `test_source_holdout`, which bears on P6. The
  `-CODE` fixtures' `source_type = 'synthetic'` conflicts with ADR-0006 §2 and F6 (`real` only) unless
  `docs/schema.md` keeps the label in fixture metadata.

### 2026-11-10 — G-ADR67 — fourth reviewer run and text fixes

- **Did:** Fourth `adr-reviewer` run on the rev 7 / rev 5 / rev 3 text; findings in packet section 6a.
  On maintainer go, drafted X1 and X2 in ADR-0007 rev 5 and updated G-ADR67's graph title, two acceptance
  rows and notes to the current revisions.
- **Proof:** Reviewer: cross-reference checks do not pass as written; 50 decision rows byte-identical to
  `aeb13b8`; each status line Proposed. After the fixes: `graph.py validate --check-outputs` OK;
  `tests/workflow/test_graph.py` 34 passed. No reviewer run on the X1 and X2 text.
- **Status:** G-ADR67 stays `review`. No ADR accepted.
- **Branch / commit:** `workflow-kit`, uncommitted. Not pushed.
- **Later the same day:** maintainer rulings X3a, X4a, E2c and X5a, recorded in
  `docs/research/dependency-graph.md` and drafted into ADR-0006 rev 7. Fifth `adr-reviewer` run: rulings
  faithful, 25 decision rows byte-identical, status lines Proposed; cross-reference checks still do not
  pass as written (packet section 6b).
- **Later again:** maintainer rulings C1a, C2a, lead-source columns a, and S7/S8 added; drafted with graph
  rows C3–C7. Sixth `adr-reviewer` run: all earlier items resolved; cross-reference checks narrowly do
  not pass (packet section 6c). `test_graph.py` 40 passed; graph, ruff and format pass.
- **Then:** maintainer rulings N1, N2 and R1–R3, drafted; E-FIELD criterion 1 reworded by the maintainer.
  Seventh `adr-reviewer` run, scoped: those items resolved; M1 and M2 remain (packet section 6d). Fourth
  consecutive round not to clear the check, so stopped under the three-attempt rule.
- **Final:** maintainer ruling option A for M1 and M2, drafted into ADR-0006 §17. Mechanical checks only, by
  agreement: approval tables byte-identical to `aeb13b8`; all three status lines Proposed; ruff, format,
  graph validate and `git diff --check` pass. No `adr-reviewer` run on that sentence.
- **Needs maintainer:** judge the cross-reference checks; read the full diff; re-approve F1, F3, F5, F9, F10,
  F12, F14, F15, S6, S7, S8 and S9 by name; confirm deferred items; commit; write the dated acceptance;
  run `graph.py approve G-ADR67`. Also send the B14 and LGD emails.
- **Maintainer direction, 2026-11-10:** version 1 uses available pinned data; live data waits for later
  versions. README updated to the current state. No node status changed: no address file is held, and
  every remaining build node waits on a maintainer gate. Claude cannot push; the maintainer pushes.

### 2026-11-10 — G-V1SCOPE — version 1 rescoped, awaiting acceptance

- **Did:** On the maintainer's direction, drafted ADR-0009: version 1 is a gazetteer toolkit and PataBench
  moves to version 2. Added nodes G-V1SCOPE, I-V1KIT and R-V1, marked 27 benchmark nodes `release = "v2"`,
  and added a version 1 count to the progress block. README updated.
- **Proof:** see the checks run before commit; `tests/workflow/test_graph.py` 44 passed; graph OK. No
  `adr-reviewer` run on ADR-0009.
- **Status:** G-V1SCOPE `review`. ADR-0009 Proposed. ADR-0006, 0007 and 0008 stay Proposed.
- **Branch / commit:** `workflow-kit`, uncommitted. Not pushed.
- **Needs maintainer:** accept ADR-0009; run `graph.py approve` for G-V1SCOPE, W0 and E-LGD.
- **Open risks:** a user's fresh LGD download is refused until they re-pin; users cannot reproduce the
  maintainer's exact gazetteer without the same files (ADR-0009 section 4).

### 2026-11-10 — I-V1KIT — done

- **Did:** The maintainer accepted ADR-0009 (`6faa28a`) and approved G-V1SCOPE, W0 and E-LGD in their own
  terminal; those nodes are `done`. Wrote `docs/toolkit.md`, `tests/test_toolkit_v1.py` and the README scope.
- **Proof:** I-V1KIT verifier: first run FAIL (guide step 2 gave a path that is not found; the test skipped
  it); fixed; second run Overall PASS, 4 of 4. `uv run pytest -q` 160 passed, 5 skipped.
- **Limits:** synthetic fixtures only. No real LGD re-pin was run, and the portal download step was not run.
- **Branch / commit:** `workflow-kit`, uncommitted. Not pushed.
- **Now ready:** R-V1 (irreversible; needs the maintainer's explicit "go R-V1").
- **Needs maintainer:** "go R-V1"; then tag, push and publish.
- **New nodes added:** none.
- **Open risks:** the README tagline still says "benchmark and ML toolkit", to reconcile in R-V1.

### 2026-11-10 — R-V1 — prepared, awaiting the maintainer

- **Did:** On the maintainer's "go R-V1", set the package and lock to 1.0.0, wrote `CHANGELOG.md`, and made
  the README and package description match ADR-0009.
- **Proof:** `uv lock --check` exit 0; ruff passed; format passed; `uv run pytest -q` 160 passed, 5 skipped;
  graph OK; `git diff --check` exit 0. R-V1 verifier: criteria 1 and 3 PASS; criterion 2 UNPROVEN (no commit
  yet) and criterion 4 not done (maintainer's step). Table in `docs/workflow/cards/R-V1.md`.
- **Status:** R-V1 `in_progress`. Graph: 8 of 36 live nodes done; version 1: 8 of 9.
- **Released, 2026-11-10:** the maintainer pushed, tagged `v1.0.0` at `718549d`, published the GitHub release
  and approved R-V1. CI passed on `718549d`. Final verifier Overall PASS, 4 of 4; on a clean export of the
  tag, pytest 159 passed, 6 skipped (the sixth skip needs the pinned LGD snapshots). R-V1 is `done`.
- **Needs maintainer, for version 2:** G-ADR67 acceptance; the B14 and LGD emails (deadline 2026-11-23);
  H-SCREENER.

## Dependency graph status

<!-- graph:progress:begin -->
_Generated from `workflow/graph.toml` on 2026-11-10 — do not edit by hand._

**Graph nodes done:** 9/36 (node count, not effort; design nodes ≠ implementation).
**Of those in version 1 (ADR-0009):** 9/9.

| Phase | Node | Status | Gate | Waiting on |
|---|---|---|---|---|
| P0-governance | **LEGACY** T0–T10 design/planning tasks (imported) | done | — | — |
| P0-governance | **W0** Install workflow kit (graph, LOOP, hooks, commands, agents) | done | maintainer | — |
| P0-governance | **G-ADR67** T11 + D10.1: review and joint acceptance of ADR-0006 rev 7 and ADR-0007 rev 5 | review | maintainer | — |
| P3-pipeline | **T12** T12 implementation task (scope per legacy dependency graph) | dropped | — | G-ADR67 |
| P1-evidence | **E-LGD** LGD level verification: state / district / sub-district / village | done | maintainer | — |
| P1-evidence | **E-INV** Candidate source inventory (exact files/snapshots, publishers) | done | — | — |
| P1-evidence | **E-FIELD** Field semantics evidence (incl. C1a Address_Original_First_Line) | blocked | — | — |
| P1-evidence | **E-LIC** Licence + redistribution evidence (B14–B17) | done | — | — |
| P1-evidence | **E-B6** Scripted aggregate inspection of candidate source files (B6) | done | — | — |
| P1-evidence | **G-SRC** Maintainer accept/reject decision per source | todo | maintainer | G-ADR67, E-FIELD |
| P2-spec | **D-SCHEMA** docs/schema.md: schemas, statuses, reason-category vocabulary, provenance fields | todo | maintainer | G-ADR67 |
| P2-spec | **D-SRCADR** Source ADRs + provenance manifests | todo | maintainer | G-SRC, D-SCHEMA |
| P2-spec | **U-UNICODE** Vendor Unicode Scripts.txt pinned to Python unicodedata version | todo | — | G-ADR67 |
| P3-pipeline | **I-INGEST-CODE** Ingestion code on labelled synthetic fixtures (no real-data run) | todo | — | G-ADR67, D-SCHEMA |
| P3-pipeline | **I-INGEST** Ingestion: strict decoding, parsing, eligibility, reason-coded exclusions | todo | — | D-SRCADR, I-INGEST-CODE |
| P3-pipeline | **G-ADR8** Maintainer acceptance of ADR-0008 (before selection records) | todo | maintainer | G-ADR67 |
| P3-pipeline | **I-SPLITKEY-CODE** Split-key code on labelled synthetic fixtures (no real-data run) | todo | — | I-INGEST-CODE, U-UNICODE |
| P3-pipeline | **I-SPLITKEY** Split-key step 1, duplicate classes, required statistics, selection records | todo | — | I-INGEST, G-ADR8, U-UNICODE, I-SPLITKEY-CODE |
| P3-pipeline | **D-SPLITCFG** Focus-state ADR + split config (salt, held-out publishers, ratio weights) | todo | maintainer | I-SPLITKEY |
| P4-screen | **I-RULESCREEN-CODE** Rules-only screen code on labelled synthetic fixtures (no real-data run) | todo | — | I-INGEST-CODE, D-SCHEMA |
| P4-screen | **I-RULESCREEN** Rules-only privacy screen in ignored staging | todo | — | I-INGEST, D-SCHEMA, I-RULESCREEN-CODE |
| P4-screen | **X-FREEZE** Freeze split in staging + start exposure log | todo | maintainer · irreversible | D-SPLITCFG, I-RULESCREEN |
| P4-screen | **H-SCREENER** Assign eligible role-restricted test/holdout screener | todo | maintainer | — |
| P4-screen | **H-SCREEN** Role-restricted human screen + private denylist | todo | maintainer | X-FREEZE, H-SCREENER |
| P5-resolve | **I-TABLES** Reference list, normalization table, cue table (dev-pool only) | todo | — | H-SCREEN |
| P5-resolve | **I-RESOLVE** Candidate generation + resolution with verification gates | todo | — | I-TABLES |
| P5-resolve | **D-GUIDE** Finalize + freeze annotation guidelines | todo | maintainer | I-RESOLVE |
| P5-resolve | **I-VALIDATOR-CODE** Validator code on labelled synthetic fixtures (no real-data run) | todo | — | D-SCHEMA |
| P5-resolve | **I-VALIDATOR** Validator: schema, invariants, provenance, splits, gates, exclusions, manifest | todo | — | D-SCHEMA, D-GUIDE, I-VALIDATOR-CODE |
| P6-annotate | **P-PILOT** Dev-pool annotation pilot + reliability metrics | todo | — | D-GUIDE, I-VALIDATOR |
| P6-annotate | **G-PILOT** Maintainer resolves pilot decisions | todo | maintainer | P-PILOT |
| P6-annotate | **A-GOLD** Gold annotation: independent annotation, adjudication, audit trail | todo | maintainer | G-PILOT |
| P7-release | **B-BASE** Baselines + evaluation scripts | todo | — | A-GOLD |
| P7-release | **R-REL** Release PataBench (version 2 under ADR-0009): manifest, hashes, metrics, exclusions, limitations, versioning | todo | maintainer · irreversible | B-BASE |
| P0-governance | **G-V1SCOPE** Maintainer decision on ADR-0009: version 1 is a gazetteer toolkit | done | maintainer | — |
| P7-release | **I-V1KIT** Toolkit v1 readiness: user guide, re-pinning path, honest claims | done | — | — |
| P7-release | **R-V1** Release Pata gazetteer toolkit 1.0.0 | done | maintainer · irreversible | — |

**Ready now:** H-SCREENER
**Awaiting maintainer:** G-ADR67
<!-- graph:progress:end -->
