import { useEffect, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import { NavArrowLeft, NavArrowRight } from "iconoir-react";
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

export function deriveModuleDockState(phases = []) {
  if (!Array.isArray(phases) || phases.length === 0) {
    return { currentIndex: -1, previousIndex: -1, nextIndex: -1, current: null };
  }
  const currentIndex = Math.max(0, phases.findIndex((phase) => phase.role === "current"));
  let previousIndex = -1;
  for (let i = currentIndex - 1; i >= 0; i -= 1) {
    if (!phases[i].disabled && phases[i].role !== "locked") {
      previousIndex = i;
      break;
    }
  }
  let nextIndex = -1;
  for (let i = currentIndex + 1; i < phases.length; i += 1) {
    if (!phases[i].disabled && phases[i].role !== "locked") {
      nextIndex = i;
      break;
    }
  }
  return { currentIndex, previousIndex, nextIndex, current: phases[currentIndex] || null };
}

/**
 * Contextual dock for an already-rendered module journey. It projects the
 * existing phase hierarchy and delegates navigation to the existing phase
 * toggle buttons. It never writes progress, unlocks a phase, or calls an API.
 */
export default function SpatialModuleDock() {
  const location = useLocation();
  const onModule = MODULE_ROUTE.test(location.pathname);
  const [phases, setPhases] = useState([]);

  useEffect(() => {
    if (!onModule || typeof document === "undefined") {
      setPhases([]);
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
      if (frame != null) window.cancelAnimationFrame(frame);
    };
  }, [location.pathname, onModule]);

  const state = useMemo(() => deriveModuleDockState(phases), [phases]);
  if (!onModule || !state.current) return null;

  const activate = (index) => {
    const phase = phases[index];
    if (!phase || phase.disabled || phase.role === "locked") return;
    phase.button?.focus?.({ preventScroll: true });
    phase.button?.click?.();
  };

  return (
    <nav
      className="spatial-module-dock"
      data-testid="spatial-module-dock"
      data-spatial-current-phase={state.current.key}
      aria-label="Navigation du module"
    >
      <button
        type="button"
        className="spatial-module-dock__nav"
        disabled={state.previousIndex < 0}
        onClick={() => activate(state.previousIndex)}
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
            />
          ))}
        </div>
      </div>

      <button
        type="button"
        className="spatial-module-dock__nav"
        disabled={state.nextIndex < 0}
        onClick={() => activate(state.nextIndex)}
        aria-label="Phase suivante disponible"
        data-testid="spatial-module-dock-next"
      >
        <NavArrowRight width={18} height={18} />
      </button>
    </nav>
  );
}
