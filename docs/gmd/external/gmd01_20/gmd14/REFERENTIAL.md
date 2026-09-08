# GMD-14 — Finance (Live-Events/Festival Industry)

```
Flagship of the GMD-01→20 external market-general pathway (task
#184). Prerequisite: none (entry-level industry role).
```

## Grounding

Real market-standard discipline: event/festival finance operations
(payment processing, revenue reconciliation, order/refund handling).
**Worked example** cited by reference, never re-derived:
`docs/gmd/gmd28/REFERENTIAL.md` — "the best-grounded payment
precedent in the entire CVLN ecosystem audited this session" (real
`POST /payments/checkout`, `GET /payments/status/{session_id}`,
`POST /stripe/webhook`, `GET /admin/orders`). This formation never
claims the real `gmfest972/goodmooddjsayd` platform implements the
full scope of event finance (multi-currency settlement, sponsor
invoicing, tax handling) beyond what GMD-28's repo-truth documents —
those remain taught as market-general knowledge, explicitly labeled.

## Prerequisites

None.

## Objectives

1. Trace a real payment end to end, citing GMD-28's worked example:
   checkout session creation → Stripe → webhook confirmation → order
   record — never re-deriving the sequence, only citing it.
2. Explain why the webhook-based confirmation pattern exists (payment
   confirmation must not depend on the buyer's browser staying open)
   and diagnose a "payment succeeded but order missing" report by
   checking webhook delivery/processing evidence, never by guessing.
3. Distinguish what GMD-28's real integration covers (single-currency
   Stripe checkout/webhook/order reconciliation) from broader event-
   finance practices it does not implement (multi-currency
   settlement, sponsor invoicing, tax handling) — teach the latter as
   market-general knowledge, explicitly labeled
   `NOT_A_PLATFORM_CAPABILITY`.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | Checkout-to-order sequence | GMD-28 (worked example) | Sequence diagram, cited not re-derived |
| M2 | Webhook literacy & failure diagnostics | GMD-28's real webhook/order-reconciliation pattern | Runbook: diagnose "payment succeeded, order missing" |
| M3 | Order reconciliation | `GET /admin/orders` (cited) | Reconciliation checklist |
| M4 | Market-general finance practices beyond the platform | Industry-standard (multi-currency, sponsor invoicing, tax) | Written note, explicitly labeled `NOT_A_PLATFORM_CAPABILITY` |

## Assessment

Per `../../CERTIFICATION_MODEL.md`. N2 includes a failure-mode case
(webhook delivery failure) with an eliminatory rule for guessing at a
cause instead of checking real evidence (webhook logs, Stripe
dashboard), matching GMD-28's own assessment discipline.

## Evidence / certification / mission eligibility

Evidence = M1 sequence diagram + M2 runbook + M4 boundary note, all
checkable against GMD-28's cited repo-truth and standard event-
finance practice. Certification eligibility: pass Assessment at N2+.
Mission eligibility: none — this Academy operates no real event-
finance role.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD14` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Chosen as one of 3 flagships
for the GMD-01→20 external cluster (task #184) — the other rows stay
at `MODULE_CONTENT_DRAFTED` per `../REFERENTIAL.md`. Not yet
delivered to a real candidate — `FULLY_COMPLETE` still requires that
verification, per `../../QUALITY_GATES.md`.
