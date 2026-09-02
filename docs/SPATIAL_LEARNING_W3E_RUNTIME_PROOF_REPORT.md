# W3-E — Authenticated Runtime Proof + Full W3 Regression — REPORT

```
Required coverage: ModuleJourney, quiz/context entry, return position,
keyboard, reduced motion, back/forward, progress unchanged, auth guard.
Fixture: test-only (e2e/fixtures/auth-fixture.js), FAKE_PRODUCTION_DATA
respected throughout W3 (grep-checkable: the fixture directory is
imported only by *.spec.js files, never by frontend/src/**).
```

## Coverage map (where each required item is actually proven)

| Required item | Proven in | Notes |
|---|---|---|
| ModuleJourney (authenticated route) | `module-journey-hierarchy.spec.js` "AUTHENTICATED_ROUTE" | W3-A |
| quiz / context entry | `module-journey-context.spec.js` "starting the quiz enters CONTEXT" + 6 more | W3-B |
| return position | `module-journey-context.spec.js` "RETURN_POSITION_PRESERVED" (×2) + `module-journey-navigation.spec.js` "BACK_FORWARD" (new, W3-E) | W3-B covered context-dismiss return; W3-E adds the browser-level back/forward round-trip, the one gap left open |
| keyboard | `keyboard-focus.spec.js` (public), `module-journey-context.spec.js` "KEYBOARD_FOCUS" (quiz internals), `module-journey-navigation.spec.js` "KEYBOARD_FOCUS" (new, W3-E — the phase stepper's own tab order, disabled/LOCKED phases correctly skipped) | W3-E closes the stepper-level gap |
| reduced motion | `module-journey-hierarchy.spec.js`, `module-journey-context.spec.js` (×2), `roadmap-progression.spec.js`, `module-journey-navigation.spec.js` (new, W3-E — the whole stepper's 4 roles under reduced motion at once) | |
| back/forward | `routing.spec.js` (public routes only, W1-E) + `module-journey-navigation.spec.js` "BACK_FORWARD" (new, W3-E — the actual gap: back/forward **from within an authenticated ModuleJourney**, not just public pages) | **New in this tranche** |
| progress unchanged | `module-journey-hierarchy.spec.js`, `module-journey-context.spec.js` (×2), `module-journey-navigation.spec.js` (new, W3-E — the back/forward round-trip itself sends zero mutating requests) | |
| auth guard | `auth-guards.spec.js` — the `ModuleJourney` URL shape (`/formations/FMS-01/modules/FMS-01-M01`) was already one of the 14 protected paths proven since W1-E | Pre-existing, reconfirmed still passing |

**What W3-E actually added**, since everything else was already covered
across W3-A→D: `frontend/e2e/module-journey-navigation.spec.js`, 4 new
specs closing the one real gap (back/forward navigation in and out of an
authenticated module) plus a keyboard/reduced-motion pass at the whole
stepper rather than one phase at a time.

| REQ_ID | BEFORE | CHANGE | FILES | RUNTIME_PROOF | TEST | PERF | A11Y | REGRESSION | STATUS |
|---|---|---|---|---|---|---|---|---|---|
| SL-RUNTIME-01 (back/forward) | No test exercised leaving/returning to an authenticated ModuleJourney via browser history | New spec: `BackButton` click (client-side) → `FormationDetail` → `page.goBack()` → `ModuleJourney` remounts with the same fixture-derived hierarchy roles → `page.goForward()` → back on `FormationDetail` | `frontend/e2e/module-journey-navigation.spec.js` | URL and `data-journey-role="current"` both hold after the round-trip | "BACK_FORWARD" | — | — | None — pure new test coverage, no product code changed | VERIFIED |
| SL-RUNTIME-02 (progress unchanged across back/forward) | — | — | — | Zero mutating requests observed across the whole click→back→forward sequence | "PROGRESS_NOT_MUTATED_BY_ANIMATION" | — | — | — | VERIFIED |
| SL-RUNTIME-03 (stepper keyboard order) | Individual phase LOCKED-disabled state tested (W3-A); full tab-order walk not yet proven | Tab from `phase-toggle-hook` → `phase-toggle-objectives` → `phase-toggle-course` (all reachable), confirms `phase-toggle-workshop` (LOCKED) is `disabled` — native browser behavior, not new wiring | — | 3-hop tab walk lands exactly where the hierarchy predicts | "KEYBOARD_FOCUS" | — | Confirms no ad hoc `tabIndex` override anywhere in the stepper breaks native order | None | VERIFIED |
| SL-RUNTIME-04 (whole-stepper reduced motion) | Reduced motion proven per-phase (W3-A, one phase) | Same assertion applied to both a CURRENT and a LOCKED phase in one render | — | Both roles report correctly with `reducedMotion: 'reduce'` emulated | "REDUCED_MOTION" | — | — | None | VERIFIED |

## Full W3 regression, run just now in sequence

| Gate | Command | Result |
|---|---|---|
| Frontend eslint (app + E2E infra) | `npx eslint src e2e playwright.config.js` | **clean** |
| Frontend unit tests | `CI=true npx craco test --watchAll=false` | **28/28 passing** |
| Frontend production build | `CI=true yarn build` | **compiled successfully**, `main.js` gzip 168.56 kB |
| Frontend E2E | `npx playwright test` | **73/73 passing** |
| Backend format/lint/types | `black --check`, `isort --check`, `flake8`, `mypy --ignore-missing-imports` | **all clean** (72 files, untouched by all of W3) |
| Backend tests | `pytest tests/ -n 0 --ignore=tests/backend_test.py` | **40/40 passing** |

## Per-tranche summary, W3 in full

| Wave | Commit | Domain data touched | Screens touched |
|---|---|---|---|
| W3-A Module journey shell | `4523ea2` | none | `ModuleJourney.js` |
| W3-B Context entry/return | `9121aa0` | none | `ModuleJourney.js`, `MentorPanel.js` |
| W3-C Mentor contextual presence | `c7b4cad` | none | `Layout.js` |
| W3-D Spatial progression | `f5ba48b` | none | `Roadmap.js`, `i18n.jsx` |
| W3-E Runtime proof | (this commit) | none | test-only (`e2e/`) |

**Cumulative freeze compliance, verified across every W3 commit:**
`MODULE_CONTENT_CHANGE`, `MODULE_CODE_CHANGE`, `PROGRESS_CHANGE`,
`UNLOCK_RULE_CHANGE`, `DB_FORMATIONS_MUTATION`, `DB_PROGRESS_MUTATION`,
`MODULE_CODE_REMAP`, `FMS_CANONICAL_MIGRATION`,
`BACKEND_CONTRACT_CHANGE`, `WEBGL`, `AUDIO_LAYER` — none breached. **No
backend file was touched by any W3 commit** (reconfirmed: `black`,
`isort`, `flake8`, `mypy`, and `pytest` all report the exact same
72-file/40-test baseline as before W3 started). `FAKE_PRODUCTION_DATA`
respected throughout — every fixture lives under `e2e/fixtures/`,
imported only by `*.spec.js` files.

**What's actually live now, visibly:** `ModuleJourney` shows a real
CURRENT/ACQUIRED/NEXT/LOCKED depth hierarchy on its phase stepper; quiz,
mini-mission, and the Mentor panel all transition through a real
ACTIVE→CONTEXT→RETURN cycle; the Mentor only ever appears inside a
module, never as a permanent floating chatbot; the Roadmap no longer
exposes "Level N" and its current stage is spatially foregrounded. Every
other authenticated screen (Dashboard, Missions, Badges, Skills,
Certifications, Wallet, FrekProfile, staff screens) is untouched by W3.

## Regression check

`git status --porcelain` before this commit showed exactly 1 new file:
`frontend/e2e/module-journey-navigation.spec.js`. No product code
changed in this tranche — W3-E is proof-only.
