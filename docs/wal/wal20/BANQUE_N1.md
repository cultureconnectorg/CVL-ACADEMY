# WAL-20 — Banque N1 (formative, M1→M3)

```
Sourced directly against backend/wallet/models.py, service.py (both
read in full this session).
```

## M1 — currency taxonomy literacy

1. Name the 3 real `Currency` literal values on `WalletTransaction`.
   (`jcc`, `token`, `eur`)
2. Where does the Academy's own pedagogical progression currency live,
   and is it part of `wallet/models.py`? (`models.User.cc_credits` — a
   separate model entirely, not part of `wallet/`)
3. Which field does `credit(currency="jcc")` increment on
   `WalletAccount`? (`jcc_balance`)
4. Which field does `credit(currency="token")` increment?
   (`token_balance`)
5. Which field does `credit(currency="eur")` increment? (None — read
   `service.py`'s own `if/elif` block: only `jcc`/`token` have a branch
   that adds to `inc`; an `eur` transaction is still recorded, but no
   `WalletAccount` balance field is ever incremented for it)

## M2 — non-conversion discipline

6. Does any function in `service.py` convert a JCC amount into CC
   credits, or vice versa? (No — no such function exists anywhere in
   `wallet/`)
7. A colleague says "CC and JCC are basically the same currency,
   just tracked in two places." Is this accurate? (No — they are two
   currencies with different purposes and different owning models,
   never one currency tracked twice; treating them as interchangeable
   is a real modeling error, not a simplification)

## M3 — cross-reference to WAL-21

8. What does WAL-20 teach that WAL-21 does not, and vice versa?
   (WAL-20 = classifying a transaction correctly by currency/model;
   WAL-21 = the ledger mechanics of `credit()` itself — the two are
   prerequisite-linked, not interchangeable)
