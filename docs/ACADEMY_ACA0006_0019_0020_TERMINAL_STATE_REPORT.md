# ACA-0006 / ACA-0019 / ACA-0020 — Terminal State Report

```
STATUS: TERMINAL STATE CONFIRMED (2026-09-08). All three items are at
their honest, correct final state for this session — not stalled by
omission, but genuinely blocked by the Founder's own binding directive
(AUTO_PEDAGOGICAL_EQUIVALENCE = FORBIDDEN). This report closes the
investigation, it does not pretend to close the items by inventing a
decision that isn't mine to make.
```

## What is actually already built (more than the task list's stale wording suggests)

Reading `backend/services/canonical_convergence.py` and its callers
directly (not just the task-tracker's summary text) shows the
CANONICAL_CURRICULUM_RUNTIME = AUTHORITATIVE Founder decision (recorded
in that module's own header, 2026-09-07, ACA-0019) is substantially
executed, on every primary read surface:

- **`get_canonical_authority_map()`** — wired into `GET /formations`
  and `GET /formations/{code}` (`api/formations.py`): a formation with
  real canonical content is marked with its authority, and the legacy
  catalogue entry defers to it.
- **`get_canonical_authority(formation_code)`** — wired into module
  detail (`api/learning.py`): visiting a canonically-authoritative
  formation's legacy module redirects to the real canonical formation,
  never silently rendering stale legacy content next to it.
- **`get_first_unviewed_canonical_module(user_id)`** — wired into
  `next_action` (`GET /user/learning-path`): a learner whose legacy
  path has nothing actionable gets a real canonical next-action
  instead of an empty one (`CONVERGENCE_RUNTIME`, proven by
  `tests/test_convergence_next_action.py`). Legacy stays authoritative
  whenever it has a real next step — this never overrides it.
- **`get_canonical_progress_summary(user_id)`** — wired into `GET
  /user/learning-path`, `GET /frek/profile`, and `GET /progression/
  summary` (`api/progression.py`): canonical viewed-module counts are
  surfaced under their own `canonical_*` keys on every surface a
  learner actually looks at, cross-linked, never silently absent.

This is real, tested, production-wired convergence — the "surfaced and
cross-linked on primary runtime" half of the task list's own
description for ACA-0006.

## The actual remaining gap, and why it can't be closed here

What's genuinely still legacy-only: **stade, CC credits, `global_pct`,
and certification eligibility** — the numbers that actually *drive*
progression (badges, unlocks, rewards) — are computed from legacy
`db.progress` only. Canonical content's contribution stays reported as
*viewed* (`content_viewed_at`), never folded into those driving
numbers as *completed*.

This is not an oversight. `services/canonical_convergence.py`'s own
header states the binding constraint this was built against:

> `AUTO_PEDAGOGICAL_EQUIVALENCE = FORBIDDEN` — canonical's one honest
> recorded signal today is *viewed*, never re-labeled *completed*: the
> legacy "completed" flag means quiz-passed + mini-mission-committed,
> a bar canonical's corpus doesn't yet have a mechanism to clear.

Concretely: FMS-canonical/Kiltikonet-canonical/KORA-canonical modules
have no graded quiz, no mini-mission commit step, no equivalent of the
legacy 7-phase validation the stade/CC math is built on. Making
canonical "the driving source" would require one of:

1. **Real grading/certification semantics for canonical content** — a
   content-authoring gap, not a runtime-wiring one. This is exactly
   what `docs/ACADEMY_ACA0020_ASSESSMENT_CHAIN_*_REPORT.md` (all 4
   domains) already discloses as open: N1/N2 question-bank binding and
   admin-UI import triggers are real, named, unstarted work — the
   actual blocker behind ACA-0020's own `[in_progress]` status.
2. **An explicit Founder decision defining a specific pedagogical
   equivalence** (e.g. "N canonical modules viewed = 1 legacy module
   validated") — which the Founder's own directive forbids inventing
   unilaterally, and no such mapping is recorded anywhere in this
   repository's docs (`grep`-confirmed empty).

Fabricating either — a fake grading pass, or an invented equivalence
ratio — would be exactly the kind of unverifiable, self-authorized
claim this session has consistently refused to make elsewhere (the
same discipline behind `NO_FAKE_PAID_STATE` in ACA-0026, and the
scope guard against inventing Projects/Collaborations in ACA-0030).

## Disposition

- **ACA-0006**: terminal at PARTIAL — canonical progress is real,
  cross-linked, and additive on every primary surface; it is correctly
  NOT the driving source, because making it one would require
  fabricating what §above forbids.
- **ACA-0019**: the Founder decision it names is executed everywhere
  it safely can be (routing authority, next-action fallback, progress
  cross-linking). The remaining "AUTHORITATIVE" scope (driving
  stade/CC/certification) is blocked on real content-authoring work
  (ACA-0020), not on further runtime code.
- **ACA-0020**: stays `[in_progress]` honestly — N1/N2 question-bank
  binding and admin-UI import triggers are real, disclosed,
  content-authoring-dependent work items, not something this pass
  fabricates a shortcut around.

No code changes accompany this report — it is a closing analysis, not
a new capability. Any of the three items becomes further buildable
the moment either (a) real N1/N2 graded content exists to bind, or (b)
the Founder records an explicit equivalence decision — neither of
which this session can supply on its own authority.
