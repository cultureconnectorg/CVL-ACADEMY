import { useEffect, useState } from "react";
import { Building, Community, GraduationCap, PeopleTag } from "iconoir-react";
import { api } from "@/lib/api";

const COPY = {
  partner: {
    eyebrow: "Espace partenaire",
    title: "Pilotage de votre partenariat",
    intro: "Suivez uniquement les cohortes et indicateurs rattachés à votre organisation.",
  },
  institution: {
    eyebrow: "Espace institution",
    title: "Suivi institutionnel",
    intro: "Vue consolidée des cohortes et de l'activité rattachées à votre organisation.",
  },
};

function Metric({ Icon, label, value }) {
  return (
    <div className="cvln-card p-5">
      <Icon width={20} height={20} className="text-[--cvln-orange]" />
      <div className="font-display font-black text-3xl mt-3">{value ?? "—"}</div>
      <div className="text-sm text-[--cvln-ink-2] mt-1">{label}</div>
    </div>
  );
}

export default function StakeholderPortal({ expectedType }) {
  const [context, setContext] = useState(null);
  const [overview, setOverview] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let alive = true;
    Promise.all([api.get("/stakeholders/me"), api.get("/stakeholders/overview")])
      .then(([me, stats]) => {
        if (!alive) return;
        if (me.data.membership?.stakeholder_type !== expectedType) {
          setError("Cet espace ne correspond pas à votre habilitation.");
          return;
        }
        setContext(me.data);
        setOverview(stats.data);
      })
      .catch((err) => {
        if (alive) setError(err?.response?.data?.detail || "Accès non disponible.");
      });
    return () => { alive = false; };
  }, [expectedType]);

  if (error) {
    return <div className="px-6 md:px-12 py-10 max-w-4xl"><div className="cvln-card p-6">{error}</div></div>;
  }
  if (!context || !overview) return null;

  const copy = COPY[expectedType];
  return (
    <div className="px-6 md:px-12 py-10 max-w-6xl" data-testid={`${expectedType}-portal-page`}>
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">{copy.eyebrow}</div>
      <h1 className="font-display font-black text-4xl tracking-tighter mt-2">{copy.title}</h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">{copy.intro}</p>
      <div className="mt-4 text-sm font-semibold">{context.organisation?.name}</div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-8">
        <Metric Icon={Community} label="Cohortes" value={overview.cohort_count} />
        <Metric Icon={GraduationCap} label="Apprenants" value={overview.learner_count} />
        <Metric Icon={PeopleTag} label="Formateurs" value={overview.trainer_count} />
      </div>

      <div className="cvln-card p-6 mt-6">
        <h2 className="font-display font-bold text-xl tracking-tight flex items-center gap-2">
          <Building width={18} height={18} className="text-[--cvln-orange]" /> Cohortes rattachées
        </h2>
        <div className="mt-4 space-y-2">
          {overview.cohorts.length === 0 ? (
            <div className="text-sm text-[--cvln-ink-2]">Aucune cohorte rattachée pour le moment.</div>
          ) : overview.cohorts.map((cohort) => (
            <div key={cohort.id} className="rounded-xl border border-black/5 px-4 py-3 flex flex-wrap items-center justify-between gap-3">
              <div>
                <div className="font-semibold">{cohort.name}</div>
                <div className="text-xs text-[--cvln-ink-2]">{cohort.pole || "Tous pôles"}</div>
              </div>
              <div className="text-xs text-[--cvln-ink-2]">
                {cohort.learner_count} apprenant(s) · {cohort.active_learners} actif(s)
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
