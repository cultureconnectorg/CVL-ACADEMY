# GMD-21 — Good Mood OS Operator (umbrella)

```
Prerequisite for GMD-22→33. Orientation formation — teaches the whole
real system's shape before any specialization goes deep on one part.
```

## Repo truth this formation is built on

`gmfest972/goodmooddjsayd/backend/server.py` (874 lines) plus
`frek_service.py`, `wallet_service.py`, `ticketing_service.py`,
`email_service.py`. Full route table already catalogued in
`docs/cvln_academy_master/20_EXTERNAL/GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`
§"Repo truth" — reused here by reference, not restated.

## Prerequisites

None (entry point of the corpus). Recommended: basic REST API literacy
(a candidate should be able to read a route signature and a Pydantic
model before starting).

## Objectives

By the end of GMD-21, a candidate can:
1. Draw the real Good Mood OS system map from memory (catalogue,
   events, tickets, scan, fans/newsletter, merch, orders/payments,
   reporting, FREK/Wallet outbox, admin auth) — not a memorized diagram,
   a derivation from having read the actual route table.
2. Explain, for any given route, which of the 13 specializations
   (GMD-22→33) owns it.
3. Identify which parts of the system have **no** real implementation
   (GMD-34's incident/recovery gap) without being told — by checking
   the repo, not by assumption.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | System map — reading `server.py`'s route table end to end | Full `@api_router.*` listing (34 routes) | Annotated route map, one line per route: model, purpose, owning specialization |
| M2 | Data model literacy | `VolumeIn/Volume`, `EventIn/Event`, `TicketTypeIn/TicketType`, `ProductIn/Product` | Short written note per model: what real-world object it represents, what it does NOT track (e.g. no double-entry ledger) |
| M3 | Auth & session boundary | `/auth/login`, `/auth/me`, `/auth/logout`, `get_current_admin` dependency | Trace which routes require admin auth vs which are public (`/catalogue`, `/events`, `/merch`, `/tour` are public; all `/admin/*` are gated) |
| M4 | Outbox pattern literacy | `frek_service.py` + `wallet_service.py` retry-queue design (`RETRY_BACKOFFS_SEC = [30,120,600,3600,21600]`) | Written explanation of why an outbox exists (network calls must never block a checkout) and what "delivered" vs "pending" means in `db.frek_id_outbox`/`db.wallet_outbox` |

## Assessment

Per `../CERTIFICATION_MODEL.md`. N1: route-ownership quiz (given a
route, name its GMD specialization). N2: "a new team member joins —
brief them on the system in 10 minutes" oral/written case. Assessment:
full annotated route map (M1 deliverable) graded against the real
route table.

## Evidence / certification / mission eligibility

Evidence = the M1 annotated route map + M4 written explanation, both
checkable against the real repo (no invented facts to grade against).
Certification eligibility: pass Assessment at N2+. Mission eligibility:
none directly (GMD-21 is a prerequisite, not a deployable role on its
own) — a candidate becomes mission-eligible once qualified in at least
one of GMD-22→33.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD21` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md` (see each file). Not yet
delivered to a real candidate — `FULLY_COMPLETE` still requires that
verification, per `../QUALITY_GATES.md`.
