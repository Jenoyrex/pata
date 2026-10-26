# Pata documentation

| Path | Contents |
|---|---|
| [`decisions/`](decisions/) | Architecture/research decision records (ADRs). One file per decision, numbered, never rewritten. Superseded ADRs are marked as such. |
| [`gazetteer.md`](gazetteer.md) | Reference gazetteer: sources, build steps, table schema, quality checks, limitations. |
| [`research/`](research/) | Research working notes, such as the source inventory. Evidence for future decisions, not decision records. |

Planned with milestone M0 (added when written, not before):

- `schema.md`: PataBench annotation schema (versioned). It is also the
  normative owner of every machine-readable format listed in ADR-0007 E3:
  address-source manifests, focus-state lists, split configurations,
  split-file fields and release manifests, including the held-out publisher
  list. ADR-0006 and ADR-0007 keep policy and required information, and each
  release ADR records that release's values; all reference the schema.
- `datasheet.md`: dataset documentation in the style of *Datasheets for Datasets*.

## Writing an ADR

Copy the structure of [ADR-0001](decisions/0001-data-privacy-licensing-scope.md):
Status, Date, Context, Decision, Consequences. Number sequentially.
