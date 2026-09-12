import { useEffect, useMemo, useRef, useState } from "react";
import { useLocation } from "react-router-dom";
import { NavArrowLeft, NavArrowRight } from "iconoir-react";
import { createCadenceTracker, CADENCE_STATES } from "@/lib/spatial/cadence";
import {
  deriveModuleDockState,
  predictReachableDockIndex,
} from "@/lib/spatial/moduleDockState";
import {
  emitSpatialInteraction,
  SPATIAL_INTERACTION_TYPES,
} from "@/lib/spatial/spatialInteractionEvents";
import "./spatial-module-dock.css";

const MODULE_ROUTE = /^\/formations\/[^/]+\/modules\/[^/?#]+$/;
const PHASE_TOGGLE_PREFIX = "phase-toggle-";

function readModulePhases(root = document) {
  if (!root?.querySelectorAll) return [];
  return Array.from(root.querySelectorAll(`[data-testid^="${PHASE_TOGGLE_PREFIX}"]`)).map((button, index) => {
    const key = button.getAttribute("data-testid")?.slice(PHASE_TOGGLE_PREFIX.length) || String(index);
    const shell = button.closest?.("[data-journey-role]");
    return {
      key,
      index,
      label: button.textContent?.replace(/\s+/g, " ").trim() || key,
      role: shell?.getAttribute("data-journey-role") || "locked",
      disabled: Boolean(button.disabled),
      button,
    };
  });
}

/**
 * Contextual dock for an already-rendered module journey. It projects the
 * existing phase hierarchy and delegates navigation to the existing phase
 * toggle buttons. It never writes progress, unlocks a phase, or calls an API.
 * Repeated navigation may preview one already-reachable adjacent phase only.
 */
export default function SpatialModuleDock() {
  const location = useLocation();
  const onModule = MODULE_ROUTE.test(location.pathname);
  const [phases, setPhases] = useState([]);
  const [cadenceState, setCadenceState] = useState(CADENCE_STATES.STOPPED);
  const [predictedIndex, setPredictedIndex] = useState(-1);
  const cadenceRef = useRef(null);

  if (!cadenceRef.current) cadenceRef.current = createCadenceTracker();

  useEffect(() => {
    if (!onModule || typeof document === "undefined") {
      setPhases([]);
      setPredictedIndex(-1);
      setCadenceState(CADENCE_STATES.STOPPED);
      return undefined;
    }

    let frame = null;
    const read = () => {
      if (frame != null) return;
      frame = window.requestAnimationFrame(() => {
        frame = null;
        setPhases(readModulePhases(document));
      });
    };

    read();
    const observer = new MutationObserver(read);
    observer.observe(document.documentElement, {
      subtree: true,
      childList: true,
      attributes: true,
      attributeFilter: ["data-journey-role", "disabled"],
    });
    return () => {
      observer.disconnect();
      cadenceRef.current?.dispose?.();
      if (frame != null) window.cancelAnimationFrame(frame);
    };
  }, [location.pathname, onModule]);

  const state = useMemo(() => deriveModuleDockState(phases), [phases]);

  useEffect(() => {
    if (predictedIndex < 0) return;
    const phase = phases[predictedIndex];
    if (!phase || phase.disabled || phase.role === "locked") setPredictedIndex(-1);
  }, [phases, predictedIndex]);

  if (!onModule || !state.current) return null;

  const activate = (index, direction) => {
    const phase = phases[index];
    if (!phase || phase.disabled || phase.role === "locked") {
      emitSpatialInteraction(SPATIAL_INTERACTION_TYPES.BLOCKED, { cadenceState });
      return;
    }

    const tracker = cadenceRef.current;
    const nextCadence = tracker?.trackInput(direction, (nextState) => {
      setCadenceState(nextState);
      if (nextState === CADENCE_STATES.STOPPED || nextState === CADENCE_STATES.REVERSAL) {
        setPredictedIndex(-1);
      }
    }) || CADENCE_STATES.SINGLE;

    setCadenceState(nextCadence);
    setPredictedIndex(predictReachableDockIndex(phases, index, direction, nextCadence));
    emitSpatialInteraction(SPATIAL_INTERACTION_TYPES.NAV_MOVE, { cadenceState: nextCadence });
    phase.button?.focus?.({ preventScroll: true });
    phase.button?.click?.();
    emitSpatialInteraction(SPATIAL_INTERACTION_TYPES.SNAP, { cadenceState: nextCadence });
  };

  const predictedPhase = phases[predictedIndex]?.key || "NONE";

  return (
    <nav
      className="spatial-module-dock"
      data-testid="spatial-module-dock"
      data-spatial-current-phase={state.current.key}
      data-spatial-cadence={cadenceState}
      data-spatial-predicted-phase={predictedPhase}
      aria-label="Navigation du module"
    >
      <button
        type="button"
        className="spatial-module-dock__nav"
        disabled={state.previousIndex < 0}
        onClick={() => activate(state.previousIndex, -1)}
        aria-label="Phase précédente"
        data-testid="spatial-module-dock-prev"
      >
        <NavArrowLeft width={18} height={18} />
      </button>

      <div className="spatial-module-dock__body" aria-live="polite">
        <div className="spatial-module-dock__eyebrow">
          Phase {state.currentIndex + 1} / {phases.length}
        </div>
        <div className="spatial-module-dock__label">{state.current.label}</div>
        <div className="spatial-module-dock__rail" aria-hidden="true">
          {phases.map((phase, index) => (
            <span
              key={phase.key}
              className="spatial-module-dock__dot"
              data-role={phase.role}
              data-current={index === state.currentIndex ? "true" : "false"}
              data-predicted={index === predictedIndex ? "true" : "false"}
            />
          ))}
        </div>
      </div>

      <button
        type="button"
        className="spatial-module-dock__nav"
        disabled={state.nextIndex < 0}
        onClick={() => activate(state.nextIndex, 1)}
        aria-label="Phase suivante disponible"
        data-testid="spatial-module-dock-next"
      >
        <NavArrowRight width={18} height={18} />
      </button>
    </nav>
  );
}
