import { useEffect, useRef } from "react";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";
import { Horizon } from "@/lib/motion-primitives";
import { captureElementDepth, restoreElementDepth } from "@/lib/depthMemory";
import { computeDepthStyle } from "@/lib/spatial/attention";
import { useSpatialRail } from "@/lib/spatial/useSpatialRail";

const STAGE_CODES = ["graine", "pousse", "racine", "branches", "arbre", "foret"];
const STAGE_EMOJI = { graine: "🌱", pousse: "🌿", racine: "🌳", branches: "🌲", arbre: "🦅", foret: "🌳🌳" };
const STAGE_CC = { graine: 0, pousse: 10, racine: 50, branches: 100, arbre: 150, foret: 300 };
const STAGE_SIGNAL = {
  graine: "FREK-TIME", pousse: "FREK-WORK", racine: "FREK-SCORE",
  branches: "FREK-LINK", arbre: "FREK-CERT", foret: "FREK-CONTRIB",
};

function attentionPresentation(index, attentionPosition) {
  const depth = computeDepthStyle(index - attentionPosition);
  return {
    depth,
    style: {
      transform: `translate3d(${depth.translateX.toFixed(2)}px, ${depth.translateY.toFixed(2)}px, ${depth.translateZ.toFixed(2)}px) rotateY(${depth.rotateY.toFixed(2)}deg) scale(${depth.scale.toFixed(4)})`,
      opacity: depth.opacity,
      filter: `saturate(${depth.saturate.toFixed(4)}) contrast(${depth.contrast.toFixed(4)}) brightness(${depth.brightness.toFixed(4)}) blur(${depth.blur.toFixed(3)}px)`,
      zIndex: depth.zIndex,
      transformStyle: "preserve-3d",
      transformOrigin: "50% 50%",
    },
  };
}

export default function Roadmap() {
  const { user } = useAuth();
  const { t } = useI18n();
  const railRef = useRef(null);
  const currentIdx = STAGE_CODES.indexOf(user?.stade);

  const STAGES = STAGE_CODES.map((code) => ({
    code, emoji: STAGE_EMOJI[code], cc: STAGE_CC[code],
    desc: t(`roadmap_p.stage_desc_${code}`), signal: STAGE_SIGNAL[code],
  }));
  const rail = useSpatialRail({
    railRef,
    itemCount: STAGES.length,
    initialIndex: currentIdx >= 0 ? currentIdx : 0,
  });
  // DOMAIN_STATE remains authoritative: the current stage comes only from the
  // authenticated user. Spatial attention can travel across the rail but never
  // writes `user.stade`, unlock state, credits, or progression.
  const currentStageCode = STAGE_CODES[currentIdx];

  useEffect(() => {
    const railElement = railRef.current;
    let secondFrame = null;
    const restore = () => restoreElementDepth("/roadmap", "stage-rail", railElement);
    const firstFrame = window.requestAnimationFrame(() => {
      secondFrame = window.requestAnimationFrame(restore);
    });

    return () => {
      window.cancelAnimationFrame(firstFrame);
      if (secondFrame !== null) window.cancelAnimationFrame(secondFrame);
      // Do not write here: once unmount/layout removal begins the detached
      // element may report scrollLeft=0 and overwrite the exact live snapshot.
      // Native onScroll is the authoritative capture point below.
    };
  }, []);

  const rememberRailDepth = (event) => {
    captureElementDepth("/roadmap", "stage-rail", event.currentTarget);
  };

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="roadmap-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">{t("roadmap")}</div>
      <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-2">
        {t("roadmap_p.hero_title_pre")} <span className="text-[--cvln-orange]">{t("stades.graine")}</span> {t("roadmap_p.hero_title_post")}
      </h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">
        {t("roadmap_p.hero_p")}
      </p>

      <div
        ref={railRef}
        {...rail.railProps}
        onScroll={rememberRailDepth}
        className="mt-12 flex gap-6 overflow-x-auto overflow-y-visible pb-10 snap-x snap-mandatory"
        data-testid="roadmap-scroll"
        data-attention-position={rail.attentionPosition.toFixed(3)}
        role="listbox"
        aria-label={t("roadmap")}
        style={{ ...rail.railProps.style, perspective: "1400px", perspectiveOrigin: "50% 45%" }}
      >
        {STAGES.map((s, i) => {
          const active = i === currentIdx;
          const done = currentIdx >= 0 && i < currentIdx;
          const future = currentIdx >= 0 && i > currentIdx;
          const horizonDistance = future ? i - currentIdx : 0;
          const { depth, style } = attentionPresentation(i, rail.attentionPosition);
          const card = (
            <div
              data-testid={`stage-visual-${s.code}`}
              data-attention-tier={depth.tier}
              data-attention-weight={depth.weight.toFixed(4)}
              data-domain-stage-state={active ? "CURRENT" : done ? "ACQUIRED" : future ? "HORIZON" : "UNKNOWN"}
              className={`h-full cvln-card p-6 flex flex-col ${active ? "border-2 border-[--cvln-orange]" : ""}`}
              style={style}
            >
              <div className="text-6xl mb-4">{s.emoji}</div>
              <div className="text-[11px] mono uppercase tracking-[0.25em] text-[--cvln-ink-2]">
                {s.cc}+ CC
              </div>
              <h3 className="font-display font-bold text-2xl tracking-tight mt-2">{t(`stades.${s.code}`)}</h3>
              <p className="text-sm text-[--cvln-ink-2] mt-3">{s.desc}</p>
              <div className="mt-auto pt-6">
                <div className="mono text-xs text-[--cvln-orange] font-semibold">{s.signal}</div>
                {done && <div className="text-xs mt-2 text-[--cvln-forest] font-bold">✓ {t("roadmap_p.crossed")}</div>}
                {active && <div className="text-xs mt-2 text-[--cvln-orange] font-bold">{t("roadmap_p.you_are_here")}</div>}
                {future && (
                  <div
                    className="text-xs mt-2 text-[--cvln-ink-2] font-semibold"
                    data-testid={`horizon-label-${s.code}`}
                    data-horizon-distance={horizonDistance}
                  >
                    Horizon · +{horizonDistance}
                  </div>
                )}
              </div>
            </div>
          );

          return (
            <div
              key={s.code}
              {...rail.itemProps(i)}
              role="option"
              aria-selected={i === rail.focusedIndex}
              aria-current={active ? "step" : undefined}
              aria-hidden={depth.ariaHidden && i !== rail.focusedIndex && !active ? true : undefined}
              data-testid={`stage-${s.code}`}
              data-spatial-focus-id={`roadmap-stage-${s.code}`}
              data-attention-tier={depth.tier}
              data-domain-stage-state={active ? "CURRENT" : done ? "ACQUIRED" : future ? "HORIZON" : "UNKNOWN"}
              className="snap-start min-w-[280px] max-w-[280px] outline-none focus-visible:ring-2 focus-visible:ring-[--cvln-orange] rounded-3xl"
            >
              {future ? (
                <Horizon visible distance={horizonDistance} className="h-full" data-testid={`horizon-${s.code}`}>
                  {card}
                </Horizon>
              ) : card}
            </div>
          );
        })}
      </div>

      <div className="sr-only" aria-live="polite" data-testid="roadmap-spatial-status">
        {currentStageCode ? `${t(`stades.${currentStageCode}`)} · ${rail.focusedIndex + 1}/${STAGES.length}` : ""}
      </div>
    </div>
  );
}
