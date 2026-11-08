---
description: Graph engineering — add a newly discovered task as a node with deps and acceptance
argument-hint: "short description of the discovered work"
---

Discovered work: `$ARGUMENTS`

1. Read `workflow/graph.toml` and `docs/workflow/LOOP.md` §Graph engineering rules.
2. Propose ONE node (or a small chain) to me before writing:
   - `id` (prefix by kind: E- evidence, D- spec, I- impl, G- gate, H- human, X- irreversible),
   - title, phase, kind, owner, gate, `irreversible` if it cannot be undone,
   - `deps` (what must be done first) and which existing nodes should now depend on it,
   - 2–5 acceptance criteria someone else could check,
   - `verify` commands where possible.
3. If adding it changes deps of a node that is already `in_progress`/`review`/`done`,
   say so explicitly and WAIT for my approval.
4. Otherwise append it, run `uv run python scripts/graph.py validate`, and show
   `graph.py show <new-id>` and `graph.py critical`.
