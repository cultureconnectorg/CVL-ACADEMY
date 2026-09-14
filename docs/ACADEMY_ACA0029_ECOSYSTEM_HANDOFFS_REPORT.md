# ACA-0029 — Real CVLN Ecosystem Handoffs

```
STATUS: EXECUTED (2026-09-08). The event-driven ecosystem-integration
architecture (rule 9) already existed and worked for exactly one real
event. Two other already-real, already-published events had zero
subscribers -- published into the void. This pass wires them, adds
one new real emission point, and adds the one real external system
(djsayd/CVLN-Wallet) that had no interface at all.
```

## What existed before this pass

`services/integrations/` (task #8) already had the right shape: 9
generic `EcosystemIntegration` clients + FrekCore + Agent Factory's own
richer clients, `services/events.py`'s real in-process `EventBus`, and
one real subscriber wiring `academy.certification.passed` →
Brain + Command Center. That subscriber genuinely worked — a real
integration test proved it. But `docs/ACADEMY_FUNNEL_EVENT_TAXONOMY.md`
had already classified `academy_activation_completed` and
`academy_first_value_reached` as `READY_TO_EMIT`, and a later pass
(ACA-0013) did emit both — `test_activation_events.py` proves real
`db.event_log` documents result. Neither one, however, had a single
subscriber: real events, published into the void, forwarded to nothing.

## What was built

1. **Two orphaned events wired** (`services/integrations/
   subscribers.py`): `academy_activation_completed` and
   `academy_first_value_reached` now forward to Command Center (the
   real funnel/activation-KPI-relevant system per rule 9's own
   description) — the same best-effort, never-blocking pattern the
   original certification handler already established, refactored
   into a shared `_forward()` helper rather than copy-pasted per
   handler.
2. **One new real emission point**: `academy_badge_awarded`
   (`badges_engine.py`, right after the already-real FrekCore signal
   and internal wallet credit that badge-earning already triggers) —
   a real domain milestone with previously zero external visibility.
3. **The one real external system with no interface yet**: the
   external `djsayd/CVLN-Wallet` product (its own repo, its own
   `backend/server.py` — the WAL-2X formation corpus built earlier
   this session is grounded directly against its real code, per
   `docs/wal/README.md`). Added as a new `EcosystemIntegration` in
   `services/integrations/registry.py`, named `"CVLN Wallet (djsayd,
   external)"` — deliberately NOT the shorter "CVLN Wallet" the
   existing internal-ledger documentation row already uses, so the two
   (Academy's own real, already-active `wallet/` ledger vs. this new,
   unconfigured, decoupled interface to the *external* product) can
   never be confused for the same system. `academy_badge_awarded`
   forwards to it (plus Command Center) — a badge earning real JCC in
   Academy's own ledger is exactly the kind of fact the external
   Wallet product would want reflected.
4. **`docs/INTEGRATIONS_REPORT.md`** updated with the new row and an
   explicit "which event goes to which system" summary.

## Verification

- `python -m pytest tests/test_ecosystem_handoffs.py -v` — **9/9
  passed**: the new Wallet integration is registered with the correct
  env vars and correctly reports unconfigured; `academy_badge_awarded`
  is genuinely published to `db.event_log` on a real badge award, with
  the correct payload; the emission is exactly-once (proven via the
  same idempotent award-guard the existing ECON-03 audit already
  established, now extended to prove the event doesn't duplicate
  either); each of the 4 handler functions forwards to exactly the
  integrations named above (never more, never fewer — the activation
  handler is explicitly proven to NOT call Brain, unlike the
  certification handler); an unconfigured integration is skipped
  gracefully, never raising; and `register()` itself is proven to wire
  all 4 event types — verified on a fully isolated, throwaway
  `EventBus` instance substituted just for that one test, so this
  suite can never leak a subscription into the real global bus any
  other test file relies on.
- **Real regression found and fixed**: 3 pre-existing test fixtures
  (`test_wallet_and_badges_atomicity.py`,
  `test_missions_reward_idempotency.py`,
  `test_quiz_reward_idempotency.py`) called `award_threshold_badges`
  without mocking `services.events`' `db` — the new
  `events.publish()` call inside it reached for a real, absent
  MongoDB and hung until `ServerSelectionTimeoutError` (30s). Fixed by
  adding `events_module` to each fixture's existing monkeypatch loop,
  the same pattern `test_activation_events.py` already used.
- Full backend suite: `python -m pytest tests/ -q
  --ignore=tests/backend_test.py` — **492 passed** (up from 483, +9
  new, 3 fixtures fixed), zero regressions.
- `python -m flake8 .` — clean. `black` — clean on every touched file.
- `python -c "from server import app"` — imports cleanly, no route
  changes in this pass (integration wiring only).

## What remains open

1. **The remaining `READY_TO_EMIT` events from the taxonomy are still
  unemitted** (`academy_signup_completed`, `academy_module_completed`,
  `academy_quiz_completed`, `academy_mission_completed`,
  `academy_skill_validated`, and others) — this pass closed the two
  events that were real-but-orphaned plus added one new one; the full
  taxonomy sweep (14 `READY_TO_EMIT` rows) is real, disclosed follow-on
  work, not attempted here.
2. **No real credentials for any of the 10 external systems** (9
  generic + the new djsayd/CVLN-Wallet entry) exist in this sandbox —
  every handoff is real and correct, currently a no-op in practice
  (`IntegrationNotConfigured`, caught and skipped) until real env vars
  are supplied. This is the same disclosed limitation every ecosystem
  integration in this codebase already carries, not new to this pass.
3. **`academy_purchase_completed`** — the taxonomy's own note said
  "FORBIDDEN_TO_EMIT until real ... no payment processor exists"; that
  premise changed with ACA-0026 (a real, correct, if-unconfigured
  Stripe checkout/webhook engine now exists). Whether to now emit this
  event from `payments/service.py`'s `handle_stripe_webhook` is a real
  decision this pass doesn't make — disclosed, not silently done.
