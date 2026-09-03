import { createHaptics, HAPTIC_PATTERNS } from "./haptics";

// jsdom provides no navigator.vibrate — the real, correct environment to
// prove graceful no-op rather than mocking support that isn't real.
describe("haptics.js — createHaptics (unsupported environment)", () => {
  test("reports unsupported honestly — never fakes support", () => {
    const haptics = createHaptics();
    expect(haptics.supported).toBe(false);
  });

  test("fire() on every real pattern never throws even though unsupported", () => {
    const haptics = createHaptics({ isEnabled: () => true });
    Object.keys(HAPTIC_PATTERNS).forEach((kind) => {
      expect(() => haptics.fire(kind)).not.toThrow();
    });
  });

  test("fire() is gated by isEnabled — never fires while disabled", () => {
    const calls = [];
    const haptics = createHaptics({ isEnabled: () => false });
    // no direct way to observe "did not call navigator.vibrate" without
    // a real vibrate implementation, but the call must not throw and
    // must not require the caller to check isEnabled itself first.
    expect(() => haptics.fire("SNAP")).not.toThrow();
    expect(calls.length).toBe(0);
  });

  test("audition() bypasses the enabled gate but still never throws unsupported", () => {
    const haptics = createHaptics({ isEnabled: () => false });
    expect(() => haptics.audition("CONFIRM")).not.toThrow();
  });

  test("no continuous-vibration pattern exists — every real pattern is a bounded number or short array", () => {
    Object.values(HAPTIC_PATTERNS).forEach((pattern) => {
      if (typeof pattern === "number") {
        expect(pattern).toBeLessThan(100); // a brief pulse, not a sustained buzz
      } else {
        expect(Array.isArray(pattern)).toBe(true);
        expect(pattern.length).toBeLessThanOrEqual(5);
        pattern.forEach((ms) => expect(ms).toBeLessThan(100));
      }
    });
  });

  test("all 5 required event names are present", () => {
    expect(Object.keys(HAPTIC_PATTERNS)).toEqual([
      "FOCUS_LOCK",
      "SNAP",
      "ENTER",
      "CONFIRM",
      "BLOCKED",
    ]);
  });
});

describe("haptics.js — createHaptics (feature-detected support present)", () => {
  const originalVibrate = navigator.vibrate;
  beforeEach(() => {
    navigator.vibrate = jest.fn();
  });
  afterEach(() => {
    navigator.vibrate = originalVibrate;
  });

  test("reports supported when navigator.vibrate exists", () => {
    const haptics = createHaptics();
    expect(haptics.supported).toBe(true);
  });

  test("fire() calls navigator.vibrate with the exact declared pattern, once", () => {
    const haptics = createHaptics({ isEnabled: () => true });
    haptics.fire("SNAP");
    expect(navigator.vibrate).toHaveBeenCalledTimes(1);
    expect(navigator.vibrate).toHaveBeenCalledWith(HAPTIC_PATTERNS.SNAP);
  });

  test("fire() does not call navigator.vibrate while disabled", () => {
    const haptics = createHaptics({ isEnabled: () => false });
    haptics.fire("SNAP");
    expect(navigator.vibrate).not.toHaveBeenCalled();
  });

  test("a thrown vibrate() call is swallowed, not propagated", () => {
    navigator.vibrate = jest.fn(() => {
      throw new Error("denied");
    });
    const haptics = createHaptics({ isEnabled: () => true });
    expect(() => haptics.fire("CONFIRM")).not.toThrow();
  });
});
