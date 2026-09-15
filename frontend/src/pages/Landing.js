import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate, Navigate } from "react-router-dom";
import { Leaf, ArrowRight } from "iconoir-react";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n, LANGS } from "@/lib/i18n.jsx";
import { toast } from "sonner";
import { Focus, Enter, Reveal, Confirm } from "@/lib/motion-primitives";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { useReducedMotion } from "@/lib/useReducedMotion";

// ACA-0010 ("Hero/Entry — world entry, not SaaS landing",
// docs/ACADEMY_HERO_ENTRY_RESEARCH.md §8-9) — the storyboard's four
// beats compressed for a real, usable product rather than the
// illustrative 0-60s cinematic timing: VOID is near-instant (a signal,
// not a wait), WORLD/FOCUS resolve within ~1s so a visitor is never
// blocked from acting. What's preserved from the research is the
// *sequencing* itself (world before identity gets primary weight),
// which is the actual acceptance criterion (§16.1), applied here to
// this page's own real hero content (kicker/title/copy/CTAs/stat-tiles,
// auth panel) rather than replacing it with different copy.
const HERO_BEATS = { world: 80, focus: 420, identity: 760 };
const HERO_SESSION_KEY = "cvln_academy_hero_played";

// ACA-0011 — the beat a fresh FREK-ID is held on screen (Confirm reveal)
// before advancing to onboarding. Short and restrained (MOT-008 "calm by
// default"), not a celebratory pause — long enough to actually register
// as an event, never long enough to feel like a blocking loading screen.
const IDENTITY_CONFIRM_BEAT = 900;

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
 * className (and any other DOM attributes, e.g. `id`/`aria-label` —
 * `Reveal` itself only accepts show/className, so those attributes
 * only reach the DOM on the non-sequencing branch; callers that need
 * them preserved during the sequenced branch too wrap this in a
 * stable, unanimated parent instead), so the "off" path never pays for
 * (or shows) an entrance fade that didn't exist before ACA-0010. */
function HeroStage({ sequencing, show, className, children, ...rest }) {
  if (!sequencing) return <div className={className} {...rest}>{children}</div>;
  return <Reveal show={show} className={className}>{children}</Reveal>;
}

const PUBLIC_NAV = [
  { label: "Accueil", href: "#top" },
  { label: "Formations", href: "#formations" },
  { label: "Parcours", href: "#parcours" },
  { label: "Communauté", href: "#communaute" },
  { label: "Entreprises", href: "#entreprises" },
  { label: "Institutions", href: "#institutions" },
  { label: "À propos", href: "#about" },
];

