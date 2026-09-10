import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";
import { FocusFieldItem } from "@/lib/CvlnFocusField";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { Horizon } from "@/lib/motion-primitives";
import { computeDepthStyle } from "@/lib/spatial/attention";
import { useDepthPhysics } from "@/lib/useDepthPhysics";
import { useReducedMotion } from "@/lib/useReducedMotion";

const STAGE_CODES = ["graine", "pousse", "racine", "branches", "arbre", "foret"];
const STAGE_EMOJI = { graine: "🌱", pousse: "🌿", racine: "🌳", branches: "🌲", arbre: "🦅", foret: "🌳🌳" };
const STAGE_CC = { graine: 0, pousse: 10, racine: 50, branches: 100, arbre: 150, foret: 300 };
const STAGE_SIGNAL = {
  graine: "FREK-TIME", pousse: "FREK-WORK", racine: "FREK-SCORE",
  branches: "FREK-LINK", arbre: "FREK-CERT", foret: "FREK-CONTRIB",
};

function StageDepthCard({ s, i, currentIdx, active, done, future, reduced, t }) {
  const targetDistance = currentIdx === -1 ? 0 : i - currentIdx;
  const distance = useDepthPhysics(targetDistance, { reduced });
  const depth = computeDepthStyle(distance);
  const style = reduced
    ? { opacity: depth.opacity, transform: `scale(${Math.max(depth.scale, 0.94)})` }
    : {
        opacity: depth.opacity,
        filter: `saturate(${depth.saturate}) contrast(${depth.contrast})`,
        transform: `translateY(${depth.translateY}px) translateZ(${depth.translateZ}px) scale(${depth.scale})`,
        zIndex: depth.zIndex,
      };
  const body = <StageCardBody s={s} done={done} active={active} future={future} t={t} />;

  return (
    <motion.div
      data-testid={`stage-${s.code}`}
      data-tier={depth.tier}
      data-stage={s.code}
      data-progression-state={active ? "current" : done ? "acquired" : "future"}
      aria-current={active ? "true" : undefined}
      aria-disabled={future ? "true" : undefined}
      style={style}
      className={`snap-start min-w-[280px] max-w-[280px] cvln-card spatial-tile spatial-stage-card p-6 flex flex-col
        ${active ? "is-current-stage" : ""} ${done ? "is-crossed-stage" : ""} ${future ? "is-future-stage" : ""}`}
    >
      {future ? <Horizon visible className="h-full flex flex-col">{body}</Horizon> : body}
    </motion.div>
  );
}

function StageCardBody({ s, done, active, future = false, t }) {
  return (
    <>
      <div className="spatial-stage-icon text-6xl mb-4" aria-hidden="true">{s.emoji}</div>
      <div className="spatial-tile-eyebrow text-[11px] mono uppercase tracking-[0.25em] text-[--cvln-ink-2]">
        {s.cc}+ CC
      </div>
      <h3 className="font-display font-bold text-2xl tracking-tight mt-2">{t(`stades.${s.code}`)}</h3>
      <p className="spatial-tile-meta text-sm text-[--cvln-ink-2] mt-3">{s.desc}</p>
      <div className="mt-auto pt-6">
        <div className="mono text-xs text-[--cvln-orange] font-semibold">{s.signal}</div>
        {done && <div className="text-xs mt-2 text-[--cvln-forest] font-bold">✓ {t("roadmap_p.crossed")}</div>}
        {active && <div className="text-xs mt-2 text-[--cvln-orange] font-bold">{t("roadmap_p.you_are_here")}</div>}
        {future && <div className="text-xs mt-2 text-[--cvln-ink-2] font-semibold">{t("common.locked")}</div>}
      </div>
    </>
  );
}

export default function Roadmap() {
  const { user } = useAuth();
  const { t } = useI18n();
  const reduced = useReducedMotion();
  const currentIdx = STAGE_CODES.indexOf(user?.stade);
  const [canonical, setCanonical] = useState(null);

  useEffect(() => {
    api.get("/progression/summary").then((r) => setCanonical(r.data.canonical));
  }, []);

  const STAGES = STAGE_CODES.map((code) => ({
    code, emoji: STAGE_EMOJI[code], cc: STAGE_CC[code],
    desc: t(`roadmap_p.stage_desc_${code}`), signal: STAGE_SIGNAL[code],
  }));
  const currentStageCode = STAGE_CODES[currentIdx];

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="roadmap-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">{t("roadmap")}</div>
      <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-2">
        {t("roadmap_p.hero_title_pre")} <span className="text-[--cvln-orange]">{t("stades.graine")}</span> {t("roadmap_p.hero_title_post")}
      </h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">
        {t("roadmap_p.hero_p")}
      </p>

      <div className={`mt-12 flex gap-6 overflow-x-auto pb-8 snap-x snap-mandatory ${FEATURE_FLAGS.SPATIAL_HUB_ENABLED ? "spatial-rail-viewport spatial-stage-rail" : ""}`} data-testid="roadmap-scroll">
        {STAGES.map((s, i) => {
          const active = i === currentIdx;
          const done = i < currentIdx;
          const future = currentIdx !== -1 && i > currentIdx;

          if (FEATURE_FLAGS.SPATIAL_HUB_ENABLED) {
            return (
              <StageDepthCard
                key={s.code}
                s={s}
                i={i}
                currentIdx={currentIdx}
                active={active}
                done={done}
                future={future}
                reduced={reduced}
                t={t}
              />
            );
          }

          return (
            <FocusFieldItem
              key={s.code}
              id={s.code}
              focusedId={currentStageCode}
              data-testid={`stage-${s.code}`}
              className={`snap-start min-w-[280px] max-w-[280px] cvln-card p-6 flex flex-col
                ${active ? "border-2 border-[--cvln-orange]" : ""}`}
            >
              <StageCardBody s={s} done={done} active={active} future={future} t={t} />
            </FocusFieldItem>
          );
        })}
      </div>

      {canonical?.canonical_modules_total > 0 && (
        <div className={`mt-8 max-w-md cvln-card p-6 ${FEATURE_FLAGS.SPATIAL_HUB_ENABLED ? "spatial-progress-card" : ""}`} data-testid="roadmap-canonical-progress">
          <div className="flex items-center justify-between text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-ink-2]">
            <span>{t("canonical_progress")}</span>
            <span className="text-[--cvln-orange]">{canonical.canonical_progress_pct}%</span>
          </div>
          <div className="stage-line mt-3">
            <div style={{ width: `${canonical.canonical_progress_pct}%` }} />
          </div>
          <div className="mt-2 text-xs text-[--cvln-ink-2]">
            {canonical.canonical_modules_viewed}/{canonical.canonical_modules_total}{" "}
            {t("canonical_modules_viewed")}
          </div>
          <div className="mt-1 text-[10px] text-[--cvln-ink-2]">
            {t("canonical_progress_hint")}
          </div>
        </div>
      )}
    </div>
  );
}