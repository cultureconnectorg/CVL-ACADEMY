# GMD-24 — Banque N1 (formative, M1→M3)

```
Sourced against server.py lines 115-131 (TicketTypeIn/TicketType),
353-394 (admin ticket-type routes), 489-560 (checkout capacity
check), 697-716 (public ticket + QR).
```

## M1 — `TicketType` field literacy + capacity

1. What two fields together define remaining capacity, and what is the
   exact formula used in `payments/checkout`? (`quota`, `sold`;
   `remaining = max(0, quota - sold)`)
2. What three fields exist on `TicketType` but not `TicketTypeIn`?
   (`id`, `sold`, `lookup_key`/`stripe_product_id`/`stripe_price_id` —
   name at least the server-generated ones)
3. What does `lookup_key` starting with `gmtt_` signal in
   `create_checkout`? (`is_ticket = req.lookup_key.startswith("gmtt_")`
   — it's how the code distinguishes a ticket purchase from a merch
   purchase, not a separate route)
4. What happens in `create_checkout` if `remaining < req.quantity`?
   (HTTP 400, `"Only {remaining} left"`)
5. What happens if a ticket purchase request has no `email`? (HTTP 422,
   `"Email required for ticket purchase"` — merch purchases don't have
   this requirement)

## M2 — ticket lifecycle: sale → QR → scan-readiness

6. Exact route to fetch a ticket's public detail. (`GET /tickets/{tid}`)
7. Exact route to fetch a ticket's QR image. (`GET /tickets/{tid}/qr.png`)
8. What HTTP media type does the QR route return, and what caching
   header? (`image/png`, `Cache-Control: public, max-age=3600`)
9. What does `public_ticket` return alongside the raw ticket record?
   (A trimmed event summary: `name`, `date`, `venue`, `city`, `country`)
10. Before a ticket can be scanned (GMD-25), what real check does
    `payments/checkout` require on the event's own `status`? (Must be
    `"on_sale"` — same gate as GMD-23's M3, cited here from the ticket
    side)

## M3 — downstream hand-off map

11. Name the two outbox systems a real ticket purchase can trigger.
    (`frek_id_outbox` via `frek_service.emit(...interaction_type=
    "purchase"...)`, `wallet_outbox` via `wallet_service`)
12. Which formation reads `db.fans` records that a ticket purchase
    upserts? (GMD-26)
13. Which formation actually processes the payment confirmation that
    marks a `TicketType.sold` count up? (GMD-28, via `POST
    /stripe/webhook`)
