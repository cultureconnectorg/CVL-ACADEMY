# FRK-17 — Trusted Timestamping & Anchoring

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Market-general (e.g. RFC
3161 timestamping standards), real and teachable independent of
CVLN's own (nonexistent) implementation.

## Objectives

A candidate who completes FRK-17 can explain and manually verify a
real trusted timestamp, as literacy in a real external standard, never
as a description of a CVLN capability:

- Explain what a trusted timestamp (RFC 3161 or equivalent) provides
  that a plain local timestamp cannot: a cryptographic binding between
  an artifact's hash and an instant attested by an independent third
  party (a Time-Stamping Authority, TSA) — verifiable by anyone,
  without trusting the party that generated the artifact.
- Explain why a TSA must be independent and verifiable, not just "a
  database that records a date": without an independent third party,
  nothing prevents the artifact's creator from falsifying the date
  after the fact — the entire guarantee comes from external
  verifiability, not from the recorded value itself.
- Explain the RFC 3161 token structure: a hash of the artifact, a
  timestamp, the TSA's identity, and a signature over all of it — and
  why each field is required for the token to be independently
  verifiable (removing the signature, for instance, reduces the token
  to an unverifiable claim).
- Manually verify a simplified RFC 3161-style token: recompute the
  artifact's hash, confirm it matches the hash in the token, then
  verify the TSA's signature over the token's contents using the
  TSA's known public key — never accept a token as valid without
  completing the signature check.
- Distinguish "verifying a timestamp anchor" from "trusting a
  displayed date": verification means replaying the cryptographic
  proof against the TSA (or equivalent anchoring structure); trusting
  a displayed date offers no guarantee at all — it is exactly the gap
  a trusted timestamp exists to close.
- Keep the CVLN-gap discipline explicit: `issue_proof()` (FRK-13,
  `frek_core.py`) generates a plain UUID with no cryptographic
  timestamp binding to any third party — it is not an implementation
  of trusted-timestamp anchoring, and the gap is total, not a nuance
  of implementation detail.

## Modules

1. **RFC 3161 / timestamping-authority fundamentals** — the
   independent-third-party trust model, and why it differs
   fundamentally from a locally recorded date.
2. **Anchoring verification practice** — the token structure (hash +
   timestamp + TSA identity + signature) and manual verification
   (recompute hash → verify TSA signature) without automated tooling.
3. **Boundary discipline vs. FRK-13's stub reality** — `issue_proof()`
   is a plain UUID generator with no cryptographic timestamp binding;
   the gap with RFC 3161 is total, never presented as an
   implementation nuance.

## Assessment

A standards-literacy exam: candidate manually verifies a supplied
simplified RFC 3161-style token (hash, TSA identity, signature) without
automated tooling, then explains in writing why substituting a
`PROOF-{uuid}` identifier from `frek_core.py` for the token would lose
all verifiable timestamp-anchoring guarantee — graded against real
timestamping standards, never against an invented CVLN capability.

## Evidence / certification / mission eligibility

`FRK17.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
