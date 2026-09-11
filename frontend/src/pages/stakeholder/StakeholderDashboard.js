import { useEffect, useMemo, useState } from "react";
import { GraduationCap, PeopleTag, ShieldCheck } from "iconoir-react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";

const roleLabel = {
  partner: "Partenaire",
  institution: "Institution / financeur",
};

function Stat({ label, value, Icon }) {
  return (
    <div className="cvln-card p-5">
      <div className="flex items-center justify-between gap-4">
        <div>
          <div className="text-xs uppercase tracking-[0.18em] text-[--cvln-ink-2] font-semibold">{label}</div>
          <div className="font-display font-black text-3xl mt-2">{value ?? 0}</div>
        </div>
        <Icon width={24} height={24} className="text-[--cvln-orange]" />
      </div>
    </div>
  );
}

export default function StakeholderDashboard() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    api.get("/stakeholders/overview")
      .then(({ data: payload }) => {
        if (!alive) return;
        setData(payload);
        setError(null);
      })
      .catch((err) => {
        if (!alive) return;
        setError(err?.response?.data?.detail || "Impossible de charger cet espace.");
      })
      .finally(() => alive && setLoading(false));
    return () => { alive = false; };
  }, []);

  const title = roleLabel[user?.role] || "Partenaire CVLN";
  const membersByCohort = useMemo(() => {
    if (!data?.cohorts) return [];
    return data.cohorts.map((cohort) => ({
      ...cohort,
      member_count: cohort.member_count || 0,
    }));
  }, [data]);

  if (loading) {
    return <div className="px-6 md:px-12 py-10 text-[--cvln-ink-2]">Chargement de l’espace…</div>;
  }

  if (error) {
    return (
      <div className="px-6 md:px-12 py-10 max-w-4xl" data-testid="stakeholder-dashboard-error">
        <div className="cvln-card p-6 border border-red-200">
          <div className="font-display font-bold text-xl">Espace indisponible</div>
          <p className="text-sm text-[--cvln-ink-2] mt-2">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="px-6 md:px-12 py-10 max-w-6xl" data-testid="stakeholder-dashboard-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">Espace sécurisé</div>
      <div className="flex flex-wrap items-end justify-between gap-4 mt-2">
        <div>
          <h1 className="font-display font-black text-4xl tracking-tighter">{title}</h1>
          <p className="text-[--cvln-ink-2] mt-2">
            {data?.organisation?.name} · visibilité limitée à votre organisation
          </p>
        </div>
        <div className="text-xs px-3 py-2 rounded-full bg-[--cvln-bg-warm] font-semibold">
          Périmètre : organisation
        </div>
      </div>

      <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4 mt-8">
        <Stat label="Apprenants" value={data?.counts?.students} Icon={GraduationCap} />
        <Stat label="Formateurs" value={data?.counts?.trainers} Icon={PeopleTag} />
        <Stat label="Cohortes" value={data?.counts?.cohorts} Icon={ShieldCheck} />
        <Stat label="Membres rattachés" value={data?.counts?.members} Icon={PeopleTag} />
      </div>

      <section className="cvln-card p-6 mt-6">
        <div className="flex items-center justify-between gap-4 mb-4">
          <div>
            <h2 className="font-display font-bold text-xl tracking-tight">Cohortes rattachées</h2>
            <p className="text-sm text-[--cvln-ink-2] mt-1">Lecture opérationnelle des groupes liés à votre organisation.</p>
          </div>
        </div>

        {membersByCohort.length === 0 ? (
          <div className="text-sm text-[--cvln-ink-2]">Aucune cohorte rattachée pour le moment.</div>
        ) : (
          <div className="grid md:grid-cols-2 gap-3">
            {membersByCohort.map((cohort) => (
              <div key={cohort.id} className="rounded-2xl border border-black/10 p-4" data-testid={`stakeholder-cohort-${cohort.id}`}>
                <div className="font-semibold">{cohort.name}</div>
                <div className="text-sm text-[--cvln-ink-2] mt-1">
                  {cohort.pole ? `${cohort.pole} · ` : ""}{cohort.member_count} membre(s)
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="cvln-card p-6 mt-6 overflow-x-auto">
        <h2 className="font-display font-bold text-xl tracking-tight">Population rattachée</h2>
        <p className="text-sm text-[--cvln-ink-2] mt-1 mb-4">
          Données minimales de suivi. Les contenus pédagogiques privés, résultats détaillés et données wallet ne sont pas exposés ici.
        </p>
        <table className="w-full text-sm min-w-[620px]">
          <thead>
            <tr className="text-left border-b border-black/10 text-[--cvln-ink-2]">
              <th className="py-3 pr-4 font-semibold">Nom</th>
              <th className="py-3 pr-4 font-semibold">Rôle</th>
              <th className="py-3 pr-4 font-semibold">Onboarding</th>
              <th className="py-3 font-semibold">Email vérifié</th>
            </tr>
          </thead>
          <tbody>
            {(data?.members || []).map((member) => (
              <tr key={member.id} className="border-b border-black/5">
                <td className="py-3 pr-4 font-medium">{member.display_name}</td>
                <td className="py-3 pr-4">{member.role}</td>
                <td className="py-3 pr-4">{member.onboarding_completed ? "Oui" : "Non"}</td>
                <td className="py-3">{member.email_verified ? "Oui" : "Non"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
