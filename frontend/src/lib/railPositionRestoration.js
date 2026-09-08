/**
 * ACA-0023 (camera/rail/focus slice) — Exact return-to-position, the
 * axis explicitly deferred by `useScrollRestoration.js`'s own scope
 * note: "The camera/rail/focus axes are a real, separate decision tied
 * to whether the spatial engine is actually mounted in production
 * (ACA-0014, still flag-gated off)." ACA-0014/H1 mounted it
 * (`SpatialHub.jsx`, `SPATIAL_HUB_ENABLED`); this closes the axis.
 *
 * Pure, framework-free position store keyed by React Router's
 * `location.key` (same convention `scrollRestoration.js` already
 * established — one entry per history entry, not per pathname), kept
 * separate from the hook/component that drives it for the same
 * unit-testability reason. Stores which real rail item had focus (its
 * own stable `key`, e.g. `"formation:FMS-01"`) and the rail's own
 * horizontal `scrollLeft` — the two things a POP navigation back to
 * Dashboard needs to restore, neither of which the browser's own
 * scroll restoration (vertical page scroll only) ever touches.
 *
 * In-memory only, deliberately — same "hard refresh starts fresh"
 * doctrine `scrollRestoration.js` already states: this only restores
 * across client-side back/forward within the same SPA session.
 */

const MAX_ENTRIES = 50;

const positions = new Map();

/**
 * @param {string} key location.key
 * @param {{ focusedKey: string, scrollLeft: number }} state
 */
export function saveRailPosition(key, state) {
  if (!key) return;
  positions.delete(key);
  positions.set(key, state);
  if (positions.size > MAX_ENTRIES) {
    const oldestKey = positions.keys().next().value;
    positions.delete(oldestKey);
  }
}

export function getRailPosition(key) {
  return positions.get(key);
}

export function clearRailPositions() {
  positions.clear();
}
