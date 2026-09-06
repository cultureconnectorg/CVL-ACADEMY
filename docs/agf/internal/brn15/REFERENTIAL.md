# BRN-15 — CVLN Brain Touchpoint Operator

## Repo truth this formation is built on

Grounded directly in the one real Brain touchpoint in this Academy:
`backend/certification/service.py:140` emits `academy.certification.
passed` via `backend/services/events.py`'s in-process pub/sub, and
`subscribers.py` relays it to `/academy/certification-passed`. Per
`AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`: coverage
`PARTIAL (real academy.certification.passed touchpoint)`, action
`NEW_INTERNAL`, "buildable now — reuse the boundary language already
established in `docs/kor/kor12/` and `FREK_01_75_RECONCILIATION.md`
(FRK-58/60) verbatim... converge, don't re-derive."

**Market-context, never the operating substrate**: `metacvln-spec/
MetaCVLN`'s real `/brain/ask` interface (a genuine Brain-interface
route, directly grep-confirmed this session) is cited as evidence a
real CVLN Brain concept exists in the ecosystem — never as something
this Academy's `academy.certification.passed` event is wired to.

## Prerequisites

IOS-07 (shares the same event-bus mechanism).

## Objectives

- Operate the one real Brain touchpoint this Academy has: a single
  event (`academy.certification.passed`) emitted on certification
  success, relayed to one route.
- Never claim this constitutes a reasoning/context/memory/knowledge
  engine — it is a single event subscription, nothing more.
- Cite `MetaCVLN`'s real `/brain/ask` as evidence the broader "CVLN
  Brain" concept is real elsewhere in the ecosystem, never as this
  Academy's own operating capability.

## Modules

1. `academy.certification.passed` event literacy.
2. Single-touchpoint discipline — never inflate into a reasoning
   engine.
3. Market-context — `MetaCVLN`'s real `/brain/ask` cited honestly.

## Assessment

A touchpoint-literacy exercise: candidate traces the event from
`certification/service.py:140` through `events.py` to `subscribers.py`
— eliminatory failure for claiming a reasoning engine exists.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.
