import { EXPERIENCE_INTENTS, LEARNING_STATES } from "@/lib/spatial/experienceState";

export const SPATIAL_SIGNAL_EVENT = "cvln:spatial-signal";

export const SPATIAL_SIGNAL_TYPES = Object.freeze({
  LEARNING_PROGRESS: "LEARNING_PROGRESS",
  PRACTICE_COMMIT: "PRACTICE_COMMIT",
  ASSESSMENT_READY: "ASSESSMENT_READY",
  ASSESSMENT_PASSED: "ASSESSMENT_PASSED",
  ASSESSMENT_RETRY: "ASSESSMENT_RETRY",
  MODULE_VALIDATED: "MODULE_VALIDATED",
  MISSION_ACCEPTED: "MISSION_ACCEPTED",
  MISSION_COMPLETED: "MISSION_COMPLETED",
});

const SIGNAL_PROFILES = Object.freeze({
  [SPATIAL_SIGNAL_TYPES.LEARNING_PROGRESS]: Object.freeze({ type: SPATIAL_SIGNAL_TYPES.LEARNING_PROGRESS, intent: EXPERIENCE_INTENTS.LEARN, learningState: LEARNING_STATES.DEEP_FOCUS, intensity: 0.14, attention: 0.97, worldBreath: 0.06, atmosphereOpacity: 0.18, ttlMs: 1200 }),
  [SPATIAL_SIGNAL_TYPES.PRACTICE_COMMIT]: Object.freeze({ type: SPATIAL_SIGNAL_TYPES.PRACTICE_COMMIT, intent: EXPERIENCE_INTENTS.PRACTICE, learningState: LEARNING_STATES.ACTION, intensity: 0.3, attention: 0.9, worldBreath: 0.18, atmosphereOpacity: 0.28, ttlMs: 1600 }),
  [SPATIAL_SIGNAL_TYPES.ASSESSMENT_READY]: Object.freeze({ type: SPATIAL_SIGNAL_TYPES.ASSESSMENT_READY, intent: EXPERIENCE_INTENTS.PROVE, learningState: LEARNING_STATES.DEEP_FOCUS, intensity: 0.12, attention: 0.98, worldBreath: 0.04, atmosphereOpacity: 0.16, ttlMs: 2000 }),
  [SPATIAL_SIGNAL_TYPES.ASSESSMENT_PASSED]: Object.freeze({ type: SPATIAL_SIGNAL_TYPES.ASSESSMENT_PASSED, intent: EXPERIENCE_INTENTS.PROVE, learningState: LEARNING_STATES.ACHIEVEMENT, intensity: 0.62, attention: 0.9, worldBreath: 0.54, atmosphereOpacity: 0.5, ttlMs: 2200 }),
  [SPATIAL_SIGNAL_TYPES.ASSESSMENT_RETRY]: Object.freeze({ type: SPATIAL_SIGNAL_TYPES.ASSESSMENT_RETRY, intent: EXPERIENCE_INTENTS.LEARN, learningState: LEARNING_STATES.DEEP_FOCUS, intensity: 0.1, attention: 0.99, worldBreath: 0.03, atmosphereOpacity: 0.14, ttlMs: 1800 }),
  [SPATIAL_SIGNAL_TYPES.MODULE_VALIDATED]: Object.freeze({ type: SPATIAL_SIGNAL_TYPES.MODULE_VALIDATED, intent: EXPERIENCE_INTENTS.PROVE, learningState: LEARNING_STATES.ACHIEVEMENT, intensity: 0.72, attention: 0.92, worldBreath: 0.62, atmosphereOpacity: 0.56, ttlMs: 2600 }),
  [SPATIAL_SIGNAL_TYPES.MISSION_ACCEPTED]: Object.freeze({ type: SPATIAL_SIGNAL_TYPES.MISSION_ACCEPTED, intent: EXPERIENCE_INTENTS.PRACTICE, learningState: LEARNING_STATES.ACTION, intensity: 0.52, attention: 0.82, worldBreath: 0.32, atmosphereOpacity: 0.38, ttlMs: 1800 }),
  [SPATIAL_SIGNAL_TYPES.MISSION_COMPLETED]: Object.freeze({ type: SPATIAL_SIGNAL_TYPES.MISSION_COMPLETED, intent: EXPERIENCE_INTENTS.PROVE, learningState: LEARNING_STATES.ACHIEVEMENT, intensity: 0.68, attention: 0.9, worldBreath: 0.58, atmosphereOpacity: 0.54, ttlMs: 2400 }),
});

export function spatialSignalProfile(type) {
  return SIGNAL_PROFILES[type] || null;
}

function normalizeUrl(url = "") {
  return String(url).split("?")[0].replace(/^https?:\/\/[^/]+\/api/, "").replace(/^\/api/, "");
}

export function signalForApiResponse(response) {
  const method = String(response?.config?.method || "get").toLowerCase();
  const url = normalizeUrl(response?.config?.url);
  const data = response?.data || {};

  if (method === "post" && /^\/modules\/[^/]+\/[^/]+\/phase$/.test(url)) return spatialSignalProfile(SPATIAL_SIGNAL_TYPES.LEARNING_PROGRESS);
  if (method === "post" && /^\/modules\/[^/]+\/[^/]+\/deliverable$/.test(url)) return spatialSignalProfile(SPATIAL_SIGNAL_TYPES.PRACTICE_COMMIT);
  if (method === "get" && /^\/formations\/[^/]+\/modules\/[^/]+\/quiz$/.test(url)) return spatialSignalProfile(SPATIAL_SIGNAL_TYPES.ASSESSMENT_READY);
  if (method === "post" && /^\/formations\/[^/]+\/modules\/[^/]+\/quiz\/submit$/.test(url)) {
    return spatialSignalProfile(data?.passed === true ? SPATIAL_SIGNAL_TYPES.ASSESSMENT_PASSED : SPATIAL_SIGNAL_TYPES.ASSESSMENT_RETRY);
  }
  if (method === "post" && /^\/modules\/[^/]+\/[^/]+\/mini-mission\/commit$/.test(url)) return spatialSignalProfile(SPATIAL_SIGNAL_TYPES.MODULE_VALIDATED);
  if (method === "post" && /^\/missions\/[^/]+\/accept$/.test(url)) return spatialSignalProfile(SPATIAL_SIGNAL_TYPES.MISSION_ACCEPTED);
  if (method === "post" && /^\/missions\/[^/]+\/submit$/.test(url)) return spatialSignalProfile(SPATIAL_SIGNAL_TYPES.MISSION_COMPLETED);
  return null;
}

/**
 * Non-blocking bridge from successful backend-owned domain events to Spatial.
 * It never changes progression state and never throws into the API path.
 */
export function emitSpatialSignalFromResponse(response) {
  try {
    const signal = signalForApiResponse(response);
    if (!signal || typeof window === "undefined" || typeof CustomEvent === "undefined") return null;
    window.dispatchEvent(new CustomEvent(SPATIAL_SIGNAL_EVENT, { detail: { type: signal.type } }));
    return signal;
  } catch (_error) {
    return null;
  }
}
