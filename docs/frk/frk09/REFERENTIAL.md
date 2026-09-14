# FRK-09 — Identity Lifecycle, Recovery & Reconciliation

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION (of FRK-08)`, action `NEW_EXTERNAL`,
sequenced after FRK-08 as prerequisite, not merged into it — a real,
separately-practiced IAM discipline. Never a description of what
`frek_core.py` implements today.

## Prerequisites

FRK-08 (DID & Verifiable Credentials).

## Objectives

A candidate who completes FRK-09 can design and reason about a real
identity lifecycle, recovery, and reconciliation practice, as an IAM
discipline distinct from FRK-08's foundational DID/VC literacy:

- Explain the three real lifecycle stages of a managed identity:
  **issuance** (initial credential creation, binding to a subject),
  **rotation** (replacing key material or credentials on a schedule or
  after a suspected compromise, without breaking existing trust
  relationships), and **revocation** (invalidating a credential before
  its natural expiry, and how relying parties learn of it — revocation
  lists, status registries, or short-lived credentials).
- Explain recovery practice: how a subject regains control of an
  identity after losing key material (social recovery, guardian-based
  schemes, custodial recovery paths) and why recovery design is itself
  a security tradeoff (easier recovery generally means a wider attack
  surface for account takeover).
- Explain reconciliation practice: detecting and resolving a state
  where two systems disagree about the current status of an identity
  (e.g. one system still trusts a revoked credential) — a real
  operational discipline in any federated identity system.
- Keep the CVLN-gap discipline explicit at all times: `mint_frek_id()`
  has none of these three lifecycle mechanisms. It issues a sequential
  counter value once and has no rotation path, no revocation registry,
  and no recovery flow. A candidate must never claim, even implicitly,
  that a FREK-ID can be rotated, revoked, or recovered today.

## Modules

1. **Identity lifecycle stages** — issuance, rotation, and revocation
   as three distinct, real mechanisms, each with its own failure modes
   and operational requirements.
2. **Recovery & reconciliation practice** — real recovery schemes
   (social/guardian-based/custodial) and their security tradeoffs;
   reconciliation as detecting and resolving cross-system disagreement
   about identity status.
3. **CVLN-gap discipline** — `mint_frek_id()` has no rotation,
   revocation, or recovery mechanism; a candidate must state this gap
   precisely for each of the three lifecycle stages, not just once in
   general terms.

## Assessment

A lifecycle-design exercise: candidate designs issuance, rotation, and
revocation flows for a hypothetical identity system, then explains a
recovery path and a reconciliation scenario — graded against real IAM
practice, never against an invented FREK-ID capability.

## Evidence / certification / mission eligibility

`FRK09.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
