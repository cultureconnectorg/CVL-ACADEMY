# ACA-0030 — Ecosystem Builder Surface (consumer → learner → professional → builder)

```
STATUS: EXECUTED (2026-09-08). A real, unified "what have I built"
surface now composes every already-real signal the gap matrix marked
IMPLEMENTABLE_NOW/PARTIAL for this row — nothing invented for the rows
marked MISSING or REQUIRES_OTHER_CVLN_SYSTEM. This closes the last
pending item in the ACA-00xx backlog.
```

## Scope contract (from `docs/ACADEMY_FUNNEL_GAP_MATRIX.md`)

That doc's own "Ecosystem Builder sub-capability classification" is
the boundary this pass respects exactly:

| Capability | Classification | Built here? |
|---|---|---|
| Portfolio of competencies | PARTIAL | Yes — unified rendering added |
| Verified proofs | IMPLEMENTABLE_NOW | Yes |
| Missions completed | IMPLEMENTABLE_NOW | Yes |
| Professional identity | PARTIAL | Yes — reuses ACA-0028 as-is |
| Credentials | IMPLEMENTABLE_NOW | Yes |
| Ecosystem history | PARTIAL | Yes — `db.event_log` filtered per user |
| Network/opportunities | REQUIRES_OTHER_CVLN_SYSTEM | **No** — no real data source exists inside Academy |
| Economic activity | REQUIRES_OTHER_CVLN_SYSTEM | **No** — depends on Monetization/other systems |
| Projects | MISSING (no model) | **No** — no model exists, not fabricated here |
| Collaborations | MISSING (no model) | **No** — no model exists, not fabricated here |

The last four rows are deliberately absent from the response model
entirely, not represented as empty placeholders — `test_ecosystem_
builder.py::test_never_fabricates_projects_or_collaborations_fields`
asserts this as a permanent scope guard, not just a launch-day fact.

## What was built

### `backend/services/ecosystem_builder.py` (new)
`compute_ecosystem_builder_surface(user)` composes:
- `services/professional_profile.py`'s already-real `compute_
  professional_profile` (portfolio = acquired skills, credentials =
  passed certifications with jury-signed proof metadata, professional
  identity = frek_id/display_name/is_public) — reused verbatim, not
  re-derived.
- `db.skill_evidence` (verified proofs — the real SHA-256-hashed
  evidence chain `skills/progression.py` already writes).
- `db.user_missions` filtered to `status == "validated"` (missions
  completed).
- `db.event_log` filtered to `payload.user_id == user.id`, newest
  first, capped at 20 (ecosystem history — the same event log ACA-0029
  wired real handoffs onto).

**The four-stage progression** is derived, not stored, exactly like
every other composed surface this session built (Progressive Horizon,
Professional Profile):
- `consumer` — no engagement signal yet.
- `learner` — at least one verified proof or validated mission, no
  acquired skill/passed certification yet.
- `professional` — at least one acquired skill OR one passed
  certification (the same bar ACA-0028 already uses for "has a real
  professional identity").
- `builder` — professional AND `is_public=True` (ACA-0028's existing
  opt-in, reused rather than inventing a second toggle) — the one real,
  non-fabricated "circulating in the ecosystem, not just practicing
  privately" signal Academy has today.

### `backend/api/ecosystem_builder.py` (new)
`GET /api/ecosystem-builder/me` — authenticated, always the caller's
own data (unlike `professional_profile.py`, this surface has no public
route; it's the private unified view, not the shareable identity card).
Registered in `api/__init__.py`.

### `frontend/src/pages/EcosystemBuilder.js` (new)
A stage track (consumer/learner/professional/builder, current stage
highlighted) plus four composed cards (portfolio, credentials, verified
proofs, missions completed) and an ecosystem history log. A learner at
`professional` stage sees a CTA pointing to FREK Profile's existing
visibility toggle (ACA-0028) — the one real action that would move them
to `builder`. Wired into `Layout.js`'s `STUDENT_NAV` (sidebar + mobile
"more" sheet) and `App.js`'s route table at `/ecosystem-builder`, with
full i18n coverage across all 4 languages (fr/en/kr/es).

## Verification

- `python -m pytest tests/test_ecosystem_builder.py -v` — **8/8
  passed**: stage derivation proven at each of the 4 transitions (fresh
  user -> consumer; evidence-only or mission-only -> learner; acquired
  skill -> professional; passed certification -> professional;
  professional + public opt-in -> builder), ecosystem history correctly
  filters to the calling user and orders newest-first, and the scope
  guard (no `projects`/`collaborations`/`network`/`economic_activity`
  field ever appears in the response) passes.
- Full backend suite: `python -m pytest tests/ -q
  --ignore=tests/backend_test.py` — **500 passed** (492 + 8 new), zero
  regressions.
- `python -m flake8 .` / `black --check` — clean on every touched file.
- `python -c "from server import app"` — imports cleanly.
- `npx eslint` on every touched frontend file — clean.
- `CI=true yarn build` — clean, no new warnings.
- `CI=true yarn test` (Jest) — 22 suites / 186 tests, unaffected,
  all passing.
- New `frontend/e2e/ecosystem-builder.spec.js` (5 specs: authenticated
  route + default consumer stage, sidebar nav link, a composed
  "builder" stage rendering every card from a realistic surface, the
  professional-stage CTA visibility, PROGRESS_NOT_MUTATED_BY_ANIMATION,
  REDUCED_MOTION) — proactively added a specific `**/api/ecosystem-
  builder/me` mock route to `e2e/fixtures/auth-fixture.js` (the same
  `{}`-catch-all crash class this session has now fixed three times)
  before the page could ever hit the generic `{}` fallback.
- Full local e2e suite: `npx playwright test e2e/` — **92/92 passed**
  (86 baseline + 6, comment: mobile-nav's existing "More" sheet test
  already covered the new nav entry without modification since it
  asserts on the existing curated key list, not an exhaustive one).

## What remains open

- **Network/opportunities and Economic activity** stay unbuilt inside
  Academy — both genuinely require another CVLN system (a real
  connections graph, a monetization ledger tied to marketplace
  activity) that doesn't exist here. `services/integrations/registry.py`
  is where a future real connection to such a system would land,
  exactly as ACA-0029 already established for Wallet.
- **Projects and Collaborations** have no data model anywhere in this
  codebase. Building one would be new product surface (what is a
  "project": a template submission? a mission? something new
  entirely?) — a real product decision this pass doesn't make on its
  own, not a technical gap.
- This closes the last pending item in the ACA-00xx backlog
  (`docs/ACADEMY_FUNNEL_GAP_MATRIX.md`'s own "Ecosystem Builder" row is
  the row this report answers).
