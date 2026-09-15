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
import ReturnToPositionCard from "@/components/spatial/ReturnToPositionCard.jsx";

const STADE_EMOJI = {
  graine: "🌱", pousse: "🌿", racine: "🌳",
  branches: "🌲", arbre: "🦅", foret: "🌳🌳",
};

// ACA-0027-lite / W-FUNNEL-2 "Retention" (Founder instruction 2026-09-07,
// "Regular Use -> Conversion -> Retention -> Expansion") — `prof.returning`
// is real, server-derived (backend/lifecycle.py's `db.refresh_tokens`-based
// `is_returning_session`, W-FUNNEL-1). One-time-per-browser-session
// (sessionStorage, same conservative pattern as the app's existing
// token/lang storage) so it never nags on every remount within one visit.
const WELCOME_BACK_SESSION_KEY = "cvln_welcome_back_shown";

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
  const [horizonItems, setHorizonItems] = useState([]);

  // FIRST_VALUE = CONTINUOUS_DASHBOARD_REVEAL (Founder decision,
  // W-FUNNEL-2, 2026-09-07) — the real `POST /onboarding/complete`
  // response, carried here via router `state` (see Onboarding.js's
  // `submit()`), becomes a one-time, non-blocking reveal on this exact
  // page. Read once on mount, then the state is cleared from history
  // immediately — a refresh or a later visit never re-triggers it.
  const [reveal] = useState(location.state?.justOnboarded ? location.state.onboardingResult : null);
  useEffect(() => {
    if (location.state?.justOnboarded) {
      nav(location.pathname, { replace: true, state: {} });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // W-FUNNEL-2 "Retention" — see WELCOME_BACK_SESSION_KEY's docstring
  // above. Guarded by `!location.state?.justOnboarded` (not just
  // `!reveal`, fixed at mount) so it can never appear on the same render
  // as the onboarding-completion reveal — never two competing "first
  // moment" surfaces at once.
  const [showWelcomeBack, setShowWelcomeBack] = useState(false);

  useEffect(() => {
    (async () => {
      // refreshMe() used to be awaited before firing the 6 dashboard calls
      // below, serializing a full network round trip in front of them for
      // no reason: none of those endpoints take anything from the fresh
      // `user` object (each is scoped server-side by the auth token via
      // get_current_user), so there is nothing for them to wait on. Firing
      // all 7 together removes that avoidable wait from every Dashboard load.
      const [, p, m, b, s, lp, horizon] = await Promise.all([
        refreshMe(),
        api.get("/frek/profile").then(r => r.data),
        api.get("/missions").then(r => r.data),
        api.get("/badges/mine").then(r => r.data),
        api.get("/progression/summary").then(r => r.data),
        api.get("/user/learning-path").then(r => r.data),
        // ACA-0027 — real, composed "next relevant opportunity" signal
        // (see services/progressive_horizon.py). Fetched alongside the
        // rest, never blocking: an empty/failed response just means no
        // CERTIFICATION_ELIGIBLE card renders below.
        api.get("/progression/horizon").then(r => r.data).catch(() => []),
      ]);
      setProf(p); setMissions(m); setBadges(b); setSummary(s); setPath(lp);
      setHorizonItems(Array.isArray(horizon) ? horizon : []);

      if (p?.returning && !location.state?.justOnboarded) {
        let alreadyShownThisSession = false;
        try {
          alreadyShownThisSession = !!sessionStorage.getItem(WELCOME_BACK_SESSION_KEY);
          if (!alreadyShownThisSession) sessionStorage.setItem(WELCOME_BACK_SESSION_KEY, "1");
        } catch {
          // Storage unavailable (private mode, blocked) — fine to show
          // once this render; simply not deduped across remounts.
        }
        if (!alreadyShownThisSession) setShowWelcomeBack(true);
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const stade = user?.stade || "graine";
  const cc = user?.cc_credits ?? 0;
  const progressPct = prof?.stade_progress_pct ?? 0;
  const firstName = user?.display_name?.split(" ")[0] || "talent";

  // RAIL 3 — additive, flag-gated (default off). Own fetch, not a
  // replacement of the effect above: reads the real pedagogical graph
  // (learning-path/missions/badges/skills/qualifications) and never
  // recomputes any of the numbers already rendered above (summary/
  // path/badges).
  const { graph } = usePedagogicalGraph({ enabled: FEATURE_FLAGS.SPATIAL_HUB_ENABLED });

  return (
    <div className="cvln-page" data-testid="dashboard-page">
      {reveal && <FirstValueReveal result={reveal} user={user} t={t} />}
      {!reveal && showWelcomeBack && (
        <WelcomeBackBanner
          userFirstName={firstName}
          globalPct={summary?.global_pct}
          onDismiss={() => setShowWelcomeBack(false)}
          t={t}
        />
      )}

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

      {/* RAIL 3 — Spatial Hub: the real pedagogical graph, rendered as a
          distance-ordered rail (`lib/spatial/attention.js`, unmodified
          formulas). Replaces the static Next Action banner only while the
          flag is on — doctrine forbids two competing "where do I go next"
          surfaces at once. */}
      {FEATURE_FLAGS.SPATIAL_HUB_ENABLED ? (
        <SpatialHub formationNodes={graph.formationNodes} missionNodes={graph.missionNodes} />
      ) : (
        path?.next_action && (
          <div className="cvln-card p-6 mt-6 relative overflow-hidden" data-testid="next-action-card">
            <div className="absolute inset-y-0 left-0 w-1.5" style={{ background: path.next_action.pole_color }} />
            <div className="flex flex-wrap items-center gap-6">
              <div className="flex-1 min-w-0">
                <div className="text-[10px] mono uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">
                  {/* ACA-0024 (CONTINUATION_ENGINE) — the backend only sets
                      `resume: true` when this module is real, already-touched
                      work being resumed, never a fresh curriculum
                      recommendation. */}
                  {path.next_action.resume ? t("dashboard_p.resume_step") : t("dashboard_p.next_step")}
                </div>
                <div className="font-display font-bold text-2xl md:text-3xl tracking-tight mt-2 leading-tight">{path.next_action.module_name}</div>
                <div className="text-sm text-[--cvln-ink-2] mt-1">{path.next_action.formation_name} · {path.next_action.status}</div>
              </div>
              <Link
                to={path.next_action.route || `/formations/${path.next_action.formation_code}/modules/${path.next_action.module_code}`}
                data-testid="next-action-open"
                className="btn-primary"
              >
                {path.next_action.status === "available" ? t("common.start") : t("common.continue_")}<ArrowRight width={16} height={16} className="ml-2" />
              </Link>
            </div>
          </div>
        )
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

        {/* CAN-01/CAN-02 convergence (P0-G backend) — a distinct, honestly-
            labeled number: canonical FMS/Kiltikonet/KORA content *viewed*,
            never blended into the legacy global_pct above (which means
            quiz-passed + mini-mission-committed — a bar canonical content
            has no mechanism to clear yet). */}
        {summary?.canonical?.canonical_modules_total > 0 && (
          <div className="mt-6 pt-6 border-t border-white/10" data-testid="card-canonical-progress">
            <div className="flex items-center justify-between text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-ink-2]">
              <span>{t("canonical_progress")}</span>
              <span className="text-[--cvln-orange]">{summary.canonical.canonical_progress_pct}%</span>
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

      {/* W-FUNNEL-2 "Expansion" — the same real ELIGIBLE/HORIZON condition
          lifecycleState.js's EXPANDING already derives (own pole fully
          validated + a real unlocked formation exists elsewhere), computed
          directly from path.own_pole/path.other_poles — no new backend
          call, no invented recommendation. */}
      {path && path.own_pole.length > 0 &&
        path.own_pole.every((f) => f.progress_pct >= 100) &&
        path.other_poles.some((f) => f.is_unlocked && f.progress_pct < 100) && (
        <div className="mt-6 cvln-card p-6" data-testid="horizon-card">
          <div className="text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-ink-2]">
            {t("dashboard_p.horizon_eyebrow")}
          </div>
          <h3 className="font-display font-bold text-2xl tracking-tight mt-2">
            {t("dashboard_p.horizon_title")}
          </h3>
          <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {path.other_poles
              .filter((f) => f.is_unlocked && f.progress_pct < 100)
              .slice(0, 3)
              .map((f) => (
                <Link
                  key={f.code}
                  to={`/formations/${f.code}`}
                  data-testid={`horizon-formation-${f.code}`}
                  className="p-4 rounded-2xl border border-white/10 hover:border-[--cvln-orange]/40 transition flex items-center gap-3"
                >
                  <span className="w-2.5 h-10 rounded-full shrink-0" style={{ background: f.pole_color }} />
                  <span className="min-w-0">
                    <span className="block text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2]">
                      {f.pole_name}
                    </span>
                    <span className="block font-semibold truncate">{f.name}</span>
                  </span>
                  <ArrowRight width={16} height={16} className="ml-auto shrink-0 text-[--cvln-ink-2]" />
                </Link>
              ))}
          </div>
        </div>
      )}

      {/* ACA-0027 — Progressive Horizon: real, server-composed
          certification-eligibility signal (services/progressive_horizon.py).
          Distinct from the FORMATION_EXPANSION card above (still driven
          directly by `path`, unchanged) — this one only ever renders an
          item `check_full_eligibility` (the exact same gate `start_attempt`
          itself uses) already confirmed True for. */}
      {horizonItems
        .filter((i) => i.type === "CERTIFICATION_ELIGIBLE")
        .map((item) => (
          <div
            key={item.certification_code}
            className="mt-6 cvln-card p-6"
            data-testid={`cert-opportunity-${item.certification_code}`}
          >
            <div className="text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-ink-2]">
              {t("dashboard_p.cert_opportunity_eyebrow")}
            </div>
            <h3 className="font-display font-bold text-2xl tracking-tight mt-2">
              {t("dashboard_p.cert_opportunity_title")}
            </h3>
            <Link
              to={item.route}
              data-testid={`cert-opportunity-open-${item.certification_code}`}
              className="mt-4 inline-flex items-center gap-2 px-4 py-3 rounded-2xl border border-white/10 hover:border-[--cvln-orange]/40 transition font-semibold"
            >
              <span
                className="w-2.5 h-10 rounded-full shrink-0"
                style={{ background: item.pole_color || "var(--cvln-orange)" }}
              />
              {item.formation_name}
              <ArrowRight width={16} height={16} className="ml-auto shrink-0 text-[--cvln-ink-2]" />
            </Link>
          </div>
        ))}

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

// W-FUNNEL-2 "Retention" — a smaller, less ceremonial sibling of
// FirstValueReveal: it acknowledges a real, server-derived RETURNING
// moment (see WELCOME_BACK_SESSION_KEY above) with a single honest fact
// (real global progress, when it exists), never a duplicate of the "next
// step" resume card rendered elsewhere on this page — no CTA here, just
// acknowledgment.
function WelcomeBackBanner({ userFirstName, globalPct, onDismiss, t }) {
  const [open, setOpen] = useState(true);
  const reduced = useReducedMotion();

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          data-testid="welcome-back-banner"
          initial={reduced ? { opacity: 0 } : { opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          exit={reduced ? { opacity: 0 } : { opacity: 0, y: -8 }}
          transition={{ duration: reduced ? 0.15 : 0.3, ease: [0.16, 1, 0.3, 1] }}
          className="mb-8 rounded-2xl px-5 py-4 bg-[--cvln-bg-warm] border border-black/5 flex items-center justify-between gap-4"
        >
          <div className="text-sm text-[--cvln-ink]">
            <span className="font-semibold">{t("dashboard_p.welcome_back")} {userFirstName}.</span>
            {typeof globalPct === "number" && (
              <span className="text-[--cvln-ink-2]"> {t("dashboard_p.welcome_back_progress_pre")} {globalPct}% {t("dashboard_p.welcome_back_progress_post")}</span>
            )}
          </div>
          <button
            data-testid="welcome-back-banner-close"
            onClick={() => { setOpen(false); onDismiss?.(); }}
            aria-label={t("close")}
            className="w-7 h-7 shrink-0 rounded-full bg-black/5 hover:bg-black/10 flex items-center justify-center text-[--cvln-ink-2]"
          >
            <Xmark width={14} height={14} />
          </button>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

/** FIRST_VALUE = CONTINUOUS_DASHBOARD_REVEAL (Founder decision,
 * W-FUNNEL-2, 2026-09-07) — a one-time, non-blocking, dismissible
 * banner composed entirely from `result`, the real `POST /onboarding/
 * complete` response (never refetched, never fabricated): a
 * recommended formation only when the backend actually named one, a
 * first mission only when one was actually pre-accepted, a badge/
 * signal count only when real. No CC/progression number is invented
 * here — Dashboard's own cards above already show those honestly, from
 * their own already-real sources. */
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
