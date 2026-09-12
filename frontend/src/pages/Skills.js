import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Sparks } from "iconoir-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";

export default function Skills() {
  const { t } = useI18n();
  const { user } = useAuth();
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);

  const STATE_LABELS = {
    not_started: t("skills_p.state_not_started"),
    in_progress: t("skills_p.state_in_progress"),
    acquired: t("skills_p.state_acquired"),
  };

  useEffect(() => {
    setLoading(true);
    api
      .get(user ? "/skills/mine" : "/skills")
      .then((r) => setSkills(r.data))
      .catch(() => toast.error(t("skills_p.load_error")))
      .finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  if (loading) return <div className="p-10 text-[--cvln-ink-2]">…</div>;

  const byBloc = skills.reduce((acc, entry) => {
    const skill = user ? entry.skill : entry;
    const bloc = skill.bloc;
    (acc[bloc] = acc[bloc] || []).push(entry);
    return acc;
  }, {});

  return (
    <div className="px-6 md:px-12 py-10 max-w-5xl" data-testid="skills-page" data-public={!user ? "true" : "false"}>
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">Skill Engine</div>
      <h1 className="font-display font-black text-4xl tracking-tighter mt-2">{t("skills_p.title")}</h1>
      {!user && (
        <>
          <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">Le registre public présente les compétences structurées par l’Academy. La progression, les preuves et l’état acquis restent personnels et ne sont chargés qu’après connexion.</p>
          <div className="mt-5 flex flex-wrap gap-3"><Link to="/register" className="btn-primary">Construire mon profil de compétences</Link><Link to="/certifications" className="btn-outline">Voir les certifications</Link></div>
        </>
      )}

      {skills.length === 0 ? (
        <div className="cvln-card p-6 mt-8 text-sm text-[--cvln-ink-2]">{user ? t("skills_p.empty") : "Le registre public ne contient actuellement aucune compétence publiée."}</div>
      ) : (
        Object.entries(byBloc).map(([bloc, list]) => (
          <div key={bloc} className="cvln-card p-6 mt-6" data-testid={`skills-bloc-${bloc}`}>
            <h3 className="font-display font-bold text-xl tracking-tight mb-4 flex items-center gap-2"><Sparks width={18} height={18} className="text-[--cvln-orange]" /> {t("skills_p.bloc")} {bloc}</h3>
            <div className="space-y-3">
              {list.map((entry) => {
                const skill = user ? entry.skill : entry;
                return (
                  <div key={skill.id} className="px-4 py-3 rounded-xl border border-black/5" data-testid={`skill-${skill.id}`}>
                    <div className="flex items-center justify-between gap-4">
                      <div className="min-w-0">
                        <div className="text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2]">{skill.id} · {skill.metier} · {skill.niveau}</div>
                        <div className="font-semibold truncate">{skill.label}</div>
                      </div>
                      {user ? (
                        <div className={`text-xs font-bold px-3 py-1 rounded-full whitespace-nowrap ${entry.state === "acquired" ? "bg-[--cvln-forest] text-white" : "bg-[--cvln-bg-warm] text-[--cvln-ink-2]"}`}>{STATE_LABELS[entry.state]}</div>
                      ) : (
                        <div className="text-xs font-bold px-3 py-1 rounded-full whitespace-nowrap bg-[--cvln-bg-warm] text-[--cvln-ink-2]">Référentiel public</div>
                      )}
                    </div>
                    {user && <div className="stage-line mt-3"><div style={{ width: `${entry.progression_pct}%` }} /></div>}
                  </div>
                );
              })}
            </div>
          </div>
        ))
      )}
    </div>
  );
}
