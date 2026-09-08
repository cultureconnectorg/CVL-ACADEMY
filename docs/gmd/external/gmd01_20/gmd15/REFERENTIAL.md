# GMD-15 — Safety/Access Management (Live-Events/Festival Industry)

```
Flagship of the GMD-01→20 external market-general pathway (task
#184). Prerequisite: none (entry-level industry role).
```

## Grounding

Real market-standard discipline: event/festival safety and access
management (door/gate operations, crowd flow, incident escalation).
**Worked example** cited by reference, never re-derived:
`docs/gmd/gmd25/REFERENTIAL.md` (real `POST /scan/check`,
`GET /scan/counter/{eid}`, `server.py:722-760` — the 3 real scan
outcomes: valid/duplicate/invalid, and the real absence of an
automated incident/recovery path, cited from GMD-34's own declared
gap). This formation never claims the real `gmfest972/goodmooddjsayd`
platform implements a full safety-operations suite (crowd-density
monitoring, emergency-services coordination, venue capacity alarms)
beyond the door-scan/counter functions GMD-25 documents.

## Prerequisites

None.

## Objectives

1. Operate the real 3 scan outcomes (valid/duplicate/invalid), citing
   GMD-25's decision table as the worked example, never re-deriving
   it independently.
2. Read the live attendance counter correctly and explain precisely
   what it counts, per GMD-25's repo-truth.
3. Escalate correctly at the exact boundary GMD-25/GMD-34 document: no
   automated incident/recovery path exists — any scan failure outside
   the 3 known outcomes is escalated to a human immediately, never
   worked around with an invented procedure. Extend this same
   escalation discipline to broader safety scenarios (medical
   incident, crowd-density concern) that have no code representation
   at all — market-general protocol knowledge, explicitly labeled.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | 3 real scan outcomes | GMD-25 decision table (worked example) | Applied decision table for a sample event-night scenario |
| M2 | Live counter literacy | GMD-25's real counter semantics | Written note on what the counter counts and does not count |
| M3 | Escalation boundary discipline | GMD-25/GMD-34's declared gap (no automated recovery) | Escalation protocol note, citing the gap explicitly |
| M4 | Market-general safety protocols beyond the platform | Industry-standard (crowd-density monitoring, medical/emergency coordination) | Written note, explicitly labeled `NOT_A_PLATFORM_CAPABILITY` |

## Assessment

Per `../../CERTIFICATION_MODEL.md`. N2 includes a simulated event-
night scenario covering all 3 scan outcomes plus one out-of-scope
failure requiring correct escalation — eliminatory if the candidate
invents a recovery procedure instead of escalating.

## Evidence / certification / mission eligibility

Evidence = M1 decision table + M2 counter note + M3 escalation
protocol, all checkable against GMD-25's cited repo-truth. Mission
eligibility: none directly through this Academy — a real door-safety
role is staffed by the operating organization, not certified through
this corpus alone.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD15` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Chosen as the 3rd of 3
flagships for the GMD-01→20 external cluster (task #184) — the other
rows stay at `MODULE_CONTENT_DRAFTED` per `../REFERENTIAL.md`. **This
closes task #184's GMD-01→20 portion.** Not yet delivered to a real
candidate — `FULLY_COMPLETE` still requires that verification, per
`../../QUALITY_GATES.md`.
