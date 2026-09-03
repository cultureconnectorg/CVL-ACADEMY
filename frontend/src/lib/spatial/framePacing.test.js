import { createFramePacing } from "./framePacing";

describe("framePacing.js — createFramePacing", () => {
  test("does nothing at construction time — no rAF loop starts on import/create", () => {
    let requested = false;
    const fp = createFramePacing({ requestFrame: () => (requested = true) });
    expect(requested).toBe(false);
    expect(fp.running).toBe(false);
  });

  test("start() begins the loop; stop() actually cancels it", () => {
    let cancelled = false;
    const fp = createFramePacing({
      requestFrame: () => 1,
      cancelFrame: () => (cancelled = true),
    });
    fp.start();
    expect(fp.running).toBe(true);
    fp.stop();
    expect(fp.running).toBe(false);
    expect(cancelled).toBe(true);
  });

  test("report() with no samples returns real zeros, not undefined/NaN", () => {
    const fp = createFramePacing({ requestFrame: () => 1, cancelFrame: () => {} });
    const report = fp.report();
    expect(report).toEqual({ mean: 0, p95: 0, p99: 0, dropped: 0, samples: 0 });
  });

  test("report() computes real mean/p95/p99/dropped from pushed samples", () => {
    const fp = createFramePacing({ requestFrame: () => 1, cancelFrame: () => {} });
    // simulate 10 frames at 16.7ms (60fps, no drops) then one 50ms drop
    let t = 0;
    for (let i = 0; i < 11; i++) {
      t += i === 10 ? 50 : 16.7;
      fp.__pushSampleForTest(t);
    }
    const report = fp.report();
    expect(report.samples).toBe(10); // 11 timestamps -> 10 deltas
    expect(report.dropped).toBe(1); // exactly the one >33ms delta
    expect(report.mean).toBeGreaterThan(16);
    expect(report.p99).toBeGreaterThanOrEqual(report.p95);
  });

  test("never fabricates a value — dropped-frame threshold is the real, disclosed 33ms (missed 60Hz frame)", () => {
    const fp = createFramePacing({ requestFrame: () => 1, cancelFrame: () => {} });
    fp.__pushSampleForTest(0);
    fp.__pushSampleForTest(33); // exactly at the boundary, not counted as dropped
    fp.__pushSampleForTest(33 + 33.1); // clearly over
    const report = fp.report();
    expect(report.dropped).toBe(1);
  });
});
