# Spatial Console Upgrade — Specification (W5 H0.5/H0.6)

```
STATUS: DESIGN_ONLY — this document specifies a direction validated in a
standalone prototype. Nothing here has been wired into frontend/src.
H1_PRODUCTION_INTEGRATION = NOT_AUTHORIZED.
```

This is the single source of truth for the Spatial Console upgrade so
that any future implementer (Claude or human) does not have to
improvise the transition/depth/token vocabulary per screen. It responds
directly to the Founder's H0.5/H0.6 authorization prompt, section by
section: Transition Matrix, Shared Element Registry, Motion State
Contract, Spatial Tokens, Input Matrix, Loading/Error/Empty/Offline
doctrine, Asset Strategy, Device/Browser Matrix, Performance Gates,
Visual Regression Plan, Feature Flag Plan, Telemetry Plan, Acceptance
Rubric, and the IP Guardrail Checklist.

The prototype that exercises this spec is
`spatial-console-h06.html` (published as an Artifact, scratchpad-only,
never committed) — see `SPATIAL_H05_H06_REPORT.md` for the link and for
what in this document is *proven* by that prototype vs. still a plan.

---

## 1. Transition Matrix

Every pair below follows the same grammar (spec §10):
`INTENT → FOCUS → APPROACH → NEIGHBOR_RECEDE → RAIL_SHIFT →
ENVIRONMENT_RESPONSE → OLD_CONTEXT_RECEDE → NEW_CONTEXT_REVEAL →
SECONDARY_SETTLE`. Return path is the inverse:
`CONTEXT → RECEDE → MEMORY_REAPPEARS → RETURN → EXACT_POSITION → SETTLE`.

| FROM | TO | SHARED_ELEMENT | Direction | Timing | Reduced-motion fallback | Back behavior |
|---|---|---|---|---|---|---|
| Hub rail (any tile, unfocused) | Hub rail (tile focused) | tile itself | X (rail shift) | `--t-rail` 300ms, `--ease-spatial` | opacity/contrast only, no translateZ | n/a (not a route change) |
| Hub → Formations | Formations rail | none (recede/reveal only) | X→Y (rail out, view in) | `--t-env` 600ms crossfade | crossfade only, no scale/Z | Formations → Hub, hub focus restored via Depth Memory |
| Hub → Roadmap | Roadmap stage row | Stage tint → backdrop glow | X→Y | `--t-env` 600ms | crossfade only | Roadmap → Hub |
| Hub → Missions / Badges / FREK | respective glanceable view | none | X→Y | `--t-env` 600ms | crossfade only | → Hub |
| **Hub "Continuer" tile → Module** | Module hero title | **tile title text node (real FLIP)** | Z (approach) + morph | 420ms `--ease-approach` | disabled — instant `goto()`, no clone/morph | Module → Hub, hub focus restored to `continue` |
| Formations card → Module | Module hero | none (not yet a FLIP path — see gaps) | X→Y | `--t-env` 600ms | crossfade only | Module → Formations, formation focus restored |
| Roadmap stage → Module | Module hero | Stage color persists as backdrop glow only (not a literal node) | X→Y | `--t-env` 600ms | crossfade only | Module → Roadmap |
| Module → Quiz/Mission/Proof/Mentor context | Context dock | none (dock is its own object, module recedes behind it) | Z (dock approaches from `translateZ(30px)`, module recedes to `translateZ(-18px)`) | `--t-context` 400ms `--ease-approach` (open) / `--ease-recede` (module recede) | translateZ removed, only opacity/scale-.985 fallback disabled entirely — dock still slides via translateX only | Escape / scrim click / close button — never the browser Back button (dock is not a route) |
| Context → Module (return) | Context dock | invoking element (real DOM focus target) | Z (recede) then exact `element.focus({preventScroll:true})` | `--t-return` 320ms | instant | n/a |
| Any section → Any section via browser Back/Forward | destination view | Depth Memory (focus id) per section | inverse of forward direction | same as forward | same | native `popstate`, `pushHistory:false` re-entry |

