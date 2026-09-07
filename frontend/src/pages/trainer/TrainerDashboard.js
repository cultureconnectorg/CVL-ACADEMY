import { useEffect, useState } from "react";
import { GraduationCap, Calendar, Check, Xmark } from "iconoir-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";
import CertificationGradeForm from "@/components/CertificationGradeForm";

const inputCls =
  "w-full bg-white border-2 border-black/10 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-[--cvln-orange] focus:ring-2 focus:ring-[--cvln-orange]/30";

/** PHYSICAL/HYBRID assessment architecture (Founder decision,
 * 2026-09-07) — trainer/staff side: view roster, mark attendance,
 * record practical assessment. Every row here is real, server-backed
 * state (`GET /physical-sessions/{id}/roster`,
 * `GET /certifications/attempts/pending`) — never fabricated. RBAC
 * lives entirely server-side (`api/physical_sessions.py`'s
 * `_assert_session_staff`, `api/certification.py`'s `_can_grade`) —
 * this component only renders what the backend already scoped to this
 * user; a session/attempt that isn't theirs simply never appears in
 * `/physical-sessions/assigned` or the filtered pending queue.
 */
function SessionRoster({ session, locationsById, pendingPractical, onChanged }) {
  const { t } = useI18n();
  const [open, setOpen] = useState(false);
  const [roster, setRoster] = useState(null);
  const [gradingId, setGradingId] = useState(null);

  const loadRoster = () => {
    api.get(`/physical-sessions/${session.id}/roster`).then((r) => setRoster(r.data));
  };

  useEffect(() => {
    if (open && !roster) loadRoster();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  const markAttendance = async (userId, present) => {
    try {
      await api.post(`/physical-sessions/${session.id}/attendance/${userId}`, null, {
        params: { present },
      });
      toast.success(t("trainer_p.physical_attendance_saved"));
      loadRoster();
    } catch {
      toast.error(t("trainer_p.physical_attendance_error"));
    }
  };

  const location = locationsById[session.location_id];
  const sessionPending = pendingPractical.filter((a) => a.session_id === session.id);

  return (
    <div className="cvln-card overflow-hidden" data-testid={`trainer-session-${session.id}`}>
      <button
        className="w-full flex items-center justify-between gap-4 p-5 text-left"
        onClick={() => setOpen(!open)}
      >
        <div className="flex items-center gap-3 min-w-0">
          <Calendar width={20} height={20} className="text-[--cvln-orange] shrink-0" />
          <div className="min-w-0">
            <div className="font-semibold truncate">
              {session.formation_code}
              {location ? ` · ${location.name}` : ""}
            </div>
            <div className="text-xs text-[--cvln-ink-2]">
              {new Date(session.starts_at).toLocaleString()} · {session.enrolled_count}/{session.capacity}
            </div>
          </div>
        </div>
        <span className="text-sm text-[--cvln-orange] font-semibold shrink-0">
          {open ? t("jury_p.close") : t("trainer_p.physical_view_roster")}
        </span>
      </button>

      {open && (
        <div className="px-5 pb-5 border-t border-black/5 pt-4 space-y-2">
          {!roster ? (
            <div className="text-sm text-[--cvln-ink-2]">…</div>
          ) : roster.length === 0 ? (
            <div className="text-sm text-[--cvln-ink-2]">{t("trainer_p.physical_no_enrollments")}</div>
          ) : (
            roster.map((row) => (
              <div
                key={row.user_id}
                className="flex items-center justify-between gap-3 py-2 border-b border-black/5 last:border-0"
                data-testid={`roster-row-${session.id}-${row.user_id}`}
              >
                <div className="min-w-0">
                  <div className="text-sm font-semibold truncate">{row.display_name}</div>
                  <div className="text-xs text-[--cvln-ink-2] mono">{row.frek_id}</div>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  {row.present === true && (
                    <span className="text-xs font-bold text-[#15803D]">{t("trainer_p.physical_present")}</span>
                  )}
                  {row.present === false && (
                    <span className="text-xs font-bold text-[--cvln-orange]">{t("trainer_p.physical_absent")}</span>
                  )}
                  <button
                    className="w-8 h-8 rounded-full bg-[#DCFCE7] text-[#15803D] flex items-center justify-center"
                    title={t("trainer_p.physical_mark_present")}
                    data-testid={`mark-present-${session.id}-${row.user_id}`}
                    onClick={() => markAttendance(row.user_id, true)}
                  >
                    <Check width={16} height={16} />
                  </button>
                  <button
                    className="w-8 h-8 rounded-full bg-black/5 text-[--cvln-ink-2] flex items-center justify-center"
                    title={t("trainer_p.physical_mark_absent")}
                    data-testid={`mark-absent-${session.id}-${row.user_id}`}
                    onClick={() => markAttendance(row.user_id, false)}
                  >
                    <Xmark width={16} height={16} />
                  </button>
                </div>
              </div>
            ))
          )}

          {sessionPending.length > 0 && (
            <div className="mt-4 pt-4 border-t border-black/5">
              <div className="text-xs uppercase tracking-wider font-bold text-[--cvln-ink-2] mb-2">
                {t("trainer_p.physical_pending_assessments")}
              </div>
              <div className="space-y-2">
                {sessionPending.map((a) => (
                  <div key={a.id} className="rounded-xl border border-black/10 overflow-hidden">
                    <button
                      className="w-full flex items-center justify-between p-3 text-left text-sm"
                      onClick={() => setGradingId(gradingId === a.id ? null : a.id)}
                    >
                      <span>{a.certification_code}</span>
                      <span className="text-[--cvln-orange] font-semibold">
                        {gradingId === a.id ? t("jury_p.close") : t("jury_p.grade")}
                      </span>
                    </button>
                    {gradingId === a.id && (
                      <CertificationGradeForm
                        attempt={a}
                        onGraded={() => { setGradingId(null); onChanged(); }}
                      />
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function TrainerDashboard() {
  const { user } = useAuth();
  const { t } = useI18n();
  const [cohorts, setCohorts] = useState([]);
  const [name, setName] = useState("");
  const [pole, setPole] = useState("");
  const [inviteCode, setInviteCode] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [locationsById, setLocationsById] = useState({});
  const [pendingPractical, setPendingPractical] = useState([]);

  const loadCohorts = () => {
    if (!user?.org_id) return Promise.resolve();
    return api.get(`/orgs/${user.org_id}/cohorts`).then((r) => setCohorts(r.data));
  };

  const loadPhysicalSessions = () =>
    Promise.all([
      api.get("/physical-sessions/assigned").then((r) => r.data),
      api.get("/physical-locations").then((r) => r.data),
      api.get("/certifications/attempts/pending").then((r) => r.data),
    ]).then(([s, locs, pending]) => {
      setSessions(s);
      setLocationsById(Object.fromEntries(locs.map((l) => [l.id, l])));
      setPendingPractical(pending.filter((a) => a.assessment_kind === "practical"));
    });

  useEffect(() => {
    loadCohorts().catch(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user?.org_id]);

  useEffect(() => {
    loadPhysicalSessions().catch(() => toast.error(t("trainer_p.physical_load_error")));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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

      <div className="mt-6" data-testid="physical-sessions-panel">
        <h3 className="font-display font-bold text-xl tracking-tight mb-4 flex items-center gap-2">
          <Calendar width={18} height={18} className="text-[--cvln-orange]" /> {t("trainer_p.physical_sessions_title")}
        </h3>
        {sessions.length === 0 ? (
          <div className="cvln-card p-6 text-sm text-[--cvln-ink-2]">{t("trainer_p.physical_no_sessions")}</div>
        ) : (
          <div className="space-y-3">
            {sessions.map((s) => (
              <SessionRoster
                key={s.id}
                session={s}
                locationsById={locationsById}
                pendingPractical={pendingPractical}
                onChanged={loadPhysicalSessions}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
