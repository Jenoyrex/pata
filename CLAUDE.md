# Pata: working rules for Claude

Pata is an open-source benchmark (PataBench) and toolkit for Indian address
intelligence. Research credibility, licensing, privacy, reproducibility, leakage
prevention and honest uncertainty come before features. See `README.md` and
`docs/decisions/` (ADRs).

## Start of every session

1. Read `PROGRESS.md` and `docs/research/dependency-graph.md`.
2. Check `git status --short --branch` and `git rev-parse HEAD` against
   `PROGRESS.md`. If they differ materially, stop and report.
3. Before relying on an ADR, read its current text. Summaries in `PROGRESS.md` or the
   graph aren't a substitute for the files.

## Commands (verified; same as `.github/workflows/ci.yml`)

```bash
uv sync --locked            # dependency/lock consistency
uv run ruff check .         # lint
uv run ruff format --check . # formatting
uv run pytest               # tests (~80 s)
git diff --check            # whitespace, for every change
```

## Loop for each task

1. **Gather:** read the code, ADRs and notes the task touches. Confirm the git state.
2. **Plan:** outcome, prerequisites (from the graph), affected files, done criteria.
   Separate facts, inferences, recommendations, and decisions only the maintainer can make.
3. **Act:** make the smallest authorized change. One ADR revision or implementation
   task per batch.
4. **Verify:** run the commands above that apply. For docs, also check the full
   diff, the cross-references, and the decision status.
5. **Diagnose:** read the full error, form a hypothesis, fix only the cause. Stop
   after three failed attempts at the same problem and report the options.
6. **Update:** record actual commands and results in `PROGRESS.md` and the graph.
   Never record a check as passed unless it ran and passed.
7. **Checkpoint:** commit only verified, in-scope changes that encode no undecided item.

Use a single agent by default. Never let parallel agents edit the same ADR, schema or
decision record.

## Guardrails

- Never commit data files, raw sources, or personal or address records (`data/*` and
  `/report data/` are ignored; only `data/manifests/` is tracked). Never quote record
  text in docs or logs (ADR-0007 §5).
- Never invent data, scores, permissions, licences, source evidence or results.
  Synthetic data is never presented as real.
- Never resolve an open maintainer decision because an implementation looks
  plausible. Record it as open.
- Never accept or reject an ADR or source without the maintainer.
- Never weaken or skip tests to get a green run.
- ADRs are never rewritten after acceptance. While an ADR is Proposed, revise it
  with a revision note in its header (see existing ADRs).

## Git

- Commit only when asked or when authorized for a checkpoint. Never push
  automatically.
- No AI co-author trailers or AI branding in commits.
- Before committing: review the diff, then run the checks.
- Before pushing: show the commit message and `git diff --stat` for the range being pushed.
- Use conventional messages (`docs: ...`, `feat: ...`), matching `git log`.
