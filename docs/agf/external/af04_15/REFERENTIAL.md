# AF-04→15 — AI Agent Engineering Disciplines (external/market)

## Grounding

Per `AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`:
coverage `NONE`, distinctness `DISTINCT_PROFESSION each`, action
`NEW_EXTERNAL`. "Real, current, industry-standard AI-agent-engineering
disciplines... teachable as market knowledge; every CVLN-specific
claim `CAPABILITY_NOT_IMPLEMENTED`."

**Boundary vs. AF-01/02/03**: those three rows are grounded in the real
`ASSISTANT_PERSONAS` persona-as-data pattern — a genuine, small, working
example of one specific engineering discipline (config-driven persona
definition). AF-04→15 is the much broader set of disciplines that
pattern does *not* cover — tool use, memory, multi-agent coordination,
orchestration, HITL, evaluation, observability, security, safety,
reliability, governance, production operations. None of these 12 is
present anywhere in this Academy's code; this cluster is taught
entirely as market-general knowledge, never anchored to a CVLN worked
example the way AF-01/02/03 is.

## Objectives

Teach the 12 real, current, industry-standard AI-agent-engineering
disciplines this candidate cluster names, entirely independent of any
CVLN implementation:

1. **Tool use / function calling** — how an agent selects, invokes, and
   interprets the results of external tools/functions, including
   schema design, error handling, and retry discipline.
2. **Agent memory architecture** — short-term context windows,
   long-term memory stores, retrieval strategies, and the trade-offs
   between them.
3. **Multi-agent coordination** — how multiple agents divide work,
   communicate, and avoid conflicting actions (message passing,
   shared state, negotiation protocols).
4. **Orchestration patterns** — sequencing, branching, and supervising
   agent workflows (single-agent loops vs. supervisor/worker
   topologies vs. pipeline composition).
5. **Human-in-the-loop (HITL) design** — where and how a human review
   or approval gate is inserted into an otherwise autonomous flow, and
   why high-stakes decisions require one.
6. **Agent evaluation methodology** — how to measure whether an agent
   is doing its job well: task success rate, groundedness, safety
   incident rate, and the difference between offline eval and live
   monitoring.
7. **Observability for agentic systems** — tracing an agent's
   reasoning/tool-call chain, logging decisions, and building
   dashboards that let an operator understand *why* an agent did what
   it did.
8. **Agent security** — threat models specific to agents (prompt
   injection, tool-permission escalation, data exfiltration via tool
   calls) and the mitigations the industry uses today.
9. **Agent safety** — bounding what an agent is allowed to do
   (guardrails, permission scopes, kill switches) independent of
   whether an attacker is involved.
10. **Reliability engineering for agents** — retries, idempotency,
    timeout handling, and graceful degradation when a tool or a model
    call fails.
11. **Agent governance** — who owns an agent's behavior in production.
    change management, audit trails, and accountability structures.
12. **Production operations for agentic systems** — deployment,
    versioning, rollback, and incident response practices specific to
    running agents at scale.

Every one of these is real, current market knowledge — but **no CVLN
system implements any of them today**. `agent_factory.py` is a single
chat-transport client with one persona; it has no tool use, no memory,
no multi-agent coordination, no orchestration, no eval harness, no
observability, no governance layer. Every CVLN-specific claim across
these 12 disciplines is explicit `CAPABILITY_NOT_IMPLEMENTED`.

A candidate must also be able to explain *why* citing the real external
`CVLNAgentfactory` (`frekcore/`, 225 files, ~143 routes, Agent
Definition Language v1/v2, 7-stage lifecycle) as market-context proof
that some of these disciplines exist at scale *elsewhere* in the
ecosystem is legitimate — while still never presenting that external
system as something this Academy's own `agent_factory.py` implements
or connects to.

## Modules

One module per discipline (12 total), each: concept fundamentals →
industry-standard patterns → explicit CVLN-gap statement citing
`agent_factory.py`'s real, narrow, single-persona chat-transport
nature as the contrasting reality.

## Assessment

A discipline-literacy exam covering all 12 areas, graded against real
industry practice, with an eliminatory check on any claim that
`agent_factory.py` or any other CVLN system implements one of them —
including a claim phrased as "planned" or "in progress" when no such
work is observed in the repository.

## Evidence / mission eligibility

`AF0415.SKILL.AGENT_ENGINEERING_DISCIPLINES.L1` reserved once
deepened, covering all 12 AF-04→15 rows. No mission eligibility path
exists today for this domain.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package, deepened this
pass. Never implies `FULLY_COMPLETE`.
