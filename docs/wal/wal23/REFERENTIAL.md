# WAL-23 — CVLN Payment & Transfer Operations

```
Prerequisite: WAL-19. UPGRADED 2026-09-06 from BLOCKED_PRODUCT_
DEPENDENCY — see wal22/REFERENTIAL.md's header note, same discipline.
```

## Repo truth

`djsayd/CVLN-Wallet/backend/server.py` (re-read directly this
session): `POST /v1/entity/transfer` — a real entity-to-user or
entity-to-entity transfer. Recipient resolved by FREK-ID (looked up in
`db.users`) or raw `entity_id` (looked up in `db.entities`); the
sender's entity balance is debited atomically (`atomic_entity_spend`,
no over-spend possible); the transfer is posted as a balanced ledger
entry (`ledger_post`) between the entity account and the destination
account, and logged on both sides (`log_entity_tx`).

**This is a real capability of the external CVLN Wallet product —
absent entirely from this Academy's own `backend/wallet/`** (which has
no transfer function of any kind, only single-account `credit()`).

## Prerequisites

WAL-19.

## Objectives

1. Explain the transfer flow exactly: amount validation, recipient
   resolution (FREK-ID vs. `entity_id`), atomic debit, and the
   balanced ledger entry posted on completion.
2. Explain why the debit uses `atomic_entity_spend` rather than a plain
   decrement — the real code guards against over-spend at the database
   level, not just in application logic.
3. Never claim this Academy's own `backend/wallet/` supports transfers
   — it does not; this formation teaches the real external product's
   mechanism, never an Academy runtime capability.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | Transfer flow literacy | `POST /v1/entity/transfer` | Sequence diagram: validate → resolve recipient → atomic debit → ledger post → dual logging |
| M2 | Atomic-debit discipline | `atomic_entity_spend` | Written note on why atomicity matters for a transfer specifically (two parties, real money) |
| M3 | Boundary discipline | Absence of any transfer function in `backend/wallet/service.py`'s `credit()` | Explicit note: real product capability, no Academy runtime access |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as WAL-19/20/21. Mission eligibility: none.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_WAL23` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Grounded in the repo-truth
already directly verified against `djsayd/CVLN-Wallet` — reused, not
re-audited, per this corpus's own established discipline. Not yet
delivered to a real candidate — `FULLY_COMPLETE` still requires that
verification, per `../QUALITY_GATES.md`.
