# FMS-15 — Banque N1 (formative, M1→M3)

```
Sourced against REFERENTIAL.md's own real fms-os/fms citations
(backend/server.py, re-read this session).
```

## M1 — lead qualification

1. Name the real fields `LeadCreate` provides that a qualification
   decision should read. (`project_type`, `objective`, `budget_range`,
   `timeline` — plus `name`/`email`/`phone`/`company`)
2. How is a real lead populated into `GET /os/leads`? (Via the public
   `POST /public/leads` endpoint)

## M2 — client lifecycle management

3. Name the real 6-stage `status` enum on `ClientCreate`. (`lead`,
   `qualified`, `prospect`, `client`, `repeat_client`, `vip`)
4. What is `ClientCreate`'s default `type`? (`"individual"`)

## M3 — commercial reporting discipline

5. What must an operator do when a `command_center` KPI (e.g.
   `revenue_mtd`) is reported as `INSUFFICIENT_DATA`? (Recognize it
   honestly as not populated — never assume or invent a value)
6. What is the assessment artifact? (A qualification decision, a
   client-status progression plan, and a commercial-report reading,
   given a representative lead record, graded against the real data
   model — never an invented CRM feature)
