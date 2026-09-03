# W2-B — Landing Spatial Learning — REPORT

```
SURFACE = PUBLIC LANDING (frontend/src/pages/Landing.js) — the only
          surface authorized for this tranche
SCOPE   = 2 functional micro-interactions, not a visual redesign
```

Doctrine applied: `UNIVERSE_BEFORE_INTERFACE`, `LEARNING_FIRST_INTERFACE_
SECOND`, `ONE_DOMINANT_FOCUS`, `CALM_BY_DEFAULT`, `DEPTH_IS_SEMANTIC`,
`CONTINUITY_OVER_PAGE_CUT`.

## Deliberate restraint: 2 primitives used, 3 authorized ones not

The authorization allowed `FOCUS`, `APPROACH`, `RECEDE`, `REVEAL`,
`ENTER` — "uniquement si chaque mouvement a une fonction claire." Landing
has exactly two real state changes a visitor triggers: picking a
language, and switching between register/login mode. Nothing else on
this static page has a genuine interaction to attach motion to.

- **Used: `FOCUS`** — on the active language pill (marks it primary,
  nothing else).
- **Used: `ENTER`** — on the register/login mode swap (heading block +
  the conditionally-rendered `display_name` field).
- **Not used: `APPROACH`, `RECEDE`, `HORIZON`** (`HORIZON` was never in
  the authorized list for this tranche either). No element on Landing
  has a "secondary context that should recede while something else is
  approached" relationship — the manifesto and the auth card are two
  independent things a visitor reads, not a target/secondary pair.
  Forcing `APPROACH`/`RECEDE` onto them to check a box would be exactly
  the "decorative" motion the doctrine forbids. `CVLN_FOCUS_FIELD`
  (W2-C) is where that target/secondary/related-context pattern gets a
  real, reusable home — building an ad hoc version of it here first
  would duplicate that work.

`UNIVERSE_BEFORE_INTERFACE` / `LEARNING_FIRST_INTERFACE_SECOND` are
already satisfied structurally, unchanged by this tranche: the manifesto
column precedes the auth card in DOM order (so it reads first on mobile
single-column, and first in any assistive-technology reading order), and
this tranche didn't touch that structure — no page-load stagger
animation was added, because a generic "everything fades in on mount"
flourish is closer to decorative page-load spectacle than to a
function-driven movement, which would violate `CALM_BY_DEFAULT` in
spirit even while technically using an authorized primitive.

## REQ_ID table

| REQ_ID | BEFORE | CHANGE | FILES | RUNTIME_PROOF | TEST | PERF | A11Y | REGRESSION | STATUS |
|---|---|---|---|---|---|---|---|---|---|
| SL-LANDING-01 (FOCUS, language pill) | Active language marked only by a static color class (`bg-[--cvln-forest]`), no motion | Active pill wrapped in `<Focus active={lang === l.code}>` — adds a minor scale (1.015)/opacity emphasis on top of the existing color class, nothing replaced | `frontend/src/pages/Landing.js` | Clicking a pill measurably raises that pill's wrapper opacity (FOCUS's `active ? 1 : 0.92`) | `landing-spatial.spec.js` "active language pill is marked distinctly" | Negligible — 1 extra `motion.div` per pill (3 total), opacity/transform only, no reflow | No a11y change — button semantics, `data-testid`, click handler all unchanged | None — color class (existing signal) untouched, FOCUS is additive | VERIFIED |
| SL-LANDING-02 (ENTER, mode heading) | `mode === "register" ? … : …` — instant text swap, no transition | Eyebrow + `<h2>` + register-only hint wrapped in `<Enter key={mode} show>` — crossfades in on every mode toggle (and once on initial mount, see below) | `frontend/src/pages/Landing.js` | Heading settles at `opacity: 1` after toggling mode, including under emulated reduced motion (collapses to ~1ms, same end state) | `landing-spatial.spec.js` "mode toggle heading settles fully visible under reduced motion" | Negligible — text-only crossfade, 420ms (or 1ms reduced), no layout-affecting properties animated | No a11y regression — same DOM structure/text, just an opacity transition on the container | None | VERIFIED |
| SL-LANDING-03 (ENTER, display_name field) | `{mode === "register" && (<div>…</div>)}` — field pops in/out instantly with the rest of React's conditional render | Field's contents wrapped in `<Enter show>` for a fade-in on mount; **field itself stays a plain conditional render, not REVEAL-while-hidden** | `frontend/src/pages/Landing.js` | Login mode: field has `toHaveCount(0)` — fully absent from the DOM, not just visually hidden | `landing-spatial.spec.js` "switching to login mode removes the display_name field from the DOM entirely" + "switching back … focusable and required" + "login form … submits cleanly" (3 tests) | Negligible | **Regression avoided, not introduced**: a REVEAL-while-hidden implementation would have kept `required` active on an invisible input, which browsers still validate on submit — the login form would silently refuse to submit. The conditional-render + ENTER-on-mount pattern used here sidesteps that entirely (see explicit test) | None — same conditional-render safety as before, ENTER is purely additive on top | VERIFIED |
| Disclosed side-effect | — | Because default `mode` is `"register"`, `<Enter key="register" show>` also plays its fade-in on the very first page load (not just on later toggles), since `Enter`'s own `initial` prop always differs from `animate` on first mount | `Landing.js` | Confirmed in the reduced-motion test above (collapses to ~1ms) | covered by the same test | Bounded to ~420ms on two small text blocks in the auth card, not the whole page | No a11y impact (text still present in the DOM immediately, only its opacity animates) | None — disclosed here rather than hidden; does not violate `CALM_BY_DEFAULT`'s intent (short, restrained, scoped) even though it wasn't the primary intent of using `ENTER` | VERIFIED (disclosed) |

## Test run (this tranche)

- `npx eslint src e2e playwright.config.js` → clean.
- `CI=true npx craco test --watchAll=false` → 5/5 Jest unit tests still passing (unrelated to Landing, confirms no import-cycle break).
- `CI=true yarn build` → compiled successfully. `main.js` gzip: 167.5 kB → 167.81 kB (+0.31 kB) — trivial, as expected for two small wrapper usages.
- `npx playwright test` → **33/33 passing** (28 pre-existing specs re-run unmodified + 5 new in `landing-spatial.spec.js`).

## Regression check

`git status --porcelain` before commit showed exactly 2 files:
`frontend/src/pages/Landing.js` and the new spec file. No backend file,
no `db.formations`/`db.progress`/module-code/FMS-corpus file, no
`db.missions` file touched — this tranche only ever concerned the public,
pre-authentication Landing page.
