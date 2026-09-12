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

function restoreSourceFocus(selector, fallbackTarget = null) {
  if (typeof window === "undefined" || typeof document === "undefined") {
    return () => {};
  }

  let explicitUserIntent = false;
  const timers = [];
  const noteExplicitIntent = () => {
    explicitUserIntent = true;
  };
  const attempt = () => {
    if (explicitUserIntent) return;
    const target = document.querySelector(selector) || fallbackTarget;
    if (!target || !target.isConnected || typeof target.focus !== "function") return;
    target.focus({ preventScroll: true });
  };

  window.addEventListener("pointerdown", noteExplicitIntent, true);
  window.addEventListener("keydown", noteExplicitIntent, true);
  window.addEventListener("touchstart", noteExplicitIntent, true);

  attempt();
  [0, 60, 180, 360, 720, 1200, 1800].forEach((delay) => {
    timers.push(window.setTimeout(attempt, delay));
  });

  const cleanup = () => {
    timers.forEach((timer) => window.clearTimeout(timer));
    window.removeEventListener("pointerdown", noteExplicitIntent, true);
    window.removeEventListener("keydown", noteExplicitIntent, true);
    window.removeEventListener("touchstart", noteExplicitIntent, true);
  };
  timers.push(window.setTimeout(cleanup, 1900));
  return cleanup;
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
    let cancelFocusRestore = null;
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

        const sharedTarget = current.sharedSourceSelector
          ? await waitForElement(current.sharedSourceSelector)
          : null;
        if (cancelled) return;
        const contract = consumeArmedCameraReturn();
        completeCameraIntent(contract, target, { returning: true, sharedElement: sharedTarget });

        // Browser history, AnimatePresence and sibling autofocus effects may
        // programmatically move focus while the returning route settles. The
        // exact invoking control remains authoritative until the learner makes
        // a new explicit pointer/keyboard/touch choice.
        cancelFocusRestore = restoreSourceFocus(selector, target);
      });
    }

    return () => {
      cancelled = true;
      cancelFocusRestore?.();
    };
  }, [location.pathname, reduced]);

  return null;
}
