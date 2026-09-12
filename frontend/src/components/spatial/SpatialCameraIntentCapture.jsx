import { useEffect } from "react";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { beginCameraIntent } from "@/lib/spatial/cameraRuntime";

const MODULE_ROUTE = /^\/formations\/([^/]+)\/modules\/([^/?#]+)$/;

function routeFromHref(href) {
  try {
    const url = new URL(href, window.location.origin);
    return url.pathname;
  } catch {
    return null;
  }
}

/**
 * Captures only existing links that really enter a module. It never prevents
 * navigation or invents a route. The source DOM geometry is recorded before
 * React unmounts it; the persistent bridge resolves the destination after mount.
 */
export default function SpatialCameraIntentCapture() {
  const reduced = useReducedMotion();

  useEffect(() => {
    if (!FEATURE_FLAGS.SPATIAL_ROUTE_TRANSITIONS || reduced || typeof document === "undefined") {
      return undefined;
    }

    const onClickCapture = (event) => {
      if (event.defaultPrevented || event.button > 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      const link = event.target?.closest?.("a[href]");
      if (!link) return;
      const destinationRoute = routeFromHref(link.getAttribute("href"));
      const match = destinationRoute?.match(MODULE_ROUTE);
      if (!match) return;
      const [, formationCode, moduleCode] = match;
      beginCameraIntent({
        anchorId: `module:${formationCode}:${moduleCode}`,
        destinationRoute,
        destinationSelector: '[data-testid="module-journey"] h1',
        element: link,
        returnRoute: window.location.pathname,
      });
    };

    document.addEventListener("click", onClickCapture, true);
    return () => document.removeEventListener("click", onClickCapture, true);
  }, [reduced]);

  return null;
}
