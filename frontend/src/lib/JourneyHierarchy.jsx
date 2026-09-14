/**
 * ModuleJourney spatial shell — visual depth hierarchy between the
 * seven phases of a module. Domain state remains authoritative in
 * ModuleJourney.js; this file is presentation-only.
 */

import { motion } from "framer-motion";
import { MOTION_EASING, motionDuration } from "@/lib/motion-tokens";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { useDepthPhysics } from "@/lib/useDepthPhysics";
import { computeDepthStyle } from "@/lib/spatial/attention";
import { FEATURE_FLAGS } from "@/lib/featureFlags";

export const JOURNEY_ROLES = Object.freeze({
  CURRENT: "current",
  ACQUIRED: "acquired",
  NEXT: "next",
  LOCKED: "locked",
});

export function deriveJourneyRole({ isOpen, done, canOpen }) {
  if (isOpen) return JOURNEY_ROLES.CURRENT;
  if (done) return JOURNEY_ROLES.ACQUIRED;
  if (canOpen) return JOURNEY_ROLES.NEXT;
  return JOURNEY_ROLES.LOCKED;
}

export const JOURNEY_VARIANTS = Object.freeze({
  current: { scale: 1.01, opacity: 1, filter: "saturate(1)" },
  acquired: { scale: 1, opacity: 0.88, filter: "saturate(0.9)" },
  next: { scale: 1, opacity: 0.7, filter: "saturate(0.85)" },
  locked: { scale: 1, opacity: 0.45, filter: "saturate(0.55)" },
});

const DURATION_KEY_BY_ROLE = Object.freeze({
  current: "approach",
  acquired: "recede",
  next: "horizon",
  locked: "recede",
});

export function JourneyPhaseShell({ isOpen, done, canOpen, idx, currentIdx, children, className }) {
  const reduced = useReducedMotion();
  const role = deriveJourneyRole({ isOpen, done, canOpen });
  const spatialClass = FEATURE_FLAGS.SPATIAL_MODULE_DEPTH ? "spatial-phase-shell" : "";
  const classes = [className, spatialClass].filter(Boolean).join(" ");

  if (FEATURE_FLAGS.SPATIAL_MODULE_DEPTH && typeof idx === "number" && typeof currentIdx === "number") {
    return (
      <PhysicsPhaseShell role={role} idx={idx} currentIdx={currentIdx} reduced={reduced} className={classes}>
        {children}
      </PhysicsPhaseShell>
    );
  }

  const duration = motionDuration(DURATION_KEY_BY_ROLE[role], reduced) / 1000;
  return (
    <motion.div
      className={classes}
      animate={JOURNEY_VARIANTS[role]}
      transition={{ duration, ease: MOTION_EASING.standard }}
      data-journey-role={role}
    >
      {children}
    </motion.div>
  );
}

function PhysicsPhaseShell({ role, idx, currentIdx, reduced, children, className }) {
  const rawDistance = idx - currentIdx;
  const targetDistance = role === JOURNEY_ROLES.LOCKED ? Math.max(rawDistance, 2) : rawDistance;
  const distance = useDepthPhysics(targetDistance, { reduced });
  const depth = computeDepthStyle(distance, { mobile: false });
  const style = reduced
    ? { opacity: depth.opacity, transform: `scale(${Math.max(depth.scale, 0.94)})` }
    : {
        opacity: depth.opacity,
        filter: `saturate(${depth.saturate}) contrast(${depth.contrast}) brightness(${depth.brightness})`,
        transform: `translateY(${depth.translateY * 0.3}px) translateZ(${depth.translateZ}px) scale(${depth.scale})`,
      };
  return (
    <div
      className={className}
      style={style}
      data-journey-role={role}
      data-tier={depth.tier}
      data-phase-depth={Math.round(distance * 100) / 100}
    >
      {children}
    </div>
  );
}
