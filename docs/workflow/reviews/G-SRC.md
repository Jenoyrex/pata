# Gate review packet — G-SRC: Maintainer accept/reject decision per source

Prepared by Claude on 2026-11-04. **Review only: nothing was modified, committed, merged, pushed
or accepted while preparing this packet.** The graph does not yet allow G-SRC to close: E-FIELD is
unfinished (section 3).

## 1. What you are being asked to decide

Whether any candidate source can move forward. **On today's evidence I recommend accepting
nothing yet.** No candidate has a clear licence, and ADR-0007 §5 (Proposed) says an unclear licence
means rejection. Three decisions of yours would change that, in section 4.

Evidence: `docs/research/source-inventory.md`, "Candidate register, field and licence evidence".

## 2. Position per source

The recommendations are mine. The decisions are yours.

| Row | What blocks it | Recommendation |
|---|---|---|
| **C2** All India Health Centres | B14 licence reading; no header row yet; 2016 data | **Lead candidate.** A single address field, no person or contact fields in the schema, a file on data.gov.in's own store |
| **C1a** National Hospital Directory | B14; `Nodal_Person_*` and other contact columns must never be ingested; `Address_Original_First_Line` undetermined | **Second candidate.** Data currency is unknown (G6), it needs more privacy handling, and its address field may be partial |
| C3 CGHS | B14; no state column, so records get no step-1 state (O4) | Defer: contributes nothing unless O4 retains unknown-state records |
| C1b | B15: host unreachable again on 2026-11-04; the file cannot be retrieved | Defer |
| C10 Blood Bank Directory | B14 for its `.xls`, B15 for its `.csv`; the `.xls` is named September 2015; nodal-officer columns must never be ingested | Defer: no gain over C1a |
| C4 Telangana | B3, B16; components only, so no records if ADR-0006 L6 is accepted | Defer. Send the drafted clarification if Telangana matters |
| C8, C9 Karnataka, Tamil Nadu | B14 and B17; small files; schemas mostly unknown; Tamil Nadu documentation route exhausted | Defer. They are the route to state-specific publishers, which affects holdout feasibility |
| C5, C6 | No reuse licence found; B4 | Reject or defer under B4. C5 has PDF, residential-area and electoral-roll risks too |
| C11, C12 | No licence text; interactive search only, with no bulk file | Reject for v0 unless a licence is found |
| C7 | Out of v0 scope (B18) | No action |

**A risk in this order:** C1a and C2 share one ministry, so `test_source_holdout` may have no
independent publisher to hold out (G4, ADR-0006 P6). Starting there is the shortest path to real
files, not a complete corpus.

## 3. Why E-FIELD is open

Its first criterion needs publisher documentation for each raw-text field. None was found for any
candidate. I did not reword the criterion. Decision 3 below resolves this.

## 4. Decisions needed, in the order that unlocks most

1. **B14: how to read data.gov.in's Copyright Policy against its GODL-India footer.** The footer
   names GODL-India and reserves rights "except published datasets/resources and metadata". The
   Copyright Policy asks for permission by mail. Options: read the footer's dataset exception as
   governing; or write to data.gov.in first (draft below) and treat C1a and C2 as unclear until a
   reply. The second is more defensible for a benchmark, and slower.
2. **Retrieval.** Download C2, and C1a if wanted, through the form, which needs your name, e-mail
   and a CAPTCHA, so I cannot do it. Save under `data/raw/data.gov.in/` with the portal's file name
   and do not re-save. Then:
   ```bash
   sha256sum data/raw/data.gov.in/geocode_health_centre.csv
   ```
   and, with that checksum:
   ```bash
   uv run python scripts/source_stats.py data/raw/data.gov.in/geocode_health_centre.csv --sha256 PASTE_CHECKSUM --missing-token NA --expected-column "Facility Address"
   ```
   This prints the header row and aggregate statistics only (ADR-0007 §5). If the named column from
   the platform field list is absent, it reports `header_mismatch` and prints nothing from the file,
   because a file with no header row would otherwise print its first record as the header.
3. **What counts as field evidence.** Options: treat platform field lists plus scripted statistics
   as enough, and amend E-FIELD's criterion yourself; or ask the publishers first. The "Procedural
   position" question in `focus-state-source-evaluation.md` is the same one.

Also open: G4 (publisher unit, "government body") and B4 (reuse on request).

**C9c located, 2026-11-08.** The file URL for `office_infrastructure_details.csv` (299 B) is now in
the candidate register (R126), so no ruling is needed to unblock E-INV. Whether C9c stays a candidate
is still yours to decide. What the file holds is UNKNOWN, and it was not downloaded.

### Draft to data.gov.in: not sent

The contact address is UNKNOWN here; take it from the portal. The project description is the
maintainer's to confirm. No permission is assumed.

> **Subject:** Licence of published datasets: Copyright Policy and GODL-India
>
> Dear OGD Platform team,
>
> I maintain Pata, an open-source research project on Indian addresses. Before using a dataset I
> check its licence. I am asking about these resources:
>
> - "All India Health Centres Directory as on 7th October, 2016"
> - "National Hospital Directory with Geo Code and additional parameters (updated till last month)"
>
> The site footer says content is licensed under the Government Open Data License - India, and
> reserves rights "except published datasets/resources and metadata". The Copyright Policy says
> material "may be reproduced free of charge after taking proper permission by sending a mail to
> us".
>
> Could you please confirm:
>
> 1. Whether these two datasets are licensed under GODL-India.
> 2. Whether the Copyright Policy's permission requirement applies to published datasets.
> 3. If permission is needed, whether this message may serve as the request, for download, research
>    use and inclusion in an open-source research benchmark, with attribution.
> 4. Whether any publisher documentation defines the address fields in these files.
>
> Thank you for your time.
>
> Regards,
> [Name]
> [Project link and contact details]

## 5. Checks

Recorded in `PROGRESS.md`, session entry of 2026-11-04.

## 6. Facts vs. assumptions

- **Verified from repository or publisher pages:** everything cited in the inventory's eleventh
  pass and the passes it refers to.
- **Assumptions and recommendations:** the order in section 2, "lead candidate", and the judgement
  that writing first is more defensible. No record or data file was read for any of this.

## 7. Maintainer checklist

- [ ] I read the inventory's eleventh pass, not only this packet
- [ ] I decided B14, retrieval and field evidence, or recorded them as open
- [ ] I wrote a dated ACCEPT / REJECT / DEFER with a reason for each candidate myself
- [ ] I ran `uv run python scripts/graph.py approve G-SRC --by <me> --ref "<doc § + sha>"`
