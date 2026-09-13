# CMD-01→14 — SRE / NOC / Incident Command Disciplines (external/market)

## Grounding

Per `AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`:
coverage `NONE`, distinctness `DISTINCT_PROFESSION` ("real SRE/NOC/
incident-command disciplines"), action `NEW_EXTERNAL`. "Market-general
(ICS/SRE-standard content); **explicitly not** `fms-os/fms`'s own
`/os/command-center` (different product, same name —
`CROSS_DOMAIN_CONTAMINATION` risk flagged, never conflate). All CVLN
Command Center claims `CAPABILITY_NOT_IMPLEMENTED`."

**Three-system discipline, the core of this cluster**: this formation
deliberately teaches a market-general discipline that must never be
merged with either of two real, unrelated systems that happen to share
vocabulary:

1. `fms-os/fms`'s own `/os/command-center` route — a real, but
   entirely different, studio-operations KPI dashboard
   (`projects_active`, `bookings_upcoming`, etc. — see
   `docs/fms/fms18/REFERENTIAL.md`). Same name, unrelated product.
2. `MetaCVLN`'s real `/command-center/overview`/`/timeline` routes —
   the actual CVLN Command Center, covered separately by CMD-15
   (`internal/`), read-only, never operated by this Academy.
3. This formation's own subject: generic, industry-standard SRE/NOC/
   Incident Command System (ICS) disciplines, taught independent of
   whether either of the above two systems exists at all.

## Objectives

- Teach real, industry-standard SRE/NOC/Incident Command System (ICS)
  disciplines — fleet monitoring, incident command roles, KPI
  dashboards, escalation runbooks — as market-general knowledge, fully
  independent of any CVLN-branded system.
- Teach the fundamentals of Site Reliability Engineering (SRE) and
  Network Operations Center (NOC) practice: fleet health monitoring,
  alerting thresholds, on-call rotation, and the discipline of
  distinguishing symptom from root cause during an incident.
- Teach the formal Incident Command System (ICS) role structure
  (incident commander, operations lead, communications lead, scribe)
  and the runbook discipline that keeps a live incident response
  organized rather than chaotic.
- Teach KPI-dashboard design as a market-general skill: choosing
  metrics that actually predict operational health, avoiding vanity
  metrics, and designing escalation thresholds tied to those metrics.
- **Mandatory, repeated boundary**: `fms-os/fms`'s own `/os/
  command-center` (a studio-operations KPI dashboard) is a different
  product with the same name — never conflated. The real CVLN Command
  Center (`MetaCVLN`'s `/command-center/overview`/`/timeline`) is
  covered separately in `internal/cmd15` — this formation teaches the
  generic discipline, independent of whether either of those systems
  exists.
- Explain precisely why a candidate confusing any two of these three
  systems is an eliminatory error: each is real (or, for the generic
  discipline, real market knowledge) on its own terms, but none is
  substitutable for another — naming one when the exercise asks about
  another inflates a scope that does not exist.

## Modules

1. SRE/NOC fundamentals — fleet health monitoring, alerting, on-call
   discipline, symptom vs. root-cause triage.
2. Incident Command System (ICS) roles and runbooks — the formal
   role structure and how a runbook keeps a live incident organized.
3. KPI-dashboard design (market-general) — choosing metrics that
   predict operational health, avoiding vanity metrics.
4. Mandatory boundary discipline — `fms-os/fms`'s unrelated
   `/os/command-center` vs. the real CVLN Command Center (`internal/
   cmd15`) vs. this formation's generic discipline — three distinct
   things, never merged.

## Assessment

An SRE/ICS-literacy exam graded against real industry standards, with
an eliminatory check on conflating any of the three systems named in
the boundary module, or on affirming that any CVLN system implements
a complete operational command center on this Academy's side.

## Evidence / mission eligibility

`CMD0114.SKILL.SRE_NOC_ICS_DISCIPLINES.L1` reserved once deepened,
covering all 14 CMD-01→14 rows. No mission eligibility path exists
today for this domain.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package, deepened this
pass. Never implies `FULLY_COMPLETE`.
