# GMD-28 — Banque N1 (formative, M1→M4)

```
Sourced against server.py lines 489-560 (create_checkout,
get_payment_status), 574-620 (_issue_tickets_for_session), 657-690
(stripe_webhook), 760-763 (admin_orders).
```

## M1 — checkout session lifecycle

1. Exact route to start a checkout. (`POST /payments/checkout`)
2. What real collection records the transaction the moment checkout
   starts — before any payment confirmation? (`db.payment_transactions`,
   `status: "initiated"`, `payment_status: "pending"`)
3. What distinguishes a ticket checkout from a merch checkout in the
   metadata? (`"type": "ticket"` vs `"type": "merch"`, set from
   `is_ticket = req.lookup_key.startswith("gmtt_")`)
4. For a ticket purchase, what does the code require that a merch
   purchase does not? (A real `email` — 422 if missing; merch requires
   `shipping_address_collection` instead)

## M2 — webhook literacy

5. Exact route Stripe calls to confirm payment.
   (`POST /stripe/webhook`)
6. What does the webhook verify before trusting the payload?
   (`stripe.Webhook.construct_event(payload, sig,
   STRIPE_WEBHOOK_SECRET)` — signature verification; raises 400 on
   `SignatureVerificationError`)
7. Which Stripe event type actually triggers order completion?
   (`"checkout.session.completed"`)
8. What real function does the webhook call for a **ticket**
   transaction specifically, and what does it NOT call for merch?
   (`_issue_tickets_for_session` — ticket-only; merch instead sends an
   order confirmation email via `send_order_confirmation`)
9. What happens on `"checkout.session.async_payment_failed"`?
   (`payment_transactions` updated to `status: "failed"`,
   `payment_status: "failed"`)

## M3 — order reconciliation

10. Exact route to see all orders. (`GET /admin/orders`)
11. What does `admin_orders` sort by, and what real cap does it apply?
    (`.sort("created_at", -1)`, `to_list(1000)`)
12. Given a Stripe payment ID, is there a direct route to look up the
    matching order by that ID alone? (No — `GET /payments/status/
    {session_id}` looks up by `session_id`, not by
    `stripe_payment_intent_id`; a candidate must trace via
    `session_id` first, never assume a payment-intent-keyed lookup
    route exists)

## M4 — failure-mode diagnostic

13. `get_payment_status` finds a transaction whose `payment_status !=
    "paid"` — what does the real code do before returning? (Calls
    `stripe.checkout.Session.retrieve(session_id)` directly and
    updates the record if Stripe itself reports paid/complete — a
    real, self-healing reconciliation path, not just a passive read)
14. If a webhook genuinely never fired (delivery failure), what real
    evidence should an operator check before escalating? (Stripe's own
    dashboard/webhook logs — the code has no separate webhook-delivery
    log of its own; never invent an internal "webhook log" table that
    doesn't exist in this schema)
