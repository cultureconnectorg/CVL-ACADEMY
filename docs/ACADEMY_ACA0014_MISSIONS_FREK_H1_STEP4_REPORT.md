# ACA-0014/ACA-0017 — H1 Sequencing Step 4 (Missions, FREK Profile), Implementation Report

```
STATUS: implemented, gated behind the existing SPATIAL_HUB_ENABLED
flag (already off by default). Missions.js and FrekProfile.js render
exactly today's production behavior until that flag is deliberately
turned on.
```

## What this closes

`docs/SPATIAL_H1_INTEGRATION_PLAN.md`'s sequencing step 4, completing
it: **Missions** and **FREK Profile** — the last two of "Missions/
Badges/FREK EXTEND (smallest, most isolated pages)". Badges was closed
in the previous commit (`ACADEMY_ACA0014_BADGES_H1_STEP4_REPORT.md`).

- Missions verdict: *"Convert from its current presentation to the
  glanceable-list treatment validated here (no card grid). Real
  mission data/status already exists server-side; only the render
  changes."*
- FREK Profile verdict: *"Convert to the identity-first, non-KPI-card
  treatment; real FREK-ID and stage already exist as data."*

## What was built

`frontend/src/pages/Missions.js`:

- `MissionDepthCard`/`MissionCardBody` — same `useDepthPhysics` +
  `computeDepthStyle` wrapper pattern Roadmap/Badges already
  established, applied to a **vertical list** (`flex flex-col`)
  instead of the `grid-cols-1 md:grid-cols-2` card grid — the plan's
  own "no card grid" instruction, and PS5's "cards, not pages"
  principle already cited in `ACADEMY_HERO_ENTRY_RESEARCH.md` §C: one
  dominant, actionable thing, the rest genuinely present but
  secondary.
- Real anchor: a mission already `accepted` (ready to submit — the
  single most actionable real commitment) takes primary attention;
  absent one, the first not-yet-accepted mission does. Both read only
  the real `status`/`status_type` fields already fetched — no ranking
  data invented.

`frontend/src/pages/FrekProfile.js`:

- The identity card (FREK-ID, display name, stade, CC) was already
  identity-first before this pass — untouched. What the plan's
  "non-KPI-card" verdict targets is the **signals grid** below it (8
  uniformly-weighted stat tiles).
- `SignalDepthCard` — same engine, applied to that grid: the signal
  with the real highest count becomes the primary target (the
  learner's own most-active real trait); an all-zero fresh account
  falls back to no forced primary, same edge case every prior page in
  this sequence already accepts.

Both reuse `FEATURE_FLAGS.SPATIAL_HUB_ENABLED` — no new flag, same
production gate Dashboard/Roadmap/ModuleJourney/Badges already share.

## Verification

- `CI=true yarn build` — compiled successfully after each file, zero
  new warnings.
- `npx eslint src/pages/Missions.js src/pages/FrekProfile.js` — clean.
- Full Playwright suite (`e2e/`, 83 specs) — **82/83 passed**, same
  single pre-existing failure already confirmed unrelated in the
  Badges report (`module-journey-navigation.spec.js` back/forward
  restoration — fails identically on the base commit, untouched by
  this diff, and not part of this repo's CI gate).

## H1 sequencing status (updated)

Step 4 is now fully executed: Dashboard (WRAP), Roadmap/ModuleJourney
(EXTEND, Rails 3/5), Badges/Missions/FREK Profile (EXTEND, this pass
and the prior commit). Remaining, still `NOT_AUTHORIZED` per the plan:
step 5 — the two `REPLACE-BLOCKED` items (Formation-card→Module FLIP
extension, environmental asset upgrade) — plus the mobile-swipe
`useSwipeRail()` promotion, each needing its own explicit go-ahead.

## Never claim

Not `FULLY_COMPLETE` H1. Every `REPLACE-BLOCKED` item keeps its own
required review per the plan's own terms; ACA-0013/0015/0016/0018
remain open, separate backlog items.
