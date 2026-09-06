# KOR-OP-12 — Release Operations (new, narrow, internal)

## Grounding

Per `KORA_OP_X_RECONCILIATION.md`: the one candidate among KOR-OP-01→12
without a clean 1:1 existing anchor — coverage `PARTIAL` (split across
`KOR-03`'s release-adjacent competencies and `KOR-04`'s programming
calendar, no dedicated release-operator module in either), action
`NEW_INTERNAL (narrow)` — "a thin capstone module bridging KOR-03/04's
release-adjacent content," not a full parallel formation.

Concretely grounded in two already-built formations' own competency
tables:
- `docs/kor/kor03/REFERENTIAL.md` C9 ("encoder pour la livraison") and
  C10 ("publier et contrôler la qualité technique avant mise en
  ligne") — the production-readiness side of a release.
- `docs/kor/kor04/REFERENTIAL.md` C3 ("construire un calendrier et des
  cycles éditoriaux") and C8 ("programmer un événement et mesurer sa
  performance") — the editorial-scheduling side of a release.

Neither formation names a single person who owns the **go/no-go
decision** that sits between "technically ready to publish" (`KOR-03`)
and "scheduled to appear in the editorial calendar" (`KOR-04`) — that
coordination role is what this formation teaches.

## Prerequisites

`KOR-03` (or literacy of its C9/C10), `KOR-04` (or literacy of its
C3/C8).

## Objectives

- Teach the real, generic release-coordination discipline: reconciling
  a technically-ready asset (`KOR-03`'s domain) against an editorial
  release slot (`KOR-04`'s domain), and making an explicit go/no-go
  call when the two are misaligned (asset not ready for its scheduled
  slot, or slot conflicts with another release).
- **Never duplicate either side's actual competency**: this formation
  does not re-teach encoding/QC (`KOR-03`) or editorial calendar
  construction (`KOR-04`) — it teaches the coordination judgment that
  sits at their handoff, which neither formation's own competency list
  names as a single role.
- **Never claim a KORA platform release-management system exists**:
  no dedicated release-tooling/CMS is found in this repo
  (`ACADEMY_LOCAL_EVIDENCE = NOT_FOUND`, consistent with both `KOR-03`
  §6 and `KOR-04` §6) — the coordination is taught as a human judgment
  exercised against two other humans' outputs, not a system.

## Modules

1. **Reading production-readiness signals** — literacy of `KOR-03`'s
   C9/C10 outputs (encoding/QC status) without re-teaching how to
   produce them.
2. **Reading the editorial release calendar** — literacy of `KOR-04`'s
   C3/C8 outputs (scheduled slots, event windows) without re-teaching
   how to build them.
3. **Go/no-go coordination** — the core new competency: reconciling
   the two signals, escalating misalignment, making and documenting an
   explicit release decision.
4. **Boundary discipline** — this formation is a thin bridge, never a
   replacement for `KOR-03` or `KOR-04`'s own competencies, and never
   evidence of a real KORA release-management platform.

## Assessment

A coordination exercise: candidate is given a simulated production-
readiness report and a simulated editorial calendar slot with a
deliberate misalignment (e.g. QC-failed asset scheduled for imminent
release, or two releases scheduled into the same slot) and must
produce a documented go/no-go decision with an explicit rationale —
eliminatory failure for silently re-deriving `KOR-03`/`KOR-04` content
instead of reading their outputs, or for claiming a real KORA release
platform exists.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package (référentiel +
N1/N2 + assessment/rubric + evidence model + 3 guides + integration
note), built this pass as the one genuinely new row in the KOR-OP/
KOR-X set. Never implies `FULLY_COMPLETE` — no real candidate has been
assessed yet.
