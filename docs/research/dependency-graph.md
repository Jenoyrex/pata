# Dependency graph: ADR-0006 / ADR-0007 acceptance work

Working note, not a decision record. It tracks the acceptance-readiness review of
ADR-0006 revision 5 and ADR-0007 revision 3, and the maintainer rulings made so
far. Rulings listed here are **not yet written into the ADRs**. The ADR text stays
authoritative until a revision incorporates them.

"Blocker N" means a blocker from that review. These are unrelated to the source
blockers B1, B2, ... in `focus-state-source-evaluation.md`.

Statuses: BLOCKED, READY, IN PROGRESS, VERIFIED, ACCEPTED. A decision task is
READY when its prerequisites are resolved and its options are written up. The
maintainer's ruling is the work.

## Edges

`A → B`: B can't proceed until A is resolved.

```
T0 ─────────────────────────────────────────────┐
T1 (Blocker 2 rest) → T2 (Blocker 8) → T3 (Blocker 9)
T4 (Blocker 5) ── same §17 text, edit together ── T5 (Blocker 4)
T6 (Blocker 6) → T8 (Blocker 3) ← Blocker 1 (decided)
T7 (Blocker 10)
T1..T8 → T9 (Blocker 7) → T10 (Blocker 11 ordering)
T1..T10 → T11 (ADR-0006 rev 6 + ADR-0007 rev 4) → maintainer acceptance → T12
```

- T1 → T2: R1f (anchor invalidation) overlaps Blocker 8's "multiple higher-level
  anchors", and both edit ADR-0006 §7–§9.
- T2 → T3: Blocker 9's per-annotator Layer D needs settled Layer C statuses and sets.
- T6 → T8: a withdrawal denylist keys on `raw_text_sha256`, which depends on
  decoding.
- T4, T5, T6, T7 have no prerequisites. The order below is a recommendation, not a
  dependency.
- T11 waits for every decision. The maintainer asked for one coordinated
  revision, not piecemeal edits.

## Tasks

| ID | Task | Status | Prerequisites | Affected text | Needs from maintainer | Done when |
|---|---|---|---|---|---|---|
| T0 | Workflow files (`CLAUDE.md`, `PROGRESS.md`, this note) | VERIFIED | — | these files | — | CI checks and `git diff --check` pass. Committed. |
| T1 | Close Blocker 2 | READY | — | ADR-0006 §3, §4, §7–§9, §14, F9, F10; ADR-0007 §8, S9 | rulings on R1f, R1g, R8b | each item ruled, and the Layer C/D precedence below has no open step |
| T2 | Blocker 8: PIN and `basis` semantics | BLOCKED (T1) | T1 | ADR-0006 §7–§9 | `conflict` vs `not_checkable`; `basis` precedence; missing `pincode_role` case; multiple PIN spans; multiple anchors; multi-level `place_unspecified` in D; confirm "valid PIN" | every case has exactly one outcome |
| T3 | Blocker 9: Layer D reliability method | BLOCKED (T2) | T2 | ADR-0006 §1, §14, §15 | derivation inputs; independent C set for `ambiguous`; meaning of `merge` | method computable from stored documents |
| T4 | Blocker 5: split-key inputs | READY | — | ADR-0006 §17 steps 1–2; ADR-0007 §5 | alias table and its evidence; one state column; district-column rules | two engineers derive the same step-1/2 result |
| T5 | Blocker 4: freeze point, salt, bucket mapping | READY | — (edit with T4) | ADR-0006 §17, F5 | freeze at first human exposure; salt provenance | mapping fully specified; freeze point testable |
| T6 | Blocker 6: `raw_text` eligibility and decoding | READY | — | ADR-0006 §2, §11, L6 | whether documented partial address lines qualify | eligibility decidable from documentation alone |
| T7 | Blocker 10: screening before the split | READY | — | ADR-0006 §12, §14; ADR-0007 §5 | option (a), (b) or (c); dev-only guideline examples | no unrecorded pre-split exposure |
| T8 | Blocker 3: withdrawal, denylist, errata | BLOCKED (T6) | T6, Blocker 1 | ADR-0006 §12, §13, §18 | denylist (a), (b) or (c); cascade to duplicate class; errata location | a rebuild can't silently re-admit a withdrawn record, or the limitation is documented |
| T9 | Blocker 7: release-manifest fields | BLOCKED (T1–T8) | T1–T8 | ADR-0006 §18 | `benchmark_version` major/minor rules | every version input is listed |
| T10 | Blocker 11: acceptance condition and ordering | BLOCKED (T9) for ordering. The acceptance condition can be ruled any time. | T9 | ADR-0006 status line, Consequences; ADR-0007 Consequences | what counts as acceptance | both ADRs give one consistent order |
| T11 | Coordinated revision: ADR-0006 rev 6, ADR-0007 rev 4 | BLOCKED (T1–T10) | T1–T10 | as above | approval of the drafted diff | full diff reviewed; cross-references checked |
| T12 | Follow-up implementation (`docs/schema.md`, procedures, validator) | BLOCKED (acceptance) | ADR acceptance | per ADR-0006 Consequences | — | per ADR |

