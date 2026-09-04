import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import BackButton from "@/components/BackButton";
import {
  getCanonicalModule,
  getMyCanonicalProgress,
  markCanonicalContentViewed,
} from "@/lib/canonicalApi";
import { deriveModuleActionLabel, formatPrerequisiteLabel } from "@/lib/canonicalDisplay";

/**
 * ACA-0006 — one canonical module, real content only (never a
 * staff-only resource's body — enforced backend-side by
 * `fms_canonical.read_model`). Deliberately does not reuse
 * ModuleJourney's 7-phase shell (mission §4: don't force canonical
 * content into the legacy shape) — this is its own, much simpler view:
 * content, real prerequisite status, real N1/N2/N3 references where the
 * source has them, and the one honest progress signal this pass
 * records (content viewed).
 */
export default function CanonicalModuleView() {
  const { formationCode, moduleCode } = useParams();
  const [module, setModule] = useState(null);
  const [progress, setProgress] = useState(null);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const load = useCallback(() => {
    Promise.all([
      getCanonicalModule(formationCode, moduleCode),
      getMyCanonicalProgress(formationCode),
    ])
      .then(([m, progressList]) => {
        setModule(m);
        setProgress(progressList.find((p) => p.canonical_module_code === moduleCode) || null);
      })
      .catch(() => setError("Module canonique introuvable."));
  }, [formationCode, moduleCode]);

  useEffect(() => {
    load();
  }, [load]);

  const handleMarkViewed = async () => {
    setSaving(true);
    try {
      const updated = await markCanonicalContentViewed(formationCode, moduleCode);
      setProgress(updated);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="px-6 md:px-12 py-10 max-w-3xl" data-testid="canonical-module-page">
      <BackButton
        to={`/canonical/${formationCode}`}
        label={formationCode}
        testId="back-to-canonical-formation"
      />

      {error && <div className="mt-8 text-red-600">{error}</div>}

      {module && (
        <>
          <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange] mt-4">
            {module.canonical_module_code}
          </div>
          <h1 className="font-display font-black text-2xl md:text-3xl tracking-tighter leading-none mt-2">
            {module.title}
          </h1>
          <div className="text-sm text-[--cvln-ink-2] mt-2" data-testid="canonical-prereq-status">
            {formatPrerequisiteLabel(module.prerequisites)}
          </div>

          {module.content_markdown ? (
            <pre
              className="mt-6 whitespace-pre-wrap font-sans text-[15px] leading-relaxed"
              data-testid="canonical-module-content"
            >
              {module.content_markdown}
            </pre>
          ) : (
            <p className="mt-6 text-[--cvln-ink-2]" data-testid="canonical-module-no-content">
              Contenu non encore disponible pour ce module.
            </p>
          )}

          {(module.assessment.n1_reference ||
            module.assessment.n2_reference ||
            module.assessment.n3_reference) && (
            <div className="mt-6 cvln-card p-4 text-sm" data-testid="canonical-assessment-refs">
              {module.assessment.n1_reference && <div>N1 : {module.assessment.n1_reference}</div>}
              {module.assessment.n2_reference && <div>N2 : {module.assessment.n2_reference}</div>}
              {module.assessment.n3_reference && <div>N3 : {module.assessment.n3_reference}</div>}
            </div>
          )}

          <button
            onClick={handleMarkViewed}
            disabled={saving || (progress && progress.content_viewed_at)}
            className="btn-primary text-sm mt-8"
            data-testid="canonical-mark-viewed"
          >
            {deriveModuleActionLabel(progress)}
          </button>
        </>
      )}
    </div>
  );
}
