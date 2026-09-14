import { lazy, Suspense, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import { useAuth } from "@/lib/auth.jsx";
import SpatialBackground from "@/components/spatial/SpatialBackground.jsx";
import SpatialWebGLBackground from "@/components/spatial/SpatialWebGLBackground.jsx";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { detectSpatialQuality, detectWebglQuality, SPATIAL_QUALITY } from "@/lib/spatial/devicePerformancePolicy";
import { sceneForPathname } from "@/lib/spatial/worldSceneMap";
import { backgroundForNode } from "@/lib/spatial/webglSceneMap";
import { webglSupported } from "@/lib/spatial/webglSupport";
import SpatialFocusManager from "@/components/spatial/SpatialFocusManager.jsx";
import SpatialModuleDock from "@/components/spatial/SpatialModuleDock.jsx";
import SpatialModuleEnvironmentBridge from "@/components/spatial/SpatialModuleEnvironmentBridge.jsx";
import ReturnPositionTracker from "@/components/spatial/ReturnPositionTracker.jsx";
import "./spatial-camera.css";

// Optional capabilities live in separate chunks. With the production defaults
// (route transitions, sensory feedback and diagnostics disabled) the browser
// no longer downloads or evaluates their implementation at startup.
const SpatialCameraBridge = lazy(() => import("@/components/spatial/SpatialCameraBridge.jsx"));
const SpatialCameraIntentCapture = lazy(() => import("@/components/spatial/SpatialCameraIntentCapture.jsx"));
const SpatialRuntimeDiagnostics = lazy(() => import("@/components/spatial/SpatialRuntimeDiagnostics.jsx"));
const SpatialSensoryBridge = lazy(() => import("@/components/spatial/SpatialSensoryBridge.jsx"));
const SpatialSharedElementLayer = lazy(() => import("@/components/spatial/SpatialSharedElementLayer.jsx"));

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
  //
  // Two independent tiers, deliberately: `quality` (detectSpatialQuality)
  // still gates the CSS world exactly as it did before this file existed
  // (unchanged — the mobile-freeze fix). `webglQuality` (detectWebglQuality)
  // is real capability only, uncapped by viewport/pointer except a safety
  // cap to BALANCED on touch — so a capable phone gets the lightweight
  // single-plane WebGL scene instead of the flat CSS world, while hardware
  // that is genuinely weak (low memory/cores/Data Saver) still never pays
  // for WebGL at all and falls through to the CSS branch below.
  const [quality] = useState(() => detectSpatialQuality());
  const [webglQuality] = useState(() => detectWebglQuality());
  const [hasWebgl] = useState(() => webglSupported());
  const { node } = sceneForPathname(location.pathname);
  const webglEligible = useMemo(
    () =>
      FEATURE_FLAGS.SPATIAL_WEBGL &&
      hasWebgl &&
      webglQuality !== SPATIAL_QUALITY.LITE &&
      Boolean(backgroundForNode(node)),
    [hasWebgl, webglQuality, node]
  );

  // Disabled optional subsystems should not even mount React effects. Their
  // own internal feature guards remain as defence-in-depth for direct tests or
  // future reuse, but the production frame avoids creating dormant component
  // instances for route-transition, sensory and debug capabilities.
  const routeTransitionsEnabled = FEATURE_FLAGS.SPATIAL_ROUTE_TRANSITIONS;
  const sensoryEnabled = FEATURE_FLAGS.SPATIAL_AUDIO || FEATURE_FLAGS.SPATIAL_HAPTICS;
  const diagnosticsEnabled = FEATURE_FLAGS.SPATIAL_DEBUG;

  return (
    <div className="relative min-h-screen overflow-hidden" data-testid="spatial-world-frame">
      <ReturnPositionTracker />
      <SpatialFocusManager />
      <Suspense fallback={null}>
        {routeTransitionsEnabled ? <SpatialCameraIntentCapture /> : null}
        {routeTransitionsEnabled ? <SpatialCameraBridge /> : null}
        {sensoryEnabled ? <SpatialSensoryBridge /> : null}
        {diagnosticsEnabled ? <SpatialRuntimeDiagnostics /> : null}
      </Suspense>
      {webglEligible ? (
        <SpatialWebGLBackground pathname={location.pathname} stade={user?.stade} quality={webglQuality} />
      ) : (
        <SpatialBackground pathname={location.pathname} stade={user?.stade} />
      )}
      <SpatialModuleEnvironmentBridge />
      <Suspense fallback={null}>
        {routeTransitionsEnabled ? <SpatialSharedElementLayer /> : null}
      </Suspense>
      <div className="relative z-10 min-h-screen">{children}</div>
      <SpatialModuleDock />
    </div>
  );
}
