# GMD-26 — Fan CRM Operator

```
Prerequisite: GMD-21. Fed by GMD-24 (a purchase creates/updates a fan record).
```

## Repo truth

`/admin/fans` route (`server.py:415-418`); `upsert_fan`
(`ticketing_service.py:24-70`, corrected pointer — the logic lives in
this service file, not inline at `server.py:611`). This is the
operator role for Good Mood's real fan database — not a full
marketing-CRM product, but richer than "raw table only": it computes
real derived fields (`total_events`, `cities`, `segments` —
`primo`/`recurring`/`vip`) on every upsert. `external_id` is derived
from the email's local-part and can collide across different domains
(e.g. `x@a.com`/`x@b.com`) — a real, citable data-quality edge case.

## Prerequisites

GMD-21.

## Objectives

1. Read and interpret the real fan record (what it captures, what it
   does not — no purchase-history analytics beyond what the raw table
   holds).
2. Explain when a fan record is created vs updated (purchase-triggered
   upsert, not manual entry as the primary path).
3. Correctly answer a "how many fans do we have from city X" question
   using only the real fields available, never inventing segments the
   data doesn't support.

## Modules

| # | Module | Deliverable |
|---|---|---|
| M1 | Fan record field literacy | Field table + upsert-trigger note |
| M2 | Fan-record query practice | Written answers to 3 realistic operator questions, each traced to the real field(s) that answer it (or explicitly flagged as unanswerable with current fields) |
| M3 | Data-honesty discipline | Short case: a stakeholder asks for a segment the schema can't produce — the correct answer is "not currently trackable," never a fabricated number |

## Assessment

Per `../CERTIFICATION_MODEL.md`. Graded specifically on M3 — this
formation's core competency is refusing to fabricate data the real
schema doesn't hold, directly mirroring this Master Package's own
`UNPROVEN_FEATURE`/`FAKE_PROOF` discipline applied at the operator
level.

## Evidence / certification / mission eligibility

Same general pattern as GMD-22.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD26` — full canonical package built.
`FULLY_COMPLETE` still requires a real candidate pass.
