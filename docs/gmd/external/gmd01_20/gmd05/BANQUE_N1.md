# GMD-05 — Banque N1 (formative, M1→M4)

```
Sourced against GMD-24's own repo-truth (cited, never re-derived) and
standard live-events ticketing-industry practice.
```

## M1 — ticket-type design

1. What three fields does a ticket-type design need at minimum, per
   GMD-24's real model? (Price, capacity/quota, name)

## M2 — quota-integrity nuance

2. Is the checkout-time quota check in the real platform an atomic
   reservation? (No — per GMD-24's own repo-truth, `remaining <
   req.quantity` is checked before Stripe session creation, with no
   lock/hold on `quota` at that moment)
3. What is the real anti-oversell guarantee, and when does it apply?
   (The atomic `$inc` on `sold`, applied at webhook-confirmation time
   in `_issue_tickets_for_session`, not at checkout time)

## M3 — sales-window & access hand-off

4. What does a ticket-operations role hand off to a door-scan
   operator (GMD-25), and where is that documented? (The confirmed
   ticket record with its QR — cited to GMD-24/GMD-25, never
   re-derived here)

## M4 — market-general practices beyond the platform

5. Name two standard live-events ticketing practices the real
   platform does not implement, per this referential. (Dynamic
   pricing, secondary-market/resale policy — also waitlist
   management)
6. How must such practices be labeled when taught in this formation?
   (Explicitly `NOT_A_PLATFORM_CAPABILITY` — legitimate market
   knowledge, never presented as something the real Good Mood
   platform does)
