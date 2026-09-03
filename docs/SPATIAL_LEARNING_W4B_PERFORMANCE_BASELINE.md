# W4-B — Performance Baseline — REPORT

```
Measured against: the real production build (`yarn build` + `serve -s
  build`, minified + gzip, no dev-server overhead) unless a row says
  "dev server" explicitly, in which case it's flagged as noise and not
  used for any conclusion.
Method: Playwright (Chromium) + the browser's own Performance API
  (paint timing, PerformanceObserver for longtask/layout-shift), plus a
  source-map byte breakdown of main.js. No third-party APM, no
  fabricated numbers — every figure below came from an actual run this
  session, reproducible with the commands shown.
```

## 1. Bundle breakdown — what the 129.24 kB → 168.56 kB growth actually is

`main.js` gzip size across the session, by commit:

| Point | Size | Δ | Cause |
|---|---|---|---|
| Before W2 (baseline) | 129.24 kB | — | `framer-motion` installed but fully dead-code-eliminated (confirmed in the W0 audit) |
| After W2-A | 167.5 kB | **+38.26 kB** | `RouteTransition` mounted around `<Routes>` → `AnimatePresence`/the animation engine become reachable for the first time |
| After W2-B | 167.81 kB | +0.31 kB | 2 small `FocusFieldItem`/`Enter` usages on Landing |
| After W3-B | 168.53 kB | +0.72 kB | `MentorPanel` (now `ContextFrame`-driven) is imported synchronously by `Layout.js` |
| After W3-C | 168.59 kB | +60 B | `mentorPresence.js` gating logic |
| After W3-D | 168.56 kB | −27 B | trimmed `i18n.jsx` strings (`level_word` removed) |
| **Current (W3-E)** | **168.56 kB** | **+39.32 kB total (+30.4%)** | |

**97% of the total growth (38.26 of 39.32 kB) happened in one single
event: W2-A.** Everything after that added low-single-digit KB or less,
because `framer-motion`'s runtime was already paid for.

### Where the bytes actually are (source-map byte attribution)

`main.js`'s embedded source map (370 modules, `sourcesContent` present)
gives an exact, non-estimated breakdown of **uncompressed source bytes**
reachable from the entry bundle:

| Category | Uncompressed source bytes | Share | Files |
|---|---|---|---|
| `react-dom` | 518,375 | 29.6% | 4 — pre-existing, unaffected by Spatial Learning |
| **`framer-motion` (+ `motion-dom` + `motion-utils`)** | **421,255** | **24.0%** | 218 — **the actual new contributor** |
| `react-router` | 366,110 | 20.9% | 1 — pre-existing |
| `axios` | 132,610 | 7.6% | 48 — pre-existing |
| `@tanstack/query-core` | 83,604 | 4.8% | 13 — pre-existing |
| **Our own `src/lib` Spatial Learning code** | **80,119** | **4.6%** | **10 files**: `motion-tokens.js`, `motion-primitives.jsx`, `useReducedMotion.js`, `RouteTransition.jsx`, `spatial-state.js`, `useSpatialState.js`, `CvlnFocusField.jsx`, `JourneyHierarchy.jsx`, `ContextFrame.jsx`, `mentorPresence.js` |
| `sonner` (toast library) | 65,406 | 3.7% | pre-existing |
| everything else (`iconoir-react`, `react`, `scheduler`, our `src/components`, app shell) | ~64,000 | 3.6% | |

**Conclusion, stated precisely**: `react-dom`/`react-router`/`axios`/
`@tanstack/query-core` were already fully present before W2 — none of
that is new. The measured +38.26 kB gzip is attributable to
`framer-motion` becoming reachable (421 KB of uncompressed source, the
single largest *new* contributor) plus our own 10 authored files (80 KB
uncompressed — small, and already unit-tested logic, not bloat).

### What can actually be lazy-loaded or isolated — concrete, actionable

- **`RouteTransition` cannot be deferred.** It wraps `<Routes>` itself —
  lazy-loading the thing that renders every page would either block the
  very first paint behind an extra chunk fetch, or require rendering
  without it on first load (defeating its purpose). `framer-motion`
  being pulled in at the App-shell level is therefore **structural, not
  a mistake** — as long as any route-level transition exists, this cost
  is paid once, up front, for the whole app.
- **`MentorPanel` is a real, fixable gap.** `Layout.js` still does a
  *static* `import MentorPanel from "@/components/MentorPanel"` even
  though, since W3-C, it's only ever *rendered* inside `ModuleJourney`.
  A static import is bundled regardless of whether it renders — React
  needs `React.lazy(() => import(...))` to actually defer the code.
  Converting this one import would move `MentorPanel`'s own weight
  (small — the component itself, not `framer-motion`, which is already
  paid for by `RouteTransition` either way) out of every Protected
  page's initial synchronous bundle and into `ModuleJourney`'s own lazy
  chunk, where it belongs. **Concrete, low-risk, not yet done.**
