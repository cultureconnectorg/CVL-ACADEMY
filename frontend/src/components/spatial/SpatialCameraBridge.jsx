import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { anchorSelector } from "@/lib/spatial/cameraAnchor";
import {
  cancelCameraIntent,
  completeCameraIntent,
  consumeArmedCameraReturn,
  consumePendingCameraIntent,
  readArmedCameraReturn,
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
    let timer = null;
    const observer = new MutationObserver(() => {
      const candidate = document.querySelector(selector);
      if (candidate) finish(candidate);
    });
    const finish = (value) => {
      if (settled) return;
      settled = true;
      observer.disconnect();
      if (timer) window.clearTimeout(timer);
      resolve(value);
    };
    observer.observe(document.documentElement, { childList: true, subtree: true });
    timer = window.setTimeout(() => finish(null), timeoutMs);
  });
}

function restoreSourceFocus(target) {
  if (!target || typeof target.focus !== "function") return;
  target.focus({ preventScroll: true });
  if (typeof window !== "undefined" && typeof window.requestAnimationFrame === "function") {
    window.requestAnimationFrame(() => {
      if (target.isConnected) target.focus({ preventScroll: true });
    });
  }
}

/**
 * Resolves forward and exact-return camera/shared-element anchors after React
 * has mounted the route. Navigation is never delayed; async API rendering gets
 * a bounded observation window, then safely falls back to normal routing.
 */
export default function SpatialCameraBridge() {
  const location = useLocation();
  const reduced = useReducedMotion();

  useEffect(() => {
    if (!FEATURE_FLAGS.SPATIAL_ROUTE_TRANSITIONS || reduced || typeof window === "undefined") {
      return undefined;
    }

    let cancelled = false;
    const pending = readPendingCameraIntent();
    const armedReturn = readArmedCameraReturn();

    if (pending && pending.destinationRoute === location.pathname) {
      const selector = pending.destinationSelector || anchorSelector(pending.anchorId, "destination");
      waitForElement(selector).then(async (target) => {
        if (cancelled) return;
        const current = readPendingCameraIntent();
        if (!current || current.destinationRoute !== location.pathname) return;
        if (!target) {
          cancelCameraIntent();
          return;
        }
        const sharedTarget = current.sharedDestinationSelector
          ? await waitForElement(current.sharedDestinationSelector)
          : null;
        if (cancelled) return;
        const intent = consumePendingCameraIntent();
        completeCameraIntent(intent, target, { sharedElement: sharedTarget });
      });
    } else if (armedReturn && armedReturn.sourceRoute === location.pathname) {
      const selector = armedReturn.sourceSelector || `a[href="${armedReturn.destinationRoute}"]`;
      waitForElement(selector).then(async (target) => {
        if (cancelled) return;
        const current = readArmedCameraReturn();
        if (!current || current.sourceRoute !== location.pathname) return;
        if (!target) {
          consumeArmedCameraReturn();
          cancelCameraIntent();
          return;
        }

        // The exact source control is the authoritative focus target for a
        // browser-back return. Focus it as soon as it exists, before any
        // optional shared-element lookup can delay completion.
        restoreSourceFocus(target);

        const sharedTarget = current.sharedSourceSelector
          ? await waitForElement(current.sharedSourceSelector)
          : null;
        if (cancelled) return;
        const contract = consumeArmedCameraReturn();
        completeCameraIntent(contract, target, { returning: true, sharedElement: sharedTarget });

        // Reassert after the camera/shared-element completion so a sibling
        // autofocus effect resolving in the same commit cannot steal focus.
        restoreSourceFocus(target);
      });
    }

    return () => {
      cancelled = true;
    };
  }, [location.pathname, reduced]);

  return null;
}
