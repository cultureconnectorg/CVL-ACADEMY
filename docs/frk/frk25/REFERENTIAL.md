# FRK-25 — Schemas, Taxonomies & Object Standards

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Market-general schema
and taxonomy governance discipline — real, teachable, industry-standard
practice, never a description of a CVLN system.

## Objectives

A candidate who completes FRK-25 can design and govern a real
taxonomy/object-standard, distinct from FRK-23's entity-modeling
discipline:

- Distinguish "modeling an entity" (FRK-23: defining what a single
  object's structure looks like) from "governing a taxonomy/object
  standard" (FRK-25: managing the evolving set of categories, fields,
  and conventions that many entities are organized under over time) —
  related but non-overlapping competencies.
- Explain why a taxonomy needs governance beyond its initial
  definition: without a versioning, extension, and deprecation
  process, a taxonomy silently drifts — incompatible versions,
  duplicate categories, inconsistent usage across consumers.
- Apply real object-standard governance practice using named examples:
  Dublin Core (a metadata vocabulary governed by a formal community
  review process, not frozen once published) and schema.org
  (a collaboratively extended vocabulary with a public proposal and
  review process for new types/properties) — what makes each a
  "governed" standard rather than a fixed, one-off schema.
- Design a versioning and deprecation process: how a taxonomy signals
  that a term is deprecated (without breaking existing consumers
  immediately), how a new version is proposed and adopted, and how
  breaking vs. non-breaking changes are distinguished.
- Cross-reference FRK-23 (cultural object modeling) by reference —
  never duplicate or re-author its entity-modeling content here; cite
  `docs/frk/frk23/REFERENTIAL.md` instead.

## Modules

1. **Taxonomy design principles** — categories, fields, and
   conventions as a coherent, extensible structure (not just a list of
   entity types).
2. **Object-standard governance practice** — versioning, deprecation
   (signaling without breaking), extension proposals, and named real
   examples (Dublin Core, schema.org) as governed vs. frozen schemas.
3. **Boundary discipline vs. FRK-23** — entity modeling (FRK-23) is
   not taxonomy governance (FRK-25); reuse FRK-23 by reference, never
   redefine it.

## Assessment

A taxonomy-design exercise: candidate designs a versioned taxonomy for
cultural objects with an explicit deprecation and extension process,
then explains on a concrete example where FRK-23's entity modeling
ends and FRK-25's taxonomy governance begins — graded against real
standards practice, never against an invented CVLN capability.

## Evidence / certification / mission eligibility

`FRK25.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
