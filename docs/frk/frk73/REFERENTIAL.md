# FRK-73 — FREK Cryptographic Architecture

## Repo truth this formation is built on

Grounded in `frek_v3/docs/FREK_Cryptographic_Architecture_Review_
v0.1.md` + `reference_verifier/frek_crypto.py` (real P-256/ECDSA
primitives, `PUF → HKDF → DRK → AK/FK/CK` key-derivation chain, raw
`r||s` signatures, canonical-message encoding) — already audited this
session, `REPO_REGISTRY.md`.

Per `FREK_01_75_RECONCILIATION.md`: coverage `PARTIAL — SOURCE_
OBSERVED`, distinctness `DISTINCT_PROFESSION`, action `NEW_EXTERNAL`.
**Still `NEEDS_EXPERT_REVIEW`** (applied cryptography, never taught as
production-audited without a named cryptographer's review) — that
caution stands independent of `ARCHITECTURE_LEVEL_2` status.

## Prerequisites

FRK-71.

## Objectives

- Teach the real key-derivation chain and signature scheme as
  specified and implemented in `frek_crypto.py`.
- Carry the `NEEDS_EXPERT_REVIEW` caveat on every claim — this content
  is never presented as cryptographically audited without a named
  expert's review, regardless of how real the code is.

## Modules

1. Key-derivation chain literacy (`PUF → HKDF → DRK → AK/FK/CK`).
2. ECDSA P-256 signature scheme literacy.
3. `NEEDS_EXPERT_REVIEW` discipline.

## Assessment

Deferred pending expert review for any certification claim; literacy
exam on the real code/spec permitted, never a security-audit claim.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`, `NEEDS_EXPERT_REVIEW` unresolved.
