import { createCadenceTracker, CADENCE_STATES } from "./cadence";

function makeManualTimers() {
  let t = 0;
  let pending = null;
  return {
    now: () => t,
    setTimeout: (fn) => {
      pending = fn;
      return 1;
    },
    clearTimeout: () => {
      pending = null;
    },
    advance(ms) {
      t += ms;
    },
    fireTimeout() {
      if (pending) {
        const fn = pending;
        pending = null;
        fn();
      }
    },
  };
}

describe("cadence.js — createCadenceTracker", () => {
  test("a single, isolated input classifies as SINGLE", () => {
    const timers = makeManualTimers();
    const cadence = createCadenceTracker(timers);
    expect(cadence.trackInput(1)).toBe(CADENCE_STATES.SINGLE);
  });

  test("two same-direction inputs within the window classify as REPEATED", () => {
    const timers = makeManualTimers();
    const cadence = createCadenceTracker(timers);
    cadence.trackInput(1);
    timers.advance(60);
    expect(cadence.trackInput(1)).toBe(CADENCE_STATES.REPEATED);
  });

  test("3+ same-direction inputs within the window classify as FAST_REPEAT", () => {
    const timers = makeManualTimers();
    const cadence = createCadenceTracker(timers);
    cadence.trackInput(1);
    timers.advance(50);
    cadence.trackInput(1);
    timers.advance(50);
    expect(cadence.trackInput(1)).toBe(CADENCE_STATES.FAST_REPEAT);
    expect(cadence.streak).toBe(3);
  });

  test("a direction change within the window classifies as REVERSAL", () => {
    const timers = makeManualTimers();
    const cadence = createCadenceTracker(timers);
    cadence.trackInput(1);
    timers.advance(50);
    cadence.trackInput(1);
    timers.advance(50);
    expect(cadence.trackInput(-1)).toBe(CADENCE_STATES.REVERSAL);
  });

  test("no input for the stop delay classifies as STOPPED and resets the streak", () => {
    const timers = makeManualTimers();
    const cadence = createCadenceTracker(timers);
    cadence.trackInput(1);
    timers.fireTimeout(); // simulate the stop-delay timer firing
    expect(cadence.state).toBe(CADENCE_STATES.STOPPED);
    expect(cadence.streak).toBe(0);
  });

  test("an input outside the fast-repeat window (slow, deliberate presses) reads as SINGLE each time, not REPEATED", () => {
    const timers = makeManualTimers();
    const cadence = createCadenceTracker(timers);
    cadence.trackInput(1);
    timers.advance(1000); // well past the window
    expect(cadence.trackInput(1)).toBe(CADENCE_STATES.SINGLE);
  });

  test("dwellDelay stretches only during FAST_REPEAT, never during normal cadence", () => {
    const timers = makeManualTimers();
    const cadence = createCadenceTracker(timers);
    expect(cadence.dwellDelay(100)).toBe(100); // STOPPED at rest
    cadence.trackInput(1);
    timers.advance(50);
    cadence.trackInput(1);
    timers.advance(50);
    cadence.trackInput(1); // now FAST_REPEAT
    expect(cadence.dwellDelay(100)).toBeCloseTo(220, 5);
  });

  test("dispose() cancels a pending stop timer without throwing", () => {
    const timers = makeManualTimers();
    const cadence = createCadenceTracker(timers);
    cadence.trackInput(1);
    expect(() => cadence.dispose()).not.toThrow();
  });
});
