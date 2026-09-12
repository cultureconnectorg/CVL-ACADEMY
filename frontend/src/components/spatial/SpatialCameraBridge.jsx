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

function waitForElement(selector, timeoutMs = 1800) {
  return new Promise((resolve) => {
    if (!selector || typeof document === "undefined") {
      resolve(null);
      return;
    }
    const immediate = document.querySelector(selector);
    if (immediate) {
      resolve(immediate);
      return;
    }
    let settled = false;
    const finish = (value) => {
      if (settled) return;
      settled = true;
      observer.disconnect();
      window.clearTimeout(timer);
      resolve(value);
    };
    const observer = new MutationObserver(() => {
      const candidate = document.querySelector(selector);
      if (candidate) finish(candidate);
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
    const timer = window.setTimeout(() => finish(null), timeoutMs);
  });
}

/**
 * Resolves the destination half of a camera-follow contract after React has
 * mounted the new route. Navigation is never delayed; async API rendering gets
 * a bounded observation window, then safely falls back to normal routing.
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

    let cancelled = false;
    const selector = pending.destinationSelector || anchorSelector(pending.anchorId, "destination");
    waitForElement(selector).then((target) => {
      if (cancelled) return;
      const current = readPendingCameraIntent();
      if (!current || current.destinationRoute !== location.pathname) return;
      if (!target) {
        cancelCameraIntent();
        return;
      }
      const intent = consumePendingCameraIntent();
      completeCameraIntent(intent, target);
    });

    return () => {
      cancelled = true;
    };
  }, [location.pathname, reduced]);

  return null;
}
