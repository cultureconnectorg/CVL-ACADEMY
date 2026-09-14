import {
  deriveKltModuleActionLabel,
  formatKltCompletenessLabel,
  formatKltPrerequisiteLabel,
  formatKltSkillStatusLabel,
} from "@/lib/canonicalKltDisplay";

describe("canonicalKltDisplay.js — branchage complet Kiltikonet (2026-09-04)", () => {
  describe("formatKltCompletenessLabel — must never claim complete when it isn't", () => {
    test("fully_complete=true -> explicit complete label", () => {
      expect(
        formatKltCompletenessLabel({
          fully_complete: true,
          built_skill_count: 11,
          skill_count: 11,
          blocked_skill_ids: [],
        })
      ).toBe("Formation complète");
    });

    test("fully_complete=false -> always names the real blocked count, never hidden", () => {
      expect(
        formatKltCompletenessLabel({
          fully_complete: false,
          built_skill_count: 5,
          skill_count: 7,
          blocked_skill_ids: ["KLT06.SKILL.C05", "KLT06.SKILL.C06"],
        })
      ).toBe("Partielle — 5/7 compétences construites, 2 bloquées");
    });

    test("single blocked skill -> singular wording", () => {
      expect(
        formatKltCompletenessLabel({
          fully_complete: false,
          built_skill_count: 6,
          skill_count: 7,
          blocked_skill_ids: ["KLT07.SKILL.C04"],
        })
      ).toBe("Partielle — 6/7 compétences construites, 1 bloquée");
    });

    test("missing formation -> unknown, not a crash", () => {
      expect(formatKltCompletenessLabel(null)).toBe("Statut inconnu");
    });
  });

  describe("formatKltPrerequisiteLabel", () => {
    test("'aucun' (real convention) -> explicit 'no prerequisite'", () => {
      expect(formatKltPrerequisiteLabel("aucun")).toBe("Aucun prérequis");
      expect(formatKltPrerequisiteLabel("Aucun")).toBe("Aucun prérequis");
    });

    test("a real prerequisite string is shown verbatim", () => {
      expect(formatKltPrerequisiteLabel("M01, M02")).toBe("Prérequis : M01, M02");
    });

    test("missing -> honest 'not precised', never a fake lock", () => {
      expect(formatKltPrerequisiteLabel(null)).toBe("Prérequis non précisé dans la source");
    });
  });

  describe("deriveKltModuleActionLabel", () => {
    test("no progress yet -> action label", () => {
      expect(deriveKltModuleActionLabel(null)).toBe("Marquer comme consulté");
    });

    test("already viewed -> reflects that", () => {
      expect(
        deriveKltModuleActionLabel({ content_viewed_at: "2026-09-04T00:00:00Z" })
      ).toBe("Déjà consulté");
    });
  });

  describe("formatKltSkillStatusLabel — the honest BLOCKED surface", () => {
    test("BUILT -> Construite", () => {
      expect(formatKltSkillStatusLabel({ status: "BUILT" })).toBe("Construite");
    });

    test("BLOCKED with a real reason -> shows it, never silently omits", () => {
      expect(
        formatKltSkillStatusLabel({ status: "BLOCKED", blocked_reason: "non construit" })
      ).toBe("Bloquée — non construit");
    });

    test("BLOCKED without a reason string -> still says Bloquée", () => {
      expect(formatKltSkillStatusLabel({ status: "BLOCKED", blocked_reason: null })).toBe(
        "Bloquée"
      );
    });
  });
});
