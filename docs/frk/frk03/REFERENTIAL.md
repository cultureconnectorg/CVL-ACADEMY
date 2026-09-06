# FRK-03 — FREK Operator

## Repo truth this formation is built on

Grounded in the real, cross-module usage patterns of `frek_core.py`'s
public methods (`emit_signal`, `mint_frek_id`, `resolve_stade`) as
already deployed across `docs/kor/`, `docs/klt/`, `docs/fms/` — per
`FREK_01_75_RECONCILIATION.md`'s own verdict: curriculum coverage
`NONE (curriculum) / PARTIAL (repo)`, occupational distinctness
`DISTINCT_OPERATOR_ROLE`, action `NEW_INTERNAL`, "buildable now."

## Prerequisites

FRK-01, FRK-58.

## Objectives

A FREK Operator reasons about how `frek_core.py`'s methods are
actually invoked and monitored *in practice* across this Academy's own
pedagogical modules — a distinct, day-to-day operational competency
from FRK-58's integration-architecture literacy:

- Reading a `FREK_PROOF_MAPPING` header on a real module (e.g. any
  `docs/kor/korXX/modules/*.md`) and correctly identifying which
  `VALID_SIGNALS` value(s) it references.
- Recognizing that a header's presence documents an *intended*
  signal-emission point, never a verified/anchored proof
  (`READY_FOR_FREK_PROOF = FALSE` everywhere — see FRK-56).
- Operating the counter/signal side-effects `emit_signal()`/
  `mint_frek_id()` produce (`db.frek_signals` inserts,
  `db.users.signals.*` increments, `db.counters` sequence) without
  ever asserting a remote mirror succeeded (best-effort, silently
  swallowed on failure).

## Modules

1. **FREK_PROOF_MAPPING literacy** — reading real module headers and
   mapping them to the real `VALID_SIGNALS` set.
2. **Side-effect operation** — grounded in `emit_signal()`'s real
   database writes (`db.frek_signals`, `db.users.signals.*`) and
   `mint_frek_id()`'s real counter mechanics (`db.counters`).
3. **Remote-mirror discipline** — never asserting a best-effort remote
   mirror succeeded; treating `is_remote_enabled()` as the sole ground
   truth for whether any remote call is even attempted.

## Assessment

An operator log-reading exercise: candidate is given a representative
set of `FREK_PROOF_MAPPING` headers plus a signal-emission trace and
must correctly map each to real signal types and side effects — graded
against the real code and headers, never an invented monitoring
dashboard.

## Evidence / certification / mission eligibility

`FRK03.SKILL.*` Skill IDs, reserved once this formation is deepened to
full package. No mission eligibility path exists yet.

## Status

`STATUS = MODULE_CONTENT_DRAFTED` — référentiel and module outline
written this pass; N1/N2 banks, full assessment/rubric, evidence
model, and the 3 guides are a future deepening pass, not performed
here.
