import { useEffect, useRef } from "react";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { useReducedMotion } from "@/lib/useReducedMotion";
import "./spatial-background.css";

/**
 * CVLN Academy world layer.
 *
 * This does not replace Spatial Learning. It consumes the existing Spatial
 * runtime contract: SPATIAL_ENGINE + SPATIAL_ENVIRONMENT gates, the shared
 * reduced-motion hook, and the doctrine that depth/light/movement convey
 * context rather than exist as decoration.
 *
 * Safe fallback: when Spatial is disabled, the world remains visible but
 * static. No pointer/keyboard interaction is ever captured.
 */
export default function SpatialBackground() {
  const rootRef = useRef(null);
  const reduced = useReducedMotion();
  const spatialEnabled = FEATURE_FLAGS.SPATIAL_ENGINE && FEATURE_FLAGS.SPATIAL_ENVIRONMENT;
  const motionEnabled = spatialEnabled && !reduced;

  useEffect(() => {
    const root = rootRef.current;
    if (!root || typeof window === "undefined" || !motionEnabled) return undefined;

    let frame = null;
    let targetX = 0;
    let targetY = 0;
    let currentX = 0;
    let currentY = 0;
    let scrollY = window.scrollY || 0;

    const render = () => {
      currentX += (targetX - currentX) * 0.055;
      currentY += (targetY - currentY) * 0.055;

      root.style.setProperty("--spatial-x", `${currentX.toFixed(3)}px`);
      root.style.setProperty("--spatial-y", `${currentY.toFixed(3)}px`);
      root.style.setProperty("--spatial-scroll", `${Math.min(scrollY, 900).toFixed(1)}px`);

      frame = window.requestAnimationFrame(render);
    };

    const onPointerMove = (event) => {
      const nx = event.clientX / Math.max(window.innerWidth, 1) - 0.5;
      const ny = event.clientY / Math.max(window.innerHeight, 1) - 0.5;
      targetX = nx * 20;
      targetY = ny * 14;
    };

    const onScroll = () => {
      scrollY = window.scrollY || 0;
    };

    window.addEventListener("pointermove", onPointerMove, { passive: true });
    window.addEventListener("scroll", onScroll, { passive: true });
    frame = window.requestAnimationFrame(render);

    return () => {
      window.removeEventListener("pointermove", onPointerMove);
      window.removeEventListener("scroll", onScroll);
      if (frame) window.cancelAnimationFrame(frame);
    };
  }, [motionEnabled]);

  return (
    <div
      ref={rootRef}
      className="spatial-background"
      aria-hidden="true"
      data-testid="spatial-background"
      data-spatial-engine={spatialEnabled ? "on" : "off"}
      data-spatial-motion={motionEnabled ? "full" : reduced ? "reduced" : "static"}
    >
      <div className="spatial-background__layer spatial-background__layer--far">
        <div className="spatial-background__base" />
        <div className="spatial-background__world" />
      </div>

      <div className="spatial-background__layer spatial-background__layer--mid">
        <div className="spatial-background__aurora spatial-background__aurora--one" />
        <div className="spatial-background__aurora spatial-background__aurora--two" />
        <div className="spatial-background__orbit spatial-background__orbit--one" />
        <div className="spatial-background__orbit spatial-background__orbit--two" />
      </div>

      <div className="spatial-background__layer spatial-background__layer--near">
        <div className="spatial-background__mist" />
      </div>

      <div className="spatial-background__readability" />
    </div>
  );
}
