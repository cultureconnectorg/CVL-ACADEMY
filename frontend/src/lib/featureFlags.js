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
  // Real WebGL world (docs/ADR_W5_WEBGL_REOPENED.md, Founder-authorized).
  // Defaults ON like SPATIAL_ENGINE/SPATIAL_ENVIRONMENT; LITE-tier devices
  // and no-WebGL browsers still fall back to the CSS world automatically
  // (SpatialWorldFrame.jsx), independent of this flag.
  SPATIAL_WEBGL: true,
  SPATIAL_AUDIO: false,
  SPATIAL_HAPTICS: false,
  SPATIAL_DEBUG: false,
  LIFECYCLE_RUNTIME: false,
  SPATIAL_HUB_ENABLED: false,
  SPATIAL_CAMERA_INTENT: false,
  SPATIAL_MODULE_DEPTH: false,
  SPATIAL_HERO_ENTRY: false,
  SPATIAL_IDENTITY_ENTRY: false,
  SPATIAL_ONBOARDING_ENTRY: false,
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
  get SPATIAL_WEBGL() {
    return readFlag("SPATIAL_WEBGL");
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
   * today's production behavior until deliberately turned on.
   *
   * ACA-0014/ACA-0017 (H1 sequencing step 4, `SPATIAL_H1_INTEGRATION_
   * PLAN.md`) reuses this same flag for Badges' continuous-depth
   * treatment (`pages/Badges.js`) — same attention/physics engine,
   * same "no forced primary when there's no real target" edge case,
   * intentionally not a second flag for what is the same production
   * gate as Dashboard/Roadmap. */
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
  /** ACA-0012 ("Onboarding spatialization") — gates whether
   * Onboarding's step-to-step transitions use the real `Enter`
   * primitive (continuous crossfade, `CONTINUITY_OVER_PAGE_CUT`)
   * instead of the plain CSS `.fade-in` class, and whether the
   * learner's own real métier choice (`options.metiers[].color`,
   * already real backend data) tints the progress bar and step
   * backdrop from that point on — "a real choice visibly changes what
   * the world looks like," never a fabricated per-territoire/objectif
   * visual (the mission explicitly warns against inventing
   * personalization there — see docs/ACADEMY_ACA0012_ONBOARDING_
   * SPATIALIZATION_REPORT.md). Off by default. */
  get SPATIAL_ONBOARDING_ENTRY() {
    return readFlag("SPATIAL_ONBOARDING_ENTRY");
  },
});

/** Test/story-only helper. Production code always reads through the getters. */
export function readFeatureFlag(name) {
  return readFlag(name);
}
