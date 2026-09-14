# WAL-27 — Banque N1 (formative, M1→M3)

```
Sourced from the repo-truth already directly verified against
djsayd/CVLN-Wallet/backend/server.py — reused here, not re-audited.
```

## M1 — global kill-switch literacy

1. Name the exact 3 global kill-switches. (`withdrawals`, `card`,
   `agents`)
2. What happens if `PUT /admin/kill-switch` is called with a switch
   name outside this exact set? (Rejected with a 400 — validated
   against the exact set)
3. Who can toggle a global kill-switch? (Admin-only)

## M2 — global vs. per-user scope discipline

4. Does toggling the global `"card"` kill-switch affect one user's card
   or all users' cards? (All users — it's a global switch)
5. Does freezing one user's card via `POST /card/freeze` affect any
   other user, or the global `"card"` switch? (No — it's a distinct,
   per-user mechanism; freezing one account touches neither the global
   switch nor any other account)
6. If an admin wants to halt card transactions for the entire platform
   during an incident, which tool is correct — the global switch or a
   per-user freeze? (The global `"card"` kill-switch — a per-user
   freeze would require freezing every account individually and misses
   new accounts created during the incident)

## M3 — audit-trail literacy

7. What real event is logged on every kill-switch toggle? (`audit(...,
   "KillSwitch.Toggled", ...)`)
8. What would a real incident post-mortem need from this audit trail?
   (Who toggled which switch, when, and — implicitly — enough context
   to reconstruct the incident timeline; never assume more detail
   exists in the trail than what `KillSwitch.Toggled` actually records)
