/**
 * Pure display logic for the canonical Kiltikonet pages — same rationale
 * as `canonicalDisplay.js`. The one function this file exists for:
 * never let a UI surface imply a formation is complete when
 * `fully_complete` is false — the exact invariant the Founder required
 * be locked structurally (2026-09-04), now carried into the runtime UI.
 */

export function formatKltCompletenessLabel(formation) {
  if (!formation) return "Statut inconnu";
  if (formation.fully_complete) return "Formation complète";
  const blockedCount = (formation.blocked_skill_ids || []).length;
  return `Partielle — ${formation.built_skill_count}/${formation.skill_count} compétences construites, ${blockedCount} bloquée${blockedCount > 1 ? "s" : ""}`;
}

export function formatKltPrerequisiteLabel(prerequisitesRaw) {
  if (!prerequisitesRaw) return "Prérequis non précisé dans la source";
  const normalized = prerequisitesRaw.trim().toLowerCase();
  if (normalized === "aucun" || normalized === "aucun.") return "Aucun prérequis";
  return `Prérequis : ${prerequisitesRaw}`;
}

export function deriveKltModuleActionLabel(progress) {
  if (progress && progress.content_viewed_at) {
    return "Déjà consulté";
  }
  return "Marquer comme consulté";
}

export function formatKltSkillStatusLabel(skill) {
  if (!skill) return "";
  if (skill.status === "BLOCKED") {
    return skill.blocked_reason ? `Bloquée — ${skill.blocked_reason}` : "Bloquée";
  }
  return "Construite";
}
