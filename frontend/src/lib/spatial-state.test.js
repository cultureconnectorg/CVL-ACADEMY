import {
  SPATIAL_STATES,
  SPATIAL_EVENTS,
  isValidSpatialTransition,
  spatialStateReducer,
} from "@/lib/spatial-state";

describe("spatial-state (W1-D)", () => {
  test("walks the full IDLE -> ... -> IDLE cycle in order", () => {
    const sequence = [
      SPATIAL_EVENTS.FOCUS,
      SPATIAL_EVENTS.APPROACH,
      SPATIAL_EVENTS.ENTER,
      SPATIAL_EVENTS.ACTIVATE,
      SPATIAL_EVENTS.REVEAL_CONTEXT,
      SPATIAL_EVENTS.DISMISS_CONTEXT,
      SPATIAL_EVENTS.LEAVE,
      SPATIAL_EVENTS.ARRIVE,
    ];
    const expected = [
      SPATIAL_STATES.FOCUS,
      SPATIAL_STATES.APPROACH,
      SPATIAL_STATES.ENTER,
      SPATIAL_STATES.ACTIVE,
      SPATIAL_STATES.CONTEXT,
      SPATIAL_STATES.ACTIVE,
      SPATIAL_STATES.RETURN,
      SPATIAL_STATES.IDLE,
    ];
    let state = SPATIAL_STATES.IDLE;
    sequence.forEach((event, i) => {
      state = spatialStateReducer(state, event);
      expect(state).toBe(expected[i]);
    });
  });

  test("LEAVE is legal directly from ACTIVE (context is optional)", () => {
    expect(isValidSpatialTransition(SPATIAL_STATES.ACTIVE, SPATIAL_EVENTS.LEAVE)).toBe(true);
    expect(spatialStateReducer(SPATIAL_STATES.ACTIVE, SPATIAL_EVENTS.LEAVE)).toBe(
      SPATIAL_STATES.RETURN
    );
  });

  test("CANCEL_APPROACH returns to FOCUS, not IDLE", () => {
    expect(spatialStateReducer(SPATIAL_STATES.APPROACH, SPATIAL_EVENTS.CANCEL_APPROACH)).toBe(
      SPATIAL_STATES.FOCUS
    );
  });

  test("an event not modeled for the current state is a no-op", () => {
    // ACTIVATE is only legal from ENTER — dispatching it from IDLE must
    // not silently jump to ACTIVE.
    expect(isValidSpatialTransition(SPATIAL_STATES.IDLE, SPATIAL_EVENTS.ACTIVATE)).toBe(false);
    expect(spatialStateReducer(SPATIAL_STATES.IDLE, SPATIAL_EVENTS.ACTIVATE)).toBe(
      SPATIAL_STATES.IDLE
    );
  });

  test("RETURN only ever resolves to IDLE via ARRIVE, no shortcuts", () => {
    expect(Object.keys(spatialStateReducerTransitionsFor(SPATIAL_STATES.RETURN))).toEqual([
      SPATIAL_EVENTS.ARRIVE,
    ]);
  });
});

// Small local helper so the "no shortcuts out of RETURN" assertion above
// doesn't need to reach into the module's private transition table.
function spatialStateReducerTransitionsFor(state) {
  const events = Object.values(SPATIAL_EVENTS);
  return events.reduce((acc, event) => {
    if (isValidSpatialTransition(state, event)) acc[event] = true;
    return acc;
  }, {});
}
