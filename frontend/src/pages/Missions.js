import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";
import { toast } from "sonner";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { computeDepthStyle } from "@/lib/spatial/attention";
import { useDepthPhysics } from "@/lib/useDepthPhysics";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { createSpatialAudio } from "@/lib/spatial/audio";
import { createHaptics } from "@/lib/spatial/haptics";

/** ACA-0014/ACA-0017 (H1 sequencing step 4, `SPATIAL_H1_INTEGRATION_
 * PLAN.md` — "Missions: convert from its current presentation to the
 * glanceable-list treatment validated here (no card grid). Real
 * mission data/status already exists server-side; only the render
 * changes") — same useDepthPhysics/computeDepthStyle wrapper Roadmap/
 * Badges already established, applied to a vertical list instead of a
 * grid: PS5's "cards, not pages" principle already cited in
 * ACADEMY_HERO_ENTRY_RESEARCH.md §C — one dominant, actionable thing,
 * the rest genuinely present but secondary, never a flat grid. */
function MissionDepthCard({ m, i, primaryIdx, s, reduced, t, accept, submit }) {
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
      data-testid={`mission-${m.code}`}
      data-tier={depth.tier}
      style={style}
      className="cvln-card p-6 flex flex-col"
    >
      <MissionCardBody m={m} s={s} t={t} accept={accept} submit={submit} />
    </motion.div>
  );
}

/** Shared card body — identical markup whichever wrapper (the plain
 * grid or the continuous-depth list) renders it, same discipline as
 * Roadmap.js's StageCardBody / Badges.js's BadgeCardBody. */
function MissionCardBody({ m, s, t, accept, submit }) {
  return (
    <>
      <div className="flex items-center justify-between">
        <div className="text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2]">
          {m.pole} · {m.entity}
        </div>
        {m.status_type === "urgent" && (
          <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded-full bg-[#FEE7DF] text-[#7B1D0D]">
            {t("missions_p.urgent")}
          </span>
        )}
        {m.status_type === "featured" && (
          <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded-full bg-[#FFF3D6] text-[#7A4A0E]">
            {t("missions_p.featured")}
          </span>
        )}
      </div>
      <h3 className="font-display font-bold text-xl md:text-2xl tracking-tight mt-3">{m.title}</h3>
      <p className="text-sm text-[--cvln-ink-2] mt-2 leading-relaxed">{m.description}</p>

      <div className="mt-5 flex items-center justify-between text-xs mono text-[--cvln-ink-2]">
        <span>{t("missions_p.stade_min")} <strong>{m.stade_required}</strong></span>
        <span className="text-[--cvln-orange] font-bold text-sm">+{m.cc_reward} CC</span>
      </div>

      <div className="mt-4 flex gap-2">
        {!s && (
          <button
            data-testid={`accept-${m.code}`}
            onClick={() => accept(m.code)}
            className="btn-outline text-sm"
          >
            {t("accept_mission")}
          </button>
        )}
        {s === "accepted" && (
          <button
            data-testid={`submit-${m.code}`}
            onClick={() => submit(m.code)}
            className="btn-primary text-sm"
          >
            {t("submit_mission")}
          </button>
        )}
        {s === "validated" && (
          <span className="text-sm text-[--cvln-forest] font-bold">✓ {t("missions_p.delivered_credited")}</span>
        )}
      </div>
    </>
  );
}

export default function Missions() {
  const { t } = useI18n();
  const { refreshMe } = useAuth();
  const reduced = useReducedMotion();
  const [missions, setMissions] = useState([]);
  const [mine, setMine] = useState([]);

  // ACA-0018 — real CONFIRM audio+haptics on a genuinely completed
  // action (mission submitted, real CC reward credited server-side),
  // same doctrine ModuleJourney.js's quiz-pass/mini-mission-commit
  // already established: fires on an actual completion, never on a
  // lighter commitment like `accept`. Gated with the same
  // SPATIAL_HUB_ENABLED flag this page's own depth engine uses.
  const audioRef = useRef(null);
  if (!audioRef.current) audioRef.current = createSpatialAudio();
  audioRef.current.setEnabled(FEATURE_FLAGS.SPATIAL_HUB_ENABLED && FEATURE_FLAGS.SPATIAL_AUDIO);
  const hapticsRef = useRef(null);
  if (!hapticsRef.current) {
    hapticsRef.current = createHaptics({
      isEnabled: () => FEATURE_FLAGS.SPATIAL_HUB_ENABLED && FEATURE_FLAGS.SPATIAL_HAPTICS,
    });
  }

  const load = async () => {
    const [m, u] = await Promise.all([
      api.get("/missions").then(r => r.data),
      api.get("/missions/mine").then(r => r.data),
    ]);
    setMissions(m); setMine(u);
  };

  useEffect(() => { load(); }, []);

  const status = (code) => mine.find(x => x.mission_code === code)?.status;

  const accept = async (code) => {
    await api.post(`/missions/${code}/accept`);
    toast.success(t("missions_p.accepted_toast"));
    load();
  };
  const submit = async (code) => {
    const { data } = await api.post(`/missions/${code}/submit`);
    toast.success(`+${data.cc_earned} CC — ${t("current_stage").toLowerCase()} : ${data.new_stade}`);
    audioRef.current.play("CONFIRM");
    hapticsRef.current.fire("CONFIRM");
    await refreshMe();
    load();
  };

  // ACA-0014/0017 — the real "what matters now" anchor: a mission
  // already accepted and ready to submit is the single most actionable
  // real state (a genuine commitment awaiting completion); absent that,
  // the first not-yet-accepted mission is the next real candidate.
  // Both branches read only real `status`/`status_type` fields already
  // fetched above — no ranking data invented for this page.
  const accIdx = missions.findIndex((m) => status(m.code) === "accepted");
  const primaryIdx = accIdx !== -1 ? accIdx : missions.findIndex((m) => !status(m.code));

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="missions-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">{t("missions")}</div>
      <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-2">
        {t("missions_p.hero_title")}
      </h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">
        {t("missions_p.hero_p")}
      </p>

      {FEATURE_FLAGS.SPATIAL_HUB_ENABLED ? (
        // Glanceable list (no card grid), per SPATIAL_H1_INTEGRATION_
        // PLAN.md's own verdict for this page — PS5's "cards, not
        // pages" principle: one dominant, actionable thing, the rest
        // genuinely present but secondary.
        <div className="mt-10 flex flex-col gap-4 max-w-2xl" data-testid="missions-list">
          {missions.map((m, i) => (
            <MissionDepthCard
              key={m.code}
              m={m}
              i={i}
              primaryIdx={primaryIdx}
              s={status(m.code)}
              reduced={reduced}
              t={t}
              accept={accept}
              submit={submit}
            />
          ))}
        </div>
      ) : (
        <div className="mt-10 grid grid-cols-1 md:grid-cols-2 gap-6">
          {missions.map((m) => (
            <div
              key={m.code}
              data-testid={`mission-${m.code}`}
              className="cvln-card p-6 flex flex-col"
            >
              <MissionCardBody m={m} s={status(m.code)} t={t} accept={accept} submit={submit} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
