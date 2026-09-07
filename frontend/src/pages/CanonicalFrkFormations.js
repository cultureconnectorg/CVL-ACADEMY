import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import BackButton from "@/components/BackButton";
import { listCanonicalFrkFormations } from "@/lib/canonicalFrkApi";
import { formatFrkCompletenessLabel } from "@/lib/canonicalFrkDisplay";

/**
 * "raccorder ces corpus au même runtime/funnel Academy" (Founder,
 * 2026-09-07) — read-only list of the canonical FREK formations,
 * backed by `db.frk_resources` (the real docs/frk/ tree) through
 * `frk_canonical`'s read model — never `db.formations`'s legacy
 * catalogue. Mirrors `CanonicalKorFormations.js`, with the same
 * non-negotiable: a partial formation is never shown as if it were
 * complete.
 */
export default function CanonicalFrkFormations() {
  const [formations, setFormations] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    listCanonicalFrkFormations()
      .then(setFormations)
      .catch(() => setError("Impossible de charger les formations FREK canoniques."));
  }, []);

  return (
    <div className="px-6 md:px-12 py-10 max-w-5xl" data-testid="canonical-frk-formations-page">
      <BackButton to="/dashboard" label="Dashboard" testId="back-to-dashboard" />
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange] mt-4">
        Corpus FREK canonique
      </div>
      <h1 className="font-display font-black text-3xl md:text-4xl tracking-tighter leading-none mt-2">
        FREK — confiance et provenance culturelle, telles que le corpus réel les décrit.
      </h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">
        Contenu source : <code>docs/frk/</code>. Distinct des corpus FMS,
        Kiltikonet et KORA — <Link to="/canonical" className="underline">FMS</Link>{" "}
        · <Link to="/kiltikonet-canonical" className="underline">Kiltikonet</Link>{" "}
        · <Link to="/kora-canonical" className="underline">KORA</Link>.
      </p>

      {error && <div className="mt-8 text-red-600">{error}</div>}

      {!formations && !error && <div className="mt-8 text-[--cvln-ink-2]">Chargement…</div>}

      {formations && formations.length === 0 && (
        <div className="mt-8 text-[--cvln-ink-2]" data-testid="no-canonical-frk-formations">
          Aucune formation FREK importée pour le moment.
        </div>
      )}

      <div className="mt-8 grid gap-4 sm:grid-cols-2" data-testid="canonical-frk-formations-list">
        {(formations || []).map((f) => (
          <Link
            key={f.frk_formation_code}
            to={`/frek-canonical/${f.frk_formation_code}`}
            className="cvln-card p-5 block hover:border-[--cvln-orange]/50"
            data-testid={`canonical-frk-formation-${f.frk_formation_code}`}
          >
            <div className="flex items-center justify-between gap-2">
              <div className="text-[11px] mono uppercase tracking-wider font-bold text-[--cvln-orange]">
                {f.frk_formation_code}
              </div>
              {!f.fully_complete && (
                <span
                  className="text-[10px] uppercase tracking-wider font-bold px-2 py-0.5 rounded bg-amber-100 text-amber-800"
                  data-testid={`canonical-frk-partial-badge-${f.frk_formation_code}`}
                >
                  {f.needs_expert_review ? "Revue experte" : "Partielle"}
                </span>
              )}
            </div>
            <div className="font-semibold mt-1">{f.title}</div>
            <div className="text-sm text-[--cvln-ink-2] mt-1">
              {f.module_count} module{f.module_count > 1 ? "s" : ""}
            </div>
            <div className="text-xs text-[--cvln-ink-2] mt-1" data-testid={`canonical-frk-completeness-${f.frk_formation_code}`}>
              {formatFrkCompletenessLabel(f)}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
