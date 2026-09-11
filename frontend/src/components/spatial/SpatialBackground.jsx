import { useEffect, useRef } from "react";
import "./spatial-background.css";

/**
 * Decorative Spatial backdrop for CVLN Academy.
 *
 * Contract:
 * - never captures pointer/keyboard interactions
 * - never participates in application state
 * - respects prefers-reduced-motion
 * - progressively enhances a static visual fallback
 */
export default function SpatialBackground() {
  const rootRef = useRef(null);

  useEffect(() => {
    const root = rootRef.current;
    if (!root || typeof window === "undefined") return undefined;

    const reduceMotion = window.matchMedia?.("(prefers-reduced-motion: reduce)");
    if (reduceMotion?.matches) return undefined;

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
  }, []);

  return (
    <div ref={rootRef} className="spatial-background" aria-hidden="true" data-testid="spatial-background">
      <div className="spatial-background__base" />
      <div className="spatial-background__world" />
      <div className="spatial-background__aurora spatial-background__aurora--one" />
      <div className="spatial-background__aurora spatial-background__aurora--two" />
      <div className="spatial-background__orbit spatial-background__orbit--one" />
      <div className="spatial-background__orbit spatial-background__orbit--two" />
      <div className="spatial-background__mist" />
      <div className="spatial-background__readability" />
    </div>
  );
}
