import { useEffect, useState } from "react";
import { UploadSquare, CheckCircle, WarningTriangle, Xmark } from "iconoir-react";
import { toast } from "sonner";
import { api } from "@/lib/api";

const inputCls =
  "w-full bg-white border-2 border-black/10 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-[--cvln-orange]";

function ImportPanel() {
  const [imports, setImports] = useState([]);
  const [busy, setBusy] = useState(false);

  const loadImports = () => api.get("/fms/imports").then((r) => setImports(r.data));

  useEffect(() => {
    loadImports().catch(() => {});
  }, []);

  const onFile = async (e) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;
    setBusy(true);
    const form = new FormData();
    form.append("file", file);
    try {
      const { data } = await api.post("/fms/import", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      toast[data.status === "success" ? "success" : data.status === "partial" ? "warning" : "error"](
        `Import ${data.status} — ${data.resources_created} ressource(s) créée(s).`,
      );
      await loadImports();
    } catch {
      toast.error("Échec de l'import du ZIP FMS.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="cvln-card p-6" data-testid="fms-import-panel">
      <h3 className="font-display font-bold text-xl tracking-tight mb-2">Importer un métier FMS</h3>
      <p className="text-sm text-[--cvln-ink-2] mb-4">
        Archive .zip contenant les fichiers Markdown (référentiel, learning map, module map, blueprint,
        modules, QCM, cas N2, assessment, templates, guides).
      </p>
      <label className="btn-primary inline-flex cursor-pointer" data-testid="fms-import-btn">
        <UploadSquare width={18} height={18} className="mr-2" />
        {busy ? "Import en cours…" : "Importer un métier FMS"}
        <input type="file" accept=".zip" className="hidden" onChange={onFile} disabled={busy} />
      </label>

      <div className="mt-6 space-y-2">
        {imports.map((report) => (
          <div key={report.id} className="px-4 py-3 rounded-xl border border-black/5" data-testid={`import-report-${report.id}`}>
            <div className="flex items-center justify-between gap-3">
              <div className="min-w-0">
                <div className="font-semibold truncate">{report.filename}</div>
                <div className="text-xs text-[--cvln-ink-2]">
                  {report.resources_created} ressource(s) · {report.issues.length} signalement(s)
                </div>
              </div>
              <StatusPill status={report.status} />
            </div>
            {report.issues.length > 0 && (
              <ul className="mt-2 space-y-1">
                {report.issues.slice(0, 5).map((issue, i) => (
                  <li key={i} className="text-xs text-[--cvln-ink-2] flex items-start gap-1.5">
                    {issue.level === "error" ? (
                      <Xmark width={12} height={12} className="text-red-500 mt-0.5 shrink-0" />
                    ) : (
                      <WarningTriangle width={12} height={12} className="text-amber-500 mt-0.5 shrink-0" />
                    )}
                    <span className="truncate">{issue.file} — {issue.message}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function StatusPill({ status }) {
  const styles = {
    success: "bg-[--cvln-forest] text-white",
    partial: "bg-amber-100 text-amber-800",
    failed: "bg-red-100 text-red-700",
  };
  return (
    <span className={`text-xs font-bold px-3 py-1 rounded-full whitespace-nowrap ${styles[status] || ""}`}>
      {status}
    </span>
  );
}

function IntegrationsPanel() {
  const [rows, setRows] = useState([]);

  useEffect(() => {
    api.get("/integrations").then((r) => setRows(r.data)).catch(() => {});
  }, []);

  return (
    <div className="cvln-card p-6" data-testid="integrations-panel">
      <h3 className="font-display font-bold text-xl tracking-tight mb-4">Écosystème CVLN</h3>
      <div className="space-y-2">
        {rows.map((row) => (
          <div key={row.name} className="flex items-center justify-between px-4 py-2.5 rounded-xl border border-black/5">
            <div className="text-sm font-semibold">{row.name}</div>
            {row.configured ? (
              <span className="text-xs font-bold text-[--cvln-forest] flex items-center gap-1">
                <CheckCircle width={14} height={14} /> Configuré
              </span>
            ) : (
              <span className="text-xs text-[--cvln-ink-2]">Non configuré</span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function OrgsPanel() {
  const [orgs, setOrgs] = useState([]);
  const [name, setName] = useState("");
  const [slug, setSlug] = useState("");
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState("student");
  const [lastCode, setLastCode] = useState(null);

  const loadOrgs = () => api.get("/orgs").then((r) => setOrgs(r.data));

  useEffect(() => {
    loadOrgs().catch(() => {});
  }, []);

  const createOrg = async (e) => {
    e.preventDefault();
    try {
      await api.post("/orgs", { name, slug });
      toast.success("Organisation créée.");
      setName("");
      setSlug("");
      await loadOrgs();
    } catch {
      toast.error("Impossible de créer l'organisation.");
    }
  };

  const createInvite = async (e) => {
    e.preventDefault();
    try {
      const { data } = await api.post("/invitations", { email: inviteEmail || undefined, role: inviteRole });
      setLastCode(data.code);
      toast.success("Invitation créée.");
      setInviteEmail("");
    } catch {
      toast.error("Impossible de créer l'invitation.");
    }
  };

  return (
    <div className="cvln-card p-6" data-testid="orgs-panel">
      <h3 className="font-display font-bold text-xl tracking-tight mb-4">Organisations & invitations</h3>

      <form onSubmit={createOrg} className="flex flex-wrap gap-2 mb-4" data-testid="create-org-form">
        <input className={inputCls} placeholder="Nom" value={name} onChange={(e) => setName(e.target.value)} required />
        <input className={inputCls} placeholder="slug" value={slug} onChange={(e) => setSlug(e.target.value)} required />
        <button type="submit" className="btn-outline">Créer l&apos;organisation</button>
      </form>

      <div className="flex flex-wrap gap-2 mb-2">
        {orgs.map((o) => (
          <span key={o.id} className="text-xs px-3 py-1 rounded-full bg-[--cvln-bg-warm]" data-testid={`org-${o.slug}`}>
            {o.name}
          </span>
        ))}
      </div>

      <form onSubmit={createInvite} className="flex flex-wrap gap-2 mt-4" data-testid="create-invite-form">
        <input
          className={inputCls}
          placeholder="Email (optionnel)"
          value={inviteEmail}
          onChange={(e) => setInviteEmail(e.target.value)}
        />
        <select className={inputCls} value={inviteRole} onChange={(e) => setInviteRole(e.target.value)}>
          {["student", "trainer", "corrector", "jury", "admin"].map((r) => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
        <button type="submit" className="btn-outline">Générer une invitation</button>
      </form>
      {lastCode && (
        <div className="mt-3 text-sm mono px-4 py-2 rounded-xl bg-[--cvln-bg-warm]" data-testid="invite-code">
          Code : <strong>{lastCode}</strong>
        </div>
      )}
    </div>
  );
}

export default function AdminDashboard() {
  return (
    <div className="px-6 md:px-12 py-10 max-w-6xl" data-testid="admin-dashboard-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">Admin CMS</div>
      <h1 className="font-display font-black text-4xl tracking-tighter mt-2">Administration</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        <ImportPanel />
        <IntegrationsPanel />
      </div>
      <div className="mt-6">
        <OrgsPanel />
      </div>
    </div>
  );
}
