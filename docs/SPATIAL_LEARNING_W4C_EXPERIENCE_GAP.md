# W4-C — Spatial Experience Gap — REPORT

```
Method: for each doctrine, ask "does a real user perceive this, right
now, on the actual pushed app" — not "does a primitive exist that could
produce this." A built-but-unused component is not a realized
experience. Cross-referenced against W4-A's surface-by-surface findings
and the session's own W1–W3 reports (which already, honestly, flagged
several of these gaps themselves rather than claiming completion).
```

| Doctrine | Classification | Why |
|---|---|---|
| `UNIVERSE_BEFORE_INTERFACE` | **PARTIAL** | DOM order structurally puts the manifesto before the auth card (mobile stacks it first, screen-reader order matches), but nothing establishes it *temporally* — both render simultaneously at first paint, with equal visual weight. The "world, then the door into it" feeling doesn't exist; only the document order does. (W4-A, Landing row) |
| `LEARNING_FIRST_INTERFACE_SECOND` | **PARTIAL** | Strong on `ModuleJourney` specifically: content dominates the screen, chrome (Mentor) only appears on request and never blocks reading (W3-C). Not established as a cross-app pattern — `Formations` (pre-learning browsing) and `Roadmap` (progression overview) don't have an equivalent "interface recedes, content leads" moment; only one screen out of four deeply embodies this. |
| `ONE_DOMINANT_FOCUS` | **PARTIAL** | Realized on `ModuleJourney` (the CURRENT phase unambiguously stands forward) and `Roadmap` (the current stage foregrounds via real progression data, not interaction). Weak on `Formations` (only when a card has real DOM focus — at rest, the grid is N equally-weighted cards, no default focus). Missing at the `Landing` page level (manifesto vs. auth card, 50/50 split, no default dominant element). 2 of 4 surfaces genuinely realize it; 2 don't. |
| `DEPTH_IS_SEMANTIC` | **REALIZED** | The one principle most rigorously enforced throughout W1–W3: every depth cue (`FOCUS`, `APPROACH`, `RECEDE`, `JourneyHierarchy`'s 4 roles) is driven by real state — `phase_flags`, `canOpen`, `stade`, real DOM focus — never `:hover`, never decorative. Explicitly checked and documented in every single W2/W3 tranche report (`NO_GENERIC_SCALE_HOVER` compliance tables). This is a genuine, verified strength, not an aspiration. |
| `CONTINUITY_OVER_TRANSITION` | **PARTIAL** | Real wins: Mentor's open/close genuinely crossfades (W3-B), Landing's mode-swap crossfades, the redirect-driven route change crossfades. Real, identified gaps (W4-A): `RouteTransition`'s `mode="wait"` has never been visually verified against a real content-to-content transition (only redirect chains, a degenerate case); `ModuleJourney`'s accordion body still pops in/out with no height transition; the quiz/mini-mission `RETURN` motion is coded but never actually triggered (the accordion unmounts the subtree instead of toggling `show`). Continuity is real in the cases explicitly built for it, and absent in the cases nobody wired yet. |
| `RETURN_EXACT_CONTEXT` | **PARTIAL** | The *functional* half is rigorously proven — `RETURN_POSITION_PRESERVED` is an actual, repeated E2E assertion (W3-B, W3-C, W3-E: URL unchanged, journey-hierarchy role unchanged, pole-filter role unchanged after a context closes or a back/forward round-trip). The *felt* half doesn't exist: no scroll-position memory anywhere, no visual "settling back into the same physical spot" — returning is provably correct but not sensorially different from a fresh render. |
| `CALM_BY_DEFAULT_ALIVE_ON_INTENT` | **REALIZED** | The best-honored principle in the whole set. Every tranche report includes an explicit "why we did NOT use this primitive here" section (W2-B skipped `APPROACH`/`RECEDE`/`HORIZON` on Landing; W3-B kept quiz/mission's exit as a plain unmount rather than forcing a RETURN animation; nothing animates on page load except one disclosed, bounded side-effect). Motion only ever fires on a real state change a user or real progression data caused — never ambient, never looping, never on mere proximity. |
| `PROGRESSIVE_HORIZON` | **MISSING** | The `Horizon` primitive exists (`motion-primitives.jsx`, built W1-B) and is grep-confirmed **unused by any screen** — not `Formations` (locked cards use a flat `opacity-75` Tailwind class instead), not `Roadmap` (future stages get the same binary "secondary" treatment as past ones, no distinct "not yet reached" cue). Zero screens currently make a locked/future thing read as "on the horizon" rather than just "dimmed." This is the single clearest infrastructure/experience gap in the whole audit. |
| `DEPTH_MEMORY` | **MISSING** | No scroll-position memory, no cross-navigation persistence of local UI state anywhere in the app. `Roadmap`'s and `Formations`' own test suites *document this as current, correct, unchanged behavior* (`roadmap-progression`/`formations-discovery` specs prove the pole filter resets on remount) rather than claim otherwise — so this gap is at least honestly self-documented, not silently assumed away. |
| `ENVIRONMENTAL_GROWTH` | **PARTIAL** | Real, meaningful progress this session: the literal gamification leak ("Level N") was found and removed (W3-D), and the current stage now foregrounds using real progression data rather than a numeric badge. But the doctrine's fuller sense — the *environment itself* visibly transforming with growth (ambient color, background texture, scene composition shifting as a learner advances) — doesn't exist; only the one stage *card* gets a depth treatment. The stage system (🌱→🌳🌳) predates this whole effort and was already non-gamified in naming; W3-D's real contribution was removing the one leak and adding the first depth cue, not building the full environmental metaphor. |

## Summary count

```
REALIZED:            2  (DEPTH_IS_SEMANTIC, CALM_BY_DEFAULT_ALIVE_ON_INTENT)
PARTIAL:              6  (UNIVERSE_BEFORE_INTERFACE, LEARNING_FIRST_INTERFACE_SECOND,
                          ONE_DOMINANT_FOCUS, CONTINUITY_OVER_TRANSITION,
                          RETURN_EXACT_CONTEXT, ENVIRONMENTAL_GROWTH)
INFRASTRUCTURE_ONLY:  0  (nothing here is "built but literally never touched" —
                          PROGRESSIVE_HORIZON's primitive is arguably this, but
                          since NO screen consumes it at all, MISSING is the
                          more honest label than crediting unused infrastructure)
MISSING:              2  (PROGRESSIVE_HORIZON, DEPTH_MEMORY)
```

## Honest read

W1–W3 built real, disciplined, well-tested **behavioral rules**
(when something is allowed to move, and why) — that part of the doctrine
is genuinely strong (`DEPTH_IS_SEMANTIC`, `CALM_BY_DEFAULT_ALIVE_ON_INTENT`
are both fully realized, and every other PARTIAL row has at least one
concretely realized case, not zero). What's missing is **breadth and
felt continuity**: the same rules haven't yet been applied everywhere
they could be (`Horizon` unused, `Roadmap`'s future stages undifferentiated
from its past ones), and the *sensation* of returning/continuing
(scroll memory, real page-to-page crossfade, the accordion's own body
transition) lags behind the *correctness* of returning (which is
rigorously proven). None of this points at a technology ceiling — every
gap here has a named, concrete DOM/motion fix already identified in
W4-A, not a missing rendering capability.
