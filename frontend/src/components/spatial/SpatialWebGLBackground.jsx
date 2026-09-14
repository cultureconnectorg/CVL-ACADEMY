import { useEffect, useMemo, useRef, useState } from "react";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { SPATIAL_CONTEXT_EVENT } from "@/lib/ContextFrame";
import { sceneForPathname } from "@/lib/spatial/worldSceneMap";
import { environmentForStade } from "@/lib/spatial/environmentState";
import { SPATIAL_QUALITY } from "@/lib/spatial/devicePerformancePolicy";
import { SPATIAL_CAMERA_EVENT } from "@/lib/spatial/cameraRuntime";
import { backgroundForNode } from "@/lib/spatial/webglSceneMap";
import "./spatial-webgl-background.css";

/**
 * Real WebGL world — ADR W4 (docs/ADR_W4_WEBGL_DECISION.md, NO_WEBGL_REQUIRED)
 * is superseded for this layer by explicit Founder authorization; see
 * docs/ADR_W5_WEBGL_REOPENED.md for the record. `SpatialBackground.jsx`
 * (the CSS/SVG world) is UNCHANGED and stays the fallback: LITE-tier
 * devices, `prefers-reduced-motion`'s hard-off path (kept fully static
 * here instead, see below), no-WebGL browsers, and every existing route
 * not covered by BACKGROUND_BY_SCENE all still render it — see the
 * mount switch in SpatialWorldFrame.jsx. This file owns rendering only;
 * DOMAIN_STATE, routing, and auth remain entirely outside it, same
 * contract as SpatialBackground.jsx.
 *
 * Two textured planes per scene (full photograph + a UV-cropped bottom
 * band on a closer plane) give real perspective parallax from a single
 * photograph — the DOM/CSS world could only ever translate3d one flat
 * layer per element; this one has actual camera-distance-driven depth.
 */
export default function SpatialWebGLBackground({ pathname = "/", stade, quality = SPATIAL_QUALITY.BALANCED }) {
  const mountRef = useRef(null);
  const canvasRef = useRef(null);
  const engineRef = useRef(null);
  const reduced = useReducedMotion();
  const { node, scene } = sceneForPathname(pathname);
  const environment = useMemo(() => environmentForStade(stade), [stade]);
  const backgroundUrl = backgroundForNode(node);
  const enabled = FEATURE_FLAGS.SPATIAL_WEBGL && quality !== SPATIAL_QUALITY.LITE && Boolean(backgroundUrl);
  const [engineReady, setEngineReady] = useState(0);

  // Mount the renderer once. Cleaned up on unmount only — scene content is
  // swapped in-place by the effect below, never torn down on route change.
  // `import()` is always async, so the very first paint's scene-transition
  // effect (below) can run before engineRef.current exists yet — bumping
  // engineReady once the engine is actually constructed re-fires that
  // effect instead of silently missing the initial texture load.
  useEffect(() => {
    if (!enabled || typeof window === "undefined") return undefined;
    let cancelled = false;

    import("@/lib/spatial/webglEngine").then((mod) => {
      if (cancelled || !canvasRef.current) return;
      engineRef.current = mod.createSpatialWorldEngine({
        canvas: canvasRef.current,
        quality,
        reducedMotion: reduced,
      });
      setEngineReady((n) => n + 1);
    });

    return () => {
      cancelled = true;
      engineRef.current?.dispose?.();
      engineRef.current = null;
    };
    // quality is captured once at mount (device tier does not change mid-session);
    // reduced can change live and is applied via the effect below instead of remounting.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [enabled]);

  // Apply reduced-motion live (toggle mid-session without recreating the renderer).
  useEffect(() => {
    engineRef.current?.setReducedMotion?.(reduced);
  }, [reduced]);

  // Scene change: crossfade to the new background + camera framing.
  // engineReady re-fires this once the async engine import above resolves,
  // so the very first paint's texture load isn't silently dropped by the
  // mount-order race between the two effects.
  useEffect(() => {
    if (!enabled || !backgroundUrl) return;
    engineRef.current?.transitionTo?.({ url: backgroundUrl, scene, environment, node });
  }, [enabled, backgroundUrl, scene, environment, node, engineReady]);

  // Camera intent events — same bridge SpatialBackground.jsx listens to,
  // so both worlds react identically to LOCK/FOLLOW/RETURN/CANCEL.
  useEffect(() => {
    if (!enabled || typeof window === "undefined") return undefined;
    const onCamera = (event) => engineRef.current?.onCameraEvent?.(event?.detail);
    window.addEventListener(SPATIAL_CAMERA_EVENT, onCamera);
    return () => window.removeEventListener(SPATIAL_CAMERA_EVENT, onCamera);
  }, [enabled]);

  useEffect(() => {
    if (!enabled || typeof window === "undefined") return undefined;
    const onContext = (event) => engineRef.current?.setContextActive?.(Boolean(event?.detail?.active));
    window.addEventListener(SPATIAL_CONTEXT_EVENT, onContext);
    return () => window.removeEventListener(SPATIAL_CONTEXT_EVENT, onContext);
  }, [enabled]);

  if (!enabled) return null;

  return (
    <div
      ref={mountRef}
      className="spatial-webgl-background"
      aria-hidden="true"
      data-testid="spatial-webgl-background"
      data-spatial-node={node || "NONE"}
      data-spatial-quality={quality}
    >
      <canvas ref={canvasRef} className="spatial-webgl-background__canvas" />
    </div>
  );
}
