# WAL-19 — Banque N1 (formative, M1→M4)

```
Sourced directly against backend/wallet/models.py, service.py,
backend/api/wallet.py (all read in full this session).
```

## M1 — system map

1. Name the three real Pydantic models in `wallet/models.py`.
   (`WalletTransaction`, `WalletAccount`, `WalletSummary`)
2. What does `_get_or_create_account()` do if no account exists yet
   for a `user_id`? (Creates a new `WalletAccount` with zeroed
   balances and inserts it — never raises an error for a first-time
   user)
3. Name the 4 real API routes and what each returns.
   (`GET /wallet/me` → `WalletSummary`; `GET /wallet/transactions` →
   list of `WalletTransaction`; `GET /wallet/pass/apple` and
   `GET /wallet/pass/google` → unsigned pass payloads)
4. Is there a route to credit a wallet directly, callable by an
   end user? (No — `credit()` is a service function called by other
   backend code, e.g. on badge/certification events; there is no
   public API route that lets a user credit their own wallet)

## M2 — data model literacy

5. Name the 5 real `TransactionType` values.
   (`badge_earned`, `jcc_earned`, `token_earned`, `reward_redeemed`,
   `payment`)
6. Name the 3 real `Currency` values. (`jcc`, `token`, `eur`)
7. Is `amount` ever negative in the schema? (The model itself allows
   any `float`; the code's own convention is that `credit()` is called
   with a positive amount, and a "spend" is represented by the caller
   passing a negative amount for `reward_redeemed` — this is a
   convention, not a distinct debit function)
8. Does `WalletTransaction` support a hold/reservation state? (No —
   no such field or status exists; every transaction is final the
   moment it's inserted)

## M3 — CC vs. JCC boundary

9. Quote (paraphrase acceptable, but the meaning must be exact) why
   `jcc_balance` is kept separate from `cc_credits`. (CC credits are
   this Academy's own pedagogical progression currency; the Wallet's
   JCC is the cross-CVLN-ecosystem ledger — two different purposes,
   never merged)
10. Where does `cc_credits` live, and where does `jcc_balance` live?
    (`models.User.cc_credits` vs. `wallet.models.WalletAccount.
    jcc_balance` — two different models entirely)

## M4 — Academy Wallet vs. real external product

11. Name at least 3 real capabilities `djsayd/CVLN-Wallet` (the
    external product) has that this Academy's own ledger does not.
    (Any 3 of: holds/authorization/capture, maker-checker, idempotency
    keys + kill-switch, monetary precision handling, outbox/inbox
    delivery, refunds/reversals/fees, settlement/reconciliation,
    virtual card audit/security)
12. Is there any observed integration between this Academy's ledger and
    the real external product? (No — none observed; they are cited
    together only for context, never as one connected system)
