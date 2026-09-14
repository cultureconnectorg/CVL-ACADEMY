# FRK-47 — Audit Trail & Institutional Accountability

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Market-general audit-
trail discipline — never a description of a CVLN system, distinct from
FRK-68's grounded operator application.

## Objectives

A candidate who completes FRK-47 can design a real institutional
audit-trail scheme, kept independent of any one technical
implementation — including FRK-68's own real grounding:

- Explain what an institutional audit trail is and why it differs from
  FRK-68's FREK Auditor operator role: FRK-47 is the general design
  discipline (what to log, how, why); FRK-68 is the concrete operator
  application of that discipline in the real FREK context.
- Explain why FRK-68 is grounded on real, verifiable artifacts
  (`db.frek_signals`, the outbox) while FRK-47 stays a general
  professional discipline: FRK-68 documents an actual operator role
  wired to actual collections; FRK-47 stays independent of any
  specific implementation, teachable in any institutional context.
- Explain a fundamental institutional-accountability principle —
  **separation of duties**: no single person should control both an
  action and its audit of that action — and why this principle holds
  regardless of the technical system in use, a general governance
  requirement, not a CVLN-specific one.
- Explain a second fundamental principle — **non-repudiable
  traceability**: an audit record must be attributable to a specific
  actor at a specific time in a way that actor cannot later credibly
  deny, typically via append-only logging plus a real identity binding
  at write time.
- Design a generic audit-trail schema (who acted, what action, when,
  under what authority) applicable to any institutional context, with
  no reference to FREK internals — then explain precisely why that
  schema would remain valid even if FRK-68 (FREK Auditor) did not
  exist, while FRK-68 remains the real reference for the actual
  operator application.
- Reuse FRK-68 by reference for the concrete operator application —
  never re-author its `db.frek_signals`/outbox grounding here; cite
  `docs/frk/frk68/REFERENTIAL.md` instead.

## Modules

1. **Audit-trail design fundamentals** — the general schema (actor,
   action, timestamp, authority) independent of any implementation.
2. **Institutional-accountability practice** — separation of duties
   and non-repudiable traceability as principles that hold regardless
   of the technical system.
3. **Boundary discipline vs. FRK-68** — FRK-47 (general discipline) vs.
   FRK-68 (real FREK operator application, grounded on
   `db.frek_signals`/outbox); reused by reference, never redefined.

## Assessment

An audit-design exercise: candidate designs a generic institutional
audit-trail schema (separation of duties, non-repudiation) with no
reference to FREK internals, then explains why that schema would stay
valid even without FRK-68 existing, while FRK-68 remains the real
reference for the concrete operator application — graded against real
accountability practice, never against an invented CVLN capability.

## Evidence / certification / mission eligibility

`FRK47.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today (FRK-68 carries the real grounding).

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
