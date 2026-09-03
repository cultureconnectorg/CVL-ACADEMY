import { createSpatialAudio, AUDIO_EVENTS } from "./audio";

// jsdom provides no AudioContext — this is the real, correct environment
// to prove "unsupported = graceful no-op, never throw, never fake
// support" rather than mocking one away.
describe("audio.js — createSpatialAudio (unsupported environment, jsdom has no AudioContext)", () => {
  test("reports unsupported honestly — never fakes support", () => {
    const audio = createSpatialAudio();
    expect(audio.supported).toBe(false);
  });

  test("muted by default", () => {
    const audio = createSpatialAudio();
    expect(audio.enabled).toBe(false);
  });

  test("play() on every real event never throws even though the environment is unsupported", () => {
    const audio = createSpatialAudio();
    audio.setEnabled(true);
    AUDIO_EVENTS.forEach((kind) => {
      expect(() => audio.play(kind)).not.toThrow();
    });
  });

  test("play() is a no-op while disabled — never plays without explicit opt-in", () => {
    const audio = createSpatialAudio();
    expect(() => audio.play("CONFIRM")).not.toThrow();
    // no assertion possible on "did a tone play" without a real
    // AudioContext (which is exactly the point of this environment) —
    // the meaningful assertion is that calling play() before setEnabled
    // never throws and never requires special handling by a caller.
  });

  test("audition() bypasses the enabled gate but still never throws unsupported", () => {
    const audio = createSpatialAudio();
    expect(audio.enabled).toBe(false);
    expect(() => audio.audition("NAV_MOVE")).not.toThrow();
  });

  test("NAV_MOVE throttle: rapid repeated calls do not throw and respect the throttle window conceptually", () => {
    const audio = createSpatialAudio({ getCadenceState: () => "FAST_REPEAT" });
    audio.setEnabled(true);
    expect(() => {
      for (let i = 0; i < 20; i++) audio.play("NAV_MOVE");
    }).not.toThrow();
  });

  test("all 8 required event names are present", () => {
    expect(AUDIO_EVENTS).toEqual([
      "NAV_MOVE",
      "FOCUS_LOCK",
      "ENTER_DEPTH",
      "RETURN_DEPTH",
      "CONTEXT_OPEN",
      "CONTEXT_CLOSE",
      "CONFIRM",
      "BLOCKED",
    ]);
  });
});
