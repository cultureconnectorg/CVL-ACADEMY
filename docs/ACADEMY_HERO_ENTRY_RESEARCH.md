# CVLN Academy — Hero / Entry-Into-a-World Research

```
DESIGN RESEARCH ONLY. No code changed to produce this document. This
does not authorize or begin any Hero/Landing redesign — that remains
W-FUNNEL-2, still NOT_AUTHORIZED. Purpose: ground the future Hero
System in real, sourced mechanisms rather than in the visual identity
of any of the four references.
```

**Method note on sourcing**: this session's outbound web access runs
through a proxy that blocks direct fetch of most of the primary
domains involved (`blog.playstation.com`, `newsroom.spotify.com`,
`gameuidatabase.com` all returned `EGRESS_BLOCKED` on direct fetch).
Every claim below is instead grounded in **search-engine-synthesized
summaries of those exact pages** (the search tool draws from real page
content and returns the source URL) — cited as `SOURCE (via search)`
to be precise about that one-step remove, never presented as if I had
read the raw page. Where I reasoned beyond what a source states, it is
marked `PRINCIPE INFÉRÉ`, never blended into the sourced claim.

---

## 1–2. The four references, decomposed

### A. Need for Speed — entering velocity

**OBSERVED/SOURCE**: Criterion Games' *Autolog* (introduced in *Need
for Speed: Hot Pursuit*, 2010) replaced global leaderboards with a
"Comparison Engine" — personalized recommendations built from
one-upmanship between named friends, tracked on a per-player "Speed
Wall" reflecting career progression and records (source: Fandom NFS
Wiki `Autolog`/`The Run/Autolog`, via search; corroborated by
`racinggames.gg`'s retrospective on Criterion's Hot Pursuit→Most
Wanted→Rivals arc, via search). *Need for Speed* (the 2014 film,
directed by Scott Waugh) used real cars and real camera cars — a
supercharged Mustang built to keep pace above 150 mph — specifically to
avoid a CGI look (source: Top Gear / Destructoid behind-the-scenes
pieces, via search). Structured, official documentation of the
in-*game* garage/car-selection camera language (angle, framing,
staging) was not reachable this session — treat any specific claim
about "the car becomes the center of the universe" camera-blocking as
`PRINCIPE INFÉRÉ` from the well-documented genre convention (hero-car
showcase screens, e.g. NFS's own historical "Car Showcase" feature
across the first five titles per Fandom), not as a directly sourced
design statement.

**PRINCIPE INFÉRÉ** (genre-level, cross-referenced against the sourced
Autolog/Car-Showcase facts, not asserted as verified per-title):
1. **Selection is never just a function call** — Autolog itself is the
   proof: choosing a car/route is instrumented into a *social,
   competitive, personal* system (times, rivalries, records), not a
   silent state change. The mechanism that generalizes: **a selection
   becomes meaningful when it visibly changes what the world says back
   to you**, not when it merely changes what's rendered.
2. **The showcased object gets dedicated screen time and camera
   attention distinct from browsing** — the historical "Car Showcase"
   (stats, 360° views, live-action footage per car) is a *separate,
   deliberate mode* from the selection list, i.e. two distinct spatial
   registers: *scanning* (list/rail) and *reverence* (showcase) —
   never collapsed into one screen.
3. Real film production evidence (authentic cars, camera cars matched
   to feature-car speed) supports a narrower, safely-transferable
   principle: **momentum reads as real only when the thing carrying it
   has weight and consequence** — in a UI, this maps to physics with
   real inertia (H0.10's spring model), not to any car-specific visual.

**APPLICATION CVLN RECOMMANDÉE**: do not attempt a literal "hero-object
showcase" (a formation isn't a car, showcasing it as an object risks
exactly the gamified/trophy tone the mission forbids). Take only the
*structural* lesson: (a) a spatial engine should distinguish a
*scanning* register (rail/list, fast, cadence-aware) from a
*commitment* register (entering a formation/module — slower, focused,
consequential) — H0.10 already has this distinction (`FOCUS` vs
`APPROACH`/`ENTER`); and (b) a real domain action (module completed,
skill validated) should visibly "talk back" to the learner the way
Autolog's rival-beaten notification does — not as gamification, but as
**acknowledgment that the action changed something real**, which is
exactly what `next_action`/`progression/summary` already compute
server-side (`ACADEMY_CURRENT_FUNNEL_AUDIT.md`, stage 09/17) and
currently under-surfaces.

