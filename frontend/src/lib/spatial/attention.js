/**
 * Spatial Learning — attention model (W-FUNNEL-1, extracted from H0.10
 * + H0.8's autofocus engine).
 *
 * H0.10 SUBSYSTEM EXTRACTION CLASSIFICATION: ADAPT.
 * H0.10's `attentionWeight`/`attentionTier`/`applyDepth` were tightly
 * coupled to specific prototype CSS custom properties (`--formation-
 * signature`, `--topo-depth`) and to the DOM directly (`el.style.*`,
 * `el.dataset.*`, `el.setAttribute('aria-hidden', ...)`). This module
 * ports the *pure math* (REUSE-grade, unchanged formulas) but separates
 * it from DOM application (ADAPT-grade — a caller decides what to do
 * with the numbers, this module never touches `document`).
 *
 * Distinct from `frontend/src/lib/spatial-state.js` (W1-D): that module
 * tracks the screen-level macro phase (IDLE/FOCUS/APPROACH/ENTER/
 * ACTIVE/CONTEXT/RETURN) a whole view moves through. This module tracks
 * *which object, among several simultaneously-visible ones, currently
 * holds attention* — the mission's own DOM_FOCUS / SPATIAL_FOCUS /
 * CAMERA_FOCUS / DOMAIN_SELECTION distinction. Both are real, and
 * neither replaces the other: a screen can be in spatial-state ACTIVE
 * while this module's PRIMARY_ATTENTION object changes several times
 * (arrow-key navigation within a rail, for instance).
 *
 * Exactly one PRIMARY_ATTENTION target at any moment is the one hard
 * invariant this module exists to guarantee — verified in attention.
 * test.js, same guarantee H0.10's own Playwright proof established
 * (docs/SPATIAL_H10_PERCEPTUAL_REFINEMENT_REPORT.md §6).
 */

/** The 4 real tiers — not ACTIVE/ADJACENT/FAR renamed. Boundaries are
 * continuous-weight ranges, not a rounded-distance bucket, so an object
 * genuinely sweeps through all four during fast, continuous motion. */
export const ATTENTION_TIERS = Object.freeze({
  PRIMARY: "PRIMARY_ATTENTION",
  SECONDARY: "SECONDARY_CONTEXT",
  PERIPHERAL: "PERIPHERAL_CONTEXT",
  LATENT: "LATENT_CONTEXT",
});

/** 1 at the focal point, falling off continuously (never a step
 * function) as `distance` (in the same units as the physics module's
 * `position`/`target` — typically index units) grows. */
export function attentionWeight(distance) {
  const absD = Math.abs(distance);
  return 1 / (1 + absD * absD * 0.55);
}

/**
 * The real 4-tier classification. `Math.round(distance) === 0` is
 * unique except at a transient .5 tie mid-flight (favors the lower
 * index) — this is what guarantees exactly one PRIMARY_ATTENTION.
 */
export function attentionTier(distance, weight = attentionWeight(distance)) {
  if (Math.round(distance) === 0) return ATTENTION_TIERS.PRIMARY;
  if (weight >= 0.28) return ATTENTION_TIERS.SECONDARY;
  if (weight >= 0.08) return ATTENTION_TIERS.PERIPHERAL;
  return ATTENTION_TIERS.LATENT;
}

/**
 * Pure depth-styling computation — 6 perceptual-occlusion channels
 * (H0.10's calibrated formulas, unchanged): translateZ/scale/opacity/
 * saturation/contrast/brightness/blur/z-index, plus a light-direction
 * bias. Returns a plain object; the caller applies it however its
 * rendering layer prefers (inline style, a CSS-in-JS prop, a data
 * attribute driving CSS variables — this module doesn't decide).
 *
 * `mobile` narrows perspective strength (weaker rotateY/Z) — same
 * H0.10 rule, now an explicit parameter instead of a `window.
 * innerWidth` read baked into the function (SSR/test-safety).
 */
