# Task card — <NODE-ID>: <title>

- **Branch:** `node/<ID>-<slug>`
- **Started:** YYYY-MM-DD · **Session(s):** 1
- **Deps confirmed done:** <list with status from `graph.py show`>
- **Gate:** none | maintainer · **Irreversible:** no | yes (maintainer "go" given on YYYY-MM-DD: "<quote>")

## Plan
1. …
2. …

## Acceptance → proof map
| # | Acceptance criterion (copied verbatim from graph) | How it will be proven | Result |
|---|---|---|---|
| 1 | … | test `tests/…::test_…` / command / evidence file | PENDING |

## Scope fence (will NOT do)
- …

## Stop-points (pause and ask the maintainer if…)
- …

## Discovered work (added as new nodes, not done here)
- …

## Proof (paste real output — no summaries)
```
$ uv run pytest -q
…
```

## Verifier verdict
<paste verifier subagent table>

## Outcome
- Graph status set to: done | review | blocked
- Commit(s): `<sha>` on `node/<ID>-<slug>` (not pushed)
