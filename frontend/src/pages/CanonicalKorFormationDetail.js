import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import BackButton from "@/components/BackButton";
import { getCanonicalKorFormation, listCanonicalKorModules, listCanonicalKorSkills } from "@/lib/canonicalKorApi";
import { formatKorCompletenessLabel, formatKorPrerequisiteLabel } from "@/lib/canonicalKorDisplay";

/** RAIL 2 — one KORA formation's real module list, ordered numerically,
 * plus its real skill registry — including any skill whose module
 * reference never resolved to an imported module, the one place a
 * viewer sees exactly which competencies remain unbacked, and why. */
export default function CanonicalKorFormationDetail() {
  const { formationCode } = useParams();
  const [formation, setFormation] = useState(null);
  const [modules, setModules] = useState(null);
  const [skills, setSkills] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([
      getCanonicalKorFormation(formationCode),
      listCanonicalKorModules(formationCode),
      listCanonicalKorSkills(formationCode),
    ])
      .then(([f, m, s]) => {
        setFormation(f);
        setModules(m);
        setSkills(s);
      })
      .catch(() => setError("Formation KORA canonique introuvable."));
  }, [formationCode]);

  const unresolvedIds = new Set(formation?.unresolved_skill_ids || []);
  const unresolvedSkills = (skills || []).filter((s) => unresolvedIds.has(s.skill_id));

  return (
    <div className="px-6 md:px-12 py-10 max-w-4xl" data-testid="canonical-kor-formation-detail-page">
      <BackButton to="/kora-canonical" label="Corpus KORA canonique" testId="back-to-canonical-kor" />

      {error && <div className="mt-8 text-red-600">{error}</div>}

      {formation && (
        <>
          <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange] mt-4">
            {formation.kor_formation_code}
          </div>
          <h1 className="font-display font-black text-3xl md:text-4xl tracking-tighter leading-none mt-2">
            {formation.title}
          </h1>
          <div className="text-sm mt-2" data-testid="canonical-kor-completeness-detail">
            {formatKorCompletenessLabel(formation)}
          </div>
        </>
      )}

      {unresolvedSkills.length > 0 && (
        <div
          className="mt-6 cvln-card p-4 border-amber-300 bg-amber-50 text-sm"
          data-testid="canonical-kor-unresolved-skills"
        >
          <div className="font-semibold text-amber-900 mb-2">
            Compétences sans module canonique importé
          </div>
          <ul className="space-y-1">
            {unresolvedSkills.map((s) => (
              <li key={s.skill_id} data-testid={`canonical-kor-unresolved-skill-${s.skill_id}`}>
                <span className="mono text-xs">{s.skill_id}</span> — {s.label}
                {s.module_code_raw ? ` (module ${s.module_code_raw} référencé, non résolu)` : ""}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="mt-8 space-y-2" data-testid="canonical-kor-module-list">
        {(modules || []).map((m) => (
          <Link
            key={m.module_code}
            to={`/kora-canonical/${formationCode}/${m.module_code}`}
            className="cvln-card p-4 flex items-center justify-between gap-4 hover:border-[--cvln-orange]/50"
            data-testid={`canonical-kor-module-${m.module_code}`}
          >
            <div>
              <div className="text-[11px] mono uppercase tracking-wider text-[--cvln-ink-2]">
                {m.module_code}
              </div>
              <div className="font-semibold">{m.title}</div>
              <div className="text-xs text-[--cvln-ink-2] mt-0.5">
                {formatKorPrerequisiteLabel(m.prerequisites_raw)}
              </div>
            </div>
          </Link>
        ))}
        {modules && modules.length === 0 && (
          <div className="text-sm text-[--cvln-ink-2]" data-testid="canonical-kor-no-modules">
            Aucun module au format canonique importé pour cette formation.
          </div>
        )}
      </div>
    </div>
  );
}
