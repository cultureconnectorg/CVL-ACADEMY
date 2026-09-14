# GMD-32 — Wallet Ticket Integration Operator

```
Prerequisite: GMD-21. Triggered by GMD-24 (ticket purchase).
```

## Repo truth

`wallet_service.py` (115 lines) — same real env-gated outbox pattern
as GMD-31 (`frek_service.py`), pointed at `WALLET_URL` instead, with
its own `db.wallet_outbox` table. Route: `GET /admin/outbox/wallet`.

## Prerequisites

GMD-21, GMD-24.

## Objectives

1. Read the wallet outbox monitoring route and interpret entry status
   the same way as GMD-31 (delivered/pending/failed).
2. Explain what a ticket purchase is meant to credit in the (not-yet-
   connected) Wallet system, per the payload shape, without asserting
   the credit has actually happened anywhere.
3. Keep this system distinct from this repo's own real `backend/
   wallet/` ledger (`WalletAccount`, `WalletTransaction`) — Good Mood's
   `wallet_service.py` is an **outbound client** to an external Wallet
   URL, not the same code as this Academy's own Wallet implementation.

## Modules

| # | Module | Deliverable |
|---|---|---|
| M1 | Outbox payload literacy (Wallet variant) | Annotated example payload |
| M2 | Retry-schedule literacy | Same backoff pattern as GMD-31, applied here |
| M3 | Boundary discipline | Explicit distinction: Good Mood's `wallet_service.py` (outbound client, `NOT_CONNECTED` by default) vs this Academy's own `backend/wallet/service.py` (a real, different, additive-only ledger) |

## Assessment

Per `../CERTIFICATION_MODEL.md`. M3 is eliminatory, same rationale as
GMD-31/M3.

## Evidence / certification / mission eligibility

Same general pattern as GMD-22.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD32` — full canonical package built.
`FULLY_COMPLETE` still requires a real candidate pass.
