import {
  emitSpatialInteraction,
  isSpatialInteractionType,
  SPATIAL_INTERACTION_EVENT,
  SPATIAL_INTERACTION_TYPES,
} from "./spatialInteractionEvents";

describe("spatial interaction events", () => {
  test("accepts only canonical perceptual interaction types", () => {
    expect(isSpatialInteractionType(SPATIAL_INTERACTION_TYPES.NAV_MOVE)).toBe(true);
    expect(isSpatialInteractionType(SPATIAL_INTERACTION_TYPES.SNAP)).toBe(true);
    expect(isSpatialInteractionType("PROGRESS_MUTATION")).toBe(false);
  });

  test("emits only perceptual cadence metadata", () => {
    const listener = jest.fn();
    window.addEventListener(SPATIAL_INTERACTION_EVENT, listener);
    expect(emitSpatialInteraction(SPATIAL_INTERACTION_TYPES.NAV_MOVE, { cadenceState: "REPEATED" })).toBe(true);
    expect(listener).toHaveBeenCalledTimes(1);
    expect(listener.mock.calls[0][0].detail).toEqual({
      type: SPATIAL_INTERACTION_TYPES.NAV_MOVE,
      cadenceState: "REPEATED",
    });
    window.removeEventListener(SPATIAL_INTERACTION_EVENT, listener);
  });

  test("rejects unknown interaction types without dispatching", () => {
    const listener = jest.fn();
    window.addEventListener(SPATIAL_INTERACTION_EVENT, listener);
    expect(emitSpatialInteraction("UNLOCK_NEXT", { cadenceState: "FAST_REPEAT" })).toBe(false);
    expect(listener).not.toHaveBeenCalled();
    window.removeEventListener(SPATIAL_INTERACTION_EVENT, listener);
  });
});
