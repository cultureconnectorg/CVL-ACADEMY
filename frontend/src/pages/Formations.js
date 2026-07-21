import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight } from "iconoir-react";
import { api } from "@/lib/api";
import { useI18n } from "@/lib/i18n.jsx";

export default function Formations() {
  const { t } = useI18n();
  const [formations, setFormations] = useState([]);
  const [poles, setPoles] = useState([]);
  const [pole, setPole] = useState("ALL");

  useEffect(() => {
    Promise.all([
      api.get("/formations").then(r => r.data),
      api.get("/poles").then(r => r.data),
    ]).then(([f, p]) => { setFormations(f); setPoles(p); });
  }, []);

  const visible = pole === "ALL" ? formations : formations.filter(f => f.pole === pole);
  const totalModules = formations.reduce((n, f) => n + (f.modules_count || 0), 0);

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="formations-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">{t("formations")}</div>
      <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-2">
        {formations.length} formations. {poles.length} pôles. {totalModules} modules.
      </h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">
        Chaque formation applique la doctrine CVLN : Hook culturel → Théorie → Démo → Atelier → Livrable → Validation.
      </p>

      {/* Poles filter */}
      <div className="mt-8 flex flex-wrap gap-2" data-testid="pole-filter">
        <button
          data-testid="pole-ALL"
          onClick={() => setPole("ALL")}
          className={`px-4 py-2 rounded-full text-sm font-semibold transition
            ${pole === "ALL" ? "bg-[--cvln-forest] text-white" : "bg-white text-[--cvln-ink-2] border border-black/10 hover:border-[--cvln-orange]/50"}`}
        >
          Tous les pôles
        </button>
        {poles.map((p) => (
          <button
            key={p.code}
            data-testid={`pole-${p.code}`}
            onClick={() => setPole(p.code)}
            className={`px-4 py-2 rounded-full text-sm font-semibold transition
              ${pole === p.code ? "text-white" : "bg-white text-[--cvln-ink-2] border border-black/10 hover:border-[--cvln-orange]/50"}`}
            style={pole === p.code ? { background: p.color } : {}}
          >
            {p.code} · {p.name}
          </button>
        ))}
      </div>

      {/* Grid */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {visible.map((f) => (
          <Link
            to={`/formations/${f.code}`}
            key={f.code}
            data-testid={`formation-${f.code}`}
            className="cvln-card p-6 group flex flex-col"
          >
            <div className="flex items-center justify-between">
              <div
                className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full text-xs font-bold text-white"
                style={{ background: f.pole_color }}
              >
                {f.pole} · {f.code}
              </div>
              <div className="text-xs mono text-[--cvln-ink-2]">{f.duration_h}h · {f.cc} CC</div>
            </div>
            <h3 className="font-display font-bold text-2xl tracking-tight mt-4 leading-tight">
              {f.name}
            </h3>
            <p className="text-sm text-[--cvln-ink-2] mt-3 line-clamp-3">{f.description}</p>
            <div className="mt-5 pt-4 border-t border-black/5 flex items-center justify-between">
              <div className="text-[11px] mono uppercase tracking-wider text-[--cvln-ink-2]">
                {f.stades[0]} → {f.stades[f.stades.length - 1]}
              </div>
              <div className="text-[--cvln-orange] group-hover:translate-x-1 transition">
                <ArrowRight width={16} height={16} />
              </div>
            </div>
            <div className="mt-3 text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2]">
              {f.modules_count > 0 ? `${f.modules_count} ${t("modules")}` : t("coming_soon")}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
