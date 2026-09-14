import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import BackButton from "@/components/BackButton";
import { getCanonicalFormation, listCanonicalModules } from "@/lib/canonicalApi";
import { formatLearnerResourceTypeLabel, formatPrerequisiteLabel } from "@/lib/canonicalDisplay";

/** ACA-0006 — real canonical module list for one métier, ordered exactly
 * as the archive's own Master Module Map — never re-sorted. */
export default function CanonicalFormationDetail() {
  const { formationCode } = useParams();
  const [formation, setFormation] = useState(null);
  const [modules, setModules] = useState(null);
  const [error, setError] = useState(null);
  // ACA-0019 — which learner_resources card (if any) is expanded. At
  // most one open at a time, closed by default: these bodies can be
  // long (a full case study, a template), never dumped on screen
  // unrequested.
  const [openResourceIdx, setOpenResourceIdx] = useState(null);

  useEffect(() => {
    Promise.all([
      getCanonicalFormation(formationCode),
      listCanonicalModules(formationCode),
    ])
      .then(([f, m]) => {
        setFormation(f);
        setModules(m);
      })
      .catch(() => setError("Formation canonique introuvable."));
  }, [formationCode]);

  return (
    <div className="px-6 md:px-12 py-10 max-w-4xl" data-testid="canonical-formation-detail-page">
      <BackButton to="/canonical" label="Corpus FMS canonique" testId="back-to-canonical" />

      {error && <div className="mt-8 text-red-600">{error}</div>}

      {formation && (
        <>
          <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange] mt-4">
            {formation.canonical_formation_code}
          </div>
          <h1 className="font-display font-black text-3xl md:text-4xl tracking-tighter leading-none mt-2">
            {formation.metier_name}
          </h1>
        </>
      )}

      {/* ACA-0019 — real formation-level learner resources (the
          continuing case, blank student templates, the candidate
          guide) — previously parsed and classified LEARNER but never
          served to any surface. Never per-module: the source itself
          doesn't scope these to one module (see the backend model's
          own docstring), so they sit here, above the module list. */}
      {formation && formation.learner_resources && formation.learner_resources.length > 0 && (
        <div className="mt-10" data-testid="canonical-learner-resources">
          <h2 className="font-display font-bold text-xl tracking-tight">Ressources</h2>
          <div className="mt-3 space-y-2">
            {formation.learner_resources.map((res, idx) => {
              const open = openResourceIdx === idx;
              return (
                <div
                  key={`${res.resource_type}-${idx}`}
                  className="cvln-card p-4"
                  data-testid={`canonical-learner-resource-${res.resource_type}`}
                >
                  <button
                    type="button"
                    onClick={() => setOpenResourceIdx(open ? null : idx)}
                    className="w-full flex items-center justify-between gap-4 text-left"
                    aria-expanded={open}
                    data-testid={`canonical-learner-resource-toggle-${res.resource_type}`}
                  >
                    <div>
                      <div className="text-[11px] mono uppercase tracking-wider text-[--cvln-ink-2]">
                        {formatLearnerResourceTypeLabel(res.resource_type)}
                      </div>
                      <div className="font-semibold">{res.title}</div>
                    </div>
                    <span className="text-[--cvln-ink-2] text-sm">{open ? "−" : "+"}</span>
                  </button>
                  {open && (
                    <pre
                      className="mt-4 whitespace-pre-wrap font-sans text-sm leading-relaxed"
                      data-testid={`canonical-learner-resource-content-${res.resource_type}`}
                    >
                      {res.content_markdown}
                    </pre>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      <div className="mt-8 space-y-2" data-testid="canonical-module-list">
        {(modules || []).map((m) => (
          <Link
            key={m.canonical_module_code}
            to={`/canonical/${formationCode}/${m.canonical_module_code}`}
            className="cvln-card p-4 flex items-center justify-between gap-4 hover:border-[--cvln-orange]/50"
            data-testid={`canonical-module-${m.canonical_module_code}`}
          >
            <div>
              <div className="text-[11px] mono uppercase tracking-wider text-[--cvln-ink-2]">
                {m.canonical_module_code}
              </div>
              <div className="font-semibold">{m.title}</div>
              <div className="text-xs text-[--cvln-ink-2] mt-0.5">
                {formatPrerequisiteLabel(m.prerequisites)}
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
