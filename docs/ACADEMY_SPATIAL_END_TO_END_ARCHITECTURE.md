# CVLN Academy — Spatial End-to-End Architecture (W-FUNNEL-0)

```
DESIGN_ONLY. No production code changed to produce this document.
H0.10 (spatial-console-h10.html) remains the untouched source reference
— this document is the plan for extracting reusable primitives from it
into frontend/src, never for editing it in place.
```

## 1. One world, contextual intensity

`ONE_CONTINUOUS_WORLD = TRUE` does not mean constant intensity — the
mission is explicit (§6) that spatial intensity must vary by context,
and forbids sacrificing usability to demonstrate the engine. Target
tiers, cross-referenced against what the current codebase already does
(`ACADEMY_CURRENT_FUNNEL_AUDIT.md`):

| Surface | Target intensity | Current reality |
|---|---|---|
| Landing | MEDIUM/HIGH | LOW today (W2-B, 2 of 5 primitives) |
| Signup/Login | LOW/MEDIUM | LOW (same page, same tranche) |
| Onboarding | MEDIUM | none (standard form) |
| Activation | HIGH | none (no dedicated moment yet) |
| Dashboard/Hub | HIGH | none (standard dashboard tiles) |
| Formation Discovery | HIGH | PARTIAL (W2-D) |
| Roadmap | HIGH | REALIZED (W3-D) |
| Module reading | LOW | REALIZED (W3-A, deliberately calm) |
| Quiz | LOW/MEDIUM | none (standard modal, presumed) |
| Mission | MEDIUM | none |
| Mentor | MEDIUM | REALIZED (W3-C, contextual not floating) |
| Certification | MEDIUM/HIGH | none |
| Payment | LOW | N/A — layer doesn't exist |
| Return/Retention | MEDIUM/HIGH | none |
| Expansion | HIGH | none |
| Ecosystem | HIGH | none — nothing to show truthfully yet |

## 2. Environmental continuity across the full journey

The mission asks for the same persistent-morphing-environment principle
H0.10 proved on a 3-route slice (`--glow-1/2/3`, `--topo-depth`,
`--formation-signature`) extended across the entire authenticated app
shell, plus Landing/Onboarding/Activation before authentication exists.

**Real constraint found this session**: today's production app has
**no persistent backdrop layer at all** — `frontend/src/components/
Layout.js` (not read line-by-line this pass, but confirmed by App.js's
structure: `<Protected><Layout>{children}</Layout></Protected>`) wraps
each page, and each page is its own route-swapped tree, same as H0.10's
`.view` sections — but H0.10's `#backdrop` sibling-to-`#app` pattern
does not yet exist in `frontend/src`. Building it is real, additive
frontend work (a new persistent `<AcademyBackdrop>` component mounted
once in `Layout.js`, outside the route-switched subtree), not a
rewrite of anything.

**Persistent elements to carry across the whole app** (extending
H0.10's 3-element proof):
- **Light field** — section/route-tinted glow, already proven pattern (H0.10 §1).
- **Formation/pole signature** — H0.10's `--formation-signature`,
  generalized: driven by `user.metier_vise` at rest, by whichever
  formation is currently focused/open when browsing.
- **Progression/stade layer** — new: `user.stade` (graine→forêt) already
  exists as real domain data (stage 09 audit) and maps naturally onto
  H0.10's botanical density selector (already built, currently a manual
  demo toggle in the prototype — becomes real, driven by the real
  `stade` field, not a doctrine demo).

`ENVIRONMENT_RESET_PER_ROUTE = FORBIDDEN` carries forward unchanged.

## 3. Camera/physics/attention/occlusion — extraction plan, not rebuild

H0.10 already contains, verified working: `makeRailPhysics` (substepped
spring), `cameraFollowTransition`/`cameraReturnTransition` + Camera
Anchor Contract, the cadence classifier, focus prediction,
`attentionTier`/`applyDepth` (6-channel occlusion), `TRANSITION_
TOPOLOGY`, `SpatialAudio`/`Haptics` controllers, `FramePacing` sampler.

