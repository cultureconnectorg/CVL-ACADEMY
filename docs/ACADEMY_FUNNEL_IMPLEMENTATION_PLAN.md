# CVLN Academy — Funnel Implementation Plan (W-FUNNEL-0)

```
This is the proposed wave plan. NONE of these waves are authorized by
this document. Per mission §45, only W-FUNNEL-0 (this audit) executes
now; W-FUNNEL-1 begins only after explicit Founder authorization.
```

## Sequencing rationale

Waves follow the funnel's own order, front-loading the stages with the
strongest existing backend (lowest domain risk) and pushing the
genuinely unbuilt layer (Monetization) and the highest-uncertainty one
(Ecosystem) toward the end, exactly as the mission's own §38 lays out.
Each wave's exit criteria (tests + evidence + rollback + clean tree)
gates the next — no wave starts early.

## W-FUNNEL-1 — Lifecycle model + event taxonomy + spatial shell architecture

**Goal**: infrastructure only, no visible product change yet.

**Files that would change**:
- New: `frontend/src/lib/spatial/physics.js` (extracted `makeRailPhysics`, substepped, H0.10-verified constants)
- New: `frontend/src/lib/spatial/attention.js` (`attentionTier`/`applyDepth`, 6-channel occlusion)
- New: `frontend/src/lib/spatial/topology.js` (`TRANSITION_TOPOLOGY` lookup)
- New: `frontend/src/lib/spatial/cadence.js` (input cadence classifier + focus prediction)
- New: `frontend/src/lib/spatial/audio.js`, `frontend/src/lib/spatial/haptics.js` (ported controllers, same event names as H0.10 + this taxonomy's naming reconciliation)
- New: `frontend/src/lib/spatial/framePacing.js`
- New: `frontend/src/lib/lifecycleState.js` (pure functions implementing `ACADEMY_LIFECYCLE_STATE_MODEL.md`'s derivation rules, given a `User` + related documents already fetched by existing endpoints — no new backend calls required for the states that are derivable today)
- New (backend, additive): `academy_returned` needs `User.last_login_at: Optional[str] = None` on `models.py` + a one-line update on `GET /auth/me` or a login-time write — the only schema change in this wave, purely additive, defaults `None`, breaks nothing existing.
- Extend (not replace): `frontend/src/lib/RouteTransition.jsx` — accept an optional Camera Anchor Contract per route pair, default behavior (today's crossfade) unchanged when none is defined.
- Config: whatever the repo's real config mechanism is (`.env` / feature-flag pattern already used for `FREK_CORE_BASE_URL`-style vars) — add `ACADEMY_SPATIAL_SHELL`, `ACADEMY_CAMERA_FOLLOW`, `ACADEMY_PHYSICS`, `ACADEMY_ENVIRONMENT`, `ACADEMY_SPATIAL_AUDIO`, `ACADEMY_HAPTICS`, `ACADEMY_LIFECYCLE_ENGINE`, `ACADEMY_CONTINUATION_ENGINE`, `ACADEMY_EXPANSION_ENGINE` as env-driven flags, same pattern as existing integration toggles — no parallel config system invented.

**Tests**: unit tests for `physics.js` against the exact node-simulation method that caught H0.10's substep bug (reversal, fast-nav, worst-case-dt stability) — ported, not re-invented. Unit tests for `lifecycleState.js` against fixture user/progress documents.

**Rollback**: every new module is inert until imported; flags default `false`. Deleting the new files or leaving flags off fully reverts.

## W-FUNNEL-2 — Landing → Signup → Onboarding → Activation → First Value

**Goal**: the pre-Hub journey gets real spatial treatment on its already-real backend contracts.

**Files**: `Landing.js`, `Onboarding.js`, a new `Activation.js` view (or a modal/reveal state on Onboarding's own completion — TBD at design time, not this document's call), `Layout.js` (mount the persistent backdrop, gated by `ACADEMY_SPATIAL_SHELL`).

**Product decision required before this wave, not a code decision**: whether/how to expose a public, unauthenticated formation preview (the Discovery gap, gap-matrix row 1) — this needs Founder input, not an engineering default.

**Tests**: extend `landing-spatial.spec.js`; new onboarding/activation specs — constrained by this sandbox's no-backend limitation (disclosed in the audit), so full auth-flow assertions need a real test backend, not just this environment.

**Rollback**: `ACADEMY_SPATIAL_SHELL=false` reverts every touched page to its current, unchanged render path (additive components, not rewritten ones).

## W-FUNNEL-3 — Hub → Formation → Roadmap → Module

**Goal**: Dashboard becomes the "Personal Academy Hub" (mission §12); Formation/Roadmap/Module get H0.10's camera-follow/attention/occlusion extracted in, at HIGH intensity, without touching their already-strong, already-tested behavior underneath.

**Files**: `Dashboard.js` (primary restructure — currently untouched by any prior spatial wave), `Formations.js`, `Roadmap.js`, `ModuleJourney.js` (additive spatial layer only — W3-A/B/D/E's real state machine and tests are the floor, not the target of change).

**Tests**: existing `formations-discovery.spec.js`, `roadmap-progression.spec.js`, 3× `module-journey-*.spec.js` must stay green throughout — this is the regression floor, checked after every commit in this wave, not just at the end.

**Rollback**: `ACADEMY_SPATIAL_SHELL`/`ACADEMY_CAMERA_FOLLOW` off → current, already-good behavior (per the audit, this is the strongest existing surface — highest care, lowest tolerance for regression).

## W-FUNNEL-4 — Quiz → Mission → Mentor → Proof

**Goal**: LOW/MEDIUM-intensity context planes for Quiz/Mission (currently presumed standard modals — verify first), preserve Mentor exactly as-is (already meets the mission's own bar), and give Skills/Badges/Certification/FrekProfile their "professional evidence, not trophy room" treatment.

**Files**: quiz/mission dock components (wherever `ModuleJourney.js`'s context surfaces live — not fully inventoried this pass, verify at wave start), `Skills.js`, `Badges.js`, `Certifications.js`, `FrekProfile.js`.

**Tests**: `mentor-presence.spec.js` must stay green unmodified (Mentor is preserve-only this wave); new specs for Skills/Badges/Certifications (none exist today).

## W-FUNNEL-5 — Monetization layer (interface-only)

**Goal**: commercial *states* (FREE/AVAILABLE/PAID/LOCKED/ELIGIBLE/OWNED/SUBSCRIBED) computed from real `FormationEconomics` data and a real (but transaction-less) entitlement model; UI communicates WHAT/WHY/PRICE/RIGHTS/DURATION/ACCESS/CANCELLATION per the mission's own requirement; **no payment processor integrated in this wave** — every "Buy"/"Subscribe" action ends in a clearly-labeled `BLOCKED_EXTERNAL` state, never a fake success.

**Files (backend, additive)**: new `backend/api/commerce.py` exposing entitlement *reads* only (derived from `FormationEconomics` + a new, empty-by-default `Entitlement` collection nothing writes to yet except manually via admin), new `models.py` additions (additive fields, not migrations).

**Explicit non-goal**: do not integrate Stripe or any processor speculatively. If/when the Founder selects one, that's a distinct, explicitly-authorized follow-up wave — not assumed here.

**Rollback**: `ACADEMY_LIFECYCLE_ENGINE`/commerce flag off — the entire surface disappears, existing Wallet/Formation pages unaffected (additive routes only).

## W-FUNNEL-6 — Retention / Return / Continuation Engine

**Goal**: `RETURN_TO_POSITION` (route/formation/module/focusedObject/rail-offset/scroll/camera-origin — H0.8's own Focus Memory pattern, extracted), surfaced "Continue where you were" using the already-real `next_action`.

**Files**: a new `frontend/src/lib/returnPosition.js` (localStorage-backed, per-user-scoped, same conservative pattern as the existing token/lang storage — not a new architecture), `Dashboard.js` wiring.

**Tests**: new specs asserting a route/scroll/focus round-trip after navigating away and back — extends the existing `RETURN_POSITION_PRESERVED` assertion pattern already proven in W3-B/W3-C/W3-E (URL/role preservation), now adding the *felt* half W4-C flagged missing.

## W-FUNNEL-7 — Expansion + real ecosystem handoffs

**Goal**: the `LOCKED/FAR → ELIGIBLE → HORIZON → NEXT` reveal moment on real unlock-state changes; ecosystem circulation UI that **only ever shows a system as available when `GET /integrations` (already real) reports it configured** — never a static "connected to 11 systems" claim.

**Files**: new expansion-reveal component wired to `learning-path`'s existing unlock data; an ecosystem-status surface (likely Admin-only initially, extending existing `GET /integrations` consumption) before ever exposing it to learners.

## W-FUNNEL-8 — Full mobile/a11y/performance/regression

**Goal**: independent mobile design (not desktop compression, per mission §28) across every wave's surfaces; full accessibility pass; real frame-pacing/performance measurement on real hardware (closing this session's own disclosed sandbox-only limitation); full regression across every existing E2E spec plus every new one added in W-FUNNEL-1..7.

## Cross-cutting rule for every wave

No wave begins until the previous one has: passing tests (old + new),
committed evidence (screenshots/traces as established in the H0.x
report lineage), a working rollback path (flag off = prior behavior),
and a clean `git status --porcelain`. This mirrors exactly the
discipline already used across every H0.x/W1–W4 wave in this repo's own
history — not a new process invented for this mission.
