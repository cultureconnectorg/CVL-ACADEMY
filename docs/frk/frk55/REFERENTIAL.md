# FRK-55 — API, Event, Error & Versioning Standards

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION`, action `NEW_EXTERNAL`. Market-general
cross-cutting standards discipline — never a description of a CVLN
system.

## Prerequisites

FRK-52 (API Engineering), FRK-54 (Event Bus/Webhooks) (recommended).

## Objectives

A candidate who completes FRK-55 can design real cross-cutting
API/event standards, synthesizing FRK-52 and FRK-54's more specific
competencies into consistency across an entire system surface:

- Explain how this formation synthesizes FRK-52 (API) and FRK-54
  (event bus/webhooks) into cross-cutting standards: each of those
  formations covers one mechanism; FRK-55 unifies the standards
  (error taxonomy, versioning) that must stay consistent across every
  mechanism, not just within one.
- Design a system-wide error taxonomy: a consistent structure (error
  code, category, human-readable message, machine-actionable detail)
  applied identically whether the error surfaces from an API response
  or an event payload — and explain why this is harder to maintain
  than a single API's error taxonomy: it must stay coherent across
  dozens of endpoints and event types, not just one surface, and a
  drift between the two erodes the "one mental model" a consumer needs.
- Design unified versioning: explain why API and event versioning
  should share one version scheme rather than being versioned
  independently — a consumer using both the API and the event stream
  needs a single mental model of "what version am I on"; two
  diverging schemes create integration confusion and bugs (e.g. an
  event payload shaped for v2 arriving while the API is still
  documented as v1).
- Diagnose a concrete integration bug caused by versioning
  inconsistency (e.g. an API field renamed in v2 while the
  corresponding event payload still uses the v1 field name) and
  propose the fix: align both surfaces under the same version
  identifier and changelog.
- Reuse FRK-52 and FRK-54's fundamentals by reference — never
  re-author them here; cite `docs/frk/frk52/REFERENTIAL.md` and
  `docs/frk/frk54/REFERENTIAL.md` instead.

## Modules

1. **Cross-cutting standards synthesis** — why standards that work
   fine within one mechanism (API or events) still need explicit
   unification across both.
2. **Versioning/error-taxonomy design** — a shared version scheme and
   a consistent error taxonomy applied identically across API
   responses and event payloads.
3. **Integration of FRK-52/54 (by reference)** — never re-authored;
   this formation only unifies what those two already established.

## Assessment

A standards-design exercise: candidate designs a unified error
taxonomy and versioning scheme applicable to both an API (FRK-52) and
an event bus (FRK-54), citing both by reference, then diagnoses a
concrete integration bug caused by version-scheme divergence and
proposes the fix — graded against real cross-cutting standards
practice, never against an invented CVLN capability.

## Evidence / certification / mission eligibility

`FRK55.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
