# H1 Integration Plan — REUSE / EXTEND / WRAP / REPLACE-BLOCKED

```
STATUS: PLANNING DOCUMENT ONLY.
H1_PRODUCTION_INTEGRATION = NOT_AUTHORIZED. Nothing in this document has
been executed. This exists so that, the moment APPROVE_DIRECTION is
given, there is no ambiguity about what happens to each real surface —
"Claude does not decide at random," per the Founder's own instruction.
```

For every real, already-shipped surface in `frontend/src`, one of four
verdicts:

- **REUSE** — the existing component/file is correct as-is and the new
  grammar wraps around it without modification.
- **EXTEND** — the existing component gets new props/CSS/behavior added,
  but its public contract (props, route, test IDs) does not change.
- **WRAP** — a new shell component is introduced around the existing one
  (e.g. the new Hub rail becomes the entry point that *contains* the
  existing Formations/Roadmap/Module pages unchanged inside it).
- **REPLACE-BLOCKED** — the existing implementation would need to be
  replaced to hit the new grammar, and that replacement is explicitly
  **not authorized to start** without a separate, later sign-off beyond
  APPROVE_DIRECTION (i.e., even after H1 is approved, this specific item
  needs its own go-ahead).

| Surface | File(s) | Verdict | Rationale |
|---|---|---|---|
| Landing (`/`) | `frontend/src/pages/Landing.js` | **REUSE** | Pre-auth marketing page, explicitly out of scope for the Spatial Console grammar (doctrine applies to the authenticated in-app shell only, consistent with W1-W4 scoping). |
| App shell / routing | `frontend/src/App.js` | **EXTEND** | Add the new Hub rail as the `/dashboard` entry point; existing `<Routes>`, `<Protected>`, role guards, and every path stay byte-identical. `SPATIAL_HUB_ENABLED` flag (see spec §11) gates which shell mounts. |
| Dashboard (`/dashboard`) | `frontend/src/pages/Dashboard.js` | **WRAP** | The prototype's Hub rail becomes the new `/dashboard` presentation. Dashboard.js's current data-fetching (real progression, real module state) is REUSED verbatim as the data source; only the render layer is wrapped by the new rail shell. |
| Formations list | `frontend/src/pages/Formations.js` | **REUSE** | Already uses `FocusFieldItem`/`CvlnFocusField` (W2-C) — the exact target/secondary/horizon vocabulary this prototype's rail generalizes. The real page needs no change to be entered *from* the new Hub; it already speaks a compatible visual language. |
| Formation detail | `frontend/src/pages/FormationDetail.js` | **EXTEND** | Add the Formation→Module shared-element FLIP (see Transition Matrix gap in the spec) — everything else unchanged. |
| Roadmap | `frontend/src/pages/Roadmap.js` | **EXTEND** | Swap the current `FocusFieldItem`-based role derivation for the richer `applyDepth()`-style continuous distance model this prototype validates; keep `useAuth()`/`t()`/all existing test IDs unchanged. Low risk — this file is small and already isolated (see the file as read this session). |
| Module Journey | `frontend/src/pages/ModuleJourney.js` | **EXTEND** | Add the module-recedes-behind-context-dock treatment (spec §"Module → Quiz/Mission/Proof/Mentor") on top of the existing `JourneyHierarchy`/`ContextFrame` machinery (W3-A/B) — those are the exact "internal bricks" the recede/approach motion in this prototype is built to sit on. Add a Proof context type alongside the existing Quiz/Mission/Mentor ones. |
| Missions | `frontend/src/pages/Missions.js` | **EXTEND** | Convert from its current presentation to the glanceable-list treatment validated here (no card grid). Real mission data/status already exists server-side; only the render changes. |
| Badges | `frontend/src/pages/Badges.js` | **EXTEND** | Convert to the glanceable-cluster treatment; earned/unearned already exists as real data. |
| FREK Profile | `frontend/src/pages/FrekProfile.js` | **EXTEND** | Convert to the identity-first, non-KPI-card treatment; real FREK-ID and stage already exist as data. |
| Mentor panel | `frontend/src/lib/mentorPresence.js` + Mentor UI | **REUSE** | Already scoped to ModuleJourney only (W3-C) — exactly matches this prototype's "Mentor = SECONDARY_CONTEXT, not a destination" requirement. No change needed beyond the visual dock treatment already covered by ModuleJourney's own EXTEND row. |
| Motion primitives | `frontend/src/lib/motion-primitives.jsx` | **EXTEND** | Add the new depth/parallax primitives (FAR/ADJACENT/FOCUS continuous model, layered-parallax helper) as new named exports alongside the existing 8 (FOCUS/APPROACH/ENTER/RECEDE/REVEAL/RETURN/CONFIRM/HORIZON) — additive, no existing primitive's contract changes. |
| Spatial state machine | `frontend/src/lib/spatial-state.js`, `ContextFrame.jsx` | **REUSE** | The DOMAIN_STATE/SPATIAL_STATE separation and the `useContextEntry()`/`enterContext`/`leaveContext` pattern this prototype's context dock reimplements standalone is *already* the real, shipped implementation — H1 should call the real hooks, not reinvent them, closing the one deliberate duplication this prototype carries for standalone-testability reasons. |
| Route transitions | `frontend/src/lib/RouteTransition.jsx` | **REUSE** | Already provides the crossfade-not-hard-cut guarantee (`AnimatePresence mode="wait"`) this spec's Transition Matrix assumes at the route level. |
| Certification / Skill / FMS / Backend | everything under `backend/`, `frontend/src/lib/auth.jsx`, `frontend/src/lib/i18n.jsx` | **REUSE**, untouched | Explicitly frozen by the Founder's hard-freeze list (AUTH, ROUTES, RBAC, FREK_ID, FMS_CANONICAL_MODEL, PROGRESSION_TRUTH, SKILL_ENGINE, CERTIFICATION_ENGINE, PWA, SECURITY, BACKEND_CONTRACTS, DB). H1 must not touch these regardless of scope pressure. |
| Formation-card → Module FLIP | *(new)* | **REPLACE-BLOCKED** | This prototype only proves the FLIP technique for one path (Hub→Module). Extending it to Formations→Module and Roadmap→Module needs its own follow-up validation pass before being built into the real app — a genuinely new interaction, not a drop-in reuse of what H0.6 already proved. Needs a separate go-ahead even after APPROVE_DIRECTION. |
| Environmental asset upgrade (real vegetal/organic imagery) | *(new)* | **REPLACE-BLOCKED** | Per spec §7, the current CSS-blob backdrop is a placeholder. Commissioning or generating real environment assets is a design decision with its own review cycle (weight budget, licensing/generation-provenance, IP guardrail re-check) — not to be rushed into H1 alongside the interaction-grammar work. |
| Mobile swipe/velocity snap | shared helper, likely `frontend/src/lib/` | **EXTEND** (net new file) | The `attachSwipe()` pointer-event logic in the prototype is small, dependency-free, and portable — promote it to a shared `useSwipeRail()` hook, used by Formations/Roadmap/Hub alike. No existing file needs to change shape to adopt it. |

## Sequencing recommendation (not authorized to start)

If/when `APPROVE_DIRECTION` is given, the lowest-risk order is: (1)
Motion primitives + spatial-state reuse wiring (pure addition, zero
visual change yet), (2) Dashboard WRAP (the new Hub rail, since it's the
most validated piece and touches no other page), (3) Roadmap/Module
EXTEND (both already carry the closest-matching existing machinery), (4)
Missions/Badges/FREK EXTEND (smallest, most isolated pages), (5) the two
REPLACE-BLOCKED items only after their own explicit review.
