import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Lock, CheckCircle } from "iconoir-react";
import { api } from "@/lib/api";
import { useI18n } from "@/lib/i18n.jsx";
import { FocusFieldItem, useFocusField } from "@/lib/CvlnFocusField";

export default function Formations() {
  const { t } = useI18n();
  const [path, setPath] = useState(null);
  const [poles, setPoles] = useState([]);
  const [pole, setPole] = useState("ALL");
  // Which formation card currently has DOM focus (keyboard tab or click)
  // — never hover. TARGET -> APPROACH, everything else -> RECEDE, nothing
  // focused -> CALM. See CvlnFocusField.jsx / W2-C for the contract.
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
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="formations-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">
        {t("formations")}
      </div>
      <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-2">
        {allFormations.length} formations. {poles.length} pôles. {totalModules} modules.
      </h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">
        Chaque formation applique la doctrine CVLN : Hook → Objectifs → Cours → Atelier → Livrable → Quiz → Mini-mission.
      </p>

      {/* Next action banner */}
      {path?.next_action && (
        <div className="mt-6 cvln-card p-5 flex items-center gap-4 flex-wrap" data-testid="next-action-banner">
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

      {/* Poles filter — the already-existing `pole` selection state is
          reused directly as the field's focusedId, no new state added. */}
      <div className="mt-8 flex flex-wrap gap-2" data-testid="pole-filter">
        <FocusFieldItem id="ALL" focusedId={pole} className="inline-block">
          <button
            data-testid="pole-ALL"
            onClick={() => setPole("ALL")}
            className={`px-4 py-2 rounded-full text-sm font-semibold transition
              ${pole === "ALL" ? "bg-[--cvln-forest] text-white" : "bg-white text-[--cvln-ink-2] border border-black/10 hover:border-[--cvln-orange]/50"}`}
          >
            Tous les pôles
          </button>
        </FocusFieldItem>
        {poles.map((p) => (
          <FocusFieldItem key={p.code} id={p.code} focusedId={pole} className="inline-block">
            <button
              data-testid={`pole-${p.code}`}
              onClick={() => setPole(p.code)}
              className={`px-4 py-2 rounded-full text-sm font-semibold transition
                ${pole === p.code ? "text-white" : "bg-white text-[--cvln-ink-2] border border-black/10 hover:border-[--cvln-orange]/50"}`}
              style={pole === p.code ? { background: p.color } : {}}
            >
              {p.code} · {p.name}
            </button>
          </FocusFieldItem>
        ))}
      </div>

      {/* Own pole section */}
      {path?.own_pole?.length > 0 && (pole === "ALL" || visible.some(f => f.is_recommended)) && (
        <>
          <div className="mt-10 flex items-baseline gap-3">
            <h2 className="font-display font-bold text-xl tracking-tight">Ta voie · {path.metier_vise}</h2>
            <span className="text-xs mono uppercase tracking-wider text-[--cvln-ink-2]">
              parcours séquentiel
            </span>
          </div>
          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {visible.filter(f => f.is_recommended).map(f => (
              <FormationCard
                key={f.code}
                f={f}
                t={t}
                focusedId={cardFocus.focusedId}
                onCardFocus={cardFocus.focus}
                onCardBlur={cardFocus.clear}
              />
            ))}
          </div>
        </>
      )}

      {/* Other poles */}
      {(pole === "ALL" || visible.some(f => !f.is_recommended)) && (
        <>
          <div className="mt-10 flex items-baseline gap-3">
            <h2 className="font-display font-bold text-xl tracking-tight">Autres pôles</h2>
            <span className="text-xs mono uppercase tracking-wider text-[--cvln-ink-2]">
              se débloquent en progressant
            </span>
          </div>
          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {visible.filter(f => !f.is_recommended).map(f => (
              <FormationCard
                key={f.code}
                f={f}
                t={t}
                focusedId={cardFocus.focusedId}
                onCardFocus={cardFocus.focus}
                onCardBlur={cardFocus.clear}
              />
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
    // TARGET -> APPROACH, other cards -> RECEDE, nothing focused -> CALM.
    // Driven by real DOM focus (keyboard tab or the click that's about to
    // navigate) on the Link below, never by :hover — NO_GENERIC_SCALE_HOVER.
    <FocusFieldItem id={f.code} focusedId={focusedId} className="h-full">
      <Link
        to={`/formations/${f.code}`}
        data-testid={`formation-${f.code}`}
        onFocus={() => onCardFocus?.(f.code)}
        onBlur={() => onCardBlur?.()}
        className={`h-full cvln-card p-6 group flex flex-col relative overflow-hidden ${locked ? "opacity-75" : ""}`}
      >
        {locked && (
          <div className="absolute top-3 right-3 w-8 h-8 rounded-full bg-black/70 flex items-center justify-center text-white" data-testid={`lock-${f.code}`}>
            <Lock width={14} height={14} />
          </div>
        )}
        {validated && (
          <div className="absolute top-3 right-3 w-8 h-8 rounded-full bg-[#15803D] flex items-center justify-center text-white">
            <CheckCircle width={16} height={16} />
          </div>
        )}
        <div className="flex items-center justify-between pr-10">
          <div
            className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full text-xs font-bold text-white"
            style={{ background: f.pole_color }}
          >
            {f.pole} · {f.code}
          </div>
          <div className="text-xs mono text-[--cvln-ink-2]">{f.duration_h}h · {f.cc} CC</div>
        </div>
        <h3 className="font-display font-bold text-xl tracking-tight mt-4 leading-tight">
          {f.name}
        </h3>

        {/* Progress bar */}
        {f.modules_count > 0 && !locked && (
          <div className="mt-4">
            <div className="h-1.5 bg-black/5 rounded-full overflow-hidden">
              <div className="h-full bg-[--cvln-orange]" style={{ width: `${f.progress_pct}%` }} />
            </div>
            <div className="mt-1.5 text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2]">
              {f.validated_count}/{f.modules_count} modules · {f.progress_pct}%
            </div>
          </div>
        )}

        {/* Lock reason */}
        {locked && (
          <div className="mt-4 text-xs text-[--cvln-ink-2] leading-relaxed">
            {f.lock_reason}
          </div>
        )}

        <div className="mt-4 pt-4 border-t border-black/5 flex items-center justify-between">
          <div className="text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2]">
            {f.modules_count} {t("modules")}
          </div>
          <div className="text-[--cvln-orange] group-hover:translate-x-1 transition">
            <ArrowRight width={16} height={16} />
          </div>
        </div>
      </Link>
    </FocusFieldItem>
  );
}
