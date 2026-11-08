---
description: Record step — update graph status, PROGRESS.md and commit on the node branch
argument-hint: "NODE-ID done|review|blocked [blocker text]"
---

Arguments: `$ARGUMENTS`

1. Refuse `done` if the card has no all-PASS verifier verdict, or if the node has
   `gate = "maintainer"` (use `review`; the maintainer approves).
2. Edit `workflow/graph.toml`: set the status (and `blocker = "..."` for blocked).
   The post-edit hook validates; fix any error it reports.
3. `uv run python scripts/graph.py progress --write PROGRESS.md`, then append a session entry
   from `docs/workflow/templates/session-log.md`.
4. Run ruff check, ruff format --check, pytest, `git diff --check`.
5. `git add` only the files this node touched (never data/raw, private, staging) and commit
   with message `<type>(<NODE-ID>): <summary>`. Do not push or merge.
6. Print the session entry.
