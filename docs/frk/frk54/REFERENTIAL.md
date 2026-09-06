# FRK-54 — Event Bus, Webhooks & Integration Contracts

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE (curriculum) /
PARTIAL (repo, services/events.py)`, distinctness `DISTINCT_
PROFESSION`, action `NEW_EXTERNAL`. Real, generic in-process pub/sub
exists in this repo (`events.py`, powers
`academy.certification.passed`) — usable as a genuine (small) worked
example, but it is Academy's own event bus, not a FREK one; boundary
must be explicit.

## Objectives

- Teach real event-bus/webhook/integration-contract design as an
  industry-general discipline.
- Use this Academy's own real `events.py` in-process pub/sub as a
  genuine, small worked example of the pattern — explicitly stating it
  is this Academy's own internal bus, not a FREK-branded system, and
  has no webhook/external-integration surface today.

## Modules

1. Event-bus design fundamentals.
2. Webhook/integration-contract patterns (market-general).
3. Worked-example discipline — `events.py` as illustration only, never
   implied to be FREK infrastructure.

## Assessment

A design exercise using `events.py` as a worked case, graded against
real event-bus practice.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.
