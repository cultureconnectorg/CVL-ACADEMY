# W3-C — Mentor Contextual Presence — REPORT

```
MENTOR                 = CONTEXTUAL_PRESENCE   (implemented)
MENTOR_ALWAYS_VISIBLE  = FORBIDDEN              (respected — see below)
MENTOR_BLOCKS_CONTENT  = FORBIDDEN              (respected — unchanged
                                                  from before, re-verified)
```

## Before → after

Before this tranche, `<MentorPanel />` was mounted unconditionally in
`Layout.js`, rendered on **every** authenticated screen — dashboard,
formation discovery, missions, badges, wallet, frek-profile, roadmap,
and every staff screen (trainer/jury/admin). That is exactly the
"chatbot flottant permanent" the doctrine forbids.

## Scope decision, stated plainly

"Un contexte pédagogique le justifie" is not self-defining, so this
tranche makes one explicit, conservative choice rather than inventing a
broad context-detection system: the Mentor is available **only inside an
actual module** (`ModuleJourney`, `/formations/:fc/modules/:mc`) — the
one screen where a learner is unambiguously mid-lesson, not just
browsing. Formation discovery/detail, dashboard, missions, badges,
wallet, frek-profile, roadmap, and every staff screen are **not**
pedagogical-content contexts by this definition. Widening the set (e.g.
to `FormationDetail`) is a separate, explicit decision left for a later
wave — not assumed here, matching the "controlled, minimal integration"
posture the whole of W2/W3 has held to.

## REQ_ID table

| REQ_ID | BEFORE | CHANGE | FILES | RUNTIME_PROOF | TEST | PERF | A11Y | REGRESSION | STATUS |
|---|---|---|---|---|---|---|---|---|---|
| SL-MENTOR-01 (route gating, pure logic) | No presence rule existed — `<MentorPanel />` was unconditional | `isPedagogicalContext(pathname)` — a pure regex match against exactly the `ModuleJourney` route shape | `frontend/src/lib/mentorPresence.js` | — (pure function) | `mentorPresence.test.js`: true inside a module (with/without trailing slash), false on discovery/detail/dashboard/missions/badges/wallet/frek-profile/roadmap/skills/certifications/staff screens/landing/onboarding, and a substring-false-positive guard — 8 tests | O(1), one regex test | N/A | None — new file, zero imports until wired below | VERIFIED (logic) |
| SL-MENTOR-02 (mounted in Layout) | `<MentorPanel />` always rendered | `{mentorAvailable && <MentorPanel />}`, `mentorAvailable = isPedagogicalContext(useLocation().pathname)` | `frontend/src/components/Layout.js` | FAB/panel absent (`toHaveCount(0)`) on `/dashboard` and `/formations`; present and visible inside a module; a **client-side** navigation out of the module (via `BackButton`, no full reload) removes it again | `mentor-presence.spec.js` (5 tests) | Negligible — one `useLocation()` read + a boolean, no new render cost elsewhere | No change to any other nav/sidebar element | None — additive conditional only, `Layout`'s other content (sidebar, nav, FREK-ID card) untouched | VERIFIED |
| SL-MENTOR-03 (MENTOR_BLOCKS_CONTENT) | FAB is a small `fixed bottom-6 right-6` corner button, never covering the main content area | Unchanged — re-verified now that presence is conditional | — | The phase stepper (`phase-toggle-objectives`) remains clickable with the FAB visible alongside it | `mentor-presence.spec.js` "MENTOR_BLOCKS_CONTENT respected" | — | — | None | VERIFIED |
| SL-MENTOR-04 (W3-B specs re-scoped) | W3-B's mentor specs used `/formations` as the mount point (mentor was reachable everywhere then) | Updated to use the module URL, the now-correct place to reach the mentor; `RETURN_POSITION_PRESERVED` re-proven against the phase-hierarchy role (W3-A) instead of the pole filter (a `/formations`-only concept) | `frontend/e2e/module-journey-context.spec.js` | All 6 mentor specs re-run and pass against the module URL | `module-journey-context.spec.js` "mentor contextual panel (W3-B/W3-C)" (6 tests) | — | — | Expected, disclosed adjustment — not a silent rewrite: the surface itself intentionally moved in this tranche, so the tests move with it | VERIFIED |

## Fixture extension (`frontend/e2e/fixtures/auth-fixture.js`)

Added `FIXTURE_FORMATION_DETAIL` + a `**/api/formations/*` route (single
formation GET, distinct from the multi-segment quiz/quiz-submit routes
already registered) — needed because `mentor-presence.spec.js`'s
"navigating out of a module" test follows `ModuleJourney`'s real
`BackButton` to `FormationDetail.js`, which reads `f.stades[0]`
unconditionally once loaded and would throw against the generic `{}`
catch-all.

## Test run (this tranche)

- `npx eslint src e2e playwright.config.js` → clean.
- `CI=true npx craco test --watchAll=false` → **28/28 Jest unit tests passing** (20 pre-existing + 8 new in `mentorPresence.test.js`).
- `CI=true yarn build` → compiled successfully. `main.js` gzip: 168.53 kB → 168.59 kB (+60 B).
- `npx playwright test` → **65/65 passing** (48 pre-existing + 12 W3-B specs re-scoped in place + 5 new in `mentor-presence.spec.js`). One run showed a single timing-flaky failure on an unrelated W3-B test under 2-worker parallel load; isolated re-runs (×3) and a full clean re-run both passed it — not a regression from this tranche, noted here rather than hidden.
- Backend regression (unchanged): `black --check`, `flake8` clean; `pytest tests/ -n 0 --ignore=tests/backend_test.py` → 40/40 passing.

## Regression check

`git status --porcelain` before commit showed exactly 6 files:
`Layout.js`, `module-journey-context.spec.js`, `auth-fixture.js` (all
modified), and 3 new files (`mentorPresence.js`, `mentorPresence.test.js`,
`mentor-presence.spec.js`). No backend file, no
`db.formations`/`db.progress`/module-code/FMS-corpus file touched.
