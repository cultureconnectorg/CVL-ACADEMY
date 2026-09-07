import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRight, Coins, Medal1st, GraduationCap, Sparks, Xmark } from "iconoir-react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { usePedagogicalGraph } from "@/lib/usePedagogicalGraph";
import SpatialHub from "@/components/SpatialHub";
import { useReducedMotion } from "@/lib/useReducedMotion";

const STADE_EMOJI = {
  graine: "🌱", pousse: "🌿", racine: "🌳",
  branches: "🌲", arbre: "🦅", foret: "🌳🌳",
};

export default function Dashboard() {
  const { user, refreshMe } = useAuth();
  const { t } = useI18n();
  const location = useLocation();
  const nav = useNavigate();
  const [prof, setProf] = useState(null);
  const [missions, setMissions] = useState([]);
  const [badges, setBadges] = useState([]);
  const [summary, setSummary] = useState(null);
  const [path, setPath] = useState(null);

  // FIRST_VALUE = CONTINUOUS_DASHBOARD_REVEAL (Founder decision,
  // W-FUNNEL-2, 2026-09-07) — no separate /activation route: the real
  // `POST /onboarding/complete` response, carried here via router
  // `state` (see Onboarding.js's `submit()`), becomes a one-time,
  // non-blocking reveal on this exact page. Read once on mount, then
  // the state is cleared from history immediately — a refresh or a
  // later visit (even via back button) never re-triggers it, with no
  // new persisted flag needed.
  const [reveal] = useState(location.state?.justOnboarded ? location.state.onboardingResult : null);
  useEffect(() => {
    if (location.state?.justOnboarded) {
      nav(location.pathname, { replace: true, state: {} });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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

  // RAIL 3 — additive, flag-gated (default off = today's behavior
  // byte-for-byte). Own fetch, not a replacement of the effect above:
  // this hook reads the real pedagogical graph (learning-path/missions/
  // badges/skills/qualifications) and never recomputes any of the
  // numbers already rendered above (`summary`, `path`, `badges`).
  const { graph } = usePedagogicalGraph({ enabled: FEATURE_FLAGS.SPATIAL_HUB_ENABLED });

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="dashboard-page">
      {reveal && <FirstValueReveal result={reveal} user={user} t={t} />}

      {/* Hero */}
      <div className="flex flex-wrap items-end justify-between gap-6 mb-10">
        <div>
          <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">
            {t("dashboard")}
          </div>
          <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-2">
            {t("dashboard_p.greeting")} {user?.display_name?.split(" ")[0]}.
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

      {/* RAIL 3 — Spatial Hub: the real pedagogical graph, rendered as
          a distance-ordered rail (`lib/spatial/attention.js`, unmodified
          formulas). Replaces the static Next Action banner only while
          the flag is on — doctrine forbids two competing "where do I go
          next" surfaces at once. */}
      {FEATURE_FLAGS.SPATIAL_HUB_ENABLED ? (
        <SpatialHub formationNodes={graph.formationNodes} missionNodes={graph.missionNodes} />
      ) : (
        path?.next_action && (
        <div className="mb-10 cvln-card p-6 relative overflow-hidden" data-testid="next-action-card">
          <div className="absolute inset-y-0 left-0 w-1.5" style={{ background: path.next_action.pole_color }} />
          <div className="flex flex-wrap items-center gap-6">
            <div className="flex-1 min-w-0">
              <div className="text-[10px] mono uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">
                {t("dashboard_p.next_step")}
              </div>
              <div className="font-display font-bold text-2xl md:text-3xl tracking-tight mt-2 leading-tight">
                {path.next_action.module_name}
              </div>
              <div className="text-sm text-[--cvln-ink-2] mt-1">
                {path.next_action.formation_name} · statut : {path.next_action.status}
              </div>
            </div>
            <Link
              to={path.next_action.route || `/formations/${path.next_action.formation_code}/modules/${path.next_action.module_code}`}
              data-testid="next-action-open"
              className="btn-primary"
            >
              {path.next_action.status === "available" ? t("common.start") : t("common.continue_")}
              <ArrowRight width={16} height={16} className="ml-2" />
            </Link>
          </div>
        </div>
        )
      )}

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
          {/* CAN-01/CAN-02 convergence (P0-G backend, surfaced here) —
              a distinct, honestly-labeled number: canonical FMS/
              Kiltikonet/KORA content *viewed*, never blended into the
              legacy global_pct above, which means quiz-passed +
              mini-mission-committed — a bar canonical content has no
              mechanism to clear yet. */}
          {summary?.canonical?.canonical_modules_total > 0 && (
            <div className="mt-6 pt-6 border-t border-black/5" data-testid="card-canonical-progress">
              <div className="flex items-center justify-between text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-ink-2]">
                <span>{t("canonical_progress")}</span>
                <span className="text-[--cvln-orange]">
                  {summary.canonical.canonical_progress_pct}%
                </span>
              </div>
              <div className="stage-line mt-3">
                <div style={{ width: `${summary.canonical.canonical_progress_pct}%` }} />
              </div>
              <div className="mt-2 text-xs text-[--cvln-ink-2]">
                {summary.canonical.canonical_modules_viewed}/{summary.canonical.canonical_modules_total}{" "}
                {t("canonical_modules_viewed")}
              </div>
              <div className="mt-1 text-[10px] text-[--cvln-ink-2]">
                {t("canonical_progress_hint")}
              </div>
            </div>
          )}
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
            {t("common.see_all")} <ArrowRight width={12} height={12} />
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
            {t("dashboard_p.no_badges")}
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

/** FIRST_VALUE = CONTINUOUS_DASHBOARD_REVEAL (Founder decision,
 * W-FUNNEL-2, 2026-09-07) — a one-time, non-blocking, dismissible
 * banner composed entirely from `result`, the real `POST /onboarding/
 * complete` response (never refetched, never fabricated): a
 * recommended formation only when the backend actually named one, a
 * first mission only when one was actually pre-accepted, a badge/
 * signal count only when real. No CC/progression number is invented
 * here — Dashboard's own cards below already show those honestly,
 * from their own already-real sources. Uses the app's existing motion
 * primitive (`framer-motion`, the same dependency Roadmap.js's spatial
 * rail already uses) — respects prefers-reduced-motion. */
function FirstValueReveal({ result, user, t }) {
  const [open, setOpen] = useState(true);
  const reduced = useReducedMotion();

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          data-testid="first-value-reveal"
          initial={reduced ? { opacity: 0 } : { opacity: 0, y: -16, scale: 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={reduced ? { opacity: 0 } : { opacity: 0, y: -12, scale: 0.98 }}
          transition={{ duration: reduced ? 0.15 : 0.4, ease: [0.16, 1, 0.3, 1] }}
          className="mb-8 cvln-card p-6 relative overflow-hidden border-2 border-[--cvln-orange]/30"
        >
          <button
            data-testid="first-value-reveal-close"
            onClick={() => setOpen(false)}
            aria-label={t("close")}
            className="absolute top-4 right-4 w-8 h-8 rounded-full bg-black/5 hover:bg-black/10 flex items-center justify-center text-[--cvln-ink-2]"
          >
            <Xmark width={16} height={16} />
          </button>

          <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">
            {t("onboarding_p.launched_eyebrow")}
          </div>
          <h2 className="font-display font-black text-2xl md:text-3xl tracking-tight mt-2 pr-10">
            {t("onboarding_p.welcome")} {user?.display_name?.split(" ")[0]}.
          </h2>
          {(result?.signals_emitted?.length > 0 || result?.badge_earned) && (
            <p className="text-[--cvln-ink-2] mt-2 max-w-xl text-sm">
              {result.signals_emitted?.length > 0 && (
                <>{result.signals_emitted.length} {t("onboarding_p.signals_emitted")} </>
              )}
              {result.badge_earned && (
                <>
                  <strong className="text-[--cvln-ink]">{result.badge_earned.name}</strong> {t("onboarding_p.delivered")}
                </>
              )}
            </p>
          )}

          {(result?.recommended_formation || result?.recommended_mission) && (
            <div className="mt-5 grid grid-cols-1 md:grid-cols-2 gap-4">
              {result.recommended_formation && (
                <div className="rounded-2xl border border-black/10 p-4" data-testid="reveal-formation">
                  <div className="text-[10px] mono uppercase tracking-[0.2em] font-bold text-[--cvln-orange]">
                    {t("onboarding_p.recommended_formation")}
                  </div>
                  <div className="font-display font-bold text-lg mt-1">
                    {result.recommended_formation.name}
                  </div>
                  <Link
                    to={`/formations/${result.recommended_formation.code}`}
                    data-testid="reveal-formation-open"
                    className="btn-primary text-sm mt-3 inline-flex"
                  >
                    {t("onboarding_p.open_formation")} <ArrowRight width={14} height={14} className="ml-1.5" />
                  </Link>
                </div>
              )}
              {result.recommended_mission && (
                <div className="rounded-2xl border border-black/10 p-4" data-testid="reveal-mission">
                  <div className="text-[10px] mono uppercase tracking-[0.2em] font-bold text-[--cvln-orange]">
                    {t("onboarding_p.first_mission")}
                  </div>
                  <div className="font-display font-bold text-lg mt-1">
                    {result.recommended_mission.title}
                  </div>
                  <Link to="/missions" data-testid="reveal-mission-open" className="btn-outline text-sm mt-3 inline-flex">
                    {t("onboarding_p.see_my_missions")}
                  </Link>
                </div>
              )}
            </div>
          )}
        </motion.div>
      )}
    </AnimatePresence>
  );
}
