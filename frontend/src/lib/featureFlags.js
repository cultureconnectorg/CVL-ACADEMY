/**
 * Academy feature flags (W-FUNNEL-1).
 *
 * Uses the repository's existing configuration mechanism — CRA's own
 * `REACT_APP_*` env-var convention (the only mechanism already in use,
 * `frontend/src/lib/api.js`'s `REACT_APP_BACKEND_URL`), never a
 * parallel config framework.
 *
 * Every flag here changes real user-visible experience once consumed —
 * every one of them DEFAULTS TO FALSE. `frontend/.env.example`
 * documents each, commented out, so a fresh clone/deploy is exactly
 * today's production behavior until a flag is deliberately set.
 */

function readFlag(name) {
  const raw = process.env[`REACT_APP_ACADEMY_${name}`];
  return raw === "true" || raw === "1";
}

export const FEATURE_FLAGS = Object.freeze({
  get SPATIAL_ENGINE() {
    return readFlag("SPATIAL_ENGINE");
  },
  get SPATIAL_ROUTE_TRANSITIONS() {
    return readFlag("SPATIAL_ROUTE_TRANSITIONS");
  },
  get SPATIAL_ENVIRONMENT() {
    return readFlag("SPATIAL_ENVIRONMENT");
  },
  get SPATIAL_AUDIO() {
    return readFlag("SPATIAL_AUDIO");
  },
  get SPATIAL_HAPTICS() {
    return readFlag("SPATIAL_HAPTICS");
  },
  get SPATIAL_DEBUG() {
    return readFlag("SPATIAL_DEBUG");
  },
  get LIFECYCLE_RUNTIME() {
    return readFlag("LIFECYCLE_RUNTIME");
  },
});

/** Test/story-only override — never used by production code, which
 * always reads `process.env` directly via the getters above (so a
 * runtime env change, e.g. between CI environments, is always honored,
 * never cached at import time). */
export function readFeatureFlag(name) {
  return readFlag(name);
}
