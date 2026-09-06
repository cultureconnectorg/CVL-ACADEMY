# GMD-29 — Newsletter & Campaign Operator

```
Prerequisite: GMD-21. Reads the fan base built by GMD-26.
```

## Repo truth

Routes `POST /newsletter`, `GET /admin/newsletter`, `GET /admin/
newsletter/export`; `email_service.py` with **real bilingual copy**
(`send_newsletter_welcome(to, lang="fr")`, a `copy` dict keyed by
`lang` with `fr` as the guaranteed fallback).

## Prerequisites

GMD-21, GMD-26 (fan data).

## Objectives

1. Send a real newsletter campaign via the admin route and export the
   subscriber list correctly.
2. Explain the real bilingual-copy mechanism: which languages are
   actually implemented in `email_service.py`, and what the fallback
   behavior is for an unimplemented language (falls back to `fr`,
   never silently fails).
3. Never claim a language is supported that isn't actually in the
   `copy` dict — the same data-honesty discipline as GMD-26.

## Modules

| # | Module | Deliverable |
|---|---|---|
| M1 | Newsletter send/export walkthrough | Runbook: compose → send via `/newsletter` → export via `/admin/newsletter/export` |
| M2 | Bilingual copy literacy | Written table: which `lang` keys actually exist in `email_service.py`'s `copy` dict, and the fallback rule |
| M3 | Campaign-to-fan-base linkage | Note on how GMD-26's fan records feed this formation's recipient list |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as GMD-22.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.
