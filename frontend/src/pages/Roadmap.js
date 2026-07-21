import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";

const STAGES = [
  { code: "graine",   emoji: "🌱", level: 1, cc: 0,   desc: "Découvrir les bases culturelles et numériques. FREK-TIME s'active.", signal: "FREK-TIME" },
  { code: "pousse",   emoji: "🌿", level: 2, cc: 10,  desc: "Premières productions, engagement, livrables archivés dans FREK.", signal: "FREK-WORK" },
  { code: "racine",   emoji: "🌳", level: 3, cc: 50,  desc: "Autonomie partielle, projets réels, première mission CVLN.", signal: "FREK-SCORE" },
  { code: "branches", emoji: "🌲", level: 4, cc: 100, desc: "Collaborations, impact mesurable, réseau structuré.", signal: "FREK-LINK" },
  { code: "arbre",    emoji: "🦅", level: 5, cc: 150, desc: "Autonomie totale, référence dans son domaine.", signal: "FREK-CERT" },
  { code: "foret",    emoji: "🌳🌳", level: 6, cc: 300, desc: "Formateur, patrimoine vivant CVLN. Tu formes les prochains.", signal: "FREK-CONTRIB" },
];

export default function Roadmap() {
  const { user } = useAuth();
  const { t } = useI18n();
  const currentIdx = STAGES.findIndex(s => s.code === user?.stade);

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="roadmap-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">{t("roadmap")}</div>
      <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-2">
        Du <span className="text-[--cvln-orange]">Graine</span> à la Forêt.
      </h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">
        {"6 stades végétaux. Chaque seuil de Crédits CC franchi débloque un signal FREK, un badge et une opportunité concrète dans l'écosystème CVLN."}
      </p>

      <div className="mt-12 flex gap-6 overflow-x-auto pb-6 snap-x snap-mandatory" data-testid="roadmap-scroll">
        {STAGES.map((s, i) => {
          const active = i === currentIdx;
          const done = i < currentIdx;
          return (
            <div
              key={s.code}
              data-testid={`stage-${s.code}`}
              className={`snap-start min-w-[280px] max-w-[280px] cvln-card p-6 flex flex-col
                ${active ? "border-2 border-[--cvln-orange]" : ""}`}
            >
              <div className="text-6xl mb-4">{s.emoji}</div>
              <div className="text-[11px] mono uppercase tracking-[0.25em] text-[--cvln-ink-2]">
                Niveau {s.level} · {s.cc}+ CC
              </div>
              <h3 className="font-display font-bold text-2xl tracking-tight mt-2">{t(`stades.${s.code}`)}</h3>
              <p className="text-sm text-[--cvln-ink-2] mt-3">{s.desc}</p>
              <div className="mt-auto pt-6">
                <div className="mono text-xs text-[--cvln-orange] font-semibold">{s.signal}</div>
                {done && <div className="text-xs mt-2 text-[--cvln-forest] font-bold">✓ Franchi</div>}
                {active && <div className="text-xs mt-2 text-[--cvln-orange] font-bold">Tu es ici</div>}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
