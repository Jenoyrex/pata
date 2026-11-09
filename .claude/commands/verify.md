---
description: Independent Prove step — verifier subagent checks a node's acceptance criteria
argument-hint: "NODE-ID"
---

Invoke the `verifier` subagent for node `$ARGUMENTS`. Give it only: the node ID, the path
`docs/workflow/cards/$ARGUMENTS.md`, and the branch name. Do not give it your own conclusions.

Relay its table verbatim into the card's "Verifier verdict" section. If any row is FAIL or
UNPROVEN, list the fixes needed and do not change the node status to done/review.
