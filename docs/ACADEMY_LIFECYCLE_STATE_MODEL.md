# CVLN Academy — Lifecycle State Model (W-FUNNEL-0)

```
DESIGN_ONLY. These are DERIVED, non-exclusive maturity states — never a
new account-status field, never a replacement for any real domain field
on `User`/`Formation`/`ModuleProgress`/etc. Nothing here authorizes a
schema migration; W-FUNNEL-1 would compute these purely at read time
from fields that already exist.
```

## Why derived, not stored

The mission is explicit (§32): "these are NOT necessarily mutually
exclusive account statuses… prefer derived lifecycle/maturity state
based on evidence." The current `User` model already has a real,
narrower status field (`role`) and a real completion flag
(`onboarding_completed`) — this model sits *above* those, computed, not
instead of them.

## States and their derivation rules

Each rule reads only fields confirmed real in `ACADEMY_CURRENT_FUNNEL_
AUDIT.md` — no field is invented to make a rule work.

| State | Derivation rule (read-only, evaluated at request time) |
|---|---|
| `DISCOVERY` | No `User` record exists for this visitor (anonymous). |
| `IDENTIFIED` | `User` exists (`frek_id` assigned). |
| `ORIENTED` | `IDENTIFIED` and `onboarding_completed == True`. |
| `ACTIVATED` | `ORIENTED` and at least one `UserMission` exists with `source == "onboarding"` (the real auto-accepted first mission) **or** `metier_vise` resolves to at least one `Formation`. |
| `FIRST_VALUE` | `ACTIVATED` and at least one `ModuleProgress` document exists for this user (any status) — i.e. they opened a module at least once. |
| `LEARNING` | `FIRST_VALUE` and at least one `ModuleProgress.completed == False` exists with recent activity (a module genuinely in progress). |
| `PRACTICING` | `LEARNING` and at least one `UserMission.status in ("submitted","validated")` or a `QuizSubmission` has occurred. |
| `PROVEN` | at least one `UserBadge`, or `SkillProgressSummary` with a validated skill, or a passed `CertificationAttempt` exists. |
| `PROGRESSING` | `current.stade` has advanced beyond `"graine"` (real field, real `frek_core.resolve_stade` computation). |
| `CUSTOMER` | **Not derivable today** — no transaction/subscription model exists (see Monetization gap). This state cannot be computed until W-FUNNEL-5's interface contracts have a real backing capability; until then, no user can ever be `CUSTOMER`, and the model must say so rather than guess. |
| `RETURNING` | A session exists where `last_login_at` (not currently a tracked field — would need adding, additive only) is later than `created_at` by more than a deterministic threshold, e.g. >1 day. **Currently not derivable** — `User` has no `last_login_at`; this is a real, small, additive schema gap (a field, not a migration of existing data) flagged for W-FUNNEL-6. |
| `EXPANDING` | `own_pole` formations are exhausted (all `validated`) and at least one `other_poles` formation has `is_unlocked == True`. |
| `ECOSYSTEM_PARTICIPANT` | At least one `db.event_log` entry exists tied to this user for a *configured* external integration (i.e. a real outbound call happened, not just an interface existing). Today this can never be true — nothing is configured — so the model must report it as currently-unreachable, not silently omit it. |
| `ECOSYSTEM_BUILDER` | Not derivable at all today — no portfolio/project/collaboration model exists. `FUTURE_CONTRACT`, per the gap matrix. |

## Non-exclusivity, worked example

A learner mid-way through their second formation, having earned two
badges and one certification, with no payment ever made, is
simultaneously: `IDENTIFIED, ORIENTED, ACTIVATED, FIRST_VALUE, LEARNING,
PRACTICING, PROVEN, PROGRESSING, EXPANDING` — and **not**
`CUSTOMER, RETURNING (until the field exists), ECOSYSTEM_PARTICIPANT,
ECOSYSTEM_BUILDER`. The model exposes this as a set, not a single
current step — matching the loop, not a line, framing in
`ACADEMY_TARGET_MATURITY_FUNNEL.md`.

## What this state model is for

1. **Driving `NEXT_BEST_MEANINGFUL_ACTION`** (Retention, Level 10) —
   the existing `next_action` logic (`learning.py`) already does most of
   this deterministically for the Learning state; the lifecycle model
   generalizes the same "what's the next real gap" reasoning to the
   other states (e.g. `PROVEN` but not `EXPANDING` → surface an
   unlocked formation).
2. **Gating which spatial intensity/copy a surface shows** — e.g.
   Dashboard's primary-attention slot differs for a learner who is only
   `ACTIVATED` (show "open your first module") vs. `PROGRESSING` (show
   "continue where you were").
3. **Never gating actual access** — access stays governed by the real
   fields it already is (`role`, `onboarding_completed`, formation
   unlock rules). The lifecycle model is read-only decoration on top,
   consistent with `DOMAIN_STATE != VISUAL_STATE`.

## Explicit non-goals

- No new `lifecycle_state` field on `User`.
- No behavior gated *only* by a derived state without also checking the
  real underlying field it derives from.
- No state here ever marks itself `True` by inference alone when the
  mission's own rule ("do not fake maturity") would require external
  evidence that doesn't exist yet (`CUSTOMER`, `ECOSYSTEM_PARTICIPANT`,
  `ECOSYSTEM_BUILDER` are explicitly unreachable today, and the model
  says so rather than approximating).
