import { useCallback, useEffect, useState } from "react";
import { CheckCircle, Download, Page, WarningTriangle } from "iconoir-react";

import { api } from "@/lib/api";

const EMPTY_PROFILE = {
  legal_name: "",
  address_line1: "",
  city: "",
  postal_code: "",
  country: "",
  vat_id: "",
  registration_id: "",
};

function apiDetail(error) {
  return error?.response?.data?.detail || "BILLING_UNAVAILABLE";
}

export default function BillingInvoicePanel({ economyCode }) {
  const [invoice, setInvoice] = useState(null);
  const [profile, setProfile] = useState(EMPTY_PROFILE);
  const [profileLoaded, setProfileLoaded] = useState(false);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");

  const load = useCallback(async () => {
    const invoiceResponse = await api.get("/billing/invoices/mine", {
      params: { economy_code: economyCode },
    });
    const latest = (invoiceResponse.data || [])[0] || null;
    setInvoice(latest);

    try {
      const profileResponse = await api.get("/billing/profile");
      setProfile({ ...EMPTY_PROFILE, ...profileResponse.data });
    } catch (error) {
      if (error?.response?.status !== 404) throw error;
    } finally {
      setProfileLoaded(true);
    }
  }, [economyCode]);

  useEffect(() => {
    let alive = true;
    load().catch(() => {
      if (alive) setMessage("La facturation n’est pas disponible pour le moment.");
    });
    return () => {
      alive = false;
    };
  }, [load]);

  function updateField(event) {
    const { name, value } = event.target;
    setProfile((current) => ({ ...current, [name]: value }));
  }

  async function saveProfile() {
    const payload = {
      legal_name: profile.legal_name,
      address_line1: profile.address_line1,
      city: profile.city,
      postal_code: profile.postal_code,
      country: profile.country.trim().toUpperCase(),
      vat_id: profile.vat_id || null,
      registration_id: profile.registration_id || null,
      registration_scheme: "0002",
    };
    const response = await api.put("/billing/profile", payload);
    setProfile({ ...EMPTY_PROFILE, ...response.data });
    return response.data;
  }

  async function issueInvoice() {
    if (!invoice || busy) return;
    setBusy(true);
    setMessage("");
    try {
      await saveProfile();
      const response = await api.post(`/billing/orders/${invoice.order_id}/issue`);
      setInvoice(response.data);
      setMessage("Facture Factur-X EN16931 émise et validée.");
    } catch (error) {
      const detail = apiDetail(error);
      if (detail === "EINVOICE_GENERATION_FAILED") {
        setMessage("La validation Factur-X a échoué. La facture n’a pas été marquée émise.");
      } else if (detail === "BILLING_PROFILE_REQUIRED") {
        setMessage("Complète les informations de facturation.");
      } else {
        setMessage(typeof detail === "string" ? detail : "Émission impossible.");
      }
    } finally {
      setBusy(false);
    }
  }

  async function download(kind) {
    if (!invoice || invoice.status !== "ISSUED") return;
    setBusy(true);
    setMessage("");
    try {
      const response = await api.get(
        `/billing/orders/${invoice.order_id}/invoice/${kind}`,
        { responseType: "blob" }
      );
      const extension = kind === "pdf" ? "pdf" : "xml";
      const url = window.URL.createObjectURL(response.data);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = `${invoice.legal_invoice_number}.${extension}`;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      setMessage(apiDetail(error));
    } finally {
      setBusy(false);
    }
  }

  if (!invoice && !message) return null;

  if (!invoice) {
    return (
      <div className="cvln-card p-5" data-testid="billing-unavailable-card">
        <div className="flex items-center gap-2 font-semibold">
          <WarningTriangle width={18} height={18} /> Facturation
        </div>
        <p className="text-sm text-[--cvln-ink-2] mt-2">{message}</p>
      </div>
    );
  }

  if (invoice.status === "ISSUED") {
    return (
      <div className="cvln-card p-5" data-testid="billing-issued-card">
        <div className="flex items-center gap-2 font-semibold text-[#15803D]">
          <CheckCircle width={20} height={20} /> Facture émise
        </div>
        <div className="font-semibold mt-2" data-testid="billing-invoice-number">
          {invoice.legal_invoice_number}
        </div>
        <p className="text-xs text-[--cvln-ink-2] mt-1">
          {invoice.einvoice_format} · XSD {invoice.einvoice_validation}
        </p>
        <div className="grid grid-cols-2 gap-2 mt-4">
          <button
            type="button"
            className="btn-outline text-sm justify-center"
            onClick={() => download("pdf")}
            disabled={busy}
            data-testid="billing-download-pdf"
          >
            <Download width={15} height={15} className="mr-1" /> PDF
          </button>
          <button
            type="button"
            className="btn-outline text-sm justify-center"
            onClick={() => download("xml")}
            disabled={busy}
            data-testid="billing-download-xml"
          >
            <Download width={15} height={15} className="mr-1" /> XML
          </button>
        </div>
        {message && <p className="text-xs mt-3">{message}</p>}
      </div>
    );
  }

  return (
    <div className="cvln-card p-5" data-testid="billing-invoice-panel">
      <div className="flex items-center gap-2 font-semibold">
        <Page width={18} height={18} /> Facture Academy
      </div>
      <p className="text-xs text-[--cvln-ink-2] mt-2">
        Le prix et la preuve de paiement viennent de la commande Economy 3D / CVLN Wallet.
      </p>

      {profileLoaded && (
        <div className="grid gap-2 mt-4">
          <input
            className="input"
            name="legal_name"
            placeholder="Nom / raison sociale"
            value={profile.legal_name || ""}
            onChange={updateField}
            data-testid="billing-legal-name"
          />
          <input
            className="input"
            name="address_line1"
            placeholder="Adresse"
            value={profile.address_line1 || ""}
            onChange={updateField}
            data-testid="billing-address"
          />
          <div className="grid grid-cols-2 gap-2">
            <input
              className="input"
              name="postal_code"
              placeholder="Code postal"
              value={profile.postal_code || ""}
              onChange={updateField}
              data-testid="billing-postal-code"
            />
            <input
              className="input"
              name="city"
              placeholder="Ville"
              value={profile.city || ""}
              onChange={updateField}
              data-testid="billing-city"
            />
          </div>
          <input
            className="input"
            name="country"
            placeholder="Pays ISO (FR, MQ…)"
            maxLength={2}
            value={profile.country || ""}
            onChange={updateField}
            data-testid="billing-country"
          />
          <input
            className="input"
            name="vat_id"
            placeholder="N° TVA (optionnel)"
            value={profile.vat_id || ""}
            onChange={updateField}
          />
          <input
            className="input"
            name="registration_id"
            placeholder="Identifiant entreprise (optionnel)"
            value={profile.registration_id || ""}
            onChange={updateField}
          />
        </div>
      )}

      <button
        type="button"
        className="btn-primary w-full mt-4 justify-center"
        onClick={issueInvoice}
        disabled={busy || !profileLoaded}
        data-testid="billing-issue-invoice"
      >
        {busy ? "Validation en cours…" : "Émettre ma facture Factur-X"}
      </button>
      {message && <p className="text-xs mt-3">{message}</p>}
    </div>
  );
}
