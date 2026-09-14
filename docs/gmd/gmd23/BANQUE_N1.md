# GMD-23 — Banque N1 (formative, M1→M3)

```
Sourced against gmfest972/goodmooddjsayd/backend/server.py lines
99-114 (EventIn/Event) and 312-394 (admin event routes).
```

## M1 — `Event`/`EventIn` field literacy

1. Which field is the finite-state one, and what are its declared
   values? (`status`: `vision`/`announced`/`on_sale`/`sold_out`/`past`
   — `EVENT_STATUSES` set)
2. What is the default `status` for a brand-new event? (`"vision"`)
3. `ticket_url` is described in code as "external fallback for legacy
   dates without ticket_types." What does that tell you about an event
   that has real `TicketType` records? (`ticket_url` becomes
   irrelevant/unused for it — it's a fallback path, not the primary one)
4. Name the two fields on `Event` not present on `EventIn`.
   (`id`, `created_at`)
5. What does `capacity: int = 0` default to, and what does a candidate
   need to check before assuming an event has a real capacity limit
   set? (Defaults to 0 — must verify it was actually set, not assume)

## M2 — full event lifecycle

6. Exact route to create an event. (`POST /admin/events`)
7. Exact route to add a ticket type to an existing event.
   (`POST /admin/events/{eid}/ticket-types`)
8. Exact route to update an event's details. (`PUT /admin/events/{eid}`)
9. Exact route to delete an event. (`DELETE /admin/events/{eid}`)
10. What is the public route a fan uses to see events, and does it
    require auth? (`GET /events` — public, no `Depends(get_current_admin)`)

## M3 — hand-off protocol

11. Per `payments/checkout`'s own real check, what event `status` value
    is required before a ticket type on that event can actually be
    purchased? (`on_sale` — checkout raises 400 "Event not on sale"
    otherwise; this is the real, code-enforced readiness gate a
    candidate must cite, not a value they invent)
12. What must exist on an event before GMD-25 (door scan) can
    meaningfully use `/scan/counter/{eid}`? (At least one issued/valid
    ticket — the counter reads `db.tickets` counts, an event with zero
    tickets returns zeroes, not an error)
13. Whose job is configuring price/quota once an event exists — GMD-23
    or GMD-24? (GMD-24 — ticket type creation is a distinct
    specialization even though its route is nested under
    `/admin/events/{eid}/ticket-types`)
