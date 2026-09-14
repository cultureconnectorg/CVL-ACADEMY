# ACA-0015 / ACA-0016 — Layout→Outlet Routing Restructure & Environmental Continuity

```
STATUS: EXECUTED (2026-09-08).
Authorization: explicit Founder instruction, this session — "tu as toutes
les autorisations pour le débloquer" — covers the first of the two
REPLACE-BLOCKED items in docs/SPATIAL_H1_INTEGRATION_PLAN.md ("App shell /
routing", implicitly the Layout-mounting pattern it depends on). The
second REPLACE-BLOCKED item (real environmental/vegetal imagery) remains
explicitly out of scope — see "What remains unbuilt" below.
```

## What this closes

`AcademyBackdrop.jsx` and `docs/SPATIAL_H1_INTEGRATION_PLAN.md` both
carried the same disclosed limitation: `Layout` was mounted **per route**
(the old `Protected({ children, roles })` wrapper in `App.js` rendered a
fresh `<Layout>{children}</Layout>` on every matched route), so the
sidebar, `AcademyBackdrop`, and the mentor dock all unmounted and
remounted on every navigation — even a same-section navigation like
`/dashboard` → `/roadmap`. `ENVIRONMENT_RESET_PER_ROUTE = FORBIDDEN` was
therefore aspirational, not real: the backdrop's tint re-painted from
scratch on every route instead of persisting and merely re-tinting when
the learner's intention pole actually changed.

This was flagged as a **REPLACE-BLOCKED** item in the H1 plan precisely
because fixing it means changing how routing itself is structured (a real
`Layout` route, not a per-page wrapper) — a change with app-wide blast
radius, not a component-local one, hence needing its own explicit
go-ahead beyond general spatial-work authorization. That go-ahead was
given this session.

## What changed

### `frontend/src/App.js`
- Removed `Protected({ children, roles })` entirely.
- Added `LayoutRoute()` — a real Outlet-based layout route:
  ```jsx
  function LayoutRoute() {
    return (
      <Layout>
        <RouteTransition>
          <Outlet />
        </RouteTransition>
      </Layout>
    );
  }
  ```
- Added `ProtectedRoute({ roles })` — the same guard logic `Protected`
  always ran (loading → null, no user → `/`, onboarding incomplete →
  `/onboarding`, role mismatch → `/dashboard`), but rendering `<Outlet/>`
  on success instead of `<Layout>{children}</Layout>` — `Layout` is now
  supplied once by the parent `LayoutRoute`, not by every guarded route.
- Restructured the route tree: `/` (Landing) and `/onboarding` stay
  top-level, unwrapped (never had `Layout`). Every other route —
  `/formations`, `/formations/:code`, `/offers` (public, no guard) and
  everything under `ProtectedRoute`/`ProtectedRoute roles={...}` (student
  area, all six canonical trees, trainer/jury/admin) — now nests under
  the single `<Route element={<LayoutRoute />}>`. Every path, every
  redirect target, every test ID is byte-identical to what `Protected`
  produced; only *which component owns mounting `Layout`* changed.

### `frontend/src/lib/RouteTransition.jsx`
`RouteTransition` gained an optional `keyFor` prop and is now mounted
**twice**, at two depths:
1. **Outer** (still wrapping the whole `<Routes>` in `App.js`), now keyed
   by the new `sectionKeyFor(pathname)` instead of the raw pathname. Every
   in-`Layout` route collapses to the same constant key (`"app-shell"`),
   so this instance only re-keys (crossfades) crossing the boundary into
   or out of that section — i.e. Landing/Onboarding ↔ everything else.
2. **Inner** (new), wrapping only `<Outlet/>` inside `LayoutRoute`, keyed
   by the raw pathname as `RouteTransition` always was — this is what
   actually crossfades page content on an in-section navigation, while
   `Layout` itself never re-keys and therefore never remounts.

New exports `isLayoutSectionPath(pathname)` and `sectionKeyFor(pathname)`
are pure functions of real location data (a `Set` membership check
against the two standalone paths) — same ROUT-SAFETY invariant the raw
pathname key already satisfied, no arbitrary counters introduced.

