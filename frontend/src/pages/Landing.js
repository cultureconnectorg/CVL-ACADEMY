import { useEffect, useState } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { Leaf, ArrowRight } from "iconoir-react";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n, LANGS } from "@/lib/i18n.jsx";
import { toast } from "sonner";
import { Focus, Enter, Reveal } from "@/lib/motion-primitives";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { useReducedMotion } from "@/lib/useReducedMotion";

// ACA-0010 ("Hero/Entry — world entry, not SaaS landing",
// docs/ACADEMY_HERO_ENTRY_RESEARCH.md §8-9) — the storyboard's four
// beats compressed for a real, usable product rather than the
// illustrative 0-60s cinematic timing: VOID is near-instant (a signal,
// not a wait), WORLD/FOCUS resolve within ~1s so a visitor is never
// blocked from acting. What's preserved from the research is the
// *sequencing* itself (world before identity gets primary weight),
// which is the actual acceptance criterion (§16.1), not the exact
// timing of an illustrative storyboard.
const HERO_BEATS = { world: 80, focus: 420, identity: 760 };
const HERO_SESSION_KEY = "cvln_academy_hero_played";

/** Stage reached once, on a real first visit within this browser
 * session — a returning visitor (same tab, back button, or a second
 * `/` hit after a redirect) lands on the settled end-state immediately
 * rather than replaying VOID→WORLD→FOCUS→IDENTITY (research §16.4:
 * "a returning visitor never replays VOID/SIGNAL"). This is a
 * `sessionStorage` best-effort, not the full RETURN_TO_POSITION
 * mechanism (that's an authenticated-route concern, ACA-0023) — Landing
 * itself carries no "position" to return to. */
function alreadyPlayedThisSession() {
  try {
    return sessionStorage.getItem(HERO_SESSION_KEY) === "1";
  } catch {
    return false; // storage blocked (private mode, etc.) — treat as first visit
  }
}

function markPlayed() {
  try {
    sessionStorage.setItem(HERO_SESSION_KEY, "1");
  } catch {
    // best-effort only — a visitor replaying the (harmless, <1s) sequence
    // once more is not a functional regression
  }
}

/** VOID → WORLD → FOCUS → IDENTITY, gated by SPATIAL_HERO_ENTRY and
 * collapsed instantly under reduced motion or a same-session replay —
 * both paths reach the exact same end state (research §16.5), never a
 * different one. Off (flag disabled, reduced motion, or already played)
 * returns `sequencing: false` — the caller then renders plain `<div>`s
 * instead of `Reveal`, so Landing is byte-identical to before this
 * change (no entrance-fade overhead either) until a real sequence runs. */
