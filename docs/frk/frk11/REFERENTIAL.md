# FRK-11 — Digital Provenance Specialist

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION (of FRK-04)`, action `SPECIALIZE_EXISTING` —
the practitioner/advanced track built on FRK-04, same pattern as
FMS-08/09 on FMS-03. Never a description of what a CVLN system
implements today.

## Prerequisites

FRK-04 (Cultural Provenance & Digital Trust).

## Objectives

A candidate who completes FRK-11 can practice provenance work at a
specialist level, building on but never re-teaching FRK-04's
fundamentals:

- **Construct a real, multi-hop provenance chain** for a cultural
  asset: each hop records who held or transformed the asset, when,
  and under what attestation — using real, named practice such as
  PROV-O-style entity/activity/agent modeling and C2PA-style
  content-provenance manifests (signed assertions bound to the asset,
  each referencing the prior manifest to form a verifiable chain).
- **Detect and repair a broken provenance chain**: a missing hop, a
  timestamp inconsistency, or an attestation that doesn't verify
  against its claimed signer — and know when a chain must be flagged
  as unverifiable rather than patched over.
- **Resolve a cross-institution provenance dispute**: two institutions
  claim conflicting custody histories for the same asset. Real
  practice: compare each side's evidentiary chain link-by-link,
  identify the first point of divergence, and apply the burden of
  proof to whichever side's chain has the weaker attestation at that
  point — never split the difference without evidence.
- **Practice cross-institution trust establishment**: federated trust
  models (each institution vouches within its own domain, a registry
  or web-of-trust connects domains) vs. a single central authority —
  and the real tradeoff between them (federation avoids a single point
  of control and failure but requires each institution to actually
  maintain trustworthy internal practice; central authority is simpler
  but creates a single point of failure and control).
- Reuse FRK-04's foundation by reference — never re-author chain-of-
  custody or metadata-standard basics here; cite `docs/frk/frk04/
  REFERENTIAL.md` instead.
- Same `CAPABILITY_NOT_IMPLEMENTED` discipline as FRK-04 for any
  CVLN-specific system claim — no CVLN provenance ledger exists today.

## Modules

1. **Advanced provenance-chain construction** — multi-hop chains,
   PROV-O-style entity/activity/agent modeling, C2PA-style signed
   manifests, and detecting/repairing a broken chain.
2. **Dispute resolution & cross-institution trust practice** — the
   link-by-link divergence method for resolving conflicting custody
   claims, and the federated-vs-central-authority trust tradeoff.
3. **CVLN-gap discipline (inherited from FRK-04)** — no CVLN
   provenance ledger or trust registry exists; every CVLN-specific
   claim stays `CAPABILITY_NOT_IMPLEMENTED`, exactly as in FRK-04.

## Assessment

A specialist case study: candidate resolves a hypothetical cross-
institution provenance dispute (two conflicting custody chains) and
proposes a cross-institution trust model, graded against real
provenance practice — building on but not duplicating FRK-04's
assessment, and never attributing any of it to a CVLN system.

## Evidence / certification / mission eligibility

`FRK11.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
