---
description: Prepare a review packet for a maintainer-gated node (review only, changes nothing)
argument-hint: "GATE-ID [base..branch]"
---

Review only. Do NOT modify tracked files, commit, merge, push, accept ADRs, write approvals
or start dependent tasks. The only file you may create is the packet itself.

Gate: `$ARGUMENTS`

1. `uv run python scripts/graph.py show <GATE-ID>`; read its acceptance criteria.
2. Delegate the evidence gathering to the `adr-reviewer` subagent, giving it the gate ID,
   the diff range (default for G-ADR67: `main..adr-0006-rev6`) and the decision IDs listed in
   the node (for G-ADR67: ADR-0006 F1, F3, F5, F9, F10, F12, F14, F15; ADR-0007 S6, S9).
3. Write the result to `docs/workflow/reviews/<GATE-ID>.md` using
   `docs/workflow/templates/gate-review-packet.md`. Old/new text verbatim from the diff.
4. Run and paste: ruff check, ruff format --check, pytest, `git diff --check`, graph validate.
5. Separate "verified from repository" from "assumption / recommendation".
6. End with the maintainer checklist and stop. Wait for my explicit decision.
