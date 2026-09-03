/**
 * Spatial Learning — haptic controller (W-FUNNEL-1, extracted from H0.10).
 *
 * H0.10 SUBSYSTEM EXTRACTION CLASSIFICATION: REUSE.
 * Same 5 named patterns, same `navigator.vibrate()`-only mechanism,
 * same feature-detection (never fake support), same gating (shared
 * opt-in with audio — H0.10's own deliberate choice, one sensory
 * opt-in, not two). No continuous vibration during drag — `SNAP` fires
 * once, at commit, never as a sustained pattern.
 */

export const HAPTIC_PATTERNS = Object.freeze({
  FOCUS_LOCK: 6,
  SNAP: 8,
  ENTER: [10, 20, 14],
  CONFIRM: 16,
  BLOCKED: [8, 30, 8],
});

/** @param {{ isEnabled?: () => boolean }} [deps] typically the SpatialAudio instance's `enabled` getter — same opt-in gate, by design */
export function createHaptics(deps = {}) {
  const isEnabled = deps.isEnabled || (() => true);
  const supported = typeof navigator !== "undefined" && typeof navigator.vibrate === "function";

  function fire(kind) {
    if (!supported || !isEnabled()) return;
    const pattern = HAPTIC_PATTERNS[kind];
    if (!pattern) return;
    try {
      navigator.vibrate(pattern);
    } catch {
      // graceful no-op — never throw for an unsupported/denied vibration call
    }
  }

  return {
    fire,
    /** Bypasses the opt-in gate — manual calibration/audition UI only. */
    audition(kind) {
      if (!supported) return;
      const pattern = HAPTIC_PATTERNS[kind];
      if (!pattern) return;
      try {
        navigator.vibrate(pattern);
      } catch {
        // graceful no-op
      }
    },
    get supported() {
      return supported;
    },
  };
}
