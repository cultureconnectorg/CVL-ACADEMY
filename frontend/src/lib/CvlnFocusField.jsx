/**
 * CVLN_FOCUS_FIELD v1 (W2-C) — reusable "target / secondary / related
 * context" composition. Landing's W2-B usages (FOCUS on the language
 * pill, ENTER on the mode swap) were deliberately kept separate from
 * this — see docs/SPATIAL_LEARNING_W2B_LANDING_REPORT.md — because
 * neither had a genuine target/secondary/related-context relationship.
 * This is the reusable home for that pattern; W2-D is where it gets
 * applied to a real screen (formation discovery).
 *
 * Behavior contract (per the W2 authorization):
 *   TARGET          -> APPROACH   (the focused item moves toward the learner)
 *   SECONDARY       -> RECEDE     (every other item dims, never disappears)
 *   RELATED_CONTEXT -> REVEAL     (optional context tied to the target)
 *   IDLE            -> CALM       (nothing focused = nothing animated = rest state)
 *
 * A single item is one continuous `motion.div` across all three roles —
 * rather than nesting the standalone `Approach`/`Recede` primitives from
 * motion-primitives.jsx, which are separate component types and would
 * unmount/remount on a role change, losing the animated interpolation —
 * so target -> secondary -> idle always interpolates smoothly through
 * one element, using the same central tokens (motion-tokens.js) the
 * atomic primitives already read from.
 *
 * Forbidden by the W2-C authorization, and how this file avoids each:
 * - NO_GENERIC_SCALE_HOVER: role is driven entirely by `focusedId`
 *   (click/keyboard selection, or any controlled value the caller
 *   passes) — never CSS `:hover`. `useFocusField` exposes no hover
 *   state at all, and `FocusFieldItem` attaches no `onMouseEnter`.
 * - NO_EXCESSIVE_CARDS: this file renders zero visual chrome (no
 *   background/border/shadow of its own) — `className` is entirely the
 *   caller's; `FocusFieldItem` only ever animates transform/opacity.
 * - NO_PILLS_AS_HIERARCHY: hierarchy is expressed only through the
 *   scale/opacity/saturation this field computes, never a badge/pill.
 * - NO_DECORATIVE_3D: 2D transforms only (scale, translateY) — no
 *   rotateX/rotateY/perspective anywhere in this file.
 * - NO_PARTICLE_BACKGROUND / NO_WEBGL: DOM/CSS motion only
 *   (framer-motion over regular elements) — nothing canvas- or
 *   WebGL-based.
 * - NO_PLAYSTATION_COPY: no menu chrome, icon carousel, or layout is
 *   prescribed here at all — this is a behavioral primitive a caller
 *   composes into their own visual design, not a themed component.
 */

import { motion } from "framer-motion";
import { useCallback, useState } from "react";
import { MOTION_DURATIONS, MOTION_EASING, motionDuration } from "@/lib/motion-tokens";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { Reveal } from "@/lib/motion-primitives";

/**
 * Pure role derivation — no React, no motion — so the field's core rule
 * ("what role does item X play given the current target?") is unit
 * testable on its own, the same way spatial-state.js's transition table
 * is (see spatial-state.test.js). `FocusFieldItem` below is a thin
 * wrapper around this.
 */
export function deriveFocusRole(id, focusedId) {
  if (focusedId == null) return "idle";
  return id === focusedId ? "target" : "secondary";
}

// One variant per role — the only three visual states a field item can
// ever be in. Kept as plain data (not JSX) so the mapping itself is
// inspectable/testable independent of framer-motion.
export const FOCUS_FIELD_VARIANTS = Object.freeze({
  idle: { scale: 1, y: 0, opacity: 1, filter: "saturate(1)" },
  target: { scale: 1.03, y: -4, opacity: 1, filter: "saturate(1)" },
  secondary: { scale: 1, y: 0, opacity: 0.55, filter: "saturate(0.7)" },
});

/**
 * Minimal focus state for a field of items. Deliberately has no hover
 * state — see NO_GENERIC_SCALE_HOVER above. Uncontrolled by default
 * (`initialId`); a caller that needs controlled state can ignore this
 * hook and pass its own `focusedId` straight to `FocusFieldItem`.
 */
export function useFocusField(initialId = null) {
  const [focusedId, setFocusedId] = useState(initialId);
  const focus = useCallback((id) => setFocusedId(id), []);
  const clear = useCallback(() => setFocusedId(null), []);
  return { focusedId, focus, clear };
}

/**
 * One item inside a focus field.
 *
 * @param id        this item's identity
 * @param focusedId the field's current target id (or null/undefined = IDLE)
 */
export function FocusFieldItem({ id, focusedId, children, className, ...rest }) {
  const reduced = useReducedMotion();
  const role = deriveFocusRole(id, focusedId);

  // APPROACH and RECEDE carry different durations in the token system —
  // moving toward a target reads calmer/slightly slower than the recede
  // response. Use APPROACH's duration for becoming/being the target and
  // for settling back to idle (a "settle" reads closer to an approach
  // than a recede), RECEDE's duration only while actually dimming.
  const duration = motionDuration(role === "secondary" ? "recede" : "approach", reduced) / 1000;
  const ease = role === "secondary" ? MOTION_EASING.exit : MOTION_EASING.standard;

  return (
    <motion.div
      className={className}
      animate={FOCUS_FIELD_VARIANTS[role]}
      transition={{ duration, ease }}
      data-focus-role={role}
      {...rest}
    >
      {children}
    </motion.div>
  );
}

/**
 * RELATED_CONTEXT -> REVEAL. Thin, named wrapper over the existing
 * `Reveal` primitive so a field's related-context usage reads as
 * intentional rather than as a bare, unlabeled import.
 */
export function FocusFieldContext({ show, children, className }) {
  return (
    <Reveal show={show} className={className}>
      {children}
    </Reveal>
  );
}

// Re-exported so a caller building a custom variant reads from the same
// tokens FocusFieldItem itself does.
export { MOTION_DURATIONS, MOTION_EASING };
