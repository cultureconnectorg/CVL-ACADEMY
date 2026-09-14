import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import BackButton from "@/components/BackButton";
import { getCanonicalFrkFormation, listCanonicalFrkModules } from "@/lib/canonicalFrkApi";
import { formatFrkCompletenessLabel } from "@/lib/canonicalFrkDisplay";

/** "raccorder ces corpus au même runtime/funnel Academy" — one FREK
 * formation's real objectives/prerequisites/assessment summary (parsed
 * straight from its own `REFERENTIAL.md`, never re-authored here) plus
 * its real module list. Unlike KOR/KLT, FRK's real corpus carries no
 * separate skill registry — see `frk_canonical/models.py`'s own
 * docstring for why this page has no "unresolved skills" section. */
export default function CanonicalFrkFormationDetail() {
  const { formationCode } = useParams();
  const [formation, setFormation] = useState(null);
  const [modules, setModules] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([
      getCanonicalFrkFormation(formationCode),
      listCanonicalFrkModules(formationCode),
    ])
      .then(([f, m]) => {
        setFormation(f);
        setModules(m);
      })
      .catch(() => setError("Formation FREK canonique introuvable."));
  }, [formationCode]);

  return (
    <div className="px-6 md:px-12 py-10 max-w-4xl" data-testid="canonical-frk-formation-detail-page">
      <BackButton to="/frek-canonical" label="Corpus FREK canonique" testId="back-to-canonical-frk" />

      {error && <div className="mt-8 text-red-600">{error}</div>}

      {formation && (
        <>
          <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange] mt-4">
            {formation.frk_formation_code}
          </div>
          <h1 className="font-display font-black text-3xl md:text-4xl tracking-tighter leading-none mt-2">
            {formation.title}
          </h1>
          <div className="text-sm mt-2" data-testid="canonical-frk-completeness-detail">
            {formatFrkCompletenessLabel(formation)}
          </div>

          {formation.prerequisites && (
            <p className="text-sm text-[--cvln-ink-2] mt-4 max-w-2xl">
              <strong className="text-[--cvln-ink]">Prérequis — </strong>
              {formation.prerequisites}
            </p>
          )}
          {formation.objectives && (
            <p className="text-sm text-[--cvln-ink-2] mt-3 max-w-2xl">
              <strong className="text-[--cvln-ink]">Objectifs — </strong>
              {formation.objectives}
            </p>
          )}
          {formation.assessment_summary && (
            <p className="text-sm text-[--cvln-ink-2] mt-3 max-w-2xl">
              <strong className="text-[--cvln-ink]">Évaluation — </strong>
              {formation.assessment_summary}
            </p>
          )}
        </>
      )}

      <div className="mt-8 space-y-2" data-testid="canonical-frk-module-list">
        {(modules || []).map((m) => (
          <Link
            key={m.module_code}
            to={`/frek-canonical/${formationCode}/${m.module_code}`}
            className="cvln-card p-4 flex items-center justify-between gap-4 hover:border-[--cvln-orange]/50"
            data-testid={`canonical-frk-module-${m.module_code}`}
          >
            <div className="min-w-0">
              <div className="text-[11px] mono uppercase tracking-wider text-[--cvln-ink-2]">
                {m.module_code}
              </div>
              <div className="font-semibold">{m.title}</div>
            </div>
          </Link>
        ))}
        {modules && modules.length === 0 && (
          <div className="text-sm text-[--cvln-ink-2]" data-testid="canonical-frk-no-modules">
            Aucun module au format canonique importé pour cette formation.
          </div>
        )}
      </div>
    </div>
  );
}
