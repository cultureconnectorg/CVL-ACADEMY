# GMD-05 — Ticketing Operations (Live-Events/Festival Industry)

```
Flagship of the GMD-01→20 external market-general pathway (task
#184). Prerequisite: none (entry-level industry role).
```

## Grounding

Real market-standard discipline: ticketing operations management for
live events/festivals (ticket type/tiering design, quota management,
sales-window operations, access-control hand-off). **Worked example**
cited by reference, never re-derived: `docs/gmd/gmd24/REFERENTIAL.md`
(real `TicketType`/`TicketTypeIn` model, `POST/PUT /admin/events/
{eid}/ticket-types/{tid}`, `GET /tickets/{tid}/qr.png`, the real
non-atomic checkout-time quota check vs. the atomic `$inc` at webhook
time, `server.py:115-131`/`574-620`). This formation never claims the
real `gmfest972/goodmooddjsayd` platform is the entire ticketing-
industry standard — it is one real, citable worked example within a
broader market discipline that also includes practices (dynamic
pricing, waitlist management, secondary-market policy) the platform
does not implement.

## Prerequisites

None.

## Objectives

1. Design a ticket-type structure (tiers, quota, pricing) for a real
   event, citing GMD-24's real field model as a worked example.
2. Explain the real quota-integrity nuance GMD-24 documents: the
   checkout-time quota check is not an atomic reservation — the
   actual anti-oversell guarantee is the atomic `$inc` on `sold` at
   webhook-confirmation time, not at checkout time. Never claim a
   reservation lock exists where GMD-24's own repo-truth says it
   doesn't.
3. Distinguish what is real-code-grounded (the GMD-24 worked example)
   from general industry practice not implemented there (dynamic
   pricing, secondary-market/resale policy, waitlists) — teach the
   latter as legitimate market-standard knowledge, never presented as
   a Good Mood platform capability.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | Ticket-type design fundamentals | GMD-24 field model (worked example) | Designed tier structure for a sample event |
| M2 | Quota-integrity nuance | GMD-24's real non-atomic check vs. atomic `$inc` at webhook time | Written explanation, cited to GMD-24, never re-derived |
| M3 | Sales-window & access hand-off | GMD-24 → GMD-25 (door-scan) hand-off, cited by reference | Hand-off checklist |
| M4 | Market-general practices beyond the platform | Industry-standard (dynamic pricing, waitlists, resale policy) | Written note, explicitly labeled `NOT_A_PLATFORM_CAPABILITY` |

## Assessment

Per `../../CERTIFICATION_MODEL.md`. N2 includes a case testing the
quota-integrity nuance (M2) with an eliminatory rule for inventing a
reservation lock that GMD-24's repo-truth does not document.

## Evidence / certification / mission eligibility

Evidence = M1 tier design + M2 written explanation + M4 boundary
note, all checkable against GMD-24's cited repo-truth and standard
industry practice. Certification eligibility: pass Assessment at N2+.
Mission eligibility: none — no real ticketing-operator role exists to
staff through this Academy today.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD05` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Chosen as one of 3 flagships
for the GMD-01→20 external cluster (task #184) — the other 17 rows
stay at `MODULE_CONTENT_DRAFTED` per `../REFERENTIAL.md`, an honest
intermediate depth for market-general content without a unique
per-row repo touchpoint. Not yet delivered to a real candidate —
`FULLY_COMPLETE` still requires that verification, per
`../../QUALITY_GATES.md`.
