# GMD-21 — Banque N1 (formative)

```
Honest count: 16 questions across the formation's 4 modules. No
padding to a round number — this reflects the real size of GMD-21's
scope (an orientation formation, not a deep specialization).
```

## M1 — System map (5 questions)

1. A new route `GET /admin/things/{id}` appears in `server.py`. Based
   on the naming convention alone, which GMD specialization would most
   plausibly own it, and why? *(Tests reasoning from convention, not
   memorization — no single correct answer if reasoned honestly.)*
2. Which of the following are **public** routes (no admin auth
   required)? `/catalogue`, `/admin/catalogue`, `/events`, `/admin/
   events/{eid}`, `/merch`, `/tour`. *(Answer: `/catalogue`, `/events`,
   `/merch`, `/tour`.)*
3. What does the FREK/Wallet outbox pattern (GMD-31/32) protect
   against that a direct, synchronous call would not?
4. Name the two Good Mood routes that generate a QR code, and which
   GMD specialization owns them.
5. True/False: `server.py` implements its own incident-response
   system for scan failures. *(False — this is GMD-34's declared gap.)*

## M2 — Data model literacy (4 questions)

6. What real-world object does the `Volume` model represent in this
   codebase?
7. Name one field `TicketType` almost certainly has, based on its
   role in the system (without looking at the code) — then verify
   against the real model.
8. Why does this Master Package's own doctrine warn against inventing
   fields a model doesn't have when answering a stakeholder's data
   question (see `gmd26/REFERENTIAL.md` §M3)?
9. What is the real difference between `Product` (GMD-27) and `Volume`
   (GMD-22) at the model level, beyond their names?

## M3 — Auth & session boundary (4 questions)

10. What does `Depends(get_current_admin)` do to a route that uses it?
11. Which three routes make up the real login/session lifecycle?
12. If a candidate cannot find `Depends(get_current_admin)` on a given
    route, what should they conclude about that route?
13. Why is GMD-33 a prerequisite for effectively operating any of
    GMD-22 through GMD-32?

## M4 — Outbox pattern literacy (3 questions)

14. List the 5 retry backoff intervals used by both `frek_service.py`
    and `wallet_service.py`.
15. What state does an outbox entry reach after all 5 retries fail?
16. Why must Good Mood's `frek_service.py` never be described as "the
    same as" this Academy's own `backend/services/frek_core.py`?

## Status

`STATUS = N1_BANK_V1`. Referenced by the Assessment
(`ASSESSMENT_AND_RUBRIC.md`); not yet administered to a real
candidate.
