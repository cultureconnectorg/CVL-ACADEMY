# docs/agf/ — Agent Factory / Intelligence OS / Brain / Command Center / Laurentia Corpus (W6 Wave 6)

```
Domain: Agent Factory (AF-01→25), AF-X (9), Laurentia (LAU-01→10),
Intelligence OS (IOS-01→25), CVLN Brain (BRN-01→15), Command Center
(CMD-01→15), Intelligent Operations (SYS-01→10) — 109 rows total.
Reconciliation source: docs/cvln_academy_master/20_EXTERNAL/
                        AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_
                        RECONCILIATION.md (0 rejected, Wave 2
                        repo-truth correction already applied).
```

## Mandatory structural separation (Founder instruction, 2026-09-06)

This corpus keeps the **EXTERNAL/market layer** and the **INTERNAL
CVLN layer** in two physically separate folders, never blended:

- **`external/`** — real, current, industry-standard AI-agent/SRE/
  executive-assistant disciplines, teachable independent of any CVLN
  implementation. Every CVLN-specific claim inside these formations is
  explicitly `CAPABILITY_NOT_IMPLEMENTED` — never softened.
- **`internal/`** — CVLN-specific literacy, grounded **only** in the
  real, directly-audited external CVLN repos this session already
  found and read (`frekcore/CVLNAgentfactory`, `cultureconnectorg/
  Cvln-ios-v.1`, `cultureconnectorg/Laurent.ia`, `metacvln-spec/
  MetaCVLN`) plus this Academy's own real, thin shims
  (`agent_factory.py`, `ai_assistant.py`, `events.py`,
  `certification/service.py`). **Never extrapolated from generic
  AI-agent textbook knowledge** — every claim here traces to a named
  file/route/schema already directly read this session.

## Repo-truth table (internal layer's real grounding)

| Real capability | Repo | File/route | Grounds |
|---|---|---|---|
| `chat_reply()`, `mentor_reply()` — real Claude-backed chat, one registered persona | `CVL-ACADEMY` (self) | `backend/services/agent_factory.py` | AF-16 |
| `ASSISTANT_PERSONAS` — persona-as-data config, not code branches | `CVL-ACADEMY` (self) | `backend/services/ai_assistant.py` | AF-16, AF-17 |
| In-process pub/sub event bus, powers `academy.certification.passed` | `CVL-ACADEMY` (self) | `backend/services/events.py`, `backend/certification/service.py:140` | IOS-07, BRN-15 |
| Real Agent Definition Language v1/v2 (`AGT-\d{3}` ids, semver, 7-stage lifecycle `Draft→Prototype→Alpha→Beta→Production→Maintenance→Archive`, `allowed_transitions()`), gates (`GATE_LEVELS`, `CRITICAL_ACTIONS`, append-only journal), event bus (DLQ+replay-spool), model/provider router | `frekcore/CVLNAgentfactory` | `backend/adl_schema.py`, `schemas/adl_v2_schema.json`, `gate_routes.py`, `provider_layer.py` | AF-16/17 (market-context, never operating substrate), AF-X-03 |
| Real governance/architecture-freeze corpus: 21 ADRs, 7 RFCs, a constitution, protocol specs (ADL/AGENT-PROTOCOL/ISA/MCL), drift-control backend | `cultureconnectorg/Cvln-ios-v.1` | `decisions/`, `CVLN-CONSTITUTION-v1.md`, `lib/anchoring.py`/`baselines.py`/`invariants.py` | IOS-07 (market-context) |
| Real `/command-center/overview` + `/command-center/timeline` routes (confirmed by direct grep, lines 184/221), Ed25519-signed event bus, runtime-state (normal/degraded/critical), `/brain/ask` | `metacvln-spec/MetaCVLN` | `backend/server.py` | CMD-15 (flagship, real external maturity `PARTIAL`), BRN-15 (market-context) |
| Real multi-service orchestrator (agents/circuit-breaker/event-bus/signals), `cvl_brain*.py`, bridges (`frekcore_bridge.py`, `kiltikonet_bridge.py`, `labelos_bridge.py`) | `cultureconnectorg/Laurent.ia` | `orchestrator/`, `services/` | AF-X-03, BRN-15 (market-context) |

