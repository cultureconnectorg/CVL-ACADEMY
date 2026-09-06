# AF-16 — CVLN Agent Factory Operator (internal, Academy-grounded)

## Repo truth this formation is built on

Grounded directly in `backend/services/agent_factory.py` (this
Academy's own real code) — `chat_reply()` (real Claude-backed chat
transport, persona-agnostic) and `mentor_reply()` (the one real
registered persona, "Mentor CVLN"). Per
`AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`: coverage
`PARTIAL (real chat/persona/mentor operations)`, action `NEW_INTERNAL`,
"buildable now."

**Market-context, never the operating substrate**: the real, external
`frekcore/CVLNAgentfactory` (225 files, ~143 routes, real Agent
Definition Language v1/v2 — `AGT-\d{3}` ids, 7-stage lifecycle
`Draft→Prototype→Alpha→Beta→Production→Maintenance→Archive`,
`allowed_transitions()`, gates with append-only journal, event bus
with DLQ, model/provider router) is a real, substantial, far more
sophisticated system than this Academy's own shim — cited here for
market-context comparison only. No observed integration exists between
it and `CVL-ACADEMY`.

## Prerequisites

None (entry point of the internal layer).

## Objectives

- Operate this Academy's own real, narrow agent-factory client:
  `chat_reply()` (persona-agnostic transport) and `mentor_reply()`
  (the one registered persona).
- Explicitly distinguish this narrow, honest reality from the real
  external `CVLNAgentfactory`'s sophistication — never imply the real
  ADL/gates/lifecycle system is what an Academy operator actually
  touches.
- Never invent a registry, detachment/mission system, multi-agent
  orchestration, or rollback mechanism — none exists in either system
  as something this Academy can operate.

## Modules

1. `chat_reply()` operation — real transport literacy.
2. `mentor_reply()` / persona-registration literacy.
3. Market-context comparison — real `CVLNAgentfactory` ADL/gates/
   lifecycle, cited honestly as "what exists in the ecosystem, not
   what this Academy operates."

## Assessment

An operator-trace exercise: candidate processes a representative
`chat_reply()`/`mentor_reply()` call sequence and must correctly
distinguish what this Academy's shim actually does from what the real
external `CVLNAgentfactory` does — eliminatory failure for conflating
the two.

## Evidence / mission eligibility

`AF16.SKILL.*` reserved once deepened. No mission eligibility path
exists — no observed integration to operate against.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.
