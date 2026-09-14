# ACA-0012 — Onboarding Spatialization, Implementation Report

```
STATUS: implemented, flag-gated OFF by default
(REACT_APP_ACADEMY_SPATIAL_ONBOARDING_ENTRY). Onboarding.js renders
exactly today's production behavior (plain CSS .fade-in per step,
flat-orange progress bar) until this flag is deliberately turned on.
```

## What this closes

Grep-confirmed before this pass: `frontend/src/pages/Onboarding.js`
imported no motion primitive at all — its 5-step wizard (`lang →
metier → territoire → objectif → recap`) swapped steps via a plain
conditional render wrapped in a static `.fade-in` CSS keyframe (already
reduced-motion-safe via the W1-A global media query, but not a real
spatial primitive, and carrying no continuity between steps). The
progress bar was a flat, always-orange fill.

## What was built

`frontend/src/pages/Onboarding.js`:

- `StepShell` now renders through the real `Enter` primitive
  (`lib/motion-primitives.jsx`, `CONTINUITY_OVER_PAGE_CUT`) when
  `SPATIAL_ONBOARDING_ENTRY` is on, `key`ed by `testId` so each step
  change re-triggers a calm crossfade instead of an abrupt swap — the
  same mechanism already used for Landing's register/login mode switch
  (W2-B) and its auth-card commit (ACA-0011).
- Once the learner picks a real métier (step 1), that métier's real
  backend `color` (`options.metiers[].color` — already fetched from
  `GET /onboarding/options`, never invented) becomes a persistent
  signature for the rest of the flow: the progress-bar fill and a
  restrained radial-gradient backdrop behind the step content both
  tint to it, using the identical mechanism `AcademyBackdrop.jsx`
  (RAIL3-05) already established for the authenticated shell (real
  pole color, `12` alpha hex suffix, purely decorative).
- **Deliberately not done**: no territoire- or objectif-derived visual
  of any kind. The research doctrine this repo has followed throughout
  (`ACADEMY_HERO_ENTRY_RESEARCH.md` §5-6, restated in every ACA-0010/
  0011 report) explicitly forbids fabricating personalization beyond
  what a real field commit supports — territoire and objectif are free
  text/choice with no backend-supplied visual attribute to ground a
  tint in, so none was invented.
- New flag: `FEATURE_FLAGS.SPATIAL_ONBOARDING_ENTRY`
  (`REACT_APP_ACADEMY_SPATIAL_ONBOARDING_ENTRY`), off by default.

## Verification

- `CI=true yarn build` — compiled successfully, zero new warnings.
- `npx eslint src/pages/Onboarding.js src/lib/featureFlags.js` — clean.
- Full relevant Playwright suite (31 tests, including `auth-guards`
  which covers the `/onboarding` protected-route redirect) —
  **31/31 passed** at the flag's default (off).
- The flag-on step sequence itself is not covered by a new e2e test:
  reaching Onboarding at all requires an authenticated session, which
  (same disclosed limitation as every prior ACA report and
  `e2e/README.md`) this sandbox's backend-less Playwright config
  cannot reach either before or after this change.

## Never claim

Not `FULLY_COMPLETE`. ACA-0013 (Activation/first-value
instrumentation), the flag's own eventual production activation with
real authenticated e2e coverage, and any richer territoire-specific
treatment (only if a real backend attribute is added to ground it in)
all remain open, separate backlog items.
