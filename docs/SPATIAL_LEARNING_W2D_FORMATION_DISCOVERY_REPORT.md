# W2-D — Formation Discovery + Deterministic Authenticated-Surface Fixture — REPORT

```
DATA_SAFETY: FMS_CANONICAL_CONTENT_MIGRATION = FORBIDDEN (respected — not touched)
             MODULEJOURNEY_CONTENT_CHANGE   = FORBIDDEN (respected — ModuleJourney.js not touched)
             DB_FORMATIONS_MUTATION         = FORBIDDEN (respected — no backend file touched)
             DB_PROGRESS_MUTATION           = FORBIDDEN (respected — no backend file touched,
                                                           and PROGRESS_NOT_MUTATED is now a
                                                           standing E2E assertion, not just a claim)
             MODULE_CODE_REMAP              = FORBIDDEN (respected)
FAKE_PRODUCTION_DATA = FORBIDDEN — the fixture below is test-only, see its own header.
```

This tranche has two parts, in the order the human authorization required:
first the deterministic authenticated-surface test fixture ("avant cela"),
then the formation-discovery change it unblocks.

## Part 1 — Deterministic authenticated-surface fixture

`frontend/e2e/fixtures/auth-fixture.js` — a Playwright-only helper
(`mockAuthenticatedSession`) that installs a fake session entirely at the
network layer: `page.addInitScript` seeds `localStorage` tokens before
any app script runs, `page.route` intercepts `/api/auth/me`,
`/api/poles`, `/api/user/learning-path`, `/api/missions`,
`/api/badges/mine` with fixture JSON, and a broad `**/api/**` catch-all
returns `{}` for anything else. Nothing here touches a real backend,
database, or production code path — it is imported only by
`*.spec.js` files (grep-checkable), never by `frontend/src/**`.

This is what makes real `RUNTIME_PROOF` possible for an authenticated
screen in a sandbox with no reachable MongoDB or backend process (the
same constraint documented since W1-E) — previously, "authenticated
surface" work could only be proven by source inspection + build. It now
has actual browser-level proof, covering exactly the five items required
before touching any authenticated screen:

| Coverage item | Test | Result |
|---|---|---|
| `AUTHENTICATED_ROUTE` | fixture session reaches `/formations` for real, not a redirect | PASS |
| `KEYBOARD_FOCUS` | tabbing to a formation card marks it TARGET, others RECEDE, blur returns to IDLE | PASS |
| `REDUCED_MOTION` | focusing a card under emulated reduced motion still reaches its target transform | PASS |
| `RETURN_POSITION` | leaving `/formations` and returning resets the pole filter to its default — documented as the actual, pre-existing behavior (local `useState`, not persisted across unmount), not silently changed into a new persistence feature | PASS |
| `PROGRESS_NOT_MUTATED` | zero `POST`/`PUT`/`PATCH`/`DELETE` requests to any `/api/` endpoint observed while browsing the catalogue | PASS |

## Part 2 — Formation discovery: `CvlnFocusField` mounted for the first time

`CVLN_FOCUS_FIELD` (W2-C, `IMPLEMENTED_NOT_INTEGRATED` until now) is
mounted on `frontend/src/pages/Formations.js` in two places:

1. **Pole filter** — the already-existing `pole` selection `useState` is
   fed directly into `FocusFieldItem` as `focusedId` for each pole
   button (including "Tous les pôles"/`ALL`). No new state added; purely
   additive motion on top of the existing click-to-filter behavior.
2. **Formation cards** — a new `useFocusField()` instance
   (`cardFocus`) tracks which card has real DOM focus (`onFocus`/`onBlur`
   on the card's own `<Link>`, fired by keyboard tab or the click that's
   about to navigate — never `:hover`, `NO_GENERIC_SCALE_HOVER`). The
   focused card becomes TARGET (APPROACH), every other visible card
   becomes SECONDARY (RECEDE), and with nothing focused every card is
   IDLE (CALM).

