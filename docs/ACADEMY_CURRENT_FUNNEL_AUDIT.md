# CVLN Academy — Current Funnel Audit (W-FUNNEL-0)

```
MODE = AUDIT_ONLY. No product code changed to produce this document.
Every claim below is grounded in a specific file/line/route/collection
read this session — see "Evidence" per stage. Where I did not verify a
claim directly, it is marked UNVERIFIED, not asserted.
STOP_AFTER_DELIVERY = TRUE. H1 = NOT_AUTHORIZED.
```

## Method

For each of the 27 stages in the mission brief, I read the actual route
table (`frontend/src/App.js`), the actual page component, the actual
backend router (`backend/api/*.py`), the actual Pydantic models
(`backend/models.py`, `backend/wallet/models.py`, `backend/skills/models.py`,
`backend/certification/models.py`), and the actual MongoDB collections
touched (grepped directly, not inferred). Where a prior audit already
verified a claim with equal or better rigor (W0, W4-A/B/C, `INTEGRATIONS_
REPORT.md`, `AUDIT_REPORT.md`), I cite it instead of re-deriving it —
the underlying evidence doesn't get weaker for being reused, and
re-deriving it here would not make it more true.

**Status legend** (per the mission's own definitions): `EXISTS` — real,
working end-to-end · `PARTIAL` — real but incomplete in a named way ·
`MISSING` — no code path produces this today · `BLOCKED_EXTERNAL` — real
interface exists, blocked on credentials/infra Academy doesn't control ·
`PROTOTYPE_ONLY` — exists only in the `spatial-console-h0*.html`
scratchpad lineage, never reached `frontend/src`.

---

## 01 — Discovery / Landing

- **Status**: `PARTIAL`
- **Route**: `/` (`frontend/src/App.js:54`), unauthenticated, public.
- **Component**: `frontend/src/pages/Landing.js` (191 lines).
- **Backend**: none required to view it.
- **State source**: none (static manifesto + inline auth card).
- **Entry point**: any unauthenticated visit; also the `*` catch-all
  redirects any unknown/invalid route back here.
- **Exit point**: register or login (inline on the same page, see stage 02).
- **Next action**: pick register/login mode; no other CTA exists.
- **Missing transition**: **formation discovery is not reachable while
  unauthenticated** — `/formations` is wrapped in `<Protected>`
  (`App.js:58`), so the mission's own Level-0 requirement ("Surfaces:
  ... formation discovery where public") is not met. A visitor cannot
  see a single formation, price, or outcome before creating an account.
  This is the single largest Discovery-stage gap.
- **Spatial coverage**: `W2-B` (`docs/SPATIAL_LEARNING_W2B_LANDING_REPORT.md`)
  deliberately used only 2 of 5 authorized primitives (`FOCUS` on the
  active language pill, `ENTER` on the register/login mode swap) —
  intensity is genuinely LOW today, not the MEDIUM/HIGH the new mission
  targets. `W4-C` independently classifies `UNIVERSE_BEFORE_INTERFACE`
  as `PARTIAL` here: DOM order puts the manifesto first, but nothing
  establishes it *temporally* — both render simultaneously, equal
  visual weight.
- **Mobile coverage**: manifesto stacks above the auth card (confirmed
  by DOM order, W4-C) — not independently verified visually this session.
- **Reduced-motion coverage**: `EXISTS` app-wide (`prefers-reduced-
  motion` respected by the shared motion primitives per W1-A) — not
  Landing-specific risk.
- **Tests**: `frontend/e2e/landing-spatial.spec.js` — real, exercises
  the two W2-B primitives.
- **Risk**: MEDIUM. Gating discovery behind signup is a real conversion
  risk (the mission explicitly forbids "force registration before
  sufficient understanding," §Level 0), and fixing it means either
  un-protecting a read-only `/formations` view or building a distinct
  public preview — a product decision, not just a spatial one.

## 02 — Registration

- **Status**: `EXISTS`
- **Route**: same as Landing (`/`, `mode="register"`), no dedicated route.
- **Component**: `Landing.js` (inline form), calls `useAuth().register`.
- **Backend**: `POST /api/auth/register` (`backend/api/auth.py:95`).
- **State source**: `db.users` (insert), `frek_core.mint_frek_id()`
  assigns a real sequential FREK-ID via `db.counters`.
- **Entry point**: Landing, mode=register.
- **Exit point**: on success, `AuthResponse{token, refresh_token, user}`
  — frontend then routes to `/onboarding` (unverified this session which
  component makes that decision; `Protected`'s own redirect rule,
  `App.js:41`, would send any authenticated-but-`onboarding_completed=
  false` user there regardless).
- **Next action**: onboarding.
- **Missing transition**: none identified — accepts an `invite_code`
  (org/cohort invitation, real: `_apply_invitation`), issues a real JWT
  + refresh token pair.
- **Spatial coverage**: same LOW intensity as Landing (same page, same
  W2-B tranche); `ENTER` fires on the register/login swap.
- **Mobile coverage**: UNVERIFIED this session (no dedicated mobile
  audit of the form itself).
- **Reduced-motion coverage**: inherits Landing's.
- **Tests**: no dedicated E2E for a real register→onboarding round-trip
  in this sandbox — `playwright.config.js`'s own header comment
  discloses **no MongoDB/backend is available here**, so authenticated
  flows (register, login, anything past the auth guard) are not
  E2E-verified in this environment, only unauthenticated
  routing/guard/keyboard/reduced-motion behavior is.
- **Risk**: LOW (backend logic is real and typed) / MEDIUM (untested
  end-to-end in this sandbox — disclosed, not hidden).

## 03 — Authentication

- **Status**: `EXISTS` (core) / `BLOCKED_EXTERNAL` (OAuth) / `PARTIAL` (2FA UI)
- **Backend**: `POST /login`, `/refresh`, `/logout`, `GET /me`,
  `/forgot-password`, `/reset-password`, `/resend-verification`,
  `/verify-email`, `GET /oauth/providers`, `/oauth/{provider}/start`,
  `/2fa/enroll`, `/2fa/verify` — all real, typed endpoints
  (`backend/api/auth.py`, 12 routes).
- **State source**: `db.users`, `db.refresh_tokens`, `db.password_
  resets`, `db.email_verifications`.
- **OAuth**: real endpoint surface, reports "not configured" until
  `OAUTH_{PROVIDER}_CLIENT_ID` env vars are set (`_provider_env_
  configured`) — correctly `BLOCKED_EXTERNAL`, not faked.
- **2FA**: enroll/verify endpoints exist and are wired to real
  `totp_secret`/`totp_enabled` fields on `User`; no frontend surface
  found for it in `pages/` — `PARTIAL` (backend `EXISTS`, frontend
  `MISSING`).
- **Missing transition**: password reset / email verification have real
  backend token issuance (`issue_password_reset_token`, `issue_email_
  verification_token`) but delivery goes through `services/
  notifications.py` — not independently verified this session whether
  that's a real transport or a logging fallback; treat as UNVERIFIED,
  check before claiming email delivery works.
- **Tests**: `frontend/e2e/auth-guards.spec.js` — real, covers the
  unauthenticated-routing half only (see stage 02's test note).
- **Risk**: LOW for the core email/password path; MEDIUM for the
  unverified notification-delivery claim.

## 04 — Identity / FREK-ID

- **Status**: `EXISTS`
- **Backend**: `frek_id` is a real field on every `User`, minted by
  `frek_core.mint_frek_id()` at registration; `GET /frek/profile`
  (`backend/api/progression.py:24`) returns identity + `stade_progress_
  pct` + `signals` + `recent_signals` (from `db.frek_signals`).
- **Frontend**: `frontend/src/pages/FrekProfile.js` at `/frek-profile`.
- **State source**: `db.users.frek_id`, `db.frek_signals`.
- **Missing transition**: none found — this is one of the most
  genuinely real, non-decorative concepts in the whole product; not a
  spatial idea invented for this mission, an actual identity primitive
  that predates it.
- **Spatial coverage**: not evaluated this session; no prior report
  scored `FrekProfile.js` specifically.
- **Tests**: none found dedicated to `/frek-profile`.
- **Risk**: LOW.

## 05 — Onboarding

- **Status**: `EXISTS`
- **Route**: `/onboarding`, unauthenticated-reachable route but the
  page itself requires a logged-in user (uses `useAuth()`).
- **Component**: `frontend/src/pages/Onboarding.js` (375 lines).
- **Backend**: `GET /onboarding/options` (langs/métiers/territoires),
  `POST /onboarding/complete` (`backend/api/onboarding.py`).
- **State source**: `db.users` (`lang`, `metier_vise`, `territoire`,
  `objectif_perso`, `onboarding_completed`), `db.poles`.
- **Real inputs used** (exactly the ones the mission names as
  pre-existing and reusable): language (4 real options: fr/en/kr/es),
  métier/profession (real `db.poles` lookup), territoire (7 real
  options incl. Martinique/Guadeloupe/Guyane/France/Caraïbe/Diaspora),
  objectif personnel (free text, 3–240 chars).
- **Next action**: activation (see stage 07) — `onboarding_complete`
  directly produces `recommended_formation` + `recommended_mission` +
  `badge_earned` + `signals_emitted` in one response.
- **Missing transition**: no "world constructs around you" spatial
  treatment (§10 of the mission) — this is currently a standard
  multi-field form, `PARTIAL` on the mission's own experiential ask
  even though the *data* half is fully real.
- **Tests**: none found dedicated to Onboarding's own flow (only
  downstream auth-guard tests reference the `/onboarding` redirect).
- **Risk**: LOW (data model) / the spatial upgrade is pure UX work on a
  real, stable backend contract — low domain risk.

## 06 — Orientation

- **Status**: `EXISTS` (as part of Onboarding — no separate stage in
  the current product)
- Same routes/backend as stage 05. The mission's "Orientation" (Level 2)
  and "Onboarding" are the same real flow here — not a gap, just a
  naming difference between the mission's target model and the current
  implementation's single combined step.

## 07 — Activation

- **Status**: `EXISTS`, and unusually strong
- **Backend**: `onboarding_complete` (`backend/api/onboarding.py:45`) —
  in one transaction: validates pole/lang/territoire, persists
  onboarding data, emits **3 real `FREK-TIME` signals** (language/
  territory/objective), auto-awards `BADGE-DECOUVERTE` via `award_
  threshold_badges`, computes a **real** recommended formation (matches
  the chosen pole, prefers one with modules), computes and
  **auto-accepts** a real first mission (`db.user_missions` insert,
  `status="accepted"`, `source="onboarding"`), emits a `FREK-MISSION`
  signal.
- **State source**: `db.users`, `db.frek_signals`, `db.badges`,
  `db.user_badges`, `db.formations`, `db.missions`, `db.user_missions`.
- **Missing transition**: no dedicated "YOUR CURRENT PATH" convergence
  moment in the frontend (mission §11) — the data is all real and
  already returned in one payload (`OnboardingResult`), but nothing
  currently stages it as a single spatial "FOCUS → APPROACH → CONFIRM →
  HORIZON_RECOMPOSITION" reveal; it likely just renders as a result
  screen or redirects straight to `/dashboard` (component not read line
  by line for its exact render — UNVERIFIED which).
- **Tests**: none found.
- **Risk**: LOW domain risk — the hard part (real backend convergence)
  is already done; this is presentation work on a stable contract.

## 08 — First Value

- **Status**: `PARTIAL`
- The activation payload already answers "what should I do now" via
  `recommended_formation` + `recommended_mission`. What's `MISSING` is
  a distinct, named "first value" moment separate from activation
  itself — today activation and first-value read as the same event.
  Not necessarily wrong (the mission's levels aren't required to be
  temporally distinct), but not separately instrumented or measured
  either (see stage 31, event taxonomy).
- **Risk**: LOW — this is a framing/measurement gap, not a missing
  capability.

## 09 — Dashboard / Return

- **Status**: `EXISTS`
- **Route**: `/dashboard`, `Protected`.
- **Component**: `frontend/src/pages/Dashboard.js` (231 lines).
- **Backend calls** (read directly from the component, `Dashboard.js:
  26-30`): `GET /frek/profile`, `GET /missions`, `GET /badges/mine`,
  `GET /progression/summary`, `GET /user/learning-path`.
- **`user/learning-path`** (`backend/api/learning.py:257`) already
  computes a real, deterministic **`next_action`** object — walks the
  learner's own pole first, then others, skips locked formations/
  modules (`is_formation_unlocked`/`is_module_unlocked`, real functions,
  not stubs), and returns the first non-validated unlocked module. This
  is precisely the mission's Level-10 "NEXT_BEST_MEANINGFUL_ACTION"
  concept — **it already exists**, deterministically, on real progress
  data. The gap is that nothing in the frontend currently *returns the
  learner to their exact prior spatial position* (route/scroll/rail
  offset/camera) — only this domain-level "what's next," not the felt
  "continue where you were." `W4-C` independently confirms:
  `RETURN_EXACT_CONTEXT`'s functional half is proven, the felt half
  (`DEPTH_MEMORY`) is `MISSING` — no scroll-position memory anywhere in
  the app, confirmed by grep (only `localStorage` usage app-wide is the
  auth token pair and the language preference, `frontend/src/lib/
  api.js`, `i18n.jsx`).
- **Spatial coverage**: not previously scored by any W1–W4 report
  (Dashboard itself was out of scope for those tranches, which focused
  on Landing/Formations/Roadmap/ModuleJourney). Currently a standard
  dashboard-tile layout, not yet a "Personal Academy Hub" per mission §12.
- **Tests**: none found dedicated to Dashboard.
- **Risk**: LOW domain risk (real, stable data underneath); the
  Personal-World spatial upgrade and the RETURN_TO_POSITION mechanism
  are both real, scoped frontend work.

## 10 / 11 — Formation Discovery / Selection

- **Status**: `EXISTS`, but authentication-gated (see stage 01's flag)
- **Routes**: `/formations` (list), `/formations/:code` (detail).
- **Components**: `Formations.js`, `FormationDetail.js`.
- **Backend**: `GET /formations/poles`, `GET /formations`, `GET
  /formations/{code}` (`backend/api/formations.py`).
- **State source**: `db.formations`, `db.poles`.
- **Spatial coverage**: `W2-D` (`SPATIAL_LEARNING_W2D_FORMATION_
  DISCOVERY_REPORT.md`) covers this surface directly — `ONE_DOMINANT_
  FOCUS` scored `PARTIAL` by W4-C (only realized when a card has real
  DOM focus; at rest, N equally-weighted cards, no default focus).
- **Tests**: `frontend/e2e/formations-discovery.spec.js` — real,
  frontend-only (same sandbox limitation as stage 02).
- **Risk**: LOW technically; the public-discovery gap (stage 01) is the
  real product risk here, not the authenticated experience itself.

## 12 / 13 — Learning Path / Module Learning

- **Status**: `EXISTS`, and this is the deepest, most rigorously built
  part of the whole product.
- **Routes**: `/roadmap`, `/formations/:fc/modules/:mc`.
- **Components**: `Roadmap.js`, `ModuleJourney.js`.
- **Backend**: `GET /modules/{formation_code}/{module_code}`, `POST
  .../phase`, `.../deliverable`, `.../mini-mission/commit`
  (`backend/api/learning.py`) — real phase-completion state machine
  (`compute_status`, `phase_completion_flags`), not a stub.
- **State source**: `db.progress` (one doc per user × module).
- **Spatial coverage**: `EXISTS` and independently verified strong —
  `W3-A` (module shell hierarchy), `W3-B` (context entry/return),
  `W3-D` (progression, gamification leak found+removed), `W3-E`
  (authenticated runtime proof). `W4-C`: `DEPTH_IS_SEMANTIC` scored
  fully `REALIZED` here — the one doctrine most rigorously enforced.
- **Tests**: `module-journey-context.spec.js`, `module-journey-
  navigation.spec.js`, `module-journey-hierarchy.spec.js`, `roadmap-
  progression.spec.js` — real, frontend-only (sandbox limitation).
- **Risk**: LOW — this is the strongest, best-tested part of the
  existing product; the mission's instruction to preserve it rather
  than rebuild it is well-founded on the evidence, not just caution.

## 14 — Quiz

- **Status**: `EXISTS`
- **Backend**: `GET /quiz`, `POST /quiz/submit` (`backend/api/
  quizzes.py`) — real scoring (`passed = score >= 0.8`), real `cc_
  credits`/`stade` update on the user, real `frek_core.emit_signal`
  calls (2 distinct signals, read at `quizzes.py:94,103`), real `award_
  threshold_badges` call after a passing score.
- **State source**: `db.users.cc_credits`, `db.progress`, `db.frek_signals`.
- **Risk**: LOW.

## 15 — Mission / Practice

- **Status**: `EXISTS`
- **Backend**: `GET /missions`, `GET /missions/mine`, `POST /{code}/
  accept`, `POST /{code}/submit` (`backend/api/missions.py`).
- **State source**: `db.missions`, `db.user_missions`.
- **Risk**: LOW.

## 16 — Mentor Context

- **Status**: `EXISTS`
- **Backend**: `GET /mentor/agents`, `GET /mentor/session/{id}`, `POST
  /mentor/chat` (`backend/api/mentor.py`) — routed through `services/
  agent_factory.py`'s real Claude Sonnet 5 client (not a stub, not the
  defunct `emergentintegrations`).
- **Spatial coverage**: `W3-C` (`SPATIAL_LEARNING_W3C_MENTOR_
  PRESENCE_REPORT.md`) — contextual, not a permanent floating chatbot
  (the mission's own §14 requirement is already met here).
- **Tests**: `frontend/e2e/mentor-presence.spec.js`.
- **Risk**: LOW.

## 17 — Progression

- **Status**: `EXISTS`
- **Backend**: `GET /frek/profile`, `GET /progression/summary`
  (`backend/api/progression.py`) — real stade-band percentage math,
  real module-completion counts against a real aggregate of all
  formations' module counts.
- **Risk**: LOW.

## 18 — Skills

- **Status**: `EXISTS`
- **Backend**: `GET /skills`, `GET /skills/mine` (`backend/api/
  skills.py`) — backed by `backend/skills/models.py` +
  `backend/skills/progression.py` (a real skill-ID/evidence-registry
  system per `AUDIT_REPORT.md`/`INTEGRATIONS_REPORT.md`, not
  re-verified line-by-line this session but corroborated by the route
  surface and by `db.skills`/`db.skill_evidence`/`db.user_skills`
  collections existing and being written to).
- **Risk**: LOW.

## 19 — Badges

- **Status**: `EXISTS`
- **Backend**: `GET /badges`, `GET /badges/mine` (`backend/api/
  badges.py`); real award logic in `backend/badges_engine.py`
  (threshold-based, triggered from onboarding/quiz).
- **State source**: `db.badges`, `db.user_badges`.
- **Risk**: LOW.

## 20 — Certification

- **Status**: `EXISTS`
- **Backend**: 9 real routes (`backend/api/certification.py`) — rubric
  CRUD, attempt lifecycle (create/submit/grade), a real PDF attestation
  endpoint (`.../attestation.pdf`), backed by `backend/certification/
  {models,scoring,service,attestation}.py`.
- **State source**: `db.certification_rubrics`, `db.certification_
  attempts`.
- **This is the only stage in the entire audit that emits a real,
  generic domain event**: `certification/service.py:139` calls
  `events.publish("academy.certification.passed", ...)` — the in-
  process event bus (`services/events.py`), persisted to `db.event_
  log`, and already best-effort-notifies CVLN Brain/Command Center once
  those are configured (`services/integrations/subscribers.py`, per
  `INTEGRATIONS_REPORT.md`). Every other domain action in this audit
  uses the FREK-signal channel instead (`frek_core.emit_signal`,
  `db.frek_signals`) — a real but *different*, narrower-purpose channel
  (see stage 31).
- **Risk**: LOW.

## 21 — Proof / FREK Profile

- **Status**: `EXISTS` — see stage 04. `skill_evidence`/`user_skills`
  entries and `JurySignature`s carry a real SHA-256 canonical hash over
  their own content (per `INTEGRATIONS_REPORT.md`'s FREKCORE-ready
  section) — real cryptographic proof infrastructure, not a visual
  effect.
- **Risk**: LOW.

## 22 — Wallet

- **Status**: `EXISTS` (internal ledger) / `BLOCKED_EXTERNAL` (Apple/Google passes)
- **Backend**: `GET /wallet/me`, `GET /wallet/transactions`, `GET
  /wallet/pass/apple`, `GET /wallet/pass/google` (`backend/api/
  wallet.py`).
- **State source**: `db.wallet_accounts`, `db.wallet_transactions`
  (append-only ledger — balance is always a sum, never mutated
  directly).
- **Real today**: JCC/token balance per user, transaction history,
  automatic credit on badge-earned (+10 JCC) and certification-passed
  (+50 JCC) — confirmed by `INTEGRATIONS_REPORT.md`, corroborated by
  the `TransactionType` literal in `wallet/models.py` including
  `"badge_earned"`/`"jcc_earned"` alongside `"payment"`.
- **Blocked**: Apple/Google Wallet passes produce correctly-shaped
  *data* but are explicitly returned as `"status": "unsigned"` — no
  Apple Developer WWDR cert, no Google Wallet Issuer account exist for
  CVLN today. Correctly disclosed by the endpoint itself, not faked.
- **Risk**: LOW (internal ledger) / the external pass signing is
  genuinely `BLOCKED_EXTERNAL`, not a code gap.

## 23 — Monetization

- **Status**: `MISSING`
- **Evidence**: grepped `stripe|payment|checkout|billing|subscription|
  invoice|price_id|paywall` across the entire `backend/` tree
  (excluding caches/venv) — the **only** hit is the string `"payment"`
  as one literal value in `wallet/models.py`'s `TransactionType` enum.
  No payment processor client, no checkout endpoint, no subscription
  model, no invoice model exists anywhere in the repository.
- **What does exist, real, that a commercial layer could be built on**:
  `Formation.economics` (`FormationEconomics` model —
  `public_price_eur`, `company_price_eur`, `funding_options`, and
  several internal cost fields) is a real, populated data shape already
  on every `Formation` document — pricing *data* exists; pricing
  *transactions* do not.
- **Risk**: this is the mission's own flagged-in-advance gap
  ("CURRENT REPOSITORY AUDIT SUGGESTS THIS LAYER IS INCOMPLETE") —
  confirmed exactly as suspected. Any commercial-state UI (FREE/
  AVAILABLE/PAID/LOCKED/ELIGIBLE/OWNED/SUBSCRIBED) must be built as
  **interface + state contracts only**, with actual transactions marked
  `BLOCKED_EXTERNAL`, per the mission's own explicit instruction.

## 24 — Retention

- **Status**: `PARTIAL`
- **What's real**: the `next_action` computation (stage 09) is a
  genuine, deterministic continuation-engine seed — real progress,
  real unlock rules, no invented recommendation intelligence.
- **What's missing**: no `RETURN_TO_POSITION` (route/scroll/rail-
  offset/camera restoration — confirmed absent by the `localStorage`
  grep, stage 09); no dedicated "continue where you were" surfaced
  copy; no return-triggered re-fetch/re-surface of `next_action` beyond
  Dashboard's own normal load.
- **Forbidden patterns already avoided** (confirmed by the stade/badge
  model): no streak counters, no countdown timers, no loss-aversion
  copy found anywhere in the audited surfaces — consistent with the
  mission's ethical-growth requirement, this is a genuine strength to
  preserve, not just an absence to fill.
- **Risk**: LOW domain risk, real frontend-state work needed.

## 25 — Expansion

- **Status**: `PARTIAL`
- `user/learning-path`'s `own_pole`/`other_poles` split with real
  `is_unlocked`/`lock_reason` per formation is a real, evidence-based
  "what could open next" seed — no invented cross-sell. What's missing
  is a distinct, contextual "this just became relevant" moment (mission
  §18's `LOCKED/FAR → ELIGIBLE → HORIZON → NEXT` semantic reveal) — the
  data supports it (unlock state changes are real domain events), the
  spatial/product surface for it doesn't exist yet.
- **Risk**: LOW domain risk.

## 26 — Ecosystem Circulation

- **Status**: `PARTIAL` (internal) / `INTERFACE_ONLY` (external, 9 systems)
- Directly corroborated by `docs/INTEGRATIONS_REPORT.md`, re-verified
  this session by reading `services/integrations/registry.py` and
  `services/frek_core.py` directly: 9 generic ecosystem integrations
  (Intelligence OS, Brain, Command Center, Laurent.ia, KORA, Factory
  Maker Studio, Good Mood, Culture Connect, Kiltikonet) are real, typed,
  env-var-gated interfaces — **none configured today**, so **none**
  make a real outbound call; FrekCore and Agent Factory have real local
  fallbacks that are the actual production behavior, not stubs, until
  remote credentials exist. Only one event (`academy.certification.
  passed`) is actually wired to notify Brain/Command Center once
  configured.
- **Risk**: no code risk (every interface fails closed/local, never
  fakes a remote success) — the product risk is that "ecosystem
  circulation" is currently invisible to the learner (no UI surfaces
  any of this), which is arguably correct given nothing is actually
  connected yet.

## 27 — User Ecosystem Development

- **Status**: `MISSING` (as a distinct product surface) / `PARTIAL`
  (as underlying evidence)
- No portfolio/competency-graph/collaboration/project surface exists.
  What's real and reusable as evidence toward it: skills + evidence
  registry (stage 18), certifications + attestations (stage 20), badges
  (stage 19), mission history (`db.user_missions`), Wallet ledger
  (stage 22) — a real, if scattered, evidence base. Building a unified
  "ecosystem builder" surface is new product work, not a rebuild of
  anything existing.
- **Risk**: this is explicitly the mission's own "highest maturity
  level, may be only partially implementable today" — treat as
  `FUTURE_CONTRACT` per §41's classification, not a near-term wave.

---

## Cross-cutting evidence notes

- **Analytics/events**: one real generic event bus (`services/
  events.py`, persisted `db.event_log`) exists and is used exactly
  once in the entire codebase (`academy.certification.passed`).
  Everything else that could be an event today uses the narrower
  FREK-signal channel. See `ACADEMY_FUNNEL_EVENT_TAXONOMY.md` for the
  full only-emit-if-real classification.
- **Testing reality**: the existing E2E suite (11 specs,
  `frontend/e2e/`) is real and well-targeted, but this sandbox has no
  MongoDB/backend process available (`playwright.config.js`'s own
  header comment) — every authenticated journey in this audit is
  therefore `UNVERIFIED end-to-end in this environment`, even where the
  backend code itself is real and correctly typed. This is a sandbox
  limitation, not a claim that the features don't work.
- **Protected pedagogical scope**: no `db.formations`/`db.progress`
  document was mutated, no module code remapped, no FMS corpus
  imported or deleted during this audit — `FMS_CANONICAL_MIGRATION`
  remains untouched, its own separate workstream doc
  (`docs/FMS_CANONICAL_MIGRATION_WORKSTREAM.md`) unchanged.
