import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Lock, CheckCircle } from "iconoir-react";
import { api } from "@/lib/api";
import { useI18n } from "@/lib/i18n.jsx";
import { FocusFieldItem, useFocusField } from "@/lib/CvlnFocusField";

// NO_GENERIC_SCALE_HOVER: Spatial depth is driven by explicit focus/selection,
// never hover. Hover remains limited to local non-spatial affordances such as
// borders or the arrow nudge; it must not move a formation card in depth.
export default function Formations() {
  const { t } = useI18n();
  const [path, setPath] = useState(null);
  const [poles, setPoles] = useState([]);
  const [pole, setPole] = useState("ALL");
  const cardFocus = useFocusField();

  useEffect(() => {
    Promise.all([
      api.get("/user/learning-path").then(r => r.data),
      api.get("/poles").then(r => r.data),
    ]).then(([lp, p]) => { setPath(lp); setPoles(p); });
  }, []);

  const allFormations = useMemo(() => {
    if (!path) return [];
    return [...path.own_pole, ...path.other_poles];
  }, [path]);

  const totalModules = allFormations.reduce((n, f) => n + (f.modules_count || 0), 0);
  const visible = pole === "ALL" ? allFormations : allFormations.filter(f => f.pole === pole);

  return (
    <div className="cvln-page" data-testid="formations-page">
      <section className="cvln-page-hero">
        <div className="cvln-kicker">04. FORMATIONS / EXPLORER LES TERRITOIRES</div>
        <h1 className="cvln-page-title mt-3">Des formations pour<br/>des talents sans frontières.</h1>
        <p className="cvln-page-subtitle">
          {allFormations.length} formations · {poles.length} pôles · {totalModules} modules. Chaque formation applique la doctrine CVLN : Hook → Objectifs → Cours → Atelier → Livrable → Quiz → Mini-mission.
        </p>
      </section>

      {path?.next_action && (
        <div className="cvln-card p-5 flex items-center gap-4 flex-wrap" data-testid="next-action-banner">
          <div className="w-1 h-10 rounded-full" style={{ background: path.next_action.pole_color }} />
          <div className="flex-1 min-w-0">
            <div className="text-[11px] mono uppercase tracking-wider font-bold text-[--cvln-orange]">
              Ta prochaine étape
            </div>
            <div className="font-semibold mt-1">
              {path.next_action.module_name}
              <span className="text-[--cvln-ink-2] font-normal"> · {path.next_action.formation_name}</span>
            </div>
          </div>
          <Link
            to={`/formations/${path.next_action.formation_code}/modules/${path.next_action.module_code}`}
            data-testid="next-action-cta"
            className="btn-primary text-sm"
          >
            Continuer <ArrowRight width={16} height={16} className="ml-1.5" />
          </Link>
        </div>
      )}

      <div className="mt-8 flex flex-wrap gap-2" data-testid="pole-filter">
        <FocusFieldItem id="ALL" focusedId={pole} className="inline-block">
          <button
            data-testid="pole-ALL"
            onClick={() => setPole("ALL")}
            className={`px-4 py-2 rounded-full text-sm font-semibold transition border ${pole === "ALL" ? "bg-[--cvln-orange] text-white border-[--cvln-orange]" : "bg-white/5 text-[--cvln-ink-2] border-white/10 hover:border-[--cvln-orange]/50"}`}
          >
            Tous les pôles
          </button>
        </FocusFieldItem>
        {poles.map((p) => (
          <FocusFieldItem key={p.code} id={p.code} focusedId={pole} className="inline-block">
            <button
              data-testid={`pole-${p.code}`}
              onClick={() => setPole(p.code)}
              className={`px-4 py-2 rounded-full text-sm font-semibold transition border ${pole === p.code ? "text-white border-transparent" : "bg-white/5 text-[--cvln-ink-2] border-white/10 hover:border-[--cvln-orange]/50"}`}
              style={pole === p.code ? { background: p.color } : {}}
            >
              {p.code} · {p.name}
            </button>
          </FocusFieldItem>
        ))}
      </div>

      {path?.own_pole?.length > 0 && (pole === "ALL" || visible.some(f => f.is_recommended)) && (
        <>
          <div className="cvln-section-heading">
            <h2>Ta voie · {path.metier_vise}</h2>
            <span>Parcours séquentiel</span>
          </div>
          <div className="cvln-formation-grid">
            {visible.filter(f => f.is_recommended).map(f => (
              <FormationCard key={f.code} f={f} t={t} focusedId={cardFocus.focusedId} onCardFocus={cardFocus.focus} onCardBlur={cardFocus.clear} />
            ))}
          </div>
        </>
      )}

      {(pole === "ALL" || visible.some(f => !f.is_recommended)) && (
        <>
          <div className="cvln-section-heading">
            <h2>Explorer les autres territoires</h2>
            <span>Se débloquent en progressant</span>
          </div>
          <div className="cvln-formation-grid">
            {visible.filter(f => !f.is_recommended).map(f => (
              <FormationCard key={f.code} f={f} t={t} focusedId={cardFocus.focusedId} onCardFocus={cardFocus.focus} onCardBlur={cardFocus.clear} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}

function FormationCard({ f, t, focusedId, onCardFocus, onCardBlur }) {
  const locked = !f.is_unlocked;
  const validated = f.validated_count > 0 && f.validated_count === f.modules_count;
  return (
    <FocusFieldItem id={f.code} focusedId={focusedId} className="h-full">
      <Link
        to={`/formations/${f.code}`}
        data-testid={`formation-${f.code}`}
        data-locked={locked ? "true" : "false"}
        onFocus={() => onCardFocus?.(f.code)}
        onBlur={() => onCardBlur?.()}
        className={`cvln-formation-card group flex flex-col h-full ${locked ? "opacity-75" : ""}`}
      >
        {locked && (
          <div className="absolute top-4 right-4 w-8 h-8 rounded-full bg-black/60 border border-white/10 flex items-center justify-center text-white" data-testid={`lock-${f.code}`}>
            <Lock width={14} height={14} />
          </div>
        )}
        {validated && (
          <div className="absolute top-4 right-4 w-8 h-8 rounded-full bg-[#15803D] flex items-center justify-center text-white">
            <CheckCircle width={16} height={16} />
          </div>
        )}
        <div className="relative z-10 flex items-center justify-between pr-10">
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full text-xs font-bold text-white" style={{ background: f.pole_color }}>
            {f.pole} · {f.code}
          </div>
          <div className="text-xs mono text-[--cvln-ink-2]">{f.duration_h}h · {f.cc} CC</div>
        </div>
        <h3 className="relative z-10 font-display font-bold text-2xl tracking-tight mt-8 leading-tight" data-spatial-shared-source={`formation:${f.code}`}>
          {f.name}
        </h3>

        {f.modules_count > 0 && !locked && (
          <div className="relative z-10 mt-6">
            <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
              <div className="h-full bg-[--cvln-orange]" style={{ width: `${f.progress_pct}%` }} />
            </div>
            <div className="mt-2 text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2]">
              {f.validated_count}/{f.modules_count} modules · {f.progress_pct}%
            </div>
          </div>
        )}

        {locked && <div className="relative z-10 mt-6 text-xs text-[--cvln-ink-2] leading-relaxed">{f.lock_reason}</div>}

        <div className="formation-footer relative z-10 flex items-center justify-between">
          <div className="text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2]">{f.modules_count} {t("modules")}</div>
          <div className="text-[--cvln-orange] group-hover:translate-x-1 transition"><ArrowRight width={16} height={16} /></div>
        </div>
      </Link>
    </FocusFieldItem>
  );
}
