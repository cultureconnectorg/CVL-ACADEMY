# CVLN Academy ↔ CVLN Wallet — Commercial Runtime

Status: **BACKEND VERIFIED / ACTIVATION GATED**

## Verified chain

`Economy 3D → server-side offer → commercial order → CVLN Wallet entity API → paid order → Academy entitlement → learning access gate`

The commercial runtime never trusts a client-supplied price. Pricing is resolved from the canonical Economy 3D projection and snapshotted on the order before any Wallet call.

## Current directly sellable Economy class

- `PUBLIC_MARKET` path: canonical `€990 path / subscription` is interpreted as an exact **€990 path** purchase.
- Subscription is intentionally refused until a concrete canonical subscription-plan mapping is available.
- `CROSS_ECOSYSTEM_PROGRAM`: quote required.
- `INTERNAL_NOT_FOR_SALE`: never sellable.
- `BUNDLED_BRIDGE`: eligibility required.
- `HOLD_FROM_SALE`: never sellable.

This is Human Authority by design: missing commercial decisions are not invented by code.

## CVLN Wallet contract consumed

Academy uses the real `djsayd/CVLN-Wallet` entity API, not the legacy internal Academy wallet:

- `GET /api/v1/entity/me`
- `POST /api/v1/entity/charge`
- authentication: `X-API-Key`

The Wallet runtime rate is read before order creation and snapshotted on the Academy order. The Wallet owns financial value movement and ledger truth. Academy owns pricing, order and entitlement state.

## Safety boundary

The current Wallet `entity/charge` endpoint does not expose an entity-scoped idempotency-key contract. Academy therefore:

1. atomically claims an order before calling Wallet;
2. never automatically retries a timeout/network-ambiguous charge;
3. moves ambiguous outcomes to `REQUIRES_REVIEW`;
4. never grants entitlement without a confirmed Wallet response;
5. returns an already `PAID` order without charging again.

A future Wallet-side idempotency contract should replace the ambiguity review boundary, not bypass it.

## Activation variables

```env
CVLN_WALLET_URL=
CVLN_WALLET_API_KEY=
CVLN_WALLET_TIMEOUT_SECONDS=10
ACADEMY_COMMERCIAL_ENTITLEMENTS_ENFORCED=false
```

`ACADEMY_COMMERCIAL_ENTITLEMENTS_ENFORCED` stays false until the deployed Wallet URL/API key are configured and an environment-level integration test is green. When enabled, PUBLIC_MARKET learning routes without an ACTIVE entitlement return `402 COMMERCIAL_ENTITLEMENT_REQUIRED`.

## CI proof

Workflow: `.github/workflows/commercial-wallet-ci.yml`

Verified gates:

- Black
- Isort (`--profile black`)
- Flake8
- Mypy
- commercial policy tests
- order/Wallet/entitlement runtime tests
- 812 Economy 3D source-line regression
- existing backend regression

## Still not FULL LIVE

The backend transaction chain is verified, but production activation still requires:

- deployment secrets for the real Wallet entity;
- Wallet-side entity charge idempotency improvement;
- frontend offer/order/payment UX;
- environment-level live/sandbox integration verification;
- richer canonical mappings for subscriptions, B2B/B2G, financing and other decided Economy 3D offer classes.
