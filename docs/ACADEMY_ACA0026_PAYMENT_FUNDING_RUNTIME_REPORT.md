# ACA-0026 — Real Payment/Funding Runtime

```
STATUS: EXECUTED (2026-09-08). A real, working checkout/webhook
runtime bound to the existing DECIDED_V1 catalogue (ACA-0025) — never
a fabricated "connected" claim. Live charge execution requires real
Stripe credentials this sandbox does not have; that limitation is
disclosed below, not hidden behind a fake success path.
```

## The doctrine this had to respect

`commerce/models.py`'s own module docstring states the constraint this
pass had to work within: `ACA-0026` was previously left explicitly
`BLOCKED` because a payment runtime cannot be honestly faked the way
"ready but decoupled" interfaces elsewhere in this codebase (FrekCore,
Agent Factory) can — those systems' local fallbacks are allowed to
*succeed* (mint a real local FREK-ID, issue a real local proof) because
Academy is a legitimate authoritative source for that data until a real
remote system exists. A payment has no equivalent safe local truth:
this process cannot make €24.90 actually move between accounts. So
"unblocking" ACA-0026 does not mean fabricating a working Stripe
connection — it means building the real, correct, integration-ready
runtime (checkout creation, webhook signature verification, ledger
records) with **one asymmetry FrekCore's own pattern does not need**:
there is no local-fallback path that can ever produce a `"paid"`
status. Only a real, signature-verified webhook from a real, configured
provider can.

## What was built

- **`backend/payments/models.py`** — `CheckoutSession`, `PaymentRecord`
  (status `pending`/`paid`/`failed`/`canceled`/`refunded`),
  `CheckoutRequest`.
- **`backend/payments/provider.py`** — the swappable provider
  boundary, mirroring `services/frek_core.py`'s shape:
  - `is_provider_configured()` — both `STRIPE_SECRET_KEY` and
    `STRIPE_WEBHOOK_SECRET` must be set; either alone counts as
    unconfigured (a key with no way to verify confirmations is worse
    than neither).
  - `create_remote_checkout_session()` — a real Stripe Checkout
    Sessions REST call over `httpx` (already a project dependency,
    used for the FrekCore/Agent Factory shims — no new hard
    dependency added). Returns `None` on any failure, never a
    fabricated session.
  - `verify_stripe_webhook_signature()` — Stripe's own publicly
    documented signature algorithm, implemented exactly:
    `HMAC-SHA256(secret, f"{t}.{raw_body}")`, constant-time comparison
    against every `v1` value in the header (multiple during a
    signing-secret rotation), plus the same 300s replay-window check
    Stripe's own reference implementations apply.
  - `sign_stripe_payload()` — the same algorithm's signer, used only
    by this module's own tests to prove the verifier round-trips
    correctly (the strongest proof available without a live Stripe
    account — disclosed, not hidden, in the module docstring).
- **`backend/payments/service.py`** — `create_checkout()` (looks up
  the real offer from `commerce.catalog`, attempts a real remote
  session when configured, raises `ProviderNotConfiguredError`
  otherwise — never a fake URL), `handle_stripe_webhook()` (verifies
  signature, is the ONLY function anywhere in this package allowed to
  write `"paid"`, idempotent on a replayed event id).
- **`backend/api/payments.py`** — `POST /payments/checkout` (503 when
  the provider isn't configured), `GET /payments/mine`,
  `POST /payments/webhook/stripe` (the one deliberately unauthenticated
  route — authenticity comes from the signature check, exactly as
  Stripe's own integration guide requires).
- **`backend/infra_indexes.py`** — unique index on
  `idempotency_key`, `checkout_session_id`, and a partial unique index
  on `(checkout_session_id, last_provider_event_id)` guarding against a
  genuine concurrent-webhook-delivery race (the primary idempotency
  guard is the explicit `find_one` check in `handle_stripe_webhook`
  itself, not the index — the index only catches the race the
  application-level check can't).

## Verification

- `python -m pytest tests/test_payments.py -v` — **16/16 passed**:
  6 signature-verification proofs (valid, tampered body, wrong secret,
  expired timestamp, malformed header, multi-signature rotation
  window), checkout creation against a real catalogue offer,
  **the critical `NO_FAKE_PAID_STATE` proof** — `create_checkout`
  raises rather than returning a session when the provider is
  unconfigured, and the persisted audit record's `checkout_url` is
  `None`/`status="pending"`, never fabricated — checkout succeeding
  with a mocked real provider response, webhook rejection on invalid
  signature, webhook marking `"paid"` only on a real verified event,
  `checkout.session.expired` correctly marking `"canceled"` (never
  `"paid"`), idempotent replay handling, unknown-session no-op, and
  unhandled-event-type no-op.
- Full backend suite: `python -m pytest tests/ -q
  --ignore=tests/backend_test.py` — **462 passed** (up from 446 before
  this pass), zero regressions.
- `python -m flake8 .` — clean.
- Route registration verified: `GET/POST /api/payments/checkout`,
  `/api/payments/mine`, `/api/payments/webhook/stripe` all present on
  the real FastAPI app (`server.py` imports cleanly with the new
  router mounted).

## What remains open (disclosed, not hidden)

1. **No live Stripe account** — this sandbox has no real
  `STRIPE_SECRET_KEY`/`STRIPE_WEBHOOK_SECRET`. Every code path that
  needs them is real and correct against Stripe's public
  documentation, but has not been exercised against a live account.
  The moment real credentials are supplied (env vars only — no code
  change), `is_provider_configured()` flips true and the full
  checkout→webhook→paid chain becomes live.
2. **No consumption of a `"paid"` `PaymentRecord`** — this pass closes
  the payment runtime itself; it does not yet wire a confirmed payment
  to granting cohort/access-level effects (e.g. unlocking a paid
  formation). `commerce/models.py`'s `NO_FAKE_PAID_STATE` gate already
  forbids inventing such an effect without a real design decision on
  what "paid" should unlock per offer — that decision is real,
  disclosed follow-on scope, not attempted here.
3. **No refund/dispute handling** — `charge.refunded`/
  `charge.dispute.created` events are real Stripe event types this
  webhook handler does not yet process (only
  `checkout.session.completed`/`.expired`); the `"refunded"` status
  exists on the model but nothing sets it yet.
4. **No admin/finance reconciliation surface** — `GET /payments/mine`
  is the only read endpoint; a staff-facing "all payments" or
  reconciliation view is not built.
