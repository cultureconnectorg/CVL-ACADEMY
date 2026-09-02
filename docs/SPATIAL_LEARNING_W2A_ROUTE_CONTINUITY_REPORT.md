# W2-A — Route Continuity Integration — REPORT

```
STATUS_BEFORE = W1-C: IMPLEMENTED_NOT_INTEGRATED (RouteTransition existed, 0 imports)
STATUS_AFTER  = W2-A: MOUNTED + RUNTIME_VERIFIED (App.js wires it around <Routes>)
```

`RouteTransition` (built unmounted in W1-C) is now the only change to
`frontend/src/App.js`: it wraps `<Routes>` exactly at the integration
point the component's own docstring specified — no other line in
`App.js` changed. `BrowserRouter`, `Protected`, and every `<Route>`
definition are untouched.

| REQ_ID | BEFORE | CHANGE | FILES | RUNTIME_PROOF | TEST | PERF | A11Y | REGRESSION | STATUS |
|---|---|---|---|---|---|---|---|---|---|
| MOT-013 (continuous route transition) | `RouteTransition` existed, unimported, 0 runtime effect | Mounted around `<Routes>` in `App.js`; `RouteTransition.jsx` docstring updated to reflect it's live, not speculative | `frontend/src/App.js`, `frontend/src/lib/RouteTransition.jsx` | `main.js` gzip grew 129.24 kB → 167.5 kB (framer-motion's `AnimatePresence` code path is now actually bundled and executing, not tree-shaken) | 5 new specs (`e2e/route-transition.spec.js`) + all 18 pre-existing W1-E specs re-run against the *mounted* wrapper (they were previously only proving the wrapper's absence didn't break anything) | No layout thrash — opacity-only transition, no reflow-triggering properties animated | Reduced-motion still respected (see below) | See regression table | **VERIFIED** (was `IMPLEMENTED_NOT_INTEGRATED`) |
| ROUT-SAFETY: `BrowserRouter` preserved | — | No change to `BrowserRouter` | `App.js` (0 lines changed in this region) | `routing.spec.js` "canonical root URL" + "hard refresh" still pass unmodified | re-run, 4/4 pass | — | — | none | VERIFIED |
| ROUT-SAFETY: `Protected` preserved | — | No change to `Protected` | `App.js` (0 lines changed in this region) | `auth-guards.spec.js`: all 14 protected paths still redirect | re-run, 14/14 pass | — | — | none | VERIFIED |
| ROUT-SAFETY: canonical URLs preserved | — | — | — | new: redirect chains land on exactly `/` with empty `search`/`hash` (no stray query/hash from the `Navigate` chain) | `route-transition.spec.js` "canonical URL after a redirect chain" | — | — | none | VERIFIED |
| ROUT-SAFETY: deep links preserved | — | — | — | `routing.spec.js` "unknown deep link redirects to /" still passes with the wrapper mounted | re-run, pass | — | — | none | VERIFIED |
| ROUT-SAFETY: refresh preserved | — | — | — | `routing.spec.js` "hard refresh re-renders, no crash" still passes | re-run, pass | — | — | none | VERIFIED |
| ROUT-SAFETY: back/forward preserved | — | — | — | `routing.spec.js` "browser back returns to previous canonical URL" still passes | re-run, pass | — | — | none | VERIFIED |
| ROUT-SAFETY: auth redirects preserved + settle correctly | — | — | — | new: a client-side redirect (protected/role-gated/unknown path → `/`) settles at `opacity: 1`, never stuck mid-fade or on the Suspense fallback | `route-transition.spec.js` 2 tests | — | — | none | VERIFIED |
| MOT-029 (reduced motion, now live) | CSS-level only (W1-A) + unmounted JS hook (W1-B) | `RouteTransition` itself now consults `useReducedMotion()` at runtime for every real transition | `RouteTransition.jsx` (unchanged logic, now executing) | new: with `page.emulateMedia({reducedMotion:'reduce'})`, the same redirect settles fully visible just as fast | `route-transition.spec.js` "reduced motion: … still settles fully visible" | — | Confirms the reduced-motion path isn't just theoretical once real navigation exercises it | none | VERIFIED |
| No navigation hijacking | — | Verified by construction: no `history`/`navigate` call anywhere in `RouteTransition.jsx` | `RouteTransition.jsx` (source inspection) | — | — | — | — | — | VERIFIED (source) |
| No scroll hijacking | — | Verified by construction (no scroll API in `RouteTransition.jsx`) **and** at runtime | — | new: `window.scrollY` identical before/after a client-side redirect | `route-transition.spec.js` "no scroll hijacking" | — | — | none | VERIFIED |

## Test run (this tranche)

- `npx eslint src e2e playwright.config.js` → clean.
- `CI=true npx craco test --watchAll=false` → 5/5 Jest unit tests still passing (unaffected — `App.js`/`RouteTransition.jsx` have no unit-test coverage of their own, this confirms no import-cycle break).
- `CI=true yarn build` → compiled successfully. `main.js` gzip: **129.24 kB → 167.5 kB** (+38.26 kB) — the expected, honest cost of `framer-motion`'s `AnimatePresence` now actually running instead of being dead code; documented here rather than left silent since it's the first real perf-relevant change of the whole Spatial Learning effort.
- `npx playwright test` → **28/28 passing** (18 pre-existing W1-E specs re-run against the mounted wrapper + 5 new W2-A specs in `route-transition.spec.js`).

## What "real navigation" means in this proof, honestly stated

Every URL hit via `page.goto()` in these specs is a genuine browser page
load (React mounts fresh) — but the *redirect* that follows (unknown
path → `/`, protected/role-gated path → `/`) happens entirely inside the
already-mounted SPA via React Router's `<Navigate>`, with no further
browser navigation event. That redirect is exactly the client-side,
`AnimatePresence`-driven crossfade this wave adds, and it is what's
actually exercised and asserted here (settled opacity, canonical URL,
scroll position, Suspense fallback not stuck). What is **not** exercised
— for the same reason as W1-E: no backend/MongoDB in this sandbox — is a
click-driven `<Link>` navigation between two distinct authenticated
pages (e.g. sidebar navigation inside `Layout`). That remains open for
whichever wave first reaches an authenticated surface with real E2E
coverage (see the pending "deterministic test fixture for authenticated
surfaces" item).

## Regression check

`git status --porcelain` before commit showed exactly 3 files: `App.js`,
`RouteTransition.jsx`, and the new spec file. No backend file, no
`db.formations`/`db.progress`/module-code/FMS-corpus file, no
`db.missions` file touched. `DB_FORMATIONS_MUTATION`,
`DB_PROGRESS_MUTATION`, `MODULE_CODE_REMAP`, `BACKEND_CONTRACT_CHANGE`
all still respected (none of those files were in scope for this
tranche at all).
