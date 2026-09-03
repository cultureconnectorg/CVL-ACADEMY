# W3-B — Context Entry / Return (ACTIVE → CONTEXT → RETURN) — REPORT

```
Applies to: quiz, mini-mission ("mission"), Mentor panel.
"Cas pédagogique": N/A — no such screen exists in the current product
  (FMS pedagogical cases are a distinct, unmounted content concept per
  docs/SPATIAL_LEARNING_W0.5_FMS_SOURCE_AUDIT.md; FMS_CANONICAL_MIGRATION
  stays FORBIDDEN, so nothing was built to fill this slot — documented
  here rather than fabricated).
```

## Naming reconciliation, stated plainly

The doctrine names the chain "ACTIVE → CONTEXT → RETURN." Read literally
against `spatial-state.js` (W1-D), `RETURN` is a *state* that only leads
to `IDLE` — but "the user returns exactly to their learning point" is
about staying on the same screen, not going idle. This tranche resolves
that by splitting the word into what it actually names in each layer:

- **State machine** (`spatial-state.js`, unchanged): dismissing a
  context is `DISMISS_CONTEXT`, which settles back at `ACTIVE` — the
  same module/panel, never navigating, `IDLE` is never reached from this
  hook.
- **Motion** (`ContextFrame.jsx`, new): the *exit* transition uses
  `RETURN`'s own duration/easing token and its documented contract
  ("restore exact prior context… never reset to a default destination")
  — this is where "RETURN" actually shows up, as the shape of the
  animation, not a state name.

This is documented in `ContextFrame.jsx`'s own header, not a silent
reinterpretation.

## What's built

- **`frontend/src/lib/ContextFrame.jsx`** — `useContextEntry()` (a thin
  binding to `useSpatialState(SPATIAL_STATES.ACTIVE)`, exposing only
  `enterContext`/`leaveContext`, the two events this hook ever needs) and
  `ContextFrame` (an always-mounted `motion.div`: REVEAL's duration/easing
  entering, RETURN's duration/easing exiting, `pointer-events:none` while
  hidden, `data-context-state` for testability). **First real use of the
  W1-D spatial-state machine** — it existed as unmounted infrastructure
  since W1-D specifically for this.

## REQ_ID table

| REQ_ID | BEFORE | CHANGE | FILES | RUNTIME_PROOF | TEST | PERF | A11Y | REGRESSION | STATUS |
|---|---|---|---|---|---|---|---|---|---|
| SL-CONTEXT-01 (quiz) | Quiz questions appeared via a plain conditional render, no transition, no explicit context state | Once quiz data loads, `PhaseQuizContext` calls `enterContext()` on mount and wraps the question list in `ContextFrame` | `frontend/src/pages/ModuleJourney.js` | Starting the quiz → `data-context-state="context"` on the questions wrapper | `module-journey-context.spec.js` "starting the quiz enters CONTEXT" | Negligible — opacity/y on one block | No change to inputs/labels/testids | None — additive wrapper, `PhaseQuiz`'s earlier branches (not-started/already-passed) untouched | VERIFIED |
| SL-CONTEXT-02 (mini_mission) | Same — plain conditional render | `PhaseMiniMission` calls `enterContext()` once `quizPassed` becomes true, wraps its content in `ContextFrame` | `ModuleJourney.js` | After a passing quiz submit (dynamic fixture — see below), the mini-mission block reads `data-context-state="context"` | `module-journey-context.spec.js` "submitting a passing quiz auto-advances to mini_mission, which enters CONTEXT too" | Negligible | No change | None | VERIFIED |
| SL-CONTEXT-03 (mentor) | Panel fully unmounted on close (`{open && (…)}`) — no exit motion at all; FAB/close both called a local `useState` setter | Panel is now always mounted, driven by `useContextEntry()`; close (X button or backdrop click) plays the RETURN motion instead of vanishing | `frontend/src/components/MentorPanel.js` | Opening → `data-context-state="context"`, `aria-hidden="false"`; closing → `"active"`, `aria-hidden="true"` | `module-journey-context.spec.js` "opening the mentor enters CONTEXT and closing it returns to ACTIVE" | Negligible — one overlay | See SL-CONTEXT-04 | None — messages state already lived above the old conditional, so history/persistence across open/close is unchanged | VERIFIED |
| SL-CONTEXT-04 (mentor a11y regression avoided) | N/A (panel didn't exist in the DOM while closed, so this risk didn't exist yet) | Every interactive control inside the panel (`mentor-close`, `mentor-input`, `mentor-send`, the backdrop) gets `tabIndex={open ? 0 : -1}`; the frame itself gets `aria-hidden`/`inert` when closed | `MentorPanel.js` | Closed: `mentor-input`/`mentor-close` both read `tabindex="-1"`. Open: `tabindex="0"` | `module-journey-context.spec.js` "closed mentor panel is not keyboard-reachable" | — | Directly avoids the same class of regression W2-B caught for a hidden `required` field — a hidden-but-mounted panel must never be keyboard-reachable or announced | None — this is a new guarantee, not a change to prior behavior (the panel used to just not exist when closed) | VERIFIED |
| SL-CONTEXT-05 (CURRENT_MODULE_PRESERVED / RETURN_POSITION_PRESERVED) | — | — | — | Quiz: URL unchanged throughout. Mentor: opening/closing on `/formations` never navigates, and the pole filter's `FocusFieldItem` role (W2-D) — set *before* opening the mentor — is still `"target"` after closing it | `module-journey-context.spec.js` (4 tests) | — | — | — | VERIFIED |
| SL-CONTEXT-06 (PROGRESS_NOT_MUTATED_BY_ANIMATION) | — | — | — | Zero mutating requests while opening/answering the quiz (before Submit) and while opening/closing the mentor | `module-journey-context.spec.js` (2 tests) | — | — | — | VERIFIED |
| SL-CONTEXT-07 (reduced motion) | — | `ContextFrame` consults `useReducedMotion()` for both its enter and exit durations | `ContextFrame.jsx` | Quiz and mentor contexts both settle at `opacity: 1` under emulated reduced motion | `module-journey-context.spec.js` (2 tests) | — | — | None | VERIFIED |

