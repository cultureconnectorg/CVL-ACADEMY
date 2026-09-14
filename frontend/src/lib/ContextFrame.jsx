/**
 * ACTIVE -> CONTEXT -> RETURN — in-route spatial context surface.
 * DOMAIN_STATE stays outside this component: it only projects a confirmed UI
 * context into depth and returns to the same active screen.
 */

import { motion } from "framer-motion";
import { useCallback, useEffect, useRef } from "react";
import { MOTION_EASING, motionDuration } from "@/lib/motion-tokens";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { useSpatialState } from "@/lib/useSpatialState";
import { SPATIAL_STATES, SPATIAL_EVENTS } from "@/lib/spatial-state";
import { createSpatialAudio } from "@/lib/spatial/audio";
import { FEATURE_FLAGS } from "@/lib/featureFlags";

export const SPATIAL_CONTEXT_EVENT = "cvln:spatial-context";

function emitContextState(show) {
  if (typeof window === "undefined" || typeof CustomEvent !== "function") return;
  window.dispatchEvent(new CustomEvent(SPATIAL_CONTEXT_EVENT, {
    detail: { active: Boolean(show), state: show ? "CONTEXT" : "ACTIVE" },
  }));
}

export function useContextEntry() {
  const [state, dispatch] = useSpatialState(SPATIAL_STATES.ACTIVE);
  const invokerRef = useRef(null);

  const enterContext = useCallback((eventOrElement = null) => {
    const candidate = eventOrElement?.currentTarget || eventOrElement;
    if (candidate && typeof candidate.focus === "function") invokerRef.current = candidate;
    dispatch(SPATIAL_EVENTS.REVEAL_CONTEXT);
  }, [dispatch]);

  const leaveContext = useCallback(() => {
    dispatch(SPATIAL_EVENTS.DISMISS_CONTEXT);
    const target = invokerRef.current;
    if (!target || typeof target.focus !== "function") return;
    const restore = () => {
      if (target.isConnected === false) return;
      target.focus({ preventScroll: true });
    };
    if (typeof requestAnimationFrame === "function") requestAnimationFrame(restore);
    else restore();
  }, [dispatch]);

  return {
    state,
    isContext: state === SPATIAL_STATES.CONTEXT,
    enterContext,
    leaveContext,
    invokerRef,
  };
}

/**
 * Context is a perceptual Z-layer, not another page. It approaches the learner
 * while remaining inside the current route. Reduced motion preserves the same
 * semantic state with no invisible entrance frame and no meaningful depth travel.
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

  // RAIL 5 (2026-09-07) — real CONTEXT_OPEN/CONTEXT_CLOSE audio, correcting
  // a wrong claim in Rail 3's own SpatialHub docstring ("belong to
  // route-level transitions") — this dock is exactly where they belong:
  // a same-page ACTIVE<->CONTEXT transition, never a route change. Audio
  // only (no haptic pairing fabricated here — `audio.js`'s own 8-event
  // set names CONTEXT_OPEN/CONTEXT_CLOSE for exactly this; no dedicated
  // haptic pattern exists for a dock open/close in `haptics.js`'s 5).
  const audioRef = useRef(null);
  if (!audioRef.current) audioRef.current = createSpatialAudio();
  audioRef.current.setEnabled(FEATURE_FLAGS.SPATIAL_MODULE_DEPTH && FEATURE_FLAGS.SPATIAL_AUDIO);
  const prevShowRef = useRef(show);
  useEffect(() => {
    if (prevShowRef.current === show) return;
    prevShowRef.current = show;
    if (!FEATURE_FLAGS.SPATIAL_MODULE_DEPTH) return;
    audioRef.current.play(show ? "CONTEXT_OPEN" : "CONTEXT_CLOSE");
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
      initial={false}
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
