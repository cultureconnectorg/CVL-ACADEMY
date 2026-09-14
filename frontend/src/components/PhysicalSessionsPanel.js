import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Calendar, MapPin, Group } from "iconoir-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";

/** PHYSICAL/HYBRID assessment architecture (Founder decision,
 * 2026-09-07) — the learner-facing half of the real chain: formation
 * → delivery mode → real session → location/date/capacity →
 * enrollment → attendance → practical assessment when required →
 * evidence → competency result → certification eligibility. Every row
 * here is real, server-backed state; a formation with no scheduled
 * session renders nothing false — it simply shows none.
 *
 * ATTENDANCE != ASSESSMENT: the "start practical assessment" action
 * only ever appears once `enrollment_status === "attended"` — a real,
 * trainer-recorded fact — and only when a real "practical"-kind rubric
 * exists for this formation (never fabricated). Starting it is gated
 * server-side (`start_practical_attempt`) on the exact same real
 * attendance record.
 */
export default function PhysicalSessionsPanel({ formationCode }) {
  const { t } = useI18n();
  const { user } = useAuth();
  const [sessions, setSessions] = useState(null);
  const [locationsById, setLocationsById] = useState({});
  const [myEnrollments, setMyEnrollments] = useState([]);
  const [practicalRubric, setPracticalRubric] = useState(null);
  const [myAttempts, setMyAttempts] = useState([]);
  const [busyId, setBusyId] = useState(null);

  const load = async () => {
    const [s, locs] = await Promise.all([
      api.get(`/formations/${formationCode}/physical-sessions`).then((r) => r.data),
      api.get("/physical-locations").then((r) => r.data),
    ]);
    setSessions(s);
    setLocationsById(Object.fromEntries(locs.map((l) => [l.id, l])));

    if (user) {
      const [enrollments, rubrics, attempts] = await Promise.all([
        api.get("/physical-sessions/mine").then((r) => r.data),
        api.get("/certifications/rubrics").then((r) => r.data),
        api.get("/certifications/attempts/mine").then((r) => r.data),
      ]);
      setMyEnrollments(enrollments);
      setPracticalRubric(
        rubrics.find((r) => r.formation_code === formationCode && r.assessment_kind === "practical") || null
      );
      setMyAttempts(attempts);
    }
  };

  useEffect(() => {
    load().catch(() => toast.error(t("formation_detail_p.physical_load_error")));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [formationCode, user?.id]);

  if (!sessions || sessions.length === 0) return null;

  const enrollmentBySession = Object.fromEntries(myEnrollments.map((e) => [e.session_id, e]));
  const myPracticalAttempt = practicalRubric
    ? myAttempts.find((a) => a.certification_code === practicalRubric.certification_code)
    : null;

  const enroll = async (sessionId) => {
    setBusyId(sessionId);
    try {
      await api.post(`/physical-sessions/${sessionId}/enroll`);
      toast.success(t("formation_detail_p.physical_enrolled"));
      await load();
    } catch {
      toast.error(t("formation_detail_p.physical_enroll_error"));
    } finally {
      setBusyId(null);
    }
  };

  const cancel = async (sessionId) => {
    setBusyId(sessionId);
    try {
      await api.post(`/physical-sessions/${sessionId}/cancel-enrollment`);
      toast.success(t("formation_detail_p.physical_cancelled"));
      await load();
    } catch {
      toast.error(t("formation_detail_p.physical_cancel_error"));
    } finally {
      setBusyId(null);
    }
  };

  const startPractical = async (sessionId) => {
    setBusyId(sessionId);
    try {
      await api.post(`/certifications/${practicalRubric.certification_code}/practical-attempts`, {
        session_id: sessionId,
      });
      toast.success(t("formation_detail_p.physical_practical_started"));
      await load();
    } catch (e) {
      toast.error(e?.response?.data?.detail || t("formation_detail_p.physical_practical_error"));
    } finally {
      setBusyId(null);
    }
  };

  const ENROLLMENT_LABEL = {
    enrolled: t("formation_detail_p.physical_status_enrolled"),
    waitlisted: t("formation_detail_p.physical_status_waitlisted"),
    attended: t("formation_detail_p.physical_status_attended"),
    no_show: t("formation_detail_p.physical_status_no_show"),
  };

  return (
    <div className="mt-12" data-testid="physical-sessions-panel">
      <h2 className="font-display font-bold text-2xl md:text-3xl tracking-tight">
        {t("formation_detail_p.physical_sessions_title")}
      </h2>
      <div className="text-sm text-[--cvln-ink-2] mt-1">{t("formation_detail_p.physical_sessions_hint")}</div>

      <div className="mt-6 grid gap-3">
        {sessions.map((s) => {
          const location = locationsById[s.location_id];
          const enrollment = enrollmentBySession[s.id];
          const full = s.status === "full" && !enrollment;
          return (
            <div key={s.id} className="cvln-card p-5 flex items-center gap-5 flex-wrap" data-testid={`physical-session-${s.id}`}>
              <div className="w-10 h-10 rounded-full bg-[--cvln-bg-warm] flex items-center justify-center text-[--cvln-orange] shrink-0">
                <Calendar width={18} height={18} />
              </div>
              <div className="min-w-0 flex-1">
                <div className="font-semibold">{new Date(s.starts_at).toLocaleString()}</div>
                {location && (
                  <div className="text-sm text-[--cvln-ink-2] mt-0.5 flex items-center gap-1">
                    <MapPin width={14} height={14} /> {location.name} · {location.city}
                  </div>
                )}
                <div className="text-xs text-[--cvln-ink-2] mt-1 flex items-center gap-1">
                  <Group width={14} height={14} /> {s.enrolled_count}/{s.capacity}
                  {enrollment && (
                    <span className="ml-2 font-bold text-[--cvln-orange]">
                      {ENROLLMENT_LABEL[enrollment.status]}
                    </span>
                  )}
                </div>
              </div>

              {!user ? (
                <Link to="/" className="btn-outline text-sm shrink-0">
                  {t("formation_detail_p.physical_signin_to_enroll")}
                </Link>
              ) : !enrollment ? (
                <button
                  className="btn-primary text-sm shrink-0"
                  disabled={busyId === s.id || full}
                  onClick={() => enroll(s.id)}
                  data-testid={`enroll-${s.id}`}
                >
                  {full ? t("formation_detail_p.physical_full") : t("formation_detail_p.physical_enroll")}
                </button>
              ) : enrollment.status === "attended" && practicalRubric && !myPracticalAttempt ? (
                <button
                  className="btn-primary text-sm shrink-0"
                  disabled={busyId === s.id}
                  onClick={() => startPractical(s.id)}
                  data-testid={`start-practical-${s.id}`}
                >
                  {t("formation_detail_p.physical_start_practical")}
                </button>
              ) : enrollment.status === "attended" && myPracticalAttempt ? (
                <Link to="/certifications" className="btn-outline text-sm shrink-0">
                  {t("formation_detail_p.physical_view_certification")}
                </Link>
              ) : (
                ["enrolled", "waitlisted"].includes(enrollment.status) && (
                  <button
                    className="btn-outline text-sm shrink-0"
                    disabled={busyId === s.id}
                    onClick={() => cancel(s.id)}
                    data-testid={`cancel-enrollment-${s.id}`}
                  >
                    {t("formation_detail_p.physical_cancel")}
                  </button>
                )
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
