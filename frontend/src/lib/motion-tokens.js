/**
 * Spatial Learning — central motion tokens (W1-B, foundation only).
 *
 * Durations/easing here mirror MOTION_SYSTEM in the source dossier
 * (`CVLN_Academy_Expert_Tech_Master_Dossier.xlsx`, sheet MOTION_SYSTEM) —
 * one row per semantic primitive, not a decorative animation library.
 * Nothing in this module is imported by any page yet: this is
 * infrastructure the way `framer-motion` itself already was before this
 * wave (a real dependency, never wired up) — VISIBLE_SPATIAL_LEARNING
 * stays NOT_AUTHORIZED until a later, separately-approved wave mounts a
 * primitive on an actual screen.
 *
 * MOT-026 "Central timing tokens" / MOT-027 "Restrained easing": every
 * duration used to exist scattered as a literal in index.css (240ms,
 * 220ms, 500ms) — this is the single place any future motion work reads
 * timing from instead of re-inventing a number per component.
 */

// One entry per MOTION_SYSTEM primitive — durations in ms, deliberately
// short and restrained (MOT-008 "Calm by default", MOT-027). FOCUS/CONFIRM
// are the shortest (a small, immediate acknowledgment); ENTER/RETURN are
// the longest (a full context change still has to read as continuous,
// MOT-013, not abrupt).
export const MOTION_DURATIONS = {
  focus: 160, // FOCUS — make one object primary: minor scale/position/light change
  approach: 320, // APPROACH — move chosen knowledge toward the learner
  enter: 420, // ENTER — turn the selected object into a destination (route transition)
  recede: 240, // RECEDE — keep secondary context available, lower contrast/depth
  reveal: 200, // REVEAL — show context when needed
  return: 340, // RETURN — restore exact prior context
  confirm: 150, // CONFIRM — short restrained acknowledgment of a validated action
  horizon: 260, // HORIZON — subdued cue for the next possibility
};

// Restrained, non-bouncy curves only (MOT-027 forbids anything that reads
// as playful/elastic — this is a professional learning tool, not a game).
export const MOTION_EASING = {
  standard: [0.4, 0.0, 0.2, 1], // calm accelerate/decelerate, the default for most primitives
  enter: [0.16, 1, 0.3, 1], // slightly slower settle, for ENTER/RETURN (bigger context changes)
  exit: [0.4, 0.0, 1, 1], // quick, no lingering, for RECEDE
};

/**
 * True while the OS-level "reduce motion" preference is set. Mirrors the
 * CSS `@media (prefers-reduced-motion: reduce)` block added in W1-A
 * (index.css) for the JS side: framer-motion variants read transform/
 * opacity via inline styles, which the CSS media query cannot reach, so
 * any future motion primitive must consult this hook and either skip the
 * animation or collapse its duration — never just rely on the CSS rule.
 */
export function prefersReducedMotion() {
  if (typeof window === "undefined" || !window.matchMedia) return false;
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

/**
 * MOT-029 "Reduced motion equivalence" — the duration a primitive should
 * actually use once the user's preference is taken into account. Never
 * returns exactly 0 (a framer-motion transition of 0 can skip firing
 * `onAnimationComplete` in some cases) — 1ms is imperceptible but still a
 * real, completing transition.
 */
export function motionDuration(key, reduced = prefersReducedMotion()) {
  if (reduced) return 1;
  const value = MOTION_DURATIONS[key];
  if (value == null) {
    throw new Error(`motion-tokens: unknown duration key "${key}"`);
  }
  return value;
}
