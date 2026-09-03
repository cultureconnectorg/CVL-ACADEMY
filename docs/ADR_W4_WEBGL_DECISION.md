# ADR W4 — WebGL Decision

```
STATUS: PROPOSED — awaiting the human decision this ADR exists to
        request (CONTINUE_DOM / AUTHORIZE_LIMITED_WEBGL / REJECT_WEBGL).
        WEBGL = NOT_AUTHORIZED regardless of this ADR's conclusion,
        until that decision is made explicitly.
DATE: 2026-09-03
INPUTS: docs/SPATIAL_LEARNING_W4A_EXPERIENCE_AUDIT.md,
        docs/SPATIAL_LEARNING_W4B_PERFORMANCE_BASELINE.md,
        docs/SPATIAL_LEARNING_W4C_EXPERIENCE_GAP.md
```

## Conclusion

# **NO_WEBGL_REQUIRED**

Only one of three permitted conclusions is chosen; the other two
(`WEBGL_OPTIONAL_ENHANCEMENT`, `WEBGL_REQUIRED_FOR_SPECIFIC_SURFACE`) are
explicitly rejected below, with the evidence that ruled each out.

## Why

W4-A audited every surface that is now genuinely spatial (Landing,
Formations, Roadmap, ModuleJourney, Quiz/context, Mentor, route
continuity) and found **zero rows requiring canvas or WebGL**. Every
limit identified traces to one of three causes, none of them a rendering
ceiling:

1. **An existing, already-built, already-tested primitive is simply
   unwired on a given screen** — `Horizon` (built W1-B) is unused by
   both `Formations` and `Roadmap`; `FocusFieldContext`/`Reveal` (built
   W2-C) is unused by `Formations`.
2. **A 2-role contract was reused where a 4-role one was needed** —
   `Roadmap` (W3-D) reused `CvlnFocusField`'s binary target/secondary
   split where `JourneyHierarchy`'s 4-role CURRENT/ACQUIRED/NEXT/LOCKED
   pattern (already proven on `ModuleJourney`, W3-A) is the right shape.
3. **A motion half was coded but never triggered** — `ContextFrame`'s
   `RETURN` exit only actually plays for Mentor (the one always-mounted
   case); quiz/mini-mission never call `leaveContext()` because the
   accordion unmounts the subtree instead (W3-B, documented at the
   time).

All three are DOM/CSS/`framer-motion` wiring gaps. None is "the DOM
cannot represent this depth cue" or "CSS cannot express this transform."

W4-B's performance baseline reinforces this from the other direction:
`main.js`'s +39.32 kB gzip growth is **97% attributable to one event**
(W2-A making `framer-motion` reachable at all) and is a **one-time,
structural cost**, not a symptom of the DOM approach straining under
load. Cumulative Layout Shift measured **0** on every surface, desktop
and mobile, in the real production build. Long tasks during real
interactions measured 61–65 ms in production (vs. 210–221 ms on the
unminified dev server — confirmed tooling noise, not a production
signal). A concrete, unexplored size-reduction lever exists
(`framer-motion`'s `dom-mini` entry point, since nothing in this
codebase uses drag/gestures/`layout` animations) that hasn't even been
tried yet. **The current approach has real, fixable inefficiencies — it
does not have a ceiling.**

W4-C confirms the gap is about *breadth and felt continuity*, not
capability: `DEPTH_IS_SEMANTIC` and `CALM_BY_DEFAULT_ALIVE_ON_INTENT` are
both fully `REALIZED` today, in pure DOM/CSS/`framer-motion`. Every
`PARTIAL` row has at least one concretely realized case already proven
somewhere in the app (e.g. `ONE_DOMINANT_FOCUS` is real on `ModuleJourney`
and `Roadmap`, just not yet on `Formations`/`Landing`). Nothing in that
audit reads as "this doctrine is structurally unreachable without a new
rendering layer" — it reads as "apply the pattern that already works
elsewhere, to the two screens that don't have it yet."

## Why the other two conclusions were rejected

- **`WEBGL_REQUIRED_FOR_SPECIFIC_SURFACE`** — rejected. This would
  require a surface whose target behavior *cannot* be expressed in
  DOM/CSS/`framer-motion` at all. No such surface exists in the W4-A
  table; every `WEBGL_REQUIRED` column reads `NO`.
