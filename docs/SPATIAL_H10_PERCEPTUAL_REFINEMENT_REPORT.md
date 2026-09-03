# H0.10 — Perceptual Refinement Pass — REPORT

```
STOP = TRUE
H1 = NOT_AUTHORIZED
DO_NOT_RESET honored: H0.9 (spatial-console-h09.html) is untouched at its
own URL, kept as the reference/rollback point. This iteration lives in a
new file (spatial-console-h10.html), same lineage, additive only.
Nothing in frontend/src, backend/, or the database was touched.
git status --porcelain on the repo is empty after this work (only docs).
```

## Deliverables

- **Prototype (interactive)**: [Spatial Console — H0.10](https://claude.ai/code/artifact/aace6209-6466-4a94-a5c3-ed9c24403570) — `spatial-console-h10.html`, scratchpad only, never committed.
- **Proof gallery** (0/20/40/60/80/100% environmental-continuity sequence + attention/occlusion + calibration mode): [H0.10 Proof Gallery](https://claude.ai/code/artifact/f5e6833c-6486-442e-a4ff-ea0b4eeac413)
- **H0.9 base, preserved as-is**: [Spatial Console — H0.9](https://claude.ai/code/artifact/850da556-71ba-4737-8521-adcbd3f313bb) — unchanged, the rollback target.
- This report.

## What H0.10 is, in one paragraph

The Founder's own framing for this pass was explicit: **not another architecture pass — a perceptual refinement pass**. Every H0.9 system (spring physics, retarget-safe motion, input cadence, focus prediction, frame-pacing instrumentation, spatial audio/haptic architecture, transition topology) stays exactly as delivered; nothing was rebuilt. What changed is *how it feels and reads*: environmental continuity is now provable end-to-end across a real 3-route journey, not just a single-pair color transition; depth reads as front/middle/rear through six calibrated perceptual channels, not two; the spring was retuned for a faster grab — and, in the process of tuning it, a real numerical-stability bug was found and fixed (see below, the most important finding of this pass); the "attention hierarchy" is now a genuine 4-tier model with its own behavioral consequence, not the old 3-bucket role renamed; a directional anticipation cue now hints at more content without ever drawing an arrow; and sound/haptics gained a manual calibration mode for exactly the kind of per-event auditioning this report needed to write honestly.

## 1. Environmental Continuity — Formations → Roadmap → Module

Three real, independently-verified elements now survive and continuously morph across all three route boundaries, never reset:

1. **Light field** (`--glow-1/2/3` on `.env-base`, unchanged since H0.6) — already section-tinted and smoothly transitioning via registered `@property` custom colors.
2. **Structural/depth layer** (`--topo-depth`, from H0.9) — a real scale nudge (1.015 deeper / 0.988 shallower / 1 lateral) applied through `goto()`'s single funnel, so every route change gets it, camera-follow or plain switch alike.
3. **Formation-specific visual signature** (new this pass, `--formation-signature`) — each formation's own tint (grouped by pôle: FMS·Culture orange, MED·Publics green, NUM·Écritures blue), captured the moment the learner explicitly focuses a formation, threaded through **three** places at once: the persistent botanical blob (`.veg-blob.veg-signature`, same DOM node across every route), a 3px accent bar on the Roadmap current-stage card, and an accent dot before the Module eyebrow — none of them reset by `goto()`.

**Real bug found and fixed while building this**: the signature was first set as an inline style on `#backdrop`. Since `#backdrop` and `#app` are sibling subtrees (not ancestor/descendant), a CSS custom property set on `#backdrop` never reaches anything inside `#app` — confirmed via `getComputedStyle`, the Roadmap/Module accents kept showing the default orange no matter which formation was focused. Fixed by moving the assignment to `document.documentElement` (the one ancestor common to both subtrees) — re-verified immediately after, all three surfaces correctly showed the same live color.

**Verified this session** (`getComputedStyle`, not visual impression): focusing "Médiation des publics" (green, `#15803D`) in Formations, then navigating Formations→Roadmap→Module, the signature read green at every single checkpoint — botanical blob, Roadmap accent, Module accent — while `--topo-depth` correctly read `1` (Formations, lateral) → `1` (Roadmap, lateral) → `1.015` (Module, deeper).

**Proof sequence** (gallery, 0/20/40/60/80/100%): Hub at rest (default orange) → Formations entered (still default, no focus yet) → "Médiation" focused (signature begins morphing to green) → Roadmap (signature persists green, accent bar visible) → Module camera-follow mid-flight (captured via `?slowmo=6` for an honest in-flight frame, not a guessed wait) → Module settled (signature still green, `--topo-depth` = 1.015). Framed honestly in the gallery as **sequence checkpoints across the real multi-route journey**, not literal keyframes of one CSS animation — Formations→Roadmap→Module spans two separate navigations (a plain lateral switch, then a camera-follow transition), and claiming otherwise would overstate what's shown.

## 2. Perceptual Occlusion

`applyDepth()` (H0.9's continuous attention-weight function) now drives six calibrated channels instead of two:

- **SHARPNESS_DEPTH**: far blur recalibrated from H0.9's ≤0.5px to the Founder's explicit ≈1–1.5px ceiling (`(1-w)*1.3`); ACTIVE plane stays exactly at 0.
- **CONTRAST_DEPTH**: new — `contrast(0.72 + 0.28·w)`, front crisp/full-contrast, receded planes measurably flatter.
- **LIGHT_DIRECTION**: new — `brightness()` biased by horizontal position relative to the world's own light source (upper-left, matching `--env-light`'s position): two tiles at equal |distance| on opposite sides of the focus measurably differ in computed brightness, a real directional (not just distance-based) cue, calibrated small enough (±0.07 max) not to read as noise.
- **OVERLAP + MASKING**: new — real `z-index` driven by the same continuous weight (`Math.round(w*100)`), so the closer plane genuinely stacks above and visually occludes farther ones when motion brings them close, layered with the existing opacity/contrast/sharpness falloff — deliberately **not** implemented via an added shadow/markup layer, which would have fought the existing per-destination tinted target box-shadow already owned by CSS.

Verified structurally (channel values read via computed style across a range of distances) and visually (gallery screenshot #7: a fast-navigation sweep shows visibly graduated blur/contrast/brightness across five simultaneously-visible tiles, front-to-back legible at a glance, no added visual clutter).

## 3. Spring Tuning — and the real bug it surfaced

Retuned from H0.9's `(STIFFNESS=220, DAMPING=27)` — damping ratio ζ≈0.91 — to `(280, 33)`, ζ≈0.986: closer to critical (removing any last-mile wobble risk) while ~27% stiffer for a faster initial grab. Verified first in a standalone Node simulation of the exact integration formula before touching the file: a step to target=1 reaches 90% by 217ms in both configs (no regression), zero overshoot, and a 5-retarget rapid sweep (90ms apart) shows velocity genuinely accumulating (up to ~12 units/s) rather than resetting between retargets — momentum, not elasticity.

**A real numerical-stability bug was found and fixed before this ever reached the Founder.** The Node simulation used a clean, regular 60fps timestep; the live browser does not. Re-running the same simulation at this sandbox's actual worst-case frame delivery (dt clamped to the engine's 50ms ceiling — a real, measured condition here, not a hypothetical: this session's own frame-pacing sampler had already shown P99 ≈100–116ms) revealed that the retuned, stiffer spring **numerically diverges into a sustained, non-decaying oscillation** under semi-implicit Euler integration at large dt — settling into a limit cycle between ~0.78 and ~1.21 and never actually reaching the target. This is *exactly* the BOUNCE/RUBBER_BAND feel this pass was explicitly asked to eliminate — and it reproduced live in the browser (Playwright trace: position swinging 0.30↔1.52 with velocity never decaying below ±20). The old, softer H0.9 spring stayed stable at the same dt; the new one didn't — a genuine regression I introduced while trying to improve feel.

**Root cause and fix**: a single large integration step against a stiffer spring is what breaks. Fixed with **substepping** — a large frame's `dt` is now split into fixed ~8.3ms (120Hz) sub-steps before the spring is integrated, keeping the physics numerically stable no matter how choppy real frame delivery is, while leaving the response at a normal 60fps frame (2–3 sub-steps) effectively unchanged. Re-verified via the exact same Node simulation (clean convergence at the same worst-case 50ms dt) **and** live in the browser (`→ → ←` and `→ → → ← ←` traces below both show smooth, monotonic convergence, zero oscillation).

## 4. Reversal Quality

Live Playwright traces (rail-position/velocity read directly from the debug panel, not inferred):

- **`→ → ←`**: position climbs toward 2, then on the reversal press smoothly decelerates and converges to 1 — velocity magnitude decreasing every sample (11.5 → 0.25 → -0.35 → -0.31 → ... → -0.02), never re-accelerating away from the new target. No stop-reset-restart.
- **`→ → → ← ←`**: same pattern at target=2 — velocity -6.38 → -7.01 → -4.30 → ... → -0.05, one clean monotonic brake-and-continue, never a double-bounce.

Both reproduced the H0.9-era spring's sustained-oscillation failure mode *before* the substep fix, and both converge cleanly *after* it — the clearest evidence this pass has that the fix is real, not cosmetic.

## 5. Fast Navigation

`→ → → → →` at a realistic rapid cadence (45ms apart) drove `CADENCE` to `FAST_REPEAT` (streak 5) with position sweeping fractionally (4.59 → 4.99) toward target=5 while every keypress was accepted immediately — no queued navigation, no delayed focus commit (the semantic `data-role`/`data-attention`/DOM-focus target all commit synchronously per keypress, independent of where the physics has visually caught up to), and the context dock/quiz cycle tested cleanly in the same session with zero flicker. `final focus after rapid nav` matched the last keypress exactly, confirming no dropped or misapplied input.

## 6. Attention Hierarchy — a real 4-tier model

`attentionTier(distance, weight)` replaces the H0.9 comment's aspiration with an actual implementation: `PRIMARY_ATTENTION` (the one tile at `round(distance)===0`), `SECONDARY_CONTEXT` (`weight≥0.28`), `PERIPHERAL_CONTEXT` (`weight≥0.08`), `LATENT_CONTEXT` (below that) — boundaries on the **continuous** attention weight, not the old rounded-distance 3-bucket. Recomputed every animation frame from the live physics position (not the committed target), so a tile genuinely sweeps through all four tiers during fast navigation.

**A real behavioral consequence, not a relabeled bucket**: `LATENT_CONTEXT` tiles get `aria-hidden="true"` — present spatially (still reachable by an arrow-key jump), but a screen reader walking the page skips them, while `PERIPHERAL_CONTEXT` stays fully in the accessibility tree. `data-role` (target/adjacent/far) is kept **only** because existing CSS selectors already key layout/CTA visibility off it — it is now presentational shorthand for the same PRIMARY boundary, not a second competing model.

**Verified**: `PRIMARY_ATTENTION` count sampled across 8 frames of an active mid-sweep — exactly one, every single frame, including the two frames where the identity of that one tile changed mid-transition. `aria-hidden` read directly off the two `LATENT_CONTEXT` tiles at rest: both `"true"`; every other tile: `"false"`.

## 7. Spatial Anticipation

A soft, purely CSS directional edge-glow (`.rail-viewport::before/::after`) appears **only** on the side where content genuinely continues — computed from the real item count (`applyAnticipationCue`), never both edges "just because," never an arrow or icon. Verified: at the first focusable item, `moreLeft=false / moreRight=true`; at the last, `moreLeft=true / moreRight=true` (correct — the disabled "À venir" tile is real, visible content one position further right, so the cue is honest about it even though that tile isn't keyboard-reachable — VISIBILITY ≠ ATTENTION, not a bug). Disabled entirely under reduced motion.

## 8. Sound Calibration

Kept the H0.9 Web Audio architecture completely unchanged. Added a **Calibration Mode** panel (🎛, next to the existing sound toggle) listing all 8 events (`NAV_MOVE, FOCUS_LOCK, ENTER_DEPTH, RETURN_DEPTH, CONTEXT_OPEN, CONTEXT_CLOSE, CONFIRM, BLOCKED`) as individually-clickable buttons, each calling a new `SpatialAudio.audition(kind)` — deliberately bypassing the `enabled` opt-in gate and the `NAV_MOVE` throttle (you're inspecting one event in isolation, not simulating real usage), while still only ever running from a real click (autoplay-restriction compliant). All 8 auditioned this session with zero errors. The real machine-gun-audio protection is unchanged from H0.9 and unaffected by this pass — `NAV_MOVE`'s 40ms/90ms throttle depends only on `cadence.state`/timestamps, not on the spring's constants, and normal (non-calibration) rapid navigation was re-verified quiet.

## 9. Haptic Calibration

Same pattern: `Haptics.audition(kind)` added, bypassing the shared opt-in gate for manual, isolated testing of all 5 patterns (`FOCUS_LOCK, SNAP, ENTER, CONFIRM, BLOCKED`) via the same calibration panel — all 5 fired with zero errors. `SNAP` still fires exactly once at drag-commit, never continuously during the drag itself (unchanged from H0.9, re-verified via a mobile-emulated drag this session).

## 10. Frame Pacing — diagnostic only, as instructed

Re-measured after tuning, during an active 10-keypress rapid-nav burst: mean 25.4ms, P95 50ms, P99 100.1ms, 39/130 frames flagged "dropped" (>33ms). **Kept explicitly diagnostic, not a hardware claim** — this sandbox is a resource-constrained, single-core, headless CI environment, not representative of a real device. The number that actually matters this pass isn't the ms figure, it's what it exposed: this environment routinely delivers frame deltas large enough to destabilize a naive spring integrator (see §3) — a real, generalizable finding, independent of exactly how slow this particular sandbox is.

- **Layout reads during rAF**: none. `hubOnFrame`/`formationsOnFrame` (the only functions on the physics rAF path) call `applyDepth()` (pure `element.style` writes) and `panCamera()` (reads only `window.innerWidth`, never a tile's geometry) — no `getBoundingClientRect()` on the animated elements inside the per-frame loop. The only `getBoundingClientRect()` calls (`centerInRail`/`centerInStage`) run once per discrete focus-commit event, not per frame — confirmed by code inspection, not just absence of visible jank.
- **Filter cost**: `applyDepth`'s filter string grew from 2 terms (saturate+blur) to 4 (saturate+contrast+brightness+blur) this pass — a real, disclosed added cost per tile per frame, not measured in isolation this session (no CDP performance trace was run; disclosed as a scope limit, not hidden).
- **Compositor layers**: not measured via a DevTools layer trace this session (same disclosed scope limit as every prior report in this lineage) — the new `z-index` write per tile could, in principle, promote more tiles to their own compositor layer than the DOM-order stacking used before; not verified either way.

## Known gaps and limitations (disclosed, not silently dropped)

1. Filter-cost and compositor-layer impact of the added occlusion channels not measured via a real performance trace this session (see §10) — a real hardware + DevTools-trace pass is needed before either is a settled claim.
2. The environmental-continuity "0-100%" sequence is honestly framed as checkpoints across a real multi-route journey, not literal keyframes of one continuous CSS animation (Formations→Roadmap→Module is two separate navigations) — see §1.
3. No audible/tactile verification of the calibration mode's actual sound/vibration output — this sandbox has neither speakers nor a vibration motor; verified structurally (every audition call throws no error) as in every prior wave.
4. All disclosed H0.8/H0.9 gaps carry forward unchanged: no Formations↔Roadmap camera-follow anchor (still not a real IA relationship, not invented), no NVDA/VoiceOver manual pass, the `?slowmo` debug-readout cosmetic artifact at extreme slowdown, the autofocus race-protection control remains a manual prototype-only debug button.

## Full regression (H0.5–H0.9 systems, re-run against H0.10)

All via Playwright, `pageerror`/console-error listeners attached throughout — **zero errors across the entire battery**:
- Full 6-section route sweep: `data-current` correct, `window.scrollY===0` at every checkpoint.
- All three camera-follow anchors (Hub "Continuer", Formations target card, Roadmap current-stage card) into Module **and** both return paths (explicit "← Retour" link and browser Back) — all six paths still land correctly.
- Context dock: focus trap confirmed (`document.activeElement` inside `#contextDock` while open), exact focus return to the opener confirmed after close.
- Reduced motion, full round trip: instant Hub→Module→Hub, back-link text present and correct (the exact H0.8-era regression class).
- Mobile drag: touch-emulated swipe correctly re-focused, zero scroll drift, zero errors.

## Founder decision requested

Per the acceptance question in the brief — *"When I move my attention, does the entire Academy world immediately reorganize around me without ever making me wait?"* — this session's own answer is **yes, with one caveat disclosed above (§10, unmeasured filter/compositor cost) that a real-hardware pass should close before treating it as fully settled.** Every other named check in the brief (environmental continuity, perceptual occlusion, spring reversal/fast-nav quality, real attention hierarchy, anticipation, sound/haptic calibration) was built and verified this session with live evidence, not narrated claims.

`STOP = TRUE`. `H1 = NOT_AUTHORIZED`. Waiting for:
- **H0.10 = FREEZE_CANDIDATE** — treat this as the ceiling for the prototype track; next step would be planning H1 integration.
- **REVISE_DIRECTION** — specify what to change; this file gets revised again, in place, without resetting.
- **REJECT_DIRECTION** — direction dropped; H0.9 (still intact at its own URL) stands as the ceiling.