export default function Landing({ initialMode }) {
  const { user, login, register, loading } = useAuth();
  const { t, lang, setLang } = useI18n();
  const nav = useNavigate();
  const location = useLocation();
  const [mode, setMode] = useState(initialMode === "login" ? "login" : "register");
  const [form, setForm] = useState({ email: "", password: "", display_name: "" });
  const [busy, setBusy] = useState(false);
  const { stage: heroStage, sequencing } = useHeroStage();
  const reducedMotion = useReducedMotion();
  // ACA-0011 — holds the freshly-issued FREK-ID while its Confirm reveal
  // plays; null the rest of the time (including the entire "off" path,
  // where this state is set and read but never rendered — see the
  // identityConfirming JSX guard below).
  const [newIdentity, setNewIdentity] = useState(null);

  useEffect(() => {
    if (initialMode === "login" || initialMode === "register") {
      setMode(initialMode);
    }
  }, [initialMode]);

  const setAuthMode = (nextMode) => {
    setMode(nextMode);
    const target = nextMode === "login" ? "/login" : "/register";
    if (location.pathname !== target) nav(target, { replace: false });
  };

  if (loading) return null;
  if (user) {
    return <Navigate to={user.onboarding_completed ? "/dashboard" : "/onboarding"} replace />;
  }

  const identityConfirming = FEATURE_FLAGS.SPATIAL_IDENTITY_ENTRY && !reducedMotion && !!newIdentity;

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      if (mode === "register") {
        const u = await register({ ...form, lang });
        toast.success(`${t("landing_p.frek_id_generated")} ${u.frek_id}`);
        if (FEATURE_FLAGS.SPATIAL_IDENTITY_ENTRY && !reducedMotion) {
          // Hold on the new identity — a real, visible acknowledgment
          // (research's NFS/Autolog lesson: an action should visibly
          // change what the world says back) — before advancing, rather
          // than an instant redirect racing the toast off-screen.
          setNewIdentity({ frek_id: u.frek_id });
          setTimeout(() => nav("/onboarding"), IDENTITY_CONFIRM_BEAT);
        } else {
          nav("/onboarding");
        }
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
    <div className="cvln-landing" data-testid="landing-page">
      <header className="cvln-topbar">
        <Link to="/" className="cvln-wordmark" aria-label="CVLN Academy — Accueil">
          <div className="cvln-wordmark-mark" aria-hidden="true">
            <Leaf width={20} height={20} />
          </div>
          <div>
            <div className="font-display font-black tracking-[0.12em] text-xl leading-none">CVLN</div>
            <div className="text-[10px] tracking-[0.24em] text-white/60 mt-1">ACADEMY</div>
          </div>
        </Link>

        <nav className="cvln-topnav" aria-label="Navigation publique">
          {PUBLIC_NAV.map((item, index) => (
            <a key={item.label} href={item.href} className={index === 0 ? "active" : ""}>
              {item.label}
            </a>
          ))}
          <Link to="/pricing">Tarifs</Link>
        </nav>

        <div className="flex items-center gap-2">
          <div className="hidden lg:flex items-center gap-1 mr-2" data-testid="landing-lang-toggle">
            {LANGS.map((l) => (
              <Focus key={l.code} active={lang === l.code} className="inline-block">
                <button
                  data-testid={`landing-lang-${l.code}`}
                  onClick={() => setLang(l.code)}
                  className={`text-[10px] px-2 py-1 rounded-full font-bold transition ${
                    lang === l.code ? "bg-white/12 text-white" : "text-white/50 hover:text-white"
                  }`}
                >
                  {l.label}
                </button>
              </Focus>
            ))}
          </div>
          <Link
            to="/login"
            onClick={() => setMode("login")}
            className="hidden sm:inline-flex px-4 py-2.5 rounded-xl border border-white/15 bg-black/10 text-sm font-semibold text-white hover:bg-white/10 transition"
          >
            Se connecter
          </Link>
          <Link
            to="/register"
            onClick={() => setMode("register")}
            className="inline-flex px-4 py-2.5 rounded-xl bg-[--cvln-orange] text-sm font-bold text-white hover:brightness-110 transition"
          >
            Rejoindre l’Academy
          </Link>
        </div>
      </header>

      <section id="top" className="cvln-hero-grid">
        {/* Left: manifesto — WORLD before FOCUS before IDENTITY (ACA-0010):
            the world establishes before any specific content, and specific
            content (stat tiles) settles before the auth card ever competes
            for primary visual weight. HeroStage is a no-op passthrough
            (byte-identical DOM/behavior to before ACA-0010) whenever
            SPATIAL_HERO_ENTRY is off, reduced motion is on, or this session
            already played the sequence once. */}
        <HeroStage sequencing={sequencing} show={reached(heroStage, "world")} className="min-w-0">
          <div className="cvln-kicker">Où la culture devient avenir</div>
          <h1 className="cvln-hero-title">
            APPRENDRE<br />
            CRÉER<br />
            <span className="accent">IMPACTER</span>
          </h1>
          <p className="cvln-hero-copy">
            CVLN Academy forme les talents d’aujourd’hui pour bâtir les industries culturelles de demain,
            en Caraïbe et dans le monde.
          </p>

          <div className="mt-8 flex flex-wrap gap-3">
            <a href="#formations" className="btn-primary rounded-xl">
              Découvrir nos formations <ArrowRight width={17} height={17} className="ml-2" />
            </a>
            <a href="#about" className="btn-outline rounded-xl border-white/30 text-white">
              Voir le monde CVLN <span className="ml-2 text-xs">▷</span>
            </a>
          </div>

          <div id="academy" aria-label="CVLN Academy en chiffres">
            <HeroStage sequencing={sequencing} show={reached(heroStage, "focus")} className="cvln-hero-meta">
              <div className="cvln-stat-tile"><strong>30+</strong><span>Formations · métiers créatifs, tech & business</span></div>
              <div className="cvln-stat-tile"><strong>400</strong><span>Talents / an · un écosystème pour grandir</span></div>
              <div className="cvln-stat-tile"><strong>Caraïbe → Monde</strong><span>Des ponts réels vers l’international</span></div>
              <div className="cvln-stat-tile"><strong>Culture & Innovation</strong><span>Des compétences d’aujourd’hui pour demain</span></div>
            </HeroStage>
          </div>
        </HeroStage>

        {/* Right: auth card — IDENTITY is `SECONDARY_CONTEXT` until the
            world/focus beats resolve (research §8.4): present in the DOM
            throughout (never conditionally unmounted — auth remains
            keyboard-reachable and testable at every stage), reaching full
            visual weight once heroStage is "identity" (immediate on the
            non-sequencing path). */}
        <HeroStage sequencing={sequencing} show={reached(heroStage, "identity")} className="cvln-glass-panel cvln-auth-panel" aria-label="Accès CVLN Academy">
          {identityConfirming ? (
            // ACA-0011 — the FREK-ID as a real, acknowledged identity
            // event (Confirm primitive: "short restrained physical
            // feedback," never confetti/celebration) instead of an
            // instant redirect racing the toast off-screen. Auto-advances
            // to onboarding after IDENTITY_CONFIRM_BEAT (see submit()).
            <div data-testid="identity-confirm">
              <Confirm triggerKey={newIdentity.frek_id}>
                <div className="text-[10px] mono uppercase tracking-[0.25em] text-white/50 font-bold">
                  {t("landing_p.new_identity")}
                </div>
                <h2 className="font-display font-bold text-3xl md:text-4xl tracking-tight mt-2 text-white">
                  {t("landing_p.frek_id_generated")}
                </h2>
                <div
                  data-testid="identity-frek-id"
                  className="mt-4 mono text-2xl font-bold text-[--cvln-orange] tracking-wide"
                >
                  {newIdentity.frek_id}
                </div>
              </Confirm>
            </div>
          ) : (
            <>
              <Enter key={mode} show>
                <div className="text-[10px] mono uppercase tracking-[0.25em] text-white/50 font-bold">
                  {mode === "register" ? t("landing_p.new_identity") : t("landing_p.sign_in")}
                </div>
                <h2 className="font-display font-bold text-3xl md:text-4xl tracking-tight mt-2 text-white">
                  {mode === "register" ? "Entre dans l’Academy" : t("welcome_back")}
                </h2>
                <p className="mt-2 text-sm text-white/60">
                  {mode === "register"
                    ? "Crée ton identité CVLN et commence ton parcours dans un même monde, plusieurs destinations."
                    : "Retrouve ton parcours, ta progression et ton prochain objectif."}
                </p>
              </Enter>

              <form onSubmit={submit} className="mt-7 space-y-4" data-testid="auth-form">
                {mode === "register" && (
                  <Enter show>
                    <label className="text-xs font-semibold text-white/65">{t("display_name")}</label>
                    <input
                      required minLength={1} maxLength={80}
                      data-testid="auth-display-name"
                      value={form.display_name}
                      onChange={(e) => setForm({ ...form, display_name: e.target.value })}
                      className="mt-1 w-full border rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[--cvln-orange]"
                    />
                  </Enter>
                )}
                <div>
                  <label className="text-xs font-semibold text-white/65">{t("email")}</label>
                  <input
                    required type="email"
                    data-testid="auth-email"
                    value={form.email}
                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                    className="mt-1 w-full border rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[--cvln-orange]"
                  />
                </div>
                <div>
                  <label className="text-xs font-semibold text-white/65">{t("password")}</label>
                  <input
                    required type="password" minLength={6}
                    data-testid="auth-password"
                    value={form.password}
                    onChange={(e) => setForm({ ...form, password: e.target.value })}
                    className="mt-1 w-full border rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[--cvln-orange]"
                  />
                </div>
                <button
                  type="submit" disabled={busy}
                  data-testid="auth-submit"
                  className="btn-primary w-full rounded-xl disabled:opacity-60"
                >
                  {mode === "register" ? t("register") : t("login")}
                  <ArrowRight width={18} height={18} className="ml-2" />
                </button>
              </form>

              <button
                data-testid="auth-toggle"
                onClick={() => setAuthMode(mode === "register" ? "login" : "register")}
                className="mt-5 text-sm text-white/55 hover:text-[--cvln-orange] transition"
              >
                {mode === "register" ? t("landing_p.toggle_to_login") : t("landing_p.toggle_to_register")}
              </button>
            </>
          )}
        </HeroStage>
      </section>

      <section id="formations" className="px-6 md:px-16 py-16 border-t border-white/10">
        <div className="max-w-6xl mx-auto grid md:grid-cols-[1.2fr_.8fr] gap-8 items-start">
          <div>
            <div className="cvln-kicker">Formations</div>
            <h2 className="font-display font-black text-4xl md:text-6xl tracking-tight text-white mt-3">Découvrir avant de s’inscrire.</h2>
            <p className="mt-4 text-white/65 max-w-2xl">Explore l’Academy, puis crée ton compte pour débloquer ton parcours personnalisé, tes modules, missions et preuves de compétences.</p>
          </div>
          <div className="flex flex-wrap gap-3 md:justify-end">
            <Link to="/register" className="btn-primary rounded-xl">Créer mon parcours</Link>
            <Link to="/pricing" className="btn-outline rounded-xl border-white/30 text-white">Voir les tarifs</Link>
          </div>
        </div>
      </section>

      <section id="parcours" className="px-6 md:px-16 py-16 border-t border-white/10">
        <div className="max-w-6xl mx-auto">
          <div className="cvln-kicker">Parcours</div>
          <h2 className="font-display font-black text-4xl md:text-5xl tracking-tight text-white mt-3">Inscription → conformité → onboarding → dashboard → formation.</h2>
        </div>
      </section>

      <section id="communaute" className="px-6 md:px-16 py-16 border-t border-white/10">
        <div className="max-w-6xl mx-auto">
          <div className="cvln-kicker">Communauté</div>
          <h2 className="font-display font-black text-4xl md:text-5xl tracking-tight text-white mt-3">Talents, mentors, jurys et partenaires réunis dans le même environnement.</h2>
        </div>
      </section>

      <section id="entreprises" className="px-6 md:px-16 py-16 border-t border-white/10">
        <div className="max-w-6xl mx-auto flex flex-wrap items-end justify-between gap-6">
          <div>
            <div className="cvln-kicker">Entreprises</div>
            <h2 className="font-display font-black text-4xl md:text-5xl tracking-tight text-white mt-3">Former, identifier et connecter les compétences.</h2>
          </div>
          <Link to="/register" className="btn-outline rounded-xl border-white/30 text-white">Créer un accès</Link>
        </div>
      </section>

      <section id="institutions" className="px-6 md:px-16 py-16 border-t border-white/10">
        <div className="max-w-6xl mx-auto flex flex-wrap items-end justify-between gap-6">
          <div>
            <div className="cvln-kicker">Institutions</div>
            <h2 className="font-display font-black text-4xl md:text-5xl tracking-tight text-white mt-3">Un pont entre financement, parcours, preuves et suivi.</h2>
          </div>
          <Link to="/login" className="btn-outline rounded-xl border-white/30 text-white">Accéder à mon espace</Link>
        </div>
      </section>

      <section id="about" className="px-6 md:px-16 py-16 border-t border-white/10">
        <div className="max-w-6xl mx-auto flex flex-wrap items-end justify-between gap-6">
          <div>
            <div className="cvln-kicker">À propos</div>
            <h2 className="font-display font-black text-4xl md:text-5xl tracking-tight text-white mt-3">CVLN Academy relie apprentissage, culture, technologie et employabilité.</h2>
          </div>
          <Link to="/legal/mentions-legales" className="btn-outline rounded-xl border-white/30 text-white">Centre juridique</Link>
        </div>
      </section>
    </div>
  );
}
