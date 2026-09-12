import { useEffect } from "react";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { createFramePacing } from "@/lib/spatial/framePacing";

export const SPATIAL_FRAME_PACING_EVENT = "cvln:spatial-frame-pacing";

/**
 * Debug-only lifecycle-aware frame pacing sampler.
 * It starts only when SPATIAL_DEBUG is explicitly enabled, pauses with the
 * document, emits measured reports (never synthetic production claims), and
 * tears every timer/rAF down on unmount.
 */
export default function SpatialRuntimeDiagnostics() {
  useEffect(() => {
    if (!FEATURE_FLAGS.SPATIAL_DEBUG || typeof window === "undefined" || typeof document === "undefined") {
      return undefined;
    }

    const pacing = createFramePacing();
    let intervalId = null;

    const emitReport = () => {
      if (document.visibilityState !== "visible" || typeof CustomEvent !== "function") return;
      window.dispatchEvent(new CustomEvent(SPATIAL_FRAME_PACING_EVENT, {
        detail: pacing.report(),
      }));
    };

    const syncLifecycle = () => {
      if (document.visibilityState === "visible") {
        pacing.start();
        if (intervalId === null) intervalId = window.setInterval(emitReport, 2000);
      } else {
        pacing.stop();
        if (intervalId !== null) {
          window.clearInterval(intervalId);
          intervalId = null;
        }
      }
    };

    document.addEventListener("visibilitychange", syncLifecycle);
    syncLifecycle();

    return () => {
      document.removeEventListener("visibilitychange", syncLifecycle);
      pacing.stop();
      if (intervalId !== null) window.clearInterval(intervalId);
    };
  }, []);

  return null;
}
