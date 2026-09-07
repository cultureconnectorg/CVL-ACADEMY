import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import BackButton from "@/components/BackButton";
import {
  getCanonicalFrkModule,
  getMyCanonicalFrkProgress,
  markCanonicalFrkContentViewed,
} from "@/lib/canonicalFrkApi";

/**
 * "raccorder ces corpus au même runtime/funnel Academy" — one canonical
 * FRK module, real content only (never a staff-only resource's body —
 * enforced backend-side by `frk_canonical.read_model`,
 * `is_learner_facing`). This module's text is a real, verbatim
 * decomposition of its formation's own `REFERENTIAL.md` "## Modules"
 * item — never a separate authored file (unlike KOR/KLT), see
 * `frk_canonical/models.py`'s own docstring.
 */
export default function CanonicalFrkModuleView() {
  const { formationCode, moduleCode } = useParams();
  const [module, setModule] = useState(null);
  const [progress, setProgress] = useState(null);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const load = useCallback(() => {
    Promise.all([
      getCanonicalFrkModule(formationCode, moduleCode),
      getMyCanonicalFrkProgress(formationCode),
    ])
      .then(([m, progressList]) => {
        setModule(m);
        setProgress(progressList.find((p) => p.module_code === moduleCode) || null);
      })
      .catch(() => setError("Module FREK canonique introuvable."));
  }, [formationCode, moduleCode]);

  useEffect(() => {
    load();
  }, [load]);

  const handleMarkViewed = async () => {
    setSaving(true);
    try {
      const updated = await markCanonicalFrkContentViewed(formationCode, moduleCode);
      setProgress(updated);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="px-6 md:px-12 py-10 max-w-3xl" data-testid="canonical-frk-module-page">
      <BackButton
        to={`/frek-canonical/${formationCode}`}
        label={formationCode}
        testId="back-to-canonical-frk-formation"
      />

      {error && <div className="mt-8 text-red-600">{error}</div>}

      {module && (
        <>
          <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange] mt-4">
            {module.module_code}
          </div>
          <h1 className="font-display font-black text-2xl md:text-3xl tracking-tighter leading-none mt-2">
            {module.title}
          </h1>

          {module.content_markdown ? (
            <p
              className="mt-6 text-[15px] leading-relaxed"
              data-testid="canonical-frk-module-content"
            >
              {module.content_markdown}
            </p>
          ) : (
            <p className="mt-6 text-[--cvln-ink-2]" data-testid="canonical-frk-module-no-content">
              Contenu non encore disponible pour ce module.
            </p>
          )}

          <button
            onClick={handleMarkViewed}
            disabled={saving || (progress && progress.content_viewed_at)}
            className="btn-primary text-sm mt-8"
            data-testid="canonical-frk-mark-viewed"
          >
            {progress && progress.content_viewed_at ? "Déjà consulté" : "Marquer comme consulté"}
          </button>
        </>
      )}
    </div>
  );
}
