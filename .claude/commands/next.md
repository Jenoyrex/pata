---
description: Show graph state and recommend the next node (read-only)
---

Read-only. Do not modify any file.

1. Run `uv run python scripts/graph.py validate`, `uv run python scripts/graph.py next`,
   `uv run python scripts/graph.py critical`, and `git status --short`.
2. Report in under 15 lines:
   - what is in progress / awaiting me / blocked,
   - the ready agent nodes, and which ONE you recommend and why (critical path first,
     then unblocking the most dependents),
   - anything only I can do that is holding up the critical path.
