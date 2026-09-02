import { useEffect, useState } from "react";
import { Medal1st, Download } from "iconoir-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useI18n } from "@/lib/i18n.jsx";

export default function Certifications() {
  const { t } = useI18n();
  const [attempts, setAttempts] = useState([]);
  const [rubrics, setRubrics] = useState([]);
  const [loading, setLoading] = useState(true);

  const STATUS_LABELS = {
    in_progress: t("certifications_p.status_in_progress"),
    submitted: t("certifications_p.status_submitted"),
    graded: t("certifications_p.status_graded"),
    passed: t("certifications_p.status_passed"),
    failed: t("certifications_p.status_failed"),
  };

  const load = async () => {
    const [a, r] = await Promise.all([
      api.get("/certifications/attempts/mine").then((res) => res.data),
      api.get("/certifications/rubrics").then((res) => res.data),
    ]);
    setAttempts(a);
    setRubrics(r);
    setLoading(false);
  };

  useEffect(() => {
    load().catch(() => {
      toast.error(t("certifications_p.load_error"));
      setLoading(false);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const startAttempt = async (code) => {
    try {
      await api.post(`/certifications/${code}/attempts`);
      toast.success(t("certifications_p.created"));
      await load();
    } catch {
      toast.error(t("certifications_p.start_error"));
    }
  };

  const downloadAttestation = (attemptId) => {
    // Fetched as a blob (not a plain <a href>) so the request carries the
    // same Authorization header as every other API call.
    api
      .get(`/certifications/attempts/${attemptId}/attestation.pdf`, { responseType: "blob" })
      .then((res) => {
        const url = URL.createObjectURL(res.data);
        window.open(url, "_blank");
      })
      .catch(() => toast.error(t("certifications_p.attestation_unavailable")));
  };

  if (loading) return <div className="p-10 text-[--cvln-ink-2]">…</div>;

  const startedCodes = new Set(attempts.map((a) => a.certification_code));

  return (
    <div className="px-6 md:px-12 py-10 max-w-5xl" data-testid="certifications-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">{t("certifications_p.eyebrow")}</div>
      <h1 className="font-display font-black text-4xl tracking-tighter mt-2">{t("certifications_p.title")}</h1>

      {attempts.length === 0 && (
        <div className="cvln-card p-6 mt-8 text-sm text-[--cvln-ink-2]">{t("certifications_p.none")}</div>
      )}

      <div className="space-y-3 mt-6">
        {attempts.map((a) => (
          <div key={a.id} className="cvln-card p-5 flex items-center justify-between gap-4" data-testid={`attempt-${a.id}`}>
            <div className="flex items-center gap-3 min-w-0">
              <Medal1st width={22} height={22} className="text-[--cvln-orange] shrink-0" />
              <div className="min-w-0">
                <div className="font-semibold truncate">
                  {a.certification_code} · {a.level} — {t("certifications_p.attempt")} #{a.attempt_number}
                </div>
                <div className="text-xs text-[--cvln-ink-2]">
                  {STATUS_LABELS[a.status]}
                  {a.status !== "in_progress" && a.status !== "submitted" ? ` · ${t("certifications_p.score")} ${a.score_global}%` : ""}
                </div>
              </div>
            </div>
            {a.passed && (
              <button
                className="btn-outline shrink-0"
                data-testid={`download-attestation-${a.id}`}
                onClick={() => downloadAttestation(a.id)}
              >
                <Download width={16} height={16} className="mr-2" /> {t("certifications_p.attestation")}
              </button>
            )}
          </div>
        ))}
      </div>

      {rubrics.length > 0 && (
        <>
          <h3 className="font-display font-bold text-xl tracking-tight mt-10 mb-4">{t("certifications_p.available_title")}</h3>
          <div className="space-y-3">
            {rubrics
              .filter((r) => !startedCodes.has(r.certification_code))
              .map((r) => (
                <div
                  key={r.certification_code}
                  className="cvln-card p-5 flex items-center justify-between gap-4"
                  data-testid={`rubric-${r.certification_code}`}
                >
                  <div>
                    <div className="font-semibold">{r.certification_code} · {r.level}</div>
                    <div className="text-xs text-[--cvln-ink-2]">{t("certifications_p.pass_threshold")} : {r.pass_threshold_pct}%</div>
                  </div>
                  <button className="btn-primary" onClick={() => startAttempt(r.certification_code)}>
                    {t("common.start")}
                  </button>
                </div>
              ))}
          </div>
        </>
      )}
    </div>
  );
}
