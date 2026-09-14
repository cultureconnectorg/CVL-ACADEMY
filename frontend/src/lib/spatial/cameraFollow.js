/**
 * Spatial Learning — camera-follow transition primitives (Rail 4,
 * 2026-09-07, extracted from the H0.8/H0.10 prototype artifact —
 * `spatial-console-h10.html`, `cameraFollowTransition`/
 * `cameraReturnTransition`/the CAMERA TRANSITION STATE MACHINE).
 *
 * H0.10 SUBSYSTEM EXTRACTION CLASSIFICATION: REUSE.
 * The state names, the token-based retarget/cancel guard, and the
 * flight math (origin-percentage, dx/dy/scale) are ported verbatim from
 * the artifact's own `cameraFollowTransition()`/`cameraReturnTransition()`
 * — not re-derived. Only the DOM creation/animation calls themselves
 * stay out of this file (framework-agnostic on purpose, same separation
 * as `physics.js`): a caller supplies the real `getBoundingClientRect()`
 * rects and owns the actual clone/`Element.animate()` calls.
 *
 * SCOPE, DISCLOSED HONESTLY: the prototype's full state machine assumes
 * a single-document SPA where `goto()` just toggles sibling `.view`
 * sections already present in the DOM — so the REVEALING phase can
 * synchronously resolve a real destination anchor element the instant
 * `requestAnimationFrame` fires after `goto()`. The real app uses React
 * Router: a route change unmounts/remounts pages, and destination pages
 * (Dashboard/Roadmap/...) fetch their own data on mount before
 * rendering the real anchor element — so a same-frame REVEALING handoff
 * to a cross-route anchor was not safely reproducible without either (a)
 * promoting Layout to an Outlet-based layout route or (b) a real
 * mount-detection race guard.
 *
 * **ACA-0015 update (2026-09-08)**: both are now real. (a) is the
 * Layout→Outlet restructure (ACA-0015/ACA-0016's routing work); (b) is
 * `lib/spatial/mountGuard.js`'s `waitForElement`. `useCameraIntent.js`'s
 * `fly()` now completes the full INTENT → LOCKING → FOLLOWING →
 * CROSSING → REVEALING → SETTLING sequence for the two real production
 * call sites `components/SpatialHub.jsx` wires (formation and mission
 * activation) — verified against a real Chromium instance (mocked auth,
 * real navigation, real destination anchors), not just unit-tested math;
 * see `docs/ACADEMY_ACA0015_CAMERA_REVEALING_REPORT.md`. `RETURNING`,
 * the full `makeAnchorContract` destination fields, and
 * `cameraReturnTransition`'s reverse-anchor resolution remain
 * NOT_AUTHORIZED for production use — extracted here, faithfully, not
 * wired now.
 */

export const CAMERA_STATES = Object.freeze({
  IDLE: "IDLE",
  INTENT: "INTENT",
  LOCKING: "LOCKING",
  FOLLOWING: "FOLLOWING",
  CROSSING: "CROSSING",
  REVEALING: "REVEALING",
  SETTLING: "SETTLING",
  RETURNING: "RETURNING",
  // CANCELLED is implicit, per the prototype's own comment: a stale
  // token never gets its own named state, the in-flight step just no-ops.
});

/** Clamp a percentage into [0, 100] — same guard the prototype's own
 * `clampPct` uses before ever writing a `perspective-origin` value. */
export function clampPct(n) {
  return Math.max(0, Math.min(100, n));
}

/**
 * Where, as a percentage of `containerRect`, an element's own center
 * sits — the exact math `cameraFollowTransition` uses twice (once for
 * the source anchor, once for the destination) to drive
 * `stage.style.perspectiveOrigin`.
 */
export function computeOriginPct(rect, containerRect) {
  if (!containerRect.width) return 50;
  return clampPct(((rect.left + rect.width / 2 - containerRect.left) / containerRect.width) * 100);
}

/**
 * The clone-flight keyframe math: how far and at what final scale a
 * cloned anchor must travel to land exactly on a destination rect —
 * ported verbatim (`dx`/`dy`/`scale` in the prototype's REVEALING
 * phase).
 */
export function computeFlightKeyframes(fromRect, toRect) {
  return {
    dx: toRect.left - fromRect.left,
    dy: toRect.top - fromRect.top,
    scale: fromRect.width > 0 ? toRect.width / fromRect.width : 1,
  };
}

/**
 * The retarget/cancel guard — LATEST_USER_INTENT_WINS, never queued.
 * Mirrors the prototype's own `cameraToken`/`myToken` pattern as a
 * small reusable primitive: `next()` supersedes anything in flight,
 * `isCurrent(token)` is what every async step checks before continuing.
 */
export function createCameraToken() {
  let current = 0;
  return {
    next() {
      current += 1;
      return current;
    },
    isCurrent(token) {
      return token === current;
    },
  };
}
