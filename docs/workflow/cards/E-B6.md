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
If a file has no header row, its first record would print as the "header" unless `--expected-column`
is given. With that flag, a missing column gives `header_mismatch` and nothing from the file is printed.
Without it, compare the header with the platform field list before showing the output to anyone.

## Hardening, 2026-11-09 (maintainer sprint instruction)
The tests the 2026-11-05 verifier found missing were added: no cell leak from ragged rows, NUL bytes,
unterminated or malformed quoting or invalid UTF-8, and output identical across processes.
Added non-CSV detection (`unsupported_format`: xlsx/zip, xls/OLE2, PDF, HTML; C10 has `.xls` files) and
`--expected-column`. Synthetic fixtures only. **Real-file validation has not occurred:**
`data/raw/data.gov.in/` is empty, and the LGD files are gazetteer sources, not address candidates.

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
were not added then: that batch was declined on 2026-11-05. Superseded by the 2026-11-09 hardening.

2026-11-09, run after the hardening: **Overall PASS** on the uncommitted working tree over `7f4eb68`.
The verifier's table, verbatim:

| # | Criterion (verbatim) | Verdict | Evidence (path:line / test id / command) |
|---|---|---|---|
| 1 | Refuses a file whose SHA-256 differs from the recorded value | PASS | E:\PATA\scripts\source_stats.py:70-72 raises before any parsing; CLI returns 2 at :140-142. Tests: `test_checksum_mismatch_refuses_before_reading`, `test_cli_exits_nonzero_on_checksum_mismatch`. Mutation (check disabled): both tests fail. |
| 2 | Report has the header row and aggregate statistics only; a test asserts no cell value appears | PASS | E:\PATA\scripts\source_stats.py:40-52 and :104-114 emit only the header, counts and spreads. Tests: `test_report_never_contains_a_cell_value`, `test_malformed_files_never_leak_a_cell` (5 cases), `test_non_csv_files_are_named_and_not_parsed`, `test_missing_expected_column_withholds_a_possible_record_header`. 9 leak mutations, all caught: first record, ragged row, column example, longest value, csv error text, NUL path, decode partial, header_mismatch, unsupported format. |
| 3 | Invalid UTF-8, NUL bytes and ragged rows are reported, never repaired | PASS | E:\PATA\scripts\source_stats.py:81-84 strict decode reports an offset; :85-86 NUL gives parse_error; :89 `strict=True`; :103 and :110 ragged rows are counted and excluded from column stats. Tests: `test_invalid_utf8_is_reported_without_replacement`, `test_nul_byte_is_a_structured_error`, `test_ragged_rows_are_counted_and_not_folded_into_columns`. 5 mutations, all caught: `errors="replace"`, NUL stripped, ragged rows folded (uncounted and still counted), `strict=False`. |
| 4 | Two runs give byte-identical output | PASS | E:\PATA\scripts\source_stats.py:117-118 (`sort_keys=True`, no time or run state). Test: `test_output_is_identical_across_processes` compares stdout bytes across PYTHONHASHSEED 1 and 2. Mutations (timestamp, per-process `hash()`): both caught by that test. `test_two_runs_are_byte_identical` is single-process and did not catch them. |

Checks: ruff ✓ · format ✓ · pytest 138 passed/0 failed (4 skipped, all in tests/workflow/test_hooks.py:305, ADRs already accepted) · graph ✓ · diff-check ✓

Overall: PASS (all rows PASS)

Limits it stated: synthetic fixtures only; one compound read-only command was refused by the permission
system and not retried, so it did not review the uncommitted `graph.toml` diff or list tracked files
under `data/`. A headerless file still prints its first record unless `--expected-column` is given.
A file whose first line is blank is refused with an inaccurate "file is empty" message.

2026-11-09, run before the commit: **Overall PASS** on the uncommitted working tree over `7f4eb68`.
The verifier's table, verbatim:

| # | Criterion (verbatim) | Verdict | Evidence (path:line / test id / command) |
|---|---|---|---|
| 1 | Refuses a file whose SHA-256 differs from the recorded value | PASS | E:\PATA\scripts\source_stats.py:70-72 raises before any parsing; CLI handling at :138-142. Tests: `test_checksum_mismatch_refuses_before_reading`, `test_cli_exits_nonzero_on_checksum_mismatch`. Mutation on a scratch copy (check disabled): both tests fail. Direct CLI run on a synthetic file with a wrong hash: rc 2, 0 bytes on stdout. |
| 2 | Report has the header row and aggregate statistics only; a test asserts no cell value appears | PASS | E:\PATA\scripts\source_stats.py:40-52 and :104-114 emit only the header, counts and spreads. Tests: `test_report_never_contains_a_cell_value`, `test_malformed_files_never_leak_a_cell` (5 cases), `test_non_csv_files_are_named_and_not_parsed` (5 cases), `test_missing_expected_column_withholds_a_possible_record_header`. 8 leak mutations, all caught: first record, ragged-row sample, longest column value, csv error text, NUL path, decode partial, header_mismatch, unsupported format. Residual risk, not a criterion failure: `--expected-column` is optional (:97-99), so a headerless file prints its first record as the "header" when the flag is omitted. The card documents this at E:\PATA\docs\workflow\cards\E-B6.md:31-33. It matters under the ADR-0007 section 5 evidence limit once real files are used. |
| 3 | Invalid UTF-8, NUL bytes and ragged rows are reported, never repaired | PASS | E:\PATA\scripts\source_stats.py:81-84 strict decode reports an offset; :85-86 NUL gives parse_error; :89 `strict=True`; :103 and :110 ragged rows are counted and excluded from column stats. Tests: `test_invalid_utf8_is_reported_without_replacement`, `test_nul_byte_is_a_structured_error`, `test_ragged_rows_are_counted_and_not_folded_into_columns`, `test_malformed_files_never_leak_a_cell`. 7 mutations, all caught: `errors="replace"`, NUL check off, NUL stripped, `strict=False`, ragged folded and uncounted, ragged folded but still counted, ragged count forced to 0. Minor, from code reading only: a blank first line is refused at :93-94 with an inaccurate "file is empty" message. It is refused, not repaired. |
| 4 | Two runs give byte-identical output | PASS | E:\PATA\scripts\source_stats.py:117-118 (`sort_keys=True`, no time or run state). `test_output_is_identical_across_processes` compares stdout bytes across PYTHONHASHSEED 1 and 2; timestamp and per-process `hash()` mutations are both caught by it. `test_two_runs_are_byte_identical`, the test the card's proof map names, is single-process and misses the `hash()` mutation, so it is not sufficient evidence alone. Direct CLI: two separate runs gave identical stdout. |

Checks: ruff ✓ · format ✓ · pytest 142 passed/0 failed (4 skipped, tests/workflow/test_hooks.py:305, ADRs already accepted) · graph ✓ · diff-check ✓ (rc 0; only a CRLF warning on docs/workflow/graph.mmd; run on the working tree)

Overall: PASS (all rows PASS)

Limits it stated: synthetic fixtures only, so no real-file validation has occurred and B6 stays open. Implementation
verified, not released. Other nodes' uncommitted edits, including `graph.toml`, are outside this node's outputs.

## Outcome
- Graph status set to: done. B6 itself stays open until a real file exists.
- Commit(s): none (maintainer safeguard)
