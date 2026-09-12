import { useEffect } from "react";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { useReducedMotion } from "@/lib/useReducedMotion";
import {
  armCameraReturn,
  beginCameraIntent,
  readReturnCameraContract,
} from "@/lib/spatial/cameraRuntime";

const MODULE_ROUTE = /^\/formations\/([^/]+)\/modules\/([^/?#]+)$/;
const FORMATION_ROUTE = /^\/formations\/([^/?#]+)$/;

function routeFromHref(href) {
  try {
    const url = new URL(href, window.location.origin);
    return url.pathname;
  } catch {
    return null;
  }
}

function findSharedSource(anchorId, link) {
  const scope = link?.closest?.("[data-testid]") || document;
  const local = Array.from(scope.querySelectorAll?.("[data-spatial-shared-source]") || []).find(
    (node) => node.getAttribute("data-spatial-shared-source") === anchorId,
  );
  if (local) return local;
  return Array.from(document.querySelectorAll("[data-spatial-shared-source]")).find(
    (node) => node.getAttribute("data-spatial-shared-source") === anchorId,
  ) || null;
}

function buildForwardContract(link, destinationRoute) {
  const moduleMatch = destinationRoute.match(MODULE_ROUTE);
  if (moduleMatch) {
    const [, formationCode, moduleCode] = moduleMatch;
    const anchorId = `module:${formationCode}:${moduleCode}`;
    const destinationSelector = '[data-testid="module-journey"] h1';
    return {
      anchorId,
      destinationRoute,
      destinationSelector,
      sharedElement: findSharedSource(anchorId, link),
      sharedSourceSelector: `[data-spatial-shared-source="${anchorId}"]`,
      sharedDestinationSelector: destinationSelector,
    };
  }

  const formationMatch = destinationRoute.match(FORMATION_ROUTE);
  if (formationMatch && window.location.pathname === "/formations") {
    const [, formationCode] = formationMatch;
    const anchorId = `formation:${formationCode}`;
    const destinationSelector = '[data-testid="formation-detail"] h1';
    return {
      anchorId,
      destinationRoute,
      destinationSelector,
      sharedElement: findSharedSource(anchorId, link),
      sharedSourceSelector: `[data-spatial-shared-source="${anchorId}"]`,
      sharedDestinationSelector: destinationSelector,
    };
  }

  return null;
}

/**
 * Captures only existing navigation. It never prevents navigation or invents a
 * route. Source geometry is recorded before React unmounts it; browser Back or
 * an explicit link to the exact source arms the inverse camera/shared-element path.
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

      const forward = buildForwardContract(link, destinationRoute);
      if (!forward) return;
      beginCameraIntent({
        ...forward,
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
