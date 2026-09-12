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

  return { currentIndex, previousIndex, nextIndex, current: phases[currentIndex] };
}
