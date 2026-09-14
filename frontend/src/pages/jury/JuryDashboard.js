import { useEffect, useState } from "react";
import { Medal1st } from "iconoir-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useI18n } from "@/lib/i18n.jsx";
import CertificationGradeForm from "@/components/CertificationGradeForm";

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
                <CertificationGradeForm attempt={a} onGraded={() => { setOpenId(null); load(); }} />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
