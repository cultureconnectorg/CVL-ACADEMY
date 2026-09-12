import { useState } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { Leaf, ArrowRight } from "iconoir-react";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n, LANGS } from "@/lib/i18n.jsx";
import { toast } from "sonner";
import { Focus, Enter } from "@/lib/motion-primitives";

const PUBLIC_NAV = ["Accueil", "Formations", "Parcours", "Communauté", "Entreprises", "Institutions", "À propos"];

export default function Landing() {
  const { user, login, register, loading } = useAuth();
  const { t, lang, setLang } = useI18n();
  const nav = useNavigate();
  const [mode, setMode] = useState("register");
  const [form, setForm] = useState({ email: "", password: "", display_name: "" });
  const [busy, setBusy] = useState(false);

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
    <div className="cvln-landing" data-testid="landing-page">
      <header className="cvln-topbar">
        <div className="cvln-wordmark">
          <div className="cvln-wordmark-mark" aria-hidden="true">
            <Leaf width={20} height={20} />
          </div>
          <div>
            <div className="font-display font-black tracking-[0.12em] text-xl leading-none">CVLN</div>
            <div className="text-[10px] tracking-[0.24em] text-white/60 mt-1">ACADEMY</div>
          </div>
        </div>

        <nav className="cvln-topnav" aria-label="Navigation publique">
          {PUBLIC_NAV.map((item, index) => (
            <a key={item} href={index === 0 ? "#top" : "#academy"} className={index === 0 ? "active" : ""}>
              {item}
            </a>
          ))}
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
          <button
            onClick={() => setMode("login")}
            className="hidden sm:inline-flex px-4 py-2.5 rounded-xl border border-white/15 bg-black/10 text-sm font-semibold text-white hover:bg-white/10 transition"
          >
            Se connecter
          </button>
          <button
            onClick={() => setMode("register")}
            className="inline-flex px-4 py-2.5 rounded-xl bg-[--cvln-orange] text-sm font-bold text-white hover:brightness-110 transition"
          >
            Rejoindre l’Academy
          </button>
        </div>
      </header>

      <section id="top" className="cvln-hero-grid">
        <div className="min-w-0">
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
            <button onClick={() => setMode("register")} className="btn-primary rounded-xl">
              Découvrir nos formations <ArrowRight width={17} height={17} className="ml-2" />
            </button>
            <a href="#academy" className="btn-outline rounded-xl border-white/30 text-white">
              Voir le monde CVLN <span className="ml-2 text-xs">▷</span>
            </a>
          </div>

          <div id="academy" className="cvln-hero-meta" aria-label="CVLN Academy en chiffres">
            <div className="cvln-stat-tile"><strong>30+</strong><span>Formations · métiers créatifs, tech & business</span></div>
            <div className="cvln-stat-tile"><strong>400</strong><span>Talents / an · un écosystème pour grandir</span></div>
            <div className="cvln-stat-tile"><strong>Caraïbe → Monde</strong><span>Des ponts réels vers l’international</span></div>
            <div className="cvln-stat-tile"><strong>Culture & Innovation</strong><span>Des compétences d’aujourd’hui pour demain</span></div>
          </div>
        </div>

        <div className="cvln-glass-panel cvln-auth-panel" aria-label="Accès CVLN Academy">
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
            onClick={() => setMode(mode === "register" ? "login" : "register")}
            className="mt-5 text-sm text-white/55 hover:text-[--cvln-orange] transition"
          >
            {mode === "register" ? t("landing_p.toggle_to_login") : t("landing_p.toggle_to_register")}
          </button>
        </div>
      </section>
    </div>
  );
}
