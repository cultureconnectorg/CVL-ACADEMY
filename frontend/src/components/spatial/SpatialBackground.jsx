import { useEffect, useRef } from "react";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { sceneForPathname } from "@/lib/spatial/worldSceneMap";
import "./spatial-background.css";

/**
 * CVLN Academy world layer.
 *
 * Visuals follow the existing Spatial topology. This component never owns
 * navigation, auth, learning state, or route transitions. It consumes the
 * authoritative pathname and translates it into cinematic camera variables.
 */
export default function SpatialBackground({ pathname = "/" }) {
  const rootRef = useRef(null);
  const reduced = useReducedMotion();
  const spatialEnabled = FEATURE_FLAGS.SPATIAL_ENGINE && FEATURE_FLAGS.SPATIAL_ENVIRONMENT;
  const motionEnabled = spatialEnabled && !reduced;
  const { node, scene } = sceneForPathname(pathname);
  const publicUrl = process.env.PUBLIC_URL || "";
  const worldImage = `url("${publicUrl}/spatial/cvln-academy-spatial-world.svg")`;

  useEffect(() => {
    const root = rootRef.current;
    if (!root || typeof window === "undefined") return undefined;

    root.style.setProperty("--scene-x", `${scene.x}vw`);
    root.style.setProperty("--scene-y", `${scene.y}vh`);
    root.style.setProperty("--scene-scale", String(scene.scale));
    root.style.setProperty("--scene-light", String(scene.light));
    root.style.setProperty("--scene-depth", String(scene.depth));
    root.style.setProperty("--scene-focus-x", `${scene.focusX}%`);
    root.style.setProperty("--scene-focus-y", `${scene.focusY}%`);
    root.style.setProperty("--scene-warmth", String(scene.warmth));
    root.style.setProperty("--scene-vignette", String(scene.vignette));

    if (!motionEnabled) return undefined;

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
      targetX = nx * 24;
      targetY = ny * 16;
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
  }, [motionEnabled, scene]);

  return (
    <div
      ref={rootRef}
      className={`spatial-background spatial-background--${scene.zone}`}
      aria-hidden="true"
      style={{ "--spatial-world-image": worldImage }}
      data-testid="spatial-background"
      data-spatial-node={node || "NONE"}
      data-spatial-zone={scene.zone}
      data-spatial-camera={scene.camera}
      data-spatial-engine={spatialEnabled ? "on" : "off"}
      data-spatial-motion={motionEnabled ? "full" : reduced ? "reduced" : "static"}
    >
      <div className="spatial-background__layer spatial-background__layer--far">
        <div className="spatial-background__base" />
        <div className="spatial-background__world" />
        <div className="spatial-background__stars" />
      </div>

      <div className="spatial-background__layer spatial-background__layer--mid">
        <div className="spatial-background__sunset-glow" />
        <div className="spatial-background__aurora spatial-background__aurora--one" />
        <div className="spatial-background__aurora spatial-background__aurora--two" />
        <div className="spatial-background__orbit spatial-background__orbit--one" />
        <div className="spatial-background__orbit spatial-background__orbit--two" />
        <div className="spatial-background__energy-rail" />
      </div>

      <div className="spatial-background__layer spatial-background__layer--near">
        <div className="spatial-background__mist" />
        <div className="spatial-background__foreground" />
      </div>

      <div className="spatial-background__readability" />
      <div className="spatial-background__vignette" />
      <div className="spatial-background__grain" />
    </div>
  );
}
