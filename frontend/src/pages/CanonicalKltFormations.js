import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import BackButton from "@/components/BackButton";
import { listCanonicalKltFormations } from "@/lib/canonicalKltApi";
import { formatKltCompletenessLabel } from "@/lib/canonicalKltDisplay";

/**
 * "Branchage complet de Kiltikonet" — read-only list of the 8 canonical
 * KLT formations, backed by `db.klt_resources` (the real docs/klt/ tree)
 * through `klt_canonical`'s read model — never `db.formations`'s legacy
 * catalogue. Mirrors `CanonicalFormations.js` exactly, with one addition
 * required by the Founder (2026-09-04): every card states its real
 * completeness — a `PARTIAL` formation is never shown as if it were
 * `COMPLETE`.
 */
export default function CanonicalKltFormations() {
  const [formations, setFormations] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    listCanonicalKltFormations()
      .then(setFormations)
      .catch(() => setError("Impossible de charger les formations Kiltikonet canoniques."));
  }, []);

  return (
    <div className="px-6 md:px-12 py-10 max-w-5xl" data-testid="canonical-klt-formations-page">
      <BackButton to="/dashboard" label="Dashboard" testId="back-to-dashboard" />
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange] mt-4">
        Corpus Kiltikonet canonique
      </div>
      <h1 className="font-display font-black text-3xl md:text-4xl tracking-tighter leading-none mt-2">
        Les 8 formations, telles que le corpus réel les décrit.
      </h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">
        Contenu source : <code>docs/klt/</code>. Distinct du corpus FMS —
        voir <Link to="/canonical" className="underline">Corpus FMS canonique</Link>{" "}
        pour ce dernier.
      </p>

      {error && <div className="mt-8 text-red-600">{error}</div>}

      {!formations && !error && <div className="mt-8 text-[--cvln-ink-2]">Chargement…</div>}

      {formations && formations.length === 0 && (
        <div className="mt-8 text-[--cvln-ink-2]" data-testid="no-canonical-klt-formations">
          Aucune formation Kiltikonet importée pour le moment.
        </div>
      )}

      <div className="mt-8 grid gap-4 sm:grid-cols-2" data-testid="canonical-klt-formations-list">
        {(formations || []).map((f) => (
          <Link
            key={f.klt_formation_code}
            to={`/kiltikonet-canonical/${f.klt_formation_code}`}
            className="cvln-card p-5 block hover:border-[--cvln-orange]/50"
            data-testid={`canonical-klt-formation-${f.klt_formation_code}`}
          >
            <div className="flex items-center justify-between gap-2">
              <div className="text-[11px] mono uppercase tracking-wider font-bold text-[--cvln-orange]">
                {f.klt_formation_code}
              </div>
              {!f.fully_complete && (
                <span
                  className="text-[10px] uppercase tracking-wider font-bold px-2 py-0.5 rounded bg-amber-100 text-amber-800"
                  data-testid={`canonical-klt-partial-badge-${f.klt_formation_code}`}
                >
                  Partielle
                </span>
              )}
            </div>
            <div className="font-semibold mt-1">{f.title}</div>
            <div className="text-sm text-[--cvln-ink-2] mt-1">
              {f.module_count} module{f.module_count > 1 ? "s" : ""}
              {f.pedagogical_case_title ? ` · Cas : ${f.pedagogical_case_title}` : ""}
            </div>
            <div className="text-xs text-[--cvln-ink-2] mt-1" data-testid={`canonical-klt-completeness-${f.klt_formation_code}`}>
              {formatKltCompletenessLabel(f)}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
