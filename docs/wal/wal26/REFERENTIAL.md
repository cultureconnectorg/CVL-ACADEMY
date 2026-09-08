# WAL-26 — Settlement & Reconciliation Operator

```
Prerequisite: WAL-19, WAL-21. UPGRADED 2026-09-06 from BLOCKED_
PRODUCT_DEPENDENCY — see wal22/REFERENTIAL.md's header note, same
discipline.
```

## Repo truth

`djsayd/CVLN-Wallet/backend/server.py` (re-read directly this
session): a real settlement state machine and reconciliation case
system. Settlement: `POST /admin/settlements` (create, admin-only,
idempotent on `transaction_id`), `POST /admin/settlements/{id}/submit`
(transitions `PENDING→SUBMITTED` via `settlement_transition`, calls a
provider abstraction `get_provider(...).submit()`, retry-safe if a
prior submit crashed mid-flight), `GET /admin/settlements` /
`GET /admin/settlements/{id}` (the latter includes full state
history from `db.financial_state_history`). Every transition emits a
correlation-ID-tagged event (`emit_event`, e.g.
`Financial.SettlementCreated`/`SettlementSubmitted`). Reconciliation:
`POST /admin/reconciliation/run` (opens cases), `GET /admin/
reconciliation/cases`, `POST /admin/reconciliation/cases/{id}/resolve`
(resolution ∈ `RESOLVED`/`ACCEPTED_DIFFERENCE`/`ESCALATED`, admin-only,
only from `OPEN`/`INVESTIGATING`). Doc: `docs/CVLN-SETTLEMENT-
RECONCILIATION.md`.

**This is a real capability of the external CVLN Wallet product —
absent entirely from this Academy's own `backend/wallet/`.**

## Prerequisites

WAL-19, WAL-21 (ledger literacy — settlements ultimately reconcile
against real ledger-tracked transactions).

## Objectives

1. Explain the settlement state machine's real transitions and why a
   retry-safe re-submit path exists (a crash between transition and
   provider-reference write must not corrupt state or double-submit).
2. Explain the 3 real reconciliation-case resolutions
   (`RESOLVED`/`ACCEPTED_DIFFERENCE`/`ESCALATED`) and when each is the
   correct call — never invent a 4th resolution.
3. Explain the role of correlation IDs and emitted events in making
   this system auditable end to end.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | Settlement lifecycle literacy | `POST/GET /admin/settlements[...]`, `settlement_transition` | State diagram: PENDING→SUBMITTED→(provider outcome), with the retry-safe re-submit branch |
| M2 | Reconciliation-case literacy | `POST /admin/reconciliation/run`, `GET .../cases`, `POST .../resolve` | Table: the 3 real resolutions and when each applies |
| M3 | Auditability via correlation/events | `emit_event`, correlation IDs, `financial_state_history` | Written note on why this makes settlement state independently reconstructible |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as WAL-19/20/21. Recommended 12-month sensitive
renewal cycle (`ECO-042`), alongside WAL-21/28 — this role handles
real financial reconciliation, even at literacy level.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_WAL26` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Grounded in the repo-truth
already directly verified against `djsayd/CVLN-Wallet` — reused, not
re-audited, per this corpus's own established discipline. Not yet
delivered to a real candidate — `FULLY_COMPLETE` still requires that
verification, per `../QUALITY_GATES.md`.
