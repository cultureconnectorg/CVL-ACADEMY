# CVLN Academy Master — Economic Model 3D (DECIDED V1)

```
SOURCE: CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx (Founder upload,
2026-09-06), 15 sheets, all preserved verbatim in raw/. STATUS:
DECIDED_V1 for 811/812 rows, DECIDED_HOLD for 1 (HOS-GAP, consistent
with the preserved coverage gap already logged in GAP_REGISTER.md).
This is the economic overlay on top of the already-reconciled 812-row
cartography — it prices and packages what RECONCILIATION_MATRIX.md
already classified, it never re-classifies or re-audits repo truth.
```

## Standing rule (carried forward without exception)

`MARKET != SYSTEM_CVLN` ; `CERTIFICATION != AUTHORIZATION` ;
`CVE != Wallet != JCC != Tokenomics` ; `Objets pédagogiques != produits
commerciaux`. The economic model reuses these boundaries verbatim
(`Sources_Methodo.csv`, `Doctrine Academy` row) — it does not
introduce new ones, and nowhere collapses a pedagogical object into a
commercial SKU. A formation's *content* stays governed by
`10_PORTFOLIO/RECONCILIATION_MATRIX.md`; its *price* is governed here.

## The 7 revenue engines (`ECO-001`)

| Engine | Covers | Buyer |
|---|---|---|
| B2C Learning | Free/Access/Pro/Career/Parcours métier/Intensive | Individual |
| Certification | Assessment Only, Certification Academy, Renewal | Learner/professional |
| B2B | Team/Growth/Enterprise seats | Company |
| B2G | Pilot/Territory/Large programs | Institution |
| Learning-to-Work | Mission/project matching | Client/partner (never the candidate) |
| Platform/IP | Methodology licence, Academy+Spatial licence, White-label | School/enterprise/institution |
| Internal Value | Internal CVLN operator qualification | CVLN entities (never sold) |

## Offers registry (`Offres_Economiques.csv`, `Pricing_V1.csv`, `Unit_Economics.csv` — 20 SKUs, all `DECIDED_V1`/`DECIDED_PHASE_2`/`DECIDED_PHASE_3`)

| Offer | Price | Margin | Floor | Gate |
|---|---|---|---|---|
| Free Orientation | €0 | — | — | Public, previews only — no certification, no restricted content |
| Academy Access | €24.90/mo or €249/yr | 82% | 80% | PASS |
| Academy Pro | €69/mo or €690/yr | 80% | 80% | PASS |
| Academy Career | €129/mo or €1,290/yr | 75% | 75% | PASS — no guaranteed mission |
| Parcours métier | €990 (12 months) | 70% | 65% | PASS — certification sold separately |
| Intensive Hybrid Week | €1,400/learner (cohort of 15, €21,000 target) | 86% | 55% | PASS |
| Assessment Only | €250 | 64% | 60% | PASS — no Academy certification granted |
| Certification Academy | €390 | 69% | 60% | PASS — no automatic authorization |
| Renewal | €190 | 68% | 60% | PASS |
| B2B Team | €12,000/yr, ≤10 seats | 65% | 55% | PASS |
| B2B Growth | €39,000/yr, ≤50 seats | 65% | 55% | PASS |
| B2B Enterprise | €69,000/yr, ≤100 seats | 65% | 55% | PASS |
| B2G Pilot | €35,000 / 25 learners | 55% | 45% | PASS |
| B2G Territory | €120,000 / 100 learners | 55% | 45% | PASS |
| B2G Large | €250,000 / 250 learners | 55% | 45% | PASS |
| Learning-to-Work | 12% GMV, min €150, billed to client — candidate fee is always €0 | 80% | 60% | PASS |
| Methodology/IP Licence | €25,000/yr (Phase 2) | 80% | 75% | PASS |
| Academy+Spatial Licence | €60,000/yr (Phase 3) | 80% | 75% | PASS |
| White-label Enterprise | €120,000/yr + €25,000 setup (Phase 3) | 80% | 75% | PASS |
| Internal CVLN Capability | Not commercial | — | — | Never sold; measured by internal KPI (`Valeur_Interne.csv`) |

**All 19 priced offers clear their own margin floor — `Offres sous marge plancher = 0`** (`Dashboard.csv`). No offer has been priced below its executive gate.

## Per-object economic mapping (`Mapping_812.csv` — 812 rows, preserved verbatim, never restated here)

Every one of the 812 already-reconciled Master 2D rows carries an
economic classification that follows its own `Dimension`/`Contexte`
mechanically, **not** a fresh judgment call per row:

| Dimension (from `RECONCILIATION_MATRIX.md`) | Rows | `Moteur primaire` | `Packaging V1` | `Prix public V1` | `Activation gate` |
|---|---|---|---|---|---|
| `External_Market` | 437 | B2C Learning | `INCLUDED_PRO + ELIGIBLE_PATH` | €990 path / subscription | `CANONICALIZED` |
| `Internal_CVLN` (incl. restricted/privileged) | 220 | Internal Value | `INTERNAL_QUALIFICATION` | `NOT_FOR_SALE` | `PRODUCT_VERIFIED + ROLE_DEFINED` |
| `Cross_Ecosystem` | 153 | B2B Workforce/Learning-to-Work | `CROSS_CVLN_PROGRAM` | B2B/B2G/Enterprise bundle | `VERTICALS_CANONICALIZED + HANDOFF_VERIFIED` |
| `BRIDGE` (`SAY-LAB`) | 1 | Learning-to-Work | `BUNDLED_BRIDGE` | €0 standalone (bundled only) | `CANONICALIZED + ELIGIBILITY_RULES` |
| `GAP` (`HOS-GAP`) | 1 | — | `HOLD_FROM_SALE` | `NOT_FOR_SALE` | `RECONCILIATION_REQUIRED` |

