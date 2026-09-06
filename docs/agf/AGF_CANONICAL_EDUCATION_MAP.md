# Agent Factory / IOS / Brain / CMD / Laurentia — Canonical Education Map

## Shared competency skeleton

Every formation follows `PROFESSIONAL_ROLE → ACTIVITIES →
COMPETENCIES`, grounded either in a real, named industry-standard
discipline (`external/`) or in a named file/route/schema from one of
the 4 directly-audited real external CVLN repos plus this Academy's
own real thin shims (`internal/`).

## Dependency graph

```
external/ (market-general, independent of CVLN implementation)
  af01_03 (grounded partially — real ai_assistant.py persona pattern)
  af04_15 (pure market-general AI-agent-engineering disciplines)
  lau01_10 (AI executive-assistant/chief-of-staff market category)
  brn01_14 (AI/ML disciplines: context/retrieval/reasoning/planning)
  cmd01_14 (SRE/NOC/incident-command disciplines)

internal/ (CVLN-specific, grounded on real audited external repos)
  af16 (Academy operator: chat/persona/mentor — agent_factory.py)
    └── af17 (narrow client architecture, same grounding)
  afx03 (Academy skill/cert engine × agent qualification bridge —
         real CVLNAgentfactory ADL as market-context)
  brn15 (academy.certification.passed touchpoint)
  ios07 (events.py pub/sub — cross-ref FRK-54, Cvln-ios-v.1 protocol
         specs as market-context)
  cmd15 (flagship — real MetaCVLN /command-center/overview+/timeline,
         PARTIAL maturity, external, not yet Academy-operable)

EXTEND_EXISTING (no separate formation)
  af22 → 00_GOVERNANCE/AUTHORIZATION_MODEL.md
  sys01_10 → 80_MISSIONS/MISSIONS_PIPELINES.md

BLOCKED_PRODUCT_DEPENDENCY (BLOCKED_CANDIDATES.md, no invented content)
  af18/19/20/21/23/25, af24, afx01/02/04/05/06/07/08, afx09,
  ios01_06/08_25
```

## Boundary notes (mandatory cross-reference discipline)

- **`external/af01_03` vs `internal/af16,af17`:** af01-03 teach
  market-general AI-agent-engineering principles that happen to be
  *illustrated* by this Academy's real `ai_assistant.py` persona-as-
  data pattern; af16/af17 teach the *operational* reality of running
  this Academy's own agent client — a different altitude (concept
  literacy vs. operator competency), never merged into one formation.
- **`internal/af16,af17` vs the real `CVLNAgentfactory`:** the real
  external Agent Factory (ADL, gates, lifecycle) is far more
  sophisticated than this Academy's own shim. AF-16/17 teach the
  honest, narrow reality of the shim as the *only* thing an Academy
  operator can actually work with today — the real `CVLNAgentfactory`
  is cited as market-context/comparison, **never** as if it were the
  operating substrate a candidate could touch.
- **`internal/cmd15` vs `external/cmd01_14`:** CMD-15 teaches literacy
  of the one real, external CVLN Command Center (`MetaCVLN`'s
  `/command-center/overview`/`/timeline`) — CMD-01→14 teach
  market-general SRE/incident-command discipline, entirely
  independent of whether CVLN has a Command Center at all. Never
  merged.
- **`internal/cmd15` vs `fms-os/fms`'s own `/os/command-center`:**
  different systems, same name — restated per the standing
  cross-domain-contamination guard.
- **`internal/ios07` vs `external` AI/ML/orchestration content:**
  IOS-07 teaches the one real, working piece of "Intelligence OS" this
  Academy has (`events.py`) — cross-referenced to FRK-54 (same
  underlying mechanism, already reconciled there), never re-derived.
- **`internal/afx03` vs `BLOCKED_CANDIDATES.md`'s other AF-X bridges:**
  AF-X-03 is buildable because *both* sides are real (Academy's own
  skill/certification engine, and the real external Agent Factory
  concept as context) — the other 7 blocked bridges have at least one
  side entirely unimplemented or stub-only.
- **`SYS-01→10` vs `80_MISSIONS/MISSIONS_PIPELINES.md`:** identical
  10-stage pipeline, already documented there — never rebuilt as 10
  separate formations restating the same stages.

## Anti-footprint verification (mandatory before certifying anything in `internal/`)

Verify every claim against the actual file/route/schema cited in the
formation's own `REFERENTIAL.md` — never against a memorized summary
of "what an agent factory usually has." The real `CVLNAgentfactory`'s
own `adl_schema.py` (directly read this session) is the canonical
example: its 7-stage lifecycle and `allowed_transitions()` function
are real, specific, and citable — never approximate them from generic
agent-lifecycle theory.

## Certification / mission eligibility doctrine

Same N1/N2/assessment structure as `CERTIFICATION_MODEL.md`. No
mission eligibility exists for any `internal/` formation beyond
literacy — none of the 4 real external repos shows any observed
integration with this Academy, so no mission can depend on one.
