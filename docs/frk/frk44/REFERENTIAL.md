# FRK-44 — Offline Recovery, Synchronization & Reconciliation

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION`, action `NEW_EXTERNAL`. Market-general
discipline — never a description of a CVLN system.

## Prerequisites

FRK-43 (recommended).

## Objectives

A candidate who completes FRK-44 can design real post-disconnection
recovery and reconciliation practice, building on FRK-43's
store-and-forward fundamentals:

- Explain how recovery-after-disconnection and sync reconciliation
  extend FRK-43's store-and-forward base: FRK-43 guarantees delivery
  despite outages (a message eventually arrives); FRK-44 adds
  detecting and resolving state divergence after a prolonged
  disconnection — a distinct problem from delivery.
- Explain what a synchronization conflict is: two concurrent updates
  to the same logical state made independently while disconnected,
  discovered only on reconnection — and why simply resuming store-
  and-forward delivery doesn't resolve it: delivery guarantees the
  messages arrive, not that the resulting state is coherent.
- Compare real reconciliation strategies and their tradeoffs:
  **last-write-wins** (simple, but can silently overwrite legitimate
  concurrent data with no user awareness); **manual resolution**
  (safe — a human decides — but costly in user friction and doesn't
  scale to high-conflict-rate systems); **CRDTs** (Conflict-free
  Replicated Data Types — merge concurrent updates automatically via a
  mathematically commutative merge function, avoiding both data loss
  and friction, but only for data structures that admit a CRDT
  formulation, and with added design complexity).
- Choose a reconciliation strategy for a given context and explicitly
  name the tradeoff accepted — never present a strategy as free of
  tradeoffs.
- Reuse FRK-43's store-and-forward fundamentals by reference — never
  re-author them here; cite `docs/frk/frk43/REFERENTIAL.md` instead.

## Modules

1. **Recovery-after-disconnection design** — the distinct problem of
   post-outage state divergence, beyond FRK-43's delivery guarantee.
2. **Synchronization/reconciliation practice** — real strategies
   (last-write-wins, manual resolution, CRDTs) and the tradeoff each
   one accepts.
3. **Integration of FRK-43 fundamentals (by reference)** — store-and-
   forward reused, never re-authored.

## Assessment

A recovery-design exercise: candidate designs a conflict-detection and
resolution mechanism for post-reconnection state, citing FRK-43 by
reference for the underlying persistent-delivery fundamentals, then
justifies a reconciliation strategy choice (e.g. last-write-wins vs.
manual resolution) for a given context, explicitly naming the
tradeoff accepted — graded against real recovery/reconciliation
practice, never against an invented CVLN capability.

## Evidence / certification / mission eligibility

`FRK44.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
