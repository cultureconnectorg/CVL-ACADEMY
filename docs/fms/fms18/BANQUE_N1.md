# FMS-18 — Banque N1 (formative, M1→M4)

```
Sourced against REFERENTIAL.md's own real fms-os/fms citations
(backend/server.py, re-read this session).
```

## M1 — command-center KPI literacy

1. What must an operator distinguish when reading `command_center`
   KPIs? (A populated metric with a stated `source`/`formula` from
   one explicitly marked `INSUFFICIENT_DATA`, e.g. `revenue_mtd`)

## M2 — ecosystem-integration operations

2. Name the real 7 ecosystem adapters in `ECOSYSTEM_INTEGRATIONS`.
   (Frek-ID, FREKCORE, FREKANSLA, KORA, CVLN Wallet, CVL Brain,
   Laurentia)
3. What is each adapter's real status in the code today? (Every one
   explicitly `"status": "NOT_CONNECTED"`)
4. What must an operator never do regarding this status? (Claim a
   connection is live when the real registry says `NOT_CONNECTED`)

## M3 — audit-log & accountability discipline

5. What real endpoint provides the audit trail, and what are its
   real characteristics? (`GET /os/audit-log` — append-style,
   `db.audit_log`, sorted by `timestamp`, capped at 500)

## M4 — content/portfolio operations (absorbed FMS-17)

6. What FMS-04 blocks does this absorbed content cite by reference?
   (Content/campaign blocks — this is content/asset-portfolio
   operations across projects, not campaign-design craft itself)
7. What must never be confused with CVLN's own "Command Center"/"CVL
   Brain" systems referenced elsewhere in this Master Package? (The
   `fms-os/fms` `/os/command-center` — a studio-operations KPI
   dashboard, a different system that happens to share a name)
