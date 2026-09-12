/**
 * ACTIVE -> CONTEXT -> RETURN — in-route spatial context surface.
 * DOMAIN_STATE stays outside this component: it only projects a confirmed UI
 * context into depth and returns to the same active screen.
 */

import { motion } from "framer-motion";
import { useCallback, useEffect } from "react";
import { MOTION_EASING, motionDuration } from "@/lib/motion-tokens";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { useSpatialState } from "@/lib/useSpatialState";
import { SPATIAL_STATES, SPATIAL_EVENTS } from "@/lib/spatial-state";

export const SPATIAL_CONTEXT_EVENT = "cvln:spatial-context";

function emitContextState(show) {
  if (typeof window === "undefined" || typeof CustomEvent !== "function") return;
  window.dispatchEvent(new CustomEvent(SPATIAL_CONTEXT_EVENT, {
    detail: { active: Boolean(show), state: show ? "CONTEXT" : "ACTIVE" },
  }));
}

export function useContextEntry() {
  const [state, dispatch] = useSpatialState(SPATIAL_STATES.ACTIVE);
  const enterContext = useCallback(() => dispatch(SPATIAL_EVENTS.REVEAL_CONTEXT), [dispatch]);
  const leaveContext = useCallback(() => dispatch(SPATIAL_EVENTS.DISMISS_CONTEXT), [dispatch]);
  return { state, isContext: state === SPATIAL_STATES.CONTEXT, enterContext, leaveContext };
}

/**
 * Context is a perceptual Z-layer, not another page. It approaches the learner
 * while remaining inside the current route. Reduced motion preserves the same
 * semantic state with a 1ms transition and no meaningful depth travel.
 */
export function ContextFrame({ show, children, className, ...rest }) {
  const reduced = useReducedMotion();
  const enterDuration = motionDuration("reveal", reduced) / 1000;
  const exitDuration = motionDuration("return", reduced) / 1000;

  useEffect(() => {
    emitContextState(show);
    return () => {
      if (show) emitContextState(false);
    };
  }, [show]);

  const activeVisual = reduced
    ? { opacity: 1, y: 0, z: 0, scale: 1 }
    : { opacity: 1, y: 0, z: 30, scale: 1 };
  const inactiveVisual = reduced
    ? { opacity: 0, y: 0, z: 0, scale: 1 }
    : { opacity: 0, y: 4, z: -18, scale: 0.985 };

  return (
    <motion.div
      className={className}
      initial={inactiveVisual}
      animate={show ? activeVisual : inactiveVisual}
      transition={{
        duration: show ? enterDuration : exitDuration,
        ease: show ? MOTION_EASING.enter : MOTION_EASING.exit,
      }}
      style={{
        pointerEvents: show ? "auto" : "none",
        transformPerspective: 1200,
        transformStyle: "preserve-3d",
        position: "relative",
        zIndex: show ? 2 : 1,
      }}
      data-context-state={show ? "context" : "active"}
      data-spatial-depth-role={show ? "context-foreground" : "context-receded"}
      aria-hidden={!show}
      {...rest}
    >
      {children}
    </motion.div>
  );
}