## REQ_ID table

| REQ_ID | BEFORE | CHANGE | FILES | RUNTIME_PROOF | TEST | PERF | A11Y | REGRESSION | STATUS |
|---|---|---|---|---|---|---|---|---|---|
| SL-DISCOVERY-01 (pole filter FOCUS_FIELD) | Selected pole marked only by a color-class swap, no motion | Each pole button wrapped in `FocusFieldItem`, `focusedId={pole}` (existing state, reused) | `frontend/src/pages/Formations.js` | `data-focus-role="target"` on the selected pole's wrapper, `"secondary"` on the others, confirmed unchanged by hovering | `formations-discovery.spec.js` "pole filter … never via hover" | Negligible — opacity/transform only on ≤3 small buttons | No change — same buttons, same click handlers, same `data-testid`s | None — color class (existing signal) untouched | VERIFIED |
| SL-DISCOVERY-02 (formation card FOCUS_FIELD) | Cards had no focus/secondary relationship — a `group-hover:translate-x-1` on the arrow icon was the only motion, and it's untouched | Each card wrapped in `FocusFieldItem`; `onFocus`/`onBlur` on the card's own `<Link>` drive `cardFocus` | `Formations.js` | Tabbing to a card sets it TARGET and every other visible card SECONDARY; blurring returns all to IDLE; reduced motion still reaches the target transform | `formations-discovery.spec.js` "KEYBOARD_FOCUS" + "REDUCED_MOTION" (2 tests) | Negligible — opacity/transform on however many cards are visible (2-6 typically) | Focus/keyboard-nav path untouched (same `<Link>`, same tab order); the wrapper adds no new focusable element | None — additive; `RELATED_CONTEXT`/`FocusFieldContext` (REVEAL) deliberately **not** used this tranche, to keep the change to a controlled, minimal increment (`w2 doit rester une première intégration visible contrôlée`) | VERIFIED |
| SL-DISCOVERY-03 (data safety) | — | No backend file touched; no `db.formations`/`db.progress`/module-code/FMS-corpus file touched; `ModuleJourney.js` untouched | — | `PROGRESS_NOT_MUTATED` E2E: zero mutating requests during a full discovery interaction | `formations-discovery.spec.js` "PROGRESS_NOT_MUTATED" | — | — | — | VERIFIED |
| SL-DISCOVERY-04 (fixture, prerequisite) | No deterministic way to reach any authenticated screen in this sandbox at all (W1-E's honest limitation) | `e2e/fixtures/auth-fixture.js` — test-only, network-layer only | `frontend/e2e/fixtures/auth-fixture.js` | 6 new specs pass against a real authenticated render | `formations-discovery.spec.js` (all 6) | — | — | None — no production file references this fixture | VERIFIED |

## Test run (this tranche)

- `npx eslint src e2e playwright.config.js` → clean.
- `CI=true npx craco test --watchAll=false` → 13/13 Jest unit tests still passing (unrelated to this tranche, confirms no import-cycle break).
- `CI=true yarn build` → compiled successfully; `main.js` gzip effectively unchanged (`Formations.js` is a separate lazy-loaded chunk, not part of `main.js`).
- `npx playwright test` → **39/39 passing** (33 pre-existing specs re-run unmodified + 6 new in `formations-discovery.spec.js`).
- Backend regression (unchanged, confirming no drift): `black --check`, `isort --check`, `flake8`, `mypy --ignore-missing-imports` all clean (72 files); `pytest tests/ -n 0 --ignore=tests/backend_test.py` → 40/40 passing.

## Regression check

`git status --porcelain` before commit showed exactly 3 changes:
`frontend/src/pages/Formations.js` (modified), and 2 new files
(`frontend/e2e/fixtures/auth-fixture.js`,
`frontend/e2e/formations-discovery.spec.js`). No backend file, no
`db.formations`/`db.progress`/module-code/FMS-corpus file, no
`db.missions` file, no `ModuleJourney.js` touched.
