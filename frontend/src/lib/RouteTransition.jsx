/**
 * Spatial Learning — route transition wrapper.
 *
 * Built as unmounted infrastructure in W1-C; mounted in App.js in W2-A
 * (MOT-013 "continuous route transition" — see docs/SPATIAL_LEARNING_
 * W2A_ROUTE_CONTINUITY_REPORT.md for the runtime proof this wave adds).
 *
 * Purely presentational: it re-keys a `motion.div` by `location.pathname`
 * so a mounted route can crossfade instead of hard-cutting, using the
 * ENTER primitive's duration/easing (MOT-013 "continuous route
 * transition", MOT-029 reduced-motion equivalence). It does **not**
 * intercept, delay, or redirect navigation in any way — `BrowserRouter`,
 * `Routes`, and `Protected` (frontend/src/App.js) keep making every
 * routing/auth decision exactly as they do today; this component only
 * ever sees whatever they already decided to render.
 *
 * ROUT-SAFETY guarantees, and why each holds:
 * - **Canonical URLs / deep links**: the key is `location.pathname`
 *   itself (from `react-router-dom`'s `useLocation`), not an internal
 *   counter — a hard refresh or a pasted deep link renders on the first
 *   paint via `initial={false}` (no phantom entry animation, no delay
 *   before content appears).
 * - **Browser history / back-forward**: history navigation is handled
 *   entirely by `BrowserRouter` before this component runs; this
 *   component reacts to the resulting `location` the same way for a
 *   back/forward navigation as for a link click — it has no branch that
 *   distinguishes them, so it cannot special-case (or break) either.
 * - **Refresh**: `initial={false}` means the very first render for a
 *   given mount of the app (i.e. every hard refresh) skips the enter
 *   animation and paints immediately.
 * - **Auth / `Protected` behavior**: `Protected` in App.js runs its
 *   redirect logic (`useAuth`, `onboarding_completed`, `roles`) and
 *   decides *what* to render before this wrapper is ever involved — this
 *   component only wraps the already-decided output, so a redirect from
 *   `Protected` (e.g. to `/onboarding` or `/dashboard`) crossfades exactly
 *   like any other route change, it is never suppressed or intercepted.
 *
 * **Integration point** (frontend/src/App.js, since W2-A):
 *
 *   <Suspense fallback={<PageFallback />}>
 *     <RouteTransition>
 *       <Routes>...</Routes>
 *     </RouteTransition>
 *   </Suspense>
 *
 * placed exactly where `<Routes>` used to sit directly under `Suspense`,
 * no other change to App.js's routing/auth structure.
 *
 * **ACA-0015/ACA-0016 update** — this component is now mounted *twice*,
 * at two different depths, each with a different `keyFor`:
 *
 * 1. Still wrapping the whole `<Routes>` in App.js, but keyed by
 *    `sectionKeyFor(pathname)` instead of the raw pathname — every route
 *    inside the authenticated/public-layout section (everything
 *    `Layout`-wrapped) now collapses to the same section key
 *    (`"app-shell"`), so this **outer** instance only re-keys (and
 *    therefore only crossfades) when a navigation crosses the boundary
 *    into or out of that section (Landing/Onboarding <-> everything
 *    else) — never on an ordinary in-section navigation.
 * 2. A **second** instance, keyed by the raw pathname as before,
 *    now wraps only `<Outlet/>` inside `LayoutRoute` (App.js) — this is
 *    what actually crossfades the page content on an in-section
 *    navigation, while `Layout` itself (sidebar, `AcademyBackdrop`,
 *    mentor dock) stays mounted the whole time, per `Layout`'s own
 *    promotion to a real Outlet-based layout route (App.js) — the
 *    exact restructure `AcademyBackdrop.jsx`'s own docstring names as
 *    the prerequisite for `ENVIRONMENT_RESET_PER_ROUTE = FORBIDDEN`
 *    to actually hold, and `SPATIAL_H1_INTEGRATION_PLAN.md`'s own
 *    REPLACE-BLOCKED note for the same reason (unblocked by explicit
 *    Founder authorization, 2026-09-08).
 *
 * Both instances are the same component, same guarantees (canonical
 * URL as the key source, `initial={false}`, reduced-motion collapse) —
 * only *which* location-derived string becomes the key differs.
 */

