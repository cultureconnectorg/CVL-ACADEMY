# Commerce Convergence Decision — RECONCILE-3 Phase 5

Status: **ANALYSIS ONLY — no code changed by this document.** Per the
Founder's explicit RECONCILE-3 instruction: "Ne pas encore unifier les
deux architectures commerce identifiées en Groupe 3 [...] Aucune
décision produit implicite pendant RECONCILE-3." This report identifies
the real, currently-coexisting commerce architectures, what each one
actually does (verified by reading the code, not assumed), where they
overlap, where they conflict, and the options for converging them. The
convergence decision itself belongs to the Founder.

## Method

Read every commerce-adjacent backend module end to end (`api/commerce.py`,
`api/commercial.py`, `api/payments.py`, `api/billing.py`,
`billing_config.py`, `commerce/` package, `payments/` package,
`commercial.py`, `economy_3d.py`) and cross-referenced each against real
frontend consumers (`grep` for the literal route prefix across
`frontend/src`). Nothing below is inferred from file names alone — every
claim traces to a specific function or route.

## The three commerce-adjacent surfaces that exist today

### CURRENT_A — `/commerce/*` (ACA-0025, `api/commerce.py` + `commerce/` package)

- **What it is**: a **read-only catalogue**, not a transaction system.
  `OFFERS`/`POLICIES` are Python constants in `commerce/catalog.py`,
  transcribed verbatim from the Founder's own
  `CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx` (`Decisions_Fondateur`
  ECO-001..024, `Offres_Economiques`, `Policies` sheets — 20 sellable
  offers, 18 policy rules, dated 2026-09-06).
- **Routes**: `GET /commerce/offers` (public, customer-facing fields
  only — no cost/margin/floor), `GET /commerce/offers/internal` and
  `GET /commerce/policies` (staff-only, full figures).
- **Currency / identity key**: EUR, `offer_id` (e.g. `academy-access`,
  `academy-pro`).
- **Explicitly, by its own module docstring**: `NO_FAKE_PAID_STATE` —
  "nothing here creates or reads a paid/subscribed state on any user."
  It cannot itself grant anything.
- **Frontend consumer**: `frontend/src/pages/Offers.js` (real, wired,
  W-FUNNEL-2 Conversion surface) — pricing display only, no purchase
  action originates here.

### CURRENT_B — `/commercial/*` (Economy 3D → CVLN Wallet, `api/commercial.py` + `commercial.py` + `economy_3d.py`)

- **What it is**: a **real, end-to-end transaction pipeline** against a
  *different* catalogue source — `economy_3d.py`'s `economy_code`
  records (Economy 3D requirements), not `commerce/catalog.py`'s
  `offer_id` list.
- **Flow**: `POST /commercial/orders` (resolves the offer via
  `resolve_offer(economy_code, offer_kind)`, which enforces real
  commercial-policy gates — `NotForSale`, `QuoteRequired`,
  `EligibilityRequired` — before an order can even be created) →
  `POST /commercial/orders/{id}/pay-wallet` (charges the amount, in
  **JCC** — converted from EUR via `amount_eur_to_jcc()` at a rate
  fetched live from the external **CVLN Wallet** service — through
  `services/integrations/cvln_wallet.py`) → on success, upserts an
  `academy_entitlements` document (`entitlement_filter(user_id,
  economy_code)`, `status="ACTIVE"`) → generates a real invoice via
  `billing.build_invoice_intent()` into `db.billing_documents`.
- **Idempotency**: real — `pay-wallet` uses `find_one_and_update` gated
  on `status: "PENDING_PAYMENT"` to claim the attempt atomically before
  calling the external wallet, and the entitlement upsert uses
  `$setOnInsert` so a retried success never double-grants.
