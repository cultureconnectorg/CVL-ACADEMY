/**
 * Academy lifecycle state — derived, non-exclusive maturity signals
 * (W-FUNNEL-1). See docs/ACADEMY_LIFECYCLE_STATE_MODEL.md for the full
 * design rationale; this module implements the exact 10-state minimum
 * named in the W-FUNNEL-1 authorization (§8), which is authoritative
 * over that earlier design doc's own slightly different naming
 * (IDENTIFIED/LEARNING/PROVEN etc.) — see docs/ACADEMY_W_FUNNEL_1_
 * FOUNDATION_REPORT.md for the reconciliation note.
 *
 * DERIVED, NOT STORED: every function here is pure — given already-
 * fetched API response shapes (the same ones `Dashboard.js` already
 * calls: `/frek/profile`, `/user/learning-path`, `/badges/mine`,
 * `/missions/mine`, `/progression/summary`), it computes a *read-time*
 * classification. Nothing here makes a network call, nothing here is
 * written back to the backend, and nothing here is a replacement for
 * any real domain field (`role`, `onboarding_completed`, `stade`, ...).
 *
 * NEVER INVENTED: no `PAID`/`CUSTOMER`/`SUBSCRIBED` state exists in
 * this module, on purpose — Monetization has no real backend capability
 * yet (docs/ACADEMY_FUNNEL_GAP_MATRIX.md), and fabricating a commercial
 * lifecycle state here would be exactly the "do not fake maturity" the
 * mission forbids. `lifecycleTest.test.js`'s own
 * `test_never_invents_a_paid_state` asserts this structurally, not just
 * by convention.
 *
 * NON-EXCLUSIVE: `deriveLifecycleStates` returns a Set — a learner is
 * commonly several of these at once (e.g. ACTIVE_LEARNER AND
 * PROGRESSING AND PROOF_BUILDING simultaneously).
 */

export const LIFECYCLE_STATES = Object.freeze({
  VISITOR: "VISITOR",
  REGISTERED: "REGISTERED",
  ONBOARDING: "ONBOARDING",
  ACTIVATED: "ACTIVATED",
  FIRST_VALUE: "FIRST_VALUE",
  ACTIVE_LEARNER: "ACTIVE_LEARNER",
  PROGRESSING: "PROGRESSING",
  PROOF_BUILDING: "PROOF_BUILDING",
  RETURNING: "RETURNING",
  EXPANDING: "EXPANDING",
});

/**
 * @typedef {Object} LifecycleSignals
 * @property {object|null} user - `UserPublic` shape from `/auth/me` or
 *   any response embedding it (`onboarding_completed`, `stade`, ...).
 *   `null` = no authenticated user at all (VISITOR).
 * @property {object|null} learningPath - `/user/learning-path` response
 *   (`own_pole`, `other_poles`, each `{ is_unlocked, progress_pct, ... }`).
 * @property {Array|null} badges - `/badges/mine` response.
 * @property {Array|null} missions - `/missions/mine` response
 *   (`{ status: "accepted"|"submitted"|"validated" }`).
 * @property {object|null} progressionSummary - `/progression/summary`
 *   response (`completed_modules`, `total_modules`, `stade`).
 * @property {object|null} frekProfile - `/frek/profile` response,
 *   including the new (W-FUNNEL-1) `returning` field.
 */

/** ACTIVE_LEARNER and FIRST_VALUE both need "has this learner touched
 * any module at all" — the real endpoints inventoried this wave only
 * expose *completed* counts, not a "started" count, so this is a
 * disclosed, conservative proxy (real evidence of SOME action beyond
 * activation), not an invented precise signal. */
function hasAnyRealActivity(signals) {
  const completedModules = signals.progressionSummary?.completed_modules ?? 0;
  const hasBadge = (signals.badges?.length ?? 0) > 0;
  const hasMissionProgress = (signals.missions ?? []).some((m) =>
    ["submitted", "validated"].includes(m.status)
  );
  return completedModules > 0 || hasBadge || hasMissionProgress;
}

/**
 * @param {LifecycleSignals} signals
 * @returns {Set<string>} the subset of LIFECYCLE_STATES currently true — never throws on partial/missing data, treats an absent signal as "cannot confirm this state" (false), never as "assume true."
 */
export function deriveLifecycleStates(signals = {}) {
  const states = new Set();
  const { user, learningPath, progressionSummary, frekProfile } = signals;

  if (!user) {
    states.add(LIFECYCLE_STATES.VISITOR);
    return states; // every other state requires a real user
  }

  states.add(LIFECYCLE_STATES.REGISTERED);

  if (!user.onboarding_completed) {
    states.add(LIFECYCLE_STATES.ONBOARDING);
    return states; // ACTIVATED and everything downstream requires onboarding_completed
  }

  states.add(LIFECYCLE_STATES.ACTIVATED);

  if (hasAnyRealActivity(signals)) {
    states.add(LIFECYCLE_STATES.FIRST_VALUE);
  }

  const completed = progressionSummary?.completed_modules ?? 0;
  const total = progressionSummary?.total_modules ?? 0;
  if (total > 0 && completed > 0 && completed < total) {
    states.add(LIFECYCLE_STATES.ACTIVE_LEARNER);
  }

  const stade = progressionSummary?.stade ?? user.stade;
  if (stade && stade !== "graine") {
    states.add(LIFECYCLE_STATES.PROGRESSING);
  }

  const hasBadge = (signals.badges?.length ?? 0) > 0;
  const hasValidatedMission = (signals.missions ?? []).some((m) => m.status === "validated");
  if (hasBadge || hasValidatedMission) {
    states.add(LIFECYCLE_STATES.PROOF_BUILDING);
  }

  // RETURNING (W-FUNNEL-1): real, derived server-side from
  // db.refresh_tokens (backend/lifecycle.py) — never guessed client-side.
  if (frekProfile?.returning === true) {
    states.add(LIFECYCLE_STATES.RETURNING);
  }

  if (learningPath) {
    const ownPole = learningPath.own_pole ?? [];
    const otherPoles = learningPath.other_poles ?? [];
    const ownPoleExhausted =
      ownPole.length > 0 && ownPole.every((f) => f.progress_pct >= 100);
    const somethingElseUnlocked = otherPoles.some((f) => f.is_unlocked);
    if (ownPoleExhausted && somethingElseUnlocked) {
      states.add(LIFECYCLE_STATES.EXPANDING);
    }
  }

  return states;
}

/** Convenience: `is(states, LIFECYCLE_STATES.PROGRESSING)` reads better
 * at a call site than `states.has(...)` in some contexts — purely a
 * readability wrapper, no different semantics. */
export function is(states, state) {
  return states.has(state);
}
