export const SPATIAL_INTERACTION_EVENT = "cvln:spatial-interaction";

export const SPATIAL_INTERACTION_TYPES = Object.freeze({
  NAV_MOVE: "NAV_MOVE",
  SNAP: "SNAP",
  BLOCKED: "BLOCKED",
});

const ALLOWED = new Set(Object.values(SPATIAL_INTERACTION_TYPES));

export function isSpatialInteractionType(type) {
  return ALLOWED.has(type);
}

/**
 * Perceptual-only interaction event. It carries no progression payload and
 * never performs a business action. Sensory consumers still apply their own
 * feature-flag + explicit-user-opt-in gates before producing feedback.
 */
export function emitSpatialInteraction(type, detail = {}) {
  if (!isSpatialInteractionType(type)) return false;
  if (typeof window === "undefined" || typeof CustomEvent !== "function") return false;
  window.dispatchEvent(new CustomEvent(SPATIAL_INTERACTION_EVENT, {
    detail: { type, cadenceState: detail.cadenceState || null },
  }));
  return true;
}
