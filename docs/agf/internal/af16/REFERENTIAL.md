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
- Precisely describe what `chat_reply()` does: a real, Claude-backed
  chat transport function, agnostic to which persona is calling it —
  it does not itself select or configure a persona, it simply carries
  a message to the model and returns the response.
- Precisely describe what `mentor_reply()` does: it wraps
  `chat_reply()` with the one real, actually-registered persona
  ("Mentor CVLN") — no other persona exists in the code today.
- Explicitly distinguish this narrow, honest reality from the real
  external `CVLNAgentfactory`'s sophistication — never imply the real
  ADL/gates/lifecycle system is what an Academy operator actually
  touches. `CVLNAgentfactory`'s 7-stage lifecycle, append-only gate
  journal, and event bus with DLQ are real, but they belong to a
  separate, unconnected system.
- Never invent a registry, detachment/mission system, multi-agent
  orchestration, or rollback mechanism — none exists in either system
  as something this Academy can operate. A candidate who proposes such
  a mechanism as a hypothetical future direction must qualify it
  explicitly as such, never as a present capability.
- Explain precisely why conflating this Academy's narrow shim with the
  real `CVLNAgentfactory` would be an eliminatory error: it would
  attribute a 225-file, ~143-route, ADL-governed system's capabilities
  to a two-function chat wrapper, inflating this Academy's actual
  operating surface far beyond what the code supports.

## Modules

1. `chat_reply()` operation — real transport literacy: what it does
   (persona-agnostic chat transport), and what it does not do (no
   persona selection logic of its own).
2. `mentor_reply()` / persona-registration literacy: the one real
   registered persona, and why no others exist in the code today.
3. Market-context comparison — real `CVLNAgentfactory` ADL/gates/
   lifecycle, cited honestly as "what exists in the ecosystem, not
   what this Academy operates."
4. Anti-invention discipline — no registry, mission/detachment system,
   multi-agent orchestration, or rollback mechanism exists; any
   hypothetical proposal must be explicitly qualified as such.

## Assessment

An operator-trace exercise: candidate processes a representative
`chat_reply()`/`mentor_reply()` call sequence and must correctly
distinguish what this Academy's shim actually does from what the real
external `CVLNAgentfactory` does — eliminatory failure for conflating
the two, or for inventing a registry/mission/rollback mechanism, even
as a stated future intention that is not observed in the code.

## Evidence / mission eligibility

`AF16.SKILL.AGENT_FACTORY_OPERATOR.L1` reserved once deepened. No
mission eligibility path exists — no observed integration to operate
against.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package, deepened this
pass. Never implies `FULLY_COMPLETE`.
