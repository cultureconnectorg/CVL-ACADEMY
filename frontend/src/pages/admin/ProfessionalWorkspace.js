import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "@/lib/api";

function asArray(value) {
  return Array.isArray(value) ? value : [];
}

function GateCard({ title, gate }) {
  const passed = gate?.pass === true;
  return (
    <div className="cvln-card p-5" data-testid={`gate-${title.toLowerCase().replaceAll(" ", "-")}`}>
      <div className="text-xs mono uppercase tracking-wider text-[--cvln-ink-2]">{title}</div>
      <div className={`font-display font-bold text-2xl mt-2 ${passed ? "text-[--cvln-forest]" : "text-red-700"}`}>
        {gate ? (passed ? "PASS" : "BLOCKED") : "…"}
      </div>
      {gate && !passed && (
        <div className="text-xs text-[--cvln-ink-2] mt-2">
          {gate.blocking_count ?? 0} blocage(s) actif(s)
        </div>
      )}
    </div>
  );
}

export default function ProfessionalWorkspace() {
  const [cases, setCases] = useState([]);
  const [experts, setExperts] = useState([]);
  const [securityGate, setSecurityGate] = useState(null);
  const [riskGate, setRiskGate] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([
      api.get("/governance/cases"),
      api.get("/governance/experts"),
      api.get("/assurance/security/release-gate"),
      api.get("/assurance/risks/critical-gate"),
    ])
      .then(([caseRes, expertRes, secRes, riskRes]) => {
        setCases(asArray(caseRes.data));
        setExperts(asArray(expertRes.data));
        setSecurityGate(secRes.data && typeof secRes.data === "object" ? secRes.data : null);
        setRiskGate(riskRes.data && typeof riskRes.data === "object" ? riskRes.data : null);
      })
      .catch((err) => setError(err?.response?.data?.detail || "Professional workspace unavailable"));
  }, []);

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="professional-workspace-page">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">
            Governance · Assurance
          </div>
          <h1 className="font-display font-black text-4xl tracking-tighter mt-2">
            Professional Workspace
          </h1>
          <p className="text-[--cvln-ink-2] mt-2 max-w-2xl">
            Vue opérationnelle des dossiers professionnels, experts assignables et gates de release.
          </p>
        </div>
        <Link to="/admin" className="btn-outline">Retour Admin</Link>
      </div>

      {error && (
        <div className="mt-6 cvln-card p-5 border-red-200 text-red-700" data-testid="workspace-error">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
        <GateCard title="Security Gate" gate={securityGate} />
        <GateCard title="Critical Risk Gate" gate={riskGate} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <section className="cvln-card p-6" data-testid="workspace-cases">
          <div className="flex items-center justify-between">
            <h2 className="font-display font-bold text-xl">Dossiers professionnels</h2>
            <span className="mono text-xs text-[--cvln-ink-2]">{cases.length}</span>
          </div>
          <div className="mt-4 space-y-2">
            {cases.length === 0 && <div className="text-sm text-[--cvln-ink-2]">Aucun dossier.</div>}
            {cases.map((row) => (
              <div key={row.id} className="border border-black/5 rounded-xl p-4" data-testid={`case-${row.id}`}>
                <div className="flex items-center justify-between gap-3">
                  <strong className="truncate">{row.title}</strong>
                  <span className="text-[10px] mono uppercase">{row.status}</span>
                </div>
                <div className="text-xs text-[--cvln-ink-2] mt-1">{row.domain} · {row.sensitivity}</div>
              </div>
            ))}
          </div>
        </section>

        <section className="cvln-card p-6" data-testid="workspace-experts">
          <div className="flex items-center justify-between">
            <h2 className="font-display font-bold text-xl">Experts</h2>
            <span className="mono text-xs text-[--cvln-ink-2]">{experts.length}</span>
          </div>
          <div className="mt-4 space-y-2">
            {experts.length === 0 && <div className="text-sm text-[--cvln-ink-2]">Aucun expert.</div>}
            {experts.map((row) => (
              <div key={row.id} className="border border-black/5 rounded-xl p-4" data-testid={`expert-${row.id}`}>
                <div className="font-semibold">{row.display_name}</div>
                <div className="text-xs text-[--cvln-ink-2] mt-1">
                  {asArray(row.domains).join(" · ") || "Aucun domaine"}
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
