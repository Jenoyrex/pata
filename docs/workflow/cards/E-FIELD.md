# Task card — E-FIELD: Field semantics evidence (incl. C1a Address_Original_First_Line)

- **Branch:** `workflow-kit` (maintainer safeguard 2026-11-04: no branch switch, no commit)
- **Started:** 2026-11-04 · **Session(s):** 1
- **Deps confirmed done:** E-INV (see graph)
- **Gate:** none · **Irreversible:** no

## Plan
1. Read every publisher-side descriptor for each candidate raw-text field.
2. Record what is documented; a column name counts for nothing.
3. State the C1a outcome.

## Acceptance → proof map
| # | Acceptance criterion (copied verbatim from graph) | How it will be proven | Result |
|---|---|---|---|
| 1 | Each candidate raw-text field backed by publisher documentation, not column names | `docs/research/source-inventory.md`, "Field semantics (E-FIELD)" | **Not met: no publisher definition found for any field** |
| 2 | C1a outcome stated: qualifies / does not qualify / undetermined, with evidence | same section | Undetermined, with evidence |

## Scope fence (will NOT do)
- Reword criterion 1 to pass it. Infer meaning from names. Read records.

## Stop-points
- Criterion 1 is the stop-point. Ask the publishers, or a maintainer ruling on what suffices.

## Discovered work
- E-B6 can add shape statistics once a file exists. Those are not publisher documentation.

## Proof
Hashes R111–R114 in the inventory. Checked per C1–C3 list: `id`, `name`, `type`, `desc`, and the
resource `note`. Each `desc` repeats the title; each `note` covers missing values and, for C1,
update timing.

## Verifier verdict
Pending.

## Outcome
- Graph status set to: todo. Evidence is drafted but the node cannot start until E-INV is done, and
  drafting early broke one-node-at-a-time (recorded in `PROGRESS.md`). Once started, criterion 1 will
  keep it blocked.
- Commit(s): none (maintainer safeguard)