- **`framer-motion` itself ships a smaller surface than what's
  imported.** The installed package (`node_modules/framer-motion`,
  v11.18.0) includes `dist/dom-mini.js`/`dist/mini.js` — a
  deliberately-reduced build for basic `animate`/`AnimatePresence` use
  without the full gesture/drag/layout-animation engine. Every usage in
  this codebase (`motion-primitives.jsx`, `CvlnFocusField.jsx`,
  `JourneyHierarchy.jsx`, `ContextFrame.jsx`, `RouteTransition.jsx`) only
  ever uses `motion.div` + `animate`/`initial`/`transition` +
  `AnimatePresence` — **no drag, no gestures, no `layout` prop**. All of
  it currently imports from the full `"framer-motion"` package. Switching
  to the mini entry point is a genuine, unexplored size-reduction lever
  — not evaluated in this discovery pass (would need a compatibility
  check against `AnimatePresence` specifically), but the single biggest
  concrete lead this audit found for shrinking the 421 KB figure above.

## 2. Real measurements (production build, Chromium, this session)

| Metric | Landing desktop | Landing mobile (390×844) | ModuleJourney desktop (fixture-authenticated) | ModuleJourney mobile |
|---|---|---|---|---|
| First Paint | 296 ms | 364 ms | 348 ms | — |
| First Contentful Paint | 328 ms | 380 ms | 436 ms | — |
| Cumulative Layout Shift | **0** | **0** | **0** | **0** |
| Horizontal overflow at mobile viewport | — | **none** | — | **none** |
| Long tasks (>50ms) during load | none | none | none | none |

**CLS = 0 on every surface measured, desktop and mobile, is the single
strongest finding in this report**: nothing shipped in W2/W3 causes a
layout-shifting reflow — consistent with the project-wide discipline
(enforced since W1-B) of animating only `opacity`/`scale`/`transform`/
`filter`, never `width`/`height`/`margin`/layout-affecting properties.

### Route-transition cost

| Scenario | Wall-clock (production build) |
|---|---|
| Normal motion (redirect chain: unknown path → `/`) | 415 ms |
| Reduced motion (same redirect chain, `prefers-reduced-motion: reduce` emulated) | 362 ms |

The normal-motion figure (415 ms) sits almost exactly on the `ENTER`
motion token's own designed duration (420 ms, `motion-tokens.js`) —
**the measured cost matches the specified cost**, which is itself the
useful finding. The reduced-motion figure did **not** collapse
proportionally (362 ms vs. the ~1 ms token) because this wall-clock
measurement is dominated by `page.goto()`'s own full top-level
navigation (fresh document parse/JS execution) for this specific
redirect-chain scenario, not by the CSS/motion transition itself, which
*is* separately and directly proven to collapse to ~1ms at the DOM level
(`reduced-motion.spec.js`, `route-transition.spec.js` — both already
part of the committed E2E suite). Stated plainly: this specific
wall-clock method isn't a clean instrument for isolating the animation's
own cost from page-load noise; the E2E suite's direct `getComputedStyle`
assertions remain the authoritative reduced-motion proof.

### Interaction long tasks (production build)

| Interaction | Long task observed |
|---|---|
| Opening two ModuleJourney phases in sequence (course, then objectives) | 65 ms |
| Focusing two Formations cards in sequence (`FocusFieldItem` role change) | 61 ms |

Both are just over the 50ms "long task" threshold — real, honestly
reported, but modest (not tens or hundreds of milliseconds) and most
plausibly attributable to React's own re-render/DOM-diff work for the
whole page on a state change, not specifically to the animation. A first
same-scenario pass against the **unminified dev server** (not reported
as a finding, only as a sanity check) showed 210–221 ms for the same
interactions — a **3.2–3.6× reduction in the real production build**,
confirming those higher dev-server numbers were tooling noise, not a
production-relevant signal, and correctly excluded from this report's
conclusions.

## 3. What this audit could not measure in this sandbox

- **True FPS during a transition** — headless Chromium doesn't expose a
  reliable frame-timing API distinct from `requestAnimationFrame`
  counting, and that method proved fragile across a real page
  navigation (the execution context resets mid-`goto`, see the raw
  script's own failed first attempt). The `getComputedStyle`-based E2E
  assertions already in the suite (opacity/transform settling correctly)
  remain the actual proof of correctness; true frame-rate profiling
  would need a real browser + DevTools Performance panel, not available
  headless here.
- **CPU/device-constrained throttling** — Playwright supports CPU
  throttling via CDP, but reproducing a *specific* target device's real
  constraints (e.g. a low-end Android CPU) credibly, rather than an
  arbitrary throttle multiplier, needs a real device lab or a
  calibrated throttling profile — out of scope for this discovery pass.

## Conclusion feeding into W4-D

Nothing measured here — bundle size, paint timing, CLS, long tasks, or
route-transition cost — points at a DOM/CSS/`framer-motion` performance
ceiling. The dominant cost (`framer-motion` reachable via
`RouteTransition`) is a one-time, structural, already-paid cost with a
concrete, unexplored reduction lever (the `mini`/`dom-mini` entry
point). CLS is zero everywhere. This is further evidence for W4-D's
`NO_WEBGL_REQUIRED` conclusion — the current stack has real, identified,
*fixable* inefficiencies, not a technology ceiling.
