# FRK-18 — Bitcoin / OpenTimestamps Proof Operations

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION`, action `NEW_EXTERNAL`. OpenTimestamps is a
real, external open protocol — teachable generically; CVLN's own usage
is `CAPABILITY_NOT_IMPLEMENTED`.

## Objectives

A candidate who completes FRK-18 can explain and manually verify a
real OpenTimestamps proof, as literacy in a real external protocol,
never as a description of a CVLN capability:

- Explain how OpenTimestamps anchors a proof in the Bitcoin
  blockchain: Bitcoin serves as a decentralized, publicly-auditable
  clock — a commitment (hash) included in a Bitcoin transaction is
  provably dated no earlier than that block, without trusting any
  single third party.
- Contrast this with RFC 3161 timestamping (FRK-17): RFC 3161 relies
  on a centralized trusted third-party timestamp authority whose
  signature must be trusted; OpenTimestamps relies on Bitcoin's
  public, decentralized ledger — a fundamentally different trust
  model, not just a different transport.
- Explain the Merkle tree aggregation that makes this practical:
  thousands of individual hashes are aggregated into a single Merkle
  root, and only that root is anchored in one Bitcoin transaction —
  each original hash is proven included via its Merkle path (a chain
  of sibling hashes) up to that root, without needing its own
  transaction.
- Manually verify a `.ots` proof without tooling: recompute the local
  file's hash, walk the Merkle path to reconstruct the claimed root,
  and confirm that root matches what was actually committed in the
  named Bitcoin transaction (by consulting a Bitcoin block explorer or
  a full node) — never accept a proof without completing this chain.
- Explain proof independence: because Bitcoin itself is the trust
  anchor (not the OpenTimestamps calendar server that helped
  aggregate the hash), a proof remains verifiable forever even if the
  server that issued it disappears — the server is a convenience, not
  a dependency.
- Keep the CVLN-gap discipline explicit: OpenTimestamps is real and
  teachable, but no system in this repo anchors proofs in Bitcoin
  today — `issue_proof()`'s conceptual proximity (both produce a
  "proof" artifact) is never grounds for claiming CVLN uses this
  protocol.

## Modules

1. **OpenTimestamps protocol literacy** — the Bitcoin-as-public-clock
   trust model, contrasted explicitly with RFC 3161's centralized
   trust model (FRK-17).
2. **Bitcoin-anchoring mechanics** — Merkle tree aggregation (one
   transaction anchors many proofs via a shared root), and manual
   `.ots` proof verification (hash → Merkle path → root → transaction).
3. **CVLN-gap discipline** — no CVLN system anchors proofs in Bitcoin
   today; `issue_proof()`'s superficial conceptual proximity is never
   grounds for claiming otherwise.

## Assessment

A protocol-literacy exam: candidate manually verifies a supplied
simplified `.ots` proof (hash, Merkle path, transaction reference)
without automated tooling, then writes a gap note explaining why CVLN
cannot claim real OpenTimestamps anchoring today despite the
conceptual proximity to `issue_proof()` — graded against the real
OpenTimestamps spec, never against an invented CVLN capability.

## Evidence / certification / mission eligibility

`FRK18.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