**Standing fact, restated in every internal-layer formation:** none of
these four external repos shows any observed integration with
`CVL-ACADEMY` itself — no shared auth, no cross-repo API calls, no
shared database. `MetaCVLN`'s own audit states plainly: "nothing
audited depends on it." Real, substantial, testable architecture
exists in the CVLN ecosystem — **never** inflated into a claim of
production integration with this Academy.

## Cross-domain contamination guard (restated)

`fms-os/fms`'s own `/os/command-center` route is a studio-operations
KPI dashboard, unrelated to CVLN's real `/command-center/overview`/
`/timeline` in `MetaCVLN` — two different systems, never conflated,
even though CMD-01→14's market-general SRE curriculum must also never
be confused with either.

## Status (post-deepening pass, Rail 1 priority 2)

| Layer | Formations | Depth |
|---|---|---|
| `external/` | 5 cluster referentials covering 53 rows (AF-01→15, LAU-01→10, BRN-01→14, CMD-01→14) | `PACKAGE_COMPLETE`, all 5, deepened this pass |
| `internal/` | 6 referentials (AF-16, AF-17, AF-X-03, BRN-15, IOS-07, CMD-15) | `PACKAGE_COMPLETE`, all 6 (CMD-15 flagship from a prior pass; AF-16/17/AF-X-03/BRN-15/IOS-07 deepened this pass) |
| `EXTEND_EXISTING_NOTE.md` | AF-22 (→ `AUTHORIZATION_MODEL.md`), SYS-01→10 (→ `MISSIONS_PIPELINES.md`) | No separate formation, 11 rows, untouched |
| `BLOCKED_CANDIDATES.md` | AF-18/19/20/21/23/25, AF-24, AF-X-01/02/04/05/06/07/08, AF-X-09, IOS-01→06/08→25 | `BLOCKED_PRODUCT_DEPENDENCY`, 39 rows, `GAP.md`-style, no invented content, untouched |

**53 + 6 + 1 + 39 + 10 = 109.** All 109 rows accounted for. 59/109
`PACKAGE_COMPLETE` (all 5 external clusters + all 6 internal
formations, i.e. 53 + 6 rows), 39/109 `BLOCKED_PRODUCT_DEPENDENCY`
(untouched, genuine), 11/109 `EXTEND_EXISTING` (AF-22 + SYS-01→10, no
separate file, untouched, genuine).

Per Rail 1's directive — "ne pas chercher 100% `PACKAGE_COMPLETE`
artificiellement : conserver `BLOCKED`, `NEEDS_EXPERT_REVIEW`,
`EXTEND_EXISTING` quand c'est la vérité" — the 39 `BLOCKED` and 11
`EXTEND_EXISTING` rows were **not** touched or reclassified in this
pass; only the 59 rows already scoped as buildable (`NEW_EXTERNAL` /
`NEW_INTERNAL` in the source reconciliation) were deepened from
`MODULE_CONTENT_DRAFTED` to `PACKAGE_COMPLETE`.

**Canonical state — never summarized otherwise:** this corpus reaches
`PACKAGE_COMPLETE` on its **59 buildable rows** (54% of the domain).
It is **not** `FULLY_COMPLETE` as a domain, and never will be until a
real human candidate pass exists — `PACKAGE_COMPLETE` here means a
full canonical package (référentiel + banques + assessment/rubric +
evidence model + 3 guides + integration note) exists and is
repo-truth-grounded or explicitly market-general, nothing more. The 50
non-`PACKAGE_COMPLETE` rows (39 `BLOCKED` + 11 `EXTEND_EXISTING`)
remain genuinely blocked or folded, per the reconciliation's own
verdict — not a gap in this pass's coverage.
