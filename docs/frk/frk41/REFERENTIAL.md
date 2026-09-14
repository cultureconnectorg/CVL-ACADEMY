# FRK-41 — Stems, Versions, Credits & Music Proof

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION`, action `NEW_EXTERNAL`. Same FMS-03/08
boundary as FRK-40 — this formation teaches the provenance layer on
top of music production, never the production craft itself (FMS-03/08
Founder-gated canon).

## Prerequisites

FRK-40 (recommended).

## Objectives

A candidate who completes FRK-41 can design a real stem/version/
credit provenance-proof scheme for a music production, specializing
FRK-40's general session-tracking base:

- Explain how stem/version/credit tracking extends FRK-40's session-
  tracking base: FRK-40 tracks a session generically (who touched
  what, when); FRK-41 specializes that tracking for the specific
  artifacts of a music production — individual stems, their versions,
  and the credits attached to each.
- Define a stem precisely: an isolated track (vocals, drums, bass,
  etc.) within a larger mix — and explain why its provenance tracking
  differs from FRK-40's generic session tracking: a stem has its own
  lifecycle (recorded, edited, exported, re-exported after a mix
  revision) that must be tracked independently of the session as a
  whole.
- Design a version-tracking scheme for stems: each export of a stem
  gets a distinct, hashed identifier; a later revision is a new
  version, never an overwrite of the proof for the prior one — so a
  dispute about "which version was used in the final master" has a
  verifiable answer.
- Design a credit-proof scheme: binding a named contributor (e.g. a
  mixing engineer) to a specific stem version at a specific time,
  purely as a technical record (hash + timestamp + credited party) —
  never as a rights or compensation determination.
- Keep the inherited FMS-03/08 boundary explicit: this formation, like
  FRK-40, never evaluates production quality, craft, or artistic
  choices — it only proves what happened (which stem, which version,
  credited to whom, when), never whether it sounds good or was made
  well.
- Reuse FRK-40's session-tracking fundamentals by reference — never
  re-author them here; cite `docs/frk/frk40/REFERENTIAL.md` instead.

## Modules

1. **Stem & version provenance tracking** — the stem-vs-session
   distinction, and hashed, non-overwriting version identifiers for
   each stem export.
2. **Music-credit proof practice** — binding a credited contributor to
   a specific stem version and timestamp as a purely technical record,
   never a rights determination.
3. **Boundary discipline (inherited from FRK-40)** — never FMS-03/08's
   production craft or quality evaluation; reuse FRK-40 by reference,
   never redefine it.

## Assessment

A proof-artifact exercise: candidate designs a stem provenance-proof
scheme (hash, version, credit) citing FRK-40 by reference for the
underlying session-tracking base, then explains on a concrete example
why the scheme never judges production quality — graded with the same
eliminatory boundary check as FRK-40.

## Evidence / certification / mission eligibility

`FRK41.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
