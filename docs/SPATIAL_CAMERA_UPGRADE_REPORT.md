# Spatial Console — Camera / Composition Upgrade — REPORT

```
STOP = TRUE
H1 = NOT_AUTHORIZED
DO_NOT_RESET honored: the H0.5/H0.6 base file (spatial-console-h06.html)
is untouched, at its own URL, as the reference/rollback point. This
iteration lives in a new file (spatial-console-h07.html) built on top of
it — same lineage, additive only, nothing removed or reset.
Nothing in frontend/src, backend/, or the database was touched.
git status --porcelain on the repo is empty after this work (only this
doc is new).
```

## Deliverables

- **Prototype (interactive)**: [Spatial Console — Camera Iteration](https://claude.ai/code/artifact/98782933-48c0-4c4e-b429-6bafe4201aec) — `spatial-console-h07.html`, scratchpad only, never committed.
- **Before/after gallery (real captures)**: [Camera Upgrade — Before/After](https://claude.ai/code/artifact/e435cb79-eb3f-4e91-aefb-19a7dc5f5f6c) — H0.6 vs. this iteration, desktop + mobile, side by side.
- **H0.6 base, preserved as-is**: [Spatial Console Prototype (H0.5/H0.6)](https://claude.ai/code/artifact/2d3f3418-c06c-436d-8951-b9ce5f574006) — unchanged, the rollback target.
- This report. (`docs/SPATIAL_UPGRADE_SPEC.md` and `docs/SPATIAL_H1_INTEGRATION_PLAN.md` from the previous pass still apply — their tokens/matrix are extended, not replaced, by the table below.)

## What this iteration is, in one paragraph

The Founder's own H0.6 review was right that the rail was "credible but
still web-prototype-flat." This pass keeps every validated mechanic
(dominant focus, receding neighbors, partial offscreen continuation,
FLIP shared-element, context dock, reduced motion, mobile drag/snap, no
SaaS grid) and pushes five things that were genuinely under-built:
**camera** (the space now visibly reorganizes around whichever tile is
focused, not just the tile itself moving), **rail composition** (the
active tile is bigger and viewport-relative, not a fixed px block),
**structured aeration** (a spotlight and a floor line replace flat empty
space), **depth staging** (the module recedes further and more
convincingly when a context opens), and **tile presence** (each
destination now carries its own faint motif instead of being a plain
rounded rectangle with text).

## Camera architecture

The camera is not a new subsystem bolted on top — it's the existing
`applyDepth()` distance-based engine (already the H0.6 depth model)
extended with three real, measured mechanisms:

1. **`perspective-origin` follow** (`panCamera()`, new function). As
   focus moves along the rail, the containing `.rail-viewport`'s
   `perspective-origin-x` shifts between 44% and 56% proportionally to
   the focused tile's position in the list (`44 + (idx/(count-1)) * 12`).
   This is the literal "camera seems to follow" cue from the Founder's
   brief — verified this session by reading the computed style before
   and after a focus change (`44% 45%` → `52% 45%` after moving right),
   not just eyeballed. Disabled under reduced motion and on mobile
   (≤860px), per the brief's own mobile guidance.
2. **Stronger, curved depth buckets.** The active tile's Z moved from
   +30px to +56px (into the brief's APPROACH/ACTIVE range); neighbors
   now carry a `rotateY` (±3° adjacent, ±4.5° far, ±5.5° locked, sign
   flipped left vs. right) so the rail reads as a shallow curve, not a
   flat fan — the literal ask in the brief's §9. Horizontal dispersion
   (`translateX`) increased from a ×9 to a ×13 multiplier so neighbors
   visibly "make room" rather than just shrinking in place.
3. **Camera lag via staged `transition-delay`.** The target tile's
   transition fires at 0ms; adjacent tiles at 40ms; far tiles at 70ms —
   so a focus change reads as the active object leading and the rest of
   the rail settling a beat later, not everything snapping in lockstep.

None of this is WebGL or a literal 3D engine — it's CSS `perspective` +
`translateZ`/`rotateY` on real DOM nodes under a `perspective`-bearing
ancestor, exactly as `WEBGL_AUTHORIZED = FALSE` requires.

## Rail composition & aeration

- **Viewport-relative sizing.** Tile widths moved from fixed px
  (`290px`/`460px`) to `clamp()` (`clamp(210px,18vw,280px)` /
  `clamp(360px,30vw,520px)` for hub tiles; similarly for Formations
  cards) — the active tile now occupies a consistent *proportion* of the
  viewport rather than a constant that reads small on a wide monitor.
- **Elegant bleed.** The rail viewport now carries a `mask-image` fading
  the first/last ~28px to transparent, so the partially-offscreen tile
  fades at the edge instead of being hard-cropped — still fully
  measured and verified present (bleed geometry re-checked this session,
  see Verification below), just softer.
- **Rail repositioned.** `.hub-view-inner` changed from
  `justify-content: center` (rail floating in a tall empty column) to
  `flex-start` with a `padding-top: clamp(28px, 9vh, 100px)` — the rail
  now sits in the upper-middle third, closer to the brief's
  `SYSTEM_HEADER → PRIMARY_RAIL → CONTEXT` reading order.
- **Structured, not just empty, space.** The `.env-light` layer was
  tightened into more of a spotlight (54vw instead of 70vw, 22% instead
  of 14% mix strength) so it reads as directed light behind the focus
  rather than a diffuse wash; a thin gradient "floor" line was added
  near the bottom of the hub view as a quiet horizon cue.
- **Header thinned further.** Padding reduced again (`20px→15px`
  resting, `13px→10px` compact-on-module), pill font-size/padding
  trimmed — the rail, not the header, is now unambiguously the dominant
  navigation surface.

## Tile presence

Each hub destination now carries a faint (`opacity:.3`, `.16` on the lit
target tile), `currentColor`-tinted CSS pattern via `::before` — no
image assets, no Sony iconography:

| Destination | Motif | Rationale |
|---|---|---|
| Continuer | none (rich forest gradient hero) | already the most visually distinct tile |
| Formations | horizontal lines | "editorial structure" |
| Feuille de route | vertical lines | "structural / directional" |
| Missions | diagonal lines | "action-oriented" |
| Badges | dot grid | "accumulated symbols," deliberately not a trophy-shelf look |
| Profil FREK | fine grid | "identity / precision" |
| À venir (disabled) | none | stays visually quiet, honestly inert |

Far-role tiles also drop their eyebrow label entirely (title only),
adjacent tiles keep eyebrow+title, only the target tile reveals the full
glance+CTA — matching the brief's "reduce inactive-tile text density"
ask, reusing the dwell-reveal mechanism already built in H0.6.

## Depth staging (context entry)

The module-recede-behind-context-dock treatment was already present in
H0.6; this pass deepened it so the plane separation is unambiguous:
module now goes to `scale(.965) translateZ(-32px) opacity(.72)` (was
`.985 / -18px / .8`), and the dock's own approach plane moved from
`translateZ(30px)` to `translateZ(50px)`. Verified visually — the module
list is now clearly a distinct, receded plane behind the dock, not a
slightly-dimmed version of the same plane.

## What was deliberately NOT done this pass (disclosed, not silently dropped)

- **No pre-beat neighbor disperse before the FLIP capture.** The brief's
  §11 implies neighbors could visibly disperse an extra beat before a
  module-entry transition begins; adding a transient state right before
  `getBoundingClientRect()` capture in `flipHeroTransition()` risked
  measuring the wrong rect if timed wrong. Skipped to protect the FLIP
  correctness already proven working; a candidate for the next pass.
- **No true continuous camera lag timeline matching the brief's exact
  0/30/60/90/120/150/220/280/520ms table.** The three-tier
  transition-delay (0/40/70ms) approximates the *ordering* (active leads,
  neighbors follow, environment lags most via its existing 140-200ms
  delays) without literally implementing nine discrete stages — judged
  sufficient to read as staged rather than simultaneous; a finer
  timeline is a refinement, not a correctness gap.
- **Roadmap and Module phase-list did not get the rotateY/motif
  treatment.** Roadmap already shares `applyDepth()` (so it got the
  stronger Z/dispersion automatically) but stage cards have no `--tint`
  per-item motif system; Module's phase list is a vertical stepper, not
  a spatial rail, and the brief's camera language is rail-specific.
  Scope line kept deliberately narrow to the actual rails.
- **Formations rail did not get its own FLIP path** — same disclosed gap
  as the H0.6 report; still only Hub→Module has a genuine shared-element
  morph.

## Verification performed this session

- Zero `pageerror` console events across the full interaction script
  (rail navigation both directions, rapid-repeated-arrow interruptibility
  check, FLIP, quiz context open/close, section switching, browser
  back/forward, reduced-motion toggle, mobile pointer-drag swipe) — same
  regression battery as H0.6, re-run against this iteration.
- **Body-scroll regression re-checked specifically**, since this pass
  added new 3D transforms (`rotateY`) on top of the H0.6 bug class
  (3D-transformed focus targets confusing `scrollIntoView`): confirmed
  `window.scrollY === 0` at every checkpoint, no recurrence.
- Camera pan confirmed via computed style, not visual inspection alone
  (`perspective-origin` measurably changes with focus).
- Partial-offscreen bleed re-measured via `getBoundingClientRect()`
  after the sizing/mask changes: with 7 hub tiles, 3 fully visible + 1-2
  partially bled at rest, 2+ fully off-screen — the requirement still
  holds, now with a softer visual edge.
- Reduced motion re-verified via computed style
  (`target.style.transform === ''`), not just visually.
- Back/forward re-verified: `#formations` → `#roadmap` → back → forward
  round-trip correct.
- Mobile: pointer-drag swipe still functions, zero errors, zero
  unwanted scroll.

## Performance notes

No new `requestAnimationFrame` loops introduced — `panCamera()` and
every other new mechanism only ever writes to `element.style` in
response to a discrete input event (arrow key, click, drag-end), never
inside a continuous loop, so the interruptible-by-default property of
plain CSS transitions (already relied on in H0.6) still holds. The
`mask-image` and `::before` motif layers are static (no animated
gradient position), so they add paint cost only once per resize, not
per frame. Not measured this session (same disclosed gap as the H0.6
report): real FPS/CLS/LCP trace — only functional/console-error
correctness was verified.

## Founder decision requested

`STOP = TRUE`. `H1 = NOT_AUTHORIZED`. Waiting for:
- **APPROVE_DIRECTION** — proceed to the H1 integration plan
  (`docs/SPATIAL_H1_INTEGRATION_PLAN.md`), updated in a future pass to
  reference this camera engine specifically.
- **REVISE_DIRECTION** — specify what to change; this file gets revised
  again, in place, without resetting.
- **REJECT_DIRECTION** — direction dropped; H0.6 (still intact at its
  own URL) stands as the ceiling.
