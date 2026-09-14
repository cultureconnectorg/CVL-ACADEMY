# FRK-01 — FREK Foundations & Cultural Trust Infrastructure (umbrella, flagship)

## Repo truth this formation is built on

Grounded directly in the real, re-read `backend/services/frek_core.py`
(142 lines, `FrekCoreClient` class) — per
`FREK_01_75_RECONCILIATION.md`'s own verdict: curriculum coverage
`NONE`, occupational distinctness `DISTINCT_PROFESSION`, action
`NEW_EXTERNAL`, "entry-point formation, same role as KOR-01/KLT-01
baseline. Highest priority to build first — everything else sequences
off it." Full real contract:

| Method | Real behavior |
|---|---|
| `mint_frek_id()` | Remote-first (`POST /mint`, `FREK_CORE_BASE_URL` env-gated), local fallback: atomic `db.counters` increment, format `FREK-{seq:03d}` |
| `emit_signal(user_id, signal, meta)` | Only 8 real signal types accepted (`VALID_SIGNALS`); silently no-ops on any other value; writes `db.frek_signals` + increments `db.users.signals.<signal>`; best-effort remote mirror |
| `issue_proof(user_id, kind, meta)` | Remote-first, local fallback = random UUID (`PROOF-{uuid4().hex[:10].upper()}`) — no crypto, no chain-of-custody, no timestamp anchoring |
| `resolve_stade(cc_credits)` | Maps a credit count to 1 of 6 named tiers via `STADE_THRESHOLDS`, descending-order check |
| `is_remote_enabled()` | Returns `bool(FREK_CORE_BASE_URL)` — `False` by default |

## Prerequisites

None (entry-point formation for the entire FRK-01→75 domain).

## Objectives

FREK Foundations & Cultural Trust Infrastructure is the entry-point
formation into the FREK domain — same structural role as KOR-01/KLT-01
in their own domains — establishing the real system map before any
specialization (FRK-58 integration architecture, FRK-03/06/13/68
operator paths, FRK-56/59 cross-ecosystem bridges) is attempted:

- System-map literacy: naming the 5 real public methods, their
  remote/local fallback shape, and what each one actually returns —
  never inventing a 6th method or a capability none of the five have
  (no direct-credit route, no transfer, no hold/reservation state).
- Signal-vocabulary discipline: the 8 real `VALID_SIGNALS` values
  (`FREK-TIME/WORK/SCORE/LINK/CERT/CONTRIB/SHARE/MISSION`) as the
  complete, closed vocabulary — any other string is silently rejected,
  never processed.
- Progression-tier literacy: the 6 real named tiers
  (`graine→pousse→racine→branches→arbre→forêt`) and their real credit
  thresholds (0/10/50/100/150/300).
- Honest-capability discipline: `issue_proof()`'s stub nature (random
  UUID, zero cryptographic guarantee) is foundational knowledge every
  downstream FRK formation depends on — never softened here.

## Modules

1. **System map** — the 5 real public methods of `FrekCoreClient`,
   their remote-first/local-fallback shape, and what a candidate must
   never invent (direct-credit route, transfer, hold/reservation).
2. **Signal vocabulary** — the 8 real `VALID_SIGNALS` values and the
   silent-rejection behavior for anything else.
3. **Progression tiers** — the 6 real named tiers and their real
   credit thresholds, checked in descending order.
4. **Honest proof-engine reality** — `issue_proof()`'s stub nature,
   as the foundational fact every specialization in this domain must
   carry forward, never contradict.

## Assessment

A system-map exam: candidate must reproduce, from memory verified
against the real file, the 5 methods, the 8 signal values, the 6
progression tiers with thresholds, and correctly state that
`issue_proof()` produces no cryptographic guarantee — graded against
the real code, zero tolerance for an invented method, signal value, or
tier.

## Evidence / certification / mission eligibility

`FRK01.SKILL.*` Skill IDs, reserved in `70_EVIDENCE/
EVIDENCE_ARCHITECTURE.md`. Mission eligibility requires literacy of the
real `frek_core.py` contract — never live production write access to
`db.frek_signals`/`db.counters`/`db.users` in production.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package (référentiel +
N1/N2 + assessment/rubric + evidence model + 3 guides + integration
note), deepened this pass as the FREK wave's flagship. Never implies
`FULLY_COMPLETE` — no real candidate has been assessed yet.
