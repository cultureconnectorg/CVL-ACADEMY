import { useEffect, useState } from "react";
import { GraduationCap } from "iconoir-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";

const inputCls =
  "w-full bg-white border-2 border-black/10 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-[--cvln-orange] focus:ring-2 focus:ring-[--cvln-orange]/30";

export default function TrainerDashboard() {
  const { user } = useAuth();
  const { t } = useI18n();
  const [cohorts, setCohorts] = useState([]);
  const [name, setName] = useState("");
  const [pole, setPole] = useState("");
  const [inviteCode, setInviteCode] = useState(null);

  const loadCohorts = () => {
    if (!user?.org_id) return Promise.resolve();
    return api.get(`/orgs/${user.org_id}/cohorts`).then((r) => setCohorts(r.data));
  };

  useEffect(() => {
    loadCohorts().catch(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user?.org_id]);

  const createCohort = async (e) => {
    e.preventDefault();
    try {
      await api.post(`/orgs/${user.org_id}/cohorts`, { name, pole: pole || undefined });
      toast.success(t("trainer_p.cohort_created"));
      setName("");
      setPole("");
      await loadCohorts();
    } catch {
      toast.error(t("trainer_p.cohort_create_error"));
    }
  };

  const inviteStudent = async () => {
    try {
      const { data } = await api.post("/invitations", {
        role: "student",
        org_id: user.org_id,
      });
      setInviteCode(data.code);
    } catch {
      toast.error(t("trainer_p.invite_error"));
    }
  };

  return (
    <div className="px-6 md:px-12 py-10 max-w-4xl" data-testid="trainer-dashboard-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">{t("trainer_p.eyebrow")}</div>
      <h1 className="font-display font-black text-4xl tracking-tighter mt-2">{t("trainer_p.title")}</h1>

      {!user?.org_id ? (
        <div className="cvln-card p-6 mt-8 text-sm text-[--cvln-ink-2]">
          {t("trainer_p.no_org")}
        </div>
      ) : (
        <>
          <div className="cvln-card p-6 mt-8" data-testid="cohorts-panel">
            <h3 className="font-display font-bold text-xl tracking-tight mb-4 flex items-center gap-2">
              <GraduationCap width={18} height={18} className="text-[--cvln-orange]" /> {t("trainer_p.cohorts")}
            </h3>
            {cohorts.length === 0 ? (
              <div className="text-sm text-[--cvln-ink-2] mb-4">{t("trainer_p.no_cohorts")}</div>
            ) : (
              <div className="flex flex-wrap gap-2 mb-4">
                {cohorts.map((c) => (
                  <span key={c.id} className="text-xs px-3 py-1 rounded-full bg-[--cvln-bg-warm]" data-testid={`cohort-${c.id}`}>
                    {c.name} {c.pole ? `· ${c.pole}` : ""}
                  </span>
                ))}
              </div>
            )}
            <form onSubmit={createCohort} className="flex flex-wrap gap-2" data-testid="create-cohort-form">
              <input className={inputCls} placeholder={t("trainer_p.cohort_name_placeholder")} value={name} onChange={(e) => setName(e.target.value)} required />
              <input className={inputCls} placeholder={t("trainer_p.pole_optional_placeholder")} value={pole} onChange={(e) => setPole(e.target.value)} />
              <button type="submit" className="btn-outline whitespace-nowrap">{t("common.create")}</button>
            </form>
          </div>

          <div className="cvln-card p-6 mt-6">
            <h3 className="font-display font-bold text-xl tracking-tight mb-4">{t("trainer_p.invite_student_title")}</h3>
            <button className="btn-primary" onClick={inviteStudent}>{t("trainer_p.generate_invite")}</button>
            {inviteCode && (
              <div className="mt-3 text-sm mono px-4 py-2 rounded-xl bg-[--cvln-bg-warm]" data-testid="trainer-invite-code">
                {t("trainer_p.code_label")} : <strong>{inviteCode}</strong>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}
