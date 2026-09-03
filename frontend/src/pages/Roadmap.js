import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";
import { FocusFieldItem } from "@/lib/CvlnFocusField";

const STAGE_CODES = ["graine", "pousse", "racine", "branches", "arbre", "foret"];
const STAGE_EMOJI = { graine: "🌱", pousse: "🌿", racine: "🌳", branches: "🌲", arbre: "🦅", foret: "🌳🌳" };
const STAGE_CC = { graine: 0, pousse: 10, racine: 50, branches: 100, arbre: 150, foret: 300 };
const STAGE_SIGNAL = {
  graine: "FREK-TIME", pousse: "FREK-WORK", racine: "FREK-SCORE",
  branches: "FREK-LINK", arbre: "FREK-CERT", foret: "FREK-CONTRIB",
};

export default function Roadmap() {
  const { user } = useAuth();
  const { t } = useI18n();
  const currentIdx = STAGE_CODES.indexOf(user?.stade);

  const STAGES = STAGE_CODES.map((code) => ({
    code, emoji: STAGE_EMOJI[code], cc: STAGE_CC[code],
    desc: t(`roadmap_p.stage_desc_${code}`), signal: STAGE_SIGNAL[code],
  }));
  // W3-D: progression is felt spatially (the current stage stands
  // forward, every other stage recedes) rather than through a "Level N"
  // counter — GRAINE_POUSSE_RACINE_BRANCHES_ARBRE_FORET stays an
  // environmental transformation, never a level/XP readout.
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

      <div className="mt-12 flex gap-6 overflow-x-auto pb-6 snap-x snap-mandatory" data-testid="roadmap-scroll">
        {STAGES.map((s, i) => {
          const active = i === currentIdx;
          const done = i < currentIdx;
          return (
            <FocusFieldItem
              key={s.code}
              id={s.code}
              focusedId={currentStageCode}
              data-testid={`stage-${s.code}`}
              className={`snap-start min-w-[280px] max-w-[280px] cvln-card p-6 flex flex-col
                ${active ? "border-2 border-[--cvln-orange]" : ""}`}
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
              </div>
            </FocusFieldItem>
          );
        })}
      </div>
    </div>
  );
}
