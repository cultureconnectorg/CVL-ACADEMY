# ACA-0017 — Real Attention/Occlusion Hierarchy on Production Components

```
STATUS: CLOSED (2026-09-08) — verified already satisfied by completed
ACA-0014/H1 work; no new code needed for this pass.
```

## What this closes

ACA-0017's own title: apply the *real* attention/occlusion hierarchy
(`lib/spatial/attention.js`'s `computeDepthStyle` — 6 perceptual-
occlusion channels: translateZ/scale/opacity/saturate/contrast/
brightness/blur/zIndex, driven by the real 4-tier `attentionTier`
classification, `aria-hidden` wired for `LATENT_CONTEXT`) to real
production components, not a prototype.

This is distinct from ACA-0014 ("mount the spatial engine in production
surfaces" — the broader integration effort) in name only: verifying the
codebase directly shows ACA-0014's own execution (Rails 3-5, then the
H1 step-4 Badges/Missions/FrekProfile passes) already *is* this
component-by-component application, because every one of those passes
specifically wired `computeDepthStyle` (or a component that itself
calls it), not a simplified stand-in. No new page conversions were
needed this pass — this report is the verification and closure, done
by direct grep evidence rather than re-doing already-real work.

## Verified evidence

`computeDepthStyle` (or a component wrapping it) is imported and called
in every real, `SPATIAL_HUB_ENABLED`-gated production surface:

| Surface | File | Mechanism |
|---|---|---|
| Dashboard (`/dashboard`) | `components/SpatialHub.jsx` | `computeDepthStyle(distance, { mobile: false })` |
| Roadmap (`/roadmap`) | `pages/Roadmap.js` | `computeDepthStyle(distance)` directly |
| Module Journey (`/formations/:fc/modules/:mc`) | `lib/JourneyHierarchy.jsx` | `computeDepthStyle(distance, { mobile: false })` |
| Badges (`/badges`) | `pages/Badges.js` | `computeDepthStyle(distance)` via `BadgeDepthCard` |
| Missions (`/missions`) | `pages/Missions.js` | `computeDepthStyle(distance)` via a depth wrapper |
| FREK Profile (`/frek-profile`) | `pages/FrekProfile.js` | `computeDepthStyle(distance)` via `SignalDepthCard` |

`lib/pedagogicalGraph.js` (the pure derivation module Dashboard/Roadmap
both consume through `usePedagogicalGraph`) also documents its own
distance scale as sharing `attentionWeight`'s units — confirming the
whole pipeline, not just the leaf render, is built on the one real
attention model.

**Formations** (`/formations`) is the one production surface in this
set that does *not* call `computeDepthStyle` — it uses the older but
equally real `FocusFieldItem`/`useFocusField` (`lib/CvlnFocusField.jsx`)
target/secondary/horizon vocabulary instead. This is not a gap:
`docs/SPATIAL_H1_INTEGRATION_PLAN.md`'s own table rates this **REUSE**
("already uses the exact target/secondary/horizon vocabulary this
prototype's rail generalizes... needs no change"), a deliberate verdict
made when the plan was written, not an oversight this pass is
discovering.

## What this does NOT close

- **ACA-0015** (camera-follow `CROSSING`/`REVEALING` wiring) — a
  *transition-between-attention-states* concern, not attention/
  occlusion styling itself. Still `in_progress`, unaffected by this
  closure.
- **ACA-0018** (audio/haptics calibration on real surfaces) — a
  separate, not-yet-started backlog item; attention/occlusion is
  visual-only.
- **The two REPLACE-BLOCKED H1-plan items** (Formation-card→Module FLIP
  extension, environmental asset upgrade) — untouched, each needs its
  own go-ahead per the plan's own terms (general spatial-work
  authorization was granted this session, but the plan still records
  these as requiring separate review before being built).
- **Wallet/Skills/Certifications pages** — never in the H1 plan's scope
  table at all (not part of the Hub/Roadmap/Module/Badges/Missions/
  FREK sequencing this ACA item tracks); no claim is made about them
  here.
