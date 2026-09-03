# CVLN Academy — Funnel Event Taxonomy (W-FUNNEL-0)

```
DESIGN_ONLY. No event emission code added by this document. No vendor
dependency invented — the audit found exactly one real, generic event
mechanism already in the codebase (services/events.py, an in-process bus
persisting to db.event_log) and it is what any new emission would use.
```

## What's real today

- `services/events.py` — a real `EventBus` (`subscribe`/`publish`),
  every published event persisted to `db.event_log` *and* fanned out to
  subscribed handlers. Not a stub — it's live production code.
- It is used **exactly once** in the entire codebase:
  `certification/service.py:139`, `events.publish("academy.certification.
  passed", ...)`.
- Every other domain action that could be an event instead uses the
  narrower `frek_core.emit_signal(user_id, signal_type, meta)` channel
  (`db.frek_signals`) — real, but purpose-built for the FREK-TIME/WORK/
  SCORE/LINK/CERT/CONTRIB/SHARE/MISSION signal vocabulary, not a
  general funnel-analytics event stream, and not queryable the same way
  `db.event_log` is (no per-event-type aggregation built on it yet).

## Classification of the mission's candidate taxonomy (§31)

Rule applied strictly: an event is only `READY_TO_EMIT` if the action it
names already has a real, working code path found in
`ACADEMY_CURRENT_FUNNEL_AUDIT.md`. An event is `NEEDS_NEW_CAPABILITY`
if the underlying action doesn't exist yet — emitting it would be
"emitting a fake conversion success," explicitly forbidden.

| Event | Classification | Real call site to wire it from (once authorized) |
|---|---|---|
| `academy_landing_viewed` | `READY_TO_EMIT` | `Landing.js` mount |
| `academy_signup_started` | `READY_TO_EMIT` | Landing mode switch to `register` |
| `academy_signup_completed` | `READY_TO_EMIT` | `POST /auth/register` success |
| `academy_onboarding_started` | `READY_TO_EMIT` | `Onboarding.js` mount |
| `academy_onboarding_step_completed` | `READY_TO_EMIT` | each real onboarding field commit (lang/métier/territoire/objectif) |
| `academy_onboarding_completed` | `READY_TO_EMIT` | `POST /onboarding/complete` success |
| `academy_activation_completed` | `READY_TO_EMIT` | same response — real convergence payload already exists |
| `academy_first_value_reached` | `READY_TO_EMIT` | first `ModuleProgress` document created for a user |
| `academy_formation_viewed` | `READY_TO_EMIT` | `GET /formations/{code}` |
| `academy_formation_started` | `READY_TO_EMIT` | first `phase` tick on any module of that formation |
| `academy_module_started` | `READY_TO_EMIT` | `POST /modules/{fc}/{mc}/phase` first call |
| `academy_module_completed` | `READY_TO_EMIT` | `ModuleProgress.completed` flips true |
| `academy_quiz_started` | `READY_TO_EMIT` | `GET /quiz` |
| `academy_quiz_completed` | `READY_TO_EMIT` | `POST /quiz/submit` |
| `academy_mission_started` | `READY_TO_EMIT` | `POST /missions/{code}/accept` |
| `academy_mission_completed` | `READY_TO_EMIT` | `POST /missions/{code}/submit` (on validation, not just submission — check `status` transition) |
| `academy_skill_validated` | `READY_TO_EMIT` | `skills/progression.py`'s real validation path |
| `academy_badge_awarded` | `READY_TO_EMIT` | `badges_engine.award_threshold_badges` |
| `academy_certification_earned` | **ALREADY EMITTED** (as `academy.certification.passed`) | `certification/service.py:139` — naming convention differs (dots vs underscores); reconcile naming rather than duplicate |
| `academy_paywall_viewed` | `NEEDS_NEW_CAPABILITY` | no paywall surface exists |
| `academy_checkout_started` | `NEEDS_NEW_CAPABILITY` | no checkout exists |
| `academy_purchase_completed` | `FORBIDDEN_TO_EMIT until real` | no payment processor exists — emitting this before one does is exactly the "fake conversion success" the mission forbids |
| `academy_returned` | `READY_TO_EMIT` | any authenticated request after a session gap — needs `last_login_at` (small real schema addition, see lifecycle doc) |
| `academy_next_action_started` | `READY_TO_EMIT` | `user/learning-path`'s `next_action`, when acted on |
| `academy_expansion_offer_viewed` | `NEEDS_NEW_CAPABILITY` | no dedicated expansion surface exists yet — the *data* (`other_poles` + `is_unlocked`) is real, the *moment* isn't built |
| `academy_expansion_started` | `NEEDS_NEW_CAPABILITY` | same |
| `academy_ecosystem_handoff_started` | `FORBIDDEN_TO_EMIT until real` | no external integration is configured — this would currently always be false |
| `academy_ecosystem_handoff_completed` | `FORBIDDEN_TO_EMIT until real` | same |

## Naming reconciliation

The existing real event uses dot-namespaced, domain-verb-first naming
(`academy.certification.passed`) while the mission's candidate list uses
underscore, subject-first naming (`academy_certification_earned`).
**Recommendation for W-FUNNEL-1**: adopt the mission's underscore
convention going forward (it's the larger, more complete list) and
either alias the one existing event or rename it at its single call
site — a one-line change, not a migration, since nothing external
depends on the string today (only the in-process bus and the two
not-yet-configured subscribers).

## Non-negotiable rule carried into every wave

> Only emit events whose underlying actions actually exist. Do not emit
> fake conversion success.

Concretely: `academy_purchase_completed` and the two ecosystem-handoff
events must not be wired to fire until W-FUNNEL-5/7 respectively produce
a real backing capability — wiring them earlier "for completeness" would
violate this document's own rule.
