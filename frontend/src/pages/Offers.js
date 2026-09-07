import { useEffect, useState } from "react";
import { CreditCard, CheckCircle } from "iconoir-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useI18n } from "@/lib/i18n.jsx";

/* ACA-0025/ACA-0026 (Founder decisions, DECIDED_V1 2026-09-06 /
 * W-FUNNEL-2 "Conversion" 2026-09-07) — `GET /commerce/offers` has
 * been real, public and fully tested (backend/commerce/*,
 * api/commerce.py, tests/test_commerce_catalog.py) since ACA-0025, but
 * had no frontend surface at all. This page renders that real
 * catalogue as-is: no page here invents a price, a discount, or an
 * offer the backend doesn't already carry.
 *
 * Hard rule this page enforces (see commerce/models.py's own
 * docstring — NO_FAKE_PAID_STATE): ACA-0026 (a real checkout, webhook,
 * reconciliation runtime) stays explicitly BLOCKED_EXTERNAL pending a
 * real payment provider. So every offer's CTA here does exactly one
 * thing — say that honestly — never a fake "purchased"/"subscribed"
 * state, never a silent no-op. No `paid`/`subscribed` flag is read or
 * written anywhere in this component.
 */
export default function Offers() {
  const { t } = useI18n();
  const [offers, setOffers] = useState(null);

  useEffect(() => {
    api.get("/commerce/offers")
      .then((r) => setOffers(r.data))
      .catch(() => setOffers([]));
  }, []);

  const notifyPaymentNotActive = () => {
    toast.info(t("offers_p.payment_not_active"));
  };

  if (offers === null) {
    return <div className="p-10 text-[--cvln-ink-2]">…</div>;
  }

  // Group offers by their real commercial engine (Acquisition, B2C
  // Learning, B2C Career, Certification, Cohorte, B2B, B2G, Mission
  // Economy, Platform/IP, Internal Value) — the catalogue's own real
  // taxonomy, preserving the backend's original ordering.
  const groups = [];
  for (const o of offers) {
    let g = groups.find((x) => x.engine === o.engine);
    if (!g) {
      g = { engine: o.engine, offers: [] };
      groups.push(g);
    }
    g.offers.push(o);
  }

  return (
    <div className="px-6 md:px-12 py-10 max-w-7xl" data-testid="offers-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">
        {t("offers_p.eyebrow")}
      </div>
      <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-3">
        {t("offers_p.title")}
      </h1>
      <p className="text-[--cvln-ink-2] mt-4 max-w-2xl">{t("offers_p.subtitle")}</p>

      {groups.length === 0 && (
        <div className="mt-10 text-[--cvln-ink-2]" data-testid="offers-empty">
          {t("offers_p.empty")}
        </div>
      )}

      {groups.map((g) => (
        <div key={g.engine} className="mt-12">
          <h2 className="font-display font-bold text-xl md:text-2xl tracking-tight">{g.engine}</h2>
          <div className="mt-5 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {g.offers.map((o) => (
              <div
                key={o.offer_id}
                data-testid={`offer-${o.offer_id}`}
                className="cvln-card p-6 flex flex-col"
              >
                <div className="text-[10px] mono uppercase tracking-wider text-[--cvln-ink-2]">
                  {o.buyer}
                </div>
                <div className="font-display font-bold text-xl mt-1">{o.label}</div>
                <div className="text-sm text-[--cvln-ink-2] mt-2 flex-1">{o.object_sold}</div>

                <div className="mt-5 flex items-end gap-2 flex-wrap">
                  <div className="font-display font-black text-3xl tracking-tighter">
                    {o.price_eur > 0
                      ? `${o.price_eur.toLocaleString()} €`
                      : t("offers_p.free")}
                  </div>
                  {o.price_eur > 0 && (
                    <div className="text-xs text-[--cvln-ink-2] mb-1.5">{o.pricing_unit}</div>
                  )}
                </div>
                {o.price_eur_annual != null && (
                  <div className="text-xs text-[--cvln-ink-2] mt-1">
                    {o.price_eur_annual.toLocaleString()} € {t("offers_p.per_year")}
                  </div>
                )}
                {o.notes && (
                  <div className="text-xs text-[--cvln-ink-2] mt-3 leading-relaxed">{o.notes}</div>
                )}

                <button
                  data-testid={`offer-cta-${o.offer_id}`}
                  onClick={notifyPaymentNotActive}
                  className="btn-primary mt-5 w-full justify-center"
                >
                  {o.price_eur > 0 ? (
                    <>
                      <CreditCard width={16} height={16} className="mr-2" />
                      {t("offers_p.cta_choose")}
                    </>
                  ) : (
                    <>
                      <CheckCircle width={16} height={16} className="mr-2" />
                      {t("offers_p.cta_start")}
                    </>
                  )}
                </button>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
