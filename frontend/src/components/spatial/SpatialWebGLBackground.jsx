import { useEffect, useMemo, useRef, useState } from "react";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { SPATIAL_CONTEXT_EVENT } from "@/lib/ContextFrame";
import { sceneForPathname } from "@/lib/spatial/worldSceneMap";
import { environmentForStade } from "@/lib/spatial/environmentState";
import { SPATIAL_QUALITY } from "@/lib/spatial/devicePerformancePolicy";
import { SPATIAL_CAMERA_EVENT } from "@/lib/spatial/cameraRuntime";
import { SPATIAL_SIGNAL_EVENT, spatialSignalProfile } from "@/lib/spatial/spatialLearningSignals";
import { backgroundForNode } from "@/lib/spatial/webglSceneMap";
import SpatialMobileLivingBackground from "./SpatialMobileLivingBackground.jsx";
import "./spatial-webgl-background.css";

export default function SpatialWebGLBackground({ pathname = "/", stade, quality = SPATIAL_QUALITY.BALANCED }) {
  const mountRef = useRef(null);
  const canvasRef = useRef(null);
  const engineRef = useRef(null);
  const reduced = useReducedMotion();
  const { node, scene } = sceneForPathname(pathname);
  const environment = useMemo(() => environmentForStade(stade), [stade]);
  const [viewportWidth] = useState(() => (typeof window !== "undefined" ? window.innerWidth : 1440));
  const backgroundUrl = backgroundForNode(node, { viewportWidth });
  const enabled = FEATURE_FLAGS.SPATIAL_WEBGL && quality !== SPATIAL_QUALITY.LITE && Boolean(backgroundUrl);
  const isFull = enabled && quality === SPATIAL_QUALITY.FULL;
  const isBalanced = enabled && quality === SPATIAL_QUALITY.BALANCED;
  const [engineReady, setEngineReady] = useState(0);

  useEffect(() => {
    if (!isFull || typeof window === "undefined") return undefined;
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isFull, quality]);

  useEffect(() => {
    engineRef.current?.setReducedMotion?.(reduced);
  }, [reduced]);

  useEffect(() => {
    if (!isFull || !backgroundUrl) return;
    engineRef.current?.transitionTo?.({ url: backgroundUrl, scene, environment, node });
  }, [isFull, backgroundUrl, scene, environment, node, engineReady]);

  useEffect(() => {
    if (!isFull || typeof window === "undefined") return undefined;
    const onCamera = (event) => engineRef.current?.onCameraEvent?.(event?.detail);
    window.addEventListener(SPATIAL_CAMERA_EVENT, onCamera);
    return () => window.removeEventListener(SPATIAL_CAMERA_EVENT, onCamera);
  }, [isFull]);

  useEffect(() => {
    if (!isFull || typeof window === "undefined") return undefined;
    const onContext = (event) => engineRef.current?.setContextActive?.(Boolean(event?.detail?.active));
    window.addEventListener(SPATIAL_CONTEXT_EVENT, onContext);
    return () => window.removeEventListener(SPATIAL_CONTEXT_EVENT, onContext);
  }, [isFull]);

  useEffect(() => {
    if (!isFull || typeof window === "undefined") return undefined;
    const onSignal = (event) => {
      const profile = spatialSignalProfile(event?.detail?.type);
      if (profile) engineRef.current?.onLearningSignal?.(profile);
    };
    window.addEventListener(SPATIAL_SIGNAL_EVENT, onSignal);
    return () => window.removeEventListener(SPATIAL_SIGNAL_EVENT, onSignal);
  }, [isFull]);

  if (isBalanced) {
    return <SpatialMobileLivingBackground pathname={pathname} />;
  }

  if (!isFull) return null;

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
