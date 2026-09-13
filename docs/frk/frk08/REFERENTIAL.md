# FRK-08 — DID & Verifiable Credentials

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Market-general (W3C
DID/VC standards) — real, teachable, but explicitly
`CAPABILITY_NOT_IMPLEMENTED` for any CVLN-specific claim. Base
formation for FRK-09's sequencing.

## Objectives

A candidate who completes FRK-08 can read, evaluate, and reason about
a real W3C DID/VC implementation — as industry-standard knowledge,
never as a description of what CVLN currently runs:

- Explain the DID (Decentralized Identifier) data model: a DID
  document, its `id`, verification methods, and service endpoints —
  and why a DID is resolvable to that document independent of any
  single registrar.
- Explain the Verifiable Credentials (VC) model: issuer, holder,
  verifier roles; the claim/proof structure of a credential; and the
  difference between credential issuance and credential presentation
  (a holder can present a derived proof without handing over the full
  credential).
- Keep the CVLN-gap discipline explicit at all times: `frek_core.py`'s
  `mint_frek_id()` implements a sequential counter formatted as a
  string — it is not a DID method, has no DID document, no
  verification methods, and issues nothing that meets the W3C VC data
  model. This formation teaches the real standard so a candidate can
  correctly identify that gap, never so they can paper over it.

## Modules

1. **DID method fundamentals** — the DID data model (`did:method:
   identifier` syntax, DID documents, verification methods, service
   endpoints), how resolution works, and why different DID methods
   (did:web, did:key, did:ion, …) trade off decentralization against
   operational simplicity differently.
2. **Verifiable Credentials issuance/verification model** — the
   issuer/holder/verifier triangle, the claim/proof structure of a
   credential, presentation vs. issuance, and selective disclosure as
   a real technique (not specific to any one implementation).
3. **CVLN-gap discipline** — `mint_frek_id()` explicitly is not a DID
   implementation: no DID document, no verification method, no
   resolvable identifier scheme. A candidate must be able to state
   this gap precisely, not vaguely.

## Assessment

A standards-literacy exam graded against the real W3C DID/VC
specifications: candidate explains the DID resolution flow for a
supplied DID, then explains how a Verifiable Credential issued for a
hypothetical claim would be presented and verified — never against an
invented CVLN adaptation of either standard.

## Evidence / certification / mission eligibility

`FRK08.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
