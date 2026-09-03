/**
 * Maps a real `frontend/src/App.js` pathname to its topology.js node key
 * (W-FUNNEL-1). Kept as its own small module, separate from topology.js
 * itself, so topology.js stays route-agnostic (a node MAY represent a
 * lifecycle state with no route at all, per mission §7) while this file
 * owns the one place that knows the real, current route strings —
 * intentionally the only file that needs updating if `App.js`'s routes
 * ever change.
 *
 * Static (non-dynamic) routes are matched exactly; the two dynamic
 * routes (`/formations/:code`, `/formations/:fc/modules/:mc`) are
 * matched by shape. An unrecognized pathname resolves to `null` — never
 * a guess — so `RouteTransition`'s topology lookup simply omits itself
 * for that navigation rather than reporting something false.
 */

const STATIC_ROUTES = {
  "/": "LANDING", // also SIGNUP (inline mode) — ambiguous by pathname alone, LANDING is the safe default
  "/onboarding": "ONBOARDING",
  "/dashboard": "DASHBOARD",
  "/formations": "FORMATIONS",
  "/roadmap": "ROADMAP",
  "/missions": "MISSIONS_LIST",
  "/badges": "BADGES",
  "/skills": "SKILLS",
  "/certifications": "CERTIFICATIONS",
  "/wallet": "WALLET",
  "/frek-profile": "FREK_PROFILE",
};

export function routeToTopologyNode(pathname) {
  if (!pathname) return null;
  if (STATIC_ROUTES[pathname]) return STATIC_ROUTES[pathname];
  if (/^\/formations\/[^/]+\/modules\/[^/]+$/.test(pathname)) return "MODULE";
  if (/^\/formations\/[^/]+$/.test(pathname)) return "FORMATION";
  return null;
}
