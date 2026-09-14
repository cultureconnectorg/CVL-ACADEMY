# FRK-37 — Source & Device Attestation

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION`, action `NEW_EXTERNAL`. Market-general
device-attestation discipline — never a description of a CVLN system.

## Objectives

A candidate who completes FRK-37 can design a real source/device
attestation mechanism, distinct from FRK-36's broader authentic-
capture discipline:

- Explain what source/device attestation is: proving which specific
  device or source produced a media asset — distinct from FRK-36's
  broader authentic-capture discipline (integrity from the moment of
  origin generally), which this formation specializes.
- Explain why device attestation requires a hardware or cryptographic
  root of trust (e.g. a key bound to the device at manufacture):
  without a root of trust, any software could claim to be any device —
  trust must anchor in a verifiable secret that only the genuine
  device possesses.
- Design an attestation mechanism using a real pattern: a signed
  device certificate, where the device's embedded key signs a
  statement (or the captured asset's hash) and a verifier checks that
  signature against a certificate chain rooted in a trusted
  manufacturer or issuer key.
- State precisely what a device certificate proves and what it does
  NOT prove: it proves the device possesses a specific key (and, by
  extension, was manufactured/provisioned by the claimed issuer); it
  does NOT prove the captured content was unmodified after capture —
  that is FRK-38's domain (content-integrity attestation), a distinct
  and later stage in the chain.
- Reuse FRK-36 by reference for the general authentic-capture
  context — never re-author it here; cite `docs/frk/frk36/
  REFERENTIAL.md` instead.

## Modules

1. **Device-attestation fundamentals** — the hardware/cryptographic
   root-of-trust requirement, and why software alone cannot attest a
   device's identity.
2. **Source-verification practice** — the signed-certificate pattern
   (device key signs a statement, verifier checks the certificate
   chain), and precisely what it proves vs. does not prove.
3. **Boundary discipline vs. FRK-36** — this formation specializes
   FRK-36's broader capture discipline into device/source attestation
   specifically; FRK-36 is cited by reference, never redefined. Also
   never conflated with FRK-38 (post-capture content-integrity
   attestation, a separate later stage).

## Assessment

An attestation-design exercise: candidate designs a device-attestation
mechanism (root of trust, signed certificate) to prove a media asset's
origin, citing FRK-36 by reference for the capture context, then
explains precisely why a valid device attestation alone does not
guarantee the content's integrity after capture — graded against real
attestation practice, never against an invented CVLN capability.

## Evidence / certification / mission eligibility

`FRK37.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
