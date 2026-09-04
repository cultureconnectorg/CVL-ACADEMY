import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import BackButton from "@/components/BackButton";
import { listCanonicalFormations } from "@/lib/canonicalApi";

/**
 * ACA-0006 — read-only list of the canonical FMS métiers, backed by
 * `db.fms_resources` (the real imported archive) through
 * `fms_canonical`'s read model — never `db.formations`'s legacy
 * catalogue. Deliberately minimal presentation (no new design system,
 * mission §13: "pas de nouvelle DA") — reuses the app's existing card/
 * typography classes.
 */
export default function CanonicalFormations() {
  const [formations, setFormations] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    listCanonicalFormations()
      .then(setFormations)
      .catch(() => setError("Impossible de charger les formations canoniques."));
  }, []);

  return (
    <div className="px-6 md:px-12 py-10 max-w-5xl" data-testid="canonical-formations-page">
      <BackButton to="/dashboard" label="Dashboard" testId="back-to-dashboard" />
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange] mt-4">
        Corpus FMS canonique
      </div>
      <h1 className="font-display font-black text-3xl md:text-4xl tracking-tighter leading-none mt-2">
        Les 6 métiers, tels que le référentiel réel les décrit.
      </h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">
        Contenu source : archive FMS canonique. Distinct du parcours historique
        (formations existantes) — voir{" "}
        <Link to="/formations" className="underline">
          Formations
        </Link>{" "}
        pour ce dernier.
      </p>

      {error && <div className="mt-8 text-red-600">{error}</div>}

      {!formations && !error && <div className="mt-8 text-[--cvln-ink-2]">Chargement…</div>}

      {formations && formations.length === 0 && (
        <div className="mt-8 text-[--cvln-ink-2]" data-testid="no-canonical-formations">
          Aucun métier canonique importé pour le moment.
        </div>
      )}

      <div className="mt-8 grid gap-4 sm:grid-cols-2" data-testid="canonical-formations-list">
        {(formations || []).map((f) => (
          <Link
            key={f.canonical_formation_code}
            to={`/canonical/${f.canonical_formation_code}`}
            className="cvln-card p-5 block hover:border-[--cvln-orange]/50"
            data-testid={`canonical-formation-${f.canonical_formation_code}`}
          >
            <div className="text-[11px] mono uppercase tracking-wider font-bold text-[--cvln-orange]">
              {f.canonical_formation_code}
            </div>
            <div className="font-semibold mt-1">{f.metier_name}</div>
            <div className="text-sm text-[--cvln-ink-2] mt-1">
              {f.module_count} module{f.module_count > 1 ? "s" : ""}
              {f.pedagogical_case_title ? ` · Cas : ${f.pedagogical_case_title}` : ""}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
