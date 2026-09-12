import { CADENCE_STATES } from "./cadence";

function reachable(phase) {
  return Boolean(phase && !phase.disabled && phase.role !== "locked");
}

export function deriveModuleDockState(phases = []) {
  if (!Array.isArray(phases) || phases.length === 0) {
    return { currentIndex: -1, previousIndex: -1, nextIndex: -1, current: null };
  }

  const foundCurrent = phases.findIndex((phase) => phase.role === "current");
  if (foundCurrent < 0) {
    return { currentIndex: -1, previousIndex: -1, nextIndex: -1, current: null };
  }

  const currentIndex = foundCurrent;
  let previousIndex = -1;
  for (let i = currentIndex - 1; i >= 0; i -= 1) {
    if (reachable(phases[i])) {
      previousIndex = i;
      break;
    }
  }

  let nextIndex = -1;
  for (let i = currentIndex + 1; i < phases.length; i += 1) {
    if (reachable(phases[i])) {
      nextIndex = i;
      break;
    }
  }

  return { currentIndex, previousIndex, nextIndex, current: phases[currentIndex] };
}

/**
 * One-step local prediction for the module dock. Prediction never skips over
 * a locked phase: the module sequence is authoritative, so only the immediate
 * adjacent phase may be previewed and only when it is already reachable.
 */
export function predictReachableDockIndex(phases = [], fromIndex, direction, cadenceState) {
  if (
    cadenceState !== CADENCE_STATES.REPEATED
    && cadenceState !== CADENCE_STATES.FAST_REPEAT
  ) return -1;
  if (direction !== 1 && direction !== -1) return -1;
  const candidate = Number(fromIndex) + direction;
  if (!Number.isInteger(candidate) || candidate < 0 || candidate >= phases.length) return -1;
  return reachable(phases[candidate]) ? candidate : -1;
}
