import { clampRailIndex, interpolateRailPosition, nearestRailIndex } from "./useSpatialRail";

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

  test("interpolates a fractional attention position between real item centers", () => {
    expect(interpolateRailPosition(100, [100, 300, 500])).toBe(0);
    expect(interpolateRailPosition(200, [100, 300, 500])).toBeCloseTo(0.5);
    expect(interpolateRailPosition(350, [100, 300, 500])).toBeCloseTo(1.25);
    expect(interpolateRailPosition(999, [100, 300, 500])).toBe(2);
  });

  test("attention interpolation fails safe without usable geometry", () => {
    expect(interpolateRailPosition(NaN, [100, 300])).toBe(0);
    expect(interpolateRailPosition(100, [])).toBe(0);
    expect(interpolateRailPosition(100, [NaN])).toBe(0);
  });

  test("fails safe to index zero without geometry", () => {
    expect(nearestRailIndex(null, [])).toBe(0);
    expect(nearestRailIndex({ left: 0, width: 100 }, [])).toBe(0);
  });
});
