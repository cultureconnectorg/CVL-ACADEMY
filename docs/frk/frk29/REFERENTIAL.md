# FRK-29 — Cultural Fingerprint Foundations

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Base formation for
FRK-30's specialization. Distinct technical domain from FRK-74's
audio-DSP "fingerprint" (see FRK-74's own note) — this formation
covers broader cultural fingerprinting concepts, not audio DSP.

## Objectives

A candidate who completes FRK-29 can explain real cultural-
fingerprinting concepts at a foundational, non-audio-DSP level, laying
the ground for FRK-30's engineering specialization:

- Explain what a cultural fingerprint is: a set of distinctive
  features extracted from a cultural asset that let it be recognized/
  compared/matched — and explain how this differs fundamentally from
  FRK-74's audio-DSP fingerprint, which is strictly limited to audio
  signal processing (spectral analysis, frequency-domain features).
- Explain why a cultural fingerprint can apply to non-audio assets
  (text, image, heritage object) while FRK-74 cannot: the feature-
  extraction principle is generic (any observable, distinctive
  property of an asset) while FRK-74 depends on properties specific
  to sound (spectral content, waveform structure).
- Explain the invariance-to-minor-transformation principle precisely:
  a fingerprint must remain recognizable despite non-substantive
  changes (a minor crop, light recompression, a format conversion)
  while still changing meaningfully when the asset itself changes
  substantively — without this property, a fingerprint would either
  be useless (breaks on any harmless change) or meaningless
  (identical for genuinely different assets).
- Explain why this formation must delimit its FRK-74 boundary
  explicitly from the introduction, not at the end: a candidate who
  later encounters FRK-74 must never assume it is the same subject
  just because both use the word "fingerprint" — the boundary has to
  be established before any risk of confusion, not after.
- Prepare the ground for FRK-30's engineering specialization
  (concrete pipeline: extraction → feature vector → storage/indexing)
  without pre-empting its content — FRK-29 stays at the concept level.

## Modules

1. **Cultural-fingerprint concept fundamentals** — what a fingerprint
   is (distinctive, extracted features enabling recognition/matching),
   independent of any specific asset type.
2. **Feature-extraction principles (non-audio-specific)** — the
   invariance-to-minor-transformation requirement, and why it is
   indispensable for any fingerprinting scheme to be useful.
3. **Boundary discipline vs. FRK-74** — established explicitly from
   the start: cultural fingerprinting (general, this formation) vs.
   audio-DSP fingerprinting (FRK-74, strictly audio-specific) —
   different technical domains, never conflated despite the shared
   word.

## Assessment

A concept exam: candidate designs a distinctive-feature extraction
scheme for a non-audio cultural asset (an image or a text), identifying
the relevant invariants, then explains in writing why that scheme
could not apply as-is to FRK-74's audio-DSP fingerprint and vice versa
— graded against real fingerprinting theory, never against an invented
CVLN capability.

## Evidence / mission eligibility

No mission eligibility path exists yet. `FRK29.SKILL.
CULTURAL_FINGERPRINT_FOUNDATIONS.L1` reserved once deepened (see
`EVIDENCE_MODEL.md`).

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package (référentiel +
N1/N2 + assessment/rubric + evidence model + 3 guides + integration
note), deepened this pass. Never implies `FULLY_COMPLETE`.
