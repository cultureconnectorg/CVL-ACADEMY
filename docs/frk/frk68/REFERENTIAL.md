# FRK-68 — FREK Auditor

## Repo truth this formation is built on

Grounded in real, inspectable audit surfaces across two systems,
directly re-verified this session — per
`FREK_01_75_RECONCILIATION.md`'s own verdict: curriculum coverage
`NONE (curriculum) / PARTIAL (repo)`, occupational distinctness
`DISTINCT_INTERNAL_ROLE`, action `NEW_INTERNAL`, "buildable now at a
procedural level":

- This Academy's `db.frek_signals` (written by `emit_signal()`, every
  insert carries `user_id`, `signal`, `meta`, `ts`).
- Good Mood's two outbox tables (`db.frek_outbox` via `frek_service.py`,
  `db.wallet_outbox` via `wallet_service.py`), each monitorable via
  `GET /admin/outbox/frek-id` / `GET /admin/outbox/wallet`.

## Prerequisites

FRK-01, FRK-58, FRK-03.

## Objectives

A FREK Auditor operates at a **procedural** level — reading real audit
surfaces, distinguishing them correctly, never implying they form one
unified audit trail across systems they do not actually connect:

- `db.frek_signals` audit literacy: reading a signal-emission record
  and correctly attributing it to this Academy's own `frek_core.py`,
  never to any other system's FREK client.
- Outbox status literacy (Good Mood): distinguishing `delivered` vs.
  `pending` vs. `failed` entries in both outbox tables, and the real
  5-attempt retry-backoff schedule (`[30s, 2m, 10m, 1h, 6h]`) each one
  follows before terminal failure.
- **Three-system discipline**: `db.frek_signals` (this Academy),
  `db.frek_outbox` (Good Mood→external FREK-ID), and `db.wallet_outbox`
  (Good Mood→external Wallet) are three separate real tables in
  separate systems — an auditor never merges them into a single
  narrative.

## Modules

1. **`db.frek_signals` audit literacy** — grounded in the real
   `emit_signal()` insert shape.
2. **Outbox status & retry-schedule literacy** — grounded in Good
   Mood's real `frek_service.py`/`wallet_service.py` behavior (same
   pattern, distinct channels), already cited in `docs/gmd/gmd31`,
   `gmd32`.
3. **Three-system discipline** — explicit written distinction of the
   three separate real tables, never merged into one audit trail.

## Assessment

An audit-trail reading exercise: candidate is given representative
entries from all three tables and must correctly attribute each to its
real system and status, and flag any attempt to present them as one
connected trail as an error — graded against the real behavior.

## Evidence / certification / mission eligibility

`FRK68.SKILL.*` Skill IDs, reserved once this formation is deepened to
full package. No mission eligibility path exists yet.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package (référentiel +
N1/N2 + assessment/rubric + evidence model + 3 guides + integration
note), deepened this pass. Never implies `FULLY_COMPLETE` — no real
candidate has been assessed yet.
