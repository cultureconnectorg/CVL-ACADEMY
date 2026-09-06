# FRK-28 — Event Registry & Event-Driven Provenance

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE (curriculum) /
PARTIAL (repo)`, distinctness `DISTINCT_PROFESSION`, action
`NEW_EXTERNAL`. Cross-reference `backend/services/events.py` (real,
but Academy-internal pub/sub, not a provenance event registry) — do
not conflate.

## Objectives

- Teach real event-driven provenance architecture as an industry
  discipline (event sourcing, provenance-event registries).
- Use this Academy's own real `events.py` (an in-process pub/sub bus
  powering `academy.certification.passed`) as a worked, small,
  *non-provenance* example of event-driven architecture — explicitly
  distinguishing it from a real provenance event registry, which does
  not exist anywhere in this repo.

## Modules

1. Event-driven architecture fundamentals.
2. Provenance-event registry design (market-general).
3. Boundary discipline vs. this Academy's own `events.py` (real, but
   not a provenance registry).

## Assessment

A design exercise graded against real event-driven architecture
practice, with an eliminatory check on conflating `events.py` with a
provenance registry.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.
