import { deriveModuleDockState, predictReachableDockIndex } from "@/lib/spatial/moduleDockState";
import { CADENCE_STATES } from "@/lib/spatial/cadence";

describe("SpatialModuleDock state", () => {
  test("projects current and adjacent reachable phases without inventing unlocks", () => {
    const phases = [
      { key: "hook", role: "acquired", disabled: false },
      { key: "objectives", role: "current", disabled: false },
      { key: "course", role: "next", disabled: false },
      { key: "workshop", role: "locked", disabled: true },
    ];
    expect(deriveModuleDockState(phases)).toMatchObject({
      currentIndex: 1,
      previousIndex: 0,
      nextIndex: 2,
      current: { key: "objectives" },
    });
  });

  test("never exposes a locked phase as next navigation", () => {
    const phases = [
      { key: "hook", role: "current", disabled: false },
      { key: "objectives", role: "locked", disabled: true },
    ];
    expect(deriveModuleDockState(phases).nextIndex).toBe(-1);
  });

  test("fails safe before the module DOM exists or before a current phase exists", () => {
    expect(deriveModuleDockState([])).toEqual({
      currentIndex: -1,
      previousIndex: -1,
      nextIndex: -1,
      current: null,
    });
    expect(deriveModuleDockState([{ key: "hook", role: "next", disabled: false }])).toEqual({
      currentIndex: -1,
      previousIndex: -1,
      nextIndex: -1,
      current: null,
    });
  });

  test("predicts only one already-reachable adjacent phase during repeated cadence", () => {
    const phases = [
      { key: "hook", role: "acquired", disabled: false },
      { key: "objectives", role: "current", disabled: false },
      { key: "course", role: "next", disabled: false },
      { key: "workshop", role: "locked", disabled: true },
    ];
    expect(predictReachableDockIndex(phases, 1, 1, CADENCE_STATES.REPEATED)).toBe(2);
    expect(predictReachableDockIndex(phases, 2, 1, CADENCE_STATES.FAST_REPEAT)).toBe(-1);
    expect(predictReachableDockIndex(phases, 1, 1, CADENCE_STATES.SINGLE)).toBe(-1);
  });

  test("prediction never jumps over a locked domain barrier", () => {
    const phases = [
      { key: "hook", role: "current", disabled: false },
      { key: "objectives", role: "locked", disabled: true },
      { key: "course", role: "acquired", disabled: false },
    ];
    expect(predictReachableDockIndex(phases, 0, 1, CADENCE_STATES.FAST_REPEAT)).toBe(-1);
  });
});
