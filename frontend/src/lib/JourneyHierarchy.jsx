/**
 * ModuleJourney spatial shell (W3-A) — visual depth hierarchy between the
 * 7 phases of a single module (hook -> objectives -> course -> workshop
 * -> deliverable -> quiz -> mini_mission), built entirely on top of
 * data ModuleJourney.js already computes (`phase_flags`, `openPhase`,
 * the existing `canOpen` derivation) — this file adds no new business
 * rule and reads no new field.
 *
 * Doctrine:
 *   CURRENT  -> FOREGROUND            (the open phase)
 *   ACQUIRED -> BEHIND_BUT_ACCESSIBLE (done, not open — still fully clickable)
 *   NEXT     -> HORIZON               (the one reachable, not-yet-entered
 *                                       phase — genuinely unlocked, so this
 *                                       is a legitimate HORIZON use per its
 *                                       own contract: "expose the next
 *                                       possibility", never a false unlock)
 *   LOCKED   -> DISTANT_SUBDUED       (not yet reachable)
 *
 * Forbidden by the W3-A authorization, and how this file avoids each:
 * - MODULE_CONTENT_CHANGE / MODULE_CODE_CHANGE: this file renders no
 *   content and reads no module/code field at all — it only classifies
 *   phase *position* (open/done/reachable), a purely presentational
 *   concern already implicit in ModuleJourney.js's own `canOpen` logic.
 * - PROGRESS_CHANGE: `deriveJourneyRole` never writes anything — it's a
 *   pure function of already-fetched state, called on every render, with
 *   zero side effects.
 * - UNLOCK_RULE_CHANGE: `canOpen` itself is computed by ModuleJourney.js
 *   exactly as before (`done || prevDone`) and passed in unchanged; this
 *   file only decides how a role *looks*, never whether a phase can open
 *   — the `disabled={!canOpen}` gate on the toggle button is untouched.
 */

import { motion } from "framer-motion";
import { MOTION_EASING, motionDuration } from "@/lib/motion-tokens";
import { useReducedMotion } from "@/lib/useReducedMotion";

export const JOURNEY_ROLES = Object.freeze({
  CURRENT: "current",
  ACQUIRED: "acquired",
  NEXT: "next",
  LOCKED: "locked",
});

/**
 * Pure role derivation — no React, no motion — unit tested directly in
 * JourneyHierarchy.test.js, the same pattern spatial-state.js and
 * CvlnFocusField.jsx's deriveFocusRole already established.
 *
 * @param isOpen  this phase is the one currently expanded (CURRENT candidate)
 * @param done    this phase's `phase_flags[key]` is true (ACQUIRED candidate)
 * @param canOpen ModuleJourney.js's own existing gate — unchanged, just read
 */
export function deriveJourneyRole({ isOpen, done, canOpen }) {
  if (isOpen) return JOURNEY_ROLES.CURRENT;
  if (done) return JOURNEY_ROLES.ACQUIRED;
  if (canOpen) return JOURNEY_ROLES.NEXT;
  return JOURNEY_ROLES.LOCKED;
}

// One variant per role — depth expressed only through scale/opacity/
// saturation, the same visual vocabulary motion-primitives.jsx and
// CvlnFocusField.jsx already use. CURRENT is the only role with any
// scale lift (FOREGROUND); ACQUIRED/NEXT/LOCKED form a deliberate
// opacity staircase (0.88 -> 0.7 -> 0.45) so "how far" a phase is reads
// at a glance without a single new color or icon.
export const JOURNEY_VARIANTS = Object.freeze({
  current: { scale: 1.01, opacity: 1, filter: "saturate(1)" },
  acquired: { scale: 1, opacity: 0.88, filter: "saturate(0.9)" },
  next: { scale: 1, opacity: 0.7, filter: "saturate(0.85)" },
  locked: { scale: 1, opacity: 0.45, filter: "saturate(0.55)" },
});

// Each role reads its transition pacing from the same central tokens the
// atomic primitives use (motion-tokens.js) — CURRENT settles at APPROACH
// speed, NEXT explicitly reuses the HORIZON duration (this *is* a HORIZON
// use), ACQUIRED/LOCKED both settle at RECEDE speed (both are a form of
// stepping back, just to different degrees).
const DURATION_KEY_BY_ROLE = Object.freeze({
  current: "approach",
  acquired: "recede",
  next: "horizon",
  locked: "recede",
});

/**
 * Wraps one phase card. `isOpen`/`done`/`canOpen` are exactly the values
 * ModuleJourney.js already computes per phase in its `.map()` — nothing
 * new is derived from module content or progress here.
 */
export function JourneyPhaseShell({ isOpen, done, canOpen, children, className }) {
  const reduced = useReducedMotion();
  const role = deriveJourneyRole({ isOpen, done, canOpen });
  const duration = motionDuration(DURATION_KEY_BY_ROLE[role], reduced) / 1000;

  return (
    <motion.div
      className={className}
      animate={JOURNEY_VARIANTS[role]}
      transition={{ duration, ease: MOTION_EASING.standard }}
      data-journey-role={role}
    >
      {children}
    </motion.div>
  );
}
