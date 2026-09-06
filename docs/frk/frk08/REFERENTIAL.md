# FRK-08 — DID & Verifiable Credentials

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Market-general (W3C
DID/VC standards) — real, teachable, but explicitly
`CAPABILITY_NOT_IMPLEMENTED` for any CVLN-specific claim. Base
formation for FRK-09's sequencing.

## Objectives

- Teach the real W3C DID (Decentralized Identifier) and Verifiable
  Credentials standards as an industry body of knowledge.
- Never claim `frek_core.py`'s `mint_frek_id()` implements DID —
  it does not (sequential counter, not a decentralized identifier
  scheme).
- Sequence prerequisite for FRK-09 (identity lifecycle/recovery).

## Modules

1. DID method fundamentals (W3C spec literacy).
2. Verifiable Credentials issuance/verification model.
3. CVLN-gap discipline — `mint_frek_id()` explicitly is not a DID
   implementation.

## Assessment

A standards-literacy exam graded against the real W3C DID/VC
specifications, never an invented CVLN adaptation.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package, deepened this
pass. Never implies `FULLY_COMPLETE`.
