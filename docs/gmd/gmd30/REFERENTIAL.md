# GMD-30 — Event Reporting Operator

```
Prerequisite: GMD-21. Reads GMD-23/24/25 (event, ticket, scan data).
```

## Repo truth

Routes `GET /admin/events/{eid}/report`, `GET /admin/events/{eid}/
tickets`. Read-only aggregation over the real event/ticket/scan data —
no separate reporting database, this is the operator role for the
system's own real report endpoints.

## Prerequisites

GMD-21, GMD-23, GMD-24, GMD-25.

## Objectives

1. Generate and correctly interpret a real event report (attendance,
   ticket sales breakdown) via `/admin/events/{eid}/report`.
2. Cross-check a report figure against the underlying ticket/scan data
   it aggregates from, to build trust in the number rather than taking
   it on faith.
3. Recognize what the report does **not** cover (e.g. no revenue
   breakdown by payment method beyond what `/admin/orders` separately
   provides) and never present it as covering more than it does.

## Modules

| # | Module | Deliverable |
|---|---|---|
| M1 | Report field literacy | Field-by-field breakdown of what `/admin/events/{eid}/report` returns |
| M2 | Cross-check exercise | Manually reconcile one report figure against `/admin/events/{eid}/tickets` raw data |
| M3 | Scope-of-report discipline | Written note on what this report does not cover, and where that data (if it exists) actually lives |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as GMD-22.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD30` — full canonical package built.
`FULLY_COMPLETE` still requires a real candidate pass.
