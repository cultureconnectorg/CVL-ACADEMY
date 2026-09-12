import { useEffect, useMemo, useRef, useState } from "react";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { makeRailPhysics } from "@/lib/spatial/physics";
import { sceneForPathname } from "@/lib/spatial/worldSceneMap";
import { directSpatialExperience } from "@/lib/spatial/spatialDirector";
import { SPATIAL_SIGNAL_EVENT, spatialSignalProfile } from "@/lib/spatial/spatialLearningSignals";
import "./spatial-background.css";
import "./spatial-living-world.css";

/** Living CVLN Academy world. Navigation/auth/business state stay outside this layer. */
export default function SpatialBackground({ pathname = "/" }) {
  const rootRef = useRef(null);
  const signalTimerRef = useRef(null);
  const [activeSignal, setActiveSignal] = useState(null);
  const reduced = useReducedMotion();
  const spatialEnabled = FEATURE_FLAGS.SPATIAL_ENGINE && FEATURE_FLAGS.SPATIAL_ENVIRONMENT;
  const { node, scene } = sceneForPathname(pathname);
  const director = useMemo(
    () => directSpatialExperience({ node, scene, reducedMotion: reduced, signal: activeSignal }),
    [node, scene, reduced, activeSignal]
  );
  const motionEnabled = spatialEnabled && !reduced;
  const publicUrl = process.env.PUBLIC_URL || "";
  const worldImage = `url("${publicUrl}/spatial/cvln-academy-spatial-world.svg")`;

  useEffect(() => {
    if (typeof window === "undefined") return undefined;
    const onSpatialSignal = (event) => {
      const trusted = spatialSignalProfile(event?.detail?.type);
      if (!trusted) return;
      if (signalTimerRef.current) window.clearTimeout(signalTimerRef.current);
      setActiveSignal({ type: trusted.type, receivedAt: Date.now() });
      signalTimerRef.current = window.setTimeout(() => {
        setActiveSignal(null);
        signalTimerRef.current = null;
      }, trusted.ttlMs);
    };
    window.addEventListener(SPATIAL_SIGNAL_EVENT, onSpatialSignal);
    return () => {
      window.removeEventListener(SPATIAL_SIGNAL_EVENT, onSpatialSignal);
      if (signalTimerRef.current) window.clearTimeout(signalTimerRef.current);
    };
  }, []);

  useEffect(() => {
    setActiveSignal(null);
    if (typeof window !== "undefined" && signalTimerRef.current) {
      window.clearTimeout(signalTimerRef.current);
      signalTimerRef.current = null;
    }
  }, [pathname]);

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
    root.style.setProperty("--spatial-motion-intensity", String(director.motionIntensity));
    root.style.setProperty("--spatial-focus-strength", String(director.focusStrength));
    root.style.setProperty("--spatial-atmosphere-opacity", String(director.atmosphereOpacity));
    root.style.setProperty("--spatial-world-breath", String(director.worldBreath));

    if (!motionEnabled) {
      root.style.setProperty("--spatial-x", "0px");
      root.style.setProperty("--spatial-y", "0px");
      root.style.setProperty("--spatial-scroll", "0px");
      return undefined;
    }

    // Reuse the verified H0.10 retarget-safe spring instead of inventing a
    // second smoothing engine. Domain signals only retarget perception.
    const xPhysics = makeRailPhysics((position) => {
      root.style.setProperty("--spatial-x", `${position.toFixed(3)}px`);
    });
    const yPhysics = makeRailPhysics((position) => {
      root.style.setProperty("--spatial-y", `${position.toFixed(3)}px`);
    });

    const onPointerMove = (event) => {
      const x = (event.clientX / Math.max(window.innerWidth, 1) - 0.5) * director.pointerRangeX;
      const y = (event.clientY / Math.max(window.innerHeight, 1) - 0.5) * director.pointerRangeY;
      xPhysics.setTarget(x);
      yPhysics.setTarget(y);
    };
    const onPointerLeave = () => {
      xPhysics.setTarget(0);
      yPhysics.setTarget(0);
    };
    const onScroll = () => {
      root.style.setProperty("--spatial-scroll", `${Math.min(window.scrollY || 0, 900).toFixed(1)}px`);
    };

    xPhysics.jump(0);
    yPhysics.jump(0);
    onScroll();
    window.addEventListener("pointermove", onPointerMove, { passive: true });
    document.documentElement.addEventListener("mouseleave", onPointerLeave, { passive: true });
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => {
      window.removeEventListener("pointermove", onPointerMove);
      document.documentElement.removeEventListener("mouseleave", onPointerLeave);
      window.removeEventListener("scroll", onScroll);
    };
  }, [motionEnabled, scene, director]);

  return (
    <div
      ref={rootRef}
      className={`spatial-background spatial-background--${scene.zone}`}
      aria-hidden="true"
      style={{ "--spatial-world-image": worldImage }}
      data-testid="spatial-background"
      data-spatial-node={node || "NONE"}
      data-spatial-zone={scene.zone}
      data-spatial-camera={director.camera}
      data-spatial-intent={director.intent}
      data-spatial-learning-state={director.learningState}
      data-spatial-signal={director.signalType || "NONE"}
      data-spatial-engine={spatialEnabled ? "on" : "off"}
      data-spatial-motion={motionEnabled ? "full" : reduced ? "reduced" : "static"}
    >
      <div className="spatial-background__layer spatial-background__layer--far">
        <div className="spatial-background__base" /><div className="spatial-background__world" />
        <div className="spatial-background__clouds spatial-background__clouds--far" /><div className="spatial-background__stars" />
      </div>
      <div className="spatial-background__layer spatial-background__layer--mid">
        <div className="spatial-background__sunset-glow" /><div className="spatial-background__clouds spatial-background__clouds--near" />
        <div className="spatial-background__aurora spatial-background__aurora--one" /><div className="spatial-background__aurora spatial-background__aurora--two" />
        <div className="spatial-background__globe"><span className="spatial-background__globe-core" /><span className="spatial-background__globe-ring spatial-background__globe-ring--a" /><span className="spatial-background__globe-ring spatial-background__globe-ring--b" /></div>
        <div className="spatial-background__orbit spatial-background__orbit--one" /><div className="spatial-background__orbit spatial-background__orbit--two" />
        <div className="spatial-background__energy-rail" /><div className="spatial-background__water-shimmer" />
      </div>
      <div className="spatial-background__layer spatial-background__layer--near">
        <div className="spatial-background__particles" /><div className="spatial-background__mist" /><div className="spatial-background__foreground" />
      </div>
      <div className="spatial-background__readability" /><div className="spatial-background__vignette" /><div className="spatial-background__grain" />
    </div>
  );
}
