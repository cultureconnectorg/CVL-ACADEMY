import { useMemo, useState, useCallback, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { computeDepthStyle } from "@/lib/spatial/attention";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { useI18n } from "@/lib/i18n.jsx";

/**
 * RAIL 3 ("Finir Spatial Learning", 2026-09-07) — the one place the
 * pedagogical graph (`lib/pedagogicalGraph.js`) actually becomes
 * something the learner sees move. Reuses `lib/spatial/attention.js`'s
 * existing, unmodified `computeDepthStyle` — this component only ever
 * feeds it real `node.distance` values; it contains no depth/occlusion
 * math of its own (`ne pas refaire Spatial`).
 *
 * Doctrine this component is the direct, visible proof of: "l'espace se
 * réorganise autour de l'intention, le savoir avance vers toi à mesure
 * que tu avances vers lui" — the intention node (`distance === 0`)
 * renders largest/sharpest/closest; every other real node recedes by
 * exactly how far it really is, never by a hand-placed layout position.
 *
 * Accessibility invariants inherited unchanged from H0.10 (see
 * `docs/ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md` §7): DOM order is
 * the real tab order (not the visual depth order), every node stays a
 * real focusable/activatable element, `prefers-reduced-motion` flattens
 * translateZ/rotateY/large translateX but keeps the tier hierarchy
 * (opacity/saturation/scale) so the "what matters most" signal survives
 * without motion.
 */
export default function SpatialHub({ formationNodes, missionNodes }) {
  const navigate = useNavigate();
  const { t } = useI18n();
  const reduced = useReducedMotion();

  // One combined, distance-sorted rail — real nodes only, closest first.
  // Distance is the sole ordering key (never a hand-picked position).
  const items = useMemo(() => {
    const formations = (formationNodes ?? []).map((n) => ({
      kind: "formation",
      key: `formation:${n.code}`,
      distance: n.distance,
      title: n.name,
      subtitle: n.poleColor ? n.pole : undefined,
      poleColor: n.poleColor,
      meta: `${n.progressPct}%`,
      progressPct: n.progressPct,
      isUnlocked: n.isUnlocked,
      onActivate: () => navigate(`/formations/${n.code}`),
    }));
    const missions = (missionNodes ?? []).map((n) => ({
      kind: "mission",
      key: `mission:${n.code}`,
      distance: n.distance,
      title: n.title,
      subtitle: n.pole,
      meta: `+${n.ccReward} CC`,
      eligible: n.eligible,
      onActivate: () => navigate("/missions"),
    }));
    return [...formations, ...missions].sort((a, b) => a.distance - b.distance);
  }, [formationNodes, missionNodes, navigate]);

  const [focusedKey, setFocusedKey] = useState(() => items.find((i) => i.distance === 0)?.key ?? items[0]?.key);
  const nodeRefs = useRef({});

  // Roving tabindex: the keyboard handler lives on each real, already-
  // interactive `<button>` (never on the non-interactive wrapper), and
  // moving between items calls real DOM `.focus()` — a roving-tabindex
  // change alone doesn't move focus, only bookkeeping does.
  const moveFocus = useCallback(
    (fromKey, dir) => {
      const idx = items.findIndex((i) => i.key === fromKey);
      if (idx === -1) return;
      const next = dir > 0 ? Math.min(idx + 1, items.length - 1) : Math.max(idx - 1, 0);
      if (next === idx) return;
      const nextKey = items[next].key;
      setFocusedKey(nextKey);
      nodeRefs.current[nextKey]?.focus();
    },
    [items]
  );

  if (items.length === 0) return null;

  return (
    <div className="mt-2 mb-10 -mx-2 px-2 overflow-x-auto" data-testid="spatial-hub">
      <h2 className="sr-only">{t("dashboard_p.next_step")}</h2>
      <div className="flex gap-5 pb-4" style={{ perspective: reduced ? "none" : "1400px" }}>
        {items.map((item) => {
          const depth = computeDepthStyle(item.distance, { mobile: false });
          const isFocused = item.key === focusedKey;
          const style = reduced
            ? {
                // Reduced motion: keep the hierarchy signal (opacity/scale/
                // saturation) — drop the perspective/rotation/large-shift
                // motion per the inherited, unchanged accessibility rule.
                opacity: depth.opacity,
                filter: `saturate(${depth.saturate}) contrast(${depth.contrast})`,
                transform: `scale(${Math.max(depth.scale, 0.94)})`,
              }
            : {
                opacity: depth.opacity,
                filter: `saturate(${depth.saturate}) contrast(${depth.contrast}) brightness(${depth.brightness}) blur(${depth.blur}px)`,
                transform: `translate3d(${depth.translateX * 0.4}px, ${depth.translateY}px, ${depth.translateZ}px) rotateY(${depth.rotateY}deg) scale(${depth.scale})`,
              };

          return (
            <motion.button
              key={item.key}
              ref={(el) => {
                nodeRefs.current[item.key] = el;
              }}
              type="button"
              data-testid={`spatial-hub-node-${item.kind}-${item.key.split(":")[1]}`}
              data-tier={depth.tier}
              aria-hidden={reduced ? undefined : depth.ariaHidden}
              aria-current={item.distance === 0 ? "true" : undefined}
              tabIndex={isFocused ? 0 : -1}
              onFocus={() => setFocusedKey(item.key)}
              onClick={item.onActivate}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  item.onActivate();
                } else if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
                  e.preventDefault();
                  moveFocus(item.key, e.key === "ArrowRight" ? 1 : -1);
                }
              }}
              animate={style}
              transition={{ duration: reduced ? 0.15 : 0.45, ease: [0.22, 1, 0.36, 1] }}
              style={{ zIndex: depth.zIndex, transformStyle: reduced ? undefined : "preserve-3d" }}
              className={`shrink-0 w-56 text-left rounded-2xl p-5 border cursor-pointer
                focus-visible:outline focus-visible:outline-2 focus-visible:outline-[--cvln-orange]
                ${item.distance === 0 ? "border-[--cvln-orange] bg-white shadow-lg" : "border-black/5 bg-white/70"}`}
            >
              <div className="text-[10px] mono uppercase tracking-[0.2em] text-[--cvln-ink-2]">
                {item.kind === "mission" ? "MISSION" : item.subtitle}
              </div>
              <div className="font-display font-bold text-lg tracking-tight mt-1 leading-snug">
                {item.title}
              </div>
              {item.kind === "formation" && (
                <div className="mt-3 stage-line">
                  <div style={{ width: `${item.progressPct}%`, background: item.poleColor || undefined }} />
                </div>
              )}
              <div className="mt-3 text-xs font-semibold text-[--cvln-orange]">{item.meta}</div>
              {item.kind === "formation" && !item.isUnlocked && (
                <div className="mt-1 text-[10px] text-[--cvln-ink-2] uppercase tracking-wider">🔒</div>
              )}
              {item.kind === "mission" && item.eligible === false && (
                <div className="mt-1 text-[10px] text-[--cvln-ink-2] uppercase tracking-wider">🔒</div>
              )}
            </motion.button>
          );
        })}
      </div>
    </div>
  );
}