**Known gap:** only the Hub→Module path has a genuine FLIP-morphed shared
DOM node today. Formations-card→Module and Roadmap-stage→Module currently
achieve continuity only through the backdrop tint and the crossfade
grammar, not a literal moving node. Extending FLIP to those two paths is
the top item in `SPATIAL_H1_INTEGRATION_PLAN.md`.

## 2. Shared Element Registry

Elements a future implementation must NOT recreate from scratch across a
transition — they should visually persist, morph, or hand off:

| Registry key | Owning surface | What persists | Persistence mechanism today |
|---|---|---|---|
| `formation:<code>` (e.g. `formation:da`) | Formations rail card ↔ Module header | formation name/pole/color | **not yet implemented** — Module currently reads its own static heading, no visual hand-off from the Formations card. Gap for H1. |
| `module:<code>` (e.g. `module:M02`) | Roadmap stage / Hub "Continuer" tile ↔ Module hero title | title text, tint | Hub path: real FLIP (WAAPI). Roadmap path: tint only, no literal node. |
| `current-stage` | Roadmap "current" stage card ↔ backdrop `--glow-1` | stage color | CSS custom property carried on the backdrop (`--stage-live-color`), not a literal node — deliberate: the *color* is the shared element, not the card shape. |
| `frek-id` | Header chip ↔ FREK Profil hero | the identifier string | Static duplication today (`FREK · Anaïs` in header, `FREK-AN7-2044` on the Profil view) — **not the same underlying value in this prototype's illustrative data**, flagged as a data-consistency gap to fix with real data in H1, not a transition gap. |
| `context-invoker` | Whatever opened a context dock (phase row, mentor affordance, mission row) | exact focus return target | Real: `state.invokerEl` + `element.focus({preventScroll:true})` on close. |

Rule for H1: before adding a new cross-surface transition, add its row
here first. Nothing should "decide at random" which elements survive a
transition, per the Founder's own note — this table is the decision
record.

## 3. Motion State Contract

Strict separation, extending the existing `spatial-state.js` /
`ContextFrame.jsx` doctrine already shipped in `frontend/src/lib/`:

- **DOMAIN_STATE** (real, backend-sourced, mutation-gated): user
  progression (`user.stade`), module unlock state, quiz/mission/cert
  results, badges earned, FREK signals. **No motion, transition, or
  prototype interaction may write to this.**
- **SPATIAL_STATE** (UI-only, ephemeral, never persisted to a backend):
  `state.section`, `state.hubFocusId`, `state.formationFocusId`,
  `state.dockOpen/dockKind/invokerEl`, `depthMemory`. Freely mutated by
  navigation and motion.
- **Contract**: a motion function may *read* DOMAIN_STATE (e.g. to decide
  a role — current/acquired/next/locked) but may only ever *write*
  SPATIAL_STATE. The prototype's "Valider (démo)" quiz-confirm button is
  the concrete test of this: it changes only a local DOM class/text,
  explicitly labeled "aucune progression réelle modifiée," and calls no
  API. Any H1 implementation of a real confirm action must call the real
  `POST` first and only *then* run the confirm motion — the prototype
  encodes this ordering as USER_ACTION → BACKEND_CONFIRMS → SUBTLE_CONFIRM
  → STATE_CHANGE → NEXT_HORIZON_MOVES_CLOSER (spec §34), never the
  reverse.

## 4. Spatial Tokens

Exact values used by the prototype (CSS custom properties in
`spatial-console-h06.html`), to stop each screen "interpreting"
its own depth/spacing:

