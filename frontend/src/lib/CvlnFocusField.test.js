import { deriveFocusRole, FOCUS_FIELD_VARIANTS } from "@/lib/CvlnFocusField";

describe("CVLN_FOCUS_FIELD role derivation (W2-C)", () => {
  test("IDLE: no focusedId means every item is idle", () => {
    expect(deriveFocusRole("a", null)).toBe("idle");
    expect(deriveFocusRole("a", undefined)).toBe("idle");
  });

  test("TARGET: the item whose id matches focusedId", () => {
    expect(deriveFocusRole("a", "a")).toBe("target");
  });

  test("SECONDARY: every other item once something is focused", () => {
    expect(deriveFocusRole("b", "a")).toBe("secondary");
    expect(deriveFocusRole("c", "a")).toBe("secondary");
  });

  test("exactly one item can be TARGET for a given focusedId — never two", () => {
    const ids = ["a", "b", "c", "d"];
    const focusedId = "c";
    const roles = ids.map((id) => deriveFocusRole(id, focusedId));
    expect(roles.filter((r) => r === "target")).toHaveLength(1);
    expect(roles.filter((r) => r === "secondary")).toHaveLength(3);
  });

  test("FOCUS_FIELD_VARIANTS has exactly the 3 roles the derivation can produce, no more", () => {
    expect(Object.keys(FOCUS_FIELD_VARIANTS).sort()).toEqual(["idle", "secondary", "target"]);
  });

  test("idle variant is neutral (CALM) — no scale, no dim, no shift", () => {
    expect(FOCUS_FIELD_VARIANTS.idle).toEqual({ scale: 1, y: 0, opacity: 1, filter: "saturate(1)" });
  });

  test("secondary variant dims (RECEDE) but never reaches 0 opacity — never disappears", () => {
    expect(FOCUS_FIELD_VARIANTS.secondary.opacity).toBeGreaterThan(0);
    expect(FOCUS_FIELD_VARIANTS.secondary.opacity).toBeLessThan(1);
  });

  test("target variant is the only one with a position/scale shift (APPROACH)", () => {
    expect(FOCUS_FIELD_VARIANTS.target.scale).toBeGreaterThan(1);
    expect(FOCUS_FIELD_VARIANTS.target.y).toBeLessThan(0);
    expect(FOCUS_FIELD_VARIANTS.idle.scale).toBe(1);
    expect(FOCUS_FIELD_VARIANTS.secondary.scale).toBe(1);
  });
});
