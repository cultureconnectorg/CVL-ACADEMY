/**
 * Spatial Learning — depth primitives (W1-B, foundation only).
 *
 * One component per MOTION_SYSTEM row (source dossier, sheet
 * MOTION_SYSTEM). Each docstring below is that row's own ALLOWED /
 * FORBIDDEN pair, verbatim — these aren't free interpretations, they're
 * the literal constraint each primitive must honor. Built on
 * `framer-motion` (already a project dependency — see docs/
 * SPATIAL_LEARNING_W0_AUDIT.md §3, "already there, never wired up") so
 * this wave adds no new library.
 *
 * **Nothing here is mounted on any page.** `VISIBLE_SPATIAL_LEARNING =
 * NOT_AUTHORIZED` per the mission's own authorization state — these
 * exist so a later, separately-approved wave has correct, tested
 * primitives to compose rather than inventing motion ad hoc per screen.
 * All eight consult `useReducedMotion()` and collapse to their `motionDuration`
 * floor (1ms) rather than skip state changes outright, so reduced-motion
 * users still reach the same end state MOT-029 requires.
 */

import { motion } from "framer-motion";
import { MOTION_DURATIONS, MOTION_EASING, motionDuration } from "@/lib/motion-tokens";
import { useReducedMotion } from "@/lib/useReducedMotion";

function useDur(key) {
  const reduced = useReducedMotion();
  return motionDuration(key, reduced) / 1000; // framer-motion durations are in seconds
}

/** FOCUS — make one object primary.
 * ALLOWED: minor scale/position/light/opacity change.
 * FORBIDDEN: border/pill explosion; generic scale hover. */
export function Focus({ active, children, className }) {
  const duration = useDur("focus");
  return (
    <motion.div
      className={className}
      animate={{ scale: active ? 1.015 : 1, opacity: active ? 1 : 0.92 }}
      transition={{ duration, ease: MOTION_EASING.standard }}
    >
      {children}
    </motion.div>
  );
}

/** APPROACH — move chosen knowledge toward the learner.
 * ALLOWED: translateZ/scale/context reveal.
 * FORBIDDEN: decorative camera swoop. */
export function Approach({ active, children, className }) {
  const duration = useDur("approach");
  return (
    <motion.div
      className={className}
      animate={{ scale: active ? 1.03 : 1, y: active ? -4 : 0 }}
      transition={{ duration, ease: MOTION_EASING.standard }}
    >
      {children}
    </motion.div>
  );
}

/** ENTER — turn the selected object into a destination.
 * ALLOWED: continuous route transition.
 * FORBIDDEN: full reload/white flash. */
export function Enter({ show, children, className }) {
  const duration = useDur("enter");
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: show ? 1 : 0, scale: show ? 1 : 0.98 }}
      transition={{ duration, ease: MOTION_EASING.enter }}
    >
      {children}
    </motion.div>
  );
}

/** RECEDE — keep secondary context available.
 * ALLOWED: lower contrast/depth.
 * FORBIDDEN: disappear irretrievably — this primitive never unmounts its
 * children, only dims them; removing content is the caller's decision,
 * not this primitive's. */
export function Recede({ active, children, className }) {
  const duration = useDur("recede");
  return (
    <motion.div
      className={className}
      animate={{ opacity: active ? 0.55 : 1, filter: active ? "saturate(0.7)" : "saturate(1)" }}
      transition={{ duration, ease: MOTION_EASING.exit }}
    >
      {children}
    </motion.div>
  );
}

/** REVEAL — show context when needed.
 * ALLOWED: opacity/position/context layer.
 * FORBIDDEN: permanent clutter — callers are responsible for hiding this
 * again once its context is no longer relevant. */
export function Reveal({ show, children, className }) {
  const duration = useDur("reveal");
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: show ? 1 : 0, y: show ? 0 : 8 }}
      transition={{ duration, ease: MOTION_EASING.standard }}
      style={{ pointerEvents: show ? "auto" : "none" }}
    >
      {children}
    </motion.div>
  );
}

/** RETURN — restore exact prior context.
 * ALLOWED: reverse layer + state restoration.
 * FORBIDDEN: reset to top/home — callers must pass the actual prior
 * state back in, this primitive only supplies the transition, never a
 * default destination. */
export function Return({ show, children, className }) {
  const duration = useDur("return");
  return (
    <motion.div
      className={className}
      animate={{ opacity: show ? 1 : 0, scale: show ? 1 : 1.02 }}
      transition={{ duration, ease: MOTION_EASING.enter }}
    >
      {children}
    </motion.div>
  );
}

/** CONFIRM — acknowledge a validated action.
 * ALLOWED: short restrained physical feedback.
 * FORBIDDEN: confetti/default celebration. */
export function Confirm({ triggerKey, children, className }) {
  const duration = useDur("confirm");
  return (
    <motion.div
      className={className}
      key={triggerKey}
      initial={{ scale: 0.96 }}
      animate={{ scale: 1 }}
      transition={{ duration, ease: MOTION_EASING.standard }}
    >
      {children}
    </motion.div>
  );
}

/** HORIZON — expose the next possibility.
 * ALLOWED: subdued distant cue.
 * FORBIDDEN: false unlock/availability — this primitive only renders
 * what the caller passes it; it must never imply a locked module is
 * reachable. */
export function Horizon({ visible, children, className }) {
  const duration = useDur("horizon");
  return (
    <motion.div
      className={className}
      animate={{ opacity: visible ? 0.65 : 0 }}
      transition={{ duration, ease: MOTION_EASING.standard }}
    >
      {children}
    </motion.div>
  );
}

// Re-exported for anything that needs the raw numbers/curves rather than
// a wrapped primitive (e.g. composing a custom framer-motion variant).
export { MOTION_DURATIONS, MOTION_EASING };
