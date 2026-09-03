/**
 * Spatial Learning — spatial audio controller (W-FUNNEL-1, extracted
 * from H0.10).
 *
 * H0.10 SUBSYSTEM EXTRACTION CLASSIFICATION: REUSE.
 * Same 8 named events, same envelope-shaped Web Audio oscillator
 * synthesis (no external files, nothing that could resemble a licensed
 * sound), same NAV_MOVE throttle (40ms / 90ms during FAST_REPEAT), same
 * muted-by-default / explicit-opt-in-only gate. Wrapped as a factory
 * (`createSpatialAudio`) instead of a module-level singleton IIFE so
 * multiple instances can exist in tests without sharing state, and so
 * nothing runs at import time (an H0.10 prototype convenience that
 * would be a real problem in a server-rendered or test environment).
 *
 * Per mission §12: not wired into any real product surface this wave —
 * infrastructure only, `SPATIAL_AUDIO` feature-flagged, default off.
 */

export const AUDIO_EVENTS = Object.freeze([
  "NAV_MOVE",
  "FOCUS_LOCK",
  "ENTER_DEPTH",
  "RETURN_DEPTH",
  "CONTEXT_OPEN",
  "CONTEXT_CLOSE",
  "CONFIRM",
  "BLOCKED",
]);

/** @param {{ getCadenceState?: () => string }} [deps] optional live cadence read, for the NAV_MOVE throttle's FAST_REPEAT case */
export function createSpatialAudio(deps = {}) {
  const getCadenceState = deps.getCadenceState || (() => "STOPPED");
  let ctx = null;
  let enabled = false;
  let lastNavPlay = 0;

  function getCtx() {
    if (ctx) return ctx;
    const AC =
      typeof window !== "undefined" && (window.AudioContext || window.webkitAudioContext);
    if (!AC) return null; // unsupported environment — graceful no-op, never fake support
    try {
      ctx = new AC();
    } catch {
      ctx = null;
    }
    return ctx;
  }

  function tone(freq, durMs, opts = {}) {
    const c = getCtx();
    if (!c) return;
    if (c.state === "suspended") c.resume();
    const t0 = c.currentTime;
    const osc = c.createOscillator();
    const gain = c.createGain();
    osc.type = opts.type || "sine";
    osc.frequency.setValueAtTime(freq, t0);
    if (opts.glideTo) osc.frequency.linearRampToValueAtTime(opts.glideTo, t0 + durMs / 1000);
    const peak = opts.volume || 0.05;
    gain.gain.setValueAtTime(0, t0);
    gain.gain.linearRampToValueAtTime(peak, t0 + 0.006);
    gain.gain.exponentialRampToValueAtTime(0.0001, t0 + durMs / 1000);
    osc.connect(gain);
    gain.connect(c.destination);
    osc.start(t0);
    osc.stop(t0 + durMs / 1000 + 0.02);
  }

  const EVENT_FNS = {
    NAV_MOVE: () => tone(720, 18, { volume: 0.028 }),
    FOCUS_LOCK: () => tone(560, 55, { volume: 0.045 }),
    ENTER_DEPTH: () => tone(340, 190, { type: "triangle", glideTo: 210, volume: 0.06 }),
    RETURN_DEPTH: () => tone(220, 170, { type: "triangle", glideTo: 360, volume: 0.055 }),
    CONTEXT_OPEN: () => tone(480, 90, { volume: 0.045 }),
    CONTEXT_CLOSE: () => tone(380, 80, { volume: 0.04 }),
    CONFIRM: () => {
      tone(520, 70, { volume: 0.05 });
      setTimeout(() => tone(780, 110, { volume: 0.05 }), 60);
    },
    BLOCKED: () => tone(160, 90, { type: "square", volume: 0.035 }),
  };

  function play(kind) {
    if (!enabled) return;
    if (kind === "NAV_MOVE") {
      const now = typeof performance !== "undefined" ? performance.now() : Date.now();
      const throttleMs = getCadenceState() === "FAST_REPEAT" ? 90 : 40;
      if (now - lastNavPlay < throttleMs) return; // rapid-repeat throttle — never machine-guns
      lastNavPlay = now;
    }
    const fn = EVENT_FNS[kind];
    if (fn) fn();
  }

  return {
    play,
    /** Bypasses the `enabled` gate and NAV_MOVE throttle — deliberate,
     * for a manual calibration/audition UI only (H0.10 §8). */
    audition(kind) {
      getCtx();
      const fn = EVENT_FNS[kind];
      if (fn) fn();
    },
    setEnabled(v) {
      enabled = Boolean(v);
      if (enabled) getCtx();
    },
    get enabled() {
      return enabled;
    },
    get supported() {
      return Boolean(
        typeof window !== "undefined" && (window.AudioContext || window.webkitAudioContext)
      );
    },
  };
}
