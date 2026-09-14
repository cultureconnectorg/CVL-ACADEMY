import {
  clearRailPositions,
  getRailPosition,
  saveRailPosition,
} from "@/lib/railPositionRestoration";

describe("railPositionRestoration store (ACA-0023 camera/rail/focus slice)", () => {
  beforeEach(() => clearRailPositions());

  test("saves and retrieves a position by key", () => {
    saveRailPosition("key-a", { focusedKey: "formation:FMS-01", scrollLeft: 240 });
    expect(getRailPosition("key-a")).toEqual({
      focusedKey: "formation:FMS-01",
      scrollLeft: 240,
    });
  });

  test("unknown key returns undefined, never a fabricated default", () => {
    expect(getRailPosition("never-seen")).toBeUndefined();
  });

  test("re-saving the same key overwrites, not duplicates", () => {
    saveRailPosition("key-a", { focusedKey: "mission:M1", scrollLeft: 0 });
    saveRailPosition("key-a", { focusedKey: "formation:FMS-02", scrollLeft: 500 });
    expect(getRailPosition("key-a")).toEqual({
      focusedKey: "formation:FMS-02",
      scrollLeft: 500,
    });
  });

  test("two distinct keys keep independent positions (same pathname, two history entries)", () => {
    saveRailPosition("entry-1", { focusedKey: "formation:A", scrollLeft: 10 });
    saveRailPosition("entry-2", { focusedKey: "formation:B", scrollLeft: 900 });
    expect(getRailPosition("entry-1").focusedKey).toBe("formation:A");
    expect(getRailPosition("entry-2").focusedKey).toBe("formation:B");
  });

  test("a falsy key is ignored, never stored", () => {
    saveRailPosition(null, { focusedKey: "x", scrollLeft: 1 });
    saveRailPosition(undefined, { focusedKey: "x", scrollLeft: 1 });
    saveRailPosition("", { focusedKey: "x", scrollLeft: 1 });
    expect(getRailPosition(null)).toBeUndefined();
    expect(getRailPosition(undefined)).toBeUndefined();
    expect(getRailPosition("")).toBeUndefined();
  });

  test("evicts the oldest entry once past the cap, keeps the most recent 50", () => {
    for (let i = 0; i < 55; i++) {
      saveRailPosition(`k${i}`, { focusedKey: `item:${i}`, scrollLeft: i });
    }
    expect(getRailPosition("k0")).toBeUndefined();
    expect(getRailPosition("k4")).toBeUndefined();
    expect(getRailPosition("k5")).toEqual({ focusedKey: "item:5", scrollLeft: 5 });
    expect(getRailPosition("k54")).toEqual({ focusedKey: "item:54", scrollLeft: 54 });
  });
});
