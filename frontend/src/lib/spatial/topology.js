/**
 * Spatial Learning — Academy transition topology (W-FUNNEL-1).
 *
 * H0.10 SUBSYSTEM EXTRACTION CLASSIFICATION: REWRITE_SMALL.
 * H0.10's `TRANSITION_TOPOLOGY` was a flat `"from|to": "lateral"/
 * "deeper"/"shallower"` lookup over 7 prototype routes, driving one
 * thing (a `--topo-depth` scale nudge). Per docs/ACADEMY_SPATIAL_END_
 * TO_END_ARCHITECTURE.md §4 and the mission's own §7, production needs
 * a richer per-edge shape (direction/depth/intent/return-intent/shared-
 * object policy/environment-continuity policy) over the *lifecycle*
 * node set (mission §7's list — including nodes with no real route,
 * e.g. ACTIVATION), not just the 7 prototype routes. The concept
 * (declared edges, direction/depth per pair, never arbitrary) is
 * unchanged; the data shape and node set are new.
 *
 * A topology node MAY represent a lifecycle state rather than an actual
 * URL (mission §7) — `route: null` marks that case explicitly rather
 * than inventing one.
 *
 * This module is pure data + pure lookup functions — no React, no DOM,
 * no coupling to `frontend/src/App.js`'s actual route strings beyond
 * what's declared here (kept in sync manually; a stale mapping fails
 * safe — see `resolveEdge`).
 */

/** One node per mission §7 concept. `route: null` = lifecycle state,
 * not a real URL (ACTIVATION, EXPANSION, ECOSYSTEM today). */
export const TOPOLOGY_NODES = Object.freeze({
  LANDING: { route: "/" },
  SIGNUP: { route: "/" }, // same route as LANDING today (inline mode switch) — see ACADEMY_CURRENT_FUNNEL_AUDIT.md stage 02
  ONBOARDING: { route: "/onboarding" },
  ACTIVATION: { route: null }, // no dedicated route today — the onboarding_complete response payload, not a URL
  DASHBOARD: { route: "/dashboard" },
  FORMATIONS: { route: "/formations" },
  FORMATION: { route: "/formations/:code" },
  ROADMAP: { route: "/roadmap" },
  MODULE: { route: "/formations/:fc/modules/:mc" },
  QUIZ: { route: null }, // context-dock overlay on MODULE, not its own route
  MISSION: { route: null }, // context-dock overlay on MODULE, not its own route; /missions is a distinct list view
  MISSIONS_LIST: { route: "/missions" },
  MENTOR: { route: null }, // context-dock overlay, not its own route
  BADGES: { route: "/badges" },
  SKILLS: { route: "/skills" },
  CERTIFICATIONS: { route: "/certifications" },
  WALLET: { route: "/wallet" },
  FREK_PROFILE: { route: "/frek-profile" },
  EXPANSION: { route: null }, // no surface exists yet — ACADEMY_FUNNEL_GAP_MATRIX.md
  ECOSYSTEM: { route: null }, // no surface exists yet — ACADEMY_FUNNEL_GAP_MATRIX.md
});

/**
 * Declared edges only — a pair not listed here has no defined spatial
 * relationship (see `resolveEdge`'s fail-safe default, never an
 * invented one). `depth`: "deeper" | "shallower" | "lateral".
 * `sharedObjectPolicy`/`environmentContinuityPolicy` are advisory
 * strings a future camera-follow implementation reads; this wave does
 * not implement camera-follow on any of these, per mission §4/§10 —
 * infrastructure only.
 */
