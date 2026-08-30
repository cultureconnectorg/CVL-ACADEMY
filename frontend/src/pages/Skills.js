import { useEffect, useState } from "react";
import { Sparks } from "iconoir-react";
import { toast } from "sonner";
import { api } from "@/lib/api";

const STATE_LABELS = {
  not_started: "Non commencé",
  in_progress: "En cours",
  acquired: "Acquis",
};

export default function Skills() {
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/skills/mine")
      .then((r) => setSkills(r.data))
      .catch(() => toast.error("Impossible de charger tes compétences."))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-10 text-[--cvln-ink-2]">…</div>;

  const byBloc = skills.reduce((acc, s) => {
    const bloc = s.skill.bloc;
    (acc[bloc] = acc[bloc] || []).push(s);
    return acc;
  }, {});

  return (
    <div className="px-6 md:px-12 py-10 max-w-5xl" data-testid="skills-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">Skill Engine</div>
      <h1 className="font-display font-black text-4xl tracking-tighter mt-2">Mes compétences</h1>

      {skills.length === 0 ? (
        <div className="cvln-card p-6 mt-8 text-sm text-[--cvln-ink-2]">
          Aucune compétence référencée pour l&apos;instant — elles apparaissent au fur et à mesure de tes
          modules, quiz et certifications.
        </div>
      ) : (
        Object.entries(byBloc).map(([bloc, list]) => (
          <div key={bloc} className="cvln-card p-6 mt-6" data-testid={`skills-bloc-${bloc}`}>
            <h3 className="font-display font-bold text-xl tracking-tight mb-4 flex items-center gap-2">
              <Sparks width={18} height={18} className="text-[--cvln-orange]" /> Bloc {bloc}
            </h3>
            <div className="space-y-3">
              {list.map((s) => (
                <div key={s.skill.id} className="px-4 py-3 rounded-xl border border-black/5" data-testid={`skill-${s.skill.id}`}>
                  <div className="flex items-center justify-between gap-4">
                    <div className="min-w-0">
                      <div className="text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2]">{s.skill.id}</div>
                      <div className="font-semibold truncate">{s.skill.label}</div>
                    </div>
                    <div
                      className={`text-xs font-bold px-3 py-1 rounded-full whitespace-nowrap
                        ${s.state === "acquired" ? "bg-[--cvln-forest] text-white" : "bg-[--cvln-bg-warm] text-[--cvln-ink-2]"}`}
                    >
                      {STATE_LABELS[s.state]}
                    </div>
                  </div>
                  <div className="stage-line mt-3"><div style={{ width: `${s.progression_pct}%` }} /></div>
                </div>
              ))}
            </div>
          </div>
        ))
      )}
    </div>
  );
}