---

### B. Universal Pictures — revealing a world, then a name

**OBSERVED/SOURCE**: the globe logo dates to the 1920s; the 1936
version circled "A Universal Picture" around it. The 1936–1990 version
was hand-painted on a rubber ball by Eyvind Earle, with the space
background and Van Allen belts, live-action model work combined with
cel animation (source: `designyourway.net` Universal Pictures logo
history, via search). The current (2012) version, animated by **Weta
Digital** for the studio's centennial, was explicitly inspired by
**satellite imagery of Earth at night** — deliberately *not*
foregrounding continents/borders, instead showing "tiny points of
bright light... symbolising the thousands of communities brought
together by their shared love of film" (source: PRNewswire official
release + Weta Workshop's own post, via search). The sequence's camera
**zooms into a specific location (Boston) on the globe** once the
byline disappears (source: Fandom Moving-Logo-Wiki `2012-`, via
search). It debuted with *Dr. Seuss' The Lorax* in March 2012. A
re-orchestrated version of the classic fanfare was composed by Brian
Tyler for this version (source: same, via search).

**PRINCIPE INFÉRÉ** (from the sourced facts, this is genuine inference
about *why* it works, not itself sourced from a design-rationale
document):
1. **The identity is deferred, not hidden** — the sequence spends its
   entire duration establishing scale and belonging (a whole world,
   lit by shared human activity) *before* any wordmark reads. The
   brand is the *last* thing understood, not the first.
2. **Camera movement is the narrative** — the zoom into Boston (a
   *specific*, not generic, point) converts an abstract "the world" into
   "a place a story is about to happen in." Scale compresses from
   planetary to local in one continuous, unbroken camera move — no cut.
3. **Light is the reveal mechanism, not a decoration** — the "tiny
   points of bright light" *are* the content (communities), not an
   effect layered on top of geography.

**APPLICATION CVLN RECOMMANDÉE**: the transferable mechanism is
**world-before-name, one continuous camera move, specific-over-generic
final focus** — not a globe, not a zoom-into-a-city. For CVLN Academy,
the equivalent "specific point" a first-time visitor's camera could
settle on is *not* a literal place but a **concrete, real professional
outcome already in the data** (a named métier, a real formation, a
real testimonial-shaped fact) rather than an abstract "welcome" banner.
`UNIVERSE_BEFORE_INTERFACE` (already a named doctrine in this repo's
own W2/W4 reports) is precisely this principle, already partially
adopted — Universal's contribution is the specific technique of
**one unbroken camera move from abstract-whole to concrete-specific**,
which the current Landing (per `ACADEMY_CURRENT_FUNNEL_AUDIT.md`
stage 01) does not yet do — manifesto and auth card render
simultaneously, no temporal sequence exists at all today.

---

### C. PlayStation 5 — the interface as a place, not a menu

