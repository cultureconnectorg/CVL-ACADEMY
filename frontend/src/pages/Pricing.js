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

function offerLabel(offer) {
  if (offer.billing === "free") return "Accès libre";
  if (offer.billing === "subscription") return "Abonnement";
  if (offer.billing === "per_learner") return "Par apprenant";
  if (offer.commercialization === "contract") return "Contrat";
  return "Offre Academy";
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

  const section = (eyebrow, title, items, note) => items.length > 0 && (
    <section className="mt-10 md:mt-14">
      <div className="cvln-section-heading !mb-5">
        <div>
          <div className="mono text-[10px] font-bold uppercase tracking-[0.24em] text-[--cvln-orange]">{eyebrow}</div>
          <h2 className="!mt-2">{title}</h2>
          {note && <p className="mt-2 max-w-2xl text-sm leading-6 text-[--cvln-ink-2]">{note}</p>}
        </div>
        <span>{items.length} offre{items.length > 1 ? "s" : ""}</span>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {items.map((offer, index) => (
          <article
            key={offer.id}
            className="cvln-glass-panel relative overflow-hidden rounded-[24px] p-6 md:p-7"
            data-testid={`pricing-${offer.id}`}
          >
            <div
              className="pointer-events-none absolute -right-14 -top-16 h-44 w-44 rounded-full opacity-50 blur-3xl"
              style={{ background: index % 2 === 0 ? "rgba(255,122,47,.26)" : "rgba(67,162,215,.18)" }}
            />
            <div className="relative z-10 flex min-h-[250px] flex-col">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="mono text-[10px] font-bold uppercase tracking-[0.22em] text-[--cvln-orange]">
                    {offer.channel || "CVLN Academy"}
                  </div>
                  <div className="mt-2 text-xs uppercase tracking-[0.16em] text-white/45">{offerLabel(offer)}</div>
                </div>
                <div className="rounded-full border border-white/10 bg-white/[.045] px-3 py-1.5 text-[10px] font-bold uppercase tracking-[0.14em] text-white/55">
                  {offer.status}
                </div>
              </div>

              <h3 className="mt-6 font-display text-2xl font-black leading-tight tracking-[-0.03em] text-white">
                {offer.name}
              </h3>
              <div className="mt-5 font-display text-[clamp(28px,4vw,42px)] font-black leading-none tracking-[-0.045em] text-white">
                {priceLine(offer)}
              </div>

              {offer.capacity && (
                <p className="mt-4 text-sm leading-6 text-white/58">
                  Jusqu’à {offer.capacity} apprenants/sièges selon l’offre.
                </p>
              )}

              <div className="mt-auto border-t border-white/10 pt-5 text-[11px] text-white/42">
                {offer.decision_id}
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );

  return (
    <div className="cvln-app-shell min-h-screen text-[--cvln-ink]" data-testid="pricing-page-shell">
      <header className="cvln-topbar !sticky !top-0">
        <Link to="/" className="cvln-wordmark" aria-label="CVLN Academy — Accueil">
          <span className="cvln-wordmark-mark">◒</span>
          <span className="font-display text-sm font-black tracking-[0.16em] text-white md:text-base">
            CVLN <span className="text-[--cvln-orange]">ACADEMY</span>
          </span>
        </Link>
        <nav className="cvln-topnav" aria-label="Navigation tarifs">
          <Link to="/formations">Formations</Link>
          <Link to="/roadmap">Parcours</Link>
          <Link to="/missions">Missions</Link>
          <Link to="/pricing" className="active">Tarifs</Link>
        </nav>
        <div className="flex items-center gap-2">
          <Link to="/login" className="btn-outline text-sm">Se connecter</Link>
          <Link to="/register" className="btn-primary text-sm">Rejoindre</Link>
        </div>
      </header>

      <main className="cvln-page relative z-10" data-testid="pricing-page">
        <section className="cvln-page-hero">
          <div className="relative z-10 max-w-4xl">
            <div className="cvln-kicker text-[--cvln-orange]">Économie 3D · DECIDED V1</div>
            <h1 className="cvln-page-title mt-4">Investir dans ton parcours, pas acheter une page.</h1>
            <p className="cvln-page-subtitle mt-5 !max-w-3xl !text-base md:!text-lg">
              Les formations restent des objets pédagogiques. Les montants ci-dessous correspondent aux offres commerciales qui donnent accès aux parcours, cohortes, évaluations ou contrats — avec les règles Economy 3D comme autorité de prix.
            </p>
            <div className="mt-7 flex flex-wrap gap-3">
              <Link to="/formations" className="btn-primary">Explorer les formations →</Link>
              <Link to="/" className="btn-outline">Retour à l’Academy</Link>
            </div>
          </div>
        </section>

        {error && (
          <div className="cvln-glass-panel mt-8 rounded-2xl p-6 text-sm text-white/72" role="alert">
            {error}
          </div>
        )}
        {!payload && !error && (
          <div className="cvln-glass-panel mt-8 rounded-2xl p-6 text-sm text-white/62">Chargement des offres…</div>
        )}

        {payload && (
          <>
            {section("01 · Individuel", "Offres individuelles", groups.public)}
            {section("02 · Cohortes", "Cohortes intensives", groups.cohort, "Le tarif intensif est exprimé par apprenant.")}
            {section("03 · B2B / B2G", "Entreprises & institutions", groups.contract, "Tarifs contractuels et économie de mission pour organisations, institutions et partenaires.")}
            {section("04 · Horizon", "Licences programmées", groups.future, "Décisions déjà fixées, activation prévue en phase 2 ou 3.")}

            <section className="cvln-glass-panel mt-12 rounded-[24px] p-6 md:p-8">
              <div className="mono text-[10px] font-bold uppercase tracking-[0.22em] text-[--cvln-orange]">Frontière de confiance</div>
              <p className="mt-3 max-w-4xl text-sm leading-7 text-white/62">
                <strong className="text-white">Règle de frontière :</strong> {payload.rules?.price_boundary}. Les claims RNCP, CPF et financement restent soumis à une preuve vérifiée.
              </p>
            </section>
          </>
        )}
      </main>
    </div>
  );
}