const EDGES = [
  edge("LANDING", "SIGNUP", { direction: "forward", depth: "lateral" }),
  edge("SIGNUP", "ONBOARDING", { direction: "forward", depth: "deeper" }),
  edge("ONBOARDING", "ACTIVATION", { direction: "forward", depth: "deeper" }),
  edge("ACTIVATION", "DASHBOARD", { direction: "forward", depth: "deeper" }),
  edge("DASHBOARD", "FORMATIONS", { direction: "forward", depth: "lateral" }),
  edge("FORMATIONS", "FORMATION", { direction: "forward", depth: "deeper" }),
  edge("FORMATION", "ROADMAP", { direction: "forward", depth: "lateral" }),
  edge("DASHBOARD", "ROADMAP", { direction: "forward", depth: "lateral" }),
  edge("ROADMAP", "MODULE", { direction: "forward", depth: "deeper" }),
  edge("FORMATION", "MODULE", { direction: "forward", depth: "deeper" }),
  edge("MODULE", "QUIZ", { direction: "forward", depth: "deeper", sharedObjectPolicy: "context-overlay" }),
  edge("MODULE", "MISSION", { direction: "forward", depth: "deeper", sharedObjectPolicy: "context-overlay" }),
  edge("MODULE", "MENTOR", { direction: "forward", depth: "deeper", sharedObjectPolicy: "context-overlay" }),
  edge("DASHBOARD", "MISSIONS_LIST", { direction: "forward", depth: "lateral" }),
  edge("DASHBOARD", "BADGES", { direction: "forward", depth: "lateral" }),
  edge("DASHBOARD", "SKILLS", { direction: "forward", depth: "lateral" }),
  edge("DASHBOARD", "CERTIFICATIONS", { direction: "forward", depth: "lateral" }),
  edge("DASHBOARD", "WALLET", { direction: "forward", depth: "lateral" }),
  edge("DASHBOARD", "FREK_PROFILE", { direction: "forward", depth: "lateral" }),
  edge("ROADMAP", "EXPANSION", { direction: "forward", depth: "lateral" }),
  edge("FREK_PROFILE", "ECOSYSTEM", { direction: "forward", depth: "lateral" }),
];

function edge(from, to, opts) {
  return {
    source: from,
    destination: to,
    direction: opts.direction,
    sourceDepth: opts.sourceDepth ?? "FOCUS",
    destinationDepth: opts.destinationDepth ?? "ACTIVE",
    spatialDirection: opts.depth, // deeper | shallower | lateral
    transitionIntent: opts.transitionIntent ?? "enter",
    returnIntent: opts.returnIntent ?? "exact-return",
    sharedObjectPolicy: opts.sharedObjectPolicy ?? "none",
    environmentContinuityPolicy: opts.environmentContinuityPolicy ?? "persist",
  };
}

const FORWARD_INDEX = new Map(EDGES.map((e) => [`${e.source}|${e.destination}`, e]));

/** Fail-safe default for any pair not explicitly declared — lateral,
 * no shared-object/camera-follow behavior. Never throws, never
 * fabricates a "deeper"/"shallower" relationship that wasn't declared
 * (mission §7: "do not invent routes that do not exist" extends here
 * to not inventing relationships either). */
const UNDECLARED_EDGE = Object.freeze({
  source: null,
  destination: null,
  direction: "forward",
  spatialDirection: "lateral",
  transitionIntent: "enter",
  returnIntent: "exact-return",
  sharedObjectPolicy: "none",
  environmentContinuityPolicy: "persist",
  declared: false,
});

/** Resolves the edge for `from -> to`. Returns the declared edge (with
 * `declared: true`) if one exists; the inverse of a declared `to -> from`
 * edge if only that direction was declared (a real "return" relation,
 * spatial direction flipped shallower<->deeper, lateral stays lateral);
 * otherwise the safe undeclared default. */
export function resolveEdge(from, to) {
  const forward = FORWARD_INDEX.get(`${from}|${to}`);
  if (forward) return { ...forward, declared: true };
  const inverse = FORWARD_INDEX.get(`${to}|${from}`);
  if (inverse) {
    return {
      ...inverse,
      source: from,
      destination: to,
      direction: "return",
      spatialDirection: invertDepth(inverse.spatialDirection),
      sourceDepth: inverse.destinationDepth,
      destinationDepth: inverse.sourceDepth,
      declared: true,
    };
  }
  return { ...UNDECLARED_EDGE, source: from, destination: to };
}

function invertDepth(depth) {
  if (depth === "deeper") return "shallower";
  if (depth === "shallower") return "deeper";
  return "lateral";
}

/** True only for an explicitly declared pair (either direction) — a
 * caller deciding whether to attempt a camera-follow/shared-object
 * transition should check this first rather than assume one exists. */
export function hasDeclaredEdge(from, to) {
  return FORWARD_INDEX.has(`${from}|${to}`) || FORWARD_INDEX.has(`${to}|${from}`);
}