function useHeroStage() {
  const reduced = useReducedMotion();
  const skip = !FEATURE_FLAGS.SPATIAL_HERO_ENTRY || reduced || alreadyPlayedThisSession();
  const [stage, setStage] = useState(skip ? "identity" : "void");

  useEffect(() => {
    if (skip) return undefined;
    const timers = [
      setTimeout(() => setStage("world"), HERO_BEATS.world),
      setTimeout(() => setStage("focus"), HERO_BEATS.focus),
      setTimeout(() => {
        setStage("identity");
        markPlayed();
      }, HERO_BEATS.identity),
    ];
    return () => timers.forEach(clearTimeout);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return { stage, sequencing: !skip }; // stage: "void"|"world"|"focus"|"identity"
}

const HERO_STAGE_ORDER = ["void", "world", "focus", "identity"];
const reached = (stage, min) => HERO_STAGE_ORDER.indexOf(stage) >= HERO_STAGE_ORDER.indexOf(min);

/** Renders `Reveal` only while an actual VOID→IDENTITY sequence is
 * running; otherwise a plain passthrough `<div>` with the same
 * className, so the "off" path never pays for (or shows) an entrance
 * fade that didn't exist before ACA-0010. */
function HeroStage({ sequencing, show, className, children }) {
  if (!sequencing) return <div className={className}>{children}</div>;
  return <Reveal show={show} className={className}>{children}</Reveal>;
}

export default function Landing() {
  const { user, login, register, loading } = useAuth();
  const { t, lang, setLang } = useI18n();
  const nav = useNavigate();
  const [mode, setMode] = useState("register"); // register | login
  const [form, setForm] = useState({ email: "", password: "", display_name: "" });
  const [busy, setBusy] = useState(false);
  const { stage: heroStage, sequencing } = useHeroStage();

  if (loading) return null;
  if (user) {
    return <Navigate to={user.onboarding_completed ? "/dashboard" : "/onboarding"} replace />;
  }

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      if (mode === "register") {
        const u = await register({ ...form, lang });
        toast.success(`${t("landing_p.frek_id_generated")} ${u.frek_id}`);
        nav("/onboarding");
      } else {
        const u = await login(form.email, form.password);
        nav(u.onboarding_completed ? "/dashboard" : "/onboarding");
      }
    } catch (err) {
      toast.error(err?.response?.data?.detail || t("landing_p.auth_error"));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden noise" data-testid="landing-page">
      {/* header */}
      <header className="relative z-10 flex items-center justify-between px-6 md:px-16 py-6 border-b border-black/5 bg-white/60 backdrop-blur-xl">
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-full bg-[--cvln-orange] flex items-center justify-center">
            <Leaf className="text-white" width={18} height={18} />
          </div>
          <div className="font-display font-black tracking-tight text-lg md:text-xl">
            CVLN <span className="text-[--cvln-orange]">Academy</span>
          </div>
        </div>
        <div className="flex items-center gap-1" data-testid="landing-lang-toggle">
          {LANGS.map((l) => (
            // FOCUS: marks the one language that is actually active —
            // "make one object primary" per the primitive's own contract,
            // not a decorative hover effect (see motion-primitives.jsx).
            <Focus key={l.code} active={lang === l.code} className="inline-block">
              <button
                data-testid={`landing-lang-${l.code}`}
                onClick={() => setLang(l.code)}
                className={`text-xs px-3 py-1.5 rounded-full font-semibold transition
                  ${lang === l.code ? "bg-[--cvln-forest] text-white" : "text-[--cvln-ink-2] hover:text-[--cvln-ink]"}`}
              >
                {l.label}
              </button>
            </Focus>
          ))}
        </div>
      </header>

      <section className="relative z-10 max-w-7xl mx-auto px-6 md:px-16 py-16 md:py-24 grid md:grid-cols-2 gap-16">
        {/* Left: manifesto — WORLD before FOCUS before IDENTITY (ACA-0010):
            the world establishes before any specific content, and specific
            content (stat line) settles before the auth card ever competes
            for primary visual weight. Reveal never unmounts on the "off"
            path (`show` starts true when heroStage mounts at "identity"),
            so this is a no-op when SPATIAL_HERO_ENTRY is disabled. */}
        <HeroStage sequencing={sequencing} show={reached(heroStage, "world")} className="flex flex-col justify-center">
          <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange] mb-6">
            {t("landing_p.brand_line")}
          </div>
          <h1 className="font-display font-black text-5xl md:text-6xl lg:text-7xl leading-[0.95] tracking-tighter">
            {t("tagline")}<br/>
            <span className="text-[--cvln-orange]">{t("tagline_h")}</span>
          </h1>
          <p className="mt-8 text-lg md:text-xl text-[--cvln-ink-2] max-w-xl leading-relaxed">
            {t("tagline_p")}
          </p>
          <HeroStage sequencing={sequencing} show={reached(heroStage, "focus")} className="mt-10 flex flex-wrap gap-3 items-center">
            <span className="stade-chip">🌱 {t("stades.graine")}</span>
            <span className="stade-chip">🌿 {t("stades.pousse")}</span>
            <span className="stade-chip">🌳 {t("stades.racine")}</span>
            <span className="stade-chip">🌲 {t("stades.branches")}</span>
            <span className="stade-chip">🦅 {t("stades.arbre")}</span>
            <span className="stade-chip">🌳🌳 {t("stades.foret")}</span>
          </HeroStage>
          <div className="mt-10 text-xs mono text-[--cvln-ink-2]">
            30 {t("landing_p.stat_formations")} · 215 {t("landing_p.stat_modules")} · 8 {t("landing_p.stat_poles")} · {t("trilingual")}
          </div>
        </HeroStage>

        {/* Right: auth card — IDENTITY is `SECONDARY_CONTEXT` until the
            world/focus beats resolve (research §8.4): present in the DOM
            throughout (never conditionally unmounted — auth remains
            keyboard-reachable and testable at every stage), but only
            reaches full visual weight once heroStage is "identity". */}
        <HeroStage sequencing={sequencing} show={reached(heroStage, "identity")} className="flex items-center">
          <div className="w-full cvln-card p-8 md:p-10 relative overflow-hidden">
            <div className="absolute -top-16 -right-16 w-48 h-48 rounded-full bg-[--cvln-orange]/10" />
            <div className="relative z-10">
              {/* ENTER, keyed by mode: the auth mode the visitor just picked
                  (register vs. login) becomes their destination for this
                  interaction — a calm crossfade instead of the instant text
                  swap this block had before (CONTINUITY_OVER_PAGE_CUT
                  applied within the component, not just at route level). */}
              <Enter key={mode} show>
                <div className="flex items-center gap-2 mb-1">
                  <div className="text-[11px] mono uppercase tracking-[0.25em] text-[--cvln-ink-2] font-bold">
                    {mode === "register" ? t("landing_p.new_identity") : t("landing_p.sign_in")}
                  </div>
                </div>
                <h2 className="font-display font-bold text-3xl tracking-tight">
                  {mode === "register" ? t("register") : t("welcome_back")}
                </h2>
                {mode === "register" && (
                  <p className="mt-2 text-sm text-[--cvln-ink-2]">{t("signup_hint")}</p>
                )}
              </Enter>

              <form onSubmit={submit} className="mt-6 space-y-4" data-testid="auth-form">
                {mode === "register" && (
                  // ENTER on mount only — this field appearing is a real
                  // state change (register mode was just chosen), so it
                  // enters smoothly rather than popping in. Kept as a plain
                  // conditional render (not REVEAL-while-hidden) so the
                  // field is fully removed from the DOM in login mode:
                  // no stray `required` validation on a hidden input, no
                  // keyboard-focus trap on an invisible field.
                  <Enter show>
                    <label className="text-xs font-semibold text-[--cvln-ink-2]">{t("display_name")}</label>
                    <input
                      required minLength={1} maxLength={80}
                      data-testid="auth-display-name"
                      value={form.display_name}
                      onChange={(e) => setForm({ ...form, display_name: e.target.value })}
                      className="mt-1 w-full bg-white border border-black/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[--cvln-orange]"
                    />
                  </Enter>
                )}
                <div>
                  <label className="text-xs font-semibold text-[--cvln-ink-2]">{t("email")}</label>
                  <input
                    required type="email"
                    data-testid="auth-email"
                    value={form.email}
                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                    className="mt-1 w-full bg-white border border-black/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[--cvln-orange]"
                  />
                </div>
                <div>
                  <label className="text-xs font-semibold text-[--cvln-ink-2]">{t("password")}</label>
                  <input
                    required type="password" minLength={6}
                    data-testid="auth-password"
                    value={form.password}
                    onChange={(e) => setForm({ ...form, password: e.target.value })}
                    className="mt-1 w-full bg-white border border-black/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[--cvln-orange]"
                  />
                </div>
                <button
                  type="submit" disabled={busy}
                  data-testid="auth-submit"
                  className="btn-primary w-full disabled:opacity-60"
                >
                  {mode === "register" ? t("register") : t("login")}
                  <ArrowRight width={18} height={18} className="ml-2" />
                </button>
              </form>

              <button
                data-testid="auth-toggle"
                onClick={() => setMode(mode === "register" ? "login" : "register")}
                className="mt-6 text-sm text-[--cvln-ink-2] hover:text-[--cvln-orange] transition"
              >
                {mode === "register"
                  ? t("landing_p.toggle_to_login")
                  : t("landing_p.toggle_to_register")}
              </button>
            </div>
          </div>
        </HeroStage>
      </section>

      <footer className="relative z-10 max-w-7xl mx-auto px-6 md:px-16 py-10 border-t border-black/5 text-sm text-[--cvln-ink-2]">
        {t("landing_p.footer")}
      </footer>
    </div>
  );
}
