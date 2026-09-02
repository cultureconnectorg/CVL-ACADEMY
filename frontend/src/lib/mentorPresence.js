/**
 * MENTOR = CONTEXTUAL_PRESENCE (W3-C). The Mentor FAB/panel must never be
 * a permanent floating chatbot (MENTOR_ALWAYS_VISIBLE = FORBIDDEN) — it
 * only appears where a pedagogical context justifies it. Pure
 * route-matching, unit-tested directly, so the rule doesn't need Layout.js
 * mounted to verify.
 *
 * Scope, deliberately conservative: only inside an actual module
 * (ModuleJourney, `/formations/:fc/modules/:mc`) — the one screen where a
 * learner is unambiguously mid-lesson, not just browsing. Formation
 * discovery/detail, dashboard, missions, badges, wallet, frek-profile,
 * and every staff screen (trainer/jury/admin) are NOT pedagogical-content
 * contexts by this definition. Widening the set is a separate, explicit
 * decision for a later wave — not assumed here.
 */
const MODULE_JOURNEY_PATTERN = /^\/formations\/[^/]+\/modules\/[^/]+\/?$/;

export function isPedagogicalContext(pathname) {
  return MODULE_JOURNEY_PATTERN.test(pathname);
}
