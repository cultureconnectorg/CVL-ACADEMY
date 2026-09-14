# ACA-0023 — Exact Return-to-Position, Camera/Rail/Focus Slice

```
STATUS: EXECUTED (2026-09-08). The scroll axis was already done
(useScrollRestoration.js). This closes the second axis that file's own
scope note deferred: "The camera/rail/focus axes are a real, separate
decision tied to whether the spatial engine is actually mounted in
production (ACA-0014, still flag-gated off)." ACA-0014/H1 mounted it;
this closes the dependency.
```

## What this closes

`useScrollRestoration.js` (built earlier this session) explicitly
scoped itself to the browser-history vertical scroll axis only, naming
the reason: restoring *which rail item had focus* and *the rail's own
horizontal scroll* only makes sense once a real, keyboard-navigable
rail exists in production — which it didn't until `SpatialHub.jsx`
(ACA-0014/H1) was mounted, flag-gated, behind `SPATIAL_HUB_ENABLED`.
That flag is still off by default, but the rail itself is now real
production code, so its own "where was I" memory can be built for real
instead of staying deferred.

## What was built

### `frontend/src/lib/railPositionRestoration.js` (new)
Pure, framework-free store — `saveRailPosition(key, {focusedKey,
scrollLeft})` / `getRailPosition(key)` / `clearRailPositions()` — keyed
by `location.key` (one entry per history entry, not per pathname),
LRU-capped at 50 entries, in-memory only. Deliberately the exact same
shape/discipline `scrollRestoration.js` already established (same
function names' pattern, same eviction logic, same "hard refresh starts
fresh" doctrine) — not a new pattern invented for this axis.

7 tests (`railPositionRestoration.test.js`), mirroring
`scrollRestoration.test.js`'s own test list line-for-line adapted to
the richer stored shape (object instead of a bare number).

### `frontend/src/components/SpatialHub.jsx`
- `focusedKey`'s initial state now checks `getRailPosition(location.key)`
  when `navType === "POP"` — if a saved key matches a real item still
  present in the current `items` list, that item is focused instead of
  the distance-0 default. A stale key (real data changed since) is
  ignored, never fabricated.
- A `railRef` on the rail's own scrollable container (the
  `overflow-x-auto` div, `data-testid="spatial-hub"`) is imperatively
  set to the saved `scrollLeft` on the same POP arrival — the axis
  `useScrollRestoration.js` never touches (that hook only manages
  `window.scrollY`).
- Every real focus change (keyboard arrow, click, or the restore itself)
  saves `{focusedKey, scrollLeft}` for the current `location.key` — the
  same "continuously remember, not just on an about-to-leave event"
  discipline `useScrollRestoration.js`'s own comment explains.

No new flag — this only ever runs where `SpatialHub` itself already
does, under the pre-existing `SPATIAL_HUB_ENABLED` gate.

## Verification

- `railPositionRestoration.test.js` — 7/7 passed.
- Full frontend unit suite: `CI=true npx craco test --watchAll=false`
  — **186/186 passed**, zero regressions.
- `npx eslint` on every touched file — clean.
- `CI=true yarn build` — clean.
- Full e2e regression: `npx playwright test e2e/` — **86/86 passed**
  (the full, now-green suite from ACA-0031 — SPATIAL_HUB_ENABLED off
  in this repo's e2e config, so this change is inert there, exactly as
  intended).
- **Real end-to-end proof against a live Chromium instance** (same
  technique as ACA-0015's camera-reveal proof, for the same reason —
  no committed e2e spec in this repo runs with `SPATIAL_HUB_ENABLED`
  on): `craco start` with the flag on, mocked auth + learning-path
  fixture (3 real rail items: FMS-01 unlocked, FMS-02/MKT-01 locked).
  Arrow-Right moved focus to `spatial-hub-node-formation-FMS-02`,
  Enter activated it (navigating to `/formations/FMS-02` — the
  existing "still real navigation" behavior for a locked item,
  unchanged), a real `page.goBack()` returned to `/dashboard`, and the
  exact same node (`spatial-hub-node-formation-FMS-02`) had focus
  again — confirmed via `document.activeElement`, not inferred.

## What remains open

- **Only `SpatialHub`'s own rail** gets this treatment. `Roadmap.js`/
  `Badges.js`/`Missions.js`/`FrekProfile.js` are depth-styled displays
  without an interactive, keyboard-navigable rail of their own
  (confirmed in the ACA-0018 audit: no `onFocus`/arrow-key handling on
  those pages) — there is no analogous "which item had focus" state to
  restore there yet.
- **ModuleJourney's own phase-stepper focus** (a different, page-local
  focus concept, not a cross-route rail) is untouched — out of this
  axis's scope.
