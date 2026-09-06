# AF-04→15 — AI Agent Engineering Disciplines (external/market)

## Grounding

Per `AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`:
coverage `NONE`, distinctness `DISTINCT_PROFESSION each`, action
`NEW_EXTERNAL`. "Real, current, industry-standard AI-agent-engineering
disciplines... teachable as market knowledge; every CVLN-specific
claim `CAPABILITY_NOT_IMPLEMENTED`."

## Objectives

Teach the 12 real, current, industry-standard AI-agent-engineering
disciplines this candidate cluster names, entirely independent of any
CVLN implementation:

1. Tool use / function calling.
2. Agent memory architecture.
3. Multi-agent coordination.
4. Orchestration patterns.
5. Human-in-the-loop (HITL) design.
6. Agent evaluation methodology.
7. Observability for agentic systems.
8. Agent security.
9. Agent safety.
10. Reliability engineering for agents.
11. Agent governance.
12. Production operations for agentic systems.

Every one of these is real, current market knowledge — but **no CVLN
system implements any of them today**. `agent_factory.py` is a single
chat-transport client with one persona; it has no tool use, no memory,
no multi-agent coordination, no orchestration, no eval harness, no
observability, no governance layer. Every CVLN-specific claim across
these 12 disciplines is explicit `CAPABILITY_NOT_IMPLEMENTED`.

## Modules

One module per discipline (12 total), each: concept fundamentals →
industry-standard patterns → explicit CVLN-gap statement.

## Assessment

A discipline-literacy exam covering all 12 areas, graded against real
industry practice, with an eliminatory check on any claim that
`agent_factory.py` or any other CVLN system implements one of them.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package, deepened this
pass. Never implies `FULLY_COMPLETE`.
