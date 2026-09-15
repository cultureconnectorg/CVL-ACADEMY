# RECONCILE-3 Runtime Report — "Does the reconstructed union actually run as ONE CVLN Academy system?"

Branch: `reconcile/canonical-main-r35l31-20260914`. Status legend used
throughout: **VERIFIED** (real evidence — a test that ran, a server that
booted, a request that returned the expected body), **PARTIAL** (some
real evidence, an honest gap remains), **BLOCKED** (cannot be proven in
this sandbox, reason stated), **FAILED** (real defect found). Nothing
below is marked DONE without the evidence that backs it.

## 0. Freeze integrity

| Branch | SHA | Status |
|---|---|---|
| `origin/main` | `c5dddc83ee09a6ec6fb8fd5e9cfda1ec917ac048` | **VERIFIED** unchanged — matches `RECONCILE_MAIN_R35L31_FREEZE.md`'s recorded freeze SHA exactly (re-fetched from origin this session) |
| `origin/claude/cvln-academy-production-r35l31` | `f9763b6e27b7f60f29577a4a26bac2710596dfc3` | **VERIFIED** unchanged — matches the recorded freeze SHA exactly |
| No branch deleted | — | **VERIFIED** — only `reconcile/canonical-main-r35l31-20260914` was pushed to this session |
| No merge to `main` | — | **VERIFIED** — every commit this session went to the reconcile branch only |

## 1. Backend boot — production contract (Phase 1, OPS-01)

**VERIFIED.** OPS-01 (BUG_PRODUCT found in RECONCILE-2 Groupe 5) is
closed: `server.py`'s `lifespan()` had lost r35l31's original fail-closed
contract during an earlier CORS-focused reconciliation pass —
`ensure_indexes()` and the PG-13 architecture-reuse manifest lock were
inside the best-effort seed `try/except`, so an index-creation failure
or a manifest-lock failure logged an error but let the app boot and
serve traffic anyway. Fixed: both calls moved outside the try/except,
`manifest.get("status") != "LOCKED"` now raises `RuntimeError`, which
FastAPI's lifespan protocol turns into a genuine ASGI
`lifespan.startup.failed` event (the server never accepts connections).

Regression suite `backend/tests/test_server_startup_and_cors.py` (13
tests, all real — a `_FakeSessionManager` substitutes the two module-level
MCP session managers so multiple real boot cycles can run in one process,
otherwise identical to a real boot):

