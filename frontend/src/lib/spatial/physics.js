/**
 * Spatial Learning — continuous, retarget-safe rail/camera physics
 * (W-FUNNEL-1, extracted from the H0.10 prototype).
 *
 * H0.10 SUBSYSTEM EXTRACTION CLASSIFICATION: REUSE.
 * The integration loop, spring constants (STIFFNESS=280, DAMPING=33,
 * ζ≈0.986) and the substep stability fix are ported verbatim from
 * `spatial-console-h10.html`'s `makeRailPhysics` — both the constants
 * and the substepping were independently verified this session's own
 * H0.10 work (see docs/SPATIAL_H10_PERCEPTUAL_REFINEMENT_REPORT.md §3):
 * a single semi-implicit-Euler step of this exact spring diverges into
 * a sustained, non-decaying oscillation whenever one frame's real dt is
 * large (a dropped/delayed frame — a real, measured risk, not a
 * hypothetical). Re-deriving these constants from scratch here would
 * discard that already-paid-for verification; changing them requires
 * re-running the same node-simulation method that caught the original
 * bug, not just "it feels fine."
 *
 * Framework-agnostic on purpose — no React import, no DOM read/write.
 * A caller (a React hook, a vanilla event handler, anything) owns
 * translating `onFrame(position, velocity)` into actual style/transform
 * writes. This mirrors H0.10's own separation (`makeRailPhysics` never
 * touched the DOM directly; `hubOnFrame`/`formationsOnFrame` did).
 *
 * DOMAIN_STATE != SPATIAL_STATE: this module has zero awareness of
 * formations, modules, or any backend-owned concept — it only ever
 * animates a scalar `position` toward a scalar `target`.
 */

// Verified-stable constants — see this file's own header comment before
// changing either value; must be re-validated with the same worst-case
// (large-dt) simulation this session used to find the original bug.
const STIFFNESS = 280;
const DAMPING = 33;
const EPS = 0.0015;

// A large frame's dt is split into fixed ~8.3ms (120Hz) sub-steps before
// integration — this is what keeps the spring stable regardless of how
// choppy real frame delivery is (see header comment).
const SUBSTEP = 1 / 120;

/**
 * Creates one independent physics instance driving a single continuous
 * scalar (a rail's "focus position," in index units, or any other
 * one-dimensional quantity a caller wants to animate this way).
 *
 * @param {(position: number, velocity: number) => void} onFrame
 *   Called every animation frame while the spring is moving, and once
 *   more on the frame it settles. Never called synchronously from
 *   `setTarget`/`jump` — always via `requestAnimationFrame`, except
 *   `jump`'s own frame (see below).
 * @param {() => void} [onSettle]
 *   Called once, the moment the spring comes to rest (`|position-
 *   target| < EPS` and `|velocity| < EPS`). Not called by `jump` (an
 *   instant jump is not a "settle" event — nothing decayed to reach it).
 * @param {{ requestFrame?: typeof requestAnimationFrame, now?: () => number }} [deps]
 *   Injectable `requestAnimationFrame`/clock, for testing in an
 *   environment (Jest/jsdom) that may not provide a real one, or to
 *   drive the loop deterministically frame-by-frame in a unit test.
 */
export function makeRailPhysics(onFrame, onSettle, deps = {}) {
  const requestFrame =
    deps.requestFrame ||
    (typeof requestAnimationFrame === "function" ? requestAnimationFrame : null);

  let position = 0;
  let velocity = 0;
  let target = 0;
  let running = false;
  let lastT = null;

  function step(t) {
    if (lastT === null) lastT = t;
    // guard against extreme stalls (tab-switch) only — the substepping
    // below is what keeps ordinary large-but-real frame gaps stable.
    const frameDt = Math.min((t - lastT) / 1000, 0.1);
    lastT = t;
    const subSteps = Math.max(1, Math.ceil(frameDt / SUBSTEP));
    const subDt = frameDt / subSteps;
    for (let i = 0; i < subSteps; i++) {
      const accel = -STIFFNESS * (position - target) - DAMPING * velocity;
      velocity += accel * subDt;
      position += velocity * subDt;
    }
    if (Math.abs(position - target) < EPS && Math.abs(velocity) < EPS) {
      position = target;
      velocity = 0;
      running = false;
      lastT = null;
      onFrame(position, velocity);
      if (onSettle) onSettle();
      return;
    }
    onFrame(position, velocity);
    if (requestFrame) requestFrame(step);
  }

  return {
    /**
     * Live-retargetable — never resets position/velocity. Calling this
     * while already in flight redirects the spring from wherever it
     * currently is, preserving velocity (this is what makes rapid
     * repeated input build momentum instead of restarting each time).
     */
    setTarget(idx) {
      target = idx;
      if (!running) {
        running = true;
        lastT = null;
        if (requestFrame) requestFrame(step);
      }
    },
    /** Instant, no animation — for reduced-motion callers. */
    jump(idx) {
      target = idx;
      position = idx;
      velocity = 0;
      running = false;
      onFrame(position, velocity);
    },
    /**
     * Advances the simulation by exactly `dtMs` milliseconds, without an
     * animation frame — for deterministic unit testing only (worst-case
     * large-dt stability, reversal traces, etc.). Not part of the
     * runtime API a real caller should use.
     */
    __stepForTest(dtMs) {
      const t = (lastT ?? 0) + dtMs;
      step(t);
    },
    get position() {
      return position;
    },
    get velocity() {
      return velocity;
    },
    get target() {
      return target;
    },
    get running() {
      return running;
    },
  };
}
