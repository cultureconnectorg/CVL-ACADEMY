import { useEffect, useState } from "react";
import { toast } from "sonner";
import { api } from "@/lib/api";

const inputCls =
  "w-full bg-white border-2 border-black/10 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-[--cvln-orange] focus:ring-2 focus:ring-[--cvln-orange]/30";

export default function StakeholderAccessPanel() {
  const [orgs, setOrgs] = useState([]);
  const [orgId, setOrgId] = useState("");
  const [email, setEmail] = useState("");
  const [type, setType] = useState("partner");
  const [code, setCode] = useState(null);

  useEffect(() => {
    api
      .get("/orgs")
      .then((r) => {
        setOrgs(r.data);
        if (r.data.length) setOrgId((current) => current || r.data[0].id);
      })
      .catch(() => {});
  }, []);

  const createInvite = async (e) => {
    e.preventDefault();
    try {
      const { data } = await api.post("/stakeholders/invitations", {
        org_id: orgId,
        stakeholder_type: type,
        email: email || undefined,
      });
      setCode(data.code);
      setEmail("");
      toast.success("Invitation d'accès créée");
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Impossible de créer l'invitation");
    }
  };

  return (
    <div className="cvln-card p-6" data-testid="stakeholder-access-panel">
      <h3 className="font-display font-bold text-xl tracking-tight mb-2">
        Partenaires & institutions
      </h3>
      <p className="text-sm text-[--cvln-ink-2] mb-4">
        Crée un accès organisation-scopé sans transformer le partenaire en administrateur CVLN.
      </p>
      <form onSubmit={createInvite} className="space-y-3">
        <select
          className={inputCls}
          value={orgId}
          onChange={(e) => setOrgId(e.target.value)}
          required
        >
          <option value="" disabled>
            Choisir une organisation
          </option>
          {orgs.map((org) => (
            <option key={org.id} value={org.id}>
              {org.name}
            </option>
          ))}
        </select>
        <select className={inputCls} value={type} onChange={(e) => setType(e.target.value)}>
          <option value="partner">Partenaire</option>
          <option value="institution">Institution / financeur</option>
        </select>
        <input
          className={inputCls}
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email du représentant (optionnel)"
        />
        <button type="submit" className="btn-outline" disabled={!orgId}>
          Générer l'accès
        </button>
      </form>
      {code && (
        <div
          className="mt-4 rounded-xl bg-[--cvln-bg-warm] p-4 text-sm"
          data-testid="stakeholder-invite-code"
        >
          <div className="font-semibold">Code d'accès</div>
          <div className="mono break-all mt-1">{code}</div>
          <div className="text-xs text-[--cvln-ink-2] mt-2">
            Lien à transmettre : /stakeholder/claim/{code}
          </div>
        </div>
      )}
    </div>
  );
}
