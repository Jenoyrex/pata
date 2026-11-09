# Task card — E-B6: Scripted aggregate inspection of candidate source files (B6)

- **Branch:** `workflow-kit` (maintainer safeguard 2026-11-04: no branch switch, no commit)
- **Started:** 2026-11-04 · **Session(s):** 1
- **Deps confirmed done:** none. It was first declared on E-INV, and the script was written before
  E-INV closed, which the guard flagged. The tool does not use the inventory, so the dep was removed
  on 2026-11-05 as wrong rather than to get around the guard. Running it on real files still needs a
  maintainer download.
- **Gate:** none · **Irreversible:** no

## Plan
1. Tests first, on synthetic CSV fixtures.
2. A standard-library script printing the header row and aggregate statistics, never a cell value.
3. Verify a file against a recorded SHA-256 before reading it.

## Acceptance → proof map
| # | Acceptance criterion (copied verbatim from graph) | How it will be proven | Result |
|---|---|---|---|
| 1 | Refuses a file whose SHA-256 differs from the recorded value | `test_checksum_mismatch_refuses_before_reading`, `test_cli_exits_nonzero_on_checksum_mismatch` | see verifier |
| 2 | Report has the header row and aggregate statistics only; a test asserts no cell value appears | `test_report_never_contains_a_cell_value` | see verifier |
| 3 | Invalid UTF-8, NUL bytes and ragged rows are reported, never repaired | `test_invalid_utf8_is_reported_without_replacement`, `test_nul_byte_is_a_structured_error`, `test_ragged_rows_are_counted_and_not_folded_into_columns` | see verifier |
| 4 | Two runs give byte-identical output | `test_two_runs_are_byte_identical` | see verifier |

## Scope fence (will NOT do)
- Run it on a real candidate: none is held. Retrieve a file. Treat this as ingestion (I-INGEST).

## Stop-points
- Real output needs a file the maintainer downloads through the form.

## Known limit
If a file has no header row, its first record would print as the "header". Compare the header with
the platform field list before showing the output to anyone.

## Discovered work
- None.

## Proof
```
$ uv run pytest tests/test_source_stats.py -q   (before the script existed)
ERROR tests/test_source_stats.py - FileNotFoundError ... scripts\source_stats.py
$ uv run pytest tests/test_source_stats.py -q
11 passed in 0.22s
```

## Verifier verdict
2026-11-05, first run: criteria 1–3 **PASS**; criterion 4 PASS on command evidence (two processes,
`PYTHONHASHSEED` 1 and 2, identical stdout on 8 synthetic cases). Overall PASS. Dep removal judged
sound. `uv run pytest tests/test_source_stats.py -q`: 11 passed.

Open, non-blocking: mutations on a scratch copy that the tests missed, though the script has none of
these faults: a ragged-row cell leak, a NUL-path leak, a partial-cell leak, `strict=False` quoting,
and per-process variation (`test_two_runs_are_byte_identical` runs in one process). Tests for these
are not added: that batch was declined on 2026-11-05 and awaits a maintainer word.

## Outcome
- Graph status set to: done. B6 itself stays open until a real file exists.
- Commit(s): none (maintainer safeguard)
