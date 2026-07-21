import { useState } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { Leaf, ArrowRight } from "iconoir-react";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n, LANGS } from "@/lib/i18n.jsx";
import { toast } from "sonner";

export default function Landing() {
  const { user, login, register, loading } = useAuth();
  const { t, lang, setLang } = useI18n();
  const nav = useNavigate();
  const [mode, setMode] = useState("register"); // register | login
  const [form, setForm] = useState({ email: "", password: "", display_name: "" });
  const [busy, setBusy] = useState(false);

  if (loading) return null;
  if (user) return <Navigate to="/dashboard" replace />;

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      if (mode === "register") {
        const u = await register({ ...form, lang });
        toast.success(`FREK-ID généré : ${u.frek_id}`);
      } else {
        await login(form.email, form.password);
      }
      nav("/dashboard");
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Erreur d'authentification");
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
            <button
              key={l.code}
              data-testid={`landing-lang-${l.code}`}
              onClick={() => setLang(l.code)}
              className={`text-xs px-3 py-1.5 rounded-full font-semibold transition
                ${lang === l.code ? "bg-[--cvln-forest] text-white" : "text-[--cvln-ink-2] hover:text-[--cvln-ink]"}`}
            >
              {l.label}
            </button>
          ))}
        </div>
      </header>

      <section className="relative z-10 max-w-7xl mx-auto px-6 md:px-16 py-16 md:py-24 grid md:grid-cols-2 gap-16">
        {/* Left: manifesto */}
        <div className="flex flex-col justify-center">
          <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange] mb-6">
            CVLN Group · Martinique · 2026
          </div>
          <h1 className="font-display font-black text-5xl md:text-6xl lg:text-7xl leading-[0.95] tracking-tighter">
            {t("tagline")}<br/>
            <span className="text-[--cvln-orange]">{t("tagline_h")}</span>
          </h1>
          <p className="mt-8 text-lg md:text-xl text-[--cvln-ink-2] max-w-xl leading-relaxed">
            {t("tagline_p")}
          </p>
          <div className="mt-10 flex flex-wrap gap-3 items-center">
            <span className="stade-chip">🌱 Graine</span>
            <span className="stade-chip">🌿 Pousse</span>
            <span className="stade-chip">🌳 Racine</span>
            <span className="stade-chip">🌲 Branches</span>
            <span className="stade-chip">🦅 Arbre</span>
            <span className="stade-chip">🌳🌳 Forêt</span>
          </div>
          <div className="mt-10 text-xs mono text-[--cvln-ink-2]">
            30 formations · 215 modules · 8 pôles · {t("trilingual")}
          </div>
        </div>

        {/* Right: auth card */}
        <div className="flex items-center">
          <div className="w-full cvln-card p-8 md:p-10 relative overflow-hidden">
            <div className="absolute -top-16 -right-16 w-48 h-48 rounded-full bg-[--cvln-orange]/10" />
            <div className="relative z-10">
              <div className="flex items-center gap-2 mb-1">
                <div className="text-[11px] mono uppercase tracking-[0.25em] text-[--cvln-ink-2] font-bold">
                  {mode === "register" ? "FrekCore · New identity" : "FrekCore · Sign in"}
                </div>
              </div>
              <h2 className="font-display font-bold text-3xl tracking-tight">
                {mode === "register" ? t("register") : t("welcome_back")}
              </h2>
              {mode === "register" && (
                <p className="mt-2 text-sm text-[--cvln-ink-2]">{t("signup_hint")}</p>
              )}

              <form onSubmit={submit} className="mt-6 space-y-4" data-testid="auth-form">
                {mode === "register" && (
                  <div>
                    <label className="text-xs font-semibold text-[--cvln-ink-2]">{t("display_name")}</label>
                    <input
                      required minLength={1} maxLength={80}
                      data-testid="auth-display-name"
                      value={form.display_name}
                      onChange={(e) => setForm({ ...form, display_name: e.target.value })}
                      className="mt-1 w-full bg-white border border-black/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[--cvln-orange]"
                    />
                  </div>
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
                  ? "Déjà un FREK-ID ? Se connecter"
                  : "Nouveau ? Créer mon FREK-ID"}
              </button>
            </div>
          </div>
        </div>
      </section>

      <footer className="relative z-10 max-w-7xl mx-auto px-6 md:px-16 py-10 border-t border-black/5 text-sm text-[--cvln-ink-2]">
        CVLN Academy OS — Learning Infrastructure for Future Cultural &amp; Technology Industries · Martinique · Diaspora
      </footer>
    </div>
  );
}