```
Easing:
  --ease-spatial:  cubic-bezier(.2,.8,.2,1)     general movement
  --ease-approach: cubic-bezier(.16,1,.3,1)     approach / open
  --ease-recede:   cubic-bezier(.4,0,.6,1)      recede / close
  --ease-env:      cubic-bezier(.25,.1,.25,1)   environment / section crossfade

Timing:
  --t-micro:   190ms   micro focus (hover, header compact)
  --t-rail:    300ms   rail shift (tile width/position change)
  --t-approach:380ms   approach (unused standalone in H0.6 — folded into rail)
  --t-context: 400ms   context dock open/close, module recede
  --t-env:     600ms   environment/section crossfade, backdrop tint
  --t-return:  320ms   context return (label only — actual return uses --t-context)

Depth buckets (applyDepth(), distance = index - focusedIndex):
  |distance| = 0 (FOCUS):    translateZ +30px, scale 1.00, opacity 1.00
  |distance| = 1 (ADJACENT): translateZ -35px, scale 0.94, opacity 0.72, saturate(.82)
  |distance| = 2 (FAR):      translateZ -70px, scale 0.88, opacity 0.48, saturate(.6), blur .2px
  |distance| ≥ 3 (LOCKED):   translateZ -90px, scale 0.83, opacity 0.30, saturate(.46), blur .4px
  horizontal nudge:  translateX = distance × min(|distance|,3) × 9px  (asymmetric left/right mass)

Perspective:
  main.stage:     perspective 1500px, perspective-origin 50% 38%
  .rail-viewport: perspective 1400px, perspective-origin 50% 45%

Camera layers (movement % of foreground rail's own translateX):
  foreground rail:  100%
  env-light layer:  ~20%  (index × 24px), 140ms transition-delay (lag)
  env-botanical:    ~10% conceptually (currently static position, opacity-only
                     density change) — see §11 gap note, true parallax
                     translateX on this layer is NOT yet implemented, only
                     the light layer moves today.

Rail geometry (desktop, 1280px reference):
  hub tile (adjacent/far): 290px wide, min-height 210px
  hub tile (target):       460px wide, min-height 250px
  formation card:          250px / 300px (target)
  rail gap:                40px (hub), 20px (formations)
  measured partial-offscreen bleed at rest: 0px of a 3rd+ tile is fully
  hidden with 7 total hub tiles — verified via Playwright
  getBoundingClientRect(), not eyeballed.

Safe zones:
  proto-badge / doctrine-demo controls never overlap primary content —
  bottom-8px band reserved on mobile (<640px) for the badge, left-14px
  reserved for the doctrine demo control (desktop only, hidden <640px).

Max shadow/blur budget (perf gate, §9 below):
  ≤ 1 blur filter concurrently animating per view (backdrop noise texture
  is static, not animated); ≤ 3 concurrent box-shadow-bearing elements in
  motion (target tile + dock + scrim).
```

## 5. Input Matrix

| Input | Surface | Behavior | Verified |
|---|---|---|---|
| Mouse click | rail tile (unfocused) | focus only (approach), does not activate | ✅ Playwright |
| Mouse click | rail tile (already focused) | activates (navigates) | ✅ Playwright |
| Mouse hover | rail tile | translateY(-2px)-class lift only (no `scale(1.05)`) — not separately implemented as a distinct CSS hover rule in H0.6, folded into the existing depth roles; **gap**: a dedicated non-activating hover micro-state (spec §27) is not yet distinct from click-to-focus | ⚠️ partial |
| Mouse move | active/target hub tile only | pointer micro-tilt, rotateX/Y ±1.5°, desktop only | ✅ Playwright (verified disabled under reduced motion) |
| Keyboard ← → | any rail | move focus, roving tabindex | ✅ Playwright |
| Keyboard Enter/Space | rail (focused tile) | activate | ✅ Playwright |
| Keyboard Escape | anywhere, context open | close context, exact return | ✅ Playwright |
| Keyboard Tab | any view | native tab order through visible/enabled controls only | ✅ (roving tabindex keeps off-focus tiles at -1) |
| Touch / pointer drag | hub rail, formations rail | 1:1 drag-follow via `scrollLeft`, velocity-based snap-to-next on release | ✅ Playwright (`hasTouch`/pointer simulation) |
| Browser Back/Forward | any section | native `popstate`, exact section + focus restore | ✅ Playwright |
| Resize / orientation change | any | CSS media queries at 860px/640px breakpoints; no JS resize listener recomputes rail centering — **gap**: rotating a device mid-session does not re-center the focused tile until the next focus change | ⚠️ gap, disclosed |
| Rapid repeated input (→→→) | any rail | CSS transitions retarget automatically (no JS animation queue exists) | ✅ Playwright rapid-arrow-press test, no queued backlog observed |

## 6. Loading / Error / Empty / Offline States

