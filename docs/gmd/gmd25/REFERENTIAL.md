# GMD-25 — Door Scan & Access Operator

```
Prerequisite: GMD-21, GMD-23 (needs an event), GMD-24 (needs tickets to scan).
```

## Repo truth

Routes `POST /scan/check`, `GET /scan/counter/{eid}` (`server.py:722-
760`). Real duplicate-scan and counter logic — this is the single most
"field-operations" role in the corpus (the person physically at the
door on event night).

## Prerequisites

GMD-21, GMD-23, GMD-24.

## Objectives

1. Operate `/scan/check` correctly under real event-night pressure:
   valid scan, duplicate scan, invalid ticket — three distinct real
   responses, not one generic error.
2. Read the live attendance counter (`/scan/counter/{eid}`) and explain
   what it counts.
3. Escalate a scan failure correctly (this is exactly the boundary
   where GMD-34's absence matters — a scanning incident has no formal
   recovery path yet; the operator must know to escalate to a human,
   never to invent a workaround).

## Modules

| # | Module | Deliverable |
|---|---|---|
| M1 | The three real scan outcomes (valid/duplicate/invalid) | Written decision table: outcome → operator action |
| M2 | Live counter literacy | Explanation of what `/scan/counter/{eid}` counts and does not count |
| M3 | Escalation boundary | Explicit note: "no automated incident/recovery exists (GMD-34) — a scan failure that isn't one of the three known outcomes is escalated to a human immediately, never worked around" |

## Assessment

Per `../CERTIFICATION_MODEL.md`. N2 case: a simulated event-night
scenario covering all three scan outcomes plus one out-of-scope
failure requiring correct escalation (not a fabricated recovery
procedure).

## Evidence / certification / mission eligibility

Same general pattern as GMD-22. Mission eligibility for this role is
the most field-time-sensitive in the cluster — it directly gates
who may staff a real door on a real event night.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD25` — full canonical package built.
`FULLY_COMPLETE` still requires a real candidate pass.
