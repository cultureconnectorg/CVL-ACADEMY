# Billing / invoicing engineering research — 2026-09-11

Status: **ENGINEERING INPUT — not a legal or accounting assertion**.

Doctrine: Current != Target · Evidence First · Human Authority.

## Sources inspected

| Project | Useful capability | License / boundary | CVLN decision |
|---|---|---|---|
| `getlago/lago` | API-first billing, usage events, hybrid subscription/usage, credits, entitlements, invoices, payments | AGPL-3.0 | **Architecture reference only**. Do not copy AGPL implementation into Academy. Adopt the separation `usage → pricing → entitlement → invoice → payment/revenue` where it fits CVLN. |
| `getlago/lago-billing-examples` | idempotent event identifiers, PAYG/per-transaction/hybrid examples | MIT examples | Reuse concepts: stable external IDs and immutable event/price snapshots. |
| `killbill/killbill` | mature modular billing/payment platform, one-off + recurring + usage, replaceable modules | Apache-2.0 | Architecture reference: keep billing separate from payment provider; explicit state machines; do not make CVLN Wallet the invoice ledger. |
| `meteroid-oss/meteroid` | pricing/billing infrastructure, subscriptions, invoicing, usage billing, grandfathering, revenue analytics | AGPL-3.0 | Architecture reference only. Adopt versioned pricing / grandfathering concept; no source copy. |
| `invoiceninja/invoiceninja` | invoices, quotes, client-facing documents, self-hosted workflows | source-available | Product/UX reference only; no code copy. |
| `akretion/factur-x` | Python generation/validation of Factur-X, UBL and EN16931 structures | BSD | **Candidate dependency** for a later compliant e-invoice adapter. It matches Academy's Python backend and can validate XSD/Schematron. Do not issue a legal invoice until issuer/tax/e-invoicing profile is configured and validated. |

## CVLN target architecture

```text
Economy 3D (commercial truth)
        ↓
Offer / price version
        ↓
Commercial order (immutable price snapshot)
        ↓
Payment attempt ─────→ CVLN Wallet (value movement)
        ↓ confirmed
Entitlement           Billing document intent
        ↓                       ↓
Learning access       Invoice/Credit Note state machine
                                ↓
                    Factur-X / UBL adapter (when configured)
                                ↓
                    Delivery / accounting / institution connector
```

### Non-negotiable invariants

1. Browser never supplies authoritative price, tax, invoice total or invoice number.
2. Payment and invoice are separate bounded contexts. A Wallet transaction is evidence of payment; it is not itself an invoice.
3. Every billable document is tied to an immutable order/pricing snapshot and payment attempt/reference.
4. Invoice issuance is idempotent per commercial order.
5. Issued documents are append-only. Corrections create a credit note / replacement relationship; they do not mutate history.
6. Invoice numbering must be generated server-side from an explicit issuer series. No random UUID is the legal invoice number.
7. Tax/VAT treatment, issuer legal identity, customer legal identity and e-invoicing route are fail-closed until configured. Academy must not invent them.
8. B2C, B2B, B2G/institutional and internal flows share the same billing primitives but can have different validation/delivery adapters.
9. `FREK-ID`, Economy requirement ID, order ID, Wallet payment reference and invoice ID remain cross-linked for audit/proof.
10. Source systems remain explicit: Economy 3D = commercial truth; CVLN Wallet = value movement; billing core = document/accounting lifecycle.

## What is implemented by this branch

- billing document state machine and immutable invoice intent model;
- deterministic idempotency key per order/document type;
- fail-closed issuer/tax readiness gate;
- exact linkage to Economy 3D order snapshot + Wallet payment evidence;
- API to inspect invoice intent for a paid order;
- tests proving duplicate issuance intent does not create two documents.

## Explicitly not claimed yet

- legal/tax compliance for a specific CVLN legal entity;
- production Factur-X issuance;
- PDP/Peppol/Chorus Pro delivery;
- VAT determination;
- accounting export;
- subscription billing execution;
- B2B/B2G quote acceptance.

Those require explicit issuer identity, tax rules, deployment choices and (where applicable) contractual/provider configuration.