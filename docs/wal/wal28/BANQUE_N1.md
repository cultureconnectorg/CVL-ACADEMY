# WAL-28 — Banque N1 (formative, M1→M3)

```
Sourced directly against backend/wallet/service.py (re-read in full
this session).
```

## M1 — transaction history retrieval

1. What does `list_transactions()` sort by, and in what order?
   (`created_at`, descending — most recent first)
2. What is the default cap on the number of transactions returned?
   (`limit=200`)
3. What real API route exposes this function? (`GET /wallet/
   transactions`)

## M2 — audit-strength honesty

4. Does `WalletTransaction` use cryptographic signing or a hash chain?
   (No — neither exists in the real schema)
5. What real guarantee DOES the append-only design provide, without
   any cryptographic depth? (No code path can update or delete a
   transaction after insertion — a genuinely inspectable surface, but
   not tamper-evident in the cryptographic sense)
6. Is it accurate to call this ledger "tamper-evident"? (No — that term
   implies cryptographic proof of non-alteration, which doesn't exist
   here; "append-only" and "tamper-evident" are not the same claim)

## M3 — balance cross-check

7. What two things does a balance cross-check compare? (The cached
   `WalletAccount.jcc_balance`/`token_balance` against the real sum of
   that user's transactions in `wallet_transactions`)
8. What real function already performs exactly this recomputation, and
   when is it used? (`reconcile_wallet_balance()`, WAL-21 — used when a
   crash between the ledger insert and the cache update is suspected)