Both `RouteTransition` instances are the same component with the same
guarantees (`initial={false}`, canonical-URL-derived key, reduced-motion
duration collapse) — only which location-derived string becomes the key
differs.

### `frontend/src/components/AcademyBackdrop.jsx`
Docstring-only change: the previous "disclosed limitation, not silently
worked around" paragraph (explaining the tint re-establishes per-route
instead of persisting) is replaced with a note that the limitation is
resolved, citing this report and the new e2e proof. Zero functional code
changed in this file — `AcademyBackdrop` was never the problem; the
problem was how often it got remounted.

### `frontend/e2e/environmental-continuity.spec.js` (new)
Three tests, using the same DOM-identity marker technique H0.9/H0.10
established (stamp a JS-only property — not an attribute a re-render
could coincidentally reproduce — on the live node, then assert it
survives or doesn't):

1. **Positive case**: `app-layout` survives `/dashboard` → `/roadmap`
   (marker present after navigation).
2. **Control case**: the same marker does **not** survive a real
   `Layout` unmount — forcing `/api/auth/me` to 401 (the real mechanism
   `auth.jsx` already reacts to: its catch calls `clearSession()`/
   `setUser(null)`) and navigating to `/` shows Landing with zero
   `app-layout` nodes. This proves the marker technique is meaningful,
   not trivially true.
3. **Reduced motion**: the same positive-case survival holds with
   `prefers-reduced-motion: reduce` emulated, navigating `/dashboard` →
   `/frek-profile`.

All three pass (confirmed locally, see Verification below).

## Verification

- `npx eslint src/App.js src/lib/RouteTransition.jsx` — clean.
- `CI=true yarn build` — clean, no warnings-as-errors.
- `npx playwright test e2e/` — 85/86 passed. The one failure
  (`module-journey-navigation.spec.js`'s BACK_FORWARD test) is a
  pre-existing, confirmed-unrelated flake: it fails identically with this
  diff stashed out, on the base commit, in every run this session. It is
  not part of this repo's GitHub Actions CI gate (only `backend`
  flake8+pytest and `frontend` build run there), so it does not block
  mergeability, and is left untouched and undisclosed-as-fixed.
- No `.env.example` change needed — no new feature flag was introduced.
  The restructure is unconditional and preserves exact existing
  behavior (every guard, every redirect, every test ID) for every flag
  state; it changes *when* `Layout` mounts, not what it renders or who
  can reach what.

## What remains unbuilt (explicitly out of scope for this pass)

This pass closes the routing prerequisite; it does **not** complete
ACA-0015 (camera-follow transitions on real routes) on its own:

1. **`cameraFollow.js`'s `CROSSING`/`REVEALING` phases are still not
   wired into any production caller.** Only `IDLE`/`INTENT`/`LOCKING`
   are wired today, via `useCameraIntent.js`. The state machine's own
   docstring names the Outlet restructure as a *necessary* prerequisite
   but explicitly *not sufficient*: it also requires a real
   mount-detection race guard, because React Router's unmount/
   remount-and-refetch cycle means a destination page's real anchor
   element is not synchronously available the instant `navigate()`
   fires (unlike the single-document-SPA prototype this state machine
   was ported from). That guard has not been designed or built in this
   pass. ACA-0015 stays `in_progress`.
2. **The second REPLACE-BLOCKED item** — real environmental/vegetal
   imagery replacing the CSS-blob backdrop placeholder — remains
   explicitly out of scope per the H1 plan's own note: a separate
   design/asset decision (weight budget, licensing/provenance review),
   not to be rushed into alongside interaction-grammar/routing work.
3. **Formation-card → Module FLIP extension** (beyond the already-proven
   Hub→Module path) is unbuilt.
4. **Mobile-swipe `useSwipeRail()` promotion** to a shared hook is
   unbuilt.

## What this pass does complete

- **ACA-0016** (environmental continuity across Hero→Formation→Roadmap→
  Module): the structural precondition is now real and proven —
  `Layout`/`AcademyBackdrop` genuinely persist across in-section
  navigation, `ENVIRONMENT_RESET_PER_ROUTE = FORBIDDEN` holds with a DOM-
  identity-verified test, not just a docstring claim. Marked complete.
