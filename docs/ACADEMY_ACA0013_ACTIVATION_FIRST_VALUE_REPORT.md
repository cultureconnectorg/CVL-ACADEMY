# ACA-0013 — Activation / First-Value Event Instrumentation

```
STATUS: EXECUTED (2026-09-08).
```

## What this closes

`docs/ACADEMY_FUNNEL_EVENT_TAXONOMY.md` (W-FUNNEL-0) classified two
funnel events `READY_TO_EMIT` — the underlying real action already
existed in the codebase — but neither was actually wired to
`services/events.py`'s already-in-production `EventBus`:

| Event | Real call site named by the taxonomy |
|---|---|
| `academy_activation_completed` | end of `POST /onboarding/complete` — "same response — real convergence payload already exists" |
| `academy_first_value_reached` | first `ModuleProgress` (`db.progress`) document created for a user |

Both are now genuinely emitted — a real `db.event_log` document is
written (`EventBus.publish`'s own persistence, unchanged) and any
subscriber gets fanned out to, exactly like the one pre-existing usage
(`academy.certification.passed` in `certification/service.py`).

Per the taxonomy's own "Naming reconciliation" recommendation, both use
the underscore, subject-first convention (`academy_activation_completed`,
`academy_first_value_reached`), not the dot-namespaced style the single
pre-existing event uses. Reconciling that one existing event's naming is
explicitly out of scope here (it has its own subscribers and tests) —
noted as remaining work below, as the taxonomy doc itself already flags.

## What was built

### `backend/services/activation.py` (new)
`emit_first_value_if_new(user_id, payload)` — call **before** a
`db.progress` upsert. Counts the user's existing `db.progress` documents;
if zero, publishes `academy_first_value_reached` with the given payload
and returns `True`; otherwise no-ops and returns `False`. This is the
only new logic this pass adds — everything else is emission of data that
already existed.

### `backend/api/learning.py`
`tick_phase` (`POST /modules/{fc}/{mc}/phase`) calls
`emit_first_value_if_new` immediately before its existing
`db.progress.update_one(..., upsert=True)`. This is the real, earliest
touch point in the learner's actual flow (`ModuleJourney.js` ticks
`hook` on module open, before quiz/deliverable/mini-mission are ever
reachable for that module) — see `services/activation.py`'s own
docstring for the full reasoning and the disclosed limitation (not
every `db.progress`-writing route is separately instrumented; see
"What remains open" below).

### `backend/api/onboarding.py`
`onboarding_complete` (`POST /onboarding/complete`) publishes
`academy_activation_completed` right before returning, with the real
convergence payload it already built: `metier_vise`, `territoire`,
`lang`, `recommended_formation_code`, `recommended_mission_code`,
`badge_earned_code`, `signals_emitted`. No new computation — every field
already existed in the function; this only emits it.

### `backend/tests/test_activation_events.py` (new)
4 tests, `mongomock_motor`-backed (same convention as every other suite
in this repo):
1. First-ever `tick_phase` call for a user emits `academy_first_value_
   reached` with the right payload.
2. A second phase tick — same module or a different one — never
   re-emits it.
3. Two different users each get their own, independent first-value
   event.
4. `onboarding_complete` emits `academy_activation_completed` with the
   real convergence fields.

## Verification

- `python -m pytest tests/test_activation_events.py -v` — 4/4 passed.
- Full backend suite: `python -m pytest tests/ -q --ignore=tests/backend_test.py`
  — **323 passed**, zero regressions.
- `python -m flake8 .` — clean (this repo's actual CI gate).
- `black --check` — clean on every touched file.
- `isort --check-only` flags `api/learning.py` — confirmed **pre-existing**
  on the base commit (`git stash` + re-run reproduces the same error with
  none of this pass's changes applied): isort has no `profile = black`
  configured in this repo, so it disagrees with black's own wrapping of
  the file's existing multi-line import block. Not something this pass
  introduced or is in scope to fix; not part of the CI gate (`ci.yml`
  runs `flake8` + `pytest` only, never `isort`).

## What remains open (explicitly out of scope for this pass)

- **Not every `db.progress`-writing route is instrumented for
  first-value** — only `tick_phase`. `submit_deliverable` and the quiz
  submit route (`api/quizzes.py`) also upsert into `db.progress` and
  could theoretically be a client's first-ever write if it skipped the
  normal UI flow; `commit_mini_mission` cannot (it requires an existing
  `quiz_passed` progress doc). This is a disclosed limitation of wiring
  the one real, earliest call site rather than all of them — not a
  silent gap.
- **The rest of the funnel taxonomy's `READY_TO_EMIT` rows** (landing
  viewed, signup started/completed, onboarding started/step-completed/
  completed, formation/module/quiz/mission started/completed, skill
  validated, badge awarded, `academy_returned`, `academy_next_action_
  started`) are not wired by this pass — ACA-0013's own title scopes it
  to activation/first-value specifically. Each remaining row already has
  a real call site named in the taxonomy for whenever it's prioritized.
- **Naming reconciliation of the one pre-existing event**
  (`academy.certification.passed` → `academy_certification_earned`) is
  untouched — it has its own subscribers (`services/integrations/
  subscribers.py`) and tests; renaming it is a small, separate,
  low-risk change but not this pass's job.
- **No frontend consumer of these events was built** — this pass is
  server-side emission only, matching the taxonomy's own scope (a
  backend `EventBus`, not a client analytics SDK). Nothing in the
  mission has asked for a specific analytics vendor to receive these;
  fabricating one would be exactly the "fake conversion success" the
  taxonomy doc's non-negotiable rule forbids.