**Not live-demoed in H0.6** (disclosed gap, not attempted) — documented
here as doctrine so H1 does not invent it under deadline pressure:

- **Loading**: a surface with no data yet should render its own shell
  (rail structure, tile outlines) at reduced opacity with no skeleton
  shimmer animation (shimmer reads as "alive/gamey," conflicts with
  CALM_BY_DEFAULT) — the shell fades to full opacity once data resolves,
  using `--t-env` timing, same as any other reveal.
- **Error**: never a full-page error screen. An error on one destination
  (e.g. Missions fails to load) should keep the Hub rail's other tiles
  fully interactive and show the failed tile in a visually "unsettled"
  state (desaturated, a small inline retry affordance in its glance
  area) — never a modal, never a red banner across the whole viewport.
- **Empty**: an empty Missions/Badges list is not a blank page — it
  should read as "this part of the environment hasn't grown here yet,"
  consistent with §8's Graine→Forêt doctrine (sparse, not broken).
- **Offline**: the environment should desaturate slightly (a global
  filter on `.env-base`, not a fresh element) with one small glanceable
  notice near the header ("Connexion perdue — reprise automatique"),
  never a full interstitial. Reconnection reverses the same desaturation
  transition, no confetti/flash.

## 7. Image / Environmental Asset Strategy

**Open question, not resolved in H0.6.** Today every environment is CSS
gradients + a handful of absolutely-positioned blurred radial-gradient
"blobs" (`.veg-blob`) — zero raster/vector image assets, zero network
weight beyond the two Google Fonts. This satisfies NO_SONY_ASSETS and
keeps the prototype self-contained, but it is explicitly a placeholder,
not a resolved visual language:

- Pro: zero asset budget, trivially themeable, no risk of resembling any
  specific reference imagery.
- Con: reads as "gradient blobs" rather than a distinctive CVLN
  environment at higher fidelity — the Founder's own research doc flags
  generic gradients as a real risk.
- **For H1**: commission or generate a small set of abstract, non-photographic
  vegetal/organic texture assets (SVG, not raster, to stay CSP/weight-safe)
  that read as CVLN's own visual language, not stock "blurred
  circles." Max weight budget: 150KB total for all environment
  assets across all 6 Graine→Forêt density levels combined, lazy-loaded
  per section.

## 8. Device / Browser Matrix

**Tested in this session**: Chromium (headless, via the pre-installed
Playwright browser) at 1280×800 (desktop) and 390×844 with touch
emulation (mobile). That is the full extent of what this sandbox can
verify.

**Not tested, disclosed gap**: Safari iOS (momentum-scroll physics,
`backdrop-filter` support nuances, bottom-sheet drag), Safari macOS,
Firefox, real Android Chrome (vs. emulated), landscape orientation on
small devices, any device with a notch/safe-area-inset (the layout does
not currently read `env(safe-area-inset-*)`). H1 must add this matrix as
real device/BrowserStack-style testing before any production rollout.

## 9. Performance Gates

Measured this session (Chromium headless, single machine, indicative
not authoritative):
- Zero `pageerror` console events across the full interaction script
  (rail navigation, FLIP, all 4 context types, section switches,
  back/forward, reduced-motion toggle, mobile swipe).
- Zero unwanted outer-page (`window.scrollY`) drift across the same
  script, after the fix described in the report.
- No JS `requestAnimationFrame` loop exists anywhere in the file — every
  motion is a CSS `transition`, so there is no animation frame budget to
  blow beyond what the browser's own compositor manages.

**Not measured this session** (disclosed gap — no real device / DevTools
tracing was run, only functional Playwright checks): actual FPS under
load, CLS, LCP, INP, long-task count, bundle weight (irrelevant here —
single static file, but relevant once this grammar moves into the real
React app in H1). H1 gate proposal, to be confirmed against real
measurement before shipping: 60fps sustained during rail navigation on a
mid-range device, CLS = 0, ≤ 3 concurrently-animating box-shadow layers,
≤ 1 concurrently-animating blur filter, no long task > 50ms attributable
to a single focus-change.

## 10. Visual Regression Plan

