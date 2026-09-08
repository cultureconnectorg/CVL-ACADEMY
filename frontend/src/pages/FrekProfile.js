import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { computeDepthStyle } from "@/lib/spatial/attention";
import { useDepthPhysics } from "@/lib/useDepthPhysics";
import { useReducedMotion } from "@/lib/useReducedMotion";

/** ACA-0014/ACA-0017 (H1 sequencing step 4, `SPATIAL_H1_INTEGRATION_
 * PLAN.md` — "FREK Profile: convert to the identity-first, non-KPI-
 * card treatment; real FREK-ID and stage already exist as data") —
 * the identity card above this grid is already identity-first; this
 * wrapper is what converts the signals grid itself away from 8
 * uniformly-weighted KPI tiles, same useDepthPhysics/computeDepthStyle
 * engine Roadmap/Badges/Missions already established. */
function SignalDepthCard({ s, i, primaryIdx, value, reduced }) {
  const targetDistance = primaryIdx === -1 ? 0 : i - primaryIdx;
  const distance = useDepthPhysics(targetDistance, { reduced });
  const depth = computeDepthStyle(distance);
  const style = reduced
    ? { opacity: depth.opacity, transform: `scale(${Math.max(depth.scale, 0.96)})` }
    : {
        opacity: depth.opacity,
        filter: `saturate(${depth.saturate}) contrast(${depth.contrast})`,
        transform: `scale(${depth.scale})`,
        zIndex: depth.zIndex,
      };
  return (
    <motion.div
      data-testid={`signal-${s.k}`}
      data-tier={depth.tier}
      style={style}
      className="cvln-card p-5"
    >
      <div className="mono text-xs text-[--cvln-orange] font-bold">{s.k}</div>
      <div className="font-display font-black text-3xl tracking-tighter mt-1">{value}</div>
      <div className="text-xs text-[--cvln-ink-2] mt-2">{s.desc}</div>
    </motion.div>
  );
}

