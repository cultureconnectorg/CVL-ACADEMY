# WAL-25 — Banque N1 (formative, M1→M3)

```
Sourced from the repo-truth already directly verified against
djsayd/CVLN-Wallet/backend/server.py — reused here, not re-audited.
```

## M1 — catalog literacy

1. How many real items does `MARKETPLACE_ITEMS` contain, and is it a
   dynamic listing system? (8 items — a static, seeded list, not a
   dynamic listing system where sellers add their own items)
2. Name 3 real fields on a marketplace item. (Any 3 of: `item_id`,
   `title`, `seller`, `price_cc`, `category`, `tag`)
3. Name 3 real named sellers appearing in the seeded catalog. (Any 3 of:
   FREKCORE, Factory Maker Studio/Academy, Culture Connect, Laurentia,
   Kiltikonet, KORA, CVLN OS)

## M2 — idempotent buy-flow literacy

4. What real route executes a purchase? (`POST /marketplace/buy`)
5. What two functions guarantee that a repeated call with the same
   idempotency key never double-charges? (`idem_begin`/`idem_finish`)
6. What function debits the buyer's available balance during a
   purchase? (`atomic_spend`)
7. What real record is created on a completed purchase? (A transaction
   record, via `add_transaction`)

## M3 — boundary discipline

8. Does this Academy's own `backend/wallet/` have any marketplace
   concept? (No — none exists; this is a real capability of the
   external `djsayd/CVLN-Wallet` product only)
9. Can a candidate invent a seller or item not in the real seeded
   catalog and present it as real? (No — the 8 items and their real
   sellers are the only ones that exist; inventing a 9th item or a
   seller not in that list is a fabrication)
