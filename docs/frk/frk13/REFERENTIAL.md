# FRK-13 — FREK Proof Engine (internal half)

## Repo truth this formation is built on

Grounded directly in `issue_proof()` (`backend/services/
frek_core.py`, re-read this session) — per
`FREK_01_75_RECONCILIATION.md`'s own verdict: curriculum coverage
`PARTIAL (repo — issue_proof() stub)`, occupational distinctness
`DISTINCT_PROFESSION + DISTINCT_INTERNAL_ROLE`, action
`NEW_EXTERNAL (market concept) + NEW_INTERNAL (operator, current
stub)`. This formation covers **only the internal/operator half** —
the honest reality of today's implementation, explicitly distinguished
from the market-general "proof engine" concept.

## Prerequisites

FRK-01, FRK-58.

## Objectives

The single most important thing this formation teaches is the gap
between "proof engine" as a professional concept and today's actual
implementation:

- **The concept** (market-general, real and teachable independent of
  this repo): a proof engine anchors a claim via chain-of-custody,
  cryptographic signature, and third-party timestamp anchoring —
  producing a verifiable, portable artifact.
- **Today's reality, verbatim**: `issue_proof()` attempts a remote
  `POST /proof` call; on any failure/absence, its local fallback is
  `f"PROOF-{uuid.uuid4().hex[:10].upper()}"` — a random UUID string
  with **no cryptographic signature, no chain-of-custody, no timestamp
  anchoring whatsoever**.
- Operating this reality honestly: a candidate must be able to explain
  to a stakeholder exactly what today's "proof" does and does not
  guarantee — never smoothing over the gap.

## Modules

1. **Proof-engine concept (market-general)** — chain-of-custody,
   cryptographic signature, timestamp anchoring as the real
   professional standard, independent of any CVLN implementation.
2. **`issue_proof()` reality literacy** — grounded in the real stub
   code: remote-first, random-UUID local fallback, zero cryptographic
   guarantee.
3. **Honest gap communication** — producing a stakeholder-facing
   explanation of exactly what today's "proof" guarantees (an
   identifier, nothing more) without either overstating or dismissing
   it.

## Assessment

A gap-explanation exercise: candidate is given a stakeholder question
("is this proof cryptographically verifiable?") and must answer
correctly from the real code (no) while still explaining the concept's
real professional value — eliminatory failure for any answer implying
`issue_proof()` produces a verifiable cryptographic artifact today.

## Evidence / certification / mission eligibility

`FRK13.SKILL.*` Skill IDs, reserved once this formation is deepened to
full package, explicitly scoped to the internal/operator half only.
No mission eligibility path exists yet — issuing a "proof" today
produces no verifiable artifact a mission could depend on.

## Status

`STATUS = MODULE_CONTENT_DRAFTED` — référentiel and module outline
written this pass; N1/N2 banks, full assessment/rubric, evidence
model, and the 3 guides are a future deepening pass, not performed
here.