export default function FrekProfile() {
  const { user } = useAuth();
  const { t } = useI18n();
  const reduced = useReducedMotion();
  const [prof, setProf] = useState(null);
  // ACA-0028 — real composed professional identity (skills genuinely
  // acquired + certifications genuinely passed, see services/
  // professional_profile.py). Fetched independently of `/frek/profile`
  // — a failure here never blocks the rest of this already-real page.
  const [proProfile, setProProfile] = useState(null);
  const [visibilityBusy, setVisibilityBusy] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    api.get("/frek/profile").then(r => setProf(r.data));
    api.get("/professional/profile/mine").then(r => setProProfile(r.data)).catch(() => {});
  }, []);

  const toggleVisibility = async () => {
    if (!proProfile) return;
    setVisibilityBusy(true);
    try {
      const nextPublic = !proProfile.is_public;
      await api.post("/professional/profile/visibility", { is_public: nextPublic });
      setProProfile((p) => ({ ...p, is_public: nextPublic }));
    } finally {
      setVisibilityBusy(false);
    }
  };

  const publicUrl = user?.frek_id
    ? `${window.location.origin}/id/${user.frek_id}`
    : "";
  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(publicUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Clipboard API unavailable — the link is still shown as text.
    }
  };

  const SIGNALS = [
    { k: "FREK-TIME", desc: t("frek_profile_p.sig_time") },
    { k: "FREK-WORK", desc: t("frek_profile_p.sig_work") },
    { k: "FREK-SCORE", desc: t("frek_profile_p.sig_score") },
    { k: "FREK-LINK", desc: t("frek_profile_p.sig_link") },
    { k: "FREK-CERT", desc: t("frek_profile_p.sig_cert") },
    { k: "FREK-CONTRIB", desc: t("frek_profile_p.sig_contrib") },
    { k: "FREK-MISSION", desc: t("frek_profile_p.sig_mission") },
    { k: "FREK-SHARE", desc: t("frek_profile_p.sig_share") },
  ];

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="frek-profile-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">{t("frek_profile")}</div>
      <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-2">
        {t("frek_profile_p.hero_title")}
      </h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">
        {t("frek_profile_p.hero_p")}
      </p>

      {/* Identity card */}
      <div className="mt-10 cvln-card p-8 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-40 h-40 rounded-full bg-[--cvln-orange]/10 -translate-y-8 translate-x-8" />
        <div className="relative z-10 grid md:grid-cols-3 gap-6 items-center">
          <div className="md:col-span-2">
            <div className="text-[11px] mono uppercase tracking-[0.25em] text-[--cvln-ink-2] font-bold">
              {t("frek_profile_p.sovereign_identity")}
            </div>
            <div className="mono font-black text-4xl md:text-5xl tracking-tight mt-2">{user?.frek_id}</div>
            <div className="text-lg mt-1">{user?.display_name}</div>
            <div className="text-sm text-[--cvln-ink-2] mt-1">{user?.email}</div>
            <div className="mt-4 flex flex-wrap gap-2">
              <span className="stade-chip">{t("frek_profile_p.stade_label")} {t(`stades.${user?.stade}`)}</span>
              <span className="stade-chip">{user?.cc_credits} CC</span>
              <span className="stade-chip">{t("frek_profile_p.lang_label")} {user?.lang?.toUpperCase()}</span>
            </div>
          </div>
          <div className="text-right">
            <div className="text-xs text-[--cvln-ink-2] mono">
              {t("frek_profile_p.stade_next_at")} <strong>{prof?.stade_next_at}</strong> {t("frek_profile_p.cc_word")}
            </div>
            <div className="stage-line mt-2">
              <div style={{ width: `${prof?.stade_progress_pct ?? 0}%` }} />
            </div>
            <div className="mt-1 text-xs text-[--cvln-ink-2] mono">
              {prof?.stade_progress_pct ?? 0}{t("frek_profile_p.stade_progress")}
            </div>
          </div>
        </div>
      </div>

      {/* CAN-01/CAN-02 convergence (P0-G backend, `/frek/profile`'s
          `canonical` field) — GLOBAL_PROGRESS (reconciliation 2026-09-07):
          canonical_progress -> learning-path -> FREK profile. Same
          honestly-labeled, never-blended-into-legacy pattern as
          Dashboard.js's card-canonical-progress — canonical content
          *viewed*, never relabeled *completed*. */}
      {prof?.canonical?.canonical_modules_total > 0 && (
        <div className="mt-8 cvln-card p-6" data-testid="frek-canonical-progress">
          <div className="flex items-center justify-between text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-ink-2]">
            <span>{t("canonical_progress")}</span>
            <span className="text-[--cvln-orange]">{prof.canonical.canonical_progress_pct}%</span>
          </div>
          <div className="stage-line mt-3">
            <div style={{ width: `${prof.canonical.canonical_progress_pct}%` }} />
          </div>
          <div className="mt-2 text-xs text-[--cvln-ink-2]">
            {prof.canonical.canonical_modules_viewed}/{prof.canonical.canonical_modules_total}{" "}
            {t("canonical_modules_viewed")}
          </div>
          <div className="mt-1 text-[10px] text-[--cvln-ink-2]">
            {t("canonical_progress_hint")}
          </div>
        </div>
      )}

      {/* ACA-0028 — Professional identity surface: real acquired
          skills + real passed certifications, composed by
          services/professional_profile.py from the already-existing
          Skill Engine and Certification Engine — nothing invented,
          nothing re-derived differently here. */}
      {proProfile && (
        <div className="mt-8 cvln-card p-6" data-testid="professional-profile-card">
          <div className="flex items-center justify-between flex-wrap gap-3">
            <h3 className="font-display font-bold text-2xl tracking-tight">
              {t("frek_profile_p.professional_title")}
            </h3>
            <button
              type="button"
              onClick={toggleVisibility}
              disabled={visibilityBusy}
              data-testid="visibility-toggle"
              className="stade-chip cursor-pointer disabled:opacity-50"
            >
              {proProfile.is_public
                ? t("frek_profile_p.visibility_public")
                : t("frek_profile_p.visibility_private")}
            </button>
          </div>
          <p className="text-xs text-[--cvln-ink-2] mt-2">{t("frek_profile_p.visibility_hint")}</p>

          {proProfile.is_public && (
            <div className="mt-3 flex items-center gap-2 flex-wrap">
              <code className="text-xs mono bg-[--cvln-bg-warm] px-3 py-1.5 rounded-lg" data-testid="public-profile-url">
                {publicUrl}
              </code>
              <button
                type="button"
                onClick={copyLink}
                data-testid="copy-public-link"
                className="text-xs font-semibold text-[--cvln-orange]"
              >
                {copied ? "✓" : t("frek_profile_p.copy_link")}
              </button>
            </div>
          )}

          <div className="mt-5">
            <div className="text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-ink-2] mb-2">
              {t("frek_profile_p.acquired_skills")}
            </div>
            {proProfile.acquired_skills.length === 0 ? (
              <div className="text-sm text-[--cvln-ink-2]">{t("frek_profile_p.no_acquired_skills")}</div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {proProfile.acquired_skills.map((s) => (
                  <div key={s.skill_id} className="p-3 rounded-xl border border-black/10" data-testid={`acquired-skill-${s.skill_id}`}>
                    <div className="mono text-xs text-[--cvln-orange] font-bold">{s.skill_id}</div>
                    <div className="text-sm font-semibold">{s.label}</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="mt-5">
            <div className="text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-ink-2] mb-2">
              {t("frek_profile_p.certifications_title")}
            </div>
            {proProfile.certifications.length === 0 ? (
              <div className="text-sm text-[--cvln-ink-2]">{t("frek_profile_p.no_certifications")}</div>
            ) : (
              <div className="space-y-2">
                {proProfile.certifications.map((c) => (
                  <div
                    key={c.certification_code}
                    className="flex items-center justify-between p-3 rounded-xl border border-black/10"
                    data-testid={`acquired-cert-${c.certification_code}`}
                  >
                    <span className="mono font-bold">{c.certification_code}</span>
                    <span className="text-sm text-[--cvln-ink-2]">{c.mention}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Signals grid — ACA-0014/0017: the real "what matters now" anchor
          is the signal with the highest real count (the learner's own
          most-active real trait), never a fabricated ranking. All-zero
          (fresh account) falls back to no forced primary. */}
      <div className="mt-8 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {(() => {
          const values = SIGNALS.map((s) => user?.signals?.[s.k] ?? 0);
          const maxVal = Math.max(0, ...values);
          const primaryIdx = maxVal > 0 ? values.indexOf(maxVal) : -1;
          return SIGNALS.map((s, i) =>
            FEATURE_FLAGS.SPATIAL_HUB_ENABLED ? (
              <SignalDepthCard
                key={s.k}
                s={s}
                i={i}
                primaryIdx={primaryIdx}
                value={values[i]}
                reduced={reduced}
              />
            ) : (
              <div key={s.k} className="cvln-card p-5" data-testid={`signal-${s.k}`}>
                <div className="mono text-xs text-[--cvln-orange] font-bold">{s.k}</div>
                <div className="font-display font-black text-3xl tracking-tighter mt-1">
                  {values[i]}
                </div>
                <div className="text-xs text-[--cvln-ink-2] mt-2">{s.desc}</div>
              </div>
            )
          );
        })()}
      </div>

      {/* Signal log */}
      <div className="mt-8 cvln-card p-6">
        <h3 className="font-display font-bold text-2xl tracking-tight mb-4">{t("frek_profile_p.signal_log")}</h3>
        {(prof?.recent_signals ?? []).length === 0 ? (
          <div className="text-sm text-[--cvln-ink-2]">
            {t("frek_profile_p.no_signals")}
          </div>
        ) : (
          <div className="space-y-1 mono text-sm">
            {(prof.recent_signals || []).map((s, i) => (
              <div key={i} className="flex items-center justify-between px-2 py-1.5 rounded-lg hover:bg-[--cvln-bg-warm]">
                <span className="text-[--cvln-orange] font-bold">{s.signal}</span>
                <span className="text-[--cvln-ink-2] truncate max-w-[50%]">
                  {s.meta?.module || s.meta?.mission || s.meta?.reason || "—"}
                </span>
                <span className="text-[--cvln-ink-2] text-xs">
                  {new Date(s.ts).toLocaleString()}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
