import { useCallback, useEffect, useState } from "react";
import { CheckCircle, Coins, Lock, Wallet } from "iconoir-react";
import { Link } from "react-router-dom";

import { api, getToken } from "@/lib/api";
import BillingInvoicePanel from "@/components/BillingInvoicePanel";

const POLICY_COPY = {
  QUOTE_REQUIRED: "Cette offre passe par un devis B2B/B2G ou entreprise.",
  ELIGIBILITY_REQUIRED: "Cette offre nécessite une validation d’éligibilité.",
  NOT_FOR_SALE: "Cette capacité n’est pas vendue séparément.",
};

function apiDetail(error) {
  return error?.response?.data?.detail || "COMMERCIAL_UNAVAILABLE";
}

export default function CommercialPurchaseCard({ economyCode, onAccessState }) {
  const authenticated = Boolean(getToken());
  const [offer, setOffer] = useState(null);
  const [accessActive, setAccessActive] = useState(false);
  const [policyState, setPolicyState] = useState(null);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");

  const publishAccess = useCallback(
    (required, active) => {
      setAccessActive(active);
      onAccessState?.({ required, active });
    },
    [onAccessState]
  );

  useEffect(() => {
    let alive = true;
    if (!authenticated) {
      publishAccess(true, false);
      return () => {
        alive = false;
      };
    }

    async function loadCommercialState() {
      try {
        const [offerResponse, entitlementResponse] = await Promise.all([
          api.get(`/commercial/offers/${economyCode}`),
          api.get("/commercial/entitlements/mine"),
        ]);
        if (!alive) return;
        const nextOffer = offerResponse.data;
        const active = (entitlementResponse.data || []).some(
          (item) => item.economy_code === economyCode && item.status === "ACTIVE"
        );
        setOffer(nextOffer);
        setPolicyState(null);
        publishAccess(true, active);
      } catch (error) {
        if (!alive) return;
        const detail = apiDetail(error);
        if (["NOT_FOR_SALE", "QUOTE_REQUIRED", "ELIGIBILITY_REQUIRED"].includes(detail)) {
          setPolicyState(detail);
          publishAccess(detail !== "NOT_FOR_SALE", false);
          return;
        }
        if (error?.response?.status === 404) {
          setPolicyState("NO_ECONOMY_MAPPING");
          publishAccess(false, true);
          return;
        }
        setMessage("Le service commercial n’est pas disponible pour le moment.");
        publishAccess(true, false);
      }
    }

    loadCommercialState();
    return () => {
      alive = false;
    };
  }, [authenticated, economyCode, publishAccess]);

  async function payWithWallet() {
    if (!offer || busy) return;
    setBusy(true);
    setMessage("");
    try {
      const orderResponse = await api.post("/commercial/orders", {
        economy_code: economyCode,
        offer_kind: offer.offer_kind,
      });
      const paidResponse = await api.post(
        `/commercial/orders/${orderResponse.data.order_id}/pay-wallet`
      );
      if (paidResponse.data.status !== "PAID") {
        throw new Error("PAYMENT_NOT_CONFIRMED");
      }
      publishAccess(true, true);
      setMessage("Paiement confirmé. Ton accès est actif.");
    } catch (error) {
      const detail = apiDetail(error);
      if (detail === "REQUIRES_REVIEW") {
        setMessage(
          "Le résultat Wallet est ambigu. Aucun nouvel essai automatique : vérification requise."
        );
      } else if (detail === "WALLET_PAYMENT_REJECTED") {
        setMessage("Paiement refusé par CVLN Wallet.");
      } else if (detail === "CVLN_WALLET_NOT_CONFIGURED") {
        setMessage("CVLN Wallet n’est pas encore activé dans cet environnement.");
      } else {
        setMessage("Le paiement n’a pas pu être confirmé.");
      }
    } finally {
      setBusy(false);
    }
  }

  if (!authenticated) {
    return (
      <div className="cvln-card p-5" data-testid="commercial-login-card">
        <div className="flex items-center gap-2 font-semibold">
          <Lock width={18} height={18} /> Accès au parcours
        </div>
        <p className="text-sm text-[--cvln-ink-2] mt-2">
          Connecte-toi pour voir ton éligibilité et ton offre Academy.
        </p>
        <Link to="/login" className="btn-primary text-sm mt-4 inline-flex">
          Se connecter
        </Link>
      </div>
    );
  }

  if (policyState === "NO_ECONOMY_MAPPING" || policyState === "NOT_FOR_SALE") {
    return null;
  }

  if (policyState) {
    return (
      <div className="cvln-card p-5" data-testid="commercial-policy-card">
        <div className="flex items-center gap-2 font-semibold">
          <Lock width={18} height={18} /> Accès encadré
        </div>
        <p className="text-sm text-[--cvln-ink-2] mt-2">
          {POLICY_COPY[policyState] || "Cette offre nécessite une validation."}
        </p>
      </div>
    );
  }

  if (!offer) {
    return message ? (
      <div className="cvln-card p-5 text-sm text-[--cvln-ink-2]">{message}</div>
    ) : null;
  }

  if (accessActive) {
    return (
      <div className="space-y-4">
        <div className="cvln-card p-5" data-testid="commercial-access-active">
          <div className="flex items-center gap-2 font-semibold text-[#15803D]">
            <CheckCircle width={20} height={20} /> Accès actif
          </div>
          <p className="text-sm text-[--cvln-ink-2] mt-2">
            Ton entitlement Academy est actif pour {economyCode}.
          </p>
          {message && <p className="text-sm mt-2">{message}</p>}
        </div>
        <BillingInvoicePanel economyCode={economyCode} />
      </div>
    );
  }

  return (
    <div className="cvln-card p-5" data-testid="commercial-purchase-card">
      <div className="flex items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 font-semibold">
            <Coins width={18} height={18} /> Parcours Academy
          </div>
          <div className="font-display font-black text-3xl mt-2">
            {Number(offer.amount_eur).toLocaleString("fr-FR")} €
          </div>
          <div className="text-xs text-[--cvln-ink-2] mt-1">
            Prix calculé côté serveur · {offer.requirement_id}
          </div>
        </div>
        <Wallet width={30} height={30} className="text-[--cvln-orange]" />
      </div>
      <button
        type="button"
        className="btn-primary w-full mt-4 justify-center"
        onClick={payWithWallet}
        disabled={busy}
        data-testid="commercial-pay-wallet"
      >
        {busy ? "Paiement en cours…" : "Payer avec CVLN Wallet"}
      </button>
      <p className="text-[11px] text-[--cvln-ink-2] mt-3">
        Le montant Wallet est figé dans la commande par le backend avant débit.
      </p>
      {message && <p className="text-sm mt-3">{message}</p>}
    </div>
  );
}
