# Gate review packet — <GATE-ID>: <title>

Prepared by Claude on YYYY-MM-DD. **Review only — nothing was modified, committed,
merged, pushed or accepted while preparing this packet.**

## 1. What you are being asked to decide
<one paragraph>

## 2. Scope of change
- Diff command: `git diff <base>..<branch> --stat` (output pasted below)
- Files touched: …

## 3. Decision-by-decision table
| ID | Old text (verbatim) | New text (verbatim) | Rationale | Edge cases | File § refs | Deviation from agreed edit map? |
|---|---|---|---|---|---|---|

## 4. Deferred items (claimed non-blocking)
| ID | What is deferred | Why it does not block this gate | Where it is recorded |
|---|---|---|---|

## 5. Checks (real output)
```
$ uv run ruff check .
$ uv run ruff format --check .
$ uv run pytest -q
$ git diff --check
$ uv run python scripts/graph.py validate
```

## 6. Facts vs. assumptions
- **Verified from repository:** …
- **Assumptions / recommendations:** …

## 7. Maintainer checklist
- [ ] I read the full diff, not only this packet
- [ ] Every changed decision above is acceptable as written
- [ ] Deferred items are genuinely non-blocking
- [ ] I wrote dated acceptance in each document myself
- [ ] I merged the branch myself
- [ ] I ran `uv run python scripts/graph.py approve <GATE-ID> --by <me> --ref "<doc § + merge sha>"`
