# GMD-32 — Banque N1 (formative, M1→M3)

```
Sourced directly against wallet_service.py (full file, 115 lines) and
server.py:770-773 (GET /admin/outbox/wallet).
```

## M1 — outbox payload literacy (Wallet variant)

1. Name the real top-level keys of the wallet push payload.
   (`source`, `wallet_action`, `identifier`, `ticket`, `timestamp`)
2. What is the fixed, literal value of `wallet_action`?
   (`"push_ticket"` — never varies, unlike GMD-31's `interaction_type`
   which has two real values)
3. Name every field inside the nested `ticket` object.
   (`ticket_id`, `event_id`, `event_name`, `city`, `venue`, `date`,
   `type`, `qr_url`, `view_url`)
4. What real endpoint path does the POST target, and how does it
   differ from GMD-31's FREK endpoint? (`{WALLET_URL}/wallet/tickets`
   vs. FREK's `{FREK_ID_URL}/frek-id/events` — different path, same
   `_post`-style client pattern)
5. Does the wallet payload contain an `external_id`, like the FREK
   payload does? (No — `identifier` here contains only `email`, not
   `external_id`; a candidate must not assume payload parity between
   the two outbox systems just because the retry mechanic is
   identical)

## M2 — retry-schedule literacy (same backoff pattern as GMD-31)

6. Are `RETRY_BACKOFFS_SEC` identical between `wallet_service.py` and
   `frek_service.py`? (Yes — `[30, 120, 600, 3600, 21600]`, same values,
   same `limit(20)` per iteration, same `asyncio.sleep(30)` cadence —
   the two outbox systems share the exact retry mechanic even though
   their payload shapes differ)
7. What env vars gate this specific outbox (name both)?
   (`WALLET_URL`, `WALLET_TOKEN` — distinct from FREK's
   `FREK_ID_URL`/`FREK_ID_TOKEN`)

## M3 — boundary discipline (eliminatory)

8. Is `wallet_service.py`'s outbox the same system as this repo's own
   `backend/wallet/service.py` (`WalletAccount`/`WalletTransaction`)?
   (**No** — Good Mood's `wallet_service.py` is an **outbound HTTP
   client** pushing ticket data to an external, not-yet-connected
   `WALLET_URL`; this Academy's own `backend/wallet/` is a real,
   different, additive-only ledger with no HTTP client at all. Two
   completely different pieces of code with the word "wallet" in
   common — conflating them is the same `CROSS_DOMAIN_CONTAMINATION`
   risk GMD-31/M3 teaches for FREK, applied here to Wallet.)
9. The payload's own docstring says "Payload contract to be finalised
   with wallet team — this is a reasonable draft." What does that
   honestly tell a candidate about this payload's stability? (It is
   explicitly provisional per the repo's own comment — never present
   this shape as a finalized, stable external contract)
