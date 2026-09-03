import { deriveLifecycleStates, LIFECYCLE_STATES, is } from "./lifecycleState";

describe("lifecycleState.js — deriveLifecycleStates", () => {
  test("no user at all -> VISITOR only", () => {
    const states = deriveLifecycleStates({});
    expect(states).toEqual(new Set([LIFECYCLE_STATES.VISITOR]));
  });

  test("registered but onboarding not completed -> REGISTERED + ONBOARDING, nothing downstream", () => {
    const states = deriveLifecycleStates({
      user: { onboarding_completed: false, stade: "graine" },
    });
    expect(states.has(LIFECYCLE_STATES.REGISTERED)).toBe(true);
    expect(states.has(LIFECYCLE_STATES.ONBOARDING)).toBe(true);
    expect(states.has(LIFECYCLE_STATES.ACTIVATED)).toBe(false);
    expect(states.has(LIFECYCLE_STATES.VISITOR)).toBe(false);
  });

  test("onboarding completed with zero real activity -> ACTIVATED only, not FIRST_VALUE", () => {
    const states = deriveLifecycleStates({
      user: { onboarding_completed: true, stade: "graine" },
      progressionSummary: { completed_modules: 0, total_modules: 12, stade: "graine" },
      badges: [],
      missions: [],
    });
    expect(states.has(LIFECYCLE_STATES.ACTIVATED)).toBe(true);
    expect(states.has(LIFECYCLE_STATES.FIRST_VALUE)).toBe(false);
    expect(states.has(LIFECYCLE_STATES.ONBOARDING)).toBe(false); // no longer onboarding
  });

  test("a completed module -> FIRST_VALUE and, if partial, ACTIVE_LEARNER", () => {
    const states = deriveLifecycleStates({
      user: { onboarding_completed: true, stade: "graine" },
      progressionSummary: { completed_modules: 2, total_modules: 12, stade: "graine" },
      badges: [],
      missions: [],
    });
    expect(states.has(LIFECYCLE_STATES.FIRST_VALUE)).toBe(true);
    expect(states.has(LIFECYCLE_STATES.ACTIVE_LEARNER)).toBe(true);
  });

  test("all modules completed -> not ACTIVE_LEARNER (nothing left in progress)", () => {
    const states = deriveLifecycleStates({
      user: { onboarding_completed: true, stade: "arbre" },
      progressionSummary: { completed_modules: 12, total_modules: 12, stade: "arbre" },
    });
    expect(states.has(LIFECYCLE_STATES.ACTIVE_LEARNER)).toBe(false);
    expect(states.has(LIFECYCLE_STATES.FIRST_VALUE)).toBe(true);
    expect(states.has(LIFECYCLE_STATES.PROGRESSING)).toBe(true); // stade advanced past graine
  });

  test("stade still graine -> not PROGRESSING", () => {
    const states = deriveLifecycleStates({
      user: { onboarding_completed: true, stade: "graine" },
      progressionSummary: { completed_modules: 1, total_modules: 12, stade: "graine" },
    });
    expect(states.has(LIFECYCLE_STATES.PROGRESSING)).toBe(false);
  });

  test("a badge earned -> PROOF_BUILDING", () => {
    const states = deriveLifecycleStates({
      user: { onboarding_completed: true, stade: "graine" },
      badges: [{ badge_code: "BADGE-DECOUVERTE" }],
    });
    expect(states.has(LIFECYCLE_STATES.PROOF_BUILDING)).toBe(true);
  });

  test("a validated mission (not just accepted) -> PROOF_BUILDING", () => {
    const acceptedOnly = deriveLifecycleStates({
      user: { onboarding_completed: true, stade: "graine" },
      missions: [{ status: "accepted" }],
    });
    expect(acceptedOnly.has(LIFECYCLE_STATES.PROOF_BUILDING)).toBe(false);

    const validated = deriveLifecycleStates({
      user: { onboarding_completed: true, stade: "graine" },
      missions: [{ status: "validated" }],
    });
    expect(validated.has(LIFECYCLE_STATES.PROOF_BUILDING)).toBe(true);
  });

  test("RETURNING reads the real backend-derived frekProfile.returning flag only", () => {
    const notReturning = deriveLifecycleStates({
      user: { onboarding_completed: true, stade: "graine" },
      frekProfile: { returning: false },
    });
    expect(notReturning.has(LIFECYCLE_STATES.RETURNING)).toBe(false);

    const returning = deriveLifecycleStates({
      user: { onboarding_completed: true, stade: "graine" },
      frekProfile: { returning: true },
    });
    expect(returning.has(LIFECYCLE_STATES.RETURNING)).toBe(true);
  });

  test("EXPANDING only when own pole is fully validated AND something else is unlocked", () => {
    const notYet = deriveLifecycleStates({
      user: { onboarding_completed: true, stade: "graine" },
      learningPath: {
        own_pole: [{ progress_pct: 60 }],
        other_poles: [{ is_unlocked: true }],
      },
    });
    expect(notYet.has(LIFECYCLE_STATES.EXPANDING)).toBe(false);

    const expanding = deriveLifecycleStates({
      user: { onboarding_completed: true, stade: "graine" },
      learningPath: {
        own_pole: [{ progress_pct: 100 }, { progress_pct: 100 }],
        other_poles: [{ is_unlocked: false }, { is_unlocked: true }],
      },
    });
    expect(expanding.has(LIFECYCLE_STATES.EXPANDING)).toBe(true);
  });

  test("EXPANDING is false when own pole is done but nothing else is unlocked", () => {
    const states = deriveLifecycleStates({
      user: { onboarding_completed: true, stade: "graine" },
      learningPath: {
        own_pole: [{ progress_pct: 100 }],
        other_poles: [{ is_unlocked: false }],
      },
    });
    expect(states.has(LIFECYCLE_STATES.EXPANDING)).toBe(false);
  });

  test("missing/partial signals never throw — absent data reads as false, never assumed true", () => {
    expect(() => deriveLifecycleStates({ user: { onboarding_completed: true } })).not.toThrow();
    const states = deriveLifecycleStates({ user: { onboarding_completed: true } });
    expect(states.has(LIFECYCLE_STATES.FIRST_VALUE)).toBe(false);
    expect(states.has(LIFECYCLE_STATES.PROOF_BUILDING)).toBe(false);
    expect(states.has(LIFECYCLE_STATES.EXPANDING)).toBe(false);
  });

  test("states are non-exclusive — a learner can be several at once", () => {
    const states = deriveLifecycleStates({
      user: { onboarding_completed: true, stade: "racine" },
      progressionSummary: { completed_modules: 3, total_modules: 12, stade: "racine" },
      badges: [{ badge_code: "BADGE-DECOUVERTE" }],
      frekProfile: { returning: true },
    });
    expect(states.has(LIFECYCLE_STATES.ACTIVATED)).toBe(true);
    expect(states.has(LIFECYCLE_STATES.FIRST_VALUE)).toBe(true);
    expect(states.has(LIFECYCLE_STATES.ACTIVE_LEARNER)).toBe(true);
    expect(states.has(LIFECYCLE_STATES.PROGRESSING)).toBe(true);
    expect(states.has(LIFECYCLE_STATES.PROOF_BUILDING)).toBe(true);
    expect(states.has(LIFECYCLE_STATES.RETURNING)).toBe(true);
    expect(states.size).toBeGreaterThanOrEqual(6);
  });

  test("is() helper matches states.has()", () => {
    const states = deriveLifecycleStates({});
    expect(is(states, LIFECYCLE_STATES.VISITOR)).toBe(true);
    expect(is(states, LIFECYCLE_STATES.PROGRESSING)).toBe(false);
  });

  test("never invents a paid/customer/subscription state — no such value exists anywhere in the enum", () => {
    const forbidden = ["PAID", "CUSTOMER", "SUBSCRIBED", "PREMIUM"];
    const enumValues = Object.values(LIFECYCLE_STATES);
    forbidden.forEach((word) => {
      expect(enumValues).not.toContain(word);
    });
    // and no derivation path can produce a value outside the declared enum
    const states = deriveLifecycleStates({
      user: { onboarding_completed: true, stade: "foret" },
      progressionSummary: { completed_modules: 100, total_modules: 100, stade: "foret" },
      badges: [{ badge_code: "x" }],
      missions: [{ status: "validated" }],
      frekProfile: { returning: true },
      learningPath: { own_pole: [{ progress_pct: 100 }], other_poles: [{ is_unlocked: true }] },
    });
    [...states].forEach((s) => expect(enumValues).toContain(s));
  });
});
