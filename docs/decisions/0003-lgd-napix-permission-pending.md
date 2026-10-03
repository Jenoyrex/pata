# ADR-0003: LGD NAPIX APIs as an acquisition route (permission pending)

- **Status:** Proposed. **PERMISSION PENDING**
- **Date:** 2026-10-03
- **Deciders:** Project maintainer

## Context

ADR-0002 selects four Ministry of Panchayati Raj (LGD) resources on data.gov.in
as v0 gazetteer sources. They currently can't be acquired from the development
environment:

- data.gov.in file URLs return 403/301 to scripted requests.
- The data.gov.in Download form's CAPTCHA does not render.
- `api.data.gov.in` is unreachable (DNS resolves, TCP 443 connect fails).

The LGD publishes the same entities through official APIs on NIC's API exchange
(NAPIX), documented at https://dev.napix.gov.in/nic/lgd/ (gateway
`https://delhigw.napix.gov.in/nic/lgd`). However, the NAPIX Subscriber Terms
(https://napix.gov.in/en/subscriber-terms/) require subscribers to confirm they are
"an authorized person to act on behalf of an Undertaking / Government / Ministry /
Department". Accounts are approved by the API owner (LGD). Use of the data is
"as per the consent and prior approval of the API / Data Owner's". The terms say
nothing about storage, automated retrieval, redistribution or attribution.

Pata is an open-source research and data-science project developed by an
individual researcher/student. It does not represent a government body or
undertaking, so it cannot make the clause 3 declaration. Permission has to come
from LGD directly.

## Request

- **Date of request:** 2026-10-03
- **Requested source:** LGD APIs on NAPIX
- **Contact:** lgdirectory@gov.in (listed as the contact in the LGD API specifications)
- **Purpose:** the open-source research project Pata (India-wide reference
  gazetteer, benchmark and toolkit for address-intelligence research)
- **Datasets:**

  | Dataset | Endpoint (POST) |
  |---|---|
  | States | `/states/v1/status/active` |
  | Districts | `/districts/v1/status/active` |
  | Sub-districts | `/subdistricts/v1/status/active` |
  | Village–PIN mapping | `/ruralUrbanBlockVillagePincodeMapping/{page}` |

- **Permission and clarifications requested:**
  1. API access eligibility for an individual open-source researcher/student who
     does not represent a government body
  2. whether automated retrieval through the API is permitted
  3. whether local storage of API responses as dated snapshots is permitted
  4. whether derived/normalized datasets may be distributed as part of an
     open-source research project
  5. the required attribution/acknowledgement wording
  6. rate limits and other restrictions
  7. whether written approval can be provided for the project
  8. for the Village–PIN API, the page size, starting page number and how the end
     of the data is indicated (not specified in the public documentation)

## Decision

NAPIX is **not** an approved acquisition source. Until LGD/NIC responds:

- No NAPIX data has been downloaded.
- No NAPIX credentials (account, application, Client ID/Secret) have been created.
- No NAPIX API calls have been made with credentials.
- The four LGD manifests (`lgd_states`, `lgd_districts`, `lgd_subdistricts`,
  `lgd_villages_pincode`) must **not** be switched to NAPIX.
- ADR-0002 must **not** be amended.

The project waits for LGD/NIC's response before treating NAPIX as an approved
source. If permission is granted, a follow-up ADR will record the conditions
and amend the sources. That ADR will reference the written approval, and its
attribution must use LGD's wording.

## Consequences

- The LGD part of the gazetteer stays blocked until data.gov.in becomes reachable,
  LGD grants permission, or another first-party route is accepted by a new ADR.
- If the request is refused or unanswered, the remaining first-party route is a
  manual download from the LGD portal (lgdirectory.gov.in). Those downloads are
  XLS/ODT/PDF only, behind a CAPTCHA, and are covered by the LGD Copyright Policy
  rather than GODL. Using them would also need its own ADR.
- The India Post PIN directory is not covered by this request. data.gov.in remains
  its only first-party source.
