import { deriveJourneyRole, JOURNEY_ROLES, JOURNEY_VARIANTS } from "@/lib/JourneyHierarchy";

describe("ModuleJourney spatial hierarchy role derivation (W3-A)", () => {
  test("CURRENT: the open phase, regardless of done/canOpen", () => {
    expect(deriveJourneyRole({ isOpen: true, done: false, canOpen: true })).toBe(
      JOURNEY_ROLES.CURRENT
    );
    // Revisiting an already-done phase: still CURRENT while open, not ACQUIRED.
    expect(deriveJourneyRole({ isOpen: true, done: true, canOpen: true })).toBe(
      JOURNEY_ROLES.CURRENT
    );
  });

  test("ACQUIRED: done and not the open phase", () => {
    expect(deriveJourneyRole({ isOpen: false, done: true, canOpen: true })).toBe(
      JOURNEY_ROLES.ACQUIRED
    );
  });

  test("NEXT: reachable (canOpen), not done, not open — the frontier phase", () => {
    expect(deriveJourneyRole({ isOpen: false, done: false, canOpen: true })).toBe(
      JOURNEY_ROLES.NEXT
    );
  });

  test("LOCKED: not reachable at all", () => {
    expect(deriveJourneyRole({ isOpen: false, done: false, canOpen: false })).toBe(
      JOURNEY_ROLES.LOCKED
    );
  });

  test("a full 7-phase sequence: exactly one CURRENT/NEXT frontier, rest partition cleanly", () => {
    // Mirrors ModuleJourney.js's own canOpen chain: phase i can open iff
    // phase i-1 is done (index 0 always can open).
    const doneFlags = [true, true, false, false, false, false, false]; // 2 done
    const openIndex = 1; // revisiting the 2nd (already-done) phase
    const roles = doneFlags.map((done, idx) => {
      const prevDone = idx === 0 ? true : doneFlags[idx - 1];
      const canOpen = done || prevDone;
      return deriveJourneyRole({ isOpen: idx === openIndex, done, canOpen });
    });
    expect(roles).toEqual([
      "acquired", // 0: done, not open
      "current", // 1: done, but open -> current wins
      "next", // 2: not done, canOpen (prev done) -> frontier
      "locked", // 3: not done, prev (2) not done -> locked
      "locked", // 4
      "locked", // 5
      "locked", // 6
    ]);
  });

  test("JOURNEY_VARIANTS has exactly the 4 roles the derivation can produce", () => {
    expect(Object.keys(JOURNEY_VARIANTS).sort()).toEqual(["acquired", "current", "locked", "next"]);
  });

  test("opacity staircase: current is fully opaque, then acquired > next > locked", () => {
    expect(JOURNEY_VARIANTS.current.opacity).toBe(1);
    expect(JOURNEY_VARIANTS.acquired.opacity).toBeGreaterThan(JOURNEY_VARIANTS.next.opacity);
    expect(JOURNEY_VARIANTS.next.opacity).toBeGreaterThan(JOURNEY_VARIANTS.locked.opacity);
    expect(JOURNEY_VARIANTS.locked.opacity).toBeGreaterThan(0); // never fully invisible
  });

  test("only CURRENT has a scale lift — the others never move, only dim (FOREGROUND is unique)", () => {
    expect(JOURNEY_VARIANTS.current.scale).toBeGreaterThan(1);
    expect(JOURNEY_VARIANTS.acquired.scale).toBe(1);
    expect(JOURNEY_VARIANTS.next.scale).toBe(1);
    expect(JOURNEY_VARIANTS.locked.scale).toBe(1);
  });
});
