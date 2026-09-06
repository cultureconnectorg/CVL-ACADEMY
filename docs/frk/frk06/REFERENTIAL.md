# FRK-06 — FREK-ID Operations

## Repo truth this formation is built on

Grounded directly in `mint_frek_id()` (`backend/services/
frek_core.py`, re-read this session) — per
`FREK_01_75_RECONCILIATION.md`'s own verdict: curriculum coverage
`PARTIAL (repo)`, occupational distinctness `DISTINCT_OPERATOR_ROLE`,
action `NEW_INTERNAL`. Scope honestly bounded to sequential-ID
minting/counter management — never a full identity architecture
(that stays FRK-07/08's market-general territory).

## Prerequisites

FRK-01, FRK-58.

## Objectives

FREK-ID Operations is the narrow, real operational competency of
minting and tracking sequential FREK identifiers — deliberately scoped
below a full identity-architecture discipline:

- Remote-first minting literacy: `mint_frek_id()` attempts a remote
  `POST /mint` first; only on failure/absence does it fall back to the
  local counter mechanism.
- Local counter mechanics: `db.counters` document keyed `"frek_id"`,
  atomically incremented (`find_one_and_update`, `$inc`, `upsert`),
  formatted `FREK-{seq:03d}` (e.g. `FREK-001`, `FREK-042`).
- Explicit scope boundary: this formation never teaches DID/VC
  architecture, EUDI/SD-JWT, or any identity-lifecycle/recovery
  discipline — those are FRK-07/08/09's separate, market-general
  professions, never merged in here.

## Modules

1. **Remote-first minting** — grounded in `mint_frek_id()`'s real
   remote-attempt-then-fallback logic.
2. **Local counter mechanics** — grounded in the real `db.counters`
   atomic-increment pattern and the `FREK-{seq:03d}` format.
3. **Scope boundary discipline** — explicit written distinction from
   FRK-07/08/09's market-general identity-architecture professions;
   never assumed to be the same competency.

## Assessment

A minting-trace exercise: candidate is given a sequence of
`mint_frek_id()` calls (remote available / remote unavailable mixed)
and must predict the resulting IDs and which path (remote vs. local)
produced each — graded against the real code.

## Evidence / certification / mission eligibility

`FRK06.SKILL.*` Skill IDs, reserved once this formation is deepened to
full package. No mission eligibility path exists yet.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package (référentiel +
N1/N2 + assessment/rubric + evidence model + 3 guides + integration
note), deepened this pass. Never implies `FULLY_COMPLETE` — no real
candidate has been assessed yet.
