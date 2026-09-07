import { clearPositions, getPosition, savePosition } from "@/lib/scrollRestoration";

describe("scrollRestoration store (ACA-0023 scroll slice)", () => {
  beforeEach(() => clearPositions());

  test("saves and retrieves a position by key", () => {
    savePosition("key-a", 420);
    expect(getPosition("key-a")).toBe(420);
  });

  test("unknown key returns undefined, never a fabricated 0", () => {
    expect(getPosition("never-seen")).toBeUndefined();
  });

  test("re-saving the same key overwrites, not duplicates", () => {
    savePosition("key-a", 100);
    savePosition("key-a", 300);
    expect(getPosition("key-a")).toBe(300);
  });

  test("two distinct keys keep independent positions (same pathname, two history entries)", () => {
    savePosition("entry-1", 50);
    savePosition("entry-2", 900);
    expect(getPosition("entry-1")).toBe(50);
    expect(getPosition("entry-2")).toBe(900);
  });

  test("a falsy key is ignored, never stored", () => {
    savePosition(null, 100);
    savePosition(undefined, 100);
    savePosition("", 100);
    expect(getPosition(null)).toBeUndefined();
    expect(getPosition(undefined)).toBeUndefined();
    expect(getPosition("")).toBeUndefined();
  });

  test("evicts the oldest entry once past the cap, keeps the most recent 50", () => {
    for (let i = 0; i < 55; i++) savePosition(`k${i}`, i);
    expect(getPosition("k0")).toBeUndefined();
    expect(getPosition("k4")).toBeUndefined();
    expect(getPosition("k5")).toBe(5);
    expect(getPosition("k54")).toBe(54);
  });
});
