import { useEffect, useState } from "react";
import { Medal1st } from "iconoir-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useI18n } from "@/lib/i18n.jsx";

const inputCls =
  "w-24 bg-white border-2 border-black/10 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:border-[--cvln-orange]";

function GradeForm({ attempt, onGraded }) {
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
        className="w-full bg-white border-2 border-black/10 rounded-xl px-4 py-2 text-sm focus:outline-none focus:border-[--cvln-orange]"
        value={comments}
        onChange={(e) => setComments(e.target.value)}
      />
      <button type="submit" className="btn-primary" disabled={submitting} data-testid={`submit-grade-${attempt.id}`}>
        {submitting ? t("jury_p.sending") : t("jury_p.sign_and_grade")}
      </button>
    </form>
  );
}

export default function JuryDashboard() {
  const { t } = useI18n();
  const [pending, setPending] = useState([]);
  const [openId, setOpenId] = useState(null);

  const load = () => api.get("/certifications/attempts/pending").then((r) => setPending(r.data));

  useEffect(() => {
    load().catch(() => toast.error(t("jury_p.load_error")));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="px-6 md:px-12 py-10 max-w-4xl" data-testid="jury-dashboard-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">{t("jury_p.eyebrow")}</div>
      <h1 className="font-display font-black text-4xl tracking-tighter mt-2">{t("jury_p.title")}</h1>

      {pending.length === 0 ? (
        <div className="cvln-card p-6 mt-8 text-sm text-[--cvln-ink-2]">{t("jury_p.none_pending")}</div>
      ) : (
        <div className="space-y-3 mt-8">
          {pending.map((a) => (
            <div key={a.id} className="cvln-card overflow-hidden" data-testid={`pending-attempt-${a.id}`}>
              <button
                className="w-full flex items-center justify-between gap-4 p-5 text-left"
                onClick={() => setOpenId(openId === a.id ? null : a.id)}
              >
                <div className="flex items-center gap-3">
                  <Medal1st width={20} height={20} className="text-[--cvln-orange]" />
                  <div>
                    <div className="font-semibold">{a.certification_code} · {a.level}</div>
                    <div className="text-xs text-[--cvln-ink-2]">{t("jury_p.submitted_on")} {a.submitted_at}</div>
                  </div>
                </div>
                <span className="text-sm text-[--cvln-orange] font-semibold">
                  {openId === a.id ? t("jury_p.close") : t("jury_p.grade")}
                </span>
              </button>
              {openId === a.id && (
                <GradeForm attempt={a} onGraded={() => { setOpenId(null); load(); }} />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
