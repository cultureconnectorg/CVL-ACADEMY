import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Book, Trophy, MediaVideo, Coins, Lock, CheckCircle, PlaySolid, ArrowRight } from "iconoir-react";
import { api } from "@/lib/api";
import { useI18n } from "@/lib/i18n.jsx";
import BackButton from "@/components/BackButton";

const STADE_EMOJI = {
  graine: "🌱", pousse: "🌿", racine: "🌳",
  branches: "🌲", arbre: "🦅", foret: "🌳🌳",
};

export default function FormationDetail() {
  const { code } = useParams();
  const { t } = useI18n();
  const [f, setF] = useState(null);

  const STATUS_META = {
    available:              { label: t("formation_detail_p.status_available"),             color: "#E05A33", bg: "#FFF3EC" },
    in_progress:            { label: t("formation_detail_p.status_in_progress"),            color: "#B45309", bg: "#FEF3C7" },
    ready_for_quiz:         { label: t("formation_detail_p.status_ready_for_quiz"),         color: "#0F4E33", bg: "#E7F5EF" },
    awaiting_mini_mission:  { label: t("formation_detail_p.status_awaiting_mini_mission"),  color: "#7C2D12", bg: "#FEE7DF" },
    validated:              { label: t("formation_detail_p.status_validated"),              color: "#15803D", bg: "#DCFCE7" },
  };

  useEffect(() => {
    api.get(`/formations/${code}`).then(r => setF(r.data));
  }, [code]);

  if (!f) return <div className="p-10 text-[--cvln-ink-2]">…</div>;

  const validatedCount = (f.modules || []).filter(m => m.status === "validated").length;
  const pct = f.modules && f.modules.length
    ? Math.round((validatedCount / f.modules.length) * 100) : 0;

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="formation-detail">
      <BackButton to="/formations" label={t("formations")} testId="back-to-formations" />

      {/* Formation lock banner */}
      {f.is_unlocked === false && (
        <div className="mb-6 p-4 rounded-2xl bg-[#FFF3EC] border border-[--cvln-orange]/30 flex gap-3 items-start" data-testid="formation-lock-banner">
          <Lock className="text-[--cvln-orange] flex-shrink-0 mt-0.5" width={22} height={22} />
          <div>
            <div className="font-semibold text-[--cvln-ink]">{t("formation_detail_p.locked_title")}</div>
            <div className="text-sm text-[--cvln-ink-2] mt-1">{f.lock_reason}</div>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2">
          <div
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold text-white"
            style={{ background: f.pole_color }}
          >
            {f.pole_name} · {f.code}
          </div>
          <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-4">
            {f.name}
          </h1>
          <p className="text-[--cvln-ink-2] mt-4 text-lg leading-relaxed max-w-2xl">
            {f.description}
          </p>
          <div className="mt-4 text-sm text-[--cvln-ink-2] max-w-2xl">
            <strong className="text-[--cvln-ink]">{t("formation_detail_p.strategic_objective")}</strong>
            {f.objective_strategic}
          </div>

          {/* Overall progress */}
          {f.modules && f.modules.length > 0 && (
            <div className="mt-6 max-w-2xl">
              <div className="flex items-center justify-between text-xs mono uppercase tracking-wider text-[--cvln-ink-2] mb-2">
                <span>{t("formation_detail_p.formation_progress")}</span>
                <span>{validatedCount} / {f.modules.length} · {pct}%</span>
              </div>
              <div className="h-2 bg-black/5 rounded-full overflow-hidden">
                <div className="h-full bg-[--cvln-orange] transition-all" style={{ width: `${pct}%` }} />
              </div>
            </div>
          )}
        </div>

        <div className="cvln-card p-6 space-y-3">
          <Row icon={<Book width={16} height={16} />} label={t("duration")} value={`${f.duration_h}h`} />
          <Row icon={<Coins width={16} height={16} />} label={t("cc_credits")} value={`${f.cc} CC`} />
          <Row icon={<Trophy width={16} height={16} />} label={t("formation_detail_p.badge_label")} value={f.badge_name} />
          <Row icon={<MediaVideo width={16} height={16} />} label={t("formation_detail_p.stades_label")} value={
            <span>{STADE_EMOJI[f.stades[0]]} → {STADE_EMOJI[f.stades[f.stades.length - 1]]}</span>
          } />
          <div className="pt-3 border-t border-black/5 text-xs">
            <div className="text-[--cvln-ink-2] font-semibold uppercase tracking-wider">{t("prerequisites")}</div>
            <div className="mt-1">{f.prerequisites}</div>
          </div>
          <div className="text-xs">
            <div className="text-[--cvln-ink-2] font-semibold uppercase tracking-wider">{t("debouches")}</div>
            <div className="mt-1">{f.debouches}</div>
          </div>
        </div>
      </div>

      {/* Modules */}
      <div className="mt-12">
        <h2 className="font-display font-bold text-2xl md:text-3xl tracking-tight">{t("modules")}</h2>
        <div className="text-sm text-[--cvln-ink-2] mt-1">
          {t("formation_detail_p.modules_doctrine")}
        </div>

        <div className="mt-6 grid gap-3">
          {(f.modules || []).map((m, i) => {
            const status = m.status || "available";
            const meta = STATUS_META[status] || STATUS_META.available;
            const locked = f.is_unlocked === false || m.is_unlocked === false;
            return (
              <div
                key={m.code}
                data-testid={`module-${m.code}`}
                className={`cvln-card p-5 flex items-center gap-5 flex-wrap ${locked ? "opacity-70" : ""}`}
              >
                {locked ? (
                  <div className="w-10 h-10 rounded-full bg-black/5 flex items-center justify-center text-[--cvln-ink-2]">
                    <Lock width={16} height={16} />
                  </div>
                ) : status === "validated" ? (
                  <div className="w-10 h-10 rounded-full bg-[#15803D] flex items-center justify-center text-white">
                    <CheckCircle width={18} height={18} />
                  </div>
                ) : (
                  <div className="w-10 h-10 rounded-full bg-[--cvln-bg-warm] flex items-center justify-center font-bold text-[--cvln-ink]">
                    {i + 1}
                  </div>
                )}
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2 text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2] flex-wrap">
                    <span>{m.code}</span>
                    <span>·</span>
                    <span>{m.duration_h}h</span>
                    <span>·</span>
                    <span>{STADE_EMOJI[m.stade]} {t(`stades.${m.stade}`)}</span>
                    {!locked && (
                      <span
                        className="ml-2 px-2 py-0.5 rounded-full font-bold"
                        style={{ background: meta.bg, color: meta.color }}
                      >
                        {meta.label}
                      </span>
                    )}
                  </div>
                  <div className="font-semibold text-lg mt-1">{m.name}</div>
                  <div className="text-sm text-[--cvln-ink-2] mt-1">
                    <strong>{t("deliverable")} : </strong>{m.deliverable}
                  </div>
                  {!locked && status === "in_progress" && m.course_progress_pct > 0 && (
                    <div className="mt-2 flex items-center gap-2">
                      <div className="h-1.5 bg-black/5 rounded-full overflow-hidden flex-1 max-w-[200px]">
                        <div className="h-full bg-[--cvln-orange]" style={{ width: `${m.course_progress_pct}%` }} />
                      </div>
                      <span className="text-[10px] mono text-[--cvln-ink-2]">{m.course_progress_pct}%</span>
                    </div>
                  )}
                </div>
                {locked ? (
                  <button
                    data-testid={`module-locked-${m.code}`}
                    disabled
                    className="btn-outline text-sm opacity-60 cursor-not-allowed"
                  >
                    <Lock width={16} height={16} className="mr-1.5" /> {t("common.locked")}
                  </button>
                ) : (
                  <Link
                    to={`/formations/${code}/modules/${m.code}`}
                    data-testid={`module-open-${m.code}`}
                    className="btn-primary text-sm"
                  >
                    {status === "validated" ? t("common.review") : status === "available" ? (
                      <>{t("common.start")} <ArrowRight width={16} height={16} className="ml-1.5" /></>
                    ) : (
                      <>{t("common.continue_")} <PlaySolid width={16} height={16} className="ml-1.5" /></>
                    )}
                  </Link>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

function Row({ icon, label, value }) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2 text-xs uppercase tracking-wider text-[--cvln-ink-2]">
        {icon} {label}
      </div>
      <div className="text-sm font-semibold">{value}</div>
    </div>
  );
}