- **`WEBGL_OPTIONAL_ENHANCEMENT`** — rejected, deliberately, not just by
  default. The doctrine's own forbidden list (`NO_DECORATIVE_3D`,
  `NO_PARTICLE_BACKGROUND`, and this ADR's own `3D_FOR_DECORATION`
  prohibition) rules out exactly the category of thing "optional
  enhancement" WebGL usually means in a product like this — a nicer-
  looking but non-functional flourish layered on top of an already-
  working DOM experience. Recommending an optional layer whose only
  honest justification would be "it would look more impressive" is the
  one thing this ADR is explicitly told never to do ("Ne jamais choisir
  WebGL uniquement pour rendre l'interface 'plus impressionnante'").
  There is no *specific, named user value* (learning outcome, task
  completion, comprehension) identified anywhere in W4-A/B/C that a
  WebGL layer would unlock and DOM cannot — the prerequisite for even
  proposing this conclusion — so it isn't proposed.

## What "reject WebGL" does not mean

Rejecting WebGL here is not a claim that the current experience is
finished. W4-C found real, honestly-classified gaps (`PROGRESSIVE_HORIZON`
and `DEPTH_MEMORY` both `MISSING`; four `PARTIAL` rows). The recommended
next work — if and when a further wave is authorized — is exactly the
gap list W4-A/C already produced: wire `Horizon` on `Formations`/
`Roadmap`, extend `JourneyHierarchy`'s 4-role pattern to `Roadmap`, wire
`leaveContext()` for quiz/mini-mission, height-animate the accordion
body, and verify `RouteTransition` against a real (non-redirect)
page-to-page transition. All of that is `SOLVABLE_WITH_DOM`/
`SOLVABLE_WITH_MOTION`/`SOLVABLE_WITH_CSS` per W4-A's own classification
— none of it needs this ADR's conclusion to change.

## Required sections when WebGL is recommended

N/A — this ADR's conclusion is `NO_WEBGL_REQUIRED`. Per the W4-D
mandate, the `SURFACE`/`USER_VALUE`/`WHY_DOM_FAILS`/`RENDERING_SCOPE`/
`SEMANTIC_DOM_FALLBACK`/`REDUCED_MOTION_FALLBACK`/`MOBILE_FALLBACK`/
`PERFORMANCE_BUDGET`/`FEATURE_FLAG`/`ROLLBACK` breakdown only applies to
a `WEBGL_REQUIRED_FOR_SPECIFIC_SURFACE` or `WEBGL_OPTIONAL_ENHANCEMENT`
conclusion, neither of which this ADR reaches. Left as a template for
whichever future ADR, if any, reaches one of those conclusions with a
named surface and evidence to back it:

```
SURFACE:                  (none proposed)
USER_VALUE:                (none proposed)
WHY_DOM_FAILS:              (no case found — see "Why" above)
RENDERING_SCOPE:            —
SEMANTIC_DOM_FALLBACK:      —
REDUCED_MOTION_FALLBACK:    —
MOBILE_FALLBACK:            —
PERFORMANCE_BUDGET:         —
FEATURE_FLAG:                —
ROLLBACK:                    —
```

## Forbidden list — compliance

This ADR does not propose any of: `FULL_APP_WEBGL`, `3D_FOR_DECORATION`,
`CANVAS_REPLACES_DOM_SEMANTICS`, `WEBGL_NAVIGATION_OWNERS_ROUTING`,
`WEBGL_CONTROLS_DOMAIN_STATE`. None of these appear anywhere in this
document as a recommendation.

## Decision requested

```
STOP = TRUE (per the W4 authorization's own stop condition)
Awaiting one of:
  CONTINUE_DOM        — proceed on the existing DOM/CSS/framer-motion
                         stack; the next work is the concrete gap list
                         in W4-A/C (Horizon wiring, Roadmap 4-role
                         pattern, quiz/mission RETURN wiring, accordion
                         height animation, real-transition verification)
  AUTHORIZE_LIMITED_WEBGL — not proposed by this ADR; would require a
                         named surface and evidence this ADR did not
                         find
  REJECT_WEBGL         — consistent with this ADR's own conclusion
No advanced/WebGL code will be written before this decision, per the
authorization's own instruction.
```
