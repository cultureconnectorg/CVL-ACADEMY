import { makeRailPhysics } from "./physics";

// Deterministic clock/frame driver: no real requestAnimationFrame — the
// test owns time completely, one call = one frame at a chosen dt.
function makeManualClock(startT = 0) {
  let t = startT;
  const pending = [];
  return {
    requestFrame(cb) {
      pending.push(cb);
    },
    advance(dtMs) {
      t += dtMs;
      const due = pending.splice(0, pending.length);
      due.forEach((cb) => cb(t));
    },
    get t() {
      return t;
    },
  };
}

describe("physics.js — makeRailPhysics", () => {
  test("target convergence: settles at the target with a clean, monotonic approach", () => {
    const clock = makeManualClock();
    const frames = [];
    let settled = false;
    const physics = makeRailPhysics(
      (pos, vel) => frames.push({ pos, vel }),
      () => {
        settled = true;
      },
      { requestFrame: clock.requestFrame }
    );
    physics.setTarget(1);
    // prime lastT, then step at a normal 60fps cadence
    clock.advance(0);
    for (let i = 0; i < 60 && !settled; i++) clock.advance(16.7);
    expect(settled).toBe(true);
    expect(physics.position).toBeCloseTo(1, 2);
    expect(physics.velocity).toBeCloseTo(0, 2);
    // monotonic: once past the midpoint, position never overshoots past 1
    const maxPos = Math.max(...frames.map((f) => f.pos));
    expect(maxPos).toBeLessThanOrEqual(1.001);
  });

  test("mid-flight retarget preserves velocity — never resets to zero then restarts", () => {
    const clock = makeManualClock();
    let lastVel = 0;
    const physics = makeRailPhysics(
      (pos, vel) => {
        lastVel = vel;
      },
      null,
      { requestFrame: clock.requestFrame }
    );
    physics.setTarget(1);
    clock.advance(0);
    clock.advance(16.7);
    clock.advance(16.7); // now genuinely moving, velocity > 0
    expect(lastVel).toBeGreaterThan(0);
    const velocityBeforeRetarget = physics.velocity;
    physics.setTarget(2); // retarget mid-flight
    // velocity must not have been reset to 0 by the retarget call itself
    expect(physics.velocity).toBeCloseTo(velocityBeforeRetarget, 5);
    clock.advance(16.7);
    // still moving with real velocity right after retarget — not relaunched from rest
    expect(Math.abs(physics.velocity)).toBeGreaterThan(0);
  });

  test("reversal (-> -> <-): brakes and converges cleanly to the new target, no oscillation", () => {
    const clock = makeManualClock();
    const physics = makeRailPhysics(() => {}, null, { requestFrame: clock.requestFrame });
    physics.setTarget(1);
    clock.advance(0);
    clock.advance(16.7);
    physics.setTarget(2);
    clock.advance(16.7);
    physics.setTarget(1); // reversal
    const positions = [];
    for (let i = 0; i < 120; i++) {
      clock.advance(16.7);
      positions.push(physics.position);
      if (!physics.running) break;
    }
    expect(physics.position).toBeCloseTo(1, 2);
    // no sustained oscillation: once it settles, velocity is ~0 (checked
    // via position stability in the tail of the trace)
    const tail = positions.slice(-5);
    const spread = Math.max(...tail) - Math.min(...tail);
    expect(spread).toBeLessThan(0.01);
  });

  test("rapid repeated input builds momentum (velocity increases across successive same-direction retargets)", () => {
    const clock = makeManualClock();
    const velocities = [];
    const physics = makeRailPhysics(
      (pos, vel) => velocities.push(vel),
      null,
      { requestFrame: clock.requestFrame }
    );
    for (let i = 1; i <= 5; i++) {
      physics.setTarget(i);
      clock.advance(0);
      clock.advance(90); // ~fast-repeat cadence
    }
    // velocity should be substantial by the last retarget — momentum
    // accumulated, not reset to ~0 each time (checked via H0.10's own
    // verified proof pattern: a sustained sweep builds real speed).
    expect(Math.abs(physics.velocity)).toBeGreaterThan(2);
  });

  test("no divergence at a large timestep (worst-case dt) — the substep fix", () => {
    const clock = makeManualClock();
    const physics = makeRailPhysics(() => {}, null, { requestFrame: clock.requestFrame });
    physics.setTarget(1);
    clock.advance(0);
    // 15 consecutive 50ms frames — the exact worst-case that, pre-substep
    // fix, diverged into a sustained oscillation between ~0.78 and ~1.21
    // (docs/SPATIAL_H10_PERCEPTUAL_REFINEMENT_REPORT.md §3).
    for (let i = 0; i < 15; i++) clock.advance(50);
    expect(physics.position).toBeCloseTo(1, 1);
    expect(Math.abs(physics.velocity)).toBeLessThan(0.5);
  });

  test("settle: onSettle fires exactly once, and the frame loop stops (no perpetual rAF)", () => {
    const clock = makeManualClock();
    let settleCount = 0;
    const physics = makeRailPhysics(() => {}, () => settleCount++, {
      requestFrame: clock.requestFrame,
    });
    physics.setTarget(1);
    clock.advance(0);
    for (let i = 0; i < 60; i++) clock.advance(16.7);
    expect(settleCount).toBe(1);
    expect(physics.running).toBe(false);
    // advancing further with nothing pending must not re-fire onSettle
    clock.advance(16.7);
    expect(settleCount).toBe(1);
  });

  test("jump: instant, no animation, does not call onSettle", () => {
    let settleCount = 0;
    let frameCount = 0;
    const physics = makeRailPhysics(() => frameCount++, () => settleCount++, {
      requestFrame: () => {},
    });
    physics.jump(3);
    expect(physics.position).toBe(3);
    expect(physics.velocity).toBe(0);
    expect(physics.running).toBe(false);
    expect(frameCount).toBe(1); // onFrame called once, synchronously
    expect(settleCount).toBe(0); // never treated as a "settle" event
  });
});
