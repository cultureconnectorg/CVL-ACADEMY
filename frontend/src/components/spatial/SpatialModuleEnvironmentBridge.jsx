import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import { environmentForModulePhase } from "@/lib/spatial/modulePhaseEnvironment";

const MODULE_ROUTE = /^\/formations\/[^/]+\/modules\/[^/?#]+$/;
const PREFIX = "phase-";

function currentPhaseKey(root = document) {
  const shell = root?.querySelector?.('[data-journey-role="current"]');
  const card = shell?.querySelector?.('[data-testid^="phase-"]');
  const testId = card?.getAttribute?.("data-testid") || "";
  return testId.startsWith(PREFIX) ? testId.slice(PREFIX.length) : null;
}

function applyEnvironment(phase, root = document) {
  const background = root?.querySelector?.('[data-testid="spatial-background"]');
  if (!background) return false;
  const profile = environmentForModulePhase(phase);
  if (!profile) {
    background.removeAttribute("data-spatial-module-phase");
    ["activity", "focus", "depth", "warmth"].forEach((key) => {
      background.style.removeProperty(`--spatial-phase-${key}`);
    });
    return false;
  }
  background.setAttribute("data-spatial-module-phase", phase);
  Object.entries(profile).forEach(([key, value]) => {
    background.style.setProperty(`--spatial-phase-${key}`, String(value));
  });
  return true;
}

/**
 * Projects the already-existing current module phase into environment variables.
 * It observes UI state only; no progression, unlock, navigation or API state is written.
 */
export default function SpatialModuleEnvironmentBridge() {
  const location = useLocation();
  const onModule = MODULE_ROUTE.test(location.pathname);

  useEffect(() => {
    if (typeof document === "undefined") return undefined;
    if (!onModule) {
      applyEnvironment(null, document);
      return undefined;
    }

    let frame = null;
    const sync = () => {
      if (frame != null) return;
      frame = window.requestAnimationFrame(() => {
        frame = null;
        applyEnvironment(currentPhaseKey(document), document);
      });
    };

    sync();
    const observer = new MutationObserver(sync);
    observer.observe(document.documentElement, {
      subtree: true,
      childList: true,
      attributes: true,
      attributeFilter: ["data-journey-role"],
    });
    return () => {
      observer.disconnect();
      if (frame != null) window.cancelAnimationFrame(frame);
      applyEnvironment(null, document);
    };
  }, [location.pathname, onModule]);

  return null;
}

export { currentPhaseKey, applyEnvironment };
