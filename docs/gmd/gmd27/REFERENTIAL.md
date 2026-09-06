# GMD-27 — Merch & Store Operator

```
Prerequisite: GMD-21. Independent subsystem (no hard upstream dependency).
```

## Repo truth

`Product`/`ProductIn` model; routes `GET /merch`, `POST/PUT/DELETE
/admin/merch/{pid}`. Structurally identical CRUD shape to GMD-22
(Catalogue) but a distinct real object (`Product` vs `Volume`) and a
distinct business meaning (physical/merch goods vs discography items).

## Prerequisites

GMD-21.

## Objectives

1. Create, update, and retire a `Product` record via the real admin
   routes.
2. Explain the real difference between `Product` (merch) and `Volume`
   (catalogue) — same CRUD shape, different domain object; never
   conflate the two models.
3. Feed accurate merch data into GMD-28 (a merch sale is one of the
   two real revenue sources Orders & Payment Operations handles).

## Modules

| # | Module | Deliverable |
|---|---|---|
| M1 | `Product`/`ProductIn` field literacy | Field table + explicit note distinguishing `Product` from `Volume` |
| M2 | CRUD walkthrough | Runbook mirroring GMD-22's M2, applied to `/admin/merch` |
| M3 | Hand-off to GMD-28 | Written note: what a "sellable" merch item looks like at the field level before a payment can be taken against it |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as GMD-22.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.
