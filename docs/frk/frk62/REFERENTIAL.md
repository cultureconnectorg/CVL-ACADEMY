# FRK-62 — Heritage Records & Long-Term Integrity

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION`, action `NEW_EXTERNAL`. Same Fondation
Cœurvolan boundary as FRK-61 (§18 doctrine: FREK owns technical
integrity, Fondation owns consent/community-rights) — inherited, never
re-derived.

## Prerequisites

FRK-61 (recommended).

## Objectives

A candidate who completes FRK-62 can design real long-term integrity
practice for heritage records specifically, deepening FRK-61's general
archiving fundamentals:

- Explain how heritage-record long-term integrity extends FRK-61's
  archiving fundamentals: FRK-61 covers general digital-archiving
  practice; FRK-62 specializes it for heritage records specifically,
  with very-long-term verification requirements (decades, not just
  the standard retention window).
- Distinguish active verification from a mere backup: a backup copies
  the current state; a verification methodology actively confirms, at
  regular intervals, that nothing has been silently corrupted or
  lost — a backup alone gives no evidence about the state of data that
  was never re-checked.
- Design a periodic verification methodology: scheduled re-hashing
  (recompute and compare a stored checksum against the archived
  object, on a defined cadence) and sample auditing (periodically
  verify a statistically meaningful sample of a large collection
  rather than every object every time, when full re-verification is
  too costly) — and justify the cadence chosen against the
  cost/risk tradeoff.
- Keep the inherited Fondation Cœurvolan boundary explicit at all
  times: a verification plan established here confirms *technical*
  integrity of a heritage record (its bits are unchanged) — it never
  makes or implies any decision about who may access that record;
  that is Fondation Cœurvolan's §18 doctrine, a separate governance
  layer never merged into this formation's scope.
- Reuse FRK-61's archiving fundamentals by reference — never re-author
  them here; cite `docs/frk/frk61/REFERENTIAL.md` instead.

## Modules

1. **Heritage-record integrity practice** — the heritage-specific
   very-long-term requirement, and its relationship to FRK-61's
   general archiving base.
2. **Long-term verification methodology** — periodic re-hashing,
   sample auditing for large collections, and cadence justification
   against cost/risk.
3. **Boundary discipline (inherited from FRK-61)** — technical
   integrity only, never a rights/consent/access decision; Fondation
   Cœurvolan's §18 doctrine is cited, never duplicated.

## Assessment

A heritage-record integrity exercise: candidate designs a periodic
verification plan (re-hashing cadence, sample-audit strategy) for a
heritage record collection, citing FRK-61 by reference for the
archiving fundamentals, then explains why the plan never makes an
access-rights decision — graded against real long-term-preservation
practice, never against an invented CVLN capability.

## Evidence / certification / mission eligibility

`FRK62.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
