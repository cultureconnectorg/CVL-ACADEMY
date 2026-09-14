# WAL-28 — Wallet Audit & Evidence Operations

```
Prerequisite: WAL-19, WAL-21.
```

## Repo truth

`list_transactions()` (`wallet/service.py`) — reads
`db.wallet_transactions` sorted by `created_at` descending, capped at
`limit=200` by default; the append-only nature of `WalletTransaction`
(no update/delete function) makes this a genuinely inspectable audit
surface, even without cryptographic depth (no signing, no hash chain
— never claim otherwise). Same pattern already established for
FRK-68 (Auditor) in `FREK_01_75_RECONCILIATION.md` — reuse that
boundary language rather than re-deriving it.

## Prerequisites

WAL-19, WAL-21.

## Objectives

1. Retrieve and interpret a user's real transaction history via
   `list_transactions()`/`GET /wallet/transactions`.
2. Explain why append-only storage alone (no cryptographic signing or
   hash chaining) provides a real but limited audit guarantee —
   never overstate it as tamper-evident.
3. Cross-check a `WalletAccount`'s cached balance against the sum of
   its real transactions, to verify the two are consistent.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | Transaction history retrieval | `list_transactions()`, `GET /wallet/transactions` | Runbook: retrieve, sort, verify against a known set of `credit()` calls |
| M2 | Audit-strength honesty | Absence of any signing/hash-chain mechanism | Written note: what append-only alone guarantees vs. what cryptographic proof would add (never invented) |
| M3 | Balance cross-check | `WalletAccount.jcc_balance`/`token_balance` vs. sum of transactions | Executed reconciliation on a real or sandboxed account |

## Assessment

Per `../CERTIFICATION_MODEL.md`. Assessment artifact: M3 reconciliation
executed and verified.

## Evidence / certification / mission eligibility

Same general pattern as WAL-19. Recommended 12-month sensitive
renewal cycle (`ECO-042`), alongside WAL-21.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_WAL28` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Not yet delivered to a real
candidate — `FULLY_COMPLETE` still requires that verification, per
`../QUALITY_GATES.md`.