| Scenario (Founder's list) | Test | Result |
|---|---|---|
| Startup normal | `test_startup_normal_boots_ready_with_real_indexes_and_manifest` | VERIFIED |
| DB indisponible | `test_startup_db_unavailable_refuses_to_boot` | VERIFIED (raises, never accepts traffic) |
| Index creation failure | `test_startup_index_creation_failure_refuses_to_boot` | VERIFIED |
| PG-13 manifest not locked | `test_startup_manifest_not_locked_refuses_to_boot` | VERIFIED |
| Configuration production | `test_startup_in_production_configuration_still_fails_closed`, `test_production_with_real_allowlist_boots_fine`, `test_production_with_wildcard_cors_refuses_to_boot`, `test_production_with_unset_cors_refuses_to_boot` | VERIFIED |
| Configuration développement/test | `test_startup_in_development_configuration_still_fails_closed`, `test_development_default_stays_wildcard` | VERIFIED |
| Shutdown | `test_shutdown_closes_db_client_and_stops_mcp_session_managers` | VERIFIED |
| Restart | `test_restart_boots_cleanly_a_second_time` | VERIFIED |
| Seed failure ≠ startup failure (documented, narrower, main's own pre-existing contract) | `test_startup_survives_seed_failures` | VERIFIED (app boots, `startup_ready=False`, `startup_error` populated, `/health/live` still 200 — matches r35l31's original narrower intent) |

## 2. Route & capability wiring (Phase 2)

**VERIFIED**, structurally and at runtime.

- Route inventory built from `app.openapi()` (FastAPI 0.141's
  `_IncludedRouter` wrapper means `app.routes` no longer flattens
  sub-routers the old way — `openapi()` is the reliable source): **514
  real HTTP operations** across the mounted API.
- Router-completeness check: all **82** modules `api/__init__.py`
  imports by name have a non-empty `.router.routes` — **0 missing
  attribute, 0 zero-route modules**, 507 summed router routes + 2
  ungated `public_router`s (professional_profile,
  governance_advanced) = matches the 514 total. Directly answers
  "aucun module ne doit être considéré récupéré uniquement parce que son
  fichier existe": every one of the 53 r35l31-recovered routers has real,
  non-empty routes wired into the live app object, not just an importable
  file.
- Gating structure (`api/__init__.py`): `health`/`auth`/`legal` ungated
  (must be, since the legal gate itself depends on auth);
  `professional_profile.public_router`/`governance_advanced.public_router`
  explicitly, documentedly ungated (real per-route auth inside instead);
  every other business router gated with `Depends(require_legal_acceptance)`;
  `learning` additionally gated with `Depends(require_commercial_learning_access)`.
  One pre-existing, still-open `NEEDS_REVIEW` (not touched, a monetization
  decision, documented in the file itself): whether `canonical`/
  `frk_canonical`/`kor_canonical`/`klt_canonical` should also carry the
  commercial gate.

Per-capability SOURCE→ROUTER→AUTH→SERVICE→DB→FRONTEND→TEST, spot-verified
this session (each row backed by a real runtime call, a real DB
collection read from `infra_indexes.py`, and a real frontend consumer
found by `grep`):

| Capability | Router prefix | Auth/gate | DB collection(s) | Frontend consumer | Runtime proof |
|---|---|---|---|---|---|
| Auth | `/auth` | ungated (issues the tokens everything else needs) | `users`, `refresh_tokens` | `lib/auth.jsx` | VERIFIED — Phase 3 journeys |
| Legal/privacy | `/legal` | ungated | `legal_acceptances` | `pages/LegalAcceptance.jsx` | VERIFIED — 428 refusal + real accept flow, Phase 3 |
| Onboarding | `/onboarding` | `require_legal_acceptance` (+ auth, via that dependency chain) | `users`, `frek_signals`, `user_badges` | `pages/Onboarding.js` | VERIFIED — Phase 3 + backend_test.py |
| Formations | `/formations` | public read (discovery), gated detail-progress paths | `formations` | `pages/Formations.js`, `pages/FormationDetail.js` | VERIFIED |
| Missions | `/missions` | `require_legal_acceptance` | `missions`, `user_missions` | `pages/Missions.js` | VERIFIED |
| Badges | `/badges` | bare catalogue ungated, `/mine` gated | `badges`, `user_badges` | `pages/Badges.js` | VERIFIED (this session's own fixture-crash finding, see §6) |
| Wallet | `/wallet` | `require_legal_acceptance` | `wallet_accounts`, `wallet_transactions` | `pages/Wallet.js` | VERIFIED — real balance read, Phase 3 |
| Commerce (catalogue) | `/commerce` | public read, staff-only internal | none (static catalogue) | `pages/Offers.js` | VERIFIED |
| Commercial (order→wallet→entitlement) | `/commercial` | `require_legal_acceptance` | `commercial_orders`, `academy_entitlements`, `billing_documents` | `components/CommercialPurchaseCard.jsx`, `BillingInvoicePanel.jsx` | VERIFIED, see §5 + `COMMERCE_CONVERGENCE_DECISION.md` |
| Payments (Stripe) | `/payments` | `require_legal_acceptance` | `payments`, `payment_checkout_sessions` | **none found** | PARTIAL — real, tested backend, zero frontend wiring (documented, see §5) |
| Certifications | `/certification` | `require_legal_acceptance` | `certification_attempts`, `certification_rubrics` | `pages/Certifications.js`, `CertificationGradeForm.js` | VERIFIED |
| Professional profiles | `/professional/profile` | public read + auth-scoped write, real per-route checks | (professional profile collections) | `pages/FrekProfile.js`, `pages/ProfessionalPublicProfile.js` | VERIFIED — Phase 3 (visibility toggle, permission boundary) |
| Canonical progress | `/canonical`, `/frk_canonical`, `/kor_canonical`, `/klt_canonical` | `require_legal_acceptance` (NEEDS_REVIEW re: commercial gate, undecided) | canonical-domain collections | `lib/canonicalApi.js`, `lib/canonicalKltApi.js`, `App.js` | VERIFIED wired; commercial-gate question open |
| Physical sessions | `/physical-sessions` (r35l31-recovered) | `require_legal_acceptance` | physical-session collections | `components/PhysicalSessionsPanel.js`, `pages/trainer/TrainerDashboard.js` | VERIFIED wired |
| FMS/FREK/KORA/Kiltikonet | multiple routers under the canonical/domain families above | as above | domain-specific | `App.js` route tree | VERIFIED — real content, not stub, per the corpus-deepening work already logged in this engagement's history |
| GMD/CVE/AGF | **not routers** | — | `seed_data.py`'s `poles` catalogue (`{"code": "GMD", ...}`) | formation/pole filters | Clarified, not a wiring gap — these are catalogue domain codes (career poles), not separate API surfaces |
| Admin / production-gates | `/production-gates` | staff-only (`require_role`) | governance/gate collections | `pages/AdminDashboard.js` | VERIFIED — Phase 3 admin journey (403 for non-admin, 200 for admin) |

## 3. User journeys (Phase 3)

**VERIFIED** — `backend/tests/test_reconcile3_user_journeys.py`, 11/11
passing, real end-to-end HTTP calls through the real FastAPI app (no
bypass of auth/legal/business logic), MOCK_DB in-memory Motor-compatible
store, real full-corpus seed.

| Journey | Steps proven | Result |
|---|---|---|
| VISITEUR | landing→formations list (public)→formation detail (public, no auth)→deep link direct to a formation with zero prior navigation | VERIFIED |
| APPRENANT | register→428 on a gated route pre-acceptance→real `/legal/accept`→missions open→onboarding options+complete (real field contract: `metier_vise`/`territoire`/`objectif_perso`)→dashboard-equivalent (progression summary + learning path)→formation→module→badges (real list)→wallet (`/wallet/me`, real `jcc_balance`/`token_balance` shape) | VERIFIED |
| RETOUR UTILISATEUR | independent second login issues an independent token, first token stays valid (real multi-session, not single-session-only)→`/frek/profile`'s real `is_returning_session()` threshold contract proven both ways: `False` immediately after signup (guards against a same-burst false positive), `True` once the account's `created_at` crosses the real 1-day `RETURNING_THRESHOLD` | VERIFIED |
| PRO/EXPERT | own professional profile read, visibility toggle (real permission-scoped write), professional-reserved route (`/production-gates`) correctly refuses a plain student (403) | VERIFIED |
| ADMIN | plain user refused `/orgs` and `/production-gates` (403 each), real server-side admin role provisioning, admin then allowed both (200 each) | VERIFIED |
| Refresh / deep link / logout / expired-invalid token / 401 vs 403 / feature flags | real refresh-token rotation (old token rejected after use), unauthenticated deep link resolves normally, logout revokes the refresh token, structurally-invalid and expired-signed tokens both 401, no-credentials request 401 vs wrong-role request 403 with a real `detail` body, and the backend-has-no-spatial-notion invariant proven directly (identical unflagged data returned regardless of any "spatial mode" framing — the ON/OFF split lives entirely in the frontend, see §4) | VERIFIED |

Two real, wrong assumptions found and fixed while building this proof
(both documented in the test file and the commit that fixed them,
not silently patched over): the real `/onboarding/complete` schema uses
`metier_vise`/`objectif_perso` (not `metier`), and the real
`/wallet/me` shape is `{"account": {"jcc_balance", "token_balance", ...}}`
(not a bare `cc_credits`/`balance` field) — both were guessed wrong on
the first pass, caught by the tests actually failing against the real
API, then corrected to match the real contract rather than the test's
prior assumption.

## 4. Spatial runtime (Phase 4)

**PARTIAL.**

- Backend invariant: **VERIFIED** (see Phase 3 above) — the backend has
  no notion of "spatial mode" at all; `SPATIAL_HUB_ENABLED` and its
  sibling flags are frontend-only (`frontend/src/lib/featureFlags.js`),
  confirmed by making the identical backend call and getting identical,
  unflagged real data back regardless.
- Frontend/E2E spatial runtime: this session ran the **full** Playwright
  suite together for the first time (159 specs — previously each wave
  only ever verified its own new specs in isolation). Result: **117
  passed, 34 failed, 8 skipped** on the first full run. Confirmed via a
  serial (`--workers=1`) re-run of the 34 failures that this is **not**
  CI-load flakiness (every failure reproduced identically) — it is real
  test debt from specs that were never run together before. Root-caused
  and fixed one directly (`badges.spec.js`, see §6) proving the method;
  delegated systematic root-causing of the remaining specs (the ones
  most relevant to spatial runtime: `spatial-camera-follow.spec.js`,
  `spatial-context-environment.spec.js`, `spatial-module-dock.spec.js`,
  `spatial-roadmap-rail.spec.js`, `environmental-continuity.spec.js`,
  `route-transition.spec.js`, plus the non-spatial
  `mobile-nav.spec.js`/`page-route-wiring.spec.js`/
  `module-journey-context.spec.js`/`module-journey-navigation.spec.js`/
  `scroll-restoration.spec.js`/`billing-invoice.spec.js`/
  `commercial-purchase.spec.js`/`ecosystem-builder.spec.js`) — **this
  work was still in progress in the background when this report was
  written; see the addendum this report will carry once that lands, or
  the live PR/branch state for the final count.**
- What this proves today with real evidence: Dashboard, Roadmap,
  ModuleJourney and the badges spatial depth cards do genuinely mount,
  fetch real (mocked-backend) data, and render — 117 of 159 specs pass,
  spanning reduced-motion, keyboard focus, formation discovery, mentor
  presence, module-journey context transitions, and more. What remains
  **unverified as of this writing**: the specific WebGL available/
  unavailable fallback, audio ON/OFF calibration, and camera-follow
  specs that are among the 34 (or were, before the in-progress fix work)
  — their real pass/fail state is not yet confirmed green.
- No simultaneous CSS/WebGL duplication was found in any file read this
  session; the architecture's own flag-gated single-path design
  (`FEATURE_FLAGS.SPATIAL_HUB_ENABLED`) is unchanged from prior phases.

## 5. Wallet / payment / commerce integrity (Phase 5)

**VERIFIED** for what exists and is tested; **explicitly not unified**
per the Founder's instruction.

- Real, passing test evidence (915 tests, run against MOCK_DB this
  session): `test_academy_wallet.py`, `test_cvln_wallet_integration.py`,
  `test_commercial_wallet_policy.py`, `test_commercial_wallet_runtime.py`,
  `test_wallet_and_badges_atomicity.py` (wallet creation/balance/ledger
  effects/idempotency, cross-user isolation, reconciliation),
  `test_certification_eligibility.py`/`test_certification_scoring.py`
  (certification→JCC path), `test_payments.py` (payment success/failure,
  duplicate webhook-event idempotency, signature verification),
  `test_commerce_catalog.py`, `test_economy_3d_traceability.py`.
- `docs/reconciliation/COMMERCE_CONVERGENCE_DECISION.md` (written this
  session): documents the three real, currently-coexisting commerce
  surfaces — `/commerce` (read-only DECIDED_V1 catalogue), `/commercial`
  (Economy-3D→CVLN-Wallet→entitlement→invoice, the only one wired to a
  real purchase UI today), `/payments` (Stripe/EUR, real and tested but
  zero frontend consumers and — verified by reading the code — never
  grants an entitlement on a successful payment). Lays out
  OVERLAP/DIFFERENCES/SHARED_PRIMITIVES/CONFLICTS and four
  TARGET_OPTIONS. **No code unified, no implicit product decision made**,
  per instruction.
- Honest caveat: all of the above runs against MOCK_DB
  (`mongomock_motor`, an in-memory Motor-API-compatible store), not real
  MongoDB — real index/uniqueness semantics under true concurrent load
  are not proven by this. Real MongoDB was not reachable in this sandbox
  (see §8).

## 6. Test debt classification (Phase 6)

| Suite | Before this session | After this session | Classification |
|---|---|---|---|
| `backend_test.py` (51 tests) | ENVIRONMENT (no real running server/DB reachable) | **51/51 VERIFIED passing** — booted the real server for real (uvicorn + MOCK_DB) and ran it as real HTTP integration tests | Reclassified from ENVIRONMENT to closed. Two real root causes found and fixed: (1) every registration fixture predated the real legal-acceptance gate — added the real `/legal/accept` flow to all 6 registration paths; (2) 5 tests called routes that a documented, already-completed P0 security fix (AUTH-01, "public quiz + sweep all routes for public-learning leakage") made auth-required — added auth headers. TEST_OBSOLETE, fixed for real, not skipped. |
| `test_reconcile3_user_journeys.py` (new, 11 tests) | — | VERIFIED, 11/11 | New this session |
| `test_server_startup_and_cors.py` (13 tests) | — | VERIFIED, 13/13 | New/rewritten this session (OPS-01) |
| Financial-integrity suites (915 tests total across 10 files) | — | VERIFIED, 915/915 | Confirmed green this session |
| `badges.spec.js` (e2e) | FAILED (4/4) | VERIFIED, 4/4 | FIXTURE_BROKEN — `auth-fixture.js` mocked `/api/badges/mine` but not the bare `/api/badges` catalogue route, so it fell through to a generic `{}` fallback and crashed `Badges.js` at `all.findIndex(...)`. Root-caused with a probe script (`page.on("pageerror")`), fixed by adding the missing mock with real `seed_data.py` badge codes and replacing the spec's invented `B10`/`B50` test-ids (which never existed) with the real ones (`BADGE-PARCOURS-10`, `BADGE-MISSION-FIRST`). |
| Remaining 30 e2e specs (of the original 34 failures) | FAILED | **in progress at time of writing** (delegated, same probe-script method, results not yet folded into this report — see §4) | To be finalized once that work lands |
| Docker/MongoDB-dependent paths (real index/transaction semantics under real Mongo) | ENVIRONMENT | still ENVIRONMENT | Confirmed again this session: both `production.cloudfront.docker.com` and `fastdl.mongodb.org` are blocked by explicit org network policy (403 CONNECT, `connect_rejected`) — not retriable per the proxy's own instructions. No real MongoDB was available to replay these against. |

No real failure was converted to a skip to reach a higher pass rate
anywhere in this session.

## 7. Environment limitations

- No real MongoDB or Docker daemon reachable in this sandbox (org
  network policy blocks both registries). Every "real DB" proof in this
  report is against `mongomock_motor`'s in-memory, Motor-API-compatible
  store (`MOCK_DB=1`) — genuine proof of real routing, auth, and business
  logic execution; **not** proof of real MongoDB-engine-level correctness
  (true index/uniqueness enforcement under concurrent writes, real
  transaction semantics).
- The Playwright e2e suite is itself fully mocked by design
  (`playwright.config.js`) — no real backend, no real Mongo, real CRA
  dev server driving real React components against Playwright
  `page.route()` mocks. This is a legitimate, documented, pre-existing
  design choice (see `playwright.config.js`'s own module comment), not a
  gap introduced this session.

## 8. Remaining blockers at time of writing

1. **Phase 4 e2e completion**: 30 of the original 34 failing e2e specs
   were still being root-caused (via the same probe-script method
   demonstrated on `badges.spec.js`) when this report was drafted. Their
   final classification (FIXTURE_BROKEN/TEST_OBSOLETE fixed, or
   BUG_PRODUCT documented for review) is not yet folded in.
2. **`/payments` (Stripe/EUR) frontend wiring**: real, tested backend
   with zero UI entry point and a real gap (no entitlement grant on
   success) — Founder decision needed per
   `COMMERCE_CONVERGENCE_DECISION.md`'s `FOUNDER_DECISION_REQUIRED` §4.
3. **Commerce architecture convergence itself**: deliberately left
   undecided per instruction — see `COMMERCE_CONVERGENCE_DECISION.md`'s
   four `TARGET_OPTIONS`.
4. **`canonical`/`frk_canonical`/`kor_canonical`/`klt_canonical` commercial
   gate**: pre-existing, still-open `NEEDS_REVIEW` in `api/__init__.py`
   (a monetization decision, not touched this session).
5. **Real MongoDB-engine-level verification**: cannot be performed in
   this sandbox (network policy). Should be replayed against a real
   MongoDB before final production canonicalization.

## Exit criteria checklist

| Criterion | Status |
|---|---|
| Backend boot production contract vérifié | VERIFIED |
| OPS-01 fermé | VERIFIED |
| Frontend build vert | VERIFIED (prior sessions; unchanged this session — no frontend product files touched except `auth-fixture.js`/`badges.spec.js` test infra) |
| Backend imports verts | VERIFIED |
| Routes runtime inventoriées | VERIFIED (514 operations, 0 dead routers) |
| Capacités critiques câblées | VERIFIED (table in §2) |
| Auth réel fonctionnel | VERIFIED |
| Post-auth fonctionnel | VERIFIED |
| Parcours apprenant fonctionnel | VERIFIED |
| Permissions vérifiées | VERIFIED |
| SpatialHub réellement exécuté | PARTIAL (117/159 e2e green as of writing, remainder in progress) |
| Wallet/idempotency vérifiés | VERIFIED (against MOCK_DB, not real Mongo) |
| Index DB vérifiés sur vraie DB lorsque disponible | BLOCKED — real MongoDB not reachable in this sandbox |
| Toutes les non-vertes classifiées | PARTIAL — backend fully classified and closed; e2e classification in progress |
| Aucune régression critique connue | VERIFIED (no product-code regression found; test-debt findings were pre-existing, not introduced) |
| `main` inchangé | VERIFIED |
| R35L31 inchangé | VERIFIED |

**Not yet at 100% green.** Per instruction: no merge to `main` yet, no
branch deleted. Presenting this report and the blockers above before any
canonicalization decision.
