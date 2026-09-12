import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Coins, Medal1st, GraduationCap, Sparks } from "iconoir-react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";
import ReturnToPositionCard from "@/components/spatial/ReturnToPositionCard.jsx";

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
  const [path, setPath] = useState(null);

  useEffect(() => {
    (async () => {
      await refreshMe();
      const [p, m, b, s, lp] = await Promise.all([
        api.get("/frek/profile").then(r => r.data),
        api.get("/missions").then(r => r.data),
        api.get("/badges/mine").then(r => r.data),
        api.get("/progression/summary").then(r => r.data),
        api.get("/user/learning-path").then(r => r.data),
      ]);
      setProf(p); setMissions(m); setBadges(b); setSummary(s); setPath(lp);
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const stade = user?.stade || "graine";
  const cc = user?.cc_credits ?? 0;
  const progressPct = prof?.stade_progress_pct ?? 0;
  const firstName = user?.display_name?.split(" ")[0] || "talent";

  return (
    <div className="cvln-page" data-testid="dashboard-page">
      <section className="cvln-page-hero">
        <div className="cvln-kicker">03. DASHBOARD / LE HUB CENTRAL</div>
        <div className="mt-4 flex flex-wrap items-end justify-between gap-6 relative z-10">
          <div>
            <h1 className="cvln-page-title">Bonjour,<br/>{firstName}.</h1>
            <p className="cvln-page-subtitle">
              Le calme est une force. Aujourd’hui, avance sur ce qui compte vraiment. Stade actuel : {STADE_EMOJI[stade]} {t(`stades.${stade}`)}.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <Link to="/roadmap" className="btn-outline" data-testid="cta-roadmap">{t("view_roadmap")}</Link>
            <Link to="/formations" className="btn-primary" data-testid="cta-formations">
              {t("view_formations")}<ArrowRight width={18} height={18} className="ml-2" />
            </Link>
          </div>
        </div>
      </section>

      <div className="cvln-kpi-grid">
        <Link to="/formations" className="cvln-kpi" data-testid="card-global-progress">
          <small>Mes formations</small>
          <strong>{summary?.global_pct ?? 0}%</strong>
          <span className="text-xs text-[--cvln-ink-2] mt-2 block">{summary?.completed_modules ?? 0}/{summary?.total_modules ?? 0} modules validés</span>
        </Link>
        <Link to="/missions" className="cvln-kpi" data-testid="card-missions-summary">
          <small>Mes missions</small>
          <strong>{missions.length}</strong>
          <span className="text-xs text-[--cvln-ink-2] mt-2 block">Opportunités disponibles</span>
        </Link>
        <Link to="/badges" className="cvln-kpi" data-testid="card-badges">
          <small>Mes badges</small>
          <strong>{badges.length}</strong>
          <span className="text-xs text-[--cvln-ink-2] mt-2 block">Preuves obtenues</span>
        </Link>
        <Link to="/wallet" className="cvln-kpi" data-testid="card-cc">
          <small>Mon wallet</small>
          <strong>{cc}</strong>
          <span className="text-xs text-[--cvln-ink-2] mt-2 block">CC disponibles</span>
        </Link>
      </div>

      <ReturnToPositionCard user={user} />

      {path?.next_action && (
        <div className="cvln-card p-6 mt-6 relative overflow-hidden" data-testid="next-action-card">
          <div className="absolute inset-y-0 left-0 w-1.5" style={{ background: path.next_action.pole_color }} />
          <div className="flex flex-wrap items-center gap-6">
            <div className="flex-1 min-w-0">
              <div className="text-[10px] mono uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">Reprendre ma formation</div>
              <div className="font-display font-bold text-2xl md:text-3xl tracking-tight mt-2 leading-tight">{path.next_action.module_name}</div>
              <div className="text-sm text-[--cvln-ink-2] mt-1">{path.next_action.formation_name} · {path.next_action.status}</div>
            </div>
            <Link to={`/formations/${path.next_action.formation_code}/modules/${path.next_action.module_code}`} data-testid="next-action-open" className="btn-primary">
              {path.next_action.status === "available" ? t("common.start") : t("common.continue_")}<ArrowRight width={16} height={16} className="ml-2" />
            </Link>
          </div>
        </div>
      )}

      <div className="cvln-section-heading">
        <h2>Ton parcours. Un futur sans limites.</h2>
        <span>{stade.toUpperCase()} · {progressPct}% vers {t(`stades.${nextStade(stade)}`)}</span>
      </div>

      <div className="cvln-card p-6 relative overflow-hidden">
        <div className="flex items-end gap-3">
          <div className="font-display font-black text-6xl tracking-tighter leading-none text-[--cvln-orange]">{summary?.global_pct ?? 0}<span className="text-2xl align-top">%</span></div>
          <div className="text-sm text-[--cvln-ink-2] pb-2">progression globale</div>
        </div>
        <div className="stage-line mt-6"><div style={{ width: `${summary?.global_pct ?? 0}%` }} /></div>
        <div className="mt-6 grid grid-cols-3 md:grid-cols-6 gap-2">
          {["graine","pousse","racine","branches","arbre","foret"].map((s) => (
            <div key={s} className={`text-center py-3 rounded-xl text-xs border ${s === stade ? "bg-[--cvln-orange]/15 text-white border-[--cvln-orange]/40 font-semibold" : "bg-white/5 text-[--cvln-ink-2] border-white/10"}`}>
              {STADE_EMOJI[s]}<div className="text-[10px] uppercase tracking-wider mt-1">{t(`stades.${s}`)}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
        <div className="cvln-card p-6 lg:col-span-2" data-testid="card-missions">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-display font-bold text-2xl tracking-tight">{t("next_missions")}</h3>
            <Link to="/missions" className="text-sm text-[--cvln-ink-2] hover:text-[--cvln-orange]">{t("missions")} →</Link>
          </div>
          <div className="space-y-3">
            {missions.slice(0, 4).map((m) => (
              <Link to="/missions" key={m.code} data-testid={`mission-preview-${m.code}`} className="flex items-center justify-between gap-4 px-4 py-3 rounded-xl border border-white/10 bg-white/[0.025] hover:border-[--cvln-orange]/50 transition">
                <div className="min-w-0">
                  <div className="text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2]">{m.pole} · {m.entity}</div>
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
              <li key={k} className="flex items-center justify-between px-2 py-1.5 rounded-lg hover:bg-white/5">
                <span className="text-[--cvln-ink-2]">{k}</span><span className="font-bold">{user?.signals?.[k] ?? 0}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="cvln-card p-6 mt-6" data-testid="card-latest-badges">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-display font-bold text-2xl tracking-tight">{t("latest_badges")}</h3>
          <GraduationCap width={18} height={18} className="text-[--cvln-orange]" />
        </div>
        {badges.length === 0 ? (
          <div className="text-sm text-[--cvln-ink-2]">{t("dashboard_p.no_badges")}</div>
        ) : (
          <div className="flex flex-wrap gap-4">
            {badges.slice(0, 8).map((b) => (
              <div key={b.code} className="flex flex-col items-center w-24 text-center">
                <div className="w-16 h-16 rounded-full flex items-center justify-center text-white text-xl font-black border border-white/10" style={{ background: b.color }}>✦</div>
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
