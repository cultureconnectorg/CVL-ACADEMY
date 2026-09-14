# CMD-15 — CVLN Command Center Literacy Operator (internal, flagship)

## Repo truth this formation is built on

Grounded directly in `metacvln-spec/MetaCVLN` (default branch `main`,
commit `b36a893049576ce9cf00da778efd4724fb469670` — audited this
session, `REPO_REGISTRY.md`): a real FastAPI backend, 1,611 lines
(`backend/server.py`), ~50 routes, including **directly grep-confirmed
real routes** `/command-center/overview` (line 184) and
`/command-center/timeline` (line 221). Also real in the same backend:
JWT+bcrypt RBAC (admin/cfo/hr_lead/ops_lead/legal_lead/employee),
registry/entities/agents/capabilities/decisions, an Ed25519-signed
event bus, runtime-state tracking (`normal`/`degraded`/`critical`),
learning-proposals, a `/brain/ask` interface, notarization,
domain-overviews (finance/people/legal/ops/knowledge), and outbound
adapters (`laurentia`, `labelos`, `wallet` — the wallet adapter
self-reports HTTP 404 upstream, honestly).

Per `AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`'s own
Wave 2 correction: CMD-15's maturity was upgraded **in place**, on
this direct evidence, from `BLOCKED_PRODUCT_DEPENDENCY` ("no real CVLN
Command Center exists to operate") to `NEW_INTERNAL`, `PARTIAL` — "real
`/command-center/overview`/`/timeline` exist in `MetaCVLN`, external to
this Academy, not yet buildable as an Academy-side operator
qualification without a wired integration — register as
`PRODUCT_DEPENDENCY` still, but no longer `BLOCKED` on 'nothing
exists.'" **This is the one row in the entire 109-row cluster whose
maturity a real, newly-audited repo directly changed this session —
chosen as this wave's flagship for exactly that reason.**

## Cross-domain contamination guard

`fms-os/fms`'s own `/os/command-center` route (a studio-operations KPI
dashboard: `projects_active`, `bookings_upcoming`, etc. — see
`docs/fms/fms18/REFERENTIAL.md`) is a **completely different system**
from `MetaCVLN`'s real `/command-center/overview`/`/timeline` — same
words, unrelated products, never conflated. Neither is CMD-01→14's
market-general SRE/ICS curriculum (`docs/agf/external/cmd01_14/`),
which is independent of whether either Command Center exists.

## Prerequisites

None (entry point of the Command Center literacy track).

## Objectives

- Read and correctly interpret the real `/command-center/overview` and
  `/command-center/timeline` route outputs from `MetaCVLN` — the only
  real, named, external CVLN Command Center this Academy has any
  evidence of.
- Correctly state the maturity boundary: this is real, working
  architecture in `MetaCVLN` (not a mockup, not a name in a registry
  stub) — **and** it has zero observed integration with
  `CVL-ACADEMY`, self-declared **not** `DEPLOYED_RUNTIME` per
  `MetaCVLN`'s own audit ("nothing audited depends on it").
- Never claim this Academy can operate the real Command Center — no
  wiring exists; certification here is literacy of a real external
  system, nothing more.
- Distinguish this real, specific system from both `fms-os/fms`'s
  unrelated route (studio ops) and the market-general SRE/ICS
  discipline taught in `external/cmd01_14`.

## Modules

1. **`/command-center/overview` literacy** — real route, real
   response shape (registry/entities/agents/capabilities/decisions
   summary), read directly against `MetaCVLN`'s own backend.
2. **`/command-center/timeline` literacy** — real route, real
   event-bus-derived timeline (Ed25519-signed events), runtime-state
   tracking (`normal`/`degraded`/`critical`).
3. **Maturity-boundary discipline** — `PARTIAL`/`PRODUCT_DEPENDENCY`,
   never `BLOCKED` (repo-verified this session), never
   `DEPLOYED_RUNTIME` or wired to this Academy (self-declared by
   `MetaCVLN`'s own audit).
4. **Three-system discipline** — `fms-os/fms`'s `/os/command-center`
   vs. `MetaCVLN`'s real `/command-center/*` vs. `external/cmd01_14`'s
   market-general SRE/ICS curriculum, never merged.

## Assessment

A route-literacy exercise: candidate is given a representative
`/command-center/overview`/`/timeline` payload shape and must correctly
describe what it represents, its real maturity classification, and
explicitly refuse to describe any operational access this Academy does
not have — eliminatory failure for claiming `DEPLOYED_RUNTIME` status
or Academy-side operability, or for conflating any of the three
systems in module 4.

## Evidence / certification / mission eligibility

`CMD15.SKILL.*` Skill IDs, reserved in `70_EVIDENCE/
EVIDENCE_ARCHITECTURE.md`. Mission eligibility requires literacy of the
real `MetaCVLN` route shapes — never live operational access to
`MetaCVLN` in production, which this Academy has no relationship with.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package (référentiel +
N1/N2 + assessment/rubric + evidence model + 3 guides + integration
note), deepened this pass as this wave's flagship. Never implies
`FULLY_COMPLETE` — no real candidate has been assessed yet, and this
status applies to CMD-15 alone, never to the AF/IOS/BRN/CMD/LAU corpus
as a whole (see `docs/agf/QUALITY_GATES.md`'s canonical state line).
