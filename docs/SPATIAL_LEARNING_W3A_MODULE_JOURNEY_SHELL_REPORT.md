# W3-A — ModuleJourney Spatial Shell — REPORT

```
DATA_SAFETY: MODULE_CONTENT_CHANGE = FORBIDDEN (respected — no phase
                                                 content/copy touched)
             MODULE_CODE_CHANGE   = FORBIDDEN (respected — module_code
                                                 never read by this file)
             PROGRESS_CHANGE      = FORBIDDEN (respected — 0 mutating
                                                 requests, standing E2E
                                                 assertion below)
             UNLOCK_RULE_CHANGE   = FORBIDDEN (respected — `canOpen`
                                                 computed by ModuleJourney.js
                                                 exactly as before, passed
                                                 in unchanged; the
                                                 `disabled={!canOpen}` gate
                                                 is untouched and tested)
```

## Doctrine → implementation mapping

```
CURRENT  -> FOREGROUND            the open phase (isOpen wins, even over done)
ACQUIRED -> BEHIND_BUT_ACCESSIBLE done, not open — still fully clickable
NEXT     -> HORIZON               the one reachable, not-yet-entered phase
                                   (genuinely unlocked — a legitimate HORIZON
                                   use per its own "never a false unlock"
                                   contract, since canOpen is real here)
LOCKED   -> DISTANT_SUBDUED       not yet reachable
```

`deriveJourneyRole({ isOpen, done, canOpen })` is a pure function
(`frontend/src/lib/JourneyHierarchy.jsx`), unit tested the same way
`spatial-state.js` and `CvlnFocusField.jsx`'s `deriveFocusRole` already
are. It reads three booleans ModuleJourney.js's own `.map()` loop already
computes — `done`, `isOpen`, `canOpen` — and writes nothing. The 4-role
opacity/scale/saturation staircase (`JOURNEY_VARIANTS`) is deliberately a
new, dedicated variant map (not a reuse of the binary `Approach`/`Recede`
primitives) because this needed two distinct "receded" weights
(ACQUIRED vs. LOCKED) that those primitives' fixed active/inactive
contract can't parametrize — the same reasoning `CvlnFocusField.jsx`
documented for its own variant map in W2-C.

## REQ_ID table

| REQ_ID | BEFORE | CHANGE | FILES | RUNTIME_PROOF | TEST | PERF | A11Y | REGRESSION | STATUS |
|---|---|---|---|---|---|---|---|---|---|
| SL-JOURNEY-01 (role derivation) | No visual distinction beyond the existing pill/ring/opacity-50-when-disabled treatment | `deriveJourneyRole` pure function + `JOURNEY_VARIANTS` (4-state opacity staircase: 1 / 0.88 / 0.7 / 0.45, current alone gets a 1.01 scale lift) | `frontend/src/lib/JourneyHierarchy.jsx` | — (pure function) | `JourneyHierarchy.test.js`: CURRENT-wins-over-done (revisit case), ACQUIRED, NEXT (frontier), LOCKED, a full 7-phase sequence partitions cleanly, opacity staircase ordering, only CURRENT scales — 7 tests | O(1) per phase | N/A (no DOM in this file) | None — new file, zero imports until wired below | VERIFIED (logic) |
| SL-JOURNEY-02 (mounted on the stepper) | Each phase card: flat `cvln-card`, only a `ring-2` when open, `opacity-50` on the *toggle button* when `!canOpen` | Each phase card wrapped in `JourneyPhaseShell` — `isOpen`/`done`/`canOpen` passed straight through from the existing loop, no new state | `frontend/src/pages/ModuleJourney.js` | fixture-authenticated render: hook (done+open) → `data-journey-role="current"`; objectives (done) → `"acquired"`; course (frontier) → `"next"`; workshop/deliverable/quiz/mini_mission → `"locked"`; opening course live re-derives it to `"current"` and hook to `"acquired"` | `module-journey-hierarchy.spec.js` (9 tests, see below) | Negligible — opacity/transform on ≤7 cards | No change — same buttons, same `data-testid`s, same disabled state | None — additive wrapper only | VERIFIED |
| SL-JOURNEY-03 (unlock rule untouched) | `disabled={!canOpen}` on each phase's toggle button | Unchanged — this tranche never reads or writes `canOpen`'s computation, only its value | `ModuleJourney.js` (0 lines changed in the `canOpen`/`prev` computation) | LOCKED phases' toggle buttons remain `disabled` | `module-journey-hierarchy.spec.js` "LOCKED phases stay disabled" | — | — | None | VERIFIED |
| SL-JOURNEY-04 (reduced motion) | — | `JourneyPhaseShell` consults `useReducedMotion()` exactly like every other primitive in this codebase | `JourneyHierarchy.jsx` | CURRENT's foreground transform still applies (non-`none`) under emulated reduced motion, just settled near-instantly | `module-journey-hierarchy.spec.js` "REDUCED_MOTION" | — | — | None | VERIFIED |
| SL-JOURNEY-05 (data safety, standing proof) | — | — | — | Zero mutating (`POST`/`PUT`/`PATCH`/`DELETE`) requests observed while opening/closing phases and reading the hierarchy | `module-journey-hierarchy.spec.js` "PROGRESS_NOT_MUTATED_BY_ANIMATION" | — | — | — | VERIFIED |

## Fixture extension (`frontend/e2e/fixtures/auth-fixture.js`)

Added `FIXTURE_MODULE` — a single fixture module deliberately built with a
mixed phase state (2 done, 1 reachable frontier, 4 locked, with the
already-done `hook` phase also the default-open one) so every
`JourneyHierarchy` role is exercised in one render, plus a
`**/api/modules/*/*` route matching only the module-fetch `GET` shape
(the exact 2-segment path ModuleJourney.js requests) — deliberately
narrower than the mutating 3+-segment endpoints (`…/phase`,
`…/deliverable`, `…/mini-mission/commit`), which stay on the generic
`{}` catch-all until a tranche that needs to click them (W3-B) extends
this fixture further.

## Test run (this tranche)

- `npx eslint src e2e playwright.config.js` → clean.
- `CI=true npx craco test --watchAll=false` → **21/21 Jest unit tests passing** (14 pre-existing + 7 new in `JourneyHierarchy.test.js`).
- `CI=true yarn build` → compiled successfully, `main.js` gzip effectively unchanged (`ModuleJourney.js` is its own lazy chunk).
- `npx playwright test` → **48/48 passing** (39 pre-existing specs re-run unmodified + 9 new in `module-journey-hierarchy.spec.js`).
- Backend regression (unchanged, confirming no drift): `black --check`, `flake8` clean; `pytest tests/ -n 0 --ignore=tests/backend_test.py` → 40/40 passing.

## Regression check

`git status --porcelain` before commit showed exactly 5 files:
`ModuleJourney.js` (modified), `auth-fixture.js` (modified), and 3 new
files (`JourneyHierarchy.jsx`, `JourneyHierarchy.test.js`,
`module-journey-hierarchy.spec.js`). No backend file, no
`db.formations`/`db.progress`/module-code/FMS-corpus file touched.
