# WAL-26 — Banque N1 (formative, M1→M3)

```
Sourced from the repo-truth already directly verified against
djsayd/CVLN-Wallet/backend/server.py — reused here, not re-audited.
```

## M1 — settlement lifecycle literacy

1. What real transition does `POST /admin/settlements/{id}/submit`
   perform? (`PENDING → SUBMITTED`, via `settlement_transition`)
2. What is a settlement idempotent on when created? (`transaction_id`
   — creating a settlement is idempotent)
3. Why does the submit path need to be retry-safe? (A crash between
   the state transition and the provider-reference write must not
   corrupt state or cause a double-submit to the provider)
4. What does `GET /admin/settlements/{id}` include beyond the current
   state? (Full state history, from `db.financial_state_history`)

## M2 — reconciliation-case literacy

5. Name the 3 real resolutions a reconciliation case can have.
   (`RESOLVED`, `ACCEPTED_DIFFERENCE`, `ESCALATED`)
6. From which states can a case be resolved? (`OPEN` or
   `INVESTIGATING` only)
7. Who can resolve a reconciliation case? (Admin-only)

## M3 — auditability via correlation/events

8. What real function emits an event on every settlement transition?
   (`emit_event`, e.g. `Financial.SettlementCreated`/
   `SettlementSubmitted`)
9. What does tagging events with a correlation ID make possible?
   (Independently reconstructing the settlement state end to end,
   without relying on any single system's current-state view alone)
