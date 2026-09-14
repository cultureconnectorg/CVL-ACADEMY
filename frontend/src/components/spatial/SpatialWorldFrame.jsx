import { useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import { useAuth } from "@/lib/auth.jsx";
import SpatialBackground from "@/components/spatial/SpatialBackground.jsx";
import SpatialWebGLBackground from "@/components/spatial/SpatialWebGLBackground.jsx";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { detectSpatialQuality, SPATIAL_QUALITY } from "@/lib/spatial/devicePerformancePolicy";
import { sceneForPathname } from "@/lib/spatial/worldSceneMap";
import { backgroundForNode } from "@/lib/spatial/webglSceneMap";
import { webglSupported } from "@/lib/spatial/webglSupport";
import SpatialCameraBridge from "@/components/spatial/SpatialCameraBridge.jsx";
import SpatialCameraIntentCapture from "@/components/spatial/SpatialCameraIntentCapture.jsx";
import SpatialFocusManager from "@/components/spatial/SpatialFocusManager.jsx";
import SpatialModuleDock from "@/components/spatial/SpatialModuleDock.jsx";
import SpatialModuleEnvironmentBridge from "@/components/spatial/SpatialModuleEnvironmentBridge.jsx";
import SpatialRuntimeDiagnostics from "@/components/spatial/SpatialRuntimeDiagnostics.jsx";
import SpatialSensoryBridge from "@/components/spatial/SpatialSensoryBridge.jsx";
import SpatialSharedElementLayer from "@/components/spatial/SpatialSharedElementLayer.jsx";
import ReturnPositionTracker from "@/components/spatial/ReturnPositionTracker.jsx";
import "./spatial-camera.css";

/**
 * Mounts the visual world behind the already-existing application routes.
 * It does not own navigation, auth, content, or route transitions.
 */
export default function SpatialWorldFrame({ children }) {
  const location = useLocation();
  const { user } = useAuth();

  // Computed once per mount — device tier and WebGL support do not change
  // mid-session. A route with no reference photograph yet
  // (backgroundForNode returns null — e.g. legal pages, auth recovery)
  // always keeps the CSS world, same as it does today.
  const [quality] = useState(() => detectSpatialQuality());
  const [hasWebgl] = useState(() => webglSupported());
  const { node } = sceneForPathname(location.pathname);
  const webglEligible = useMemo(
    () =>
      FEATURE_FLAGS.SPATIAL_WEBGL &&
      hasWebgl &&
      quality !== SPATIAL_QUALITY.LITE &&
      Boolean(backgroundForNode(node)),
    [hasWebgl, quality, node]
  );

  return (
    <div className="relative min-h-screen overflow-hidden" data-testid="spatial-world-frame">
      <ReturnPositionTracker />
      <SpatialFocusManager />
      <SpatialCameraIntentCapture />
      <SpatialCameraBridge />
      <SpatialSensoryBridge />
      <SpatialRuntimeDiagnostics />
      {webglEligible ? (
        <SpatialWebGLBackground pathname={location.pathname} stade={user?.stade} />
      ) : (
        <SpatialBackground pathname={location.pathname} stade={user?.stade} />
      )}
      <SpatialModuleEnvironmentBridge />
      <SpatialSharedElementLayer />
      <div className="relative z-10 min-h-screen">{children}</div>
      <SpatialModuleDock />
    </div>
  );
}
