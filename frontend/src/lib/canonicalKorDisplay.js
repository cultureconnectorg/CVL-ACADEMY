/**
 * Pure display logic for the canonical KORA pages — same rationale as
 * `canonicalKltDisplay.js`: never let a UI surface imply a formation is
 * complete when `fully_complete` is false. KORA's own registry carries
 * no BUILT/BLOCKED column (unlike Kiltikonet), so the label reads
 * differently — see `kor_canonical/read_model.py`'s docstring for the
 * real invariant behind `unresolved_skill_ids`.
 */

export function formatKorCompletenessLabel(formation) {
  if (!formation) return "Statut inconnu";
  if (formation.fully_complete) return "Formation complète";
  const unresolvedCount = (formation.unresolved_skill_ids || []).length;
  if (unresolvedCount === 0) {
    return "Pas encore de compétence enregistrée pour cette formation";
  }
  return `Contenu partiel — ${unresolvedCount} compétence${unresolvedCount > 1 ? "s" : ""} sans module correspondant importé`;
}

export function formatKorPrerequisiteLabel(prerequisitesRaw) {
  if (!prerequisitesRaw) return "Prérequis non précisé dans la source";
  const normalized = prerequisitesRaw.trim().toLowerCase();
  if (normalized === "aucun" || normalized === "aucun.") return "Aucun prérequis";
  return `Prérequis : ${prerequisitesRaw}`;
}

export function deriveKorModuleActionLabel(progress) {
  if (progress && progress.content_viewed_at) {
    return "Déjà consulté";
  }
  return "Marquer comme consulté";
}
