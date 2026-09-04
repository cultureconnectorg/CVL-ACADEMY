import {
  deriveModuleActionLabel,
  formatAudienceLabel,
  formatPrerequisiteLabel,
} from "@/lib/canonicalDisplay";

describe("canonicalDisplay.js (ACA-0006)", () => {
  describe("formatPrerequisiteLabel — never invents a lock", () => {
    test("NONE -> explicit 'no prerequisite'", () => {
      expect(formatPrerequisiteLabel({ status: "NONE", required_module_codes: [] })).toBe(
        "Aucun prérequis"
      );
    });

    test("DEFINED -> lists the real canonical codes", () => {
      expect(
        formatPrerequisiteLabel({ status: "DEFINED", required_module_codes: ["FMS01-M01"] })
      ).toBe("Prérequis : FMS01-M01");
    });

    test("UNSPECIFIED -> honest 'not precised', never a fake lock", () => {
      expect(
        formatPrerequisiteLabel({ status: "UNSPECIFIED", required_module_codes: [] })
      ).toBe("Prérequis non précisé dans la source");
    });

    test("missing prerequisites object -> unknown, not a crash", () => {
      expect(formatPrerequisiteLabel(null)).toBe("Statut inconnu");
      expect(formatPrerequisiteLabel(undefined)).toBe("Statut inconnu");
    });
  });

  describe("deriveModuleActionLabel — one honest signal only", () => {
    test("no progress yet -> action label", () => {
      expect(deriveModuleActionLabel(null)).toBe("Marquer comme consulté");
      expect(deriveModuleActionLabel({ content_viewed_at: null })).toBe(
        "Marquer comme consulté"
      );
    });

    test("already viewed -> reflects that, never a fabricated 'completed'", () => {
      expect(deriveModuleActionLabel({ content_viewed_at: "2026-09-03T00:00:00Z" })).toBe(
        "Déjà consulté"
      );
    });
  });

  describe("formatAudienceLabel", () => {
    test("joins real audience roles", () => {
      expect(formatAudienceLabel(["TRAINER", "ADMIN"])).toBe("TRAINER, ADMIN");
    });

    test("empty/missing -> explicit 'unclassified', not blank", () => {
      expect(formatAudienceLabel([])).toBe("Non classifié");
      expect(formatAudienceLabel(undefined)).toBe("Non classifié");
    });
  });
});
