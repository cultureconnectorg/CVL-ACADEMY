/**
 * Spatial Learning — route transition wrapper (W1-C, foundation only).
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
 * **Intended integration point** (not wired in this wave —
 * VISIBLE_SPATIAL_LEARNING is NOT_AUTHORIZED, so App.js is unmodified):
 *
 *   <Suspense fallback={<PageFallback />}>
 *     <RouteTransition>
 *       <Routes>...</Routes>
 *     </RouteTransition>
 *   </Suspense>
 *
 * placed exactly where `<Routes>` already sits in App.js, no other
 * change required.
 */

import { AnimatePresence, motion } from "framer-motion";
import { useLocation } from "react-router-dom";
import { MOTION_EASING, motionDuration } from "@/lib/motion-tokens";
import { useReducedMotion } from "@/lib/useReducedMotion";

export function RouteTransition({ children }) {
  const location = useLocation();
  const reduced = useReducedMotion();
  const duration = motionDuration("enter", reduced) / 1000;

  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={location.pathname}
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
