import { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  CheckCircle, Circle, Lock, ArrowRight, PlaySolid,
  BookmarkBook, Bookmark, MediaVideo, Medal1st, Sparks, EmojiTalkingHappy,
} from "iconoir-react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";
import { toast } from "sonner";
import BackButton from "@/components/BackButton";

const PHASE_KEYS = [
  { key: "hook",          labelKey: "phase_hook",         icon: Sparks },
  { key: "objectives",    labelKey: "phase_objectives",   icon: BookmarkBook },
  { key: "course",        labelKey: "phase_course",       icon: MediaVideo },
  { key: "workshop",      labelKey: "phase_workshop",     icon: Bookmark },
  { key: "deliverable",   labelKey: "phase_deliverable",  icon: EmojiTalkingHappy },
  { key: "quiz",          labelKey: "phase_quiz",         icon: PlaySolid },
  { key: "mini_mission",  labelKey: "phase_mini_mission", icon: Medal1st },
];

export default function ModuleJourney() {
  const { fc, mc } = useParams();
  const nav = useNavigate();
  const { refreshMe } = useAuth();
  const { t } = useI18n();
  const [data, setData] = useState(null);
  const [openPhase, setOpenPhase] = useState("hook");
  const [deliverableText, setDeliverableText] = useState("");
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [quizResult, setQuizResult] = useState(null);

  const PHASE_META = PHASE_KEYS.map((p) => ({ ...p, label: t(`module_journey.${p.labelKey}`) }));

  const load = useCallback(async () => {
    const { data } = await api.get(`/modules/${fc}/${mc}`);
    setData(data);
  }, [fc, mc]);

  useEffect(() => {
    load();
  }, [load]);

  if (!data) return <div className="p-10 text-[--cvln-ink-2]">…</div>;

  const { formation, module, is_unlocked, lock_reason, phase_flags, status } = data;
  const phases = module.phases;

  const tickPhase = async (key, extra = {}) => {
    const { data: r } = await api.post(`/modules/${fc}/${mc}/phase`, { key, ...extra });
    setData((prev) => ({ ...prev, ...r, module: prev.module, formation: prev.formation }));
  };

  const submitDeliverable = async () => {
    try {
      const { data: r } = await api.post(`/modules/${fc}/${mc}/deliverable`, { text: deliverableText });
      setData((prev) => ({ ...prev, ...r, module: prev.module, formation: prev.formation }));
      toast.success(t("module_journey.deliverable_saved"));
      setOpenPhase("quiz");
    } catch (e) {
      toast.error(e?.response?.data?.detail || t("module_journey.deliverable_too_short"));
    }
  };

  const openQuiz = async () => {
    if (!phase_flags.deliverable) {
      toast.error(t("module_journey.complete_deliverable_first"));
      return;
    }
    setQuizResult(null); setAnswers({});
    const { data } = await api.get(`/formations/${fc}/modules/${mc}/quiz`);
    setQuiz(data);
    setOpenPhase("quiz");
  };

  const submitQuiz = async () => {
    try {
      const { data } = await api.post(
        `/formations/${fc}/modules/${mc}/quiz/submit`,
        { module_code: mc, answers },
      );
      setQuizResult(data);
      if (data.passed) {
        toast.success(`+${data.cc_earned} CC · signal ${data.signal_emitted}`);
        await refreshMe();
        await load();
        setOpenPhase("mini_mission");
      } else {
        toast.error(t("module_journey.need_80_retry"));
      }
    } catch (e) {
      toast.error(e?.response?.data?.detail || t("module_journey.quiz_error"));
    }
  };

  const commitMiniMission = async () => {
    try {
      await api.post(`/modules/${fc}/${mc}/mini-mission/commit`);
      toast.success(t("module_journey.module_validated_toast"));
      await refreshMe();
      await load();
    } catch (e) {
      toast.error(e?.response?.data?.detail || t("module_journey.mini_mission_error"));
    }
  };

  // LOCKED
  if (!is_unlocked) {
    return (
      <div className="px-6 md:px-12 py-10 max-w-3xl" data-testid="module-locked">
        <BackButton to={`/formations/${fc}`} label={formation.name} testId="back-to-formation" />
        <div className="cvln-card p-10 text-center">
          <Lock width={40} height={40} className="mx-auto text-[--cvln-ink-2]" />
          <h2 className="font-display font-bold text-3xl tracking-tight mt-4">{t("module_journey.locked_title")}</h2>
          <p className="text-[--cvln-ink-2] mt-3 max-w-md mx-auto">{lock_reason}</p>
          <button
            data-testid="back-to-formation-btn"
            onClick={() => nav(`/formations/${fc}`)}
            className="btn-primary mt-6"
          >
            {t("module_journey.back_to_formation")}
          </button>
        </div>
      </div>
    );
  }

  const doneCount = Object.values(phase_flags).filter(Boolean).length;

  return (
    <div className="px-6 md:px-12 py-10 max-w-6xl" data-testid="module-journey">
      <BackButton to={`/formations/${fc}`} label={formation.name} testId="back-to-formation" />

      {/* Header */}
      <div
        className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold text-white"
        style={{ background: formation.pole_color }}
      >
        {formation.pole_name} · {module.code}
      </div>
      <h1 className="font-display font-black text-3xl md:text-5xl tracking-tighter leading-none mt-3">
        {module.name}
      </h1>
      <div className="text-sm text-[--cvln-ink-2] mt-2">
        {module.duration_h}h · {phases.workshop.estimated_min}min {t("module_journey.workshop_suffix")} · {t("module_journey.stade_word")} {module.stade}
      </div>

      {/* Progress banner */}
      <div className="mt-8 cvln-card p-5 flex flex-col md:flex-row md:items-center gap-4" data-testid="journey-progress">
        <div className="flex-1">
          <div className="text-[10px] mono uppercase tracking-wider font-bold text-[--cvln-orange]">
            {t("module_journey.your_progress")}
          </div>
          <div className="font-display font-bold text-xl mt-1">
            {doneCount} / 7 {t("module_journey.phases_word")} · {t("module_journey.status_word")} : <span className="text-[--cvln-orange]">{statusLabel(status, t)}</span>
          </div>
        </div>
        <div className="flex gap-1">
          {PHASE_META.map((p) => (
            <div
              key={p.key}
              data-testid={`phase-pill-${p.key}`}
              className={`w-8 h-8 rounded-full flex items-center justify-center border-2 transition
                ${phase_flags[p.key]
                  ? "bg-[--cvln-orange] border-[--cvln-orange] text-white"
                  : openPhase === p.key
                    ? "bg-white border-[--cvln-orange] text-[--cvln-orange]"
                    : "bg-white border-black/15 text-[--cvln-ink-2]"}`}
              title={p.label}
            >
              <p.icon width={14} height={14} />
            </div>
          ))}
        </div>
      </div>

      {/* Phase stepper */}
      <div className="mt-8 space-y-3" data-testid="phase-stepper">
        {PHASE_META.map((p, idx) => {
          const done = phase_flags[p.key];
          const isOpen = openPhase === p.key;
          const prev = idx === 0 ? true : phase_flags[PHASE_META[idx - 1].key];
          const canOpen = done || prev;
          return (
            <div
              key={p.key}
              data-testid={`phase-${p.key}`}
              className={`cvln-card overflow-hidden transition ${isOpen ? "ring-2 ring-[--cvln-orange]/40" : ""}`}
            >
              <button
                data-testid={`phase-toggle-${p.key}`}
                disabled={!canOpen}
                onClick={() => setOpenPhase(isOpen ? null : p.key)}
                className={`w-full p-5 flex items-center gap-4 text-left transition
                  ${!canOpen ? "opacity-50 cursor-not-allowed" : "hover:bg-black/[0.02]"}`}
              >
                <div className="w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0"
                     style={{ background: done ? "#15803D" : "#F3F4F6", color: done ? "white" : "#525252" }}>
                  {done ? <CheckCircle width={18} height={18} /> : <Circle width={18} height={18} />}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2] font-semibold">
                    {t("module_journey.phase_label")} {idx + 1} / 7
                  </div>
                  <div className="font-semibold text-lg">{p.label}{done ? ` · ${t("module_journey.validated_suffix")}` : ""}</div>
                </div>
                <ArrowRight
                  width={18} height={18}
                  className={`transition ${isOpen ? "rotate-90" : ""} text-[--cvln-ink-2]`}
                />
              </button>

              {isOpen && (
                <div className="px-5 pb-5 -mt-1 border-t border-black/5">
                  <div className="pt-5">
                    {p.key === "hook" && (
                      <PhaseHook phase={phases.hook} done={done} onValidate={() => tickPhase("hook")} />
                    )}
                    {p.key === "objectives" && (
                      <PhaseObjectives phase={phases.objectives} done={done} onValidate={() => tickPhase("objectives")} />
                    )}
                    {p.key === "course" && (
                      <PhaseCourse
                        phase={phases.course}
                        progressPct={module.course_progress_pct || data.progress?.course_progress_pct || 0}
                        onProgress={(pct) => tickPhase("course", { progress_pct: pct })}
                      />
                    )}
                    {p.key === "workshop" && (
                      <PhaseWorkshop phase={phases.workshop} done={done} onValidate={() => tickPhase("workshop")} />
                    )}
                    {p.key === "deliverable" && (
                      <PhaseDeliverable
                        phase={phases.deliverable} done={done}
                        text={deliverableText} setText={setDeliverableText}
                        onSubmit={submitDeliverable}
                      />
                    )}
                    {p.key === "quiz" && (
                      <PhaseQuiz
                        canOpen={phase_flags.deliverable}
                        done={done}
                        quiz={quiz} answers={answers} setAnswers={setAnswers}
                        result={quizResult}
                        onOpen={openQuiz} onSubmit={submitQuiz}
                      />
                    )}
                    {p.key === "mini_mission" && (
                      <PhaseMiniMission
                        phase={phases.mini_mission} done={done}
                        quizPassed={phase_flags.quiz}
                        onCommit={commitMiniMission}
                      />
                    )}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {status === "validated" && (
        <div className="mt-8 cvln-card p-6 bg-gradient-to-br from-[#FFF6EF] to-white border-[--cvln-orange]/40" data-testid="module-validated-banner">
          <div className="text-[11px] mono uppercase tracking-wider font-bold text-[--cvln-orange]">
            {t("module_journey.module_validated_title")}
          </div>
          <h3 className="font-display font-bold text-2xl mt-1">{t("module_journey.ready_next_module")}</h3>
          <button
            data-testid="next-module-btn"
            onClick={() => nav(`/formations/${fc}`)}
            className="btn-primary mt-4"
          >
            {t("module_journey.see_formation")} <ArrowRight width={16} height={16} className="ml-2" />
          </button>
        </div>
      )}
    </div>
  );
}

function statusLabel(s, t) {
  return {
    available: t("module_journey.status_available"),
    in_progress: t("module_journey.status_in_progress"),
    ready_for_quiz: t("module_journey.status_ready_for_quiz"),
    awaiting_mini_mission: t("module_journey.status_awaiting_mini_mission"),
    validated: t("module_journey.status_validated"),
    locked: t("module_journey.status_locked"),
  }[s] || s;
}

/* ---------------- Phase components ---------------- */

function PhaseHook({ phase, done, onValidate }) {
  const { t } = useI18n();
  return (
    <div>
      <p className="text-base leading-relaxed text-[--cvln-ink] whitespace-pre-wrap">
        {phase.narrative}
      </p>
      <button
        data-testid="phase-hook-validate"
        disabled={done}
        onClick={onValidate}
        className="btn-primary mt-5 disabled:opacity-50"
      >
        {done ? t("module_journey.validated_label") : t("module_journey.read_continue")}
      </button>
    </div>
  );
}

function PhaseObjectives({ phase, done, onValidate }) {
  const { t } = useI18n();
  return (
    <div>
      <ul className="space-y-2">
        {phase.items.map((it, i) => (
          <li key={i} className="flex gap-3 items-start" data-testid={`objective-${i}`}>
            <span className="mt-1 w-6 h-6 rounded-full bg-[--cvln-bg-warm] flex items-center justify-center text-xs font-bold text-[--cvln-orange]">{i + 1}</span>
            <span className="text-[--cvln-ink]">{it}</span>
          </li>
        ))}
      </ul>
      <button
        data-testid="phase-objectives-validate"
        disabled={done}
        onClick={onValidate}
        className="btn-primary mt-5 disabled:opacity-50"
      >
        {done ? t("module_journey.validated_label") : t("module_journey.understood_continue")}
      </button>
    </div>
  );
}

function PhaseCourse({ phase, progressPct, onProgress }) {
  const { t } = useI18n();
  const [scrolled80, setScrolled80] = useState(false);
  const onScroll = (e) => {
    const el = e.currentTarget;
    const pct = Math.round(((el.scrollTop + el.clientHeight) / el.scrollHeight) * 100);
    if (pct >= 80 && !scrolled80) setScrolled80(true);
  };
  return (
    <div>
      {/* Video placeholder */}
      <div className="rounded-2xl overflow-hidden border border-black/10 aspect-video bg-gradient-to-br from-[#1a1a1a] to-[#0a0a0a] flex flex-col items-center justify-center text-white p-6" data-testid="video-placeholder">
        <MediaVideo width={40} height={40} className="opacity-40" />
        <div className="text-xs mono uppercase tracking-wider text-white/60 mt-4">
          {t("module_journey.video_placeholder_title")}
        </div>
        <div className="text-sm text-white/80 mt-1 max-w-md text-center">
          {t("module_journey.video_placeholder_studio")} {phase.video_placeholder?.duration_min || 20}min {t("module_journey.duration_planned_suffix")}
        </div>
      </div>

      {/* Reading */}
      <div className="text-xs mono text-[--cvln-ink-2] mt-6 mb-2">
        {t("module_journey.reading_label")} ~{phase.reading_min} min · {t("module_journey.reading_hint")}
      </div>
      <div
        onScroll={onScroll}
        className="prose prose-sm max-w-none border border-black/10 rounded-2xl p-5 max-h-[380px] overflow-y-auto bg-white"
        data-testid="course-content"
      >
        {phase.content_md.split("\n").map((line, i) => {
          if (line.startsWith("## ")) return <h3 key={i} className="font-display font-bold text-xl mt-4 mb-2">{line.slice(3)}</h3>;
          if (line.startsWith("- ")) return <li key={i} className="ml-4">{line.slice(2)}</li>;
          if (/^\d+\./.test(line)) return <p key={i} className="ml-1">{line}</p>;
          if (line.trim().startsWith("**")) return <p key={i} className="font-semibold my-2">{line.replaceAll("**", "")}</p>;
          return <p key={i} className="my-2">{line}</p>;
        })}
      </div>

      <div className="mt-4 h-2 bg-black/5 rounded-full overflow-hidden">
        <div
          className="h-full bg-[--cvln-orange] transition-all"
          style={{ width: `${Math.max(progressPct, scrolled80 ? 100 : 0)}%` }}
        />
      </div>
      <button
        data-testid="phase-course-validate"
        disabled={!scrolled80 && progressPct < 80}
        onClick={() => onProgress(100)}
        className="btn-primary mt-4 disabled:opacity-40"
      >
        {progressPct >= 80 ? t("module_journey.course_validated") : t("module_journey.mark_course_read")}
      </button>
    </div>
  );
}

function PhaseWorkshop({ phase, done, onValidate }) {
  const { t } = useI18n();
  return (
    <div>
      <div className="text-sm text-[--cvln-ink-2] mb-4">
        {t("module_journey.workshop_estimate")} {phase.estimated_min}min · {t("module_journey.workshop_hint")}
      </div>
      <ol className="space-y-3">
        {phase.steps.map((s) => (
          <li key={s.n} className="flex gap-3 items-start" data-testid={`workshop-step-${s.n}`}>
            <span className="w-7 h-7 rounded-full bg-[--cvln-orange] text-white flex items-center justify-center text-xs font-bold flex-shrink-0">{s.n}</span>
            <div>
              <div className="font-semibold">{s.action}</div>
              <div className="text-sm text-[--cvln-ink-2]">{s.detail}</div>
            </div>
          </li>
        ))}
      </ol>
      <button
        data-testid="phase-workshop-validate"
        disabled={done}
        onClick={onValidate}
        className="btn-primary mt-5 disabled:opacity-50"
      >
        {done ? t("module_journey.workshop_done") : t("module_journey.workshop_do")}
      </button>
    </div>
  );
}

function PhaseDeliverable({ phase, done, text, setText, onSubmit }) {
  const { t } = useI18n();
  const min = phase.min_chars;
  return (
    <div>
      <div className="text-[--cvln-ink] whitespace-pre-wrap mb-3">{phase.spec_md.replaceAll("**", "")}</div>
      <textarea
        data-testid="deliverable-textarea"
        rows={8}
        disabled={done}
        placeholder={t("module_journey.deliverable_placeholder")}
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="w-full border-2 border-black/10 rounded-2xl px-4 py-3 focus:outline-none focus:border-[--cvln-orange] focus:ring-2 focus:ring-[--cvln-orange]/30 disabled:bg-black/[0.02]"
      />
      <div className="mt-1 text-xs text-[--cvln-ink-2]">
        {text.length}/{min} {t("module_journey.min_chars")} {text.length >= min ? "· ✓" : ""}
      </div>
      <button
        data-testid="deliverable-submit"
        disabled={done || text.length < min}
        onClick={onSubmit}
        className="btn-primary mt-4 disabled:opacity-40"
      >
        {done ? t("module_journey.deliverable_submitted") : t("module_journey.deliverable_submit")}
      </button>
    </div>
  );
}

function PhaseQuiz({ canOpen, done, quiz, answers, setAnswers, result, onOpen, onSubmit }) {
  const { t } = useI18n();
  if (!canOpen) {
    return (
      <div className="text-sm text-[--cvln-ink-2]">
        {t("module_journey.quiz_need_deliverable")}
      </div>
    );
  }
  if (!quiz && !done) {
    return (
      <button data-testid="phase-quiz-open" onClick={onOpen} className="btn-primary">
        {t("module_journey.quiz_start")}
      </button>
    );
  }
  if (done && !quiz) {
    return <div className="text-sm text-[--cvln-orange] font-semibold">{t("module_journey.quiz_already_passed")}</div>;
  }
  return (
    <div>
      <div className="space-y-4" data-testid="phase-quiz-questions">
        {quiz.quiz.map((q) => (
          <div key={q.n} data-testid={`quiz-q-${q.n}`}>
            <div className="text-xs mono text-[--cvln-ink-2] font-semibold">{q.n} · {q.type}</div>
            <div className="mt-1 font-semibold">{q.question}</div>
            <div className="mt-2 space-y-2">
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
      </div>
      {result && (
        <div
          data-testid="quiz-result"
          className={`mt-4 p-4 rounded-xl ${result.passed ? "bg-[#E7F5EF] text-[#0F4E33]" : "bg-[#FEE7DF] text-[#7B1D0D]"}`}
        >
          <div className="font-bold">
            {result.passed ? t("module_journey.quiz_passed") : t("module_journey.quiz_failed")}
          </div>
          <div className="text-sm mt-1 mono">
            {Math.round(result.score * 100)}% ({result.correct}/{result.total})
            {result.passed && ` · +${result.cc_earned} CC · signal ${result.signal_emitted}`}
          </div>
        </div>
      )}
      <button
        data-testid="quiz-submit"
        onClick={onSubmit}
        disabled={Object.keys(answers).length < quiz.quiz.length}
        className="btn-primary mt-4 disabled:opacity-40"
      >
        {t("quiz_submit")}
      </button>
    </div>
  );
}

function PhaseMiniMission({ phase, done, quizPassed, onCommit }) {
  const { t } = useI18n();
  if (!quizPassed) {
    return (
      <div className="text-sm text-[--cvln-ink-2]">
        {t("module_journey.mini_mission_need_quiz")}
      </div>
    );
  }
  return (
    <div>
      <div className="p-4 rounded-2xl bg-[--cvln-bg-warm] border border-[--cvln-orange]/20">
        <div className="text-[10px] mono uppercase tracking-wider text-[--cvln-orange] font-bold">
          {t("module_journey.mini_mission_field_title")}
        </div>
        <div className="text-[--cvln-ink] mt-2 leading-relaxed">{phase.brief}</div>
      </div>
      <button
        data-testid="mini-mission-commit"
        disabled={done}
        onClick={onCommit}
        className="btn-primary mt-4 disabled:opacity-40"
      >
        {done ? t("module_journey.mini_mission_engaged") : t("module_journey.mini_mission_commit")}
      </button>
    </div>
  );
}
