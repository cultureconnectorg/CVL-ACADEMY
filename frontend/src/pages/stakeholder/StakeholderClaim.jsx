import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";

export default function StakeholderClaim() {
  const { code } = useParams();
  const { user } = useAuth();
  const nav = useNavigate();
  const [invite, setInvite] = useState(null);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api
      .get(`/stakeholders/invitations/${code}`)
      .then((r) => setInvite(r.data))
      .catch((err) => setError(err?.response?.data?.detail || "Invitation invalide."));
  }, [code]);

  const claim = async () => {
    if (!user) {
      toast.error("Connectez-vous d'abord avec le compte destinataire.");
      nav("/");
      return;
    }
    setBusy(true);
    try {
      const { data } = await api.post(`/stakeholders/invitations/${code}/claim`);
      const target =
        data.membership.stakeholder_type === "institution" ? "/institution" : "/partner";
      toast.success("Accès activé.");
      nav(target, { replace: true });
    } catch (err) {
      setError(err?.response?.data?.detail || "Impossible d'activer cet accès.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div
      className="min-h-[70vh] flex items-center justify-center px-6 py-12"
      data-testid="stakeholder-claim-page"
    >
      <div className="cvln-card p-7 max-w-xl w-full">
        <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">
          Accès CVLN Academy
        </div>
        <h1 className="font-display font-black text-3xl tracking-tight mt-2">
          Invitation partenaire / institution
        </h1>
        {error ? (
          <div className="mt-5 text-sm text-red-700">{error}</div>
        ) : !invite ? null : (
          <>
            <div className="mt-5 rounded-xl bg-[--cvln-bg-warm] p-4 text-sm">
              <div>
                <strong>Organisation :</strong> {invite.org_name}
              </div>
              <div className="mt-1">
                <strong>Type d’accès :</strong> {invite.stakeholder_type}
              </div>
              {invite.email && (
                <div className="mt-1">
                  <strong>Compte attendu :</strong> {invite.email}
                </div>
              )}
            </div>
            <button className="btn-primary mt-5" onClick={claim} disabled={busy}>
              {busy ? "Activation…" : "Activer mon espace"}
            </button>
          </>
        )}
      </div>
    </div>
  );
}
