# ACA-0027 — Progressive Horizon (next relevant learning/opportunity)

```
STATUS: EXECUTED (2026-09-08). One new real signal (CERTIFICATION_
ELIGIBLE) composed with two already-existing ones (RESUME_MODULE,
FORMATION_EXPANSION) into a single ordered "what's next" endpoint and
Dashboard surface. Every item traces to a real, pre-existing
capability — nothing here is an invented recommendation.
```

## What existed before this pass

Two real, separately-triggered "next step" surfaces already lived on
`Dashboard.js`, both driven directly by `/user/learning-path`:
- `next_action` (the real continuation-engine/sequential-curriculum
  computation, ACA-0024/ACA-0019) — a "resume" or "continue" card.
- The `horizon-card` (W-FUNNEL-2 "Expansion", 2026-09-07) — the exact
  `EXPANDING` condition `lifecycleState.js` already derives (own pole
  100% validated, a real unlocked formation exists elsewhere).

Neither could ever surface a certification opportunity — a learner who
had completed a whole formation but never checked the certification
catalogue got no signal that they were eligible, even though
`certification.service.check_full_eligibility` already existed and
already knew the answer.

## What was built

- **`backend/services/progressive_horizon.py`** (new) —
  `compute_progressive_horizon(user_id, learning_path)`, a pure
  composition function over an already-fetched `user_learning_path()`
  response. Reproduces the two existing triggers (`RESUME_MODULE`,
  `FORMATION_EXPANSION`) server-side so they can be ordered alongside
  the new one, and adds `CERTIFICATION_ELIGIBLE`: for every formation
  (own pole or other) the learner has reached 100% progress on, looks
  up its real `Rubric` by `formation_code` (no naming-convention
  guess), skips it if an attempt already exists with status
  `in_progress`/`submitted`/`graded`/`passed` (a `failed` attempt
  legitimately re-surfaces — a real retry opportunity, not hidden
  forever), and runs it through `check_full_eligibility` — the exact
  same gate `start_attempt` itself uses. Deliberately bounded: only
  checks eligibility for formations the learner has actually completed
  (typically 0-3), never a full catalogue scan.
- **`backend/api/progression.py`** — new `GET /progression/horizon`
  (reuses `api.learning.user_learning_path` directly rather than
  recomputing its logic — the route decorator doesn't prevent calling
  the function like any other).
- **`frontend/src/pages/Dashboard.js`** — fetches `/progression/
  horizon` alongside the existing calls (network-failure-safe via
  `.catch(() => [])`, and defensively `Array.isArray`-guarded before
  `setHorizonItems`), renders a new, additive `CERTIFICATION_ELIGIBLE`
  card per eligible item — the existing `next_action`/`horizon-card`
  sections are completely untouched, still driven directly by `path`.
- **`frontend/src/lib/i18n.jsx`** — 3 new keys
  (`cert_opportunity_eyebrow`/`_title`/`_cta`) in all 4 languages
  (fr/en/ht/es).
- **`frontend/e2e/fixtures/auth-fixture.js`** — added a specific
  `**/api/progression/horizon` mock route returning `"[]"`. Without
  this, the fixture's generic `**/api/**` catch-all (`"{}"`, an
  object) would have made `horizonItems.filter()` crash the whole
  Dashboard tree in every e2e spec touching it — the exact same class
  of bug ACA-0031's report already documents finding and fixing once
  for `PhysicalSessionsPanel`; caught proactively here before it ever
  shipped as a real regression, not discovered after the fact.

## Verification

- `python -m pytest tests/test_progressive_horizon.py -v` — **12/12
  passed**: resume-item derivation, no-item-when-nothing-to-resume,
  expansion only when own pole is genuinely fully exhausted (never
  partially), expansion correctly excludes locked/already-complete
  formations, expansion capped at 3, certification item appears only
  when `check_full_eligibility` (stubbed here — that function has its
  own extensive coverage elsewhere) says eligible, correctly absent
  when not eligible / no rubric exists for the formation / the
  formation isn't actually complete / an attempt already exists —
  each of those last three proven via a `called` flag showing
  `check_full_eligibility` was never even invoked, not just that its
  result was ignored — a failed attempt correctly re-surfaces the
  opportunity, and the full priority order (resume → expansion →
  certification) end to end.
- Full backend suite: `python -m pytest tests/ -q
  --ignore=tests/backend_test.py` — **474 passed** (up from 462), zero
  regressions.
- `python -m flake8 .` — clean. `black --check` — clean on every
  touched file.
- `yarn build` (CRA production build) — compiled successfully, zero
  new warnings.
- Full local e2e suite (`npx playwright test`) — **86/86 passed**,
  proving the new fixture route prevents the crash class described
  above and that the new Dashboard card renders with zero regression
  to any existing spec.
- Route registration verified: `GET /api/progression/horizon` present
  on the real FastAPI app.

## What remains open

1. **`MISSION_OPPORTUNITY` items are not built** — the `qualification`
   package (RAIL2-03/04) already computes real Mission eligibility via
   its own "Opportunity view," but this pass didn't wire a fourth
   `HorizonItem` type for it; disclosed follow-on scope, not attempted
   here to keep this pass to the one clearly-missing signal
   (certification) rather than re-deriving qualification's own logic.
2. **No de-duplication against a formation's OWN pole vs. others when
   BOTH show a certification opportunity simultaneously** — real, but
   rare (a learner would need two fully-completed formations at once);
   the list simply carries both, which is correct, just not
   specifically tested for more than one certification item at a time.
3. **No admin/analytics visibility into how often each item type is
   shown or acted on** — this pass is the real signal + surface only,
   not an instrumentation/funnel-analytics layer on top of it.
