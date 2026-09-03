/**
 * Spatial Learning — input cadence classifier (W-FUNNEL-1, extracted
 * from H0.10).
 *
 * H0.10 SUBSYSTEM EXTRACTION CLASSIFICATION: REUSE.
 * Already framework-agnostic pure JS in the prototype — ported near
 * verbatim, only the injectable clock is new (test-determinism, same
 * reason `physics.js` accepts an injectable `now`).
 *
 * Classifies real input timestamps into SINGLE / REPEATED / FAST_REPEAT
 * / REVERSAL / STOPPED — used to defer non-essential detail resolution
 * during rapid navigation without ever delaying the navigation itself
 * (the spatial/camera response stays driven by physics.js regardless of
 * cadence; only secondary detail/announcement timing reads this).
 */

const FAST_REPEAT_WINDOW_MS = 260;
const FAST_REPEAT_STREAK_THRESHOLD = 3;
const STOPPED_DELAY_MS = 260;

export const CADENCE_STATES = Object.freeze({
  SINGLE: "SINGLE",
  REPEATED: "REPEATED",
  FAST_REPEAT: "FAST_REPEAT",
  REVERSAL: "REVERSAL",
  STOPPED: "STOPPED",
});

/**
 * @param {{ now?: () => number, setTimeout?: typeof setTimeout, clearTimeout?: typeof clearTimeout }} [deps]
 */
export function createCadenceTracker(deps = {}) {
  const now = deps.now || (() => (typeof performance !== "undefined" ? performance.now() : Date.now()));
  const scheduleTimeout = deps.setTimeout || setTimeout;
  const cancelTimeout = deps.clearTimeout || clearTimeout;

  const state = {
    // `null` (not 0) marks "no prior input yet" — a plain falsy check
    // (`state.lastTime ? ... : Infinity`) breaks if the very first real
    // timestamp is legitimately 0, which a real `performance.now()`
    // never is in practice but an injectable test clock can easily be.
    lastTime: null,
    lastDir: 0,
    streak: 0,
    state: CADENCE_STATES.STOPPED,
  };
  let stopTimer = null;

  function armStopTimer(onStop) {
    if (stopTimer) cancelTimeout(stopTimer);
    stopTimer = scheduleTimeout(() => {
      state.state = CADENCE_STATES.STOPPED;
      state.streak = 0;
      if (onStop) onStop(state.state);
    }, STOPPED_DELAY_MS);
  }

  return {
    /** @param {1|-1} dir @param {() => void} [onChange] fired after every classification, including the delayed STOPPED transition */
    trackInput(dir, onChange) {
      const t = now();
      const interval = state.lastTime === null ? Infinity : t - state.lastTime;
      if (interval < FAST_REPEAT_WINDOW_MS) {
        if (dir !== state.lastDir && state.lastDir !== 0) {
          state.state = CADENCE_STATES.REVERSAL;
          state.streak = 1;
        } else {
          state.streak += 1;
          state.state =
            state.streak >= FAST_REPEAT_STREAK_THRESHOLD
              ? CADENCE_STATES.FAST_REPEAT
              : CADENCE_STATES.REPEATED;
        }
      } else {
        state.streak = 1;
        state.state = CADENCE_STATES.SINGLE;
      }
      state.lastTime = t;
      state.lastDir = dir;
      armStopTimer(onChange);
      if (onChange) onChange(state.state);
      return state.state;
    },
    /** Detail/announcement dwell should stretch during FAST_REPEAT so rapid
     * traversal never machine-guns text/announcements — the spatial
     * response itself never reads this. */
    dwellDelay(baseMs) {
      return state.state === CADENCE_STATES.FAST_REPEAT ? baseMs * 2.2 : baseMs;
    },
    get state() {
      return state.state;
    },
    get streak() {
      return state.streak;
    },
    get lastDir() {
      return state.lastDir;
    },
    dispose() {
      if (stopTimer) cancelTimeout(stopTimer);
    },
  };
}
