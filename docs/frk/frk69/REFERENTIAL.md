# FRK-69 — Evidence & Provenance Audit

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION (of FRK-68)`, action `NEW_INTERNAL`,
sequenced after FRK-68. Grounded in the same real surfaces FRK-68
established: `db.frek_signals` (this Academy), `db.frek_outbox` and
`db.wallet_outbox` (Good Mood).

## Prerequisites

FRK-68 (FREK Auditor).

## Objectives

A candidate who completes FRK-69 can audit a specific evidence
artifact against its real source event, deepening FRK-68's general
procedural audit competency:

- Explain how evidence-artifact auditing extends FRK-68's general
  procedural competency: FRK-68 establishes the general discipline of
  reading and correctly distinguishing three real audit surfaces
  (`db.frek_signals`, `db.frek_outbox`, `db.wallet_outbox`); FRK-69
  specializes that discipline into auditing one specific artifact
  against its claimed source event.
- Recall FRK-68's three real audit surfaces without re-describing
  them: `db.frek_signals` (written by `emit_signal()`, every insert
  carries `user_id`, `signal`, `meta`, `ts`), and Good Mood's two
  outbox tables (`db.frek_outbox`, `db.wallet_outbox`) with their real
  5-attempt retry-backoff schedule (`[30s, 2m, 10m, 1h, 6h]`) — reused
  by reference, never redefined here.
- Explain what distinguishes an evidence-artifact audit from a general
  procedural audit: an artifact audit verifies coherence between a
  specific artifact (e.g. a `PROOF-{uuid}` identifier) and its claimed
  source event actually existing in `db.frek_signals` — more specific
  than a general procedural audit, which verifies the process itself
  conforms (correct system attribution, correct status reading), not a
  single artifact's traceability.
- Perform a concrete evidence-artifact audit: given a `PROOF-{uuid}`
  artifact and access to `db.frek_signals`, determine whether a
  corresponding real event exists, and if not, document the
  inconsistency rather than silently ignoring or assuming it away.
- Explain precisely why confusing FRK-68 and FRK-69 would be
  eliminatory here: it would collapse this formation's specific
  artifact-level specialization back into FRK-68's general procedural
  competency, needlessly duplicating it.

## Modules

1. **Evidence-artifact audit fundamentals** — verifying one specific
   artifact against its claimed source event, distinct from general
   procedural conformance.
2. **Provenance-audit practice** — the concrete audit procedure (locate
   claimed source event, confirm or document its absence) applied to a
   `PROOF-{uuid}`-style artifact.
3. **Integration of FRK-68's three-system discipline (by reference)** —
   the three real surfaces and their behavior reused verbatim, never
   redescribed.

## Assessment

An evidence-audit exercise: candidate audits a `PROOF-{uuid}` artifact
against `db.frek_signals` for source-event correspondence, citing
FRK-68 by reference for the three-surface discipline, then identifies
and documents a case where an artifact has no corresponding source
event — graded against the same real audit surfaces as FRK-68, with an
eliminatory check on ignoring a detected inconsistency.

## Evidence / certification / mission eligibility

`FRK69.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