- **Currency / identity key**: JCC (CVLN Wallet's own token), keyed by
  `economy_code`.
- **Frontend consumer**: `frontend/src/components/CommercialPurchaseCard.jsx`
  (real, wired — this is the actual "buy" UI in production today), plus
  `frontend/src/components/BillingInvoicePanel.jsx` and
  `frontend/src/pages/Pricing.js` for the invoice side.
- **This is the only one of the three that a real user can complete a
  purchase through end to end in the current UI.**

### CURRENT_C — `/payments/*` (ACA-0026, `payments/` package)

- **What it is**: a **real, independently complete Stripe-style
  checkout/webhook pipeline** — but against `commerce/catalog.py`'s
  `offer_id` catalogue (the *same* catalogue CURRENT_A reads, **not**
  CURRENT_B's `economy_code` one).
- **Flow**: `POST /payments/checkout` (`create_checkout()` resolves a
  real `commerce.catalog.get_offer(offer_id)`; if no real payment
  provider is configured it persists the attempt and raises a **503**
  rather than fabricate a checkout URL — its own documented
  `NO_FAKE_PAID_STATE` discipline) → `POST /payments/webhook/stripe`
  (real Stripe signature verification via
  `verify_stripe_webhook_signature`; only a verified
  `checkout.session.completed` event may ever write `status="paid"`;
  idempotent by `last_provider_event_id`, guarding Stripe's documented
  at-least-once delivery).
- **Currency / identity key**: EUR, `offer_id`.
- **Critical gap, verified by reading `payments/service.py` in full**:
  on a successful webhook, `handle_stripe_webhook()` updates
  `db.payments` and `db.payment_checkout_sessions` status to `"paid"`
  and returns — **it never touches `db.academy_entitlements` or any
  other unlock mechanism.** A real, verified Stripe payment through this
  pipeline today does not grant the buyer anything. This is not a
  hypothetical edge case; it is what the code, read end to end, actually
  does.
- **Frontend consumer**: **none.** `grep -rl "/payments" frontend/src`
  returns zero matches. This is a real, tested (backend test suite),
  fully wired backend capability with no UI entry point — "recovered"
  in the file-exists sense, but not reachable by any real user journey.

## OVERLAP

- CURRENT_A and CURRENT_C share the exact same catalogue
  (`commerce/catalog.py`'s `OFFERS`, `offer_id`, EUR pricing) — CURRENT_A
  is that catalogue's read surface, CURRENT_C is (an unwired) purchase
  surface for it.
- CURRENT_B and CURRENT_C both claim the domain concept "pay to unlock
  an Academy capability," each with its own real order/payment record,
  its own idempotency mechanism, and its own success path.
- CURRENT_B and CURRENT_C both produce a persisted "did this succeed"
  record (`commercial_orders` vs `payments`) that a hypothetical unified
  "my purchases" view would need to merge.

## DIFFERENCES

| | CURRENT_A (`/commerce`) | CURRENT_B (`/commercial`) | CURRENT_C (`/payments`) |
|---|---|---|---|
| Role | Read-only catalogue | Real purchase pipeline | Real purchase pipeline |
| Catalogue source | `commerce/catalog.py` (DECIDED_V1, `offer_id`) | `economy_3d.py` (`economy_code`) | `commerce/catalog.py` (DECIDED_V1, `offer_id`) — same as A |
| Currency | EUR (display) | JCC via CVLN Wallet | EUR via Stripe |
| Payment rail | none | CVLN Wallet (external, internal ecosystem) | Stripe (external, standard PSP) |
| Grants entitlement on success? | N/A | **Yes** (`academy_entitlements`) | **No** (verified gap above) |
| Generates invoice? | N/A | Yes (`billing.build_invoice_intent`) | No |
| Policy gating (eligibility/quote/not-for-sale) | N/A | Yes (`resolve_offer`) | No — any authenticated user can checkout any offer |
| Frontend wired? | Yes (`Offers.js`) | Yes (`CommercialPurchaseCard.jsx`, `BillingInvoicePanel.jsx`) | **No** |

## SHARED_PRIMITIVES

Real, reusable pieces that any convergence path should keep rather than
rebuild:

- `NO_FAKE_PAID_STATE` discipline — consistently enforced across all
  three (A never claims a paid state; B only grants after a real wallet
  charge; C only marks paid after a real verified webhook). This
  invariant should survive any convergence unchanged.
- Idempotent-write pattern — B's `find_one_and_update` status-gated
  claim and C's `last_provider_event_id` dedup are the same underlying
  discipline (never let a retried success double-apply) applied to two
  different payment rails. A converged design should keep one such
  guard per payment rail, not invent a third pattern.
- `commerce/catalog.py`'s `OFFERS`/`get_offer()` — already the shared
  source of truth between A and C; a converged catalogue should extend
  this, not replace it.
- `db.academy_entitlements` — B's entitlement shape
  (`entitlement_filter`: `user_id` + `economy_code` + `status`) is the
  only real "what did this user unlock" record that exists today; C has
  no equivalent. Any convergence needs exactly one entitlement model,
  and B's is the only one currently wired to anything that checks it.

## CONFLICTS

1. **Two different catalogue keys for "the same idea" of an offer**:
   `economy_code` (B) vs `offer_id` (A/C). A converged system needs one
   canonical offer identity, or an explicit, documented mapping between
   the two — silently aliasing them risks selling the wrong thing at the
   wrong price.
2. **Two different currencies with no defined exchange authority
   outside a single order**: B converts EUR→JCC per-order via a rate
   fetched live from CVLN Wallet; C is EUR-only via Stripe. If a future
   unified checkout must offer both payment rails for the same offer,
   the EUR price is the only value both currently agree on — the JCC
   price is order-time-derived, not a catalogue fact.
3. **C's missing entitlement grant is a real product gap, not a stylistic
   difference**: if C were exposed to users today as-is, a successful
   real Stripe payment would silently grant nothing. Converging toward
   "use C for EUR/Stripe payments" requires adding the same
   entitlement-grant step B already has — not a redesign, but not a
   trivial merge either.
4. **C has no policy gate**: B's `resolve_offer()` enforces
   `NotForSale`/`QuoteRequired`/`EligibilityRequired` before an order can
   exist; C's `create_checkout()` has no equivalent check against
   `commerce/catalog.py`'s own `EconomicPolicy` rules. An offer B would
   refuse to sell (e.g. `INTERNAL_NOT_FOR_SALE`) could currently be
   checked out through C without any policy check applying, because C
   was built against a catalogue that carries policy data (`POLICIES` in
   `commerce/__init__.py`) it never reads.

## TARGET_OPTIONS (for Founder decision — not decided here)

**Option 1 — B is canonical, C is retired or repurposed.**
Keep `/commercial` (Economy 3D + CVLN Wallet + entitlement + invoice) as
the one real purchase path, since it is the one already wired to a real
UI and the only one that gates on policy and grants entitlements. Retire
`/payments` (Stripe) entirely, or repurpose its real, working
Stripe/webhook plumbing as the *implementation* of a future
"pay in EUR instead of JCC" option inside B's own order flow, rather
than a parallel pipeline.

**Option 2 — C is canonical, B is retired or repurposed.**
Standardize on Stripe/EUR as the one real payment rail (arguably more
familiar to an external, non-ecosystem buyer), close B's gaps into C
(port the policy gate, the entitlement grant, and the invoice step from
B into C), and retire the CVLN Wallet/JCC path — or keep it only as an
optional internal-ecosystem settlement layer behind the same catalogue.

**Option 3 — Both remain, explicitly scoped by buyer type.**
Keep B for JCC/CVLN-ecosystem buyers (its own catalogue —
`economy_code`) and C for EUR/external buyers (`commerce/catalog.py`'s
`offer_id`), but close C's real gaps (entitlement grant, policy gate)
so a completed Stripe payment behaves identically to a completed wallet
payment from the buyer's perspective, and expose C in the frontend.
Requires an explicit, documented mapping between `economy_code` and
`offer_id` wherever the two catalogues describe the same real offer, to
avoid divergent pricing/eligibility for "the same thing" sold two ways.

**Option 4 — Unify catalogues first, defer payment-rail decision.**
Merge `commerce/catalog.py` and `economy_3d.py` into one canonical
offer/policy source (the harder, more foundational move — everything
downstream, both B and C, currently reads a different one), then decide
the payment-rail question (Option 1/2/3) against a single catalogue
instead of two.

## FOUNDER_DECISION_REQUIRED

1. Which of Options 1-4 (or a variant) should CVLN Academy converge
   toward?
2. If any form of C (Stripe/EUR) survives: is CVLN Wallet/JCC meant to
   be the *only* real settlement rail (C's EUR flow ultimately routes
   through B), or a genuinely independent second rail?
3. If B and C are meant to coexist per-buyer-type (Option 3): what is
   the authoritative mapping between `economy_code` and `offer_id` for
   every current DECIDED_V1 offer, and who owns keeping it in sync as
   either catalogue changes?
4. Is `/payments/*`'s current zero-frontend-consumer state intentional
   (a deliberately staged, not-yet-launched capability) or an oversight
   from ACA-0026's original scope? This determines whether Phase 6
   should classify its currently-untested UI-integration gap as
   `EXPECTED_FAILURE` (deliberately unfinished) or `BUG_PRODUCT`
   (should have been wired and wasn't).

No code in `commerce.py`, `commercial.py`, `payments.py`, `billing.py`,
or their frontend consumers was modified to produce this document.