## Fixture extension (`frontend/e2e/fixtures/auth-fixture.js`)

- `FIXTURE_MODULE_QUIZ_READY` — a **separate** module object (not a
  mutation of W3-A's `FIXTURE_MODULE`), with `deliverable: true` and
  `quiz`/`mini_mission: false`, so quiz is the reachable frontier. Kept
  separate specifically so W3-A's 9 existing role-derivation tests keep
  asserting against the exact state they were written for — confirmed by
  re-running them unmodified (still 9/9 passing).
- `FIXTURE_QUIZ` / `FIXTURE_QUIZ_RESULT_PASSED` — one question, a passing
  result.
- The module-GET route is now **stateful within one browser context**
  (a closure flag, reset per test, never persisted): after a passing
  `quiz/submit`, it starts reporting `phase_flags.quiz: true`, exactly
  what a real backend would do on ModuleJourney.js's own post-submit
  reload. This is not `FAKE_PRODUCTION_DATA` — it's in-memory simulation
  of the real contract, scoped entirely to the test process, needed to
  prove the mini_mission auto-advance without which that CONTEXT
  transition couldn't be exercised at all.
- `POST /api/mentor/chat` mocked with a fixed fixture reply.

## Test run (this tranche)

- `npx eslint src e2e playwright.config.js` → clean.
- `CI=true npx craco test --watchAll=false` → 21/21 Jest unit tests unaffected (no new unit-testable pure logic this tranche — `useContextEntry`/`ContextFrame` are thin bindings over already-tested `spatial-state.js`).
- `CI=true yarn build` → compiled successfully. `main.js` gzip: 167.8 kB → 168.53 kB (+727 B) — `MentorPanel`/`ContextFrame`/the spatial-state machine are reached through `Layout.js`'s synchronous import chain (not lazy), so this is the real, disclosed cost of the state machine actually executing for the first time, not a regression to hide.
- `npx playwright test` → **60/60 passing** (48 pre-existing specs re-run unmodified + 12 new in `module-journey-context.spec.js`).
- Backend regression (unchanged): `black --check`, `flake8` clean; `pytest tests/ -n 0 --ignore=tests/backend_test.py` → 40/40 passing.

## Regression check

`git status --porcelain` before commit showed exactly 5 files:
`ModuleJourney.js`, `MentorPanel.js`, `auth-fixture.js` (all modified),
and 2 new files (`ContextFrame.jsx`, `module-journey-context.spec.js`).
No backend file, no `db.formations`/`db.progress`/module-code/FMS-corpus
file touched.
