# ACA-0018 — Audio/Haptics Calibration on Real Production Surfaces

```
STATUS: EXECUTED (2026-09-08), scoped. Gated behind the existing
SPATIAL_AUDIO/SPATIAL_HAPTICS flags (both default off) — zero
behavioral change until deliberately turned on.
```

## What this closes

`lib/spatial/audio.js`/`lib/spatial/haptics.js` (W-FUNNEL-1) were real,
tested infrastructure (8 named tone events, 5 haptic patterns, muted-
by-default opt-in) but per their own docstrings, "not wired into any
real product surface" at extraction time. RAIL3-08 wired them into
`SpatialHub.jsx` (Dashboard) and Rail 5 wired a `CONFIRM`-only usage
into `ModuleJourney.js`. This pass audits every remaining
`SPATIAL_HUB_ENABLED`-gated H1 surface and wires the same real-
completion `CONFIRM` pattern wherever a genuine user-triggered
completion actually exists.

## What was built

### `frontend/src/pages/Missions.js`
`submit(code)` (`POST /missions/{code}/submit`) — the real completion
moment (a real CC reward, `refreshMe()` reflects the actual credited
balance) — now calls `audioRef.current.play("CONFIRM")` /
`hapticsRef.current.fire("CONFIRM")`, same instantiation pattern as
`ModuleJourney.js`'s existing wiring (`createSpatialAudio()`/
`createHaptics()`, refs so the instance survives re-renders), gated by
`FEATURE_FLAGS.SPATIAL_HUB_ENABLED && FEATURE_FLAGS.SPATIAL_AUDIO` /
`... && SPATIAL_HAPTICS` — the same flag this page's own depth engine
already uses, no new flag introduced.

`accept(code)` is deliberately **not** wired: it's a lighter commitment
(agreeing to attempt a mission), not a completion — the same
distinction `ModuleJourney.js` already draws by firing `CONFIRM` only
on quiz-pass/mini-mission-commit, never on opening a phase.

## What was audited and found to have no real hook (disclosed, not a gap)

- **`Roadmap.js`, `Badges.js`, `FrekProfile.js`** — all three are
  read-only displays of already-computed server data (stage list, badge
  earned/unearned, signal counts). None has a user-triggered `onClick`/
  `api.post` action anywhere in the file (verified by direct grep: zero
  matches). Wiring `CONFIRM`/`BLOCKED` to any interaction on these pages
  would mean inventing an event with no real underlying action —
  exactly what this codebase's audio/haptics doctrine forbids ("never
  fake support," extended here to "never fake a completion"). No code
  change was made to these three files.
- **`NAV_MOVE`/`FOCUS_LOCK`** (the rail-navigation events `SpatialHub.
  jsx` fires on keyboard/pointer index changes) do not apply outside
  `SpatialHub` itself: none of Roadmap/Badges/Missions/FrekProfile has
  an interactive, arrow-key-driven rail — their `currentIdx`/
  `primaryIdx` is derived once from real data, not moved by user input.
  Firing a "navigation" sound on a page with no navigable rail would be
  the same kind of fabrication.

## Verification

- `npx eslint src/pages/Missions.js` — clean.
- `CI=true yarn build` — compiled successfully, zero new warnings.
- Full Playwright suite (`e2e/`, 86 specs) — **85/86 passed**, the one
  failure (`module-journey-navigation.spec.js`'s back/forward test) is
  the same pre-existing, confirmed-unrelated flake documented in every
  prior report this session (not part of this repo's CI gate — only
  `backend` flake8+pytest and `frontend` build run there).
- No new automated test added for this specific wiring: `audio.test.js`/
  `haptics.test.js` already cover `createSpatialAudio`/`createHaptics`
  themselves at the unit level, and `ModuleJourney.js`'s equivalent
  `CONFIRM` wiring (Rail 5) carries no dedicated test either — this
  keeps the same verification rigor already established for that
  precedent rather than introducing an inconsistent new bar.

## What remains open

- Audio/haptics on Roadmap/Badges/FrekProfile stays genuinely
  inapplicable unless one of those pages gains a real interactive
  action in a future pass (e.g. if Badges ever gains a claim/share
  button) — tracked as a future trigger, not a current gap.
- ACA-0015's camera-follow `CROSSING`/`REVEALING` phases (still
  unwired) will eventually want their own `ENTER_DEPTH`/`RETURN_DEPTH`
  audio cues — `audio.js` already defines those events but nothing
  calls them yet; out of scope here since the camera wiring itself
  isn't built.
