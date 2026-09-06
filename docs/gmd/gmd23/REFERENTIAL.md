# GMD-23 — Event Operator

```
Prerequisite: GMD-21.
```

## Repo truth

`Event`/`EventIn` model (`server.py:99-114`); routes `GET /events`,
`POST/PUT/DELETE /admin/events/{eid}`, `POST /admin/events/{eid}/
ticket-types` (co-owned with GMD-24). Feeds GMD-25 (door scan needs an
event to scan into) and GMD-30 (reporting reads event data).

## Prerequisites

GMD-21.

## Objectives

1. Create and manage the full lifecycle of an `Event` record (create,
   update details, add ticket types, close/archive).
2. Correctly hand off a newly-created event to GMD-24 (ticket sales
   configuration) and GMD-25 (door scan readiness) without duplicating
   their work.
3. Recognize which fields an event needs before it can be safely sold
   or scanned against.

## Modules

| # | Module | Deliverable |
|---|---|---|
| M1 | `Event`/`EventIn` field literacy + the ticket-type sub-resource relationship | Field table + a diagram of Event → TicketType ownership |
| M2 | Full event lifecycle walkthrough | Runbook: create event → add ≥1 ticket type → verify via public `/events` → update → archive |
| M3 | Hand-off protocol to GMD-24/GMD-25 | Written checklist: "an event is ready to sell/scan when..." |

## Assessment

Per `../CERTIFICATION_MODEL.md`. Assessment artifact: M2 runbook
executed + M3 checklist reviewed against a real event's actual field
state.

## Evidence / certification / mission eligibility

Same pattern as GMD-22 (see that file for the general shape). Mission
eligibility ties specifically to live-event production support.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.
