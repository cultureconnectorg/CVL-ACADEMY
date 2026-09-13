# FRK-34 — Works, Tracks, Albums & Creative Identity

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION`, action `NEW_EXTERNAL`. Cross-domain boundary
with LabelOS (LOS-02 Metadata & Catalog) — FREK proves/tracks identity
of the work, LabelOS manages its catalog/rights record. Not a
duplicate; explicit boundary statement required.

## Objectives

A candidate who completes FRK-34 can design a real work-identity
tracking scheme, kept structurally separate from any catalog/rights
management function:

- Explain what work-identity tracking is at the provenance level
  (work/track/album) and why it differs from catalog/rights management
  (LabelOS LOS-02): identity answers "what is this, how do we
  recognize it"; catalog/rights answers "who owns it, under what
  conditions" — two genuinely distinct functions.
- Explain why LabelOS itself has "zero repo footprint" today
  (`REPO_REGISTRY.md`) and what that implies for this formation's
  boundary: no LabelOS implementation exists to observe, so the
  boundary stays conceptual and preventive — a discipline applied in
  advance, not derived from avoiding duplication of a real system.
- Design a concrete work-identity proof: content hash + structural
  metadata (e.g. duration, track count for an album, structural
  fingerprint) that identifies the work — saying nothing whatsoever
  about who holds rights to it.
- Explain precisely why merging identity and catalog would be a
  structural error even if LabelOS existed tomorrow with a real
  LOS-02: work identity would remain a separate technical function
  from commercial/legal catalog management even then — merging them
  would break separation of responsibilities regardless of whether
  the counterpart system is real or not yet built.
- Reuse the LabelOS boundary discipline as a permanent, never-relaxed
  principle: cite `REPO_REGISTRY.md`'s LabelOS entry as evidence, never
  assume or invent how a future LOS-02 would behave.

## Modules

1. **Creative-work identity tracking fundamentals** — content hash +
   structural metadata as a real, rights-free identity proof.
2. **Provenance-vs-catalog boundary discipline (vs. LabelOS LOS-02)** —
   the boundary holds even though LabelOS has zero repo footprint
   today, and would hold identically if LabelOS existed tomorrow.
3. **Application to works/tracks/albums specifically** — concrete
   identity schemes for each of the three creative-work types.

## Assessment

An identity-tracking exercise: candidate designs a work-identity
scheme (content hash + structural metadata) for a work/track/album
with zero reference to rights or a commercial catalog, then explains
why that scheme would remain valid even if LabelOS (LOS-02) is never
built, and why it would still be structurally separate even if LabelOS
existed — with an eliminatory check on conflating identity-proof with
catalog/rights management.

## Evidence / mission eligibility

No mission eligibility path exists yet. `FRK34.SKILL.
WORK_IDENTITY_TRACKING.L1` reserved once deepened (see
`EVIDENCE_MODEL.md`).

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package (référentiel +
N1/N2 + assessment/rubric + evidence model + 3 guides + integration
note), deepened this pass. Never implies `FULLY_COMPLETE`.
