# IOS-07 — Intelligence OS Event-Bus Operator

## Repo truth this formation is built on

Grounded directly in `backend/services/events.py` — this Academy's
real in-process pub/sub bus, the same mechanism that powers
`academy.certification.passed` (BRN-15) and that FRK-54 already
treats as a worked example of the general event-bus/webhook-contract
discipline. Per
`AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`: coverage
`PARTIAL (real events.py pub/sub)`, action `NEW_INTERNAL`, "best-
grounded IOS candidate — build on the real event bus, cross-reference
FRK-54 (same underlying mechanism, already reconciled there) rather
than re-deriving."

**Market-context, never the operating substrate**: `cultureconnectorg/
Cvln-ios-v.1`'s real governance/architecture-freeze corpus (21 ADRs,
7 RFCs, a constitution, protocol specs ADL/AGENT-PROTOCOL/ISA/MCL,
drift-control backend `lib/anchoring.py`/`baselines.py`/
`invariants.py`) is the real, substantial "Intelligence OS" the CVLN
ecosystem actually has — cited here as evidence of real scope and
maturity, never as something this Academy's own `events.py` implements
or connects to. That corpus self-declares its own status as **not**
`DEPLOYED_RUNTIME` — a governance-and-specification layer, not a
running system this Academy could plug into even if it wanted to.

## Prerequisites

None (entry point of IOS in this corpus, alongside BRN-15).

## Objectives

- Operate this Academy's real event bus literacy: what `events.py`
  actually is (in-process pub/sub, not a distributed system), and how
  it powers the one real subscriber chain (`academy.certification.
  passed` → `subscribers.py` → `/academy/certification-passed`).
- Precisely describe what `events.py` is not: no network transport, no
  message durability, no delivery guarantee across process restarts,
  no external webhook surface. It lives entirely inside one running
  Python process.
- Cross-reference FRK-54 (`docs/frk/frk54/REFERENTIAL.md`) explicitly
  — same underlying mechanism, never re-derived twice. A candidate who
  has already passed FRK-54 should recognize `events.py` immediately;
  a candidate arriving here first should be pointed to FRK-54 for the
  fuller market-general treatment of event-bus/webhook design.
- Cite `Cvln-ios-v.1`'s real governance corpus as evidence the
  ecosystem's actual "Intelligence OS" is a governance/architecture-
  freeze layer, self-declared **not** `DEPLOYED_RUNTIME` — never
  implied to be what this Academy's `events.py` is or connects to.
- Explain precisely why conflating the two would be an eliminatory
  error: `events.py` is a small, real, in-process mechanism inside
  this Academy's own codebase; `Cvln-ios-v.1` is a separate,
  substantial, external governance corpus with no observed runtime
  connection to this Academy. Naming both in the same breath as if
  they were one system inflates a two-line pub/sub helper into
  membership in a 21-ADR governance framework it has never joined.
- Explain why this formation exists as `NEW_INTERNAL` rather than
  simply merging into BRN-15 or FRK-54: it isolates the IOS-labeled
  literacy specifically, so a candidate can be assessed on the
  "Intelligence OS" market vocabulary without either inflating the
  internal mechanism or being tested twice on identical content.

## Modules

1. `events.py` in-process pub/sub literacy — what it does, and the
   precise boundary of what it does not do (no network, no
   durability, no external webhook surface).
2. Cross-reference discipline vs. FRK-54 — same mechanism, one
   authoritative treatment; recognize it rather than re-deriving it.
3. Market-context — `Cvln-ios-v.1`'s real governance/protocol-spec
   corpus, cited honestly as a separate, unconnected, non-
   `DEPLOYED_RUNTIME` system.

## Assessment

An event-bus literacy exercise, cross-checked against FRK-54's own
treatment for consistency — eliminatory failure for implying `events.py`
is connected to `Cvln-ios-v.1`'s real governance layer, or for
describing `events.py` itself as distributed, durable, or externally
reachable.

## Evidence / mission eligibility

`IOS07.SKILL.EVENT_BUS_OPERATOR.L1` reserved once deepened. No mission
eligibility path exists today for this domain.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package, deepened this
pass. Never implies `FULLY_COMPLETE` — requires a real human-verified
pass.
