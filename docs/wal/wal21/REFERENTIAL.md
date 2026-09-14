# WAL-21 — CVLN Ledger Operator

```
Prerequisite: WAL-19.
```

## Repo truth

`credit()` (`wallet/service.py`) — checks for an existing transaction
matching `(user_id, economic_event_id)` first (idempotency pre-check);
if none exists, inserts a `WalletTransaction`, catching
`DuplicateKeyError` from the real unique index (`infra_indexes.py`) as
a second, concurrency-safe idempotency layer; then updates the cached
`WalletAccount` balance via `$inc` (for `jcc`/`token` currencies) and
optionally `$addToSet` on `badges` if a `badge_code` is passed.
Append-only: no update or delete function exists for a
`WalletTransaction` once inserted. `reconcile_wallet_balance()` is the
real repair path for the one documented gap this ordering leaves open
(a crash between the ledger insert and the cache update) — it
recomputes `jcc_balance`/`token_balance` directly from
`wallet_transactions` via a real Mongo aggregation and overwrites the
cache.

## Prerequisites

WAL-19.

## Objectives

1. Explain the two-write pattern `credit()` performs (insert
   transaction, then update cached account balance) and why both steps
   exist rather than computing the balance from transactions on every
   read.
2. Explain the real idempotency mechanism: the `economic_event_id`
   pre-check plus the `DuplicateKeyError` catch on the real unique
   index — and why both are needed (the pre-check alone has a race
   window under real concurrency; the unique index closes it).
3. Recognize that `WalletTransaction` is genuinely append-only — no
   real code path modifies or deletes a transaction after creation.
4. Explain `reconcile_wallet_balance()`'s real repair path and when it
   is needed (a crash between the ledger insert and the cache update —
   never a routine operation).
5. Explain the real single-entry nature of this ledger (WAL-03's
   market-standard double-entry accounting is NOT what this ledger
   implements — never claim otherwise).

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | `credit()` walkthrough | `wallet/service.py` | Sequence diagram: pre-check → insert transaction (`DuplicateKeyError` caught) → `_get_or_create_account` → `$inc`/`$addToSet` update |
| M2 | Idempotency mechanism | `economic_event_id` unique index (`infra_indexes.py`), `DuplicateKeyError` catch | Written note: the two-layer guarantee (pre-check + index), and the real, honestly-scoped limit (not a multi-document ACID transaction — no replica-set MongoDB in this sandbox) |
| M3 | Append-only discipline | Absence of any update/delete function on `WalletTransaction` | Written note on why append-only ledgers matter for auditability (cross-reference WAL-28) |
| M4 | Reconciliation repair path | `reconcile_wallet_balance()`, real Mongo `$group`/`$sum` aggregation | Written note: what triggers a real drift (crash between insert and cache update), and how reconciliation fixes it without ever mutating the ledger itself |
| M5 | Single-entry vs. double-entry boundary | Real code has no debit/credit pair, no journal entry concept | Honest comparison note, citing WAL-03's market content without implying this ledger meets that standard |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as WAL-19. Recommended 12-month sensitive
renewal cycle (`ECO-042`), per `../CERTIFICATION_MODEL.md`.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_WAL21` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Not yet delivered to a real
candidate — `FULLY_COMPLETE` still requires that verification, per
`../QUALITY_GATES.md`.
