# GMD-25 — Banque N1 (formative, M1→M3)

```
Sourced against server.py lines 715-753 (scan_check, scan_counter).
```

## M1 — the three real scan outcomes

1. Name the exact three `result` values `POST /scan/check` can return.
   (`"invalid"`, `"already_scanned"`, `"valid"`)
2. What are the two distinct reasons a scan can return `"invalid"`?
   (Ticket not found at all; or `req.event_id` provided and it doesn't
   match the ticket's real `event_id` — "Wrong event")
3. What three fields does a successful scan write onto the ticket
   document? (`status: "scanned"`, `scanned_at`, `scanned_by` — the
   admin's own `email`)
4. What real side-effect does a successful (`"valid"`) scan trigger
   besides updating the ticket? (A `frek_service.emit(...
   interaction_type="entry_scan"...)` call — wrapped in try/except so a
   FREK emit failure never blocks the scan result)
5. Is `event_id` on `ScanRequest` required? (No —
   `Optional[str] = None`; it's an optional guard, only checked if
   provided)

## M2 — live counter literacy

6. Exact route for the live attendance counter.
   (`GET /scan/counter/{eid}`)
7. Name the two counts it returns and what each actually counts.
   (`scanned`: `status=="scanned"` tickets; `issued`: tickets with
   `status` in `["valid","scanned"]` — i.e. issued-but-not-yet-scanned
   plus scanned)
8. What does the counter return for `capacity`, and where does that
   number come from? (The event's own `capacity` field, read from
   `db.events` — not computed from tickets)
9. If an event has `capacity=0` (the field's default), what would the
   counter honestly report? (`capacity: 0` — a candidate must recognize
   this as "capacity was never set," not "the venue holds zero people")

## M3 — escalation boundary

10. What must a door operator do when a scan result doesn't match any
    of the three known outcomes (a genuinely unexpected system error)?
    (Escalate to a human immediately — no automated incident/recovery
    path exists, per GMD-34's declared gap; never invent a workaround
    or a fourth outcome)
11. Why is this specific formation the one where GMD-34's gap matters
    most concretely? (It is the field-operations role physically at the
    door on event night — an unhandled failure here has immediate,
    real-time consequences, unlike a back-office reporting error)
