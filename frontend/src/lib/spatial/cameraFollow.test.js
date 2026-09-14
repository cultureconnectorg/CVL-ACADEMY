import {
  CAMERA_STATES,
  clampPct,
  computeOriginPct,
  computeFlightKeyframes,
  createCameraToken,
} from "./cameraFollow";

describe("cameraFollow.js — camera-follow primitives (Rail 4)", () => {
  test("CAMERA_STATES carries the exact 8 named states from the H0.8 spec, frozen", () => {
    expect(Object.keys(CAMERA_STATES).sort()).toEqual(
      ["IDLE", "INTENT", "LOCKING", "FOLLOWING", "CROSSING", "REVEALING", "SETTLING", "RETURNING"].sort()
    );
    expect(Object.isFrozen(CAMERA_STATES)).toBe(true);
  });

  describe("clampPct", () => {
    test("clamps below 0 to 0", () => {
      expect(clampPct(-15)).toBe(0);
    });
    test("clamps above 100 to 100", () => {
      expect(clampPct(140)).toBe(100);
    });
    test("passes through an in-range value", () => {
      expect(clampPct(42.5)).toBe(42.5);
    });
  });

  describe("computeOriginPct", () => {
    test("center of the container is 50%", () => {
      const containerRect = { left: 0, width: 1000 };
      const rect = { left: 450, width: 100 }; // center at 500 -> 50%
      expect(computeOriginPct(rect, containerRect)).toBeCloseTo(50, 5);
    });
    test("left edge clamps to 0, right edge clamps to 100", () => {
      const containerRect = { left: 0, width: 1000 };
      expect(computeOriginPct({ left: -500, width: 10 }, containerRect)).toBe(0);
      expect(computeOriginPct({ left: 1400, width: 10 }, containerRect)).toBe(100);
    });
    test("zero-width container never divides by zero", () => {
      expect(computeOriginPct({ left: 10, width: 10 }, { left: 0, width: 0 })).toBe(50);
    });
  });

  describe("computeFlightKeyframes", () => {
    test("same rect twice: zero travel, scale 1", () => {
      const rect = { left: 20, top: 30, width: 100 };
      expect(computeFlightKeyframes(rect, rect)).toEqual({ dx: 0, dy: 0, scale: 1 });
    });
    test("real dx/dy/scale for a genuine source->destination flight", () => {
      const from = { left: 100, top: 200, width: 80 };
      const to = { left: 300, top: 150, width: 160 };
      expect(computeFlightKeyframes(from, to)).toEqual({ dx: 200, dy: -50, scale: 2 });
    });
    test("zero-width source never divides by zero", () => {
      const from = { left: 0, top: 0, width: 0 };
      const to = { left: 10, top: 10, width: 50 };
      expect(computeFlightKeyframes(from, to).scale).toBe(1);
    });
  });

  describe("createCameraToken — retarget/cancel guard", () => {
    test("a fresh token is current until superseded", () => {
      const cam = createCameraToken();
      const t1 = cam.next();
      expect(cam.isCurrent(t1)).toBe(true);
    });
    test("calling next() again supersedes the previous token (LATEST_USER_INTENT_WINS)", () => {
      const cam = createCameraToken();
      const t1 = cam.next();
      const t2 = cam.next();
      expect(cam.isCurrent(t1)).toBe(false);
      expect(cam.isCurrent(t2)).toBe(true);
      expect(t2).not.toBe(t1);
    });
    test("rapid repeated retargets never confuse an old token for current", () => {
      const cam = createCameraToken();
      const tokens = Array.from({ length: 5 }, () => cam.next());
      tokens.slice(0, -1).forEach((t) => expect(cam.isCurrent(t)).toBe(false));
      expect(cam.isCurrent(tokens[tokens.length - 1])).toBe(true);
    });
  });
});
