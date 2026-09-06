# GMD-33 — Good Mood Admin & Security Operations

```
Prerequisite for every other GMD-2X/3X role (all admin routes sit behind this).
```

## Repo truth

Routes `POST /auth/login`, `GET /auth/me`, `POST /auth/logout` — real
JWT-based admin authentication (`get_current_admin` dependency used
throughout `server.py`). This is the boundary that separates the
public routes (`/catalogue`, `/events`, `/merch`, `/tour`) from every
`/admin/*` route the other 12 formations operate.

## Prerequisites

GMD-21.

## Objectives

1. Explain the real login/session lifecycle (`/auth/login` →
   token → `/auth/me` verification → `/auth/logout`).
2. Correctly identify which routes require admin auth and which are
   public, without guessing — by reading the `Depends(get_current_
   admin)` usage directly.
3. Recognize a credential-security incident (leaked token, unexpected
   admin session) and know the correct human escalation path — this
   formation does not invent an incident-response runtime (that
   remains GMD-34's declared gap); it teaches recognition and
   escalation only.

## Modules

| # | Module | Deliverable |
|---|---|---|
| M1 | Auth lifecycle literacy | Sequence diagram: login → token issuance → `/auth/me` check → logout |
| M2 | Route-boundary audit | Full list of public vs admin-gated routes, verified against the real `Depends()` usage in `server.py` |
| M3 | Incident recognition (not response) | Written note: what a credential-compromise signal looks like, and that response is a human/GMD-34-gap escalation, never an invented runbook |

## Assessment

Per `../CERTIFICATION_MODEL.md`. This formation inherits the 12-month
sensitive-qualification renewal cycle (`ECO-042`) rather than the
standard 24 months, since it covers authentication/session security.

## Evidence / certification / mission eligibility

Same general pattern as GMD-22, with the shorter renewal cycle noted
above.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.
