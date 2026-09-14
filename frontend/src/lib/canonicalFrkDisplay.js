/**
 * Pure display logic for the canonical FREK pages — same rationale as
 * `canonicalKorDisplay.js`/`canonicalKltDisplay.js`: never let a UI
 * surface imply a formation is complete when `fully_complete` is
 * false, and never hide a real `NEEDS_EXPERT_REVIEW` hold behind a
 * generic "partial" label.
 */

export function formatFrkCompletenessLabel(formation) {
  if (!formation) return "Statut inconnu";
  if (formation.fully_complete) return "Formation complète";
  if (formation.needs_expert_review) {
    return "En attente d'une revue experte réelle avant certification";
  }
  return "Contenu en construction";
}

export function formatFrkPrerequisiteLabel(prerequisites) {
  if (!prerequisites) return "Prérequis non précisé dans la source";
  return `Prérequis : ${prerequisites}`;
}
