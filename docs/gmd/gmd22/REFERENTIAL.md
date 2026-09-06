# GMD-22 — Catalogue Operator

```
Prerequisite: GMD-21.
```

## Repo truth

`Volume`/`VolumeIn` model (`server.py:80-98`); routes `GET/POST/PUT/
DELETE /catalogue`, `GET/POST/PUT/DELETE /admin/catalogue`. `Volume`
is Good Mood/DJ Sayd's discography/tour catalogue object.

## Prerequisites

GMD-21 (system map).

## Objectives

1. Create, read, update, and retire a `Volume` record via the real
   admin routes without violating the model's required fields.
2. Explain the difference between the public `GET /catalogue` (what a
   fan sees) and the admin CRUD routes (what an operator does).
3. Diagnose a "catalogue item not showing publicly" report by
   checking the actual fields the public route filters on.

## Modules

| # | Module | Deliverable |
|---|---|---|
| M1 | `Volume`/`VolumeIn` field-by-field literacy | Written field table: name, type, required?, public-visible? |
| M2 | CRUD walkthrough on the real admin routes | Step-by-step operator runbook: create → verify via public route → update → verify → soft-retire |
| M3 | Diagnostic case | Given a symptom ("item missing from `/catalogue`"), trace to the real cause using only the model/route definitions |

## Assessment

Per `../CERTIFICATION_MODEL.md`. Assessment artifact: the M2 runbook,
executed and verified (screenshots/log excerpts of each step against
a real or sandboxed instance where available; otherwise a fully
reasoned code-level walkthrough).

## Evidence / certification / mission eligibility

Evidence = M1 field table + M2 runbook + M3 diagnostic writeup.
Certification eligibility: Assessment at N2+. Mission eligibility: a
certified GMD-22 operator is eligible for a real catalogue-maintenance
mission once GMD-21 is also certified and a genuine operational need
is confirmed (per `GMD_CANONICAL_EDUCATION_MAP.md` §Mission
eligibility).

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.
