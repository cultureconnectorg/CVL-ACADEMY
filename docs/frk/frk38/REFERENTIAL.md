# FRK-38 — Media Integrity & Anti-Tamper Verification

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION`, action `NEW_EXTERNAL`. Market-general
anti-tamper discipline — never a description of a CVLN system.

## Objectives

A candidate who completes FRK-38 can design a real post-capture
media-integrity verification, completing the third link of the
capture/attestation/integrity chain begun by FRK-36 and FRK-37:

- Explain the three distinct moments of the chain precisely: FRK-36
  covers integrity at the moment of origin (authentic capture);
  FRK-37 covers proof of which device/source produced the asset
  (attestation); FRK-38 covers verifying, after the fact, that no
  alteration occurred since capture — three genuinely distinct
  concerns, none redundant with the others.
- Explain a real anti-tamper detection technique with its actual
  principle: **compression-consistency analysis** — a JPEG (or
  similar) re-saved after editing typically shows double-compression
  artifacts (inconsistent quantization patterns across regions) that
  a single, untouched compression pass would not produce; detecting
  this inconsistency is real forensic-image-analysis practice, not a
  CVLN invention.
- Explain a second real technique: **edit-artifact detection** —
  cloning, splicing, or retouching often leaves statistically
  detectable traces (noise-pattern discontinuities, inconsistent
  lighting/shadow geometry, or a hash-chain break if the asset carries
  incremental integrity hashes) that a verifier can check for.
- Explain precisely why a full media-trust chain needs all three
  formations together, with none substituting for the other two: an
  asset can be authentically captured (FRK-36) by an attested device
  (FRK-37) and still fail integrity verification (FRK-38) if it was
  altered after capture — only FRK-38 covers that failure mode, and
  no single formation of the three is sufficient alone for full trust.
- Reuse FRK-36 and FRK-37 by reference for the capture and attestation
  stages — never re-author them here; cite `docs/frk/frk36/
  REFERENTIAL.md` and `docs/frk/frk37/REFERENTIAL.md` instead.

## Modules

1. **Media-integrity verification fundamentals** — the post-capture
   verification concern, distinct from capture (FRK-36) and
   attestation (FRK-37).
2. **Anti-tamper detection practice** — compression-consistency
   analysis and edit-artifact detection as real, named forensic
   techniques.
3. **Boundary discipline vs. FRK-36/37** — the full three-stage chain
   (capture → attestation → integrity verification), each stage cited
   by reference, none redundant, none sufficient alone.

## Assessment

A verification exercise: candidate designs a post-capture tamper-
detection control (e.g. compression-consistency check or hash-chain
verification) for a media asset, citing FRK-36/37 by reference for the
upstream stages, then explains why an authentically captured asset
(FRK-36) from an attested device (FRK-37) can still fail integrity
verification (FRK-38) if altered after capture — graded against real
integrity-checking practice, never against an invented CVLN
capability.

## Evidence / certification / mission eligibility

`FRK38.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
