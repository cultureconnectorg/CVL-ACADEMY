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

**VERIFIED, with 2 real product defects surfaced and documented (not fixed).**

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
  test debt from specs that were never run together before.
- Every one of the 34 failures was root-caused for real (probe-script
  method: `page.on("pageerror")`/`page.on("response")` plus reading the
  real frontend component and backend contract each spec drives — never
  guessed). **9 specs were genuine FIXTURE_BROKEN/TEST_OBSOLETE issues**
  in the e2e test infrastructure itself and are now fixed and verified
  green: `badges.spec.js`, `ecosystem-builder.spec.js`,
  `billing-invoice.spec.js`, `commercial-purchase.spec.js`,
  `page-route-wiring.spec.js`, `module-journey-context.spec.js`,
  `environmental-continuity.spec.js` (partially — see below),
  `route-transition.spec.js`, `module-journey-navigation.spec.js` (the
  last two turned out to share root causes with the fixes above).
- **The remaining 15-16 failures (varies by run — see below) are real,
  pre-existing product defects, not test debt**, each documented with an
  exact repro rather than papered over:
  1. **WebGL background swap loses its DOM contract** — the single
     largest cluster (7 test failures: `spatial-camera-follow.spec.js`
     ×1, `spatial-context-environment.spec.js` ×3,
     `spatial-module-dock.spec.js` ×2, `spatial-roadmap-rail.spec.js` ×1).
     `SpatialWorldFrame.jsx` renders `SpatialWebGLBackground` instead of
     `SpatialBackground` whenever WebGL is eligible (the default in this
     headless-Chromium environment). `SpatialWebGLBackground.jsx` uses a
     different `data-testid` (`spatial-webgl-background` vs
     `spatial-background`) and never mirrors
     `data-spatial-context`/`data-spatial-motion`/
     `data-spatial-module-phase` onto the DOM the way the CSS variant
     does — even though its internal engine does receive the underlying
     signals. `SpatialModuleEnvironmentBridge.jsx`'s imperative
     `document.querySelector('[data-testid="spatial-background"]')`
     silently no-ops against the WebGL variant. **This is precisely the
     kind of WebGL-path gap the Founder asked Phase 4 to prove or
     disprove — and it disproves clean WebGL/CSS parity today.**
  2. **Layout's claimed Outlet-based promotion was never actually done**
     (2 failures in `environmental-continuity.spec.js`). Both this
     spec's own docstring and `RouteTransition.jsx`'s docstring claim
     ACA-0015/ACA-0016 promoted `Layout` to a real Outlet-based
     `LayoutRoute` so it survives in-section navigation without
     remounting. **No `LayoutRoute`/`Outlet` exists anywhere in `App.js`**
     (grep-verified, 0 matches). `/dashboard` renders via `<Protected>`
     while `/roadmap`/`/frek-profile` render via `<PublicOrMember>` — a
     different component type at the same tree position — so React
     remounts the whole `Layout` subtree (sidebar, `AcademyBackdrop`,
     mentor dock) on that navigation, non-deterministically (~40-60% of
     repeated runs, confirmed by direct instrumentation). `Layout.js`'s
     own inline comment already half-admits the promotion was deferred.
  3. **Scroll-position key-corruption race** (1 failure,
     `scroll-restoration.spec.js`). `useScrollRestoration.js`'s
     save/restore effects both key off `location.key`; on a dashboard→
     formations navigation, the DOM content swap triggers a native
     browser scroll-clamp event that fires *before* the old-route
     listener's cleanup has run, so the still-attached old listener
     captures the clamp and overwrites the just-saved real position
     (e.g. 260) with 0 — a deterministic, 100%-reproducible corruption,
     not a flake, verified via direct `Map.prototype.set/get`
     instrumentation showing the exact overwrite sequence.
  4. **The ACA-0022 mobile bottom-tab-bar/"More" sheet feature was never
     built** (6 failures, all of `mobile-nav.spec.js`). Only the i18n
     strings exist (`mobile_nav_more`/`mobile_nav_close` in
     `lib/i18n.jsx`); grep for `mobile-nav`/`MobileNav`/`BottomNav`
     across `frontend/src` returns 0 matches. `Layout.js` only ever
     renders the desktop sidebar, shrunk by CSS on mobile, never
     replaced by the claimed bottom nav.
- Final suite state after this session's fixes:
  **135-136 passed / 15-16 failed / 8 skipped** (the 1-test variance is
  finding 2 above's own documented ~40-60% non-determinism — it is not
  a new flake, it *is* the defect). Every remaining red is a classified,
  documented, real product finding — none is unexplained test debt.
- What this proves with real evidence: Dashboard, Roadmap, ModuleJourney,
  the badges spatial depth cards, formation discovery, mentor presence,
  module-journey context transitions, reduced-motion handling, and
  keyboard focus all genuinely mount, fetch real (mocked-backend) data,
  and render correctly — the large majority of the spatial and
  non-spatial surface. The 4 defects above are the genuine gaps, not
  assumed clean until proven otherwise.
