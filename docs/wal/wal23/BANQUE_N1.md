# WAL-23 — Banque N1 (formative, M1→M3)

```
Sourced from the repo-truth already directly verified against
djsayd/CVLN-Wallet/backend/server.py — reused here, not re-audited.
```

## M1 — transfer flow literacy

1. What real route performs an entity-to-user or entity-to-entity
   transfer? (`POST /v1/entity/transfer`)
2. Name the two ways a recipient can be resolved. (By FREK-ID, looked
   up in `db.users`; or by raw `entity_id`, looked up in `db.entities`)
3. What real function debits the sender's entity balance? (`atomic_
   entity_spend`)
4. What happens on both sides of a completed transfer besides the
   ledger post? (Both sides are logged via `log_entity_tx`)

## M2 — atomic-debit discipline

5. Why does the debit use `atomic_entity_spend` rather than a plain
   decrement? (It guards against over-spend at the database level, not
   just in application logic — two concurrent transfer requests can't
   both succeed past an insufficient balance)
6. Is the ledger entry for a transfer balanced (debit + credit) or a
   single-sided record? (Balanced — posted via `ledger_post` between the
   entity account and the destination account)

## M3 — boundary discipline

7. Does this Academy's own `backend/wallet/service.py` have any
   transfer function? (No — only single-account `credit()` exists, no
   transfer of any kind)
8. Can a real Academy candidate initiate a transfer in the real
   `djsayd/CVLN-Wallet` product through this formation? (No — this
   formation teaches the mechanism, never operational access)
