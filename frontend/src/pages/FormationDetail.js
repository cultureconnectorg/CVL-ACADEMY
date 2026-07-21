import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { NavArrowLeft, Play, Book, Trophy, MediaVideo, Coins } from "iconoir-react";
import { api } from "@/lib/api";
import { useI18n } from "@/lib/i18n.jsx";
import { useAuth } from "@/lib/auth.jsx";
import { toast } from "sonner";

const STADE_EMOJI = {
  graine: "🌱", pousse: "🌿", racine: "🌳",
  branches: "🌲", arbre: "🦅", foret: "🌳🌳",
};

export default function FormationDetail() {
  const { code } = useParams();
  const { t } = useI18n();
  const { refreshMe } = useAuth();
  const [f, setF] = useState(null);
  const [quiz, setQuiz] = useState(null); // { module, quiz[] }
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);

  useEffect(() => {
    api.get(`/formations/${code}`).then(r => setF(r.data));
  }, [code]);

  const openQuiz = async (mod) => {
    setResult(null); setAnswers({});
    const { data } = await api.get(`/formations/${code}/modules/${mod.code}/quiz`);
    setQuiz(data);
  };

  const submit = async () => {
    if (!quiz) return;
    try {
      const { data } = await api.post(
        `/formations/${code}/modules/${quiz.module.code}/quiz/submit`,
        { module_code: quiz.module.code, answers },
      );
      setResult(data);
      if (data.passed) {
        toast.success(`+${data.cc_earned} CC · signal ${data.signal_emitted} émis`);
        await refreshMe();
      } else {
        toast.error(t("quiz_result_failed"));
      }
    } catch (e) {
      toast.error("Erreur lors de la soumission du quiz.");
    }
  };

  if (!f) return <div className="p-10 text-[--cvln-ink-2]">…</div>;

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="formation-detail">
      <Link to="/formations" className="inline-flex items-center gap-1 text-sm text-[--cvln-ink-2] hover:text-[--cvln-orange] mb-6">
        <NavArrowLeft width={16} height={16} /> {t("formations")}
      </Link>

      {/* header */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2">
          <div
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold text-white"
            style={{ background: f.pole_color }}
          >
            {f.pole_name} · {f.code}
          </div>
          <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-4">
            {f.name}
          </h1>
          <p className="text-[--cvln-ink-2] mt-4 text-lg leading-relaxed max-w-2xl">
            {f.description}
          </p>
          <div className="mt-4 text-sm text-[--cvln-ink-2] max-w-2xl">
            <strong className="text-[--cvln-ink]">Objectif stratégique — </strong>
            {f.objective_strategic}
          </div>
        </div>

        <div className="cvln-card p-6 space-y-3">
          <Row icon={<Book width={16} height={16} />} label={t("duration")} value={`${f.duration_h}h`} />
          <Row icon={<Coins width={16} height={16} />} label={t("cc_credits")} value={`${f.cc} CC`} />
          <Row icon={<Trophy width={16} height={16} />} label="Badge" value={f.badge_name} />
          <Row icon={<MediaVideo width={16} height={16} />} label="Stades" value={
            <span>{STADE_EMOJI[f.stades[0]]} → {STADE_EMOJI[f.stades[f.stades.length - 1]]}</span>
          } />
          <div className="pt-3 border-t border-black/5 text-xs">
            <div className="text-[--cvln-ink-2] font-semibold uppercase tracking-wider">{t("prerequisites")}</div>
            <div className="mt-1">{f.prerequisites}</div>
          </div>
          <div className="text-xs">
            <div className="text-[--cvln-ink-2] font-semibold uppercase tracking-wider">{t("debouches")}</div>
            <div className="mt-1">{f.debouches}</div>
          </div>
        </div>
      </div>

      {/* Modules */}
      <div className="mt-12">
        <h2 className="font-display font-bold text-2xl md:text-3xl tracking-tight">{t("modules")}</h2>
        {(!f.modules || f.modules.length === 0) ? (
          <div className="mt-4 cvln-card p-8 text-center text-[--cvln-ink-2]">
            {t("coming_soon")} — équipe formateur en cours de production.
          </div>
        ) : (
          <div className="mt-4 grid gap-3">
            {f.modules.map((m, i) => (
              <div
                key={m.code}
                data-testid={`module-${m.code}`}
                className="cvln-card p-5 flex items-center gap-5 flex-wrap"
              >
                <div className="w-10 h-10 rounded-full bg-[--cvln-bg-warm] flex items-center justify-center font-bold text-[--cvln-ink]">
                  {i + 1}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2 text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2]">
                    <span>{m.code}</span>
                    <span>·</span>
                    <span>{m.duration_h}h</span>
                    <span>·</span>
                    <span>{STADE_EMOJI[m.stade]} {t(`stades.${m.stade}`)}</span>
                  </div>
                  <div className="font-semibold text-lg mt-1">{m.name}</div>
                  <div className="text-sm text-[--cvln-ink-2] mt-1">
                    <strong>{t("deliverable")} : </strong>{m.deliverable}
                  </div>
                </div>
                <button
                  data-testid={`quiz-open-${m.code}`}
                  onClick={() => openQuiz(m)}
                  className="btn-primary text-sm"
                >
                  <Play width={16} height={16} className="mr-1.5" />
                  {t("quiz_open")}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Quiz Modal */}
      {quiz && (
        <div className="fixed inset-0 z-50 flex items-start md:items-center justify-center p-4 bg-black/40" data-testid="quiz-modal">
          <div className="relative bg-white rounded-2xl w-full max-w-2xl max-h-[92vh] overflow-hidden flex flex-col fade-in">
            <div className="p-6 border-b border-black/5">
              <div className="text-xs mono uppercase tracking-wider text-[--cvln-orange] font-bold">
                {t("quiz_title")}
              </div>
              <h3 className="font-display font-bold text-2xl tracking-tight mt-1">{quiz.module.name}</h3>
              <button
                data-testid="quiz-close"
                onClick={() => { setQuiz(null); setResult(null); setAnswers({}); }}
                className="absolute top-4 right-4 w-9 h-9 rounded-full hover:bg-black/5 flex items-center justify-center"
              >✕</button>
            </div>
            <div className="p-6 overflow-y-auto space-y-5">
              {quiz.quiz.map((q) => (
                <div key={q.n} data-testid={`quiz-q-${q.n}`}>
                  <div className="text-xs mono text-[--cvln-ink-2] font-semibold">{q.n} · {q.type}</div>
                  <div className="mt-1 font-semibold">{q.question}</div>
                  <div className="mt-3 space-y-2">
                    {q.choices.map((c) => (
                      <label
                        key={c.id}
                        data-testid={`quiz-q-${q.n}-${c.id}`}
                        className={`flex gap-3 items-start px-4 py-3 border rounded-xl cursor-pointer transition
                          ${answers[q.n] === c.id ? "border-[--cvln-orange] bg-[#FFF3EC]" : "border-black/10 hover:border-black/20"}`}
                      >
                        <input
                          type="radio" name={`q-${q.n}`}
                          checked={answers[q.n] === c.id}
                          onChange={() => setAnswers({ ...answers, [q.n]: c.id })}
                          className="mt-1 accent-[--cvln-orange]"
                        />
                        <span className="text-sm">{c.text}</span>
                      </label>
                    ))}
                  </div>
                </div>
              ))}

              {result && (
                <div
                  data-testid="quiz-result"
                  className={`p-4 rounded-xl ${result.passed ? "bg-[#E7F5EF] text-[#0F4E33]" : "bg-[#FEE7DF] text-[#7B1D0D]"}`}
                >
                  <div className="font-bold">
                    {result.passed ? t("quiz_result_passed") : t("quiz_result_failed")}
                  </div>
                  <div className="text-sm mt-1 mono">
                    Score : {Math.round(result.score * 100)}% ({result.correct}/{result.total})
                    {result.passed && ` · +${result.cc_earned} CC · signal ${result.signal_emitted}`}
                  </div>
                </div>
              )}
            </div>
            <div className="p-4 border-t border-black/5 bg-white flex items-center justify-end gap-2">
              <button
                onClick={() => { setQuiz(null); setResult(null); setAnswers({}); }}
                className="btn-outline text-sm"
              >
                {t("close")}
              </button>
              <button
                data-testid="quiz-submit"
                onClick={submit}
                disabled={Object.keys(answers).length < quiz.quiz.length}
                className="btn-primary text-sm disabled:opacity-50"
              >
                {t("quiz_submit")}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Row({ icon, label, value }) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2 text-xs uppercase tracking-wider text-[--cvln-ink-2]">
        {icon} {label}
      </div>
      <div className="text-sm font-semibold">{value}</div>
    </div>
  );
}