- No simultaneous CSS/WebGL duplication was found — the architecture's
  flag-gated single-path design is real, but finding 1 above shows the
  WebGL path's DOM observability contract diverges from the CSS path's,
  which is itself a real defect worth the Founder's attention alongside
  the architecture being otherwise sound.

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
| `ecosystem-builder.spec.js`, `billing-invoice.spec.js`, `commercial-purchase.spec.js`, `page-route-wiring.spec.js`, `module-journey-context.spec.js`, `route-transition.spec.js`, `module-journey-navigation.spec.js`, `environmental-continuity.spec.js` (1 of 3 tests) | FAILED (24 tests total) | VERIFIED, all now green | FIXTURE_BROKEN, all real and distinct: missing `/ecosystem-builder/me` mock (crashed on `{}.portfolio.length`); missing `physical-sessions`/`physical-locations`/`certifications` mocks unconditionally fetched by `PhysicalSessionsPanel` on every formation-detail page, crashing the whole page (explains 3 specs at once); missing `/trainer` and `/admin` canonical-formation-list mocks; a real sub-20ms animation-settle race in two REDUCED_MOTION assertions (single-shot `evaluate()` read vs. an in-flight opacity transition — fixed with `expect.poll(...)`, matching this suite's existing pattern elsewhere); missing `/professional/profile/mine` mock (crashed `FrekProfile.js`); a real render-timing race in the spec itself (`page.goto` resolves on `load`, not on React's lazy Suspense chunk finishing). Each fix verified re-running its file alone (2-5x for timing-sensitive ones), committed with the real root cause explained, pushed. |
| Remaining 15-16 e2e failures (of the original 34) | FAILED | **Correctly left red** — real product defects, not test debt | Reclassified BUG_PRODUCT, documented not fixed (product changes need review): (1) WebGL background swap loses its DOM contract vs the CSS variant — 7 tests across `spatial-camera-follow`/`spatial-context-environment`/`spatial-module-dock`/`spatial-roadmap-rail`; (2) Layout's claimed Outlet-based promotion (ACA-0015/ACA-0016) was never actually built — 2 tests in `environmental-continuity.spec.js`, ~40-60% non-deterministic remount; (3) a real scroll-position key-corruption race in `useScrollRestoration.js` — 1 test; (4) the ACA-0022 mobile bottom-nav feature was never built at all, only its i18n strings exist — 6 tests in `mobile-nav.spec.js`. Full repro detail for each in §4. |
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

## 8. Remaining blockers

1. **4 real frontend product defects found by Phase 4's e2e completion**
   (full detail in §4, none fixed here per instruction that product
   fixes need review — only test infrastructure was touched this
   session):
   - WebGL spatial background's DOM contract diverges from the CSS
     variant (`SpatialWebGLBackground.jsx` vs `SpatialBackground.jsx`) —
     affects camera-follow, context-environment, module-dock, and
     roadmap-rail specs under reduced motion / WebGL-eligible paths.
   - `Layout`'s claimed Outlet-based promotion (ACA-0015/ACA-0016) was
     never actually implemented — `Layout` remounts non-deterministically
     on certain in-section navigations.
   - A real key-corruption race in `useScrollRestoration.js` silently
     overwrites a saved scroll position with 0 on some navigations.
   - The ACA-0022 mobile bottom-nav/"More" sheet feature does not exist
     in the codebase — only its i18n strings were ever added.
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
| Frontend build vert | VERIFIED (re-confirmed this session with `npx craco build` after the test-infra changes) |
| Backend imports verts | VERIFIED |
| Routes runtime inventoriées | VERIFIED (514 operations, 0 dead routers) |
| Capacités critiques câblées | VERIFIED (table in §2) |
| Auth réel fonctionnel | VERIFIED |
| Post-auth fonctionnel | VERIFIED |
| Parcours apprenant fonctionnel | VERIFIED |
| Permissions vérifiées | VERIFIED |
| SpatialHub réellement exécuté | VERIFIED (135-136/159 e2e green; the remainder are 4 classified, documented real product defects — see §4/§8, not unverified surface) |
| Wallet/idempotency vérifiés | VERIFIED (against MOCK_DB, not real Mongo) |
| Index DB vérifiés sur vraie DB lorsque disponible | BLOCKED — real MongoDB not reachable in this sandbox |
| Toutes les non-vertes classifiées | VERIFIED — every backend and e2e non-green this session is classified (FIXTURE_BROKEN/TEST_OBSOLETE fixed, or BUG_PRODUCT/ENVIRONMENT documented); none left unexplained |
| Aucune régression critique connue | VERIFIED (no product-code regression found; all 4 BUG_PRODUCT findings are pre-existing gaps this session discovered, not introduced) |
| `main` inchangé | VERIFIED |
| R35L31 inchangé | VERIFIED |

**Not at 100% green, by design — 4 real product defects remain, correctly
red rather than papered over.** Per instruction: no merge to `main`, no
branch deleted. Presenting this report and the blockers above before any
canonicalization decision.
