# FRK-59 — FREK × CVLN Wallet Integration

## Repo truth this formation is built on

Grounded in real precedent at Good Mood — per
`FREK_01_75_RECONCILIATION.md`'s own verdict: curriculum coverage
`PARTIAL`, occupational distinctness `CROSS_ECOSYSTEM_ROLE`, action
`NEW_CROSS_ECOSYSTEM`, "teach this exact gap (two decoupled outboxes
is not yet an 'integration') rather than implying a wired pipeline
that doesn't exist":

- `frek_service.py` (127 lines, cited in `docs/gmd/gmd31/
  REFERENTIAL.md`) — real env-gated outbox posting to Good Mood's own
  `FREK_ID_URL`, persistent retry on failure (`[30s, 2m, 10m, 1h, 6h]`),
  monitored via `GET /admin/outbox/frek-id`.
- `wallet_service.py` (115 lines, cited in `docs/gmd/gmd32/
  REFERENTIAL.md`) — same real pattern, posting to Good Mood's own
  `WALLET_URL`, its own `db.wallet_outbox`, monitored via `GET /admin/
  outbox/wallet`.
- **These two outboxes are real, independent, and not linked to each
  other.** CVL-ACADEMY's own `backend/wallet/` does not call
  `frek_core` at all today, either.

## Prerequisites

FRK-01, FRK-58, GMD-31, GMD-32 (or literacy of their referentials).

## Objectives

FREK × CVLN Wallet Integration teaches the honest current state of
this cross-ecosystem relationship — two decoupled real outbox clients,
not a wired pipeline:

- Recognizing that Good Mood's `frek_service.py` and `wallet_service.py`
  are two **separate** real systems, each independently env-gated
  (`FREK_ID_URL`, `WALLET_URL`), each `NOT_CONNECTED` by default, and
  **never observed to call each other**.
- Explaining that "FREK × Wallet integration" today means *two
  independent outbound clients that happen to exist in the same
  codebase* — not a functioning cross-system pipeline a candidate
  could operate end-to-end.
- Explicit boundary against this Academy's own systems: Good Mood's
  outboxes are outbound *clients* to external URLs; they are not the
  same code as this Academy's own `frek_core.py`/`backend/wallet/`,
  which do not call each other either.

## Modules

1. **`frek_service.py` outbox literacy** — grounded in the real
   env-gated pattern, retry schedule, monitoring route.
2. **`wallet_service.py` outbox literacy** — grounded in the same real
   pattern applied to `WALLET_URL`.
3. **"Not yet an integration" discipline** — explicit written
   recognition that two decoupled real clients is the accurate
   description of today's state, never inflated into a claimed working
   pipeline, and never confused with this Academy's own separate
   `frek_core.py`/`backend/wallet/` (which also don't call each other).

## Assessment

A cross-ecosystem-briefing exercise: candidate must brief a
stakeholder on "the current state of FREK × Wallet integration" using
only the real facts above — eliminatory failure for describing a
working, connected pipeline that does not exist.

## Evidence / certification / mission eligibility

`FRK59.SKILL.*` Skill IDs, reserved once this formation is deepened to
full package. No mission eligibility path exists yet.

## Status

`STATUS = MODULE_CONTENT_DRAFTED` — référentiel and module outline
written this pass; N1/N2 banks, full assessment/rubric, evidence
model, and the 3 guides are a future deepening pass, not performed
here.