**OBSERVED/SOURCE**: Sony's own "First look" announcement (`blog.
playstation.com`, Oct 15 2020 — content reached via search summary,
direct fetch blocked) states the **Control Center** gives "immediate
access to almost everything you need... at a single press of the
PlayStation button... all without leaving the game," and that
**Activities** are "displayed via on-screen cards in the Control
Center, enabling you to discover new gameplay opportunities... and jump
directly into levels or challenges" (source: PlayStation Blog, via
search, corroborated independently by `wccftech.com`, `gameskinny.
com`, `thesixthaxis.com`, `techradar.com` reporting on the same
official reveal). Some Activity cards support picture-in-picture,
letting a player watch/interact with the card **without leaving the
current game** (source: TheSixthAxis / MakeUseOf, via search). More
recent UI iterations moved the top navigation to separate system apps
from the content feed and let players switch tabs via L1/R1 without
extra scrolling (source: multiple 2023–2025 UI-update articles, via
search).

**PRINCIPE INFÉRÉ** (the mission's own framing — `INPUT → FOCUS →
CAMERA/WORLD RECOMPOSITION → CONTEXT REVEAL` — is exactly what H0.10
already built and verified, so this section states it as *confirmed
consistent with sourced PS5 behavior*, not as newly discovered):
1. **"Without leaving the game" is the load-bearing phrase** — every
   sourced description of the Control Center returns to this same
   idea: context (store, friends, trophies, help) opens *as an overlay
   on the still-running world*, never as a navigation event that
   replaces it. This is precisely H0.10's `CONTEXT` plane (dock
   opens, module recedes but stays visible, not unmounted) — already
   built, already tested (`ACADEMY_CURRENT_FUNNEL_AUDIT.md` stage
   12/13's `DEPTH_IS_SEMANTIC = REALIZED` finding).
2. **Cards, not pages** — Activities are self-contained, glanceable,
   individually actionable units surfaced *in response to current
   context* (what you're playing), not a static menu tree. This maps
   to `PRIMARY_ATTENTION`/`SECONDARY_CONTEXT` — one dominant thing,
   several genuinely-present-but-secondary things, never a flat grid.
3. **Fast tab-switching without full re-navigation** (L1/R1) is the
   real-product analogue of H0.10's `ZERO_NAVIGATION_BLOCKING` /
   retarget-safe physics — Sony solved the same "don't make me wait
   for the last transition to finish" problem with a hardware-input
   shortcut; Academy's own solution is software (interruptible spring
   physics), same underlying user need.

**APPLICATION CVLN RECOMMANDÉE**: PS5 is the reference requiring the
*least* translation — its "world persists, context overlays it, never
leaves it" principle is already H0.10's architecture (Camera Anchor
Contract, `CONTEXT` plane, attention tiers) and already scoped for
extraction in W-FUNNEL-1. The one genuinely new lesson for CVLN not yet
built: **Activities' "discover new opportunities you might have
missed"** framing — a card surfacing something *earned but not yet
seen* — maps directly onto the still-unbuilt Expansion moment (gap
matrix row "Expansion": real `is_unlocked` data, no reveal surface yet).

---

### D. Spotify — a catalogue that answers "what matters to me now"

**OBSERVED/SOURCE**: Spotify's Home personalization runs in two real,
documented stages — **candidate generation** (selecting the best
albums/playlists/artists/podcasts *for that listener*) then **ranking**
(ordering those candidates specifically for them) (source: Spotify
Engineering blog, "The Rise (and Lessons Learned) of ML Models to
Personalize Content on Home," Parts I & II, 2021, via search). Spotify
explicitly names its approach **"algotorial"** — a deliberate
combination of algorithmic personalization *and* human editorial/data
curation, not algorithm alone (source: Spotify Newsroom, "How Spotify
Uses Design To Make Personalization Features Delightful," Oct 2023, via
search). Spotify separates its personalization tech stack from its
experimentation tech stack specifically so that trying a new ranking
idea doesn't destabilize what's already working for real listeners
(source: Spotify Engineering blog, Jan 2026, via search). Deeper
UI-level detail (hero-card art-driven color, Now Playing continuity
into next recommendations) could not be independently re-verified this
session (direct fetch of the Newsroom article was blocked) — treat any
claim about the *exact visual mechanism* of artwork-driven color as
`PRINCIPE INFÉRÉ` from widely-observable public product behavior, not
as sourced from an official design document reached this session.

**PRINCIPE INFÉRÉ**:
1. **Personalization is a pipeline with an editorial check, not a raw
   model output** — the "algotorial" framing is the key transferable
   idea: a recommendation surface should combine *real derived signal*
   (what the learner has actually done — exactly the lifecycle-state
   evidence in `ACADEMY_LIFECYCLE_STATE_MODEL.md`) with *deliberate,
   human-set priority rules* (e.g. "always surface the next unlocked
   module before a tangential one"), never pure black-box ranking.
   This is precisely why `learning.py`'s `next_action` is
   **deterministic rules first** (own pole before other poles, first
   unlocked non-validated module) — already Spotify's own stated
   philosophy, arrived at independently.
2. **Separating what's stable from what's experimental** — Spotify's
   split tech stack for personalization vs. experimentation is a
   direct analogue for CVLN's own `ACADEMY_FUNNEL_IMPLEMENTATION_
   PLAN.md` flag strategy: new spatial/lifecycle behavior stays
   flag-gated and separable from the stable, tested `next_action`
   logic underneath it.
3. **The catalogue answers "now," not "everything"** — Home doesn't
   show the whole library; it shows a small, prioritized slice keyed to
   the current moment. This is the direct precedent for
   `MAX_PRIMARY_SPATIAL_FOCUS = 1` (H0.10's attention model) applied at
   the *page* level, not just the *rail* level: a Dashboard showing
   everything at equal weight is the "catalogue," not the "Home."

**APPLICATION CVLN RECOMMANDÉE**: the transferable mechanism is
**one ranked, evidence-based "what matters now" slot, backed by
deterministic rules the learner could in principle explain to
themselves** — not ML, not a black box (the mission itself forbids
inventing recommendation intelligence without real data/model,
`ACADEMY_TARGET_MATURITY_FUNNEL.md` Level 10). CVLN already has the
data half of this (`next_action`); what Spotify's pattern adds is the
**explicit separation between the ranking engine and the editorial/
business-priority layer on top of it** — worth preserving as an
architectural seam even while the ranking stays simple/deterministic
for a long time.

---

## 3. Cross-reference patterns confirmed present in the sourced material

| Pattern | A (NFS) | B (Universal) | C (PS5) | D (Spotify) |
|---|---|---|---|---|
| `WORLD_BEFORE_UI` | inferred (showcase-before-stats convention) | **sourced** (globe fully established before wordmark) | **sourced** ("without leaving the game") | inferred (Home before catalogue browse) |
| `FOCUS_BEFORE_INFORMATION` | inferred | **sourced** (Boston zoom precedes any text) | **sourced** (card selected → detail revealed) | **sourced** (ranking stage runs after candidate stage, i.e. relevance before volume) |
| `ANTICIPATION_BEFORE_REVEAL` | inferred | **sourced** (full sequence duration before wordmark) | inferred | inferred |
| `ENVIRONMENT_RESPONDS_TO_ATTENTION` | inferred | N/A (pre-recorded sequence, no interactivity) | **sourced** (Activities surface based on current game/context) | **sourced** (Home literally recomputed per listener/moment) |
| `SELECTION_CHANGES_THE_WORLD` | **sourced** (Autolog turns a chosen route/car into a social/competitive fact) | N/A | **sourced** (selecting a card changes what's on screen without a page change) | **sourced** (what you play changes what Home shows next) |
| `CONTENT_BEFORE_CONTROLS` | inferred | **sourced** | **sourced** | **sourced** |
| `NEXT_ACTION_EMERGES_FROM_CURRENT_CONTEXT` | **sourced** (Autolog's rival-beat prompts) | N/A | **sourced** (Activities: "discover... jump directly into") | **sourced** (ranked Home slate) |

## 4. Fundamental differences (unchanged from the mission's own framing, now evidence-checked)

- **Universal = one-shot cinematic revelation** — no interactivity, a
  single authored camera move, works because it happens exactly once
  per screening and never has to handle a return visit.
- **NFS = object-centered energy under real physical consequence** —
  the sourced material (real cars, real camera cars, Autolog's
  competitive stakes) is fundamentally about *stakes and weight*, not
  about a UI layout technique.
- **PS5 = spatial navigation with persistent context** — the only one
  of the four that is a genuine, repeated-use *operating system*, which
  is why it's the closest structural analogue to Academy (a returning,
  multi-session product) — not a coincidence that H0.10 already
  converged on PS5-shaped mechanics independently.
- **Spotify = statistical personalization with an editorial ceiling** —
  the only one of the four solving "too much content" rather than "not
  enough context"; Academy's catalogue is orders of magnitude smaller
  than Spotify's, so the *ranking-pipeline* lesson transfers, the
  *scale of the personalization problem* does not.

## 5–6. Transferable vs. forbidden

**Transferable** (mechanism only, verified against sourced material):
one continuous camera move from whole-to-specific before naming
anything (Universal); context overlays a persisted world rather than
replacing it (PS5); a single ranked "what matters now" slot driven by
explainable rules, with a named seam between the ranking and the
editorial layer (Spotify); a real action visibly changing what the
world says back (NFS/Autolog).

**Forbidden** (explicit, restated from the mission and reinforced by
this research — none of the sourced mechanisms require any of this):
no globe, no satellite/night-Earth visual, no film-grade camera
choreography budget, no car or vehicle metaphor, no "Activities feed"
visual language, no PlayStation button/DualSense iconography, no
Spotify green/circular-artwork/wave visual language, no algorithmic
personalization presented as smarter than it is, no fake "for you"
copy backed by nothing real.

## 7. Matrix: PRINCIPE → MÉCANISME → APPLICATION CVLN

| Principe | Mécanisme (sourced) | Application CVLN recommandée |
|---|---|---|
| World before name | Universal: full globe sequence before wordmark, one unbroken camera move | Landing's manifesto/world establishes *before* any auth card gets primary visual weight — sequenced, not simultaneous (fixes the `PARTIAL` finding in the current audit) |
| Context overlays, never replaces | PS5: Control Center "without leaving the game" | Every CVLN context surface (quiz/mission/mentor) keeps the enclosing world/module visible and receded — already H0.10's `CONTEXT` plane, extend to Dashboard-level overlays too |
| One ranked "now" slot | Spotify: candidate-generation → ranking, algotorial | Dashboard's single `PRIMARY_ATTENTION` = the real, deterministic `next_action` — never a grid of equally-weighted tiles |
| Action changes the world | NFS/Autolog: rival-beat becomes a social fact | A completed module/validated skill should visibly update the persistent environment (stade/botanical layer, formation signature) the moment it happens — not just update a database row silently |
| Specific over generic reveal | Universal: zoom into Boston, not "the world" in the abstract | Activation's convergence moment (mission §11) should land on the *specific* recommended formation/mission by name, not a generic "you're all set" |
| Fast, uninterrupted switching | PS5: L1/R1 tab switch; NFS: nothing queued mid-race | H0.10's retarget-safe physics (already built, verified stable) is the CVLN equivalent — port before building any new Hero motion |

## 8. Proposed CVLN Academy Hero System (architecture, not visual design)

**Not** H1 + subtitle + CTA + image + cards. Proposed structure, framed
as *the first state of the world*, not a section that disappears:

1. **VOID/SIGNAL** (0–2s): near-empty stage, one quiet signal (a
   single light/motif cue — no specific asset prescribed here) —
   establishes that *something* is about to compose itself, deliberately
   withholding content (Universal's anticipation-before-reveal).
2. **WORLD** (2–6s): the persistent environmental layer resolves
   (light field + botanical/progression layer, both already real H0.10
   primitives) — establishes scale and belonging before any specific
   content (Universal's whole-before-specific).
3. **FOCUS** (6–10s): one specific, concrete thing gains
   `PRIMARY_ATTENTION` — a real professional outcome or a real
   formation, not an abstract manifesto line (Universal's Boston-zoom
   principle, applied to real CVLN content).
4. **IDENTITY invitation**: the register/login card is present as
   `SECONDARY_CONTEXT`, not competing for primary weight, until a
   visitor acts (fixes the current `PARTIAL`/simultaneous-weight
   finding).
5. **ENTRY**: choosing register/login is a **camera anchor**, not a
   route change — the identity plane approaches (PS5-style context
   overlay, H0.8's Camera Anchor Contract), the world recedes but
   never unmounts.

This is a proposal for **W-FUNNEL-2 design work**, not implemented by
this document or by W-FUNNEL-1.

## 9. Storyboard, first 60 seconds (illustrative, not final copy/asset design)

| t | State | What the visitor perceives |
|---|---|---|
| 0–2s | VOID/SIGNAL | Near-empty, one quiet cue — calm, not blank |
| 2–6s | WORLD | Environmental layer resolves — light, depth, a sense of scale |
| 6–10s | FOCUS | One real, specific, concrete thing (outcome/formation) takes `PRIMARY_ATTENTION` |
| 10–20s | ORIENTATION | Visitor can explore laterally (if the public-discovery decision allows it) without committing to identity yet |
| 20–35s | INTENT | Visitor chooses to register/login — camera anchor begins, not a page swap |
| 35–50s | IDENTITY→ONBOARDING | Same world, identity plane approached, onboarding's real inputs (lang/métier/territoire/objectif) begin reshaping the environment as they're answered (mission §10's "world construction" idea) |
| 50–60s | ACTIVATION begins | Convergence moment starts assembling from the real onboarding payload (recommended formation + mission), landing on FOCUS→APPROACH→CONFIRM→HORIZON per mission §11 |

## 10–11. Continuity architecture

**Hero → Signup → Onboarding → Activation → First Value**: one
persistent backdrop (new, doesn't exist in `frontend/src` today per
`ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md` §2) mounted once above the
route-switched tree; each transition in this chain gets a Camera Anchor
Contract (H0.8 pattern) rather than a route-level fade; onboarding's
real field commits progressively reshape the same environment
(pole → light/motif, territoire → contextual layer only if truly
supported, objectif → nothing decorative — the mission explicitly warns
against fabricating personalization here).

**Rest of the lifecycle**: Dashboard/Formation/Roadmap/Module continue
the same environment (H0.10's proven 3-route continuity, generalized —
`ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md` §2); Quiz/Mission/Mentor
stay `CONTEXT`-plane overlays (already real); Proof/Progression surfaces
use the same attention-tier model to distinguish past/current/next/
future (mission §15); Monetization (once real) deliberately drops
intensity to LOW (mission §16, trust over spectacle); Retention's
return moment restores exact position (W-FUNNEL-6) rather than
re-running the Hero sequence — **the Hero only ever plays once, for a
true first visit; a returning user re-enters the world at their last
position, not at VOID/SIGNAL again**.

## 12–14. Camera/depth/light/environment/motion/sound/haptics, desktop/mobile — see existing docs

All of this is already specified and, for the camera/physics/attention/
occlusion core, already *built and verified* in the H0.10 lineage
(`docs/SPATIAL_H09_FULL_SPATIAL_FEEL_REPORT.md`,
`docs/SPATIAL_H10_PERCEPTUAL_REFINEMENT_REPORT.md`) and the extraction
plan (`docs/ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md`). This
research does not restate those — it confirms, via the four references,
that H0.10's existing choices (interruptible physics, context-overlay
planes, one primary attention target, restrained sound/haptics) are
independently consistent with how PS5 and, structurally, NFS's Autolog
already solve the same problems in shipped, sourced products — a
convergent-validity finding, not a reason to change anything already
built.

## 15. Technical recommendations (DOM/CSS/React/Framer Motion/Web Audio/Haptics)

No WebGL — none of the four references *required* it for the
mechanisms extracted here (Universal's globe is pre-rendered video, not
a runtime requirement; PS5/Spotify are DOM-equivalent UI layers on
their respective platforms). H0.10 already proves CSS 3D
(`perspective`/`translateZ`/`rotateY`) + a JS spring physics loop is
sufficient for the camera/depth/attention mechanisms this research
recommends adopting. Framer Motion (already likely available or easily
added per the repo's React/craco stack) is a reasonable *implementation
detail* for W-FUNNEL-2's Hero sequence specifically (declarative
sequencing of the VOID→WORLD→FOCUS states), but the underlying
rail/camera physics should stay the hand-rolled, verified-stable H0.10
spring model (`ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md` §3) — mixing
two physics systems for the same motion would be exactly the kind of
untested, competing-animation-system risk H0.9/H0.10's own bug-fix
history (CSS transition vs. JS physics double-damping, found and fixed)
already warns against.

## 16. Measurable acceptance criteria (does it feel like entering, not visiting)

1. **Zero simultaneous full-weight elements at t=0** — a frame capture
   at Hero mount must show exactly one element at `PRIMARY_ATTENTION`
   (same invariant H0.10 already tests for the rail).
   `OBSERVED/SOURCE`: Universal's sequencing, PS5's one-card-focus model.
2. **No hard cut between Hero and Onboarding** — a route/DOM inspection
   at the transition boundary must show the persistent backdrop's DOM
   node surviving un-remounted (same test method already used in H0.9/
   H0.10's `data-current` continuity checks).
3. **Time-to-first-real-content ≤ the sequence's own FOCUS beat**
   (~6–10s per the storyboard) — no visitor should wait through
   decoration before seeing something real and specific.
4. **A returning visitor never replays VOID/SIGNAL** — testable via
   the same `RETURN_TO_POSITION` mechanism W-FUNNEL-6 builds.
5. **Reduced-motion visitors reach the same informational end-state**
   (world established, identity reachable) in a flattened, non-animated
   sequence — same accessibility invariant already proven across every
   H0.x wave.

---

## Sources consulted (via search-tool synthesis, this session)

- [designyourway.net — Universal Pictures Logo History](https://www.designyourway.net/blog/universal-pictures-logo/)
- [PRNewswire — Universal Pictures new animated logo (2012)](https://www.prnewswire.com/news-releases/universal-pictures-continues-yearlong-centennial-celebration-with-reveal-of-new-animated-logo-141017033.html)
- [Weta Workshop — Universal Pictures logo announcement](https://www.facebook.com/WetaWorkshop/posts/new-universal-pictures-logo-designed-by-our-colleagues-at-weta-digital-httpwwwyo/336021023114779/)
- [Moving Logo Wiki — Universal Pictures 2012–](https://movinglogo.fandom.com/wiki/Universal_Pictures/2012-)
- [PlayStation Blog — First look: PS5's next-generation UX](https://blog.playstation.com/2020/10/15/first-look-playstation-5s-next-generation-user-experience/)
- [TheSixthAxis — PS5 Activity Cards guide](https://www.thesixthaxis.com/2020/11/11/ps5-activity-cards-guide-how-they-work-ps4/)
- [Spotify Engineering — Rise of ML Models to Personalize Home, Part I](https://engineering.atspotify.com/2021/11/the-rise-and-lessons-learned-of-ml-models-to-personalize-content-on-home-part-i) / [Part II](https://engineering.atspotify.com/2021/11/the-rise-and-lessons-learned-of-ml-models-to-personalize-content-on-home-part-ii)
- [Spotify Newsroom — How Spotify Uses Design to Make Personalization Delightful](https://newsroom.spotify.com/2023-10-18/how-spotify-uses-design-to-make-personalization-features-delightful/)
- [Spotify Engineering — Separate tech stacks for personalization/experimentation](https://engineering.atspotify.com/2026/1/why-we-use-separate-tech-stacks-for-personalization-and-experimentation)
- [NFS Wiki (Fandom) — Autolog](https://nfs.fandom.com/wiki/Autolog), [The Run/Autolog](https://nfs.fandom.com/wiki/Need_for_Speed:_The_Run/Autolog)
- [racinggames.gg — The Takedown Era: Criterion's early NFS games](https://racinggames.gg/article/the-takedown-era-a-retrospective-on-criterions-early-need-for-speed-games)
- [Top Gear — Behind the scenes on Need for Speed](https://www.topgear.com/car-news/movies/behind-scenes-need-speed), [Destructoid — camera cars](https://www.destructoid.com/behind-the-scenes-with-the-camera-cars-of-need-for-speed/)

Internal (this repository): `docs/ACADEMY_CURRENT_FUNNEL_AUDIT.md`,
`docs/ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md`,
`docs/SPATIAL_H09_FULL_SPATIAL_FEEL_REPORT.md`,
`docs/SPATIAL_H10_PERCEPTUAL_REFINEMENT_REPORT.md`,
`docs/SPATIAL_LEARNING_W4C_EXPERIENCE_GAP.md`.
