# ACA-0028 — Professional FREK Profile as Identity Surface

```
STATUS: EXECUTED (2026-09-08). FrekProfile.js was already real (FREK-ID,
stade, 8 engagement signals, a signal log) but purely an internal
dashboard. This pass composes it into an actual professional identity:
real acquired skills, real passed certifications, and a real,
explicit-opt-in public share link.
```

## What existed before this pass

`FrekProfile.js` — real identity card, canonical-progress card, an
8-tile signal-count grid, a raw signal log. Real data throughout, but
none of it was ever composed into something a learner could point an
employer or a collaborator to. Two real engines already had the raw
material this needed: the Skill Engine (`skills/progression.py` —
`Skill`/`UserSkill`/`EvidenceEntry`, states `not_started`/`in_progress`/
`acquired`) and the Certification Engine's attestation proof
(`certification/attestation.py`'s `attestation_export_metadata` — jury
signature hash, score, mention). Neither was surfaced anywhere.

## What was built

- **`backend/services/professional_profile.py`** (new) —
  `compute_professional_profile(user)`: real acquired skills (via
  `skills.progression.get_user_progress`, filtered to `state ==
  "acquired"`), real passed certifications (via `certification.
  service.list_user_attempts`, filtered to `status == "passed"`, each
  proof built from `attestation_export_metadata` — reused verbatim,
  not reshaped), real badge count. `set_profile_visibility` /
  `get_public_professional_profile`: a new, additive
  `db.professional_profile_settings` collection
  (`{user_id, is_public, updated_at}`), `is_public` defaulting to
  `False` (opt-in, never opt-out) — nothing here ever touches
  `db.users`. The public lookup returns `None` uniformly for "no such
  FREK-ID" and "exists but private," so a public caller can never use
  it to enumerate real FREK-IDs.
- **`backend/api/professional_profile.py`** (new) — `GET /professional/
  profile/mine` (auth), `POST /professional/profile/visibility` (auth),
  `GET /professional/public/{frek_id}` (deliberately the one
  unauthenticated route — a real identity surface has to be reachable
  without a session to function as a shareable link).
- **`backend/infra_indexes.py`** — unique index on
  `professional_profile_settings.user_id`.
- **`frontend/src/pages/FrekProfile.js`** — new "Professional profile"
  card: acquired skills grid, passed certifications list, a real
  visibility toggle (calls the new endpoint), and — once public — the
  actual shareable `/id/{frek_id}` link with a copy button. Fetched
  independently of the existing `/frek/profile` call; a failure never
  blocks the rest of the already-real page.
- **`frontend/src/pages/ProfessionalPublicProfile.js`** (new) — the
  public, unauthenticated page at `/id/:frekId`. Renders the same
  composed data for a signed-out visitor; a 404 (unknown FREK-ID or a
  real one that's private) renders one honest "not available" state,
  never distinguishing the two cases in the UI either.
- **`frontend/src/lib/i18n.jsx`** — new `frek_profile_p` keys
  (professional section + visibility toggle) and a new
  `professional_profile_p` namespace (public page), all 4 languages
  (fr/en/ht/es).
- **`frontend/e2e/fixtures/auth-fixture.js`** — added a specific
  `**/api/professional/profile/mine` mock returning a real, correctly-
  shaped `ProfessionalProfile` object. Without it, the generic
  `**/api/**` catch-all's `"{}"` would leave `proProfile` truthy but
  shapeless, crashing `FrekProfile.js`'s `.acquired_skills.length`
  access — the same crash class ACA-0031's report already documents
  once, and ACA-0027's report documents a second time (an array
  shape); this is the third instance, an object shape, caught
  proactively again before shipping.

## Verification

- `python -m pytest tests/test_professional_profile.py -v` — **9/9
  passed**: empty profile has no skills/certs, only `acquired` skills
  surface (not `in_progress`), only `passed` attempts surface (not
  `failed`) with the real attestation fields (score, mention, jury
  signature hash, graded_at), badge count reflects only the real
  user's own badges, default visibility is private, visibility
  toggles both directions, public lookup returns `None` for an unknown
  FREK-ID / a real-but-private one, and returns the real composed
  profile once made public.
- Full backend suite: `python -m pytest tests/ -q
  --ignore=tests/backend_test.py` — **483 passed** (up from 474), zero
  regressions.
- `python -m flake8 .` — clean.
- `yarn build` (CRA production build) — compiled successfully; the new
  `ProfessionalPublicProfile` page is its own lazy-loaded chunk, zero
  new warnings.
- Full local e2e suite (`npx playwright test`) — **86/86 passed**,
  proving the new fixture route prevents the crash class above and
  that existing specs touching `/frek-profile`
  (`environmental-continuity.spec.js`, `mobile-nav.spec.js`,
  `auth-guards.spec.js`) still pass with the new card mounted.
- Route registration verified: `GET/POST /api/professional/profile/
  mine`, `/api/professional/profile/visibility`,
  `/api/professional/public/{frek_id}` all present on the real
  FastAPI app.

## What remains open

1. **No dedicated e2e spec exercises the new card's own interaction**
  (clicking the visibility toggle, verifying the copy-link button) —
  covered indirectly (the page renders without crashing across 3
  existing specs) but not with a spec asserting the toggle's own
  behavior. Real, disclosed follow-on scope.
2. **No PDF/exportable version of the professional profile** — the
  existing certification attestation PDF (`certification/attestation.
  py::generate_attestation_pdf`) is per-certification, not a composed
  whole-profile export; not attempted here.
3. **No social/OG meta tags on the public `/id/:frekId` page** for
  link-preview purposes (a real, common expectation for a "shareable
  identity link") — this pass proves the page itself works; preview-
  card metadata is disclosed follow-on scope.
