# FRK-61 — Cultural Digital Archiving & Preservation

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Cross-reference
Fondation Cœurvolan (§18 doctrine) — FREK owns technical integrity of
archived objects, Fondation owns consent/community-rights. Explicit
boundary, not a merge.

## Objectives

A candidate who completes FRK-61 can design a real long-term digital
preservation strategy, kept strictly separate from Fondation
Cœurvolan's rights/consent doctrine:

- Explain what digital archiving/long-term preservation is (technical
  integrity of an object over time) and why it stays distinct from
  Fondation Cœurvolan's community-consent/rights doctrine (§18):
  archiving answers "how do we guarantee the object stays intact and
  readable in 50 years"; Fondation Cœurvolan answers "who has the
  right to access it and under what conditions" — two genuinely
  distinct questions.
- Explain three real technical preservation principles needed over
  decades: **format migration** (moving content to current formats
  before the original becomes unreadable, avoiding technological
  obsolescence), **geographic redundancy** (multiple physically
  separated copies, protecting against physical loss — fire, disaster,
  single-site failure), and **periodic integrity verification**
  (re-checking stored objects against known checksums on a schedule,
  to detect silent corruption before it becomes unrecoverable).
- Explain precisely why merging FREK's technical role with Fondation
  Cœurvolan's doctrine would be a design error, even though both touch
  "cultural memory": merging would make the technical system carry
  governance decisions it has no legitimacy to make.
- Design a concrete technical archiving action that takes zero consent
  decisions: e.g. verifying today's recomputed SHA-256 checksum still
  matches the one recorded at initial archival — a purely technical
  action, no rights question anywhere in it.
- Keep the boundary absolute: a preservation strategy is complete and
  valid on its own even if it never mentions Fondation Cœurvolan's
  §18 doctrine at all.

## Modules

1. **Digital-archiving fundamentals** — the technical-integrity-over-
   time framing, distinct from any rights/consent question.
2. **Long-term technical-integrity practice** — format migration,
   geographic redundancy, and periodic integrity verification as the
   three real pillars needed to survive decades.
3. **Boundary discipline vs. Fondation Cœurvolan** — the doctrine
   referenced only as a boundary, never duplicated or merged; a valid
   technical strategy needs zero mention of it.

## Assessment

An archiving-design exercise: candidate designs a preservation
strategy (redundancy, format migration, periodic verification) for a
digital cultural object without ever addressing access rights, then
explains why that strategy would remain valid even without ever
mentioning Fondation Cœurvolan's §18 doctrine — graded against real
preservation practice, never against an invented CVLN capability.

## Evidence / mission eligibility

No mission eligibility path exists yet. `FRK61.SKILL.
DIGITAL_ARCHIVING_PRESERVATION.L1` reserved once deepened (see
`EVIDENCE_MODEL.md`).

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package (référentiel +
N1/N2 + assessment/rubric + evidence model + 3 guides + integration
note), deepened this pass. Never implies `FULLY_COMPLETE`.
