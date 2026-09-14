# FRK-27 — Cultural Knowledge Graph Engineering

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION (of FRK-26)`, action `NEW_EXTERNAL`.
Market-general knowledge-graph discipline — never a description of a
CVLN system.

## Prerequisites

FRK-26 (Relationship & Provenance Graphs).

## Objectives

A candidate who completes FRK-27 can engineer a real cultural
knowledge graph, deepening FRK-26's graph-modeling fundamentals into
semantically rich, inference-capable structures:

- Explain how knowledge-graph engineering extends FRK-26's foundation
  beyond a simple derivation structure: FRK-26 establishes the
  acyclic, timestamped derivation graph shape; FRK-27 adds rich
  semantics — typed nodes and relationships (an ontology) and
  inference over them — beyond plain traceability.
- Explain why a cultural knowledge graph needs semantically typed
  nodes/relationships (an ontology) rather than plain node-edge pairs:
  a typed relationship (e.g. "influencedBy", "createdDuring",
  "memberOf") carries meaning a generic edge cannot, and only typed
  relationships support meaningful inference rules.
- Design a minimal ontology for a cultural domain: node types (e.g.
  Artwork, Movement, Period, Place, Creator) and typed relationship
  types between them (e.g. Artwork —createdDuring→ Period, Creator
  —memberOf→ Movement) that together support real queries a
  relational join could not express naturally.
- Explain why an inference query ("find all works indirectly
  influenced by X") is natural on a knowledge graph but awkward in
  classic relational SQL: a knowledge graph traverses typed
  relationships transitively (a native graph operation); the
  equivalent in SQL requires recursive self-joins of unknown depth,
  which is exactly the limitation FRK-26 already identified for
  variable-depth chains — FRK-27 shows the same limitation resurfacing
  at the semantic-query level.
- Reuse FRK-26's graph-modeling fundamentals by reference — never
  re-author them here; cite `docs/frk/frk26/REFERENTIAL.md` instead.

## Modules

1. **Knowledge-graph engineering practice** — the ontology-design
   step (typed nodes/relationships) built on top of FRK-26's
   acyclic/timestamped structural foundation.
2. **Cultural-domain application patterns** — a real minimal ontology
   example (Artwork/Movement/Period/Place/Creator) and the kind of
   inference query it enables.
3. **Integration of FRK-26 fundamentals (by reference)** — the
   acyclicity/timestamping discipline is inherited, never re-derived.

## Assessment

A knowledge-graph design exercise: candidate designs a minimal
ontology (node types, relationship types) for a given cultural domain,
citing FRK-26 by reference for the underlying graph structure, then
explains why an indirect-influence inference query is natural on the
resulting knowledge graph but awkward in classic relational SQL —
graded against real knowledge-graph engineering practice, never
against an invented CVLN capability.

## Evidence / certification / mission eligibility

`FRK27.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
