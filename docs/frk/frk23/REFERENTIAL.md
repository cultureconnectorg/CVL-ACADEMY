# FRK-23 — Cultural Object Modeling

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Independent of the
`.fk` format blocker (FRK-21/22) — this formation teaches the general
discipline of modeling cultural objects (metadata schemas, entity
relationships), not the specific `.fk` binary format.

## Objectives

A candidate who completes FRK-23 can design a real cultural-object
data model, entirely independent of any binary encoding decision:

- Explain the two-layer distinction precisely: modeling (entities,
  attributes, relationships — the conceptual structure) is a distinct
  layer from serialization (how that structure is encoded to bytes —
  JSON, XML, or a hypothetical `.fk` binary format). This formation
  teaches only the first layer.
- Explain why a well-designed metadata schema stays independent of any
  particular serialization format: a sound conceptual schema
  translates into any format (JSON, XML, binary) without changing
  meaning — if a schema breaks when you change its serialization, the
  schema was never truly well-designed.
- Explain precisely why this formation stays teachable and gradeable
  even while `.fk` (FRK-21/22) remains `BLOCKED_PRODUCT_DEPENDENCY`:
  no `.fk` specification exists anywhere in this repository, so a
  schema built here has literally nothing real to depend on — the two
  subjects are structurally independent, not just conveniently
  decoupled.
- Design real entity-relationship structures for a cultural object:
  identify the entities (e.g. Work, Creator, Provenance Record),
  their attributes, and the relationships between them (e.g. Work
  —createdBy→ Creator, Work —derivesFrom→ Source Work) — using
  general modeling practice, never referencing any CVLN format.
- Keep the boundary absolute: a model that only "happens" to work
  today because of an assumption about how it might later be encoded
  is a hidden dependency and must be redesigned until it has none.

## Modules

1. **Cultural-entity modeling fundamentals** — the modeling-vs-
   serialization distinction, and why a sound schema survives any
   encoding choice.
2. **Metadata schema design** — real entity/attribute/relationship
   design for cultural objects (Work, Creator, Provenance Record, and
   their relationships).
3. **Boundary discipline vs. `.fk` (FRK-21/22, blocked)** — no real
   `.fk` spec exists in this repo; a model built here must never
   depend on one, hidden or explicit.

## Assessment

A modeling exercise: candidate designs a schema (entities, attributes,
relationships) for a cultural object (e.g. a heritage artifact) with
no reference to any serialization format, then explains precisely why
that schema would remain valid even if `.fk` (FRK-21/22) is never
specified — demonstrating the real independence of the two subjects —
graded against real data-modeling practice, never against an invented
CVLN capability.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package, deepened this
pass. Never implies `FULLY_COMPLETE`.
