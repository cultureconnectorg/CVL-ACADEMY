# W4-A — Current Experience Audit (AUDIT_ONLY, NO_CODE)

```
AUDIT_ONLY = true
NO_CODE    = true (this session made zero product-code changes to
                    produce this document — read-only inspection of
                    the current, already-pushed W3 state)
```

Purpose: decide, with evidence, whether `DOM + CSS + framer-motion`
(what's already installed and used throughout W1–W3) can reach the
Spatial Learning target, or whether a genuinely new rendering layer
(canvas/WebGL) is required for any of it. The short answer, argued
surface by surface below: **every current limit is a wiring or
architecture gap in the DOM/motion layer already in the codebase, not a
rendering-technology ceiling.** No surface in this audit needs canvas or
WebGL to reach its stated target.

## Table

| SURFACE | CURRENT_BEHAVIOR | TARGET_BEHAVIOR | CURRENT_LIMIT | TECHNICAL_CAUSE | DOM_CSS_POSSIBLE | WEBGL_REQUIRED | EVIDENCE |
|---|---|---|---|---|---|---|---|
| **Landing** | FOCUS (scale 1.015/opacity) on the active language pill; ENTER crossfade on the register/login mode swap. Manifesto column and auth card render simultaneously, equal visual weight, no page-load choreography (deliberate, W2-B) | `UNIVERSE_BEFORE_INTERFACE`: the manifesto should read as the established reality before the interface (auth form) asks for engagement; `ONE_DOMINANT_FOCUS` at first paint | Manifesto and auth card compete for attention from the first frame — nothing establishes "this is the world" before "this is the form" | Deliberate W2-B scope restraint: no primitive was attached to page-load itself, only to the two real state changes (language pick, mode swap) — see `docs/SPATIAL_LEARNING_W2B_LANDING_REPORT.md`'s own "deliberate restraint" section | YES — a staged reveal (manifesto settles first, auth card `ENTER`s ~150–250ms later) is ordinary `framer-motion` sequencing, already the same mechanism `ContextFrame`/`Enter` use elsewhere | NO | `frontend/src/pages/Landing.js` lines ~72–96 (manifesto, no motion wrapper) vs. 98–183 (auth card) |
| **Formations** | Pole filter + formation cards wrapped in `FocusFieldItem` (target = real DOM focus via click/tab, never hover); locked cards get a flat `opacity-75` Tailwind class; no related-context panel | `DEPTH_IS_SEMANTIC` (a focused card's context should reveal *why* it matters); `PROGRESSIVE_HORIZON` (locked formations should read as "not yet reached," distinct from "currently receded") | Locked-card dimming and secondary-card dimming are visually identical (`opacity-75` vs. `FOCUS_FIELD_VARIANTS.secondary`'s `opacity:0.55`) — no HORIZON treatment exists on this screen at all, despite the primitive existing; `FocusFieldContext` (REVEAL-based related context) is built but unused here | `FormationCard`'s lock styling predates Spatial Learning and was never migrated; `RELATED_CONTEXT` was explicitly out of scope for W2-D's "controlled, minimal first integration" (see `docs/SPATIAL_LEARNING_W2D_FORMATION_DISCOVERY_REPORT.md`) | YES — both `Horizon` (`motion-primitives.jsx`) and `FocusFieldContext` (`CvlnFocusField.jsx`) already exist, tested, unused; this is a wiring gap, not a capability gap | NO | `frontend/src/pages/Formations.js:160` (`locked ? "opacity-75" : ""`); grep-confirmed zero imports of `FocusFieldContext`/`Horizon` in `Formations.js` |
| **Roadmap** | 6 stage cards in a horizontal scroll-snap row; current stage = `FocusFieldItem` target (APPROACH), every other stage = secondary (RECEDE) — identical treatment for "already crossed" and "not yet reached" | `ENVIRONMENTAL_GROWTH` (the page should feel like traversing a forest, each stage a real place passed through); `PROGRESSIVE_HORIZON` (future stages distinct from past ones) | `CvlnFocusField`'s binary target/secondary contract has no third "not yet reached" role, so crossed and future stages look the same | W3-D reused `CvlnFocusField` as-is (2-role contract, built for Formations' card grid) rather than porting the 4-role pattern `JourneyHierarchy.jsx` already built for exactly this shape of problem (CURRENT/ACQUIRED/NEXT/LOCKED) | YES — `JourneyHierarchy.jsx` is the proof this is solvable in pure DOM/motion: it already solves the identical "sequence with a past/present/future" problem for `ModuleJourney`'s phase stepper | NO | `frontend/src/pages/Roadmap.js` (`FocusFieldItem` usage); `frontend/src/lib/CvlnFocusField.jsx`'s `FOCUS_FIELD_VARIANTS` (2 non-idle roles) vs. `frontend/src/lib/JourneyHierarchy.jsx`'s `JOURNEY_VARIANTS` (4 roles) |
| **ModuleJourney** | Full CURRENT/ACQUIRED/NEXT/LOCKED hierarchy on the phase stepper (`JourneyHierarchy.jsx`); phase *body* open/close is a hard React conditional, not height-animated | `DEPTH_MEMORY` / `CONTINUITY_OVER_TRANSITION`: opening/closing a phase should read as a continuous reveal, not a layout jump | The stepper's per-phase depth roles (W3-A) are real and animated, but the accordion body itself (`{isOpen && (<div>…</div>)}`) still pops in/out with no height transition — a visible cut between two otherwise-smooth motion layers | The hierarchy work (W3-A) targeted the *card's* depth role; the *body's* mount/unmount mechanism was never in scope for that tranche and was left as the pre-existing plain conditional | YES — CSS grid-template-rows interpolation or `framer-motion`'s `layout`/`AnimatePresence` height animation are both standard, already-used-elsewhere techniques | NO | `frontend/src/pages/ModuleJourney.js:221` (`{isOpen && (`) |
| **Quiz/context** | `ContextFrame` (REVEAL-in) wraps the quiz questions and mini-mission content on mount; the matching RETURN-out motion is coded but never actually triggered for these two, since the accordion closes by unmounting the whole subtree rather than toggling `ContextFrame`'s own `show` prop | `CONTINUITY_OVER_TRANSITION` / `RETURN_EXACT_CONTEXT`: leaving a context should be felt (RETURN motion), not just entering it | The RETURN half of ACTIVE→CONTEXT→RETURN is infrastructure-only for quiz/mini-mission — built, unit-and-E2E-proven for the *state*, but the *motion* only actually plays for Mentor (the one always-mounted case) | Explicit, documented W3-B architecture choice — `PhaseQuizContext`/`PhaseMiniMission` don't call `leaveContext()` at all (see that file's own comment: "this component doesn't need its own dismiss control") | YES — the fix is to stop unmounting the subtree on accordion-close and instead toggle `ContextFrame`'s `show` prop, exactly as `MentorPanel.js` already does | NO | `frontend/src/pages/ModuleJourney.js` `PhaseQuizContext`/`PhaseMiniMission` (no `leaveContext` call); contrast with `frontend/src/components/MentorPanel.js` (`show={open}`, always mounted) |
| **Mentor contextual** | Always-mounted, `ContextFrame`-driven, real REVEAL-in/RETURN-out on every open/close; gated to `ModuleJourney` only | `MENTOR = CONTEXTUAL_PRESENCE`; `RETURN_EXACT_CONTEXT` | None functional — the only open question is whether "inside a module" is the right scope, a product decision, not a rendering gap | N/A | N/A (already achieved) | NO | `frontend/src/components/MentorPanel.js`, `frontend/src/lib/mentorPresence.js` |
| **Route continuity** | `AnimatePresence mode="wait"` crossfade keyed by `location.pathname`, mounted app-wide around `<Routes>` | `CONTINUITY_OVER_TRANSITION`: a route change should read as one continuous scene, not two separate pages | `mode="wait"` fully unmounts the outgoing page before mounting the incoming one — for the redirect-chain cases W2-A tested (mostly-empty pages), this reads fine; for a real content-heavy page-to-page transition (e.g. Formations → FormationDetail) it has **never been visually verified** — `mode="wait"`'s sequential gap is more likely to read as a pause than a crossfade once both sides have real content and a lazy-chunk load in between | Deliberate choice to avoid two full, unrelated page layouts overlapping mid-transition; not yet revisited against a real (non-redirect) transition | YES — `AnimatePresence mode="popLayout"`, or a custom overlap window, are both ordinary `framer-motion` techniques | NO | `frontend/src/lib/RouteTransition.jsx:61` (`mode="wait"`); `docs/SPATIAL_LEARNING_W2A_ROUTE_CONTINUITY_REPORT.md`'s own "what real navigation means" section, which already flagged this as untested |

## Classification summary

| Surface | Limit | Classification |
|---|---|---|
| Landing | No page-load sequencing (universe before interface) | `SOLVABLE_WITH_MOTION` |
| Formations | Locked-card treatment not on HORIZON; no related-context reveal | `SOLVABLE_WITH_MOTION` (Horizon swap) + `SOLVABLE_WITH_DOM` (Reveal panel) |
| Roadmap | No 3rd role distinguishing past vs. future stages | `SOLVABLE_WITH_MOTION` |
| ModuleJourney | Accordion body pop-in/out, no height transition | `SOLVABLE_WITH_CSS` / `SOLVABLE_WITH_MOTION` |
| Quiz/context | RETURN motion coded but never played | `SOLVABLE_WITH_MOTION` (wire `leaveContext`) |
| Mentor contextual | — | `NOT_REQUIRED` (already realized) |
| Route continuity | `mode="wait"` gap unverified against real content transitions | `SOLVABLE_WITH_MOTION` |

**Zero rows are `REQUIRES_CANVAS` or `REQUIRES_WEBGL`.** Every limit
found in this audit is closeable with the DOM/CSS/`framer-motion` stack
already in the project — most of it by wiring an *existing, already-built,
already-tested* primitive (`Horizon`, `FocusFieldContext`, the
`JourneyHierarchy` 4-role pattern, `ContextFrame`'s own `leaveContext`)
into a screen that doesn't call it yet, not by inventing new rendering
capability. This is the evidentiary basis for W4-D's ADR conclusion.
