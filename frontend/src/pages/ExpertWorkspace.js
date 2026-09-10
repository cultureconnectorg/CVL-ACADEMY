import { useState } from "react";

const API_BASE = process.env.REACT_APP_BACKEND_URL || "";

export default function ExpertWorkspace() {
  const [caseId, setCaseId] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [workspace, setWorkspace] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function openWorkspace(event) {
    event.preventDefault();
    setError("");
    setWorkspace(null);
    setLoading(true);
    try {
      const response = await fetch(
        `${API_BASE}/api/governance-advanced/expert-workspace/${encodeURIComponent(caseId)}`,
        {
          headers: { "X-CVLN-Expert-Key": apiKey },
        },
      );
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(body.detail || "Accès refusé");
      setWorkspace(body);
    } catch (err) {
      setError(err.message || "Accès refusé");
    } finally {
      setLoading(false);
    }
  }

  function closeWorkspace() {
    setWorkspace(null);
    setApiKey("");
    setError("");
  }

  if (workspace) {
    const queues = workspace.queues || {};
    return (
      <main className="mx-auto max-w-6xl p-6" data-testid="expert-workspace">
        <div className="mb-6 flex items-start justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-widest text-neutral-500">
              {workspace.domain} · périmètre assigné uniquement
            </p>
            <h1 className="text-3xl font-semibold">{workspace.case?.title}</h1>
            <p className="mt-2 text-neutral-600">{workspace.case?.description}</p>
          </div>
          <button className="rounded border px-4 py-2" onClick={closeWorkspace}>
            Fermer
          </button>
        </div>

        <section className="grid gap-4 md:grid-cols-3">
          <article className="rounded-xl border p-4">
            <h2 className="font-semibold">Expert</h2>
            <p>{workspace.expert?.display_name}</p>
            <p className="text-sm text-neutral-500">
              Autorité: {workspace.assignment?.authority_level || "—"}
            </p>
          </article>
          <article className="rounded-xl border p-4">
            <h2 className="font-semibold">Documents</h2>
            <p className="text-2xl">{queues.documents?.length || 0}</p>
          </article>
          <article className="rounded-xl border p-4">
            <h2 className="font-semibold">Décisions</h2>
            <p className="text-2xl">{queues.decisions?.length || 0}</p>
          </article>
        </section>

        <section className="mt-6 rounded-xl border p-4">
          <h2 className="font-semibold">Scopes accordés</h2>
          <div className="mt-2 flex flex-wrap gap-2">
            {(workspace.assignment?.scope || []).map((scope) => (
              <span key={scope} className="rounded-full border px-3 py-1 text-sm">
                {scope}
              </span>
            ))}
          </div>
        </section>

        <p className="mt-6 text-xs text-neutral-500">
          Global browse: disabled · Cross-case access: disabled. La clé reste uniquement
          en mémoire de cette page et est effacée à la fermeture.
        </p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-xl p-6" data-testid="expert-login-shell">
      <h1 className="text-3xl font-semibold">Espace professionnel CVLN Academy</h1>
      <p className="mt-2 text-neutral-600">
        Ouvrez uniquement le dossier qui vous a été assigné avec votre clé professionnelle.
      </p>
      <form className="mt-6 space-y-4" onSubmit={openWorkspace}>
        <label className="block">
          <span className="text-sm">Dossier</span>
          <input
            className="mt-1 w-full rounded border px-3 py-2"
            value={caseId}
            onChange={(event) => setCaseId(event.target.value)}
            autoComplete="off"
            required
          />
        </label>
        <label className="block">
          <span className="text-sm">Clé expert</span>
          <input
            className="mt-1 w-full rounded border px-3 py-2"
            value={apiKey}
            onChange={(event) => setApiKey(event.target.value)}
            type="password"
            autoComplete="off"
            required
          />
        </label>
        {error ? <p className="text-sm text-red-700">{error}</p> : null}
        <button className="w-full rounded bg-black px-4 py-2 text-white" disabled={loading}>
          {loading ? "Vérification…" : "Ouvrir mon dossier"}
        </button>
      </form>
    </main>
  );
}
