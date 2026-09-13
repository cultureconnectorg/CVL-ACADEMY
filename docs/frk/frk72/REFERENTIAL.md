# FRK-72 — FREK Attestation Protocol

## Repo truth this formation is built on

Grounded in `frek_v3/docs/FREK_Attestation_Protocol_v0.1.md` —
`cultureconnectorg/frekcoreAout2026`, commit
`fb272f1d491b09a6d068fb3f6c9c75d407bb0626` (already audited this
session, `REPO_REGISTRY.md`): a specified 283-byte binary attestation
protocol with three levels (L0/L1/L2), backed by a real Python
reference verifier (`reference_verifier/`, 16 passing tests, golden
vectors, real ECDSA P-256 signature verification).

Per `FREK_01_75_RECONCILIATION.md`: coverage `PARTIAL —
SOURCE_OBSERVED`, distinctness `DISTINCT_PROFESSION`, action
`NEW_EXTERNAL`. `ARCHITECTURE_LEVEL_2` per FRK-71's ladder.

## Prerequisites

FRK-71 (FREK v3 Architecture).

## Objectives

A candidate who completes FRK-72 can explain the real, specified
283-byte attestation protocol and its level structure, without ever
inventing a field the specification does not name:

- Describe the protocol's real, verified shape: a fixed 283-byte
  binary attestation format, with three increasing attestation levels
  (L0, L1, L2) — each level adding stronger guarantees over the
  previous one, as the specification itself defines (this formation
  never invents the exact byte offsets or field names beyond what the
  real specification states — see the discipline note below).
- Explain what backs this specification beyond paper: a real Python
  reference verifier (`reference_verifier/`) exists in the repo, with
  16 passing tests and golden test vectors, exercising real ECDSA
  P-256 signature verification — this is genuine engineering evidence,
  not a bare document.
- Explain precisely why this protocol remains classified
  `ARCHITECTURE_LEVEL_2` like FRK-71, rather than "implemented and
  tested in production": the specification is real and internally
  consistent, and a reference verifier exists and passes its tests,
  but no hardware (FPGA) proof and no live production integration
  accompany it — the same maturity discipline as FRK-71, never
  softened just because this formation goes one level deeper into
  detail.
- State the conceptual difference between L0, L1, and L2 in terms of
  increasing attestation strength (each level a superset of guarantees
  over the previous) without asserting specific field content this
  formation cannot verify — a candidate who invents plausible-sounding
  byte-level details not actually in the specification has fabricated
  evidence, exactly what this discipline forbids.
- Reuse FRK-71's maturity ladder by reference — never re-author it
  here; cite `docs/frk/frk71/REFERENTIAL.md` instead.

## Modules

1. **Attestation-protocol structural literacy** — the 283-byte fixed
   binary format and the reference-verifier evidence (16 tests, golden
   vectors, real ECDSA P-256) that backs the specification.
2. **L0/L1/L2 level structure** — the conceptual progression of
   increasing attestation strength across levels, without inventing
   unverified field-level detail.
3. **Maturity-ladder discipline (inherited from FRK-71)** — real
   specification + real reference verifier is still `ARCHITECTURE_
   LEVEL_2`, never inflated to hardware-proven or production-
   integrated status.

## Assessment

A protocol-literacy exam: candidate describes the attestation
protocol's real, verified shape (283 bytes, L0/L1/L2, reference-
verifier evidence) and correctly classifies its maturity level,
without inventing any field or byte-offset beyond what is genuinely
specified — eliminatory failure for inventing unspecified fields or
asserting hardware-proven status.

## Evidence / mission eligibility

`FRK72.SKILL.*` reserved once deepened. No mission eligibility path
exists yet.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package, deepened this
pass. Never implies `FULLY_COMPLETE`.
