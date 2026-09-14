import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "@/lib/api";
import { useI18n } from "@/lib/i18n.jsx";

// ACA-0030 — Ecosystem Builder surface (consumer -> learner ->
// professional -> builder). Composes GET /ecosystem-builder/me, itself
// a composition of already-real data (see backend/services/
// ecosystem_builder.py's module docstring for the exact scope
// contract). Nothing here invents Projects/Collaborations/Network/
// Economic activity rows — those stay absent, per that same contract.
const STAGES = ["consumer", "learner", "professional", "builder"];

function StageTrack({ stage, t }) {
  const activeIdx = STAGES.indexOf(stage);
  return (
    <div className="flex items-center gap-2" data-testid="builder-stage-track">
      {STAGES.map((s, i) => (
        <div key={s} className="flex items-center gap-2 flex-1">
          <div
            data-testid={`builder-stage-${s}`}
            data-active={i === activeIdx}
            className={`flex-1 text-center py-2 rounded-xl text-xs font-bold uppercase tracking-[0.15em] transition
              ${i <= activeIdx
                ? "bg-[--cvln-forest] text-white"
                : "bg-[--cvln-bg-warm] text-[--cvln-ink-2]"}`}
          >
            {t(`ecosystem_builder_p.stage_${s}`)}
          </div>
          {i < STAGES.length - 1 && (
            <div className={`h-0.5 w-4 shrink-0 ${i < activeIdx ? "bg-[--cvln-forest]" : "bg-black/10"}`} />
          )}
        </div>
      ))}
    </div>
  );
}

export default function EcosystemBuilder() {
  const { t } = useI18n();
  const [surface, setSurface] = useState(null);

  useEffect(() => {
    api.get("/ecosystem-builder/me").then((r) => setSurface(r.data)).catch(() => {});
  }, []);

  if (!surface) {
    return (
      <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="ecosystem-builder-page">
        <div className="text-sm text-[--cvln-ink-2]">…</div>
      </div>
    );
  }

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="ecosystem-builder-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">
        {t("ecosystem_builder")}
      </div>
      <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-2">
        {t("ecosystem_builder_p.hero_title")}
      </h1>
      <p className="text-[--cvln-ink-2] mt-3 max-w-2xl">{t("ecosystem_builder_p.hero_p")}</p>

      {/* Stage track */}
      <div className="mt-10 cvln-card p-6" data-testid="builder-stage-card">
        <div className="text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-ink-2] mb-3">
          {t("ecosystem_builder_p.stage_label")}
        </div>
        <StageTrack stage={surface.stage} t={t} />
        <p className="text-sm text-[--cvln-ink-2] mt-4" data-testid="builder-stage-desc">
          {t(`ecosystem_builder_p.stage_${surface.stage}_desc`)}
        </p>
        {surface.stage === "professional" && (
          <Link
            to="/frek-profile"
            data-testid="builder-become-builder-cta"
            className="inline-block mt-3 text-xs font-semibold text-[--cvln-orange]"
          >
            {t("ecosystem_builder_p.become_builder_cta")}
          </Link>
        )}
      </div>

      <div className="mt-8 grid md:grid-cols-2 gap-6">
        {/* Portfolio */}
        <div className="cvln-card p-6" data-testid="builder-portfolio-card">
          <h3 className="font-display font-bold text-xl tracking-tight mb-3">
            {t("ecosystem_builder_p.portfolio_title")}
          </h3>
          {surface.portfolio.length === 0 ? (
            <div className="text-sm text-[--cvln-ink-2]">{t("ecosystem_builder_p.no_portfolio")}</div>
          ) : (
            <div className="space-y-2">
              {surface.portfolio.map((s) => (
                <div
                  key={s.skill_id}
                  className="p-3 rounded-xl border border-black/10"
                  data-testid={`builder-portfolio-${s.skill_id}`}
                >
                  <div className="mono text-xs text-[--cvln-orange] font-bold">{s.skill_id}</div>
                  <div className="text-sm font-semibold">{s.label}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Credentials */}
        <div className="cvln-card p-6" data-testid="builder-credentials-card">
          <h3 className="font-display font-bold text-xl tracking-tight mb-3">
            {t("ecosystem_builder_p.credentials_title")}
          </h3>
          {surface.credentials.length === 0 ? (
            <div className="text-sm text-[--cvln-ink-2]">{t("ecosystem_builder_p.no_credentials")}</div>
          ) : (
            <div className="space-y-2">
              {surface.credentials.map((c) => (
                <div
                  key={c.certification_code}
                  className="flex items-center justify-between p-3 rounded-xl border border-black/10"
                  data-testid={`builder-credential-${c.certification_code}`}
                >
                  <span className="mono font-bold">{c.certification_code}</span>
                  <span className="text-sm text-[--cvln-ink-2]">{c.mention}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Verified proofs */}
        <div className="cvln-card p-6" data-testid="builder-proofs-card">
          <h3 className="font-display font-bold text-xl tracking-tight mb-3">
            {t("ecosystem_builder_p.proofs_title")}
          </h3>
          {surface.verified_proofs.length === 0 ? (
            <div className="text-sm text-[--cvln-ink-2]">{t("ecosystem_builder_p.no_proofs")}</div>
          ) : (
            <div className="space-y-1 mono text-xs">
              {surface.verified_proofs.map((p, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between px-2 py-1.5 rounded-lg hover:bg-[--cvln-bg-warm]"
                  data-testid={`builder-proof-${i}`}
                >
                  <span className="text-[--cvln-orange] font-bold">{p.skill_id}</span>
                  <span className="text-[--cvln-ink-2] truncate max-w-[40%]">{p.evidence_type}</span>
                  <span className="text-[--cvln-ink-2]">{p.sha256.slice(0, 10)}…</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Missions completed */}
        <div className="cvln-card p-6" data-testid="builder-missions-card">
          <h3 className="font-display font-bold text-xl tracking-tight mb-3">
            {t("ecosystem_builder_p.missions_title")}
          </h3>
          {surface.missions_completed.length === 0 ? (
            <div className="text-sm text-[--cvln-ink-2]">{t("ecosystem_builder_p.no_missions")}</div>
          ) : (
            <div className="space-y-1 mono text-xs">
              {surface.missions_completed.map((m) => (
                <div
                  key={m.mission_code}
                  className="flex items-center justify-between px-2 py-1.5 rounded-lg hover:bg-[--cvln-bg-warm]"
                  data-testid={`builder-mission-${m.mission_code}`}
                >
                  <span className="text-[--cvln-orange] font-bold">{m.mission_code}</span>
                  <span className="text-[--cvln-ink-2]">
                    {m.submitted_at ? new Date(m.submitted_at).toLocaleDateString() : "—"}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Ecosystem history */}
      <div className="mt-8 cvln-card p-6" data-testid="builder-history-card">
        <h3 className="font-display font-bold text-xl tracking-tight mb-3">
          {t("ecosystem_builder_p.history_title")}
        </h3>
        {surface.ecosystem_history.length === 0 ? (
          <div className="text-sm text-[--cvln-ink-2]">{t("ecosystem_builder_p.no_history")}</div>
        ) : (
          <div className="space-y-1 mono text-xs">
            {surface.ecosystem_history.map((h, i) => (
              <div
                key={i}
                className="flex items-center justify-between px-2 py-1.5 rounded-lg hover:bg-[--cvln-bg-warm]"
                data-testid={`builder-history-${i}`}
              >
                <span className="text-[--cvln-orange] font-bold">{h.event_type}</span>
                <span className="text-[--cvln-ink-2] text-xs">
                  {new Date(h.published_at).toLocaleString()}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
