# FRK-26 — Relationship & Provenance Graphs

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Base formation for
FRK-27's specialization. Market-general graph-modeling discipline —
never a description of a CVLN system.

## Objectives

A candidate who completes FRK-26 can design a real relationship/
provenance graph, as an industry-general discipline, never as a
description of a CVLN capability:

- Explain what a relationship graph is and why a provenance graph is
  a special case of it: nodes represent entities or versions, edges
  represent derivation/production relationships (this was produced
  from that, this version derives from that version) — a graph
  oriented specifically toward traceability.
- Explain why a classic relational (table-based) model struggles to
  represent deep, variable-length provenance chains: representing an
  arbitrary-depth derivation chain in tables requires either a
  self-referencing join repeated at query time (expensive, awkward)
  or a fixed-depth schema that breaks the moment a chain is deeper
  than anticipated — a graph model represents arbitrary depth
  natively.
- Design a structurally sound provenance graph: every derivation edge
  must be timestamped (when did this derivation happen) and the graph
  must stay acyclic for derivation edges specifically — a chain where
  A derives from B and B derives (even transitively) from A is
  logically incoherent and must never be produced.
- Distinguish a provenance graph from a general relationship graph: not
  every edge in a relationship graph need be acyclic (e.g. "is a
  collaborator of" can be symmetric or cyclic) — only derivation edges
  carry the acyclicity requirement, because derivation implies a
  before/after temporal order.
- Keep the CVLN-gap discipline explicit: no system in this repo
  maintains a real provenance graph today — this is taught as
  market-general graph-design discipline, never attributed to CVLN.

## Modules

1. **Graph-modeling fundamentals** — nodes/edges, the relational-model
   limitation for variable-depth chains, and when a graph model is the
   right structural choice.
2. **Provenance-graph structure design** — the acyclicity requirement
   for derivation edges specifically, mandatory edge timestamping, and
   the distinction between provenance edges and general relationship
   edges.
3. **CVLN-gap discipline** — no CVLN system maintains a real
   provenance graph today; the discipline is taught as market-general
   design practice.

## Assessment

A graph-design exercise: candidate models the derivation chain of a
cultural object (source → derivative → derivative-of-derivative) as a
timestamped, acyclic directed graph, then explains why claiming a CVLN
system maintains "a provenance graph" would be false today — graded
against real graph-modeling practice, never against an invented CVLN
capability.

## Evidence / certification / mission eligibility

`FRK26.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
