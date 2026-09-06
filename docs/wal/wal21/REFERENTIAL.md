# WAL-21 — CVLN Ledger Operator

```
Prerequisite: WAL-19.
```

## Repo truth

`credit()` (`wallet/service.py`) — inserts a `WalletTransaction`, then
updates the cached `WalletAccount` balance via `$inc` (for `jcc`/
`token` currencies) and optionally `$addToSet` on `badges` if a
`badge_code` is passed. Append-only: no update or delete function
exists for a `WalletTransaction` once inserted.

## Prerequisites

WAL-19.

## Objectives

1. Explain the two-write pattern `credit()` performs (insert
   transaction, then update cached account balance) and why both steps
   exist rather than computing the balance from transactions on every
   read.
2. Recognize that `WalletTransaction` is genuinely append-only — no
   real code path modifies or deletes a transaction after creation.
3. Explain the real single-entry nature of this ledger (WAL-03's
   market-standard double-entry accounting is NOT what this ledger
   implements — never claim otherwise).

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | `credit()` walkthrough | `wallet/service.py` | Sequence diagram: insert transaction → `_get_or_create_account` → `$inc`/`$addToSet` update |
| M2 | Append-only discipline | Absence of any update/delete function on `WalletTransaction` | Written note on why append-only ledgers matter for auditability (cross-reference WAL-28) |
| M3 | Single-entry vs. double-entry boundary | Real code has no debit/credit pair, no journal entry concept | Honest comparison note, citing WAL-03's market content without implying this ledger meets that standard |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as WAL-19. Recommended 12-month sensitive
renewal cycle (`ECO-042`), per `../CERTIFICATION_MODEL.md`.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.
