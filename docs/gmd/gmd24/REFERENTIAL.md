# GMD-24 — Ticket Type & Sales Operator

```
Prerequisite: GMD-21, GMD-23 (an event must exist before it can sell tickets).
```

## Repo truth

`TicketType`/`TicketTypeIn` model; routes `POST/PUT /admin/events/
{eid}/ticket-types/{tid}`, `GET /tickets/{tid}`, `GET /tickets/{tid}/
qr.png` (real QR code generation for the ticket). Feeds GMD-26 (a
purchase creates/updates a fan record), GMD-28 (payment), GMD-31/32
(FREK/Wallet outbox emit on purchase).

## Prerequisites

GMD-21, GMD-23.

## Objectives

1. Configure ticket types (price, capacity, name) for a real event.
2. Trace a ticket from purchase through QR generation to the record a
   door-scan operator (GMD-25) will later validate.
3. Explain what "sold out" means at the code level (capacity check)
   and what happens when it's hit.

## Modules

| # | Module | Deliverable |
|---|---|---|
| M1 | `TicketType` field literacy + capacity semantics | Field table + written note on the capacity-check logic |
| M2 | Ticket lifecycle: sale → QR generation → scan-readiness | Traced walkthrough with the real `/tickets/{tid}/qr.png` route |
| M3 | Downstream hand-off map | Diagram: ticket sale → GMD-26 (fan record), GMD-28 (payment), GMD-31/32 (outbox emit) |

## Assessment

Per `../CERTIFICATION_MODEL.md`. Assessment artifact: M2 traced
walkthrough, verified against the real route chain.

## Evidence / certification / mission eligibility

Same general pattern as GMD-22. This is the most cross-referenced
specialization in the cluster (four downstream dependents) — its
certification is the most operationally load-bearing of the 13.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.
