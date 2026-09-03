# W5 H0.5 / H0.6 — Spatial Console Upgrade — REPORT

```
STOP = TRUE
H1_PRODUCTION_INTEGRATION = NOT_AUTHORIZED
Nothing in frontend/src, backend/, or the database was touched.
git status --porcelain on the repo is empty after this work.
```

## Deliverables

- **Prototype (interactive)**: [Spatial Console Prototype](https://claude.ai/code/artifact/2d3f3418-c06c-436d-8951-b9ce5f574006)
  — `spatial-console-h06.html`, single self-contained file, scratchpad
  only, never committed.
- **Screenshot gallery (real captures)**: [Spatial Console H0.5/H0.6 Gallery](https://claude.ai/code/artifact/f2b9fc9e-dae7-4060-88a8-5507670cba22)
  — 9 Playwright captures, desktop 1280×800 + mobile 390×844.
- **Spec**: `docs/SPATIAL_UPGRADE_SPEC.md` — Transition Matrix, Shared
  Element Registry, Motion State Contract, spatial tokens, input matrix,
  loading/error/empty/offline doctrine, asset strategy, device/browser
  matrix, performance gates, visual-regression/feature-flag/telemetry
  plans, acceptance rubric, IP guardrail checklist.
- **Integration plan**: `docs/SPATIAL_H1_INTEGRATION_PLAN.md` —
  REUSE/EXTEND/WRAP/REPLACE-BLOCKED verdict per real surface. Not
  executed.
- This report.

## What was changed

Nothing in the repository's application code. All work is a new
standalone HTML/CSS/JS artifact (`spatial-console-h06.html`, ~1050
lines) built on top of the previously-approved H0 base
(`hub-prototype.html`, left untouched at its own URL as the historical
reference point), plus three new markdown docs under `docs/` (planning
artifacts, matching the established pattern from W1-W4 where design-only
documents were committed while interactive prototypes stayed
scratchpad-only).

Concretely, versus the H0 base:

- Replaced the earlier discrete target/secondary/horizon CSS classes
  with a continuous, distance-based depth engine (`applyDepth()`) using
  real CSS 3D transforms (`perspective` + `translateZ`) — FAR / ADJACENT
  / FOCUS, with asymmetric left/right horizontal displacement so the
  rail reads as a structure with mass, not a symmetric card fan.
- Added a two-layer parallax environment (`.env-light`, `.env-botanical`)
  on top of the existing tinted backdrop, each moving less than the rail
  and with `transition-delay`-based lag, plus a Graine→Forêt density
  demo control (clearly labeled prototype-only) so all 6 progression
  stages' environmental richness can be seen without needing real
  progression data.
- Applied the Founder's full timing/easing token table as CSS custom
  properties, used consistently across every transition in the file.
- Added dwell-based context reveal (rail responds to input instantly;
  a tile's detail text only commits ~130ms after focus settles).
- Added a real FLIP shared-element transition (Hub "Continuer" tile
  title → Module hero title, using `getBoundingClientRect()` + the Web
  Animations API — a genuine morphing DOM node, not a crossfade).
- Added real pointer-drag swipe with velocity-based snap on both the Hub
  and Formations rails (not just native `scroll-snap`).
- Added desktop-only pointer micro-tilt (±3° rotateX/Y) on the active
  Hub tile, disabled under reduced motion.
- Extended the route set from 4 to 7: Hub, Formations, Roadmap, Module
  (all previously in H0) plus new Missions, Badges, and FREK Profil
  views, each built to the "glanceable list/cluster, never a card grid"
  doctrine.
- Added a fourth context type (Proof/"Preuve") alongside the existing
  Quiz/Mission/Mentor, and a subtle client-only confirm motion on the
  quiz's "Valider" button.
- Added an ARIA live region announcing section and context changes.
- Added a header "compact" state on the Module view (reduced padding/
  opacity, no large transition).
- Fixed a real bug caught during verification (see below) where
  3D-transformed rail tiles' `scrollIntoView`/`focus()` calls were
  cascading a scroll adjustment onto `<body>` itself.

## What is simulated vs. what is repo-real

**Simulated (prototype-only, illustrative data)**: every formation,
mission, badge, FREK-ID, stage, and phase name/status in the file is
static JS data, clearly labeled in the visible "Prototype H0.5/H0.6 ·
données d'exemple" badge. No network call, no backend, no database
anywhere in this file.

**Repo-real, referenced but not modified**: the CVLN brand tokens
(colors, fonts) are copied from the actual `frontend/src/index.css`; the
depth/context vocabulary (target/secondary/horizon,
ACTIVE→CONTEXT→RETURN, DOMAIN_STATE vs SPATIAL_STATE) is the same
vocabulary already shipped in `frontend/src/lib/` (W1-W4) — this
prototype is a standalone reimplementation of that vocabulary for
testability, not a fork of the real components, and `SPATIAL_H1_INTEGRATION_PLAN.md`
explicitly calls out reusing the real hooks (`useContextEntry`,
`ContextFrame`) rather than keeping this duplication in any future
production version.

**Remains prototype-only** (see spec §§6-8, 12 for full detail, not
repeated here): Loading/Error/Empty/Offline states (documented, not
demoed), real environmental image/vegetal assets (currently CSS
gradient blobs only), telemetry (no target to wire against),
Formations-card→Module and Roadmap-stage→Module FLIP (only the Hub→Module
path is a genuine shared-element morph today), true velocity-aware
continuous response for keyboard input (only pointer-drag has real
velocity sampling; keyboard uses the dwell debounce instead), and a
distinct non-activating hover micro-state (folded into the click-to-focus
behavior rather than implemented separately).

## Performance observations

No `pageerror` console events across the full interaction script
(rail navigation in both directions, rapid-repeated-arrow-press
interruptibility check, FLIP transition, all 4 context types, section
switching across all 7 routes, browser back/forward, reduced-motion
toggle on and off, mobile pointer-drag swipe). No JS
`requestAnimationFrame` loop exists anywhere — every motion is a CSS
`transition`, so there is no custom animation-frame budget to blow;
interruptibility (rapid →→→→→→ presses not queuing a backlog of
animations) was verified by observation, not just assumed, since CSS
transitions retarget automatically when their target value changes
mid-flight. No real FPS/CLS/LCP/INP measurement was taken (disclosed gap
— this sandbox has no real-device tracing available); see spec §9 for
the proposed H1 gate numbers.

## Accessibility observations

Verified this session: full keyboard operability (arrow/Enter/Space on
every rail, Escape closes any open context, Tab respects roving
tabindex so off-focus tiles are skipped), `:focus-visible` outline
preserved throughout, ARIA live region fires on section and context
changes, reduced motion verified via computed style (not just visual
inspection) to actually remove `transform` and flatten opacity/filter
rather than merely speeding up the same animation, exact-return focus
verified to land back on the literal invoking element after closing a
context. Not verified this session (disclosed gap, see spec §8): screen
reader output (no screen reader available in this sandbox), 200% zoom
behavior, color contrast ratios were not run through an automated
checker, keyboard-trap testing beyond the contexts already exercised.

## Known gaps (full list)

See `docs/SPATIAL_UPGRADE_SPEC.md` for the complete, itemized gap list
inline with each relevant section (marked ⚠️ or "not yet implemented" /
"not done" throughout) — summarized here:
1. FLIP shared-element continuity proven for one path only (Hub→Module).
2. Real environmental image/vegetal asset strategy unresolved (CSS blobs
   only).
3. Loading/Error/Empty/Offline states documented but not demoed live.
4. Device/browser matrix limited to headless Chromium this session —
   no Safari/Firefox/real-Android/landscape testing.
5. No resize/orientation-change re-centering of the focused rail tile.
6. No dedicated non-activating hover micro-state, separate from
   click-to-focus.
7. No real performance trace (FPS/CLS/LCP/INP) — only functional
   correctness was verified.
8. No second-reviewer visual side-by-side against actual PlayStation UI
   screenshots (none available in this sandbox) — flagged for a human
   check before H1.
9. Telemetry, feature-flag, and visual-regression plans are written but
   not implemented (nothing to wire them to yet, correctly, since H1 is
   not authorized).

## Bug found and fixed during this session's own verification

Rail tiles carrying `translateZ()` under a `perspective` ancestor,
combined with `el.focus()` + `scrollIntoView()`, caused Chromium to
cascade a small scroll adjustment onto `<body>` itself — even though
`body` has `overflow:hidden` (an overflow:hidden ancestor is still a
legal `scrollIntoView` target, it just can't be scrolled by the user
directly). This was caught by an automated `window.scrollY` check added
specifically because the file uses 3D transforms for the first time in
this prototype series, not by visual inspection alone — the visual
symptom (header apparently "scrolled off") was subtle enough that a
quick look could have missed it. Fixed by using `{preventScroll:true}`
everywhere and manually computing `scrollBy()` on exactly the intended
container (the rail, horizontally; the stage, vertically) instead of
letting the browser walk the full ancestor chain. Re-verified clean
across the entire interaction script after the fix.

## Founder decision requested

Per the stop condition: `STOP = TRUE`, `H1 = NOT_AUTHORIZED`. Waiting
for one of:
- **APPROVE_DIRECTION** — proceed to define and separately authorize the
  H1 production integration wave, using `SPATIAL_H1_INTEGRATION_PLAN.md`
  as the starting sequencing document.
- **REVISE_DIRECTION** — specify what to change; this same prototype
  gets revised again.
- **REJECT_DIRECTION** — the Spatial Console direction is dropped; the
  W4-approved roadmap stands as the ceiling.
