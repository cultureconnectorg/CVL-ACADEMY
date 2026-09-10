import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { computeDepthStyle } from "@/lib/spatial/attention";
import { useDepthPhysics } from "@/lib/useDepthPhysics";
import { useReducedMotion } from "@/lib/useReducedMotion";

function BadgeDepthCard({ b, i, primaryIdx, owned, reachable, reduced, t }) {
  const targetDistance = primaryIdx === -1 ? 0 : i - primaryIdx;
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
  return (
    <motion.div
      data-testid={`badge-${b.code}`}
      data-tier={depth.tier}
      data-owned={owned ? "true" : "false"}
      data-reachable={reachable ? "true" : "false"}
      style={{ ...style, "--badge-accent": b.color || "var(--cvln-orange)" }}
      className="cvln-card spatial-tile spatial-badge-card p-6 flex flex-col items-center text-center"
    >
      <BadgeCardBody b={b} owned={owned} reachable={reachable} t={t} />
    </motion.div>
  );
}

function BadgeCardBody({ b, owned, reachable, t }) {
  return (
    <>
      <div
        className={`spatial-badge-medallion w-28 h-28 rounded-full flex items-center justify-center text-white text-4xl font-black relative
          ${owned ? "shadow-lg" : "grayscale opacity-70"}`}
        style={{ background: b.color }}
      >
        ✦
        {owned && (
          <div className="absolute -bottom-1 -right-1 bg-[--cvln-forest] text-white text-[10px] font-bold px-2 py-0.5 rounded-full">
            {t("badges_p.obtained")}
          </div>
        )}
      </div>
      <div className="font-display font-bold text-lg tracking-tight mt-4">{b.name}</div>
      <div className="spatial-tile-eyebrow text-xs mono uppercase tracking-wider text-[--cvln-ink-2] mt-1">
        {b.tier} · {b.cc_threshold} CC
      </div>
      <div className="spatial-tile-meta text-xs text-[--cvln-ink-2] mt-3">{b.description}</div>
      {!owned && (
        <div className="mt-3 text-xs font-semibold text-[--cvln-orange]">
          {reachable ? t("badges_p.unlock_next_refresh") : `${b.cc_threshold} CC`}
        </div>
      )}
    </>
  );
}

export default function Badges() {
  const { user } = useAuth();
  const { t } = useI18n();
  const reduced = useReducedMotion();
  const [all, setAll] = useState([]);
  const [mine, setMine] = useState([]);

  useEffect(() => {
    Promise.all([
      api.get("/badges").then(r => r.data),
      api.get("/badges/mine").then(r => r.data),
    ]).then(([a, m]) => { setAll(a); setMine(m); });
  }, []);

  const earned = new Set(mine.map(b => b.code));
  const primaryIdx = all.findIndex((b) => !earned.has(b.code));
  const spatial = FEATURE_FLAGS.SPATIAL_HUB_ENABLED;

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="badges-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">{t("badges")}</div>
      <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-2">
        {t("badges_p.hero_title")}
      </h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">
        {t("badges_p.hero_p")}
      </p>

      <div className={`mt-10 grid grid-cols-2 md:grid-cols-4 gap-6 ${spatial ? "spatial-badge-grid" : ""}`}>
        {all.map((b, i) => {
          const owned = earned.has(b.code);
          const reachable = (user?.cc_credits ?? 0) >= b.cc_threshold;

          if (spatial) {
            return (
              <BadgeDepthCard
                key={b.code}
                b={b}
                i={i}
                primaryIdx={primaryIdx}
                owned={owned}
                reachable={reachable}
                reduced={reduced}
                t={t}
              />
            );
          }

          return (
            <div
              key={b.code}
              data-testid={`badge-${b.code}`}
              className={`cvln-card p-6 flex flex-col items-center text-center transition
                ${owned ? "" : "opacity-70"}`}
            >
              <BadgeCardBody b={b} owned={owned} reachable={reachable} t={t} />
              {!owned && !reachable && (
                <div className="mt-3 text-xs font-semibold text-[--cvln-orange]">
                  {b.cc_threshold - (user?.cc_credits ?? 0)} {t("badges_p.cc_remaining")}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
