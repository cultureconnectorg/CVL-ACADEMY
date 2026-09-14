import {
  formatFrkCompletenessLabel,
  formatFrkPrerequisiteLabel,
} from "@/lib/canonicalFrkDisplay";

describe("canonicalFrkDisplay.js — raccorder ces corpus au même runtime/funnel Academy (2026-09-07)", () => {
  describe("formatFrkCompletenessLabel — must never claim complete when it isn't", () => {
    test("no formation -> unknown status, never a guess", () => {
      expect(formatFrkCompletenessLabel(null)).toBe("Statut inconnu");
    });

    test("fully_complete=true -> explicit complete label", () => {
      expect(
        formatFrkCompletenessLabel({ fully_complete: true, needs_expert_review: false })
      ).toBe("Formation complète");
    });

    test("needs_expert_review=true -> names the real hold, never a generic 'partial'", () => {
      expect(
        formatFrkCompletenessLabel({ fully_complete: false, needs_expert_review: true })
      ).toBe("En attente d'une revue experte réelle avant certification");
    });

    test("neither complete nor expert-review-held -> generic in-construction label", () => {
      expect(
        formatFrkCompletenessLabel({ fully_complete: false, needs_expert_review: false })
      ).toBe("Contenu en construction");
    });
  });

  describe("formatFrkPrerequisiteLabel", () => {
    test("no prerequisites text -> honest 'not specified', never invented", () => {
      expect(formatFrkPrerequisiteLabel(null)).toBe("Prérequis non précisé dans la source");
      expect(formatFrkPrerequisiteLabel("")).toBe("Prérequis non précisé dans la source");
    });

    test("real prerequisites text -> passed through verbatim", () => {
      expect(formatFrkPrerequisiteLabel("FRK-01 (Foundations).")).toBe(
        "Prérequis : FRK-01 (Foundations)."
      );
    });
  });
});
