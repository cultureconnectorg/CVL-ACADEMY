# FRK-12 — Evidence Engineering

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Base formation for
FRK-15's sequencing (alongside FRK-14).

## Objectives

A candidate who completes FRK-12 can design, structure, and validate a
verifiable evidence artifact as a professional discipline — independent
of any CVLN implementation, and never presented as if CVLN already runs
a production evidence pipeline:

- Design a verifiable evidence artifact from first principles: what
  claim it supports, what data it carries, how a third party checks it
  without trusting the issuer's word alone.
- Apply a real validation & verification methodology — the difference
  between "this artifact exists" and "this artifact is actually valid
  for the claim it makes."
- Distinguish this general evidence-engineering discipline from FRK-13's
  narrow "FREK Proof Engine" scope (a specific implementation
  question, including its real stub state) — this formation is about
  the craft, not one system's unfinished implementation.

## Modules

1. **Evidence-artifact design principles** — what makes an artifact
   verifiable (structure, provenance, tamper-evidence) versus merely
   asserted; the difference between a claim and a proof.
2. **Validation & verification methodology** — the real engineering
   distinction between validating an artifact's internal structure and
   verifying it actually supports the claim it's attached to; common
   failure modes (self-referential proof, unfalsifiable claims).
3. **Boundary discipline vs. FRK-13** — FRK-12 never claims or implies
   that CVLN's own `issue_proof()` stub (FRK-13's exact territory)
   constitutes a working evidence-engineering implementation; the
   candidate must be able to state, precisely, what is real and what
   is not.

## Assessment

An evidence-design exercise: candidate designs a verifiable evidence
artifact for a supplied hypothetical claim, then documents how a third
party would validate its structure and verify it actually supports the
claim — graded against real evidence-engineering practice, never
against a CVLN-specific implementation that does not exist.

## Evidence / certification / mission eligibility

`FRK12.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
