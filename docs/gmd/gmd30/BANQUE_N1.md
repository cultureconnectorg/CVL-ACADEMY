# GMD-30 — Banque N1 (formative, M1→M3)

```
Sourced against server.py lines 389-410 (admin_event_tickets,
admin_event_report).
```

## M1 — report field literacy

1. Name every field the real report returns.
   (`event`, `by_type[]`, `total_sold`, `total_quota`, `revenue_cents`,
   `currency`, `fill_rate`, `checked_in`)
2. How is `revenue_cents` actually computed? (`sum(sold * price_cents)`
   **per ticket type** — a theoretical figure derived from `TicketType`
   fields, NOT a sum of real `payment_transactions.amount_cents`. A
   candidate must cite this exact computation, never assume it reads
   real payment records.)
3. What does `total_quota` fall back to if the event has zero
   `TicketType` records? (`ev.get("capacity", 0)` — the event's own
   `capacity` field)
4. What is `fill_rate` when `total_quota` is 0? (`0.0` — the code
   guards against division by zero explicitly: `(total_sold /
   total_quota) if total_quota else 0.0`)
5. What does `checked_in` count, exactly? (Tickets with
   `status == "scanned"`, counted from the raw `db.tickets` query — the
   same underlying data GMD-25's counter reads, computed independently
   here)

## M2 — cross-check exercise

6. Exact route for the raw per-ticket data behind the report.
   (`GET /admin/events/{eid}/tickets`)
7. What real cap does that raw-tickets route apply?
   (`to_list(2000)` — if an event genuinely has more than 2000 tickets,
   the raw list is truncated even though the report's own aggregation
   over `to_list(5000)` would still be complete; a candidate cross-
   checking a discrepancy must know these two caps differ)

## M3 — scope-of-report discipline

8. Does the report distinguish revenue by payment method (card vs.
   other)? (No — no such breakdown exists in the real return shape;
   that granularity, if needed, would come from `payment_transactions`
   directly via GMD-28, a different data source entirely)
9. Is `revenue_cents` the same number an accountant reconciling real
   Stripe payouts would use? (Not necessarily — it's a theoretical
   sold×price figure, not a confirmed-payment sum; a candidate must
   flag this distinction rather than present the report figure as
   audited revenue)
