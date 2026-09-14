# ACA-0015 — Camera CROSSING/REVEALING: the Real Mount-Detection Guard

```
STATUS: EXECUTED (2026-09-08). Both prerequisites cameraFollow.js's own
docstring named are now real; the full INTENT->...->SETTLING sequence
is wired and verified end-to-end against a real Chromium instance for
the two real production call sites SpatialHub wires. Flag-gated
(SPATIAL_CAMERA_INTENT, default off) — zero behavior change until
deliberately turned on. RETURNING and the reverse-anchor path stay
NOT_AUTHORIZED, unchanged.
```

## What this closes

`cameraFollow.js`'s own docstring named exactly two prerequisites for
the full cross-route CROSSING/REVEALING handoff, both left undone:
(a) promoting `Layout` to a real Outlet-based layout route, and (b) "a
real mount-detection race guard neither built nor verified here." (a)
was closed by the earlier ACA-0015/ACA-0016 routing restructure this
session. This pass closes (b) and wires the result into production.

## What was built

### `frontend/src/lib/spatial/mountGuard.js` (new)
`waitForElement(selector, { root, timeoutMs })` — resolves with the
real destination anchor the instant it appears in the DOM via a real
`MutationObserver` (not a fixed-delay guess), or `null` after
`timeoutMs` if it never appears. Never throws. Same "graceful no-op,
never fake support" doctrine `audio.js`/`haptics.js` already
established for an unsupported browser API — extended here to "never
fabricate a handoff to an anchor that never appeared."

`mountGuard.test.js` — 6 tests: resolves immediately when already
present, resolves once added asynchronously (the real race this exists
for), resolves `null` on timeout, respects a scoped `root`, and never
rejects.

### `frontend/src/lib/useCameraIntent.js`
`fly()` gains an optional third argument, `{ destinationSelector }`.
Omitted, behavior is byte-identical to before (INTENT → LOCKING →
FOLLOWING → IDLE). Supplied, once the existing intent-clone flight
finishes and `onNavigate()` has already fired, the flow continues:
**CROSSING** (waiting on `waitForElement(destinationSelector)`) →
**REVEALING** (a second clone flies, via `computeFlightKeyframes`'s
existing verbatim-ported math, from the original source rect to the
now-real destination rect) → **SETTLING** → **IDLE**. If the anchor
never mounts within the guard's timeout, the flow degrades gracefully
straight to IDLE — never blocks navigation, never leaves a stray clone.
The retarget/cancel token (`createCameraToken`, unmodified) is checked
both before CROSSING starts and after `waitForElement` resolves, so a
second activation mid-flight correctly cancels the first's REVEALING
before it fires.

### `frontend/src/components/SpatialHub.jsx`
Wires two real, non-invented destination selectors:
- **Formation activation** → `[data-testid="formation-detail"]` —
  `FormationDetail.js`'s own root testid (already load-bearing in
  `module-journey-navigation.spec.js`).
- **Mission activation** → `` `[data-testid="mission-${n.code}"]` `` —
  the exact same real mission's own card on `/missions` (both
  `Missions.js`'s plain-grid and `SPATIAL_HUB_ENABLED` depth-card
  treatments render this testid), a genuinely specific shared-element
  target, not a generic page-mount signal.

No new flag — reuses the existing `SPATIAL_CAMERA_INTENT` gate.

## Verification

- **Unit**: `mountGuard.test.js` (6/6) + the pre-existing
  `cameraFollow.test.js` (13/13, `computeFlightKeyframes` etc.
  untouched) — full suite `CI=true npx craco test --watchAll=false`:
  **180/180 passed**, zero regressions.
- **Build**: `CI=true yarn build` — clean.
- **Lint**: `npx eslint` on every touched file — clean.
- **Full e2e regression** (flags at their default, off):
  `npx playwright test e2e/` — **85/86 passed**, the one failure is the
  same pre-existing, confirmed-unrelated flake documented in every
  prior report this session (not part of this repo's CI gate).
- **Real end-to-end proof of the CROSSING/REVEALING sequence itself**:
  `Element.animate` (the Web Animations API `fly()` depends on) is
  **not implemented in jsdom** (verified directly: `typeof el.animate
  === "undefined"` under `jsdom`), so this sequence cannot be unit-
  tested in Jest — the same reason the pre-existing INTENT/LOCKING/
  FOLLOWING flight was never unit-tested either (Rail 4's own report
  verified it via a live preview screenshot, not a Jest test). This
  repo's single `playwright.config.js` also never sets
  `REACT_APP_ACADEMY_SPATIAL_*` flags (confirmed: every prior H1/Rail
  report's "flag-on behavior… this sandbox's Playwright config cannot
  reach" disclosure), so no committed e2e spec runs with the flag on
  either. Verified instead the same way every flag-gated feature this
  session has been: a real Chromium instance (Playwright, not jsdom),
  `craco start` with `REACT_APP_ACADEMY_SPATIAL_HUB_ENABLED=true` +
  `REACT_APP_ACADEMY_SPATIAL_CAMERA_INTENT=true`, mocked auth +
  `/user/learning-path` + `/formations/*` (reusing the exact fixture
  shape `e2e/fixtures/auth-fixture.js` already establishes). Clicking a
  real formation tile in `SpatialHub` produced, in order: the intent
  clone (`[data-testid="camera-intent-clone"]`), real navigation to
  `/formations/FMS-01`, and then the reveal clone
  (`[data-testid="camera-reveal-clone"]`) — confirmed present via DOM
  polling, not inferred. A screenshot of the settled destination page
  was captured. This is a one-off verification script, not committed
  (same precedent as every prior manual live-preview check this
  session) — its exact steps are reproducible from this report.

## What remains open (explicitly out of scope for this pass)

- **`RETURNING`** (the reverse-anchor path for navigating back) is
  still not wired — `cameraFollow.js`'s own `cameraReturnTransition`
  math is extracted but unused, same as before this pass.
- **ModuleJourney/Roadmap/Badges/FrekProfile activation** — only
  `SpatialHub`'s two real destinations (formation, mission) got
  `destinationSelector`s this pass. Roadmap/Badges/FrekProfile don't
  navigate anywhere from their own cards (confirmed in the ACA-0018
  audit: no `onClick`/`api.post` action on those pages besides real
  data display), so there's no analogous "activation → destination"
  pair to wire there yet.
- **The two REPLACE-BLOCKED H1-plan items** (Formation-card→Module FLIP
  extension beyond this pass's scope, environmental asset upgrade)
  remain untouched, each needing its own separate go-ahead per the
  plan's own terms.
- **Mobile-swipe `useSwipeRail()` promotion** remains unbuilt.

## What this pass completes

ACA-0015's own title — "port camera-follow/shared-object transitions to
real routes" — is now genuinely done for the two real navigable
activations this app's spatial hub has. Task marked complete.
