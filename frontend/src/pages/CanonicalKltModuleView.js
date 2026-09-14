import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import BackButton from "@/components/BackButton";
import {
  getCanonicalKltModule,
  getMyCanonicalKltProgress,
  markCanonicalKltContentViewed,
} from "@/lib/canonicalKltApi";
import { deriveKltModuleActionLabel, formatKltPrerequisiteLabel } from "@/lib/canonicalKltDisplay";

/**
 * "Branchage complet de Kiltikonet" — one canonical KLT module, real
 * content only (never a staff-only resource's body — enforced backend-
 * side by `klt_canonical.read_model`, `is_learner_facing`). Mirrors
 * `CanonicalModuleView.js`'s own minimal shell (mission: don't force
 * canonical content into the legacy 7-phase shape).
 */
export default function CanonicalKltModuleView() {
  const { formationCode, moduleCode } = useParams();
  const [module, setModule] = useState(null);
  const [progress, setProgress] = useState(null);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const load = useCallback(() => {
    Promise.all([
      getCanonicalKltModule(formationCode, moduleCode),
      getMyCanonicalKltProgress(formationCode),
    ])
      .then(([m, progressList]) => {
        setModule(m);
        setProgress(progressList.find((p) => p.module_code === moduleCode) || null);
      })
      .catch(() => setError("Module Kiltikonet canonique introuvable."));
  }, [formationCode, moduleCode]);

  useEffect(() => {
    load();
  }, [load]);

  const handleMarkViewed = async () => {
    setSaving(true);
    try {
      const updated = await markCanonicalKltContentViewed(formationCode, moduleCode);
      setProgress(updated);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="px-6 md:px-12 py-10 max-w-3xl" data-testid="canonical-klt-module-page">
      <BackButton
        to={`/kiltikonet-canonical/${formationCode}`}
        label={formationCode}
        testId="back-to-canonical-klt-formation"
      />

      {error && <div className="mt-8 text-red-600">{error}</div>}

      {module && (
        <>
          <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange] mt-4">
            {module.module_code}
            {module.competency_id ? ` · ${module.competency_id}` : ""}
          </div>
          <h1 className="font-display font-black text-2xl md:text-3xl tracking-tighter leading-none mt-2">
            {module.title}
          </h1>
          <div className="text-sm text-[--cvln-ink-2] mt-2" data-testid="canonical-klt-prereq-status">
            {formatKltPrerequisiteLabel(module.prerequisites_raw)}
          </div>

          {module.kiltikonet_dependency && (
            <div
              className="mt-4 cvln-card p-4 text-sm"
              data-testid="canonical-klt-dependency"
            >
              <span className="font-semibold">Dépendance Kiltikonet : </span>
              {module.kiltikonet_dependency}
            </div>
          )}

          {module.content_markdown ? (
            <pre
              className="mt-6 whitespace-pre-wrap font-sans text-[15px] leading-relaxed"
              data-testid="canonical-klt-module-content"
            >
              {module.content_markdown}
            </pre>
          ) : (
            <p className="mt-6 text-[--cvln-ink-2]" data-testid="canonical-klt-module-no-content">
              Contenu non encore disponible pour ce module.
            </p>
          )}

          <button
            onClick={handleMarkViewed}
            disabled={saving || (progress && progress.content_viewed_at)}
            className="btn-primary text-sm mt-8"
            data-testid="canonical-klt-mark-viewed"
          >
            {deriveKltModuleActionLabel(progress)}
          </button>
        </>
      )}
    </div>
  );
}