import { useRef } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { useLocation } from "react-router-dom";
import { MOTION_EASING, motionDuration } from "@/lib/motion-tokens";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { resolveEdge } from "@/lib/spatial/topology";
import { routeToTopologyNode } from "@/lib/spatial/routeTopologyMap";

// ACA-0016 — the only two routes that render *outside* the Layout shell
// (App.js: Landing at "/", Onboarding at "/onboarding"). Every other
// route is nested under `LayoutRoute`, so its section key collapses to
// the same constant regardless of which of those routes it is — the
// mechanism that lets Layout/AcademyBackdrop persist across in-section
// navigation instead of remounting on every route change.
const NO_LAYOUT_PATHS = new Set(["/", "/onboarding"]);
const APP_SHELL_SECTION = "app-shell";

/** Exported for `sectionKeyFor`'s own test coverage and for anything
 * else that needs to know "is this pathname inside the Layout shell"
 * without duplicating `NO_LAYOUT_PATHS` (e.g. a future camera-follow
 * cross-route guard deciding whether a same-shell REVEALING handoff is
 * even possible). */
export function isLayoutSectionPath(pathname) {
  return !NO_LAYOUT_PATHS.has(pathname);
}

/** The outer RouteTransition's key: the real pathname for the two
 * standalone routes, or the constant section key for everything else —
 * still a pure function of real location data, never an arbitrary
 * counter, same ROUT-SAFETY invariant the raw-pathname key already
 * satisfied. */
export function sectionKeyFor(pathname) {
  return isLayoutSectionPath(pathname) ? APP_SHELL_SECTION : pathname;
}

/**
 * W-FUNNEL-1 extension: RouteTransition can now resolve which
 * topology edge (docs/ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md §4)
 * a navigation crosses — infrastructure only. Per the W-FUNNEL-1
 * authorization §10/§22: "with feature flags OFF, retain exact current
 * production motion/navigation... do not implement major visual
 * spatial movement yet." So the actual rendered animation below
 * (opacity crossfade, `motionDuration("enter")`) is **unconditional
 * and unchanged** regardless of any flag — SPATIAL_ROUTE_TRANSITIONS
 * only gates whether the resolved edge is exposed at all (as an inert
 * `data-topology-edge` attribute, consumed by nothing yet, visible only
 * to future spatial work or to SPATIAL_DEBUG inspection), never
 * whether it changes what's on screen.
 */
export function RouteTransition({ children, keyFor }) {
  const location = useLocation();
  const reduced = useReducedMotion();
  const duration = motionDuration("enter", reduced) / 1000;
  const previousPathnameRef = useRef(null);

  let topologyEdgeAttr;
  if (FEATURE_FLAGS.SPATIAL_ROUTE_TRANSITIONS) {
    const fromNode = routeToTopologyNode(previousPathnameRef.current);
    const toNode = routeToTopologyNode(location.pathname);
    if (fromNode && toNode) {
      const edge = resolveEdge(fromNode, toNode);
      topologyEdgeAttr = `${fromNode}->${toNode}:${edge.spatialDirection}`;
    }
  }
  previousPathnameRef.current = location.pathname;

  // `keyFor` lets a caller re-key on something coarser than the raw
  // pathname (App.js's outer instance uses `sectionKeyFor` so it only
  // re-keys crossing the Layout-shell boundary) — defaults to the raw
  // pathname, i.e. today's exact original behavior, when omitted.
  const transitionKey = keyFor ? keyFor(location.pathname) : location.pathname;

  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={transitionKey}
        data-topology-edge={topologyEdgeAttr}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration, ease: MOTION_EASING.enter }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
