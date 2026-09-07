import { useEffect, useRef, useState } from "react";
import { makeRailPhysics } from "@/lib/spatial/physics";

/**
 * RAIL 3 remediation (2026-09-07) — "on a stoppé Spatial pour finir le
 * corpus, et ce qui a été rebranché n'était pas au niveau d'avant."
 * Correct: the first Rail 3 pass wired only `attention.js`'s static
 * depth formulas, driven by a fixed-duration Framer Motion tween — never
 * `physics.js`'s already-verified rAF spring (STIFFNESS=280, DAMPING=33,
 * ζ≈0.986, H0.9/H0.10). This hook is the missing glue: it owns zero
 * motion math of its own (that would be redoing Spatial, forbidden by
 * the mandate) — it only ever supplies the React lifecycle a caller must
 * provide per `physics.js`'s own docstring (`onFrame`/`onSettle`).
 *
 * @param {number} targetDistance a real GRAPH_DISTANCE / stage-index
 *   distance — never an arbitrary layout position.
 * @param {{ reduced?: boolean, onSettle?: () => void }} [opts]
 *   `reduced`: reduced-motion callers get `jump()` (instant) instead of
 *   the spring — same accessibility invariant as the rest of Spatial;
 *   `onSettle` still fires (as an immediate, synchronous "arrival") so
 *   non-visual feedback (audio/haptics) isn't silently dropped for
 *   reduced-motion users — only the motion itself is.
 * @returns {number} the live, continuously-animated distance to feed
 *   into `computeDepthStyle`.
 */
export function useDepthPhysics(targetDistance, opts = {}) {
  const { reduced = false, onSettle } = opts;
  const [position, setPosition] = useState(targetDistance);
  const physicsRef = useRef(null);
  const mountedRef = useRef(true);
  const onSettleRef = useRef(onSettle);
  const firstRunRef = useRef(true);
  onSettleRef.current = onSettle;

  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
    };
  }, []);

  useEffect(() => {
    if (!physicsRef.current) {
      physicsRef.current = makeRailPhysics(
        (p) => {
          if (mountedRef.current) setPosition(p);
        },
        () => {
          if (mountedRef.current && onSettleRef.current) onSettleRef.current();
        }
      );
    }
    const physics = physicsRef.current;

    if (firstRunRef.current) {
      // Silent initial placement: mounting at the real depth is not a
      // "the space reorganized" event — the engine only ever animates
      // in response to a real, subsequent change.
      firstRunRef.current = false;
      physics.jump(targetDistance);
      setPosition(targetDistance);
      return;
    }

    if (reduced) {
      physics.jump(targetDistance);
      setPosition(targetDistance);
      // No visible spring for a reduced-motion caller, but arrival
      // feedback (audio/haptics) is not motion — still fire it.
      if (onSettleRef.current) onSettleRef.current();
    } else {
      physics.setTarget(targetDistance);
    }
  }, [targetDistance, reduced]);

  return position;
}
