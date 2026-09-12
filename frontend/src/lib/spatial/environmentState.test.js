import { environmentForStade } from "./environmentState";

describe("environmentForStade", () => {
  test("grows monotonically from graine to foret", () => {
    const order = ["graine", "pousse", "racine", "branches", "arbre", "foret"];
    const values = order.map((stade) => environmentForStade(stade));
    for (let i = 1; i < values.length; i += 1) {
      expect(values[i].density).toBeGreaterThan(values[i - 1].density);
      expect(values[i].growth).toBeGreaterThan(values[i - 1].growth);
    }
  });

  test("fails safe to graine for an unknown stade", () => {
    expect(environmentForStade("unknown")).toMatchObject({ stade: "graine", density: 0.18 });
  });
});