Other open records outside this graph: ADR-0003 (NAPIX permission pending), ADR-0008
(Proposed), and the source blockers in `focus-state-source-evaluation.md`.

## Ruling ledger (maintainer, 2026-10-27 and 2026-10-28; not yet in the ADRs)

**Blocker 1: decided.**
- Merge only records with identical `name_key(raw_text)`.
- The class key is the lexicographically smallest member key.
- If any member is from a held-out publisher, the whole class goes to `test_source_holdout`.
- No district-level transitive grouping.
- Drop "union-find" from ADR-0006 §17 step 4 and ADR-0007 §3 and §6.

**Blocker 2: decided so far.**
- **Evidence standard (C).** LGD-side evidence, with URL and retrieval date, for all
  four levels, national or per state as the evidence supports.
  - State-government material only corroborates (S9).
  - Name patterns, counts and annotator knowledge are not evidence.
- **Layer A (4).** Layer A records the role as written. Verification gates only
  Layer C and Layer D.
  - The guidelines and cue table own the word-to-label mapping.
  - The F10 exceptions (`Block`, `Sub-division` → `place_unspecified`) stay (R6).
- **Unverified designators (1, R3).** An unverified designator removes its claimed
  level, and never falls back to the no-designator route.
  - The inversion with bare names is documented as a known limitation.
- **Gate (R1a, R1b, R1c).** Runs after the hierarchy stage and before the PIN stage,
  on generated sets only.
  - If any candidate is outside the verified scope, the role becomes
    `not_in_gazetteer` / `level_mapping_unverified`.
  - Its lists are kept for audit, `final_set` is `[]`, and it anchors nothing.
  - A new stage flag, `level_mapping_unverified`, records the outcome.
  - A PIN never establishes verification scope.
- **Reconciliation additions (R1d).** An addition outside the scope is recorded, and
  the role becomes `level_mapping_unverified` with `final_set` `[]`. Additions can't
  bypass the gate.
- **Empty name stage (R1e).** `no_match_in_snapshot`, kept distinct from a gate failure.
- **`pending_level` (R2).** A rejected designator whose written role is an LGD label
  records that level as its `pending_level`.
- **F10 designators (R8).** `pending_level` only where evidence supports it.
  Otherwise Layer D stays `not_specified`, with no guessed level.
- **`not_checkable` (R4).** Causes are ordered: no valid PIN, then
  `deferred_coverage`, then any other reason.
  - The PIN stage filters only the village members of a mixed-level
    `place_unspecified` role.
- **Conflicting evidence (3, R5, R5b).** Compatible state LGD evidence narrows a
  national mapping.
  - Contradicting state LGD evidence leaves the mapping unverified for that state.
  - Contradicting national LGD evidence leaves it unverified nationally.
  - State-government material can't demote a national mapping.
- **PIN stage not run (R7).** `pincode_role` `not_applicable` also covers "the PIN
  stage did not run", stated as meaning no PIN was checked.
- **Agreement (R9).** Mechanically derived Layer C statuses are excluded from status
  kappa and counted separately.
  - Excluded: non-linkable defaults, designators unverified everywhere, failures at
    the generation gate.
  - Not excluded: R1d failures.
- **Timing (5).** Verification is complete, or frozen as unverified, before the
  guidelines freeze. A later change means a new `cue_table_version` and
  re-annotation.
- **Village records (V).** They cover `(Ct)`, `(Og)` and `(Part)` where evidence
  permits, with nothing assumed.
- **Out of scope here.** Bare-name state/district matching (P5).

**Blocker 2: open.**
- **R1f.** An anchor is applied at generation time. If the anchoring role's final
  outcome later stops supporting it (an R1d failure, an addition, a pruning), what
  happens to the roles it anchored?
  - Options: (a) new reason `anchor_invalidated` (recommended), (b) top-down
    reconciliation, (c) document as a limitation.
  - (c) leaves a false-link risk.
- **R1g.** For a gated role, are human additions and prunings recorded but without
  effect, in both gate cases? (Recommended.)
- **R8b.** What evidence can support an F10 `pending_level`? Recommended: any S9
  source kind, cited, and never sufficient for "verified".

**Proposed Layer C precedence**, one linkable role (to confirm with T1):
0. A non-linkable label gets the §4 default.
1. A designator unverified everywhere gets `level_mapping_unverified`, with lists
   `null` and no flag.
2. An empty name stage gives `no_match_in_snapshot`.
3. The hierarchy stage runs.
4. The generation gate runs.
5. The PIN stage runs.
6. Independent annotation, then reconciliation.
7. The reconciliation gate.
8. `final_set` = stage + additions − prunings, unless a gate failed, in which case
   it's `[]`. Its size then gives `linked`, `ambiguous` or `no_supported_match`.

Gated lists never feed Layer D.
