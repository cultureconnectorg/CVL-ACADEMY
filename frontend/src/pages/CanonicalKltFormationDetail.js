import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import BackButton from "@/components/BackButton";
import { getCanonicalKltFormation, listCanonicalKltModules, listCanonicalKltSkills } from "@/lib/canonicalKltApi";
import { formatKltCompletenessLabel, formatKltPrerequisiteLabel, formatKltSkillStatusLabel } from "@/lib/canonicalKltDisplay";

/** "Branchage complet de Kiltikonet" — one formation's real module list,
 * ordered numerically (never lexicographically — see
 * `read_model.get_canonical_klt_formation`), plus its real skill
 * registry including BLOCKED rows — the one place a viewer sees exactly
 * which competencies remain unbuilt, and why. */
export default function CanonicalKltFormationDetail() {
  const { formationCode } = useParams();
  const [formation, setFormation] = useState(null);
  const [modules, setModules] = useState(null);
  const [skills, setSkills] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([
      getCanonicalKltFormation(formationCode),
      listCanonicalKltModules(formationCode),
      listCanonicalKltSkills(formationCode),
    ])
      .then(([f, m, s]) => {
        setFormation(f);
        setModules(m);
        setSkills(s);
      })
      .catch(() => setError("Formation Kiltikonet canonique introuvable."));
  }, [formationCode]);

  const blockedSkills = (skills || []).filter((s) => s.status === "BLOCKED");

  return (
    <div className="px-6 md:px-12 py-10 max-w-4xl" data-testid="canonical-klt-formation-detail-page">
      <BackButton to="/kiltikonet-canonical" label="Corpus Kiltikonet canonique" testId="back-to-canonical-klt" />

      {error && <div className="mt-8 text-red-600">{error}</div>}

      {formation && (
        <>
          <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange] mt-4">
            {formation.klt_formation_code}
          </div>
          <h1 className="font-display font-black text-3xl md:text-4xl tracking-tighter leading-none mt-2">
            {formation.title}
          </h1>
          <div className="text-sm mt-2" data-testid="canonical-klt-completeness-detail">
            {formatKltCompletenessLabel(formation)}
          </div>
        </>
      )}

      {blockedSkills.length > 0 && (
        <div
          className="mt-6 cvln-card p-4 border-amber-300 bg-amber-50 text-sm"
          data-testid="canonical-klt-blocked-skills"
        >
          <div className="font-semibold text-amber-900 mb-2">
            Compétences bloquées, non construites
          </div>
          <ul className="space-y-1">
            {blockedSkills.map((s) => (
              <li key={s.skill_id} data-testid={`canonical-klt-blocked-skill-${s.skill_id}`}>
                <span className="mono text-xs">{s.skill_id}</span> — {s.label} —{" "}
                {formatKltSkillStatusLabel(s)}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="mt-8 space-y-2" data-testid="canonical-klt-module-list">
        {(modules || []).map((m) => (
          <Link
            key={m.module_code}
            to={`/kiltikonet-canonical/${formationCode}/${m.module_code}`}
            className="cvln-card p-4 flex items-center justify-between gap-4 hover:border-[--cvln-orange]/50"
            data-testid={`canonical-klt-module-${m.module_code}`}
          >
            <div>
              <div className="text-[11px] mono uppercase tracking-wider text-[--cvln-ink-2]">
                {m.module_code}
              </div>
              <div className="font-semibold">{m.title}</div>
              <div className="text-xs text-[--cvln-ink-2] mt-0.5">
                {formatKltPrerequisiteLabel(m.prerequisites_raw)}
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