**This is the single most important fact for sequencing W6:** every
gate above requires the object to already be built and verified
(`CANONICALIZED`, `PRODUCT_VERIFIED`, `HANDOFF_VERIFIED`) before it can
be sold at all. Since every one of the 812 rows is currently
`RECONCILED_NOT_BUILT` (`00_GOVERNANCE/QUALITY_GATES.md`), **0/812
objects are commercially activatable today** — this is not a
limitation of the economic model, it is the model's own discipline,
identical in spirit to this Master Package's own
`NO_FAKE_PROOF`/`UNPROVEN_FEATURE=0` gates. Pricing "goes live" for an
object exactly when its W6 wave completes and its gate is verified,
never before.

## Policies (`Policies.csv`)

- Free access = orientation/previews only — never certification, guaranteed mission, or internal content.
- Split payment: 3x no-fee from €300; no 6x in V1.
- Annual discount: 16.7%, already priced into annual tiers.
- Scholarships: 10% of cohort seats (sponsor/B2G/impact budget).
- Partner commission: 15% max, on attributable, traceable revenue only.
- Content/R&D reinvestment: 10% of Academy revenue.
- `BRIDGE` objects: never sold standalone — bundled into Career/B2B/B2G/sponsor only.
- `Cross-CVLN`: no B2C micro-courses — B2B/B2G/Enterprise/internal only.
- Internal-restricted: never for sale — access by role/governance only.
- Mission fee: candidate always €0; client 12% GMV, min €150; no permanent-placement fee in V1.
- Operator qualification: standard 24 months, sensitive (cyber/finance/privileged) 12 months.
- Executive authority: never granted by the Academy — governance mandate only.
- CVE/JCC/Wallet: separated from public pricing — EUR is the only pricing unit; **this is the same boundary just closed by `FD-CVE-001`** (`20_EXTERNAL/WALLET_CVE_RECONCILIATION.md`) — CVE's `FORMALIZED_METHODOLOGY` status measures cultural value, it never becomes a price.
- Regulated claims (RNCP/CPF/financing): require verified proof before any public claim — never asserted without a named source, same discipline as this Master Package's `UNPROVEN_FEATURE` gate.

## Monetization roadmap (`Roadmap_Monetisation.csv`)

| Phase | Timing | Engines activated | Entry condition |
|---|---|---|---|
| Phase 1 — Launch | 0-6 months | Free, Access, Pro, Career, Path, Intensive, Assessment, Certification, B2B Team/Growth, B2G Pilot/Territory | Priority canonical packages + checkout + assessment |
| Phase 2 — Scale | 6-18 months | B2B Enterprise, B2G Large, Methodology/IP, Learning-to-Work at volume | Proven demand + mission ops + portfolio |
| Phase 3 — Platform | 18-36 months | Academy+Spatial licence, White-label | Stabilized product + licensing controls |
| Internal — continuous | Now | Internal CVLN qualification | Roles/gates defined |

36-month base plan (`Plan_36M.csv`): Y1 CA €2,144,800 → Y2 €4,600,400
→ Y3 €7,739,040 (`Dashboard.csv`) — a planning hypothesis, not a
commitment; contingent on the same activation gates above.

## Internal value (`Valeur_Interne.csv`) — never counted as revenue

Seven KPI levers measure Internal_CVLN qualification value without
ever becoming a price: onboarding time-to-autonomy (-30% target),
incident rate (-25%), supervision hours (-20%), critical-procedure
documentation (90%), field-mission validation rate (85%), traced
critical-incident coverage (100%), internal role-mobility (10% of
qualified population). All explicitly `NON-CA` (not revenue).

## Learning-to-Work economics (`Learning_to_Work.csv`)

The full chain — Apprentissage → Assessment → Certification →
Qualification → Opportunity → Mission → Expérience → Portfolio — is
priced stage by stage: learning/assessment/certification are
commercialized (per the offers above); qualification and opportunity
matching are **included, never separately charged to the candidate**;
the mission itself is billed to the client/partner (12% GMV, min €150)
and the field experience/portfolio are included in Career/B2B. This
is the same chain already documented as the "Learning-to-Opportunity"
pipeline in `60_CROSS_ECOSYSTEM/CROSS_ECOSYSTEM_MAP.md` and its stage
breakdown in `XCV_TRANSVERSAL_RECONCILIATION.md` (XCV-27→34) — the
economic layer prices that exact pipeline, it does not invent a
parallel one.

## Sources (`Sources_Methodo.csv`)

Cartography (812 objects/contexts) + this Founder economic decision
(2026-09-06) + the prior Academy working model (real baseline:
€1,400/intensive week, 15 learners, 15% commission, 10%
reinvestment, €3,000 direct cohort cost) + standing Academy doctrine
+ the legal/compliance gate (offers/prices decided; regulated claims
activate only with proof).

## Status

`STATUS = DECIDED_V1` for the economic doctrine itself (pricing,
packaging, engines, margins, policies — the Founder's decision,
applied verbatim). `STATUS = RECONCILED_NOT_BUILT` still holds for
every one of the 812 pedagogical objects the pricing attaches to —
**this document changes what an object will cost once built, never
what has been built.** No runtime pricing table, Stripe product,
checkout flow, or entitlement gate is created or modified by this
document — that implementation follows per-object, gated on
`CANONICALIZED`/`PRODUCT_VERIFIED`/`HANDOFF_VERIFIED`, as each W6 wave
completes.
