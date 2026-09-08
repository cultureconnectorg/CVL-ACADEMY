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
  /** RAIL 3 ("Finir Spatial Learning", 2026-09-07) — gates whether
   * Dashboard/Roadmap render their attention-tier layout driven by the
   * real pedagogical graph (`lib/pedagogicalGraph.js`) instead of
   * today's static bento grid / index-based stage rail. Off by default,
   * same discipline as every other flag here: a fresh deploy is exactly
   * today's production behavior until deliberately turned on. */
  get SPATIAL_HUB_ENABLED() {
    return readFlag("SPATIAL_HUB_ENABLED");
  },
  /** RAIL 4 ("continue les H", 2026-09-07) — gates whether activating a
   * SpatialHub node plays a real camera-intent flight (INTENT->LOCKING->
   * FOLLOWING, `lib/spatial/cameraFollow.js`, ported from H0.8) before
   * navigating, instead of navigating instantly. Same-page scope only —
   * the full cross-route REVEALING handoff stays NOT_AUTHORIZED (see
   * cameraFollow.js's own docstring). Off by default. */
  get SPATIAL_CAMERA_INTENT() {
    return readFlag("SPATIAL_CAMERA_INTENT");
  },
  /** RAIL 5 (2026-09-07) — correcting a wrong assumption from Rail 3's
   * own SpatialHub docstring, which claimed CONTEXT_OPEN/CONTEXT_CLOSE/
   * ENTER_DEPTH/RETURN_DEPTH "belong to route-level transitions" — they
   * don't: `lib/ContextFrame.jsx` (W3-B) is a same-page dock system,
   * never a route change. This flag gates: (a) ModuleJourney's phase
   * hierarchy (`JourneyHierarchy.jsx`) rendering through the real
   * physics/attention engine instead of a static 4-bucket variant
   * table, and (b) ContextFrame/quiz-submit/mini-mission-commit firing
   * real CONTEXT_OPEN/CONTEXT_CLOSE/CONFIRM audio+haptics. Off by
   * default. See docs/ACADEMY_RAIL5_MODULE_JOURNEY_ENGINE_REPORT.md. */
  get SPATIAL_MODULE_DEPTH() {
    return readFlag("SPATIAL_MODULE_DEPTH");
  },
  /** ACA-0010 ("Hero/Entry — world entry, not SaaS landing",
   * `docs/ACADEMY_HERO_ENTRY_RESEARCH.md`) — gates whether Landing's
   * manifesto and auth card appear as a sequenced VOID→WORLD→FOCUS→
   * IDENTITY entry (world established before identity competes for
   * primary visual weight) instead of rendering simultaneously at full
   * weight, as today. Off by default — an unauthenticated visitor sees
   * exactly today's Landing until this is deliberately turned on. */
  get SPATIAL_HERO_ENTRY() {
    return readFlag("SPATIAL_HERO_ENTRY");
  },
  /** ACA-0011 ("Identity/FREK-ID entry as contextual transition") —
   * gates whether a successful registration's new FREK-ID is
   * acknowledged as a real, in-context identity event (a `Confirm`
   * reveal inside the auth card — "a real action visibly changing what
   * the world says back," `ACADEMY_HERO_ENTRY_RESEARCH.md`'s NFS/
   * Autolog lesson) before advancing to onboarding, instead of a
   * fire-and-forget toast + instant redirect, as today. Off by
   * default — registration behaves exactly as before until this is
   * deliberately turned on. */
  get SPATIAL_IDENTITY_ENTRY() {
    return readFlag("SPATIAL_IDENTITY_ENTRY");
  },
});

/** Test/story-only override — never used by production code, which
 * always reads `process.env` directly via the getters above (so a
 * runtime env change, e.g. between CI environments, is always honored,
 * never cached at import time). */
export function readFeatureFlag(name) {
  return readFlag(name);
}