**W-FUNNEL-1's job**: extract these as framework-agnostic modules
(plain JS, no React coupling in the physics/attention math itself) under
a new `frontend/src/lib/spatial/` directory, each independently
testable against the same node-simulation method used to catch and fix
H0.10's substepping bug (`docs/SPATIAL_H10_PERCEPTUAL_REFINEMENT_
REPORT.md` §3) — that verification method is itself a reusable asset,
not just a one-time fix.

**Do not** re-derive the physics constants or the substep fix from
memory — copy the verified values (`STIFFNESS=280, DAMPING=33,
SUBSTEP=1/120`) and the exact integration loop structure from
`spatial-console-h10.html`, then adapt call sites to React idioms
(likely a `useSpatialPhysics` hook wrapping the same `makeRailPhysics`
factory).

## 4. Camera model (mission §20-22)

```
USER INTENT → SPATIAL FOCUS → CAMERA LOCK → CAMERA FOLLOW →
WORLD RECOMPOSITION → DESTINATION REVEAL → SETTLE
```

This is H0.8/H0.9's Camera Anchor Contract + state machine, unchanged
in shape. Route transitions in `frontend/src` currently go through
`RouteTransition.jsx` (W1-C/W2-A) — a real, existing seam. W-FUNNEL-1
extends `RouteTransition` to accept an optional Camera Anchor Contract
per transition rather than replacing its existing fade/crossfade
default, so routes with no defined anchor (most of them, initially)
keep exactly today's behavior — additive, never a hard cut.

Forbidden, unchanged: hard camera reset, route fade as *primary*
navigation once an anchor exists for that pair, page teleport,
wait-for-animation, queued transitions.

## 5. Attention system (mission §23) — one canonical model, not per-page reinvention

H0.10's `PRIMARY_ATTENTION/SECONDARY_CONTEXT/PERIPHERAL_CONTEXT/
LATENT_CONTEXT` tiers, continuous-weight-driven, become the one model
used everywhere a screen has to decide what's foregrounded — Dashboard
(mission §12), Formation/Roadmap/Module (§13), Proof surfaces (§15).
Exactly one `PRIMARY_ATTENTION` at all times is a hard invariant,
carried forward unchanged from H0.10's own verified guarantee.

## 6. Mobile (mission §28)

H0.10's mobile drag/snap (`attachSwipe`, velocity-aware commit, SNAP
haptic) is real and verified (H0.9/H0.10 reports). Extending it means
the same extraction as §3, not new physics. Forms and payment stay
outside the physics system entirely, per the mission's own instruction
— they were never spatialized in H0.10 either (its quiz/mission dock
content is plain DOM, only the *container* motion is spatial).

## 7. Accessibility & performance — inherited invariants

Every H0.10-verified rule carries forward unchanged: DOM semantics
primary, keyboard navigation required, visible focus required, focus
restoration required, `prefers-reduced-motion` reduces Z/rotation/
perspective-origin/parallax/tilt/large-displacement but preserves
hierarchy/state-change/orientation/context/autofocus. Degradation order
(blur → environmental parallax → secondary transforms → decorative
motif) is H0.10's own disclosed scope, not new policy. Never-degrade
list (input, focus, camera target, domain correctness, route
continuity, accessibility) is unchanged.

**New this pass**: the current production app's own real E2E coverage
(`keyboard-focus.spec.js`, `reduced-motion.spec.js`, `auth-guards.spec.
js`, `route-transition.spec.js`) is the baseline every new spatial
surface must not regress — extend these specs, don't replace them.

## 8. What this document deliberately does not do

It does not specify component APIs, file diffs, or a build order beyond
naming the wave — that's `ACADEMY_FUNNEL_IMPLEMENTATION_PLAN.md`'s job,
and per the mission's own staging rule (§38), no implementation begins
until W-FUNNEL-0 is authorized.
