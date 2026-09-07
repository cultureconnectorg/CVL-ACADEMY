/**
 * ACA-0023 (scroll slice) — Exact return-to-position, scroll axis.
 *
 * Pure, framework-free position store keyed by React Router's
 * `location.key` (a unique id per history entry, not per pathname — two
 * visits to the same route get independent scroll memories, matching
 * what a real browser back/forward stack does). Kept separate from the
 * hook that drives it (`useScrollRestoration.js`) so the storage logic
 * is unit-testable without mounting a router or touching `window`.
 *
 * In-memory only, deliberately: a hard refresh starting at the top of
 * the page is the correct, expected default — this only restores
 * position across *client-side* back/forward navigation within the
 * same SPA session, never across a reload.
 */

const MAX_ENTRIES = 50;

const positions = new Map();

export function savePosition(key, y) {
  if (!key) return;
  // Re-inserting moves the key to the end of Map's iteration order,
  // giving cheap LRU eviction below without a second data structure.
  positions.delete(key);
  positions.set(key, y);
  if (positions.size > MAX_ENTRIES) {
    const oldestKey = positions.keys().next().value;
    positions.delete(oldestKey);
  }
}

export function getPosition(key) {
  return positions.get(key);
}

export function clearPositions() {
  positions.clear();
}
