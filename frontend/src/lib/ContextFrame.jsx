/**
 * ACTIVE -> CONTEXT -> RETURN (W3-B) — the first real use of the W1-D
 * spatial state machine (`spatial-state.js`), built for exactly this:
 * "a later, separately-approved wave would drive which primitives fire
 * from which spatial state." `REVEAL_CONTEXT`/`DISMISS_CONTEXT` are the
 * existing, already-tested transitions this file wires to a visual
 * treatment — no new state-machine logic is added here.
 *
 * Applies to quiz / mini-mission / mentor context entries that happen
 * *inside* an already-ACTIVE screen (a module already open, a page
 * already loaded) — never to route-level navigation, which RouteTransition
 * (W2-A) already owns.
 *
 * Naming note, stated plainly rather than silently reinterpreted: "RETURN"
 * in the doctrine names the *motion* an exit uses — matching
 * motion-primitives.jsx's own `Return` primitive contract ("restore exact
 * prior context... never reset to a default destination") — not a jump
 * all the way to spatial-state.js's `IDLE`. Dismissing a context settles
 * the machine back at `ACTIVE` (`DISMISS_CONTEXT`), still on the same
 * screen, never navigating anywhere. `IDLE` is not reachable from this
 * hook at all (it starts at `ACTIVE` and only ever mixes with `CONTEXT`).
 */

import { motion } from "framer-motion";
import { useCallback } from "react";
import { MOTION_EASING, motionDuration } from "@/lib/motion-tokens";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { useSpatialState } from "@/lib/useSpatialState";
import { SPATIAL_STATES, SPATIAL_EVENTS } from "@/lib/spatial-state";

/**
 * `state` starts at ACTIVE (this hook is only ever used from within an
 * already-active screen — see the note above on IDLE). `enterContext`/
 * `leaveContext` are the only two events this hook ever dispatches;
 * anything else the machine would reject is simply not exposed here.
 */
export function useContextEntry() {
  const [state, dispatch] = useSpatialState(SPATIAL_STATES.ACTIVE);
  const enterContext = useCallback(() => dispatch(SPATIAL_EVENTS.REVEAL_CONTEXT), [dispatch]);
  const leaveContext = useCallback(() => dispatch(SPATIAL_EVENTS.DISMISS_CONTEXT), [dispatch]);
  return { state, isContext: state === SPATIAL_STATES.CONTEXT, enterContext, leaveContext };
}

/**
 * `show=true` -> CONTEXT entrance (REVEAL's own duration/easing: opacity
 * + a small upward settle). `show=false` -> RETURN's exit (opacity +
 * scale settle, RETURN's own duration/easing) — the frame stays mounted
 * either way (like `Reveal`), so a caller can drive `show` purely from
 * `isContext` without an unmount/remount losing the transition.
 */
export function ContextFrame({ show, children, className, ...rest }) {
  const reduced = useReducedMotion();
  const enterDuration = motionDuration("reveal", reduced) / 1000;
  const exitDuration = motionDuration("return", reduced) / 1000;

  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y: 8 }}
      animate={show ? { opacity: 1, y: 0, scale: 1 } : { opacity: 0, y: 0, scale: 1.02 }}
      transition={{
        duration: show ? enterDuration : exitDuration,
        ease: show ? MOTION_EASING.standard : MOTION_EASING.enter,
      }}
      style={{ pointerEvents: show ? "auto" : "none" }}
      data-context-state={show ? "context" : "active"}
      // Callers with real focusable content (a form, buttons) should also
      // pass `aria-hidden`/`inert` keyed off the same `show` value — this
      // component only owns the motion, not a caller's own a11y wiring,
      // so it forwards whatever the caller passes via `...rest`.
      {...rest}
    >
      {children}
    </motion.div>
  );
}
