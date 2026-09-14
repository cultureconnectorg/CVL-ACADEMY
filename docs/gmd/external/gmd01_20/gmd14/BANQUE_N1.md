# GMD-14 — Banque N1 (formative, M1→M4)

```
Sourced against GMD-28's own repo-truth (cited, never re-derived) and
standard event/festival finance practice.
```

## M1 — checkout-to-order sequence

1. Name the 4 real steps of the payment sequence, per GMD-28's
   worked example. (`POST /payments/checkout` creates a Stripe
   session → Stripe processes payment → `POST /stripe/webhook`
   confirms → order appears in `GET /admin/orders`)

## M2 — webhook literacy & failure diagnostics

2. Why does the webhook-based confirmation pattern exist rather than
   confirming payment directly from the buyer's browser? (Payment
   confirmation must not depend on the buyer's browser staying open —
   the same asynchronous-confirmation principle as the FREK/Wallet
   outbox pattern, GMD-31/32)
3. If a report says "payment succeeded but order missing," what is
   the correct first diagnostic step? (Check whether the webhook
   fired and was processed — via webhook logs / Stripe dashboard —
   never guess at a cause)

## M3 — order reconciliation

4. What real endpoint lets an operator verify an order against a
   Stripe payment ID? (`GET /admin/orders`, cited from GMD-28)

## M4 — market-general finance practices beyond the platform

5. Name two standard event-finance practices GMD-28's real
   integration does not implement, per this referential.
   (Multi-currency settlement, sponsor invoicing — also tax handling)
6. How must such practices be labeled when taught here? (Explicitly
   `NOT_A_PLATFORM_CAPABILITY`)
