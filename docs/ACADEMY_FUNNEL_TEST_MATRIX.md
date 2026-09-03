# CVLN Academy — Funnel Test Matrix (W-FUNNEL-0)

```
DESIGN_ONLY — no test files added by this document. Maps the mission's
required scenarios (§35/36) against what already exists vs. what each
wave must add. "Real" here means: read directly from
frontend/e2e/*.spec.js this session, not assumed from a file name.
```

## Existing real coverage (11 specs, `frontend/e2e/`)

| Spec | Covers |
|---|---|
| `routing.spec.js` | canonical URLs, deep links |
| `auth-guards.spec.js` | unauthenticated redirect rules |
| `route-transition.spec.js` | `RouteTransition` behavior on redirect chains |
| `keyboard-focus.spec.js` | keyboard navigation, visible focus |
| `reduced-motion.spec.js` | `prefers-reduced-motion` compliance |
| `landing-spatial.spec.js` | Landing's 2 real motion primitives |
| `formations-discovery.spec.js` | Formations list/filter behavior |
| `module-journey-navigation.spec.js` | ModuleJourney routing |
| `module-journey-context.spec.js` | quiz/mission/mentor context entry/return |
| `module-journey-hierarchy.spec.js` | current/acquired/next/locked roles |
| `roadmap-progression.spec.js` | stage progression rendering |
| `mentor-presence.spec.js` | contextual (not floating) Mentor |

**Disclosed, load-bearing limitation** (from `playwright.config.js`'s
own header comment, re-confirmed this session): this sandbox has no
MongoDB/backend process, so **all 11 specs exercise unauthenticated or
frontend-only behavior**. No spec in this repository today logs in for
real and drives an authenticated journey end-to-end. This is the
single most important fact for interpreting every "tests: real" claim
in this document — real code, unverified end-to-end here.

## Required scenario matrix (mission §35)

| Scenario | Exists today | Gap | Target wave |
|---|---|---|---|
| New visitor → Landing → Signup → Onboarding → Activation → First Value | PARTIAL (routing/guards real; full round-trip needs a backend-enabled test env) | authenticated round-trip | W-FUNNEL-2 |
| Returning user → restored context → next action → module | MISSING | `RETURN_TO_POSITION` doesn't exist yet (product gap, not just test gap) | W-FUNNEL-6 |
| Learner → Module → Quiz → return exact position | PARTIAL (`module-journey-context.spec.js` covers context entry/return structurally) | needs a real backend to assert quiz submission + score | W-FUNNEL-4 |
| Learner → Module → Mission → return | PARTIAL (same pattern) | same | W-FUNNEL-4 |
| Progression → domain update → horizon update | MISSING | no test asserts a formation transitioning `locked→unlocked` | W-FUNNEL-7 |
| Paid path | N/A | correctly not tested — no backend exists; must stay untested until W-FUNNEL-5 produces a real (even if interface-only) capability, never faked | W-FUNNEL-5 |
| Fast nav `→→→→→` | EXISTS (H0.10 prototype level, Playwright-verified in `docs/SPATIAL_H10_PERCEPTUAL_REFINEMENT_REPORT.md`) | not yet ported to `frontend/src` | W-FUNNEL-1 (unit) + W-FUNNEL-3 (integration) |
| Reversal `→→←`, `→→→←←` | EXISTS (H0.10, same as above, including the substep-stability proof) | same porting gap | W-FUNNEL-1 |
| Back: browser Back, explicit Back | PARTIAL (H0.8/H0.9/H0.10 prototype proved this repeatedly; production app's own `route-transition.spec.js` covers redirect chains only, not a real content-to-content back) | production coverage | W-FUNNEL-3 |
| Mobile: swipe, snap, context sheet, return | EXISTS (H0.9/H0.10 prototype, Playwright-verified) | porting gap | W-FUNNEL-3/4 |
| Accessibility: keyboard, reduced motion, focus restore, screen-reader semantics | PARTIAL — keyboard/reduced-motion real and tested; focus-restore real and tested in ModuleJourney context only; **no screen-reader semantic assertions found in any existing spec** (Playwright can assert ARIA roles/attributes but none of the 11 specs currently do) | screen-reader assertions | every wave, starting W-FUNNEL-1 |
| Failure: network error, API error, stale recommendation, unauthorized | MISSING | no failure-path spec found in `frontend/e2e/` | every wave introducing a new network call must add its own |
| Payment failure | N/A | correctly not applicable — no payment exists | W-FUNNEL-5, once interfaces exist |

## Visual regression (mission §36)

No existing screenshot-diffing infrastructure found in `frontend/` (no
`percy`, `chromatic`, or Playwright `toHaveScreenshot` baseline files
located). The H0.x prototype lineage's own screenshot-gallery method
(Playwright capture → published artifact gallery, used for every H0.5
through H0.10 report) is a real, proven *process* but has never been
pointed at `frontend/src` — every wave from W-FUNNEL-2 onward should
capture before/after frames (desktop + mobile) for its touched surfaces
using that same method, stored the same way (published gallery per
wave, referenced from that wave's own report), rather than inventing a
new visual-regression tool.

For camera transitions specifically: the `?slowmo=N` deterministic
capture hook (H0.8, reused unchanged through H0.10) is the proven
method for the required 0/20/40/60/80/100% sequences — port the query
param convention alongside the physics extraction in W-FUNNEL-1, don't
rebuild it.

## Test debt acknowledged, not hidden

- No backend-enabled test environment exists in this sandbox — closing
  this is a prerequisite for W-FUNNEL-2 onward to claim real
  authenticated-flow coverage, not something any single wave can fix
  from the frontend side alone.
- No accessibility screen-reader semantic assertions exist today,
  despite 5 waves of prior spatial work (H0.5–H0.10, W1–W4) each
  claiming accessibility compliance — those claims rest on structural/
  DOM inspection (documented explicitly as such in every report), never
  an actual AT (NVDA/VoiceOver) pass. This gap is real and should be
  named in every future report rather than allowed to look closed by
  omission.
