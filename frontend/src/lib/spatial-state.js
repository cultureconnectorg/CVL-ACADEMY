/**
 * Spatial Learning — spatial state machine (W1-D, foundation only).
 *
 * DOMAIN_STATE != SPATIAL_STATE. This module tracks only *which
 * navigation phase the UI chrome is currently presenting* — never
 * business/domain data. It has zero awareness of formations, modules,
 * quiz answers, progression, badges, certifications, or any other
 * backend-owned concept. It does not call `api`, does not read/write
 * `db.formations`/`db.progress`, and must never be used to gate, derive,
 * or store anything a domain reducer/API response already owns. If a
 * screen needs "is this module unlocked" or "what's my quiz score", that
 * comes from the existing domain state/API calls exactly as it does
 * today — this machine only ever answers "what spatial phase is the UI
 * in", nothing else.
 *
 * Distinct from `motion-primitives.jsx`: the primitives (FOCUS, APPROACH,
 * ENTER, RECEDE, REVEAL, RETURN, CONFIRM, HORIZON) are *per-object*
 * micro-animations a component applies to itself. This machine is the
 * *screen-level* macro phase a whole view moves through while the user
 * navigates — IDLE → FOCUS → APPROACH → ENTER → ACTIVE → CONTEXT →
 * RETURN — and a later, separately-approved wave would drive which
 * primitives fire from which spatial state, not the reverse.
 *
 * Nothing in this module is imported by any page yet (same posture as
 * W1-B/W1-C): this is infrastructure for a future, separately-approved
 * wave to consume.
 */

/** The 7 spatial states, exported as a frozen enum-like object. */
export const SPATIAL_STATES = Object.freeze({
  IDLE: "IDLE",
  FOCUS: "FOCUS",
  APPROACH: "APPROACH",
  ENTER: "ENTER",
  ACTIVE: "ACTIVE",
  CONTEXT: "CONTEXT",
  RETURN: "RETURN",
});

/**
 * Named events a caller may dispatch — deliberately *not* raw state
 * names. A caller says what happened ("the user picked something"), not
 * which state to jump to; the machine alone decides the resulting state,
 * so an invalid sequence (e.g. ACTIVATE while IDLE) can never desync
 * spatial state from what actually happened on screen.
 */
export const SPATIAL_EVENTS = Object.freeze({
  FOCUS: "FOCUS", // user focuses/selects one object (IDLE -> FOCUS)
  DEFOCUS: "DEFOCUS", // user cancels focus (FOCUS -> IDLE)
  APPROACH: "APPROACH", // system begins moving toward the focused object (FOCUS -> APPROACH)
  CANCEL_APPROACH: "CANCEL_APPROACH", // approach aborted, back to focus (APPROACH -> FOCUS)
  ENTER: "ENTER", // approach completes, entering the destination (APPROACH -> ENTER)
  ACTIVATE: "ACTIVATE", // entry completes, destination is now the active screen (ENTER -> ACTIVE)
  REVEAL_CONTEXT: "REVEAL_CONTEXT", // secondary context surfaced while staying active (ACTIVE -> CONTEXT)
  DISMISS_CONTEXT: "DISMISS_CONTEXT", // secondary context dismissed (CONTEXT -> ACTIVE)
  LEAVE: "LEAVE", // user initiates leaving, from ACTIVE or CONTEXT (-> RETURN)
  ARRIVE: "ARRIVE", // return transition completes, back to rest (RETURN -> IDLE)
});

// The full transition table: { [state]: { [event]: nextState } }. Any
// event not listed for the current state is invalid and rejected rather
// than silently coerced to some default — an unmodeled jump is a bug in
// the caller, not a state this machine should paper over.
const TRANSITIONS = Object.freeze({
  [SPATIAL_STATES.IDLE]: Object.freeze({
    [SPATIAL_EVENTS.FOCUS]: SPATIAL_STATES.FOCUS,
  }),
  [SPATIAL_STATES.FOCUS]: Object.freeze({
    [SPATIAL_EVENTS.DEFOCUS]: SPATIAL_STATES.IDLE,
    [SPATIAL_EVENTS.APPROACH]: SPATIAL_STATES.APPROACH,
  }),
  [SPATIAL_STATES.APPROACH]: Object.freeze({
    [SPATIAL_EVENTS.CANCEL_APPROACH]: SPATIAL_STATES.FOCUS,
    [SPATIAL_EVENTS.ENTER]: SPATIAL_STATES.ENTER,
  }),
  [SPATIAL_STATES.ENTER]: Object.freeze({
    [SPATIAL_EVENTS.ACTIVATE]: SPATIAL_STATES.ACTIVE,
  }),
  [SPATIAL_STATES.ACTIVE]: Object.freeze({
    [SPATIAL_EVENTS.REVEAL_CONTEXT]: SPATIAL_STATES.CONTEXT,
    [SPATIAL_EVENTS.LEAVE]: SPATIAL_STATES.RETURN,
  }),
  [SPATIAL_STATES.CONTEXT]: Object.freeze({
    [SPATIAL_EVENTS.DISMISS_CONTEXT]: SPATIAL_STATES.ACTIVE,
    [SPATIAL_EVENTS.LEAVE]: SPATIAL_STATES.RETURN,
  }),
  [SPATIAL_STATES.RETURN]: Object.freeze({
    [SPATIAL_EVENTS.ARRIVE]: SPATIAL_STATES.IDLE,
  }),
});

/** True if `event` is a legal transition out of `state`. */
export function isValidSpatialTransition(state, event) {
  return Boolean(TRANSITIONS[state] && TRANSITIONS[state][event]);
}

/**
 * Pure reducer: `(state, event) => nextState`. An event that isn't legal
 * for the current state is a no-op — it returns `state` unchanged rather
 * than throwing, so a stray dispatch (e.g. a double-click race) can never
 * crash a screen; callers that need to know a dispatch was rejected
 * should check `isValidSpatialTransition` first.
 */
export function spatialStateReducer(state, event) {
  const next = TRANSITIONS[state] && TRANSITIONS[state][event];
  return next || state;
}
