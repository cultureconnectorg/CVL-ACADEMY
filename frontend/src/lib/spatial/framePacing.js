/**
 * Spatial Learning — frame pacing diagnostic sampler (W-FUNNEL-1,
 * extracted from H0.10).
 *
 * H0.10 SUBSYSTEM EXTRACTION CLASSIFICATION: REWRITE_SMALL.
 * H0.10's `FramePacing` started its `requestAnimationFrame` loop as a
 * module-load side effect (an IIFE calling `requestAnimationFrame(tick)`
 * immediately) — fine for a standalone prototype HTML file, a real bug
 * risk in a React app: every test file or SSR pass that merely imports
 * this module would otherwise start an uncontrolled rAF loop. This
 * version keeps the exact same sampling/percentile math (unchanged) but
 * requires an explicit `start()` call, and `stop()` actually cancels
 * the loop (H0.10 had no stop path at all, by design, since the
 * prototype never needed one).
 *
 * Debug-only, per mission §14 — never part of normal user-facing UI,
 * `SPATIAL_DEBUG` feature-flagged.
 */

const MAX_SAMPLES = 240; // ~4s at 60fps

export function createFramePacing(deps = {}) {
  const requestFrame =
    deps.requestFrame ||
    (typeof requestAnimationFrame === "function" ? requestAnimationFrame : null);
  const cancelFrame =
    deps.cancelFrame || (typeof cancelAnimationFrame === "function" ? cancelAnimationFrame : null);

  let samples = [];
  let lastT = null;
  let rafId = null;
  let running = false;

  function tick(t) {
    if (lastT !== null) {
      const d = t - lastT;
      samples.push(d);
      if (samples.length > MAX_SAMPLES) samples.shift();
    }
    lastT = t;
    if (running && requestFrame) rafId = requestFrame(tick);
  }

  function percentile(arr, p) {
    if (!arr.length) return 0;
    const sorted = [...arr].sort((a, b) => a - b);
    const idx = Math.min(sorted.length - 1, Math.floor(p * sorted.length));
    return sorted[idx];
  }

  return {
    start() {
      if (running || !requestFrame) return;
      running = true;
      lastT = null;
      rafId = requestFrame(tick);
    },
    stop() {
      running = false;
      if (rafId != null && cancelFrame) cancelFrame(rafId);
      rafId = null;
    },
    get running() {
      return running;
    },
    /** Real, measured, never fabricated — see docs/SPATIAL_H09_FULL_
     * SPATIAL_FEEL_REPORT.md and SPATIAL_H10_PERCEPTUAL_REFINEMENT_
     * REPORT.md §10 for how this exact mechanism was interpreted
     * (diagnostic-only, sandbox-caveated) once real numbers came back. */
    report() {
      if (!samples.length) return { mean: 0, p95: 0, p99: 0, dropped: 0, samples: 0 };
      const mean = samples.reduce((a, b) => a + b, 0) / samples.length;
      const dropped = samples.filter((s) => s > 33).length; // missed a 60Hz frame
      return {
        mean: Number(mean.toFixed(2)),
        p95: Number(percentile(samples, 0.95).toFixed(2)),
        p99: Number(percentile(samples, 0.99).toFixed(2)),
        dropped,
        samples: samples.length,
      };
    },
    /** Test-only: feed synthetic frame timestamps without a real rAF loop. */
    __pushSampleForTest(t) {
      tick(t);
    },
  };
}
