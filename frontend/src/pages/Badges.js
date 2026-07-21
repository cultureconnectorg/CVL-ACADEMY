import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";

export default function Badges() {
  const { user } = useAuth();
  const { t } = useI18n();
  const [all, setAll] = useState([]);
  const [mine, setMine] = useState([]);

  useEffect(() => {
    Promise.all([
      api.get("/badges").then(r => r.data),
      api.get("/badges/mine").then(r => r.data),
    ]).then(([a, m]) => { setAll(a); setMine(m); });
  }, []);

  const earned = new Set(mine.map(b => b.code));

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="badges-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">{t("badges")}</div>
      <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-2">
        Preuves publiques, portables.
      </h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">
        {"Chaque badge est un signal d'appartenance CVLN et une compétence prouvée, valable dans tout l'écosystème et au-delà."}
      </p>

      <div className="mt-10 grid grid-cols-2 md:grid-cols-4 gap-6">
        {all.map((b) => {
          const owned = earned.has(b.code);
          const reachable = (user?.cc_credits ?? 0) >= b.cc_threshold;
          return (
            <div
              key={b.code}
              data-testid={`badge-${b.code}`}
              className={`cvln-card p-6 flex flex-col items-center text-center transition
                ${owned ? "" : "opacity-70"}`}
            >
              <div
                className={`w-28 h-28 rounded-full flex items-center justify-center text-white text-4xl font-black relative
                  ${owned ? "shadow-lg" : "grayscale opacity-70"}`}
                style={{ background: b.color }}
              >
                ✦
                {owned && (
                  <div className="absolute -bottom-1 -right-1 bg-[--cvln-forest] text-white text-[10px] font-bold px-2 py-0.5 rounded-full">
                    Obtenu
                  </div>
                )}
              </div>
              <div className="font-display font-bold text-lg tracking-tight mt-4">{b.name}</div>
              <div className="text-xs mono uppercase tracking-wider text-[--cvln-ink-2] mt-1">
                {b.tier} · {b.cc_threshold} CC
              </div>
              <div className="text-xs text-[--cvln-ink-2] mt-3">{b.description}</div>
              {!owned && (
                <div className="mt-3 text-xs font-semibold text-[--cvln-orange]">
                  {reachable ? "Débloqué au prochain rafraîchissement" : `${b.cc_threshold - (user?.cc_credits ?? 0)} CC restants`}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
