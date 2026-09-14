# FRK-58 — FREK × CVLN Academy Integration

## Repo truth this formation is built on

Grounded directly in `backend/services/frek_core.py` (142 lines,
re-read in full this session) — per `FREK_01_75_RECONCILIATION.md`'s
own verdict, this formation **is** the entire real FREK footprint in
`cultureconnectorg/CVL-ACADEMY`, the best-grounded of all 75
candidates in the domain. `FrekCoreClient` class: `mint_frek_id()`,
`emit_signal()`, `issue_proof()`, `resolve_stade()`,
`is_remote_enabled()` — remote-first (`FREK_CORE_BASE_URL` env-gated)
with a local fallback on every method.

## Prerequisites

FRK-01 (Foundations).

## Objectives

FREK × CVLN Academy Integration is the professional practice of
operating and reasoning about *this specific* integration — not FREK
in the abstract, and not any other CVLN product's FREK client:

- Remote/local fallback literacy: every method attempts a remote call
  first (`_remote_post`, 8s timeout, best-effort — failures are
  swallowed silently) and falls back to a local implementation that
  fully substitutes for it. `is_remote_enabled()` simply checks whether
  `FREK_CORE_BASE_URL` is set (it is not, by default).
- Signal-emission discipline: `emit_signal()` silently no-ops for any
  signal not in the real 8-value `VALID_SIGNALS` set — a candidate must
  recognize this as **silent rejection**, not an error.
- Progression-tier literacy: `resolve_stade()` maps a `cc_credits`
  count to one of 6 real named tiers via `STADE_THRESHOLDS`
  (graine=0, pousse=10, racine=50, branches=100, arbre=150,
  foret=300) — checked in descending order.

## Modules

1. **Remote/local fallback pattern** — grounded in `_remote_post()`,
   `is_remote_enabled()`; recognizing "remote-first, silent local
   fallback" as the integration's actual behavior today.
2. **Signal emission & validation** — grounded in `VALID_SIGNALS` (8
   real values) and `emit_signal()`'s silent no-op on an invalid
   signal.
3. **Progression-tier resolution** — grounded in `STADE_THRESHOLDS`
   (6 real tiers, descending-order check logic).

## Assessment

A trace-reading exercise: candidate is given a representative
`emit_signal`/`mint_frek_id`/`resolve_stade` call sequence (valid and
invalid inputs mixed) and must predict the real behavior — including
correctly identifying silent no-ops and fallback paths — graded
against the real code, never an invented error-handling behavior.

## Evidence / certification / mission eligibility

`FRK58.SKILL.*` Skill IDs, reserved once this formation is deepened to
full package. Mission eligibility requires literacy of the real
`frek_core.py` contract — never live production write access to
`db.frek_signals`/`db.counters`/`db.users` in production.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package (référentiel +
N1/N2 + assessment/rubric + evidence model + 3 guides + integration
note), deepened this pass. Never implies `FULLY_COMPLETE` — no real
candidate has been assessed yet.
