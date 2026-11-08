# Pata workflow kit — LOOP + graph engineering for Claude Code

Drop-in workflow architecture for `Jenoyrex/pata` (`E:\PATA`). It gives Claude Code a
machine-checked task graph, a fixed execution protocol, independent verification, and
hooks that make the project rules physically enforceable.

```
workflow/graph.toml            ← the dependency graph (single source of truth)
scripts/graph.py               ← validate · next · show · status · critical · mermaid · progress · approve
docs/workflow/LOOP.md          ← the protocol for working one node
docs/workflow/ARCHITECTURE.md  ← how the pieces fit + generated graph diagram
docs/workflow/templates/       ← task card · evidence record · gate packet · session log
.claude/commands/              ← /next /loop /verify /checkpoint /gate-review /add-node
.claude/agents/                ← verifier · adr-reviewer · evidence-scout
.claude/hooks/pata_guard.py    ← guard hooks (fail closed)
.claude/settings.json          ← hook wiring + deny rules
tests/workflow/                ← 86 tests for the graph engine and the hooks
CLAUDE.workflow.md             ← block to merge into your CLAUDE.md
gitignore.additions            ← lines to append to .gitignore
```

Stdlib only (Python ≥ 3.11, you're on 3.12). No new dependencies.

---

## 1. Install (≈10 minutes, you do this — not Claude)

In PowerShell or Git Bash at `E:\PATA`, on a fresh branch:

```bash
git switch main
git switch -c workflow-kit
# unzip the kit into E:\PATA, then:
```

1. **Merge, don't overwrite.**
   - `.claude/settings.json`: if you already have one, merge the `hooks` and `permissions.deny` keys.
   - `CLAUDE.md`: paste `CLAUDE.workflow.md` at the top of your existing file, then delete `CLAUDE.workflow.md`.
   - `.gitignore`: append `gitignore.additions`, then delete it.
2. **Hooks need `uv` on PATH** (they run `uv run --no-project python …`). On Windows, Claude Code
   runs hooks through Git Bash if installed — install Git for Windows if you haven't.
3. Check it works:
   ```bash
   uv run python scripts/graph.py validate
   uv run pytest -q            # your 26 tests + 86 workflow tests (4 skip: accepted ADRs)
   uv run python scripts/graph.py next
   ```
4. Restart Claude Code in `E:\PATA`. The first message you see from the session-start hook
   should contain "PATA SESSION START" and the READY list. Run `/hooks` to confirm they're loaded.

## 2. First Claude Code session: reconcile the graph (node W0)

The graph was built from the 28 Oct dossier, so it's **reported state**, not verified state.
Give Claude this:

```
/loop W0

Extra instructions for W0:
- Read docs/research/dependency-graph.md, PROGRESS.md and CLAUDE.md.
- Reconcile workflow/graph.toml against them: every legacy task T0–T12 must map to a node
  (split LEGACY into T0..T10 nodes if that's clearer); fill T12's real scope and acceptance;
  flag anything in either file that the other lacks. Do not invent tasks or statuses.
- Show me the reconciliation table before editing graph.toml.
- Then run the W0 verify commands, the verifier, and set W0 to review.
```

Then approve it yourself (see §4).

## 3. Daily driving

| You want to… | Type |
|---|---|
| Know what to do next | `/next` |
| Work the next node end-to-end | `/loop` (or `/loop E-LGD`) |
| Prepare a decision for yourself | `/gate-review G-ADR67` |
| Re-check a node independently | `/verify I-INGEST` |
| Close out a node | `/checkpoint I-INGEST done` |
| Record new work found mid-task | `/add-node "vendor Scripts.txt test fixture"` |
| Let Claude run an irreversible node | say `go X-FREEZE` in chat, then `/loop X-FREEZE` |

**Recommended right now** (critical path is source evidence, not the ADRs):

1. `/gate-review G-ADR67` → read the packet → accept/request changes yourself.
2. In parallel: `/loop E-INV`, then `/loop E-LGD`.
3. Assign the screener (H-SCREENER) early — it's a people problem with lead time.

Run one LOOP per Claude Code session when you can (`/clear` between nodes). Context stays
small, and the session-start hook reloads real state every time.

## 4. Maintainer-only actions

```bash
# approve a gate (interactive: you must type "APPROVE <ID>")
uv run python scripts/graph.py approve G-ADR67 --by Jenoy --ref "ADR-0006 §Status; ADR-0007 §Status; merge <sha>"
# then set status = "done" for that node (or ask Claude to — it can change status, not write approvals)

git merge --no-ff node/E-INV-inventory     # merges are yours
git push                                    # pushes are yours
uv run python scripts/graph.py mermaid --out docs/workflow/graph.mmd   # refresh the diagram
```

## 5. What the hooks block (and why)

| Blocked | Why |
|---|---|
| `git push`, `merge`, `rebase`, `reset --hard`, `clean -f`, `branch -D`, `--no-verify`, `gh pr merge/repo edit/release` | rule: no remote/merge/history changes without you |
| `git add` of `data/raw`, `private`, `staging`, denylist/exposure; `git add -f` | raw/private data never enters Git |
| Writing `Status: Accepted` in `docs/decisions/*.md` | ADR acceptance is your act |
| Writing `[[approval]]` into graph.toml, or running `graph.py approve` | approvals can't be fabricated |
| Editing `.claude/hooks/`, `.claude/settings.json`, `data/raw/`, `private/`, `staging/` | guards can't be disabled by the agent; data only via scripts |
| `git commit` while graph.toml is invalid | state and code stay consistent |
| Reading `private/`, `staging/test/`, `staging/holdout/` (settings deny) | avoid test contamination |

Hooks fail closed: if the guard itself errors, the action is blocked. Edit the guard yourself
if a rule is wrong — then add a test in `tests/workflow/test_hooks.py`.

## 6. Limits — be clear-eyed

- Hooks are guard rails, not a security boundary. They catch the obvious paths (and the
  tests prove which); a determined workaround via an unusual command could slip past.
  The `CLAUDE.md` rule "if a hook blocks you, report it" plus your review is the backstop.
- The graph's statuses are seeded from the dossier and must be reconciled (W0) before you
  rely on them.
- Node sizes past P3 are coarse on purpose; split them with `/add-node` when you reach them.
