import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";
import { toast } from "sonner";

export default function Missions() {
  const { t } = useI18n();
  const { refreshMe } = useAuth();
  const [missions, setMissions] = useState([]);
  const [mine, setMine] = useState([]);

  const load = async () => {
    const [m, u] = await Promise.all([
      api.get("/missions").then(r => r.data),
      api.get("/missions/mine").then(r => r.data),
    ]);
    setMissions(m); setMine(u);
  };

  useEffect(() => { load(); }, []);

  const status = (code) => mine.find(x => x.mission_code === code)?.status;

  const accept = async (code) => {
    await api.post(`/missions/${code}/accept`);
    toast.success("Mission acceptée. Livre-la pour gagner tes CC.");
    load();
  };
  const submit = async (code) => {
    const { data } = await api.post(`/missions/${code}/submit`);
    toast.success(`+${data.cc_earned} CC — stade actuel : ${data.new_stade}`);
    await refreshMe();
    load();
  };

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="missions-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">{t("missions")}</div>
      <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-2">
        Défis réels. Preuves de compétence.
      </h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">
        {"Chaque mission accomplie génère un signal FREK et alimente une entité concrète de l'écosystème CVLN."}
      </p>

      <div className="mt-10 grid grid-cols-1 md:grid-cols-2 gap-6">
        {missions.map((m) => {
          const s = status(m.code);
          return (
            <div
              key={m.code}
              data-testid={`mission-${m.code}`}
              className="cvln-card p-6 flex flex-col"
            >
              <div className="flex items-center justify-between">
                <div className="text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2]">
                  {m.pole} · {m.entity}
                </div>
                {m.status_type === "urgent" && (
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded-full bg-[#FEE7DF] text-[#7B1D0D]">
                    Urgent
                  </span>
                )}
                {m.status_type === "featured" && (
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded-full bg-[#FFF3D6] text-[#7A4A0E]">
                    À la une
                  </span>
                )}
              </div>
              <h3 className="font-display font-bold text-xl md:text-2xl tracking-tight mt-3">{m.title}</h3>
              <p className="text-sm text-[--cvln-ink-2] mt-2 leading-relaxed">{m.description}</p>

              <div className="mt-5 flex items-center justify-between text-xs mono text-[--cvln-ink-2]">
                <span>Stade min : <strong>{m.stade_required}</strong></span>
                <span className="text-[--cvln-orange] font-bold text-sm">+{m.cc_reward} CC</span>
              </div>

              <div className="mt-4 flex gap-2">
                {!s && (
                  <button
                    data-testid={`accept-${m.code}`}
                    onClick={() => accept(m.code)}
                    className="btn-outline text-sm"
                  >
                    {t("accept_mission")}
                  </button>
                )}
                {s === "accepted" && (
                  <button
                    data-testid={`submit-${m.code}`}
                    onClick={() => submit(m.code)}
                    className="btn-primary text-sm"
                  >
                    {t("submit_mission")}
                  </button>
                )}
                {s === "validated" && (
                  <span className="text-sm text-[--cvln-forest] font-bold">✓ Livrée · CC créditée</span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
