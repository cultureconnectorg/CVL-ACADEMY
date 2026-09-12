import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { anchorSelector } from "@/lib/spatial/cameraAnchor";
import {
  cancelCameraIntent,
  completeCameraIntent,
  consumePendingCameraIntent,
  readPendingCameraIntent,
} from "@/lib/spatial/cameraRuntime";

/**
 * Resolves the destination half of a camera-follow contract after React has
 * mounted the new route. Navigation is never delayed; an absent anchor simply
 * falls back to the normal route transition.
 */
export default function SpatialCameraBridge() {
  const location = useLocation();
  const reduced = useReducedMotion();

  useEffect(() => {
    if (!FEATURE_FLAGS.SPATIAL_ROUTE_TRANSITIONS || reduced || typeof window === "undefined") {
      return undefined;
    }

    const pending = readPendingCameraIntent();
    if (!pending || pending.destinationRoute !== location.pathname) return undefined;

    let frameA = null;
    let frameB = null;
    frameA = window.requestAnimationFrame(() => {
      frameB = window.requestAnimationFrame(() => {
        const current = readPendingCameraIntent();
        if (!current || current.destinationRoute !== location.pathname) return;
        const selector = current.destinationSelector || anchorSelector(current.anchorId, "destination");
        const target = selector ? document.querySelector(selector) : null;
        if (!target) {
          cancelCameraIntent();
          return;
        }
        const intent = consumePendingCameraIntent();
        completeCameraIntent(intent, target);
      });
    });

    return () => {
      if (frameA) window.cancelAnimationFrame(frameA);
      if (frameB) window.cancelAnimationFrame(frameB);
    };
  }, [location.pathname, reduced]);

  return null;
}
