# LOOP — how every unit of Pata work is executed

LOOP is the execution protocol. The **graph** (`workflow/graph.toml`) decides *what* may be
worked on; LOOP decides *how* one node is worked on. One loop = one graph node.

```
        ┌───────────────────────────────────────────────────────────┐
        │                                                           │
        ▼                                                           │
   L  LOAD ──► O  OUTLINE ──► O  OPERATE ──► P  PROVE ──► ⟲ RECORD ─┘
   state       task card      small steps    independent   graph + PROGRESS
   pick node   stop-points    tests first    verifier      + commit + report
```

---

## L — Load (never skip)

1. `uv run python scripts/graph.py next` and `git status`, `git branch --show-current`.
2. Read the last session entry in `PROGRESS.md`.
3. Pick **exactly one** node:
   - the one the maintainer named, otherwise
   - an `in_progress` node you own, otherwise
   - the first *ready* node with `owner = "agent"`, preferring nodes on the
     critical path (`graph.py critical`).
4. `uv run python scripts/graph.py show <ID>` — read deps, acceptance, outputs, notes.
5. Stop and ask the maintainer if:
   - the node is `owner = maintainer | screener | annotator` (you may only *prepare* for it),
   - the node is `irreversible = true` (needs an explicit "go" in chat for this run),
   - any dep is not `done` (the graph says no; do not reason around it).

## O — Outline (write it down before touching code)

1. Create the task card: copy `docs/workflow/templates/task-card.md` to
   `docs/workflow/cards/<ID>.md` and fill it in.
2. Map **each acceptance criterion → how it will be proven** (test name, command, evidence file).
3. List explicitly what you will **not** do (scope fence).
4. Create branch `node/<ID>-<slug>` from `main` (or from the branch the maintainer named).
5. Set the node `status = "in_progress"` in `graph.toml` (post-edit hook re-validates).
6. **Pause for the maintainer** if the plan changes an accepted ADR's meaning, adds a
   source, touches split/salt/holdout config, or alters `docs/schema.md` vocabulary.
   Otherwise proceed.

## O — Operate (small, reversible steps)

- **impl** nodes: write the failing test first, then the code. Commit-sized steps.
- **evidence** nodes: every claim gets URL + retrieval date (+ SHA-256 if a file was
  downloaded) in the evidence file. Unknown stays `UNKNOWN`/`UNVERIFIED`.
  CAPTCHA/403 ⇒ log it and ask the maintainer to fetch manually. Never bypass.
- **spec / decision** nodes: draft in the target file with status `Proposed`.
- New work discovered? **Do not expand scope.** Add a node (`/add-node`) with deps and
  carry on with the current one.
- A dep turns out wrong? Stop, write it in the card, ask. Don't edit started nodes' deps silently.
- Never fabricate: source rows, licence terms, field meanings, approvals, results, test output.

## P — Prove (the work doesn't grade itself)

1. Run the node's `verify` commands, then the standard gate:
   ```
   uv run ruff check .
   uv run ruff format --check .
   uv run pytest -q
   uv run python scripts/graph.py validate --check-outputs
   git diff --check
   ```
2. Hand off to the **verifier** subagent (`/verify <ID>`). It has not seen your reasoning,
   re-runs the commands, and returns PASS / FAIL / UNPROVEN per acceptance criterion with
   evidence. Any FAIL or UNPROVEN ⇒ back to Operate.
3. Paste real command output into the task card's *Proof* section. Summaries are not proof.

## ⟲ Record (close the loop)

1. Status transition in `graph.toml`:
   - `gate = "none"` and verifier all-PASS → `done`
   - `gate = "maintainer"` → `review` (maintainer approves with `graph.py approve`, then `done`)
   - can't finish → `blocked` with a `blocker` sentence
2. `uv run python scripts/graph.py progress --write PROGRESS.md`
3. Append a session entry to `PROGRESS.md` (template: `docs/workflow/templates/session-log.md`).
4. Commit on the node branch (checks must pass; the commit hook re-validates the graph).
5. Report to the maintainer: node, result, proof summary, what is now ready,
   what needs their decision. **No push, no merge** — those are theirs.

---

## Status machine

```
todo ──► in_progress ──► done                      (gate = none, verifier PASS)
                    └──► review ──(approve)──► done (gate = maintainer)
           any ─────────► blocked ──► in_progress   (blocker resolved)
           any ─────────► dropped                   (never delete nodes)
```

## Graph engineering rules

- The graph is code: it is validated on every edit (hook), on every commit (hook) and in
  `tests/workflow`.
- Every node has acceptance criteria that can be checked by someone who didn't do the work.
- Prefer many small nodes over one vague node. A node should fit in 1–3 sessions.
- Gates are nodes, not comments. Anything needing a human decision is a `gate = "maintainer"`
  node that the dependent work lists in `deps`.
- Irreversible steps (split freeze, release) are flagged `irreversible = true`.
- Nodes are never deleted; use `status = "dropped"` with a note.
- Approvals are append-only and written only by the maintainer.

## Enforcement map (rule → mechanism)

| Rule | Enforced by |
|---|---|
| No push / merge / force / history rewrite | `pre-bash` hook + settings `deny` |
| No ADR "Accepted" written by Claude | `pre-edit` hook (status check on docs/decisions/) |
| No fabricated approvals | `pre-edit` hook on graph.toml + `approve` needs a real TTY |
| Raw/private/staging data never in Git | `pre-bash` (`git add`), `pre-edit`, `.gitignore` |
| Test/holdout data not read by Claude | settings `deny` Read rules |
| Can't start before deps done | `graph.py validate` (post-edit + commit hook + tests) |
| Gated node can't be `done` without approval | `graph.py validate` |
| Session starts with real state, not memory | `session-start` hook injects `graph.py next` + git state |
| Work doesn't grade itself | `verifier` subagent in Prove |
