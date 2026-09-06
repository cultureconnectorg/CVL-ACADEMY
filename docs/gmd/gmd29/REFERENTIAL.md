# GMD-29 — Newsletter & Campaign Operator

```
Prerequisite: GMD-21. Reads the fan base built by GMD-26.
```

## Repo truth

Routes `POST /newsletter`, `GET /admin/newsletter`, `GET /admin/
newsletter/export` (`server.py:241-252`); `email_service.py:64-82`
with **real 4-language copy** (`send_newsletter_welcome(to,
lang="fr")`, a `copy` dict keyed by `lang` with `fr` as the guaranteed
fallback). **Re-verified this session:** the 4 real keys are
`fr`/`en`/`es`/`kr` — and `"kr"`'s content is Haitian Creole ("Byenveni
nan Good Mood"), not Korean, despite the key name. No unsubscribe
route exists anywhere in the audited code.

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

`STATUS = PACKAGE_COMPLETE_FOR_GMD29` — full canonical package built.
`FULLY_COMPLETE` still requires a real candidate pass.
