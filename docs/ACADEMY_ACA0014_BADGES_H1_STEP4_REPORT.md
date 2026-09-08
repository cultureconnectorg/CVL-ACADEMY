# ACA-0014/ACA-0017 — H1 Sequencing Step 4 (Badges), Implementation Report

```
STATUS: implemented, gated behind the existing SPATIAL_HUB_ENABLED
flag (already off by default). Badges.js renders exactly today's
production behavior (uniform card grid) until that flag is
deliberately turned on.
```

## What this closes

`docs/SPATIAL_H1_INTEGRATION_PLAN.md`'s own sequencing recommendation,
step 4 ("Missions/Badges/FREK EXTEND — smallest, most isolated
pages"), for the **Badges** row specifically: *"Convert to the
glanceable-cluster treatment; earned/unearned already exists as real
data."* Steps 1-3 (motion primitives, Dashboard WRAP, Roadmap/
ModuleJourney EXTEND) were already executed in Rails 3-5.

Before this pass, `Badges.js` rendered every badge in a uniform
`grid-cols-2 md:grid-cols-4` grid — earned/unearned distinguished only
by opacity/grayscale, no attention hierarchy, no reuse of the
already-built continuous-depth engine.

## What was built

`frontend/src/pages/Badges.js`:

- `BadgeDepthCard` — the exact same `useDepthPhysics` +
  `computeDepthStyle` wrapper `Roadmap.js`'s `StageDepthCard`
  established in Rail 3, ported verbatim rather than re-derived (same
  rAF spring engine, same 6-channel perceptual-occlusion styling).
- The real "what matters now" anchor (`primaryIdx`): the first
  not-yet-owned badge, in the array's own real `cc_threshold` order —
  the genuinely relevant next target, exactly the Spotify-pattern
  "ranked now slot" principle already applied to Dashboard/Roadmap.
  All-earned or no-data-yet falls back to `-1` (no forced primary),
  the same edge case `Roadmap.js` already accepts for a stade-less
  user — not a new behavior invented for this page.
- `BadgeCardBody` — the shared markup both the plain-grid and
  continuous-depth wrappers render, so the two treatments can never
  drift in content, only in motion (same discipline as `Roadmap.js`'s
  `StageCardBody`).
- **No new flag.** Reuses `FEATURE_FLAGS.SPATIAL_HUB_ENABLED` —
  already the real production gate for this exact attention/physics
  engine on Dashboard/Roadmap; its docstring in `featureFlags.js` is
  updated to note Badges now shares it, rather than fragmenting one
  engine's activation across per-page flags.

## Verification

- `CI=true yarn build` — compiled successfully, zero new warnings.
- `npx eslint src/pages/Badges.js` — clean.
- Full Playwright suite (`e2e/`, 83 specs) — **82/83 passed.** The one
  failure (`module-journey-navigation.spec.js` — back/forward state
  restoration) is confirmed pre-existing and unrelated: it fails
  identically on the base commit (`800de83`, before this change) with
  `git stash` isolating the Badges/featureFlags diff, and
  `module-journey-navigation.spec.js` is untouched by this pass.
  Playwright/e2e is not part of this repo's GitHub Actions CI gate
  (only `backend` flake8+pytest and `frontend` build run there), so
  this pre-existing flake does not affect PR mergeability — flagged
  here rather than silently worked around.

## Never claim

Not `FULLY_COMPLETE` H1. Missions and FrekProfile (the rest of step 4)
remain open, as do ACA-0013/0015/0016/0018 and every `REPLACE-BLOCKED`
item in the H1 plan (Formation-card→Module FLIP extension,
environmental asset upgrade) — those keep their own required
go-ahead per the plan's own terms, not implied by this step's
completion.
