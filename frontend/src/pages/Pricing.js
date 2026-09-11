import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "@/lib/api";

const eur = new Intl.NumberFormat("fr-FR", {
  style: "currency",
  currency: "EUR",
  maximumFractionDigits: 2,
});

function priceLine(offer) {
  if (offer.billing === "free") return "Gratuit";
  if (offer.billing === "subscription") {
    return `${eur.format(offer.monthly_eur)}/mois · ${eur.format(offer.annual_or_unit_eur)}/an`;
  }
  if (offer.billing === "per_learner") return `${eur.format(offer.annual_or_unit_eur)} / apprenant`;
  if (offer.billing === "12_percent_gmv_minimum") return `12 % GMV · minimum ${eur.format(offer.minimum_eur)}`;
  if (offer.billing === "annual_contract_plus_setup") {
    return `${eur.format(offer.annual_or_unit_eur)}/an + ${eur.format(offer.setup_eur)} setup`;
  }
  if (offer.billing === "annual_contract") return `${eur.format(offer.annual_or_unit_eur)}/an`;
  return eur.format(offer.annual_or_unit_eur || 0);
}

export default function Pricing() {
  const [payload, setPayload] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/economy/offers")
      .then(({ data }) => setPayload(data))
      .catch(() => setError("Les tarifs sont momentanément indisponibles."));
  }, []);

  const groups = useMemo(() => {
    const result = { public: [], cohort: [], contract: [], future: [] };
    for (const offer of payload?.items || []) {
      if (offer.status === "DECIDED_PHASE_2" || offer.status === "DECIDED_PHASE_3") {
        result.future.push(offer);
      } else if (offer.commercialization === "public") {
        result.public.push(offer);
      } else if (offer.commercialization === "cohort") {
        result.cohort.push(offer);
      } else {
        result.contract.push(offer);
      }
    }
    return result;
  }, [payload]);

  const section = (title, items, note) => items.length > 0 && (
    <section className="mt-12">
      <div className="flex items-end justify-between gap-6 mb-5">
        <div>
          <h2 className="font-display font-black text-2xl tracking-tight">{title}</h2>
          {note && <p className="text-sm text-[--cvln-ink-2] mt-1">{note}</p>}
        </div>
      </div>
      <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
        {items.map((offer) => (
          <article key={offer.id} className="cvln-card p-6" data-testid={`pricing-${offer.id}`}>
            <div className="text-[11px] mono uppercase tracking-[0.2em] text-[--cvln-orange] font-bold">
              {offer.channel}
            </div>
            <h3 className="font-display font-black text-xl mt-2">{offer.name}</h3>
            <div className="font-display font-black text-3xl mt-4 tracking-tight">{priceLine(offer)}</div>
            {offer.capacity && <p className="text-sm text-[--cvln-ink-2] mt-2">Jusqu’à {offer.capacity} apprenants/sièges selon l’offre.</p>}
            <div className="text-xs text-[--cvln-ink-2] mt-5">{offer.decision_id} · {offer.status}</div>
          </article>
        ))}
      </div>
    </section>
  );

  return (
    <div className="min-h-screen noise">
      <header className="border-b border-black/5 bg-white/70 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-6 md:px-12 py-5 flex items-center justify-between">
          <Link to="/" className="font-display font-black text-lg">CVLN <span className="text-[--cvln-orange]">Academy</span></Link>
          <Link to="/" className="text-sm font-semibold text-[--cvln-ink-2] hover:text-[--cvln-orange]">Accueil</Link>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-6 md:px-12 py-12 md:py-16" data-testid="pricing-page">
        <div className="max-w-3xl">
          <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">Économie 3D · DECIDED V1</div>
          <h1 className="font-display font-black text-4xl md:text-6xl tracking-tighter mt-3">Tarifs CVLN Academy</h1>
          <p className="text-lg text-[--cvln-ink-2] mt-5 leading-relaxed">
            Les formations sont des objets pédagogiques. Les montants ci-dessous sont les prix des offres commerciales qui donnent accès aux parcours, cohortes, évaluations ou contrats — pas un prix arbitraire attaché à chaque formation.
          </p>
        </div>

        {error && <div className="cvln-card p-6 mt-8 text-sm">{error}</div>}
        {!payload && !error && <div className="mt-8 text-[--cvln-ink-2]">Chargement…</div>}
        {payload && (
          <>
            {section("Offres individuelles", groups.public)}
            {section("Cohortes intensives", groups.cohort, "Le tarif intensive est par apprenant.")}
            {section("Entreprises & institutions", groups.contract, "Tarifs contractuels B2B/B2G et économie de mission.")}
            {section("Licences programmées", groups.future, "Décisions déjà fixées, activation prévue en phase 2 ou 3.")}
            <div className="mt-12 cvln-card p-6 text-sm text-[--cvln-ink-2]">
              <strong className="text-[--cvln-ink]">Règle de frontière :</strong> {payload.rules?.price_boundary}. Les claims RNCP/CPF/financement restent soumis à une preuve vérifiée.
            </div>
          </>
        )}
      </main>
    </div>
  );
}
