# GMD-31 — FREK Outbox Operator

```
Prerequisite: GMD-21. Triggered by GMD-24/25 (purchase, entry scan).
```

## Repo truth

`frek_service.py` (127 lines) — real env-gated outbox: `emit()` builds
a payload (`source: "good-mood-os"`, `interaction_type: "purchase"|
"entry_scan"`), attempts a synchronous POST to `{FREK_ID_URL}/frek-id/
events` with a 3s timeout, and on any failure (including
`FREK_ID_URL` being empty — the default, `NOT_CONNECTED` state) falls
straight to a persistent outbox with retry backoffs `[30s, 2m, 10m,
1h, 6h]`. Route: `GET /admin/outbox/frek-id`.

## Prerequisites

GMD-21.

## Objectives

1. Read the outbox monitoring route (`/admin/outbox/frek-id`) and
   correctly distinguish `delivered` vs `pending` entries.
2. Explain the exact retry-backoff schedule and what happens after all
   5 attempts fail (marked `failed`, per the reconciliation's own
   repo-truth finding).
3. **Never claim this outbox is connected to this Academy's own
   `frek_core.py`** — it is a different system's FREK client, pointed
   at Good Mood's own `FREK_ID_URL` env var. This boundary is the
   single most important thing this formation teaches (see
   `../CERTIFICATION_MODEL.md` §Evidence chain).

## Modules

| # | Module | Deliverable |
|---|---|---|
| M1 | Outbox payload literacy | Annotated example payload for both `interaction_type`s |
| M2 | Retry-schedule literacy | Written timeline of the 5 retry attempts and the `failed` terminal state |
| M3 | Boundary discipline | Explicit written distinction: Good Mood's `frek_service.py` vs this Academy's `backend/services/frek_core.py` — same *pattern*, never the same *channel* |

## Assessment

Per `../CERTIFICATION_MODEL.md`. M3 is eliminatory — a candidate who
conflates the two FREK systems fails this formation regardless of
other scores, since that confusion is exactly the
`CROSS_DOMAIN_CONTAMINATION` failure mode this whole Master Package
exists to prevent.

## Evidence / certification / mission eligibility

Same general pattern as GMD-22.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD31` — full canonical package built.
`FULLY_COMPLETE` still requires a real candidate pass.
