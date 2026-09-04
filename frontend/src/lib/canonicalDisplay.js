/**
 * ACA-0006 — pure display logic for the canonical FMS pages. Kept as
 * plain functions, separate from the React components that render them,
 * so this is genuinely unit-testable the same way the rest of this
 * repo's frontend logic is (see e.g. CvlnFocusField.js's
 * `deriveFocusRole`) — no `@testing-library/react` (or any component
 * render harness) is installed in this project, so a real Jest
 * regression for a new surface here means testing its pure logic, not
 * a rendered DOM.
 */

/** Never invents a lock — mirrors backend/fms_canonical's own
 * DEFINED/NONE/UNSPECIFIED, once for display. */
export function formatPrerequisiteLabel(prerequisites) {
  if (!prerequisites) return "Statut inconnu";
  switch (prerequisites.status) {
    case "NONE":
      return "Aucun prérequis";
    case "DEFINED":
      return `Prérequis : ${prerequisites.required_module_codes.join(", ")}`;
    case "UNSPECIFIED":
    default:
      return "Prérequis non précisé dans la source";
  }
}

/** The one real progress signal this pass records — never a fabricated
 * "completed" state. */
export function deriveModuleActionLabel(progress) {
  if (progress && progress.content_viewed_at) {
    return "Déjà consulté";
  }
  return "Marquer comme consulté";
}

export function formatAudienceLabel(audience) {
  if (!audience || audience.length === 0) return "Non classifié";
  return audience.join(", ");
}
