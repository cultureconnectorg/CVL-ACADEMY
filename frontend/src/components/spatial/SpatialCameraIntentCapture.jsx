import { useEffect } from "react";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { useReducedMotion } from "@/lib/useReducedMotion";
import {
  armCameraReturn,
  beginCameraIntent,
  readReturnCameraContract,
} from "@/lib/spatial/cameraRuntime";

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
 * Captures only existing navigation. It never prevents navigation or invents a
 * route. Source geometry is recorded before React unmounts it; browser Back or
 * an explicit link to the exact source arms the inverse camera path.
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
      if (!destinationRoute) return;

      const returnContract = readReturnCameraContract();
      if (
        returnContract &&
        window.location.pathname === returnContract.destinationRoute &&
        destinationRoute === returnContract.sourceRoute
      ) {
        const destinationAnchor = returnContract.destinationSelector
          ? document.querySelector(returnContract.destinationSelector)
          : null;
        armCameraReturn(returnContract, destinationAnchor);
        return;
      }

      const match = destinationRoute.match(MODULE_ROUTE);
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

    const onPopState = () => {
      const contract = readReturnCameraContract();
      if (!contract) return;
      const destinationAnchor = contract.destinationSelector
        ? document.querySelector(contract.destinationSelector)
        : null;
      if (destinationAnchor) armCameraReturn(contract, destinationAnchor);
    };

    document.addEventListener("click", onClickCapture, true);
    window.addEventListener("popstate", onPopState);
    return () => {
      document.removeEventListener("click", onClickCapture, true);
      window.removeEventListener("popstate", onPopState);
    };
  }, [reduced]);

  return null;
}
