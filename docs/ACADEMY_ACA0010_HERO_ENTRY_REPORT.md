# ACA-0010 — Hero/Entry Sequencing, Implementation Report

```
STATUS: implemented, flag-gated OFF by default
(REACT_APP_ACADEMY_SPATIAL_HERO_ENTRY). Landing.js renders exactly
today's production behavior until this flag is deliberately turned on
— same discipline as every other spatial flag in this repo.
```

## What this closes

`docs/ACADEMY_HERO_ENTRY_RESEARCH.md` (design research only, no code)
identified one concrete, `PARTIAL`-graded gap in
`ACADEMY_CURRENT_FUNNEL_AUDIT.md` stage 01: Landing's manifesto and
auth card render **simultaneously at full visual weight**, with no
temporal sequence at all — the opposite of every sourced reference's
own "world before identity" mechanism (Universal's globe-before-
wordmark, PS5's context-overlay, Spotify's ranked "now" slot).

This closes that gap for the acceptance criterion that is actually
testable in this sandbox (research §16.1 — "zero simultaneous
full-weight elements at t=0") without the full persistent-backdrop/
cross-route continuity work the research scopes separately (§10-11,
which depends on ACA-0014/ACA-0016 — the spatial engine's H1
production mount, still `NOT_AUTHORIZED`).

## What was built

`frontend/src/pages/Landing.js`:

- `useHeroStage()` — a `VOID → WORLD → FOCUS → IDENTITY` state machine,
  compressed from the research's illustrative 0-60s cinematic
  storyboard to a real, usable ~800ms sequence (a visitor is never
  blocked from acting — research §16.3's "time-to-first-real-content"
  criterion, applied conservatively).
- Manifesto (brand line, headline, tagline) reveals at `WORLD`; the
  stade-chip row reveals at `FOCUS`; the auth card reveals at
  `IDENTITY` — using the existing `Reveal` primitive
  (`lib/motion-primitives.jsx`, already MOT-029 reduced-motion-safe).
- `alreadyPlayedThisSession()` / `markPlayed()` — a `sessionStorage`
  best-effort so a returning visitor within the same tab/session lands
  on the settled end-state immediately (research §16.4), never
  replaying the sequence. Not the full `RETURN_TO_POSITION` mechanism
  (that's ACA-0023, authenticated-route scope) — Landing itself carries
  no "position."
- `HeroStage` — renders the real `Reveal` primitive only while a
  sequence is actually running; otherwise a plain passthrough `<div>`
  with the identical className. This is the mechanism that keeps the
  "off" path byte-identical to pre-change Landing: no entrance-fade
  overhead, no DOM structure change, when the flag is disabled (the
  default), reduced motion is on, or the session already played it.
- New flag: `FEATURE_FLAGS.SPATIAL_HERO_ENTRY`
  (`REACT_APP_ACADEMY_SPATIAL_HERO_ENTRY`), documented in
  `frontend/.env.example`, off by default like every flag before it.

## What was deliberately not built here

- The persistent cross-route backdrop (Hero → Signup → Onboarding →
  Activation, research §10) — depends on promoting `Layout` to a
  router layout route, already flagged as a separate, larger
  restructure by `AcademyBackdrop.jsx`'s own docstring (RAIL3-05).
- Camera Anchor Contract on the register/login transition (research
  §8.5, "ENTRY") — `cameraFollow.js` exists (Rail 4) but is scoped to
  same-page `SpatialHub` activation only; wiring it into Landing's
  auth-card commit is ACA-0011/ACA-0015 territory, not this task.
- Any visual/asset design (light field, botanical layer specific to
  Landing) — the research explicitly forbids literal genre-visual
  borrowing (§5-6) and this pass adds none.

## Verification

- `CI=true yarn build` — compiled successfully, zero new warnings.
- `npx eslint src/pages/Landing.js src/lib/featureFlags.js` — clean.
- Full relevant Playwright suite (31 tests: `landing-spatial`,
  `reduced-motion`, `route-transition`, `routing`, `auth-guards`,
  `keyboard-focus`) — **31/31 passed**, flag at its default (off),
  proving the "off" path is unchanged: auth form usability, keyboard
  flow, reduced-motion equivalence, and routing all unaffected.
- The flag-on path (actual VOID→WORLD→FOCUS→IDENTITY sequence) is not
  covered by a new e2e test in this pass — same convention as every
  other spatial flag in this repo (RAIL3/RAIL4/RAIL5 reports), which
  build and reason about the "on" behavior without flipping it on in
  this sandbox's single playwright webServer config (no backend, no
  flag matrix). A future wave enabling `SPATIAL_HERO_ENTRY` in a real
  environment should add a dedicated `hero-entry.spec.js` asserting
  the acceptance criteria in research §16 against real timing.

## Never claim

This is not `FULLY_COMPLETE` Hero/Entry — it is the one gap from the
research this pass could close safely and testably. ACA-0011 (Identity/
FREK-ID as contextual transition), ACA-0012 (Onboarding spatialization),
ACA-0016 (environmental continuity), and the flag's own eventual
production activation all remain open, separate backlog items.