export function computeDepthStyle(distance, { mobile = false } = {}) {
  const absD = Math.abs(distance);
  const w = attentionWeight(distance);
  const z = (-96 + 152 * w) * (mobile ? 0.5 : 1);
  const scale = 0.79 + 0.21 * w;
  const opacity = 0.22 + 0.78 * w;
  const saturate = 0.4 + 0.6 * w;
  const blur = Math.max(0, (1 - w) * 1.3); // far <=~1.3px, active 0 — H0.10 §2 calibration
  const contrast = 0.72 + 0.28 * w;
  const translateY = 16 - 26 * w;
  const dir = distance === 0 ? 0 : distance > 0 ? 1 : -1;
  const translateX = distance * Math.min(absD, 3) * 13;
  let rotateY = dir * (1 - w) * -5.5;
  if (mobile) rotateY *= 0.3;
  // light-direction bias: a real, directional (not just distance-based)
  // brightness cue toward wherever the world's own light source sits —
  // callers pass their own light-origin sign via `translateX`'s own
  // convention (positive = away from a left-sited light, by default).
  const brightness = Math.max(0.85, Math.min(1.05, 0.93 + 0.09 * w - translateX * 0.0006));
  const zIndex = Math.round(w * 100);
  const tier = attentionTier(distance, w);
  return {
    weight: w,
    tier,
    translateX,
    translateY,
    translateZ: z,
    rotateY,
    scale,
    opacity,
    saturate,
    contrast,
    brightness,
    blur,
    zIndex,
    // LATENT_CONTEXT's real behavioral consequence (H0.10 §6): present
    // spatially, absent from the accessibility tree — a caller applying
    // this to a real DOM node should set aria-hidden accordingly.
    ariaHidden: tier === ATTENTION_TIERS.LATENT,
  };
}

/**
 * Deterministic focus prediction (H0.10 §, ported unchanged) — only
 * active during a consistent-direction repeated-input cadence (see
 * cadence.js), only one step ahead, never near a boundary. Never
 * commits selection — a caller surfaces this as a barely-visible cue,
 * nothing more.
 */
export function predictNextIndex(count, currentIdx, cadenceState, lastDir) {
  if ((cadenceState !== "REPEATED" && cadenceState !== "FAST_REPEAT") || lastDir === 0) {
    return -1;
  }
  const next = currentIdx + lastDir;
  return next >= 0 && next < count ? next : -1;
}

/**
 * Async autofocus race protection (H0.8's engine, ported). A caller
 * requests an automatic focus change (e.g. a background recommendation
 * arriving); if the learner makes an explicit choice (keyboard/pointer/
 * touch) before the delayed request resolves, the automatic change must
 * be discarded — LATEST_EXPLICIT_USER_INTENT_WINS, never a stale
 * autofocus stealing focus after the fact.
 */
export function createAutofocusGuard(deps = {}) {
  // Monotonically-increasing tie-breaking clock, not just Date.now(): two
  // synchronous calls (a real risk — e.g. a test, or two events in the
  // same microtask) can land in the same millisecond, and a stale
  // request must never win a genuine tie against a later explicit
  // intent. Injectable for deterministic testing.
  let tick = 0;
  const now = deps.now || (() => ++tick);
  let lastExplicitIntentAt = -1;
  let requestId = 0;

  return {
    /** Call on every explicit (keyboard/pointer/touch) focus change. */
    noteExplicitIntent() {
      lastExplicitIntentAt = now();
    },
    /**
     * Registers an automatic focus request. `apply` runs only if no
     * explicit intent landed at or after `requestedAt` and no newer
     * automatic request has superseded this one.
     */
    request(apply) {
      const myId = ++requestId;
      const requestedAt = now();
      return {
        resolve() {
          if (myId !== requestId) return; // superseded by a newer auto request
          if (lastExplicitIntentAt >= requestedAt) return; // explicit intent wins, ties included
          apply();
        },
      };
    },
  };
}
