import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Coins, Medal1st, GraduationCap, Sparks } from "iconoir-react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";

const STADE_EMOJI = {
  graine: "🌱", pousse: "🌿", racine: "🌳",
  branches: "🌲", arbre: "🦅", foret: "🌳🌳",
};

export default function Dashboard() {
  const { user, refreshMe } = useAuth();
  const { t } = useI18n();
  const [prof, setProf] = useState(null);
  const [missions, setMissions] = useState([]);
  const [badges, setBadges] = useState([]);
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    (async () => {
      await refreshMe();
      const [p, m, b, s] = await Promise.all([
        api.get("/frek/profile").then(r => r.data),
        api.get("/missions").then(r => r.data),
        api.get("/badges/mine").then(r => r.data),
        api.get("/progression/summary").then(r => r.data),
      ]);
      setProf(p); setMissions(m); setBadges(b); setSummary(s);
    })();
  }, []);

  const stade = user?.stade || "graine";
  const cc = user?.cc_credits ?? 0;
  const progressPct = prof?.stade_progress_pct ?? 0;

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="dashboard-page">
      {/* Hero */}
      <div className="flex flex-wrap items-end justify-between gap-6 mb-10">
        <div>
          <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">
            {t("dashboard")}
          </div>
          <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-2">
            Bonjour {user?.display_name?.split(" ")[0]}.
          </h1>
          <p className="text-[--cvln-ink-2] mt-3 max-w-lg">
            {t("current_stage")} : <strong className="text-[--cvln-ink]">
              {STADE_EMOJI[stade]} {t(`stades.${stade}`)}
            </strong>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link to="/roadmap" className="btn-outline" data-testid="cta-roadmap">
            {t("view_roadmap")}
          </Link>
          <Link to="/formations" className="btn-primary" data-testid="cta-formations">
            {t("view_formations")}
            <ArrowRight width={18} height={18} className="ml-2" />
          </Link>
        </div>
      </div>

      {/* North star + KPI bento */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 md:gap-6">
        {/* Global progression card */}
        <div className="cvln-card p-6 md:col-span-2 relative overflow-hidden" data-testid="card-global-progress">
          <div className="absolute top-4 right-4 text-[10px] mono uppercase tracking-[0.2em] text-[--cvln-ink-2]">
            {stade.toUpperCase()}
          </div>
          <div className="text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-ink-2]">
            {t("global_progress")}
          </div>
          <div className="mt-4 flex items-end gap-3">
            <div className="font-display font-black text-6xl tracking-tighter leading-none text-[--cvln-orange]">
              {summary?.global_pct ?? 0}<span className="text-2xl align-top">%</span>
            </div>
            <div className="text-sm text-[--cvln-ink-2] pb-2">
              {summary?.completed_modules ?? 0}/{summary?.total_modules ?? 0} modules
            </div>
          </div>
          <div className="stage-line mt-6"><div style={{ width: `${summary?.global_pct ?? 0}%` }} /></div>
          <div className="mt-6 grid grid-cols-6 gap-2">
            {["graine","pousse","racine","branches","arbre","foret"].map((s) => (
              <div key={s} className={`text-center py-2 rounded-lg text-xs
                ${s === stade ? "bg-[--cvln-forest] text-white font-semibold" : "bg-[--cvln-bg-warm] text-[--cvln-ink-2]"}`}>
                {STADE_EMOJI[s]}
                <div className="text-[10px] uppercase tracking-wider mt-1">{t(`stades.${s}`)}</div>
              </div>
            ))}
          </div>
        </div>

        {/* CC + stage progress */}
        <div className="cvln-card p-6" data-testid="card-cc">
          <div className="flex items-center justify-between">
            <div className="text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-ink-2]">{t("cc_credits")}</div>
            <Coins width={18} height={18} className="text-[--cvln-orange]" />
          </div>
          <div className="mt-2 font-display font-black text-5xl tracking-tighter leading-none">{cc}</div>
          <div className="mt-2 text-xs text-[--cvln-ink-2]">
            {progressPct}% vers {t(`stades.${nextStade(stade)}`)}
          </div>
          <div className="stage-line mt-3"><div style={{ width: `${progressPct}%` }} /></div>
        </div>

        {/* Badges */}
        <div className="cvln-card p-6" data-testid="card-badges">
          <div className="flex items-center justify-between">
            <div className="text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-ink-2]">{t("badges_won")}</div>
            <Medal1st width={18} height={18} className="text-[--cvln-orange]" />
          </div>
          <div className="mt-2 font-display font-black text-5xl tracking-tighter leading-none">{badges.length}</div>
          <Link to="/badges" className="mt-3 text-xs text-[--cvln-orange] font-semibold inline-flex items-center gap-1">
            Voir tout <ArrowRight width={12} height={12} />
          </Link>
        </div>
      </div>

      {/* Featured missions + Signals */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
        <div className="cvln-card p-6 lg:col-span-2" data-testid="card-missions">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-display font-bold text-2xl tracking-tight">{t("next_missions")}</h3>
            <Link to="/missions" className="text-sm text-[--cvln-ink-2] hover:text-[--cvln-orange]">
              {t("missions")} →
            </Link>
          </div>
          <div className="space-y-3">
            {missions.slice(0, 4).map((m) => (
              <Link
                to="/missions" key={m.code}
                data-testid={`mission-preview-${m.code}`}
                className="flex items-center justify-between gap-4 px-4 py-3 rounded-xl border border-black/5 hover:border-[--cvln-orange]/50 hover:bg-[--cvln-bg-warm] transition"
              >
                <div className="min-w-0">
                  <div className="text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2]">
                    {m.pole} · {m.entity}
                  </div>
                  <div className="font-semibold truncate">{m.title}</div>
                </div>
                <div className="text-sm font-bold text-[--cvln-orange] whitespace-nowrap">+{m.cc_reward} CC</div>
              </Link>
            ))}
          </div>
        </div>

        <div className="cvln-card p-6" data-testid="card-signals">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-display font-bold text-2xl tracking-tight">{t("signal_activity")}</h3>
            <Sparks width={18} height={18} className="text-[--cvln-orange]" />
          </div>
          <ul className="space-y-2 mono text-sm">
            {["FREK-TIME","FREK-WORK","FREK-SCORE","FREK-LINK","FREK-CERT","FREK-CONTRIB"].map((k) => (
              <li key={k} className="flex items-center justify-between px-2 py-1.5 rounded-lg hover:bg-[--cvln-bg-warm]">
                <span className="text-[--cvln-ink-2]">{k}</span>
                <span className="font-bold">{user?.signals?.[k] ?? 0}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Latest badges */}
      <div className="cvln-card p-6 mt-6" data-testid="card-latest-badges">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-display font-bold text-2xl tracking-tight">{t("latest_badges")}</h3>
          <GraduationCap width={18} height={18} className="text-[--cvln-orange]" />
        </div>
        {badges.length === 0 ? (
          <div className="text-sm text-[--cvln-ink-2]">
            {"Aucun badge pour l'instant. Complète un module ou une mission pour en gagner."}
          </div>
        ) : (
          <div className="flex flex-wrap gap-4">
            {badges.slice(0, 8).map((b) => (
              <div key={b.code} className="flex flex-col items-center w-24 text-center">
                <div
                  className="w-16 h-16 rounded-full flex items-center justify-center text-white text-xl font-black"
                  style={{ background: b.color }}
                >
                  ✦
                </div>
                <div className="text-xs mt-2 font-semibold">{b.name}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function nextStade(s) {
  const order = ["graine","pousse","racine","branches","arbre","foret"];
  const i = order.indexOf(s);
  return order[Math.min(i + 1, order.length - 1)];
}
