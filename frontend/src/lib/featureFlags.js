/**
 * Academy feature flags (W-FUNNEL-1).
 *
 * Uses the repository's existing CRA `REACT_APP_*` convention.
 * Spatial world rendering is now an approved production capability, so the
 * engine + environment default ON. Every flag remains explicitly overrideable
 * from the deployment environment (`true`/`1` => on, `false`/`0`/garbage => off).
 * Experimental capabilities stay opt-in.
 */

const DEFAULTS = Object.freeze({
  SPATIAL_ENGINE: true,
  SPATIAL_ROUTE_TRANSITIONS: false,
  SPATIAL_ENVIRONMENT: true,
  SPATIAL_AUDIO: false,
  SPATIAL_HAPTICS: false,
  SPATIAL_DEBUG: false,
  LIFECYCLE_RUNTIME: false,
});

function readFlag(name) {
  const raw = process.env[`REACT_APP_ACADEMY_${name}`];
  if (raw === undefined || raw === null || raw === "") {
    return DEFAULTS[name] === true;
  }
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

/** Test/story-only helper. Production code always reads through the getters. */
export function readFeatureFlag(name) {
  return readFlag(name);
}
