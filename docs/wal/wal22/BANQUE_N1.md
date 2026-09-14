# WAL-22 — Banque N1 (formative, M1→M3)

```
Sourced from the repo-truth already directly verified against
djsayd/CVLN-Wallet/backend/server.py (commit 359aaee1) — reused here,
not re-audited.
```

## M1 — coffre lifecycle literacy

1. What does `POST /coffres` create, and what does `amount_cc` start
   at? (A new vault, with `name`/`icon`/`goal_cc`/`color`; `amount_cc`
   starts at 0)
2. What happens to the user's available balance when they move cash
   *into* a coffre? (It is spent via `atomic_spend` — the coffre isn't
   free money, it's a reallocation of the same balance)
3. What happens when they move cash *out* of a coffre? (It is credited
   back to the user via `apply_user_balance`)
4. What happens to a coffre's remaining balance when it is deleted via
   `DELETE /coffres/{coffre_id}`? (It is refunded to the user before
   deletion — closing a non-empty coffre never destroys value)

## M2 — ledger-posting discipline

5. Is a coffre move a raw field update on `amount_cc`, or something
   more? (Something more — every move calls `ledger_post`, recording a
   balanced double-entry between the user's cash account and the
   coffre's own account)
6. Why does this matter for audit purposes? (A raw field update leaves
   no trace of where the value came from or went; a balanced ledger
   entry does)

## M3 — boundary discipline

7. Does this Academy's own `backend/wallet/` have any vault/coffre
   concept? (No — none exists; this is a real capability of the
   external `djsayd/CVLN-Wallet` product only)
8. Can a real Academy candidate create or move funds in a real user's
   `djsayd/CVLN-Wallet` coffre through this formation? (No — no
   integration between the two repos is observed; this formation
   teaches literacy of the real product's mechanism, never operational
   access to it)
