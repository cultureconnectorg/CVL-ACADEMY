# FRK-42 — Offline Proof Transport

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`, `CAPABILITY_NOT_
IMPLEMENTED` — no CVLN system moves proof artifacts across
disconnected environments today. Real, industry-general security
engineering discipline (air-gap transfer, "sneakernet" proof delivery),
never a description of a CVLN capability.

## Objectives

A candidate who completes FRK-42 can design a real offline-proof-
transport scheme, distinct from FRK-20's offline *verification*
discipline:

- Explain the transport problem precisely: FRK-20 verifies a proof
  artifact with no network access; FRK-42 designs how that artifact
  physically moves from one disconnected environment to another
  (USB drive, printed QR code, optical media) without losing its
  verifiability or being silently tampered with in transit — a
  distinct engineering problem from verification itself.
- Design self-verifying artifacts: the artifact carries proof of its
  own integrity (a detached signature, or a signature embedded in the
  artifact's own structure) so any bit-level change in transit is
  detectable without needing network access to check.
- Detect tampering in transit: a self-verifying artifact carries
  enough of its own proof (hash + signature, or a Merkle proof against
  a previously-published root) that the receiving environment can
  verify it end-to-end without trusting the transport medium itself.
- Handle multi-artifact ordering and gaps: when several proof
  artifacts must arrive in sequence (e.g. a hash-chained log), the
  transport design must let the receiver detect a missing or
  out-of-order artifact rather than silently accepting a gap as
  complete.
- Real transport patterns: USB/removable media with a manifest file
  listing expected hashes, printed/QR-code transport for small
  artifacts (a signed JWT small enough to encode visually), and
  data-diode-style one-way transfer for high-assurance air-gapped
  environments.
- Keep the CVLN-gap discipline explicit: no system in this repo
  implements offline proof transport today — this is taught as
  market-general design practice, never as a CVLN capability.

## Modules

1. **Offline-transport design patterns** — self-verifying artifact
   construction (embedded or detached signature), USB/removable-media
   patterns with manifest hashes, QR-code transport for small
   artifacts, and data-diode-style one-way transfer.
2. **Disconnected-environment proof-artifact handling** — tamper
   detection at the receiving end (verify without trusting the
   medium), and multi-artifact ordering/gap detection for sequences
   that must arrive complete and in order.
3. **CVLN-gap discipline** — no CVLN system transports proof
   offline today; the discipline is taught as market-general design,
   never attributed to this repo.

## Assessment

A design exercise: candidate designs a self-verifying proof-artifact
format for transport across a disconnected environment, addressing
tamper detection and ordering — graded against real offline-transport
practice, never against an invented CVLN capability.

## Evidence / certification / mission eligibility

`FRK42.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
