# GMD-28 — Orders & Payment Operations

```
Prerequisite: GMD-21, GMD-24 (ticket sales) and GMD-27 (merch sales) as its two real revenue sources.
```

## Repo truth

**Real Stripe integration**: `POST /payments/checkout`, `GET /payments/
status/{session_id}`, `POST /stripe/webhook`; `GET /admin/orders`. This
is the best-grounded payment precedent in the entire CVLN ecosystem
audited this session (cited as the worked example for `WAL-08` in
`WALLET_CVE_RECONCILIATION.md`).

## Prerequisites

GMD-21, GMD-24, GMD-27.

## Objectives

1. Trace a real checkout end to end: `POST /payments/checkout` creates
   a Stripe session → the webhook (`POST /stripe/webhook`) confirms
   payment → the order appears in `/admin/orders`.
2. Explain why the webhook exists (payment confirmation must not
   depend on the buyer's browser staying open) — the same asynchronous-
   confirmation principle already documented for the FREK/Wallet
   outbox pattern (GMD-31/32), applied to payments.
3. Diagnose a "payment succeeded but order missing" report by checking
   whether the webhook fired and was processed, not by guessing.

## Modules

| # | Module | Deliverable |
|---|---|---|
| M1 | Checkout session lifecycle | Sequence diagram: checkout → Stripe → webhook → order record |
| M2 | Webhook literacy | Written explanation of what `/stripe/webhook` verifies and records |
| M3 | Order reconciliation | Runbook: given a Stripe payment ID, verify the corresponding order via `/admin/orders` |
| M4 | Failure-mode diagnostic | Case: webhook delivery failure — what real evidence to check (webhook logs, Stripe dashboard) before escalating |

## Assessment

Per `../CERTIFICATION_MODEL.md`. Assessment artifact: M1 sequence
diagram + M3 runbook executed against a real or sandboxed checkout.

## Evidence / certification / mission eligibility

Same general pattern as GMD-22. This is the one GMD-2X/3X role
directly handling real money — its qualification cycle should be
reviewed for whether it warrants the 12-month sensitive cycle
(`ECO-042`) alongside GMD-33; flagged here as a recommendation, not
yet decided (a genuine Founder/governance call, not resolved
unilaterally in this referential).

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD28` — full canonical package built.
`FULLY_COMPLETE` still requires a real candidate pass.
