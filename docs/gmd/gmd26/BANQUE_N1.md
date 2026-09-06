# GMD-26 — Banque N1 (formative, M1→M3)

```
Sourced against ticketing_service.py lines 24-70 (upsert_fan) and
server.py:415-418 (GET /admin/fans).
```

## M1 — fan record field literacy

1. Name the fields a real fan document actually holds.
   (`email`, `external_id`, `name`, `purchases[]`, `total_events`,
   `cities[]`, `segments[]`, `created_at`, `updated_at`)
2. Correction check: does the fan record hold **only** raw purchase
   history, with zero derived fields? (No — `segments` and
   `total_events`/`cities` ARE derived/computed on every upsert; a
   candidate who claims "no analytics at all" is wrong. The honesty
   discipline is about what these specific derived fields can and
   cannot answer, not about denying they exist.)
3. What are the three possible values in `segments`, and what triggers
   each? (`"primo"` — first purchase; `"recurring"` — 2nd+ purchase;
   `"vip"` — added whenever any purchase's `ticket_type` starts with
   `"VIP"`, case-insensitive, on top of primo/recurring)
4. What generates `external_id`, and is it guaranteed unique across
   fans with similar emails? (`f"gm-fan-{email.split('@')[0]}"` — the
   local-part before `@`; two different emails with the same local
   part, e.g. `x@a.com` and `x@b.com`, would collide — a real,
   citable data-quality edge case, never to be denied)

## M2 — fan-record query practice

5. Can the real fields answer "how many fans are VIP"? (Yes —
   `segments` contains `"vip"`)
6. Can they answer "how many fans from city X"? (Yes — `cities[]`)
7. Can they answer "average spend per fan"? (No — no `amount_cents`/
   monetary field exists on the fan document itself; that data lives on
   `payment_transactions`, a different collection, not joined here)

## M3 — data-honesty discipline

8. A stakeholder asks "which fans opened our last 3 emails" — what is
   the correct answer given the real schema? ("Not currently
   trackable" — no email-open tracking field exists anywhere in the
   fan document; never fabricate a number)
9. Why is inventing a plausible-sounding number worse than saying "not
   trackable"? (It creates false confidence for a real business
   decision — this is the same `FAKE_PROOF`/`UNPROVEN_FEATURE`
   discipline this whole Master Package applies to code, now applied to
   data honesty at the operator level)
