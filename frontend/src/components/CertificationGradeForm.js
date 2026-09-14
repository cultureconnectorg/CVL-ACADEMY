import { useEffect, useState } from "react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useI18n } from "@/lib/i18n.jsx";

const inputCls =
  "w-24 bg-white border-2 border-black/10 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:border-[--cvln-orange] focus:ring-2 focus:ring-[--cvln-orange]/30";

/** PHYSICAL/HYBRID assessment architecture (2026-09-07) — extracted
 * verbatim from JuryDashboard.js's own `GradeForm` (unchanged
 * behavior/markup) so the trainer-side practical-assessment grading
 * UI (TrainerDashboard.js) and the jury's final-certification grading
 * UI share one real component. `POST /certifications/attempts/{id}/
 * grade` is the exact same endpoint either caller hits — the backend's
 * own RBAC (`_can_grade`) is what actually differentiates a trainer's
 * narrower authority (their own assigned session's "practical" attempt
 * only) from jury/corrector/admin's broader one; this component has
 * no opinion on who may submit it. */
export default function CertificationGradeForm({ attempt, onGraded }) {
  const { t } = useI18n();
  const [rubric, setRubric] = useState(null);
  const [scores, setScores] = useState({});
  const [comments, setComments] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    api.get(`/certifications/${attempt.certification_code}/rubric`).then((r) => setRubric(r.data));
  }, [attempt.certification_code]);

  const submit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.post(`/certifications/attempts/${attempt.id}/grade`, {
        scores: Object.fromEntries(Object.entries(scores).map(([k, v]) => [k, Number(v) || 0])),
        comments,
      });
      toast.success(t("jury_p.graded_success"));
      onGraded();
    } catch {
      toast.error(t("jury_p.grade_error"));
    } finally {
      setSubmitting(false);
    }
  };

  if (!rubric) return <div className="text-sm text-[--cvln-ink-2] px-4 py-3">{t("jury_p.loading_rubric")}</div>;

  return (
    <form onSubmit={submit} className="px-4 py-4 border-t border-black/5 space-y-3" data-testid={`grade-form-${attempt.id}`}>
      {rubric.criteria.map((c) => (
        <div key={c.id} className="flex items-center justify-between gap-3">
          <div className="text-sm">
            {c.label} <span className="text-[--cvln-ink-2]">({c.bloc}, /{c.max_score})</span>
          </div>
          <input
            type="number"
            min={0}
            max={c.max_score}
            step="0.5"
            className={inputCls}
            value={scores[c.id] ?? ""}
            onChange={(e) => setScores({ ...scores, [c.id]: e.target.value })}
            data-testid={`score-${attempt.id}-${c.id}`}
            required
          />
        </div>
      ))}
      <textarea
        rows={2}
        placeholder={t("jury_p.comment_placeholder")}
        className="w-full bg-white border-2 border-black/10 rounded-xl px-4 py-2 text-sm focus:outline-none focus:border-[--cvln-orange] focus:ring-2 focus:ring-[--cvln-orange]/30"
        value={comments}
        onChange={(e) => setComments(e.target.value)}
      />
      <button type="submit" className="btn-primary" disabled={submitting} data-testid={`submit-grade-${attempt.id}`}>
        {submitting ? t("jury_p.sending") : t("jury_p.sign_and_grade")}
      </button>
    </form>
  );
}
