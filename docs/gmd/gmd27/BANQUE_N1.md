# GMD-27 — Banque N1 (formative, M1→M3)

```
Sourced against server.py lines 133-150 (ProductIn/Product) and
440-467 (admin merch routes).
```

## M1 — `Product`/`ProductIn` field literacy

1. Name the fields unique to `ProductIn` that have no equivalent on
   `VolumeIn` (GMD-22). (`price_cents`, `currency`, `category`,
   `variant_label`, `variants[]`, `active`)
2. What does `active: bool = True` control? (Whether the product
   appears in `GET /merch` — the public route filters
   `{"active": True}`, confirmed at `server.py:255`)
3. What field distinguishes size/color options, and what type is it?
   (`variants: List[str]`, plus a `variant_label` describing what the
   list represents, e.g. "Size")
4. Which two fields exist on `Product` but not `ProductIn`?
   (`lookup_key`, plus `stripe_product_id`/`stripe_price_id` — at least
   name `lookup_key`)

## M2 — CRUD walkthrough

5. Exact route to create a product. (`POST /admin/merch`)
6. Exact route to list products as admin (all, active or not) vs.
   public (active only). (`GET /admin/merch` vs. `GET /merch` — the
   public route filters `active: True`, the admin route does not)
7. Exact routes to update/delete. (`PUT /admin/merch/{pid}`,
   `DELETE /admin/merch/{pid}`)

## M3 — hand-off to GMD-28

8. What must be true of a `Product` before `payments/checkout` can
   sell it? (It needs a real `lookup_key` used as a Stripe price lookup
   key — `create_checkout` calls `stripe.Price.list(lookup_keys=
   [req.lookup_key]...)`, and if no price is found the checkout returns
   404 "Price not found") — never claim a product is "sellable" just
   because it exists in `db.products`; a Stripe-side price must also be
   wired via `_sync_stripe_item`.
9. What exact prefix does `_sync_stripe_item` use for a merch
   product's `lookup_key`, and how does that differ from a ticket
   type's? (Merch: `lookup_prefix="gm"` → `f"gm_{id[:8]}"`; ticket
   types: `lookup_prefix="gmtt"` → `f"gmtt_{id[:8]}"` — this is exactly
   how `create_checkout`'s `is_ticket = req.lookup_key.startswith
   ("gmtt_")` check tells the two apart; a candidate must cite the
   real prefixes, not invent a different distinguishing mechanism)
10. What distinguishes `Product` from `Volume` (GMD-22) at the business
    level, despite the identical CRUD shape? (`Product` = physical/merch
    goods with price/variants, sold via checkout; `Volume` = discography
    catalogue entries, never sold directly — never conflate the two
    models even though their admin routes look structurally identical)
