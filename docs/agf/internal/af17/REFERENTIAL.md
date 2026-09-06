# AF-17 — CVLN Agent Factory Client Architecture (internal, narrow)

## Repo truth this formation is built on

Per `AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`:
coverage `PARTIAL (the real architecture is a single client + one
persona — teach that honestly, not an invented taxonomy)`, action
`NEW_INTERNAL (narrow)`. Same grounding as AF-16:
`backend/services/agent_factory.py`.

## Prerequisites

AF-16.

## Objectives

- Teach the real architectural shape of this Academy's agent client:
  **one** client, **one** registered persona — not a taxonomy of agent
  types, roles, or a fleet of specialized agents.
- Explicitly refuse any invented taxonomy (e.g. "planner agent,"
  "critic agent," "tool agent") that does not exist in the real code —
  the honest architecture is deliberately narrow.
- Cite the real external `CVLNAgentfactory`'s far richer architecture
  (multiple agent types via ADL, lifecycle stages) as market-context
  only, per AF-16's own discipline — never as this Academy's actual
  shape.

## Modules

1. Single-client, single-persona architecture literacy.
2. Anti-taxonomy discipline — refusing invented agent-type
   classifications.
3. Market-context comparison (inherited from AF-16).

## Assessment

An architecture-description exercise: candidate must describe this
Academy's real agent architecture without inventing a taxonomy —
eliminatory failure for describing multiple agent types/roles that do
not exist in `agent_factory.py`.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package, deepened this
pass. Never implies `FULLY_COMPLETE`.
