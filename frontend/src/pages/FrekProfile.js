import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";

export default function FrekProfile() {
  const { user } = useAuth();
  const { t } = useI18n();
  const [prof, setProf] = useState(null);

  useEffect(() => {
    api.get("/frek/profile").then(r => setProf(r.data));
  }, []);

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="frek-profile-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">{t("frek_profile")}</div>
      <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-2">
        Identité culturelle souveraine.
      </h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">
        Ton FREK-ID capture chaque compétence, chaque livrable et chaque signal — horodaté, immuable, portable.
      </p>

      {/* Identity card */}
      <div className="mt-10 cvln-card p-8 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-40 h-40 rounded-full bg-[--cvln-orange]/10 -translate-y-8 translate-x-8" />
        <div className="relative z-10 grid md:grid-cols-3 gap-6 items-center">
          <div className="md:col-span-2">
            <div className="text-[11px] mono uppercase tracking-[0.25em] text-[--cvln-ink-2] font-bold">
              FrekCore · Sovereign identity
            </div>
            <div className="mono font-black text-4xl md:text-5xl tracking-tight mt-2">{user?.frek_id}</div>
            <div className="text-lg mt-1">{user?.display_name}</div>
            <div className="text-sm text-[--cvln-ink-2] mt-1">{user?.email}</div>
            <div className="mt-4 flex flex-wrap gap-2">
              <span className="stade-chip">Stade : {t(`stades.${user?.stade}`)}</span>
              <span className="stade-chip">{user?.cc_credits} CC</span>
              <span className="stade-chip">Lang : {user?.lang?.toUpperCase()}</span>
            </div>
          </div>
          <div className="text-right">
            <div className="text-xs text-[--cvln-ink-2] mono">
              Stade next à <strong>{prof?.stade_next_at}</strong> CC
            </div>
            <div className="stage-line mt-2">
              <div style={{ width: `${prof?.stade_progress_pct ?? 0}%` }} />
            </div>
            <div className="mt-1 text-xs text-[--cvln-ink-2] mono">
              {prof?.stade_progress_pct ?? 0}% du stade en cours
            </div>
          </div>
        </div>
      </div>

      {/* Signals grid */}
      <div className="mt-8 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {[
          { k: "FREK-TIME", desc: "Temps investi sur les modules" },
          { k: "FREK-WORK", desc: "Livrables produits et archivés" },
          { k: "FREK-SCORE", desc: "Quiz validés à ≥80%" },
          { k: "FREK-LINK", desc: "Collaborations avec des pairs" },
          { k: "FREK-CERT", desc: "Certifications / badges obtenus" },
          { k: "FREK-CONTRIB", desc: "Contributions à l'écosystème" },
          { k: "FREK-MISSION", desc: "Missions CVLN acceptées" },
          { k: "FREK-SHARE", desc: "Partages publics" },
        ].map((s) => (
          <div key={s.k} className="cvln-card p-5" data-testid={`signal-${s.k}`}>
            <div className="mono text-xs text-[--cvln-orange] font-bold">{s.k}</div>
            <div className="font-display font-black text-3xl tracking-tighter mt-1">
              {user?.signals?.[s.k] ?? 0}
            </div>
            <div className="text-xs text-[--cvln-ink-2] mt-2">{s.desc}</div>
          </div>
        ))}
      </div>

      {/* Signal log */}
      <div className="mt-8 cvln-card p-6">
        <h3 className="font-display font-bold text-2xl tracking-tight mb-4">Journal FREK</h3>
        {(prof?.recent_signals ?? []).length === 0 ? (
          <div className="text-sm text-[--cvln-ink-2]">
            {"Aucun signal émis pour l'instant. Complète un module ou une mission pour commencer à alimenter ton FREK-ID."}
          </div>
        ) : (
          <div className="space-y-1 mono text-sm">
            {(prof.recent_signals || []).map((s, i) => (
              <div key={i} className="flex items-center justify-between px-2 py-1.5 rounded-lg hover:bg-[--cvln-bg-warm]">
                <span className="text-[--cvln-orange] font-bold">{s.signal}</span>
                <span className="text-[--cvln-ink-2] truncate max-w-[50%]">
                  {s.meta?.module || s.meta?.mission || s.meta?.reason || "—"}
                </span>
                <span className="text-[--cvln-ink-2] text-xs">
                  {new Date(s.ts).toLocaleString()}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
