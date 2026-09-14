import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import BackButton from "@/components/BackButton";
import {
  getCanonicalKorModule,
  getMyCanonicalKorProgress,
  markCanonicalKorContentViewed,
} from "@/lib/canonicalKorApi";
import { deriveKorModuleActionLabel, formatKorPrerequisiteLabel } from "@/lib/canonicalKorDisplay";

/**
 * RAIL 2 — one canonical KOR module, real content only (never a
 * staff-only resource's body — enforced backend-side by
 * `kor_canonical.read_model`, `is_learner_facing`). Mirrors
 * `CanonicalKltModuleView.js`'s minimal shell (mission: don't force
 * canonical content into the legacy 7-phase shape).
 */
export default function CanonicalKorModuleView() {
  const { formationCode, moduleCode } = useParams();
  const [module, setModule] = useState(null);
  const [progress, setProgress] = useState(null);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const load = useCallback(() => {
    Promise.all([
      getCanonicalKorModule(formationCode, moduleCode),
      getMyCanonicalKorProgress(formationCode),
    ])
      .then(([m, progressList]) => {
        setModule(m);
        setProgress(progressList.find((p) => p.module_code === moduleCode) || null);
      })
      .catch(() => setError("Module KORA canonique introuvable."));
  }, [formationCode, moduleCode]);

  useEffect(() => {
    load();
  }, [load]);

  const handleMarkViewed = async () => {
    setSaving(true);
    try {
      const updated = await markCanonicalKorContentViewed(formationCode, moduleCode);
      setProgress(updated);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="px-6 md:px-12 py-10 max-w-3xl" data-testid="canonical-kor-module-page">
      <BackButton
        to={`/kora-canonical/${formationCode}`}
        label={formationCode}
        testId="back-to-canonical-kor-formation"
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
          <div className="text-sm text-[--cvln-ink-2] mt-2" data-testid="canonical-kor-prereq-status">
            {formatKorPrerequisiteLabel(module.prerequisites_raw)}
          </div>

          {module.kora_dependency && (
            <div
              className="mt-4 cvln-card p-4 text-sm"
              data-testid="canonical-kor-dependency"
            >
              <span className="font-semibold">Dépendance KORA : </span>
              {module.kora_dependency}
            </div>
          )}

          {module.content_markdown ? (
            <pre
              className="mt-6 whitespace-pre-wrap font-sans text-[15px] leading-relaxed"
              data-testid="canonical-kor-module-content"
            >
              {module.content_markdown}
            </pre>
          ) : (
            <p className="mt-6 text-[--cvln-ink-2]" data-testid="canonical-kor-module-no-content">
              Contenu non encore disponible pour ce module.
            </p>
          )}

          <button
            onClick={handleMarkViewed}
            disabled={saving || (progress && progress.content_viewed_at)}
            className="btn-primary text-sm mt-8"
            data-testid="canonical-kor-mark-viewed"
          >
            {deriveKorModuleActionLabel(progress)}
          </button>
        </>
      )}
    </div>
  );
}
