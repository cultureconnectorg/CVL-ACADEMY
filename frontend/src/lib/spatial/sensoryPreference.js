export const SPATIAL_SENSORY_STORAGE_KEY = "cvln:spatial-sensory-opt-in:v1";
export const SPATIAL_SENSORY_PREFERENCE_EVENT = "cvln:spatial-sensory-preference";

export function readSpatialSensoryOptIn(storage = globalThis?.localStorage) {
  try {
    return storage?.getItem?.(SPATIAL_SENSORY_STORAGE_KEY) === "true";
  } catch {
    return false;
  }
}

export function writeSpatialSensoryOptIn(enabled, storage = globalThis?.localStorage) {
  const value = Boolean(enabled);
  try {
    storage?.setItem?.(SPATIAL_SENSORY_STORAGE_KEY, value ? "true" : "false");
  } catch {
    // Preference persistence is progressive enhancement; never block UX.
  }
  if (typeof window !== "undefined" && typeof CustomEvent === "function") {
    window.dispatchEvent(new CustomEvent(SPATIAL_SENSORY_PREFERENCE_EVENT, { detail: { enabled: value } }));
  }
  return value;
}
