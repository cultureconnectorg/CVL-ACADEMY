import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import BackButton from "@/components/BackButton";
import { getCanonicalFormation, listCanonicalModules } from "@/lib/canonicalApi";
import { formatPrerequisiteLabel } from "@/lib/canonicalDisplay";

/** ACA-0006 — real canonical module list for one métier, ordered exactly
 * as the archive's own Master Module Map — never re-sorted. */
export default function CanonicalFormationDetail() {
  const { formationCode } = useParams();
  const [formation, setFormation] = useState(null);
  const [modules, setModules] = useState(null);
  const [error, setError] = useState(null);

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