The W4-E gallery methodology (git-checkout-overlay + Playwright
screenshot + gallery Artifact, see
`docs/SPATIAL_LEARNING_W4E_VISUAL_REVIEW_PACKAGE.md`) is the template to
reuse once this grammar lands in `frontend/src` under H1: same three-way
Before/After comparison technique, same fixture-authenticated capture
approach, same desktop+mobile pairing. **Not re-run for H0.6** — this is
a standalone prototype with no production commit to diff against yet;
the W4-E baseline stays the reference point for whenever H1 actually
touches `frontend/src`.

## 11. Feature Flag / Rollback Plan (for H1, not built)

Proposed, not implemented: `SPATIAL_HUB_ENABLED` env-driven flag at the
`App.js` routing layer, defaulting `false` in production until an
explicit rollout decision. Rollback is "flip the flag back to false" —
the existing (currently shipped, W1-W4) Spatial Learning UI stays fully
intact underneath as the fallback, never removed until the new grammar
is proven. No domain/backend code would ever be touched by this flag —
it only gates which presentational shell mounts.

## 12. Telemetry / Observability Plan (for H1, not built)

Proposed, not implemented (no analytics target exists in this sandbox to
wire against): navigation-error counter (a `goto()` call that resolves
to an unknown section), transition-abandoned counter (a context opened
and closed within < 150ms, suggesting a mis-click), context-not-restored
counter (an `invoker` element no longer in the DOM at return time —
already guarded against crashing via `document.contains(invoker)`, but
worth counting since it means Depth Memory failed silently), and
frame-drop sampling during rail shifts. Explicitly **not** proposed:
engagement/session-length/streak metrics — the Founder's own doctrine
(`CALM_BY_DEFAULT`, no gamification) rules out addictive-pattern
telemetry, and this plan does not introduce any.

## 13. Acceptance Rubric (stricter than "site vs. environment")

For a future human reviewer, score 1–5 on each axis rather than a single
yes/no:

| Axis | 1 (fails) | 5 (fully achieved) |
|---|---|---|
| Air (negative space) | dense, bordered, dashboard-like | generous space, minimal chrome, one object reads first |
| Depth | flat, same-plane cards | real perceived Z-order, FAR/ADJACENT/FOCUS legible at a glance |
| Focus | multiple equal-weight objects compete | exactly one dominant object at any moment |
| Continuity | hard cuts, white flashes between views | crossfade + shared-element hand-off, never a blank frame |
| Calm | motion fires without being asked | motion only on FOCUS/APPROACH/RECEDE/REVEAL/CONNECT/CONFIRM/RETURN, idle is still |
| CVLN identity | reads as generic/Sony-adjacent | unmistakably CVLN's own palette/type/doctrine, PS reference invisible in the output |

`H0 = NOT APPROVED` if the *Focus* or *CVLN identity* axis scores below
3, per the Founder's own validation question — those two are the
non-negotiables.

## 14. IP / Asset Guardrail Checklist

Explicit visual review performed before delivery, not just "we didn't
copy assets":
- [x] No Sony/PlayStation wordmark, logo, icon, or system font anywhere
  in the file (grepped for any embedded image/font reference — the only
  external resource is the Google Fonts stylesheet link, verified above).
- [x] No PS5-specific geometry reused at 1:1 (e.g. no repeated diagonal
  "tile carousel" silhouette matching a specific PS5 screen; tile shape
  here is a plain rounded rectangle, not the PS5's parallelogram-ish
  cards).
- [x] No color lifted from PlayStation's own blue/white system palette —
  every hue in this file traces to `frontend/src/index.css`'s existing
  tokens (orange #E05A33, forest #143628, stage colors) or a
  `color-mix()` of them.
- [x] No sound (`AUDIO = NOT_AUTHORIZED` honored — zero `<audio>`, zero
  Web Audio API calls anywhere in the file).
- [ ] **Not done**: a second-reviewer visual side-by-side against actual
  PS5 UI screenshots was not performed in this session (no such
  reference images exist in this sandbox to compare against) — flagged
  for a human Founder-level check before H1, per the request for an
  "explicit visual review to avoid a composition too close to a specific
  PlayStation screen."
