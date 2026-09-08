# WAL-21 — Banque N1 (formative, M1→M5)

```
Sourced directly against backend/wallet/service.py (re-read in full
this session, including credit()'s docstring and reconcile_wallet_
balance()).
```

## M1 — `credit()` walkthrough

1. What is the first thing `credit()` does before inserting anything?
   (Checks for an existing transaction matching `(user_id,
   economic_event_id)` — the idempotency pre-check)
2. If that pre-check finds an existing transaction, what does
   `credit()` return? (The original transaction — never a new one,
   never an error)
3. After a successful insert, what two things does `credit()` update on
   `WalletAccount`? (The `jcc_balance`/`token_balance` via `$inc`, and
   optionally `badges` via `$addToSet` if a `badge_code` was passed)

## M2 — idempotency mechanism

4. What real exception does `credit()` catch around the insert, and
   from what? (`DuplicateKeyError`, from the real unique index on
   `(user_id, economic_event_id)` defined in `infra_indexes.py`)
5. Why does `credit()` need both the pre-check AND the unique index,
   if either alone would catch a duplicate call? (The pre-check alone
   has a race window under real concurrency — two calls could both
   pass the pre-check before either inserts; the unique index closes
   that window at the database level)
6. Does this idempotency mechanism amount to a multi-document ACID
   transaction? (No — the docstring is explicit: this sandbox has no
   replica-set MongoDB to build or test one against; the real,
   honestly-scoped guarantee is an idempotent, append-only ledger plus
   a tested repair path for its derived cache, never a stronger claim)

## M3 — append-only discipline

7. Does any function in `wallet/service.py` update or delete a
   `WalletTransaction` after it's inserted? (No — none exists)

## M4 — reconciliation repair path

8. What specific failure does `reconcile_wallet_balance()` repair?
   (A crash between the ledger insert and the cached-balance update in
   `credit()` — never a routine operation)
9. Does `reconcile_wallet_balance()` ever modify `wallet_transactions`
   itself? (No — it only recomputes and overwrites the cached
   `jcc_balance`/`token_balance` on `WalletAccount`, via a real Mongo
   `$group`/`$sum` aggregation over the ledger)

## M5 — single-entry vs. double-entry boundary

10. Does this ledger implement double-entry accounting (a debit/credit
    pair per transaction)? (No — there is no journal-entry concept in
    the real schema; each `WalletTransaction` is a single amount/
    currency/type record)
