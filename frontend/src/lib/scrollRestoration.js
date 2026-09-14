/**
 * ACA-0023 — Exact return-to-position memory.
 *
 * Pure, framework-free stores keyed by React Router's `location.key`
 * (a unique id per history entry, not per pathname). Document scroll,
 * named spatial rails and focus therefore return to the exact history
 * entry instead of leaking state between two visits to the same route.
 *
 * In-memory only, deliberately: a hard refresh starts from a fresh
 * document. This memory exists only for client-side back/forward within
 * the same Academy session.
 */

const MAX_ENTRIES = 50;

const positions = new Map();
const focusTargets = new Map();
const elementPositions = new Map();

function setBounded(map, key, value) {
  if (!key) return;
  map.delete(key);
  map.set(key, value);
  if (map.size > MAX_ENTRIES) {
    const oldestKey = map.keys().next().value;
    map.delete(oldestKey);
  }
}

export function savePosition(key, y) {
  setBounded(positions, key, y);
}

export function getPosition(key) {
  return positions.get(key);
}

export function saveFocusTarget(key, target) {
  if (!target || !target.kind || !target.value) return;
  setBounded(focusTargets, key, target);
}

export function getFocusTarget(key) {
  return focusTargets.get(key);
}

export function saveElementPosition(key, memoryKey, position) {
  if (!key || !memoryKey || !position) return;
  const existing = elementPositions.get(key) || {};
  setBounded(elementPositions, key, {
    ...existing,
    [memoryKey]: { left: position.left || 0, top: position.top || 0 },
  });
}

export function getElementPositions(key) {
  return elementPositions.get(key) || {};
}

export function clearPositions() {
  positions.clear();
  elementPositions.clear();
}

export function clearFocusTargets() {
  focusTargets.clear();
}
