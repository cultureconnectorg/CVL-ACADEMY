import { useEffect, useMemo, useRef, useState } from "react";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { sceneForPathname } from "@/lib/spatial/worldSceneMap";
import { backgroundForNode } from "@/lib/spatial/webglSceneMap";
import { SPATIAL_CAMERA_EVENT } from "@/lib/spatial/cameraRuntime";
import { SPATIAL_SIGNAL_EVENT, spatialSignalProfile } from "@/lib/spatial/spatialLearningSignals";
import "./spatial-mobile-living-background.css";

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

export default function SpatialMobileLivingBackground({ pathname = "/" }) {
  const rootRef = useRef(null);
  const reduced = useReducedMotion();
  const { node, scene } = sceneForPathname(pathname);
  const [viewportWidth] = useState(() => (typeof window !== "undefined" ? window.innerWidth : 390));
  const backgroundUrl = backgroundForNode(node, { viewportWidth });
  const [signal, setSignal] = useState(0);
  const focus = useMemo(() => ({
    x: ((scene?.focusX ?? 50) - 50) / 50,
    y: ((scene?.focusY ?? 50) - 50) / 50,
  }), [scene?.focusX, scene?.focusY]);

  useEffect(() => {
    const el = rootRef.current;
    if (!el || reduced) return undefined;

    let touchStart = null;
    let raf = null;
    let tx = 0;
    let ty = 0;
    let sx = 0;
    let sy = 0;

    const paint = () => {
      raf = null;
      el.style.setProperty("--mobile-world-x", `${sx + focus.x * 10}px`);
      el.style.setProperty("--mobile-world-y", `${sy + focus.y * 10}px`);
      el.style.setProperty("--mobile-world-near-x", `${(sx + focus.x * 10) * -0.42}px`);
      el.style.setProperty("--mobile-world-near-y", `${(sy + focus.y * 10) * -0.56}px`);
    };

    const request = () => {
      if (raf == null) raf = requestAnimationFrame(paint);
    };

    const onScroll = () => {
      const max = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
      const p = clamp(window.scrollY / max, 0, 1);
      sy = (p - 0.5) * 34;
      request();
    };

    const onTouchStart = (event) => {
      const t = event.touches?.[0];
      if (!t) return;
      touchStart = { x: t.clientX, y: t.clientY };
    };

    const onTouchMove = (event) => {
      const t = event.touches?.[0];
      if (!t || !touchStart) return;
      tx = clamp((t.clientX - touchStart.x) / Math.max(window.innerWidth, 1), -1, 1) * 18;
      ty = clamp((t.clientY - touchStart.y) / Math.max(window.innerHeight, 1), -1, 1) * 14;
      sx = tx;
      sy += ty * 0.12;
      request();
    };

    const onTouchEnd = () => {
      touchStart = null;
      sx *= 0.3;
      request();
    };

    const onCamera = (event) => {
      const detail = event?.detail;
      const origin = detail?.cameraOriginTarget || detail?.cameraOriginFrom;
      if (!origin) return;
      sx = clamp((origin.x - 50) * 0.35, -16, 16);
      sy = clamp((50 - origin.y) * 0.28, -14, 14);
      request();
    };

    const onSignal = (event) => {
      const profile = spatialSignalProfile(event?.detail?.type);
      if (!profile) return;
      setSignal(clamp(profile.worldBreath ?? profile.intensity ?? 0.2, 0, 1));
      window.setTimeout(() => setSignal(0), profile.ttlMs ?? 1600);
    };

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("touchstart", onTouchStart, { passive: true });
    window.addEventListener("touchmove", onTouchMove, { passive: true });
    window.addEventListener("touchend", onTouchEnd, { passive: true });
    window.addEventListener(SPATIAL_CAMERA_EVENT, onCamera);
    window.addEventListener(SPATIAL_SIGNAL_EVENT, onSignal);
    onScroll();

    return () => {
      if (raf != null) cancelAnimationFrame(raf);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("touchstart", onTouchStart);
      window.removeEventListener("touchmove", onTouchMove);
      window.removeEventListener("touchend", onTouchEnd);
      window.removeEventListener(SPATIAL_CAMERA_EVENT, onCamera);
      window.removeEventListener(SPATIAL_SIGNAL_EVENT, onSignal);
    };
  }, [focus.x, focus.y, reduced]);

  if (!backgroundUrl) return null;

  return (
    <div
      ref={rootRef}
      className="spatial-mobile-living-background"
      data-spatial-node={node || "NONE"}
      data-signal-active={signal > 0 ? "true" : "false"}
      aria-hidden="true"
      style={{
        "--mobile-world-image": `url(${backgroundUrl})`,
        "--mobile-world-breath": signal,
      }}
    >
      <div className="spatial-mobile-living-background__far" />
      <div className="spatial-mobile-living-background__near" />
      <div className="spatial-mobile-living-background__veil" />
    </div>
  );
}
