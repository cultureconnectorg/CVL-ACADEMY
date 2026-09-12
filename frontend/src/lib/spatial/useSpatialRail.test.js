import { clampRailIndex, nearestRailIndex } from "./useSpatialRail";

describe("useSpatialRail pure helpers", () => {
  test("clamps focus index into the real item range", () => {
    expect(clampRailIndex(-4, 6)).toBe(0);
    expect(clampRailIndex(2.4, 6)).toBe(2);
    expect(clampRailIndex(2.6, 6)).toBe(3);
    expect(clampRailIndex(99, 6)).toBe(5);
    expect(clampRailIndex(1, 0)).toBe(0);
  });

  test("selects the item nearest the rail viewport center", () => {
    const rail = { left: 100, width: 600 };
    const items = [
      { left: 120, width: 180 },
      { left: 330, width: 180 },
      { left: 540, width: 180 },
    ];
    // Rail center = 400. Item centers = 210, 420, 630.
    expect(nearestRailIndex(rail, items)).toBe(1);
  });

  test("fails safe to index zero without geometry", () => {
    expect(nearestRailIndex(null, [])).toBe(0);
    expect(nearestRailIndex({ left: 0, width: 100 }, [])).toBe(0);
  });
});
