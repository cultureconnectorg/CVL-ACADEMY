import { useEffect, useMemo, useState } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { ArrowRight, NavArrowLeft, Sparks, CheckCircle } from "iconoir-react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n, LANGS } from "@/lib/i18n.jsx";
import { toast } from "sonner";

const STEPS = ["lang", "metier", "territoire", "objectif", "recap"];

export default function Onboarding() {
  const { user, loading, refreshMe } = useAuth();
  const { t, lang, setLang } = useI18n();
  const nav = useNavigate();

  const [step, setStep] = useState(0);
  const [options, setOptions] = useState({ metiers: [], territoires: [], langs: [] });
  const [choices, setChoices] = useState({
    lang: lang || "fr",
    metier_vise: "",
    territoire: "",
    objectif_perso: "",
  });
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    api.get("/onboarding/options").then((r) => setOptions(r.data));
  }, []);

  useEffect(() => {
    // Only auto-redirect if user is already onboarded and we're not showing a fresh result.
    if (user && user.onboarding_completed && !result) nav("/dashboard", { replace: true });
  }, [user, nav, result]);

  const canNext = useMemo(() => {
    if (step === 0) return !!choices.lang;
    if (step === 1) return !!choices.metier_vise;
    if (step === 2) return !!choices.territoire;
    if (step === 3) return choices.objectif_perso.trim().length >= 3;
    return true;
  }, [step, choices]);

  const next = () => setStep((s) => Math.min(STEPS.length - 1, s + 1));
  const prev = () => setStep((s) => Math.max(0, s - 1));

  const submit = async () => {
    setSubmitting(true);
    try {
      const { data } = await api.post("/onboarding/complete", choices);
      setResult(data);
      await refreshMe();
      toast.success(t("onboarding_p.success_toast"));
    } catch (e) {
      toast.error(e?.response?.data?.detail || t("onboarding_p.error_toast"));
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return null;
  if (!user) return <Navigate to="/" replace />;

  const stepPct = Math.round(((step + 1) / STEPS.length) * 100);

  return (
    <div className="min-h-screen bg-white noise flex flex-col" data-testid="onboarding-page">
      {/* header */}
      <header className="flex items-center justify-between px-6 md:px-16 py-6 border-b border-black/5">
        <div className="text-xs mono uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">
          FREK Origin Story · <span className="text-[--cvln-ink-2]">{user.frek_id}</span>
        </div>
        <div className="text-xs mono text-[--cvln-ink-2]">
          {t("onboarding_p.step_label")} {step + 1} / {STEPS.length}
        </div>
      </header>

      {/* progress */}
      <div className="h-1 bg-black/5">
        <div
          className="h-full bg-[--cvln-orange] transition-all duration-500"
          style={{ width: `${stepPct}%` }}
          data-testid="onboarding-progress"
        />
      </div>

      <main className="flex-1 flex items-start md:items-center justify-center px-6 md:px-16 py-10 md:py-16">
        <div className="w-full max-w-3xl">
          {/* STEP 0 — Language */}
          {step === 0 && (
            <StepShell
              kicker={t("onboarding_p.step1_kicker")}
              title={t("onboarding_p.step1_title")}
              subtitle={t("onboarding_p.step1_subtitle")}
              testId="step-lang"
            >
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-8">
                {LANGS.map((l) => (
                  <button
                    key={l.code}
                    data-testid={`ob-lang-${l.code}`}
                    onClick={() => {
                      setChoices({ ...choices, lang: l.code });
                      setLang(l.code);
                    }}
                    className={`text-left p-5 rounded-2xl border-2 transition
                      ${choices.lang === l.code
                        ? "border-[--cvln-orange] bg-[#FFF3EC]"
                        : "border-black/10 hover:border-black/25"}`}
                  >
                    <div className="text-2xl font-display font-black">{l.label}</div>
                    <div className="text-sm text-[--cvln-ink-2] mt-1">{l.name}</div>
                  </button>
                ))}
              </div>
            </StepShell>
          )}

          {/* STEP 1 — Métier visé */}
          {step === 1 && (
            <StepShell
              kicker={t("onboarding_p.step2_kicker")}
              title={t("onboarding_p.step2_title")}
              subtitle={t("onboarding_p.step2_subtitle")}
              testId="step-metier"
            >
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-8 max-h-[52vh] overflow-y-auto pr-1">
                {options.metiers.map((m) => (
                  <button
                    key={m.code}
                    data-testid={`ob-metier-${m.code}`}
                    onClick={() => setChoices({ ...choices, metier_vise: m.code })}
                    className={`text-left p-4 rounded-2xl border-2 transition flex items-center gap-3
                      ${choices.metier_vise === m.code
                        ? "border-[--cvln-orange] bg-[#FFF3EC]"
                        : "border-black/10 hover:border-black/25"}`}
                  >
                    <span
                      className="w-3 h-10 rounded-full shrink-0"
                      style={{ background: m.color }}
                    />
                    <span className="min-w-0">
                      <span className="block font-semibold">{m.name}</span>
                      <span className="block text-xs mono uppercase tracking-wider text-[--cvln-ink-2]">
                        {m.code}
                      </span>
                    </span>
                  </button>
                ))}
              </div>
            </StepShell>
          )}

          {/* STEP 2 — Territoire */}
          {step === 2 && (
            <StepShell
              kicker={t("onboarding_p.step3_kicker")}
              title={t("onboarding_p.step3_title")}
              subtitle={t("onboarding_p.step3_subtitle")}
              testId="step-territoire"
            >
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-8">
                {options.territoires.map((tr) => (
                  <button
                    key={tr.code}
                    data-testid={`ob-terr-${tr.code}`}
                    onClick={() => setChoices({ ...choices, territoire: tr.code })}
                    className={`text-left p-4 rounded-2xl border-2 transition
                      ${choices.territoire === tr.code
                        ? "border-[--cvln-orange] bg-[#FFF3EC]"
                        : "border-black/10 hover:border-black/25"}`}
                  >
                    <div className="font-semibold">{tr.name}</div>
                  </button>
                ))}
              </div>
            </StepShell>
          )}

          {/* STEP 3 — Objectif */}
          {step === 3 && (
            <StepShell
              kicker={t("onboarding_p.step4_kicker")}
              title={t("onboarding_p.step4_title")}
              subtitle={t("onboarding_p.step4_subtitle")}
              testId="step-objectif"
            >
              <textarea
                data-testid="ob-objectif"
                rows={4}
                maxLength={240}
                value={choices.objectif_perso}
                onChange={(e) => setChoices({ ...choices, objectif_perso: e.target.value })}
                placeholder={t("onboarding_p.step4_placeholder")}
                className="mt-8 w-full bg-white border-2 border-black/10 rounded-2xl px-5 py-4 text-base focus:outline-none focus:border-[--cvln-orange] focus:ring-2 focus:ring-[--cvln-orange]/30"
              />
              <div className="mt-2 text-xs text-[--cvln-ink-2]">
                {choices.objectif_perso.length}/240
              </div>
            </StepShell>
          )}

          {/* STEP 4 — Récap + submit */}
          {step === 4 && !result && (
            <StepShell
              kicker={t("onboarding_p.step5_kicker")}
              title={t("onboarding_p.step5_title")}
              subtitle={t("onboarding_p.step5_subtitle")}
              testId="step-recap"
            >
              <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-3">
                <Recap label={t("onboarding_p.recap_lang")} value={LANGS.find(l => l.code === choices.lang)?.label} />
                <Recap
                  label={t("onboarding_p.recap_metier")}
                  value={options.metiers.find(m => m.code === choices.metier_vise)?.name}
                />
                <Recap
                  label={t("onboarding_p.recap_territoire")}
                  value={options.territoires.find(tr => tr.code === choices.territoire)?.name}
                />
                <Recap label={t("onboarding_p.recap_objectif")} value={choices.objectif_perso} />
              </div>
            </StepShell>
          )}

          {/* Final — result */}
          {result && (
            <div data-testid="onboarding-result" className="fade-in">
              <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">
                {t("onboarding_p.launched_eyebrow")}
              </div>
              <h2 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-3">
                {t("onboarding_p.welcome")} {user.display_name.split(" ")[0]}.
              </h2>
              <p className="text-[--cvln-ink-2] mt-3 max-w-xl">
                {result.signals_emitted.length} {t("onboarding_p.signals_emitted")}{" "}
                <strong className="text-[--cvln-ink]">{result.badge_earned?.name}</strong> {t("onboarding_p.delivered")}
              </p>

              <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
                {result.recommended_formation && (
                  <div className="cvln-card p-6" data-testid="reco-formation">
                    <div className="text-[11px] mono uppercase tracking-[0.2em] font-bold text-[--cvln-orange]">
                      {t("onboarding_p.recommended_formation")}
                    </div>
                    <div
                      className="inline-flex items-center gap-2 px-2 py-1 rounded-full text-[10px] font-bold text-white mt-3"
                      style={{ background: result.recommended_formation.pole_color }}
                    >
                      {result.recommended_formation.pole_name} · {result.recommended_formation.code}
                    </div>
                    <div className="font-display font-bold text-2xl mt-2">
                      {result.recommended_formation.name}
                    </div>
                    <div className="text-sm text-[--cvln-ink-2] mt-2">
                      {result.recommended_formation.description}
                    </div>
                    <div className="text-xs mono text-[--cvln-ink-2] mt-3">
                      {result.recommended_formation.duration_h}h · {result.recommended_formation.cc} CC · {result.recommended_formation.modules_count} {t("modules").toLowerCase()}
                    </div>
                    <button
                      data-testid="reco-formation-start"
                      onClick={() => nav(`/formations/${result.recommended_formation.code}`)}
                      className="btn-primary mt-5"
                    >
                      {t("onboarding_p.open_formation")} <ArrowRight width={16} height={16} className="ml-2" />
                    </button>
                  </div>
                )}
                {result.recommended_mission && (
                  <div className="cvln-card p-6" data-testid="reco-mission">
                    <div className="text-[11px] mono uppercase tracking-[0.2em] font-bold text-[--cvln-orange]">
                      {t("onboarding_p.first_mission")}
                    </div>
                    <div className="text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2] mt-3">
                      {result.recommended_mission.pole} · {result.recommended_mission.entity}
                    </div>
                    <div className="font-display font-bold text-2xl mt-1">
                      {result.recommended_mission.title}
                    </div>
                    <div className="text-sm text-[--cvln-ink-2] mt-2">
                      {result.recommended_mission.description}
                    </div>
                    <div className="text-xs mono text-[--cvln-orange] font-bold mt-3">
                      +{result.recommended_mission.cc_reward} CC · {t("onboarding_p.already_accepted")}
                    </div>
                    <button
                      data-testid="reco-mission-open"
                      onClick={() => nav("/missions")}
                      className="btn-outline mt-5"
                    >
                      {t("onboarding_p.see_my_missions")}
                    </button>
                  </div>
                )}
              </div>

              <div className="mt-8">
                <button
                  data-testid="onboarding-goto-dashboard"
                  onClick={() => nav("/dashboard")}
                  className="btn-primary"
                >
                  {t("onboarding_p.goto_dashboard")} <ArrowRight width={16} height={16} className="ml-2" />
                </button>
              </div>
            </div>
          )}

          {/* Nav buttons */}
          {!result && (
            <div className="mt-10 flex items-center justify-between">
              <button
                data-testid="onboarding-prev"
                onClick={prev}
                disabled={step === 0}
                className="btn-outline text-sm disabled:opacity-40"
              >
                <NavArrowLeft width={16} height={16} className="mr-1" /> {t("onboarding_p.back")}
              </button>
              {step < STEPS.length - 1 ? (
                <button
                  data-testid="onboarding-next"
                  onClick={next}
                  disabled={!canNext}
                  className="btn-primary disabled:opacity-40"
                >
                  {t("onboarding_p.continue_btn")} <ArrowRight width={16} height={16} className="ml-2" />
                </button>
              ) : (
                <button
                  data-testid="onboarding-submit"
                  onClick={submit}
                  disabled={submitting}
                  className="btn-primary disabled:opacity-40"
                >
                  {submitting ? t("onboarding_p.generating") : t("onboarding_p.launch")}
                  <Sparks width={16} height={16} className="ml-2" />
                </button>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

function StepShell({ kicker, title, subtitle, children, testId }) {
  return (
    <div className="fade-in" data-testid={testId}>
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">
        {kicker}
      </div>
      <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-3">
        {title}
      </h1>
      {subtitle && (
        <p className="text-[--cvln-ink-2] mt-3 max-w-xl">{subtitle}</p>
      )}
      {children}
    </div>
  );
}

function Recap({ label, value }) {
  return (
    <div className="p-4 rounded-2xl border border-black/10 bg-[--cvln-bg-warm]">
      <div className="text-[10px] uppercase tracking-wider text-[--cvln-ink-2] font-semibold flex items-center gap-1">
        <CheckCircle width={12} height={12} className="text-[--cvln-orange]" /> {label}
      </div>
      <div className="mt-1 font-semibold text-sm">{value || "—"}</div>
    </div>
  );
}
