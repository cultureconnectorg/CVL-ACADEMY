# ADR W5 — WebGL Reopened

```
STATUS: DECIDED — supersedes docs/ADR_W4_WEBGL_DECISION.md's conclusion
        (NO_WEBGL_REQUIRED) for the background/world layer only.
DATE: 2026-09-14
AUTHORIZED BY: Founder, explicit ("C" — reopen the WebGL/3D decision),
               in-session, after reviewing the CSS/SVG world's structural
               ceiling and supplying real reference photographs for every
               WORLD_SCENES zone.
```

## Why ADR W4 is superseded, not wrong

ADR W4 (03/09/2026) correctly found that every *interaction/behavior* gap
audited at the time (camera continuity, attention hierarchy, motion
grammar) was a DOM/CSS wiring gap, not a rendering ceiling — nothing
there has changed, and this ADR does not reopen any of it.

What changed is the *visual material* itself. The CSS/SVG world
(`frontend/src/components/spatial/SpatialBackground.jsx`) is built on
one 9 KB procedural vector (`frontend/public/spatial/
cvln-academy-spatial-world.svg`) — flat gradients, no photographic
detail. That is a real ceiling: no amount of `calc()`/`blur()` tuning
recovers photographic depth, light, or material from a hand-authored
vector. The Founder supplied 12 real reference photographs (one per
`WORLD_SCENES` zone) specifically to close that gap, which DOM/CSS
cannot use as anything more than a flat `background-image`.

## Decision

`SPATIAL_WEBGL_APPROVED_FOR_BACKGROUND_LAYER`. Scope is deliberately
narrow:

- **In scope**: the world *background* only — real photographs mapped
  onto real 3D geometry, a real perspective camera, real GPU
  post-processing (bloom). This is `SpatialWebGLBackground.jsx` +
  `lib/spatial/webglEngine.js`.
- **Out of scope, unchanged**: every foreground primitive — rail
  physics, camera-follow, attention hierarchy, module dock, focus
  memory, mobile drag — stays exactly the DOM/CSS/`framer-motion`
  system ADR W4 confirmed sufficient for. This ADR does not authorize
  3D UI, 3D text, or WebGL-driven interaction of any kind. ADR W4's own
  forbidden list (`NO_DECORATIVE_3D`, `NO_PARTICLE_BACKGROUND`) still
  governs everything *inside* that background — the near/far photograph
  layers render the Founder's own reference material, not a decorative
  flourish invented to look impressive.

## Guardrails carried over from ADR W4 and reinforced

- `ENVIRONMENT_RESET_PER_ROUTE = FORBIDDEN` — unchanged; the WebGL
  world crossfades (900ms) rather than cutting, same doctrine as the
  CSS world.
- **Never regress the mobile fix** (`2ae1282`, `ccd6529` on this
  branch): `SpatialWorldFrame.jsx` mounts the WebGL world only when
  `detectSpatialQuality() !== LITE` **and** a synchronous WebGL
  capability probe succeeds — LITE-tier devices and any browser without
  WebGL keep the unmodified CSS world, automatically, with no flag to
  misconfigure.
- `prefers-reduced-motion` disables idle camera drift and pointer
  parallax in the WebGL engine (`setReducedMotion`) but keeps the
  scene-change crossfade — a hard cut on navigation would be more
  disorienting than a 900ms fade, same reasoning the CSS world already
  applies to its own transitions.
- `SPATIAL_WEBGL` (`frontend/src/lib/featureFlags.js`) is a real
  deployment kill-switch, same pattern as `SPATIAL_ENGINE`/
  `SPATIAL_ENVIRONMENT` — `REACT_APP_ACADEMY_SPATIAL_WEBGL=false` forces
  the CSS world unconditionally.

## What this does not claim

Not every `WORLD_SCENES` zone has a reference photograph yet
(`FREK_PROFILE` borrows `Community`'s; `COMMUNITY` and `ADMIN` have
photographs staged in `frontend/public/spatial/backgrounds/` but no
route to spend them on — see `lib/spatial/webglSceneMap.js`'s own
`RESERVED_BACKGROUNDS`). Every route without a real photograph keeps
the CSS world today, by construction (`backgroundForNode` returns
`null`), never a placeholder or a stretched substitute.
