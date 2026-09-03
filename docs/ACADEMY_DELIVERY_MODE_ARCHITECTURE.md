# CVLN Academy — Delivery Mode Architecture (E_LEARNING / PHYSICAL / HYBRID)

```
MODE = ARCHITECTURE_PROPOSAL. This document designs; it does not implement.
No route, model, or seed data is changed by this pass. Every proposal
below is additive to what docs/ACADEMY_DELIVERY_MODE_AUDIT.md found —
nothing here contradicts that evidence.
STOP_AFTER_DELIVERY = TRUE. H1 = NOT_AUTHORIZED. FMS pedagogy untouched.
```

## 0. Reading order

This is the second of three required documents. It assumes
`ACADEMY_DELIVERY_MODE_AUDIT.md` as its evidence base and feeds
`ACADEMY_DELIVERY_MODE_FUNNEL_MATRIX.md`. Nothing here is authorized to
build yet — see §7 "What this document does NOT authorize."

## 1. Product rule, restated as an architecture constraint

`FORMATION_DELIVERY_MODE = REQUIRED`, taxonomy `{E_LEARNING, PHYSICAL,
HYBRID}`. The audit found a real but ambiguous backend equivalent
(`catalog_cartography.DELIVERY_FORMATS = ["E_LEARNING", "PRESENTIEL",
"HYBRIDE"]`). The architecture decision is:

- **Map, do not rename.** `PRESENTIEL → PHYSICAL` and `HYBRIDE → HYBRID`
  become a translation performed at the API boundary (a small constant
  dict in the formations router), not a rewrite of
  `catalog_cartography.py`'s French internal vocabulary. The seed data,
  written in French throughout (`primary_job`, `contexts`, `audience`,
  etc.), keeps its own internal language; the mission's English taxonomy
  is what the API contract and frontend speak. This satisfies §17's "do
  not rename existing production concepts unnecessarily" while still
  giving the frontend the exact three-value enum §1 requires.
- **Stop treating `delivery_formats` as capability truth.** Today it is
  reused wholesale across formations (9 get `DEFAULT_FORMAT`, 21 get
  `PRO_FORMAT` — audit §"Headline finding"). Before any UI reads it to
  decide what to *offer* a learner, each formation needs a real,
  individually-assessed value — see §3 below. Until that per-formation
  review happens, `delivery_formats` may keep informing marketing copy
  ("this profession can, in principle, be taught in person") but must
  **not** drive a "Choisir une session" CTA, because no session data
  exists to back it (§4 below, and audit's monetization/session
  findings).

## 2. Shared Academy spine (mission §2)

```
DISCOVERY → IDENTITY/FREK-ID → ORIENTATION → ACTIVATION → PROGRESSION
   → PROOF → CERTIFICATION → RETENTION → EXPANSION
```

Concretely, in terms of what already exists:

- **DISCOVERY**: `GET /formations`, `GET /formations/{code}` — already
  real, already supports unauthenticated preview (audit's "Public
  discovery" section). This stage is genuinely shared across all three
  modes; formation *browsing* does not branch.
- **IDENTITY/FREK-ID**: existing auth + FREK-ID onboarding — shared,
  unchanged.
- **ORIENTATION**: existing `Onboarding.js` + recommendation logic —
  shared entry point; the mode-specific prerequisite/eligibility checks
  (mission §4) are additive to it, not a fork of it.
- **ACTIVATION → PROGRESSION → PROOF → CERTIFICATION**: this is where the
  three modes genuinely diverge (§3–§5 below), because "progression"
  itself means a different domain object per mode (mission §10).
- **RETENTION / EXPANSION**: shared return surfaces (Dashboard, wallet,
  next_action) stay shared; what feeds `next_action` per mode differs
  (an e-learning learner's next action is a module; a physical learner's
  next action may be "your session is in 3 days" or "your attendance is
  pending trainer validation").

The single-world requirement (mission §12 "never feel like separate
website/LMS/booking-site") is satisfied by keeping all three modes inside
the *same* `FormationDetail`/`Dashboard`/`RouteTransition` surfaces and
letting mode-specific sections render conditionally inside them, rather
than routing to disjoint page trees per mode.

## 3. E-learning flow — no architecture change required

```
DISCOVER → SELECT FORMATION → IDENTITY/FREK-ID → ORIENTATION →
ELIGIBILITY/ACCESS CHECK → START → MODULE → CONTENT →
WORKSHOP/DELIVERABLE → QUIZ → MINI-MISSION → PROGRESSION → PROOF →
CERTIFICATION → NEXT ACTION
```

This is, almost verbatim, the flow the product already runs today
(`is_module_unlocked`, `ModuleProgress`, quiz/mission engines, badges,
certification). **No new domain model is proposed for e-learning.** The
only real gap is presentational: nothing currently *labels* a formation's
page as "this is the e-learning flow" versus a generic "formation page,"
because there has never been a second flow to distinguish it from. That
labeling is a W-FUNNEL-2 UI concern, not an architecture gap — flagged
here, not designed further, per §7 below.

## 4. Physical training flow — real new domain models required

```
DISCOVER → SELECT PHYSICAL FORMATION → IDENTITY/FREK-ID → ORIENTATION →
PREREQUISITES → CHOOSE SESSION → CHOOSE LOCATION → AVAILABILITY →
REGISTRATION/APPLICATION → FUNDING OR PAYMENT STATE → CONFIRMATION →
PRE-SESSION INSTRUCTIONS → ATTENDANCE → ASSESSMENT → PROOF →
CERTIFICATION/ATTESTATION → FOLLOW-UP/NEXT ACTION
```

The audit confirmed **zero** operational backing for this flow: no
Session/Location/Capacity/Attendance model exists anywhere (audit "What
this audit did NOT find"). `Cohort` (org_id, name, pole, starts_at,
ends_at) is the nearest existing shape but is a B2B org-grouping concept,
not a bookable physical session — reusing it directly would conflate two
different truths (an org's cohort membership vs. a specific session
someone registered for) and violate mission §9's
`PHYSICAL_ENROLLMENT != MODULE_UNLOCK` by overloading a B2B field for an
individual-facing concept it wasn't built for.

**Proposed new domain models (design only, not created this pass):**

| Model | Purpose | Key fields (proposed) |
|---|---|---|
| `TrainingSession` | one bookable, dated occurrence of a formation delivered physically | `id, formation_code, starts_at, ends_at, location_id, trainer_id, capacity, seats_taken, status (SCHEDULED/CONFIRMED/CANCELLED/COMPLETED)` |
| `TrainingLocation` | a real venue | `id, name, address, territoire, capacity_default` |
| `SessionEnrollment` | one learner's registration to one session — distinct from `ModuleProgress` per mission §9/§10 | `id, session_id, user_id, status (APPLIED/CONFIRMED/WAITLISTED/CANCELLED), funding_status, applied_at, confirmed_at` |
| `AttendanceRecord` | trainer-validated presence, per session per learner | `id, session_id, user_id, present (bool), validated_by, validated_at` |
| `AssessmentResult` | practical/jury evaluation, distinct from e-learning quiz | `id, session_id, user_id, result, evaluator_id, evaluated_at` |

These are proposed as **separate collections/domain objects**, never as
new fields bolted onto `Formation`/`ModuleProgress` — this is the direct
architectural answer to mission §9 ("design separate domain semantics; do
not overload e-learning fields") and §10 (four distinct truths, never
merged into one percentage).

`PHYSICAL_SESSION_AVAILABILITY = REAL_DATA_ONLY` (mission §4) means: this
flow **cannot ship any UI** — not even a read-only "upcoming sessions"
list — until `TrainingSession`/`TrainingLocation` exist and are
populated with real Founder-provided data. There is currently no
substitute; a placeholder session would be exactly the "fake 3 places
left" the mission forbids. This is the flow's hard blocker, not a
sequencing preference.

## 5. Hybrid flow — composition model, not a merge

Mission §5 is explicit: hybrid is not "duplicate e-learning + physical,"
and different formations may compose it differently, so this document
does **not** propose one global hybrid sequence. Instead, the proposed
architecture is a **composition descriptor per formation**:

```
HybridComposition {
  formation_code: str
  steps: [
    { type: "E_LEARNING_MODULE", ref: <module_code> },
    { type: "PHYSICAL_SESSION",  ref: <training_session_id or slot label> },
    { type: "E_LEARNING_MODULE", ref: <module_code> },
    { type: "ASSESSMENT",        ref: <assessment kind> },
    ...
  ]
}
```

- Each step's completion is read from **its own domain truth**
  (`ModuleProgress` for an e-learning step, `AttendanceRecord`/
  `AssessmentResult` for a physical step) — never a shared counter. This
  is the direct mechanism satisfying
  `HYBRID_PROGRESS_MUST_NOT_DOUBLE_COUNT`: a hybrid learner's overall
  progress is `completed_steps / total_steps` computed by checking each
  step's *own* source of truth once, not by summing an e-learning
  percentage and a physical percentage (which is exactly how double
  counting would happen).
- The example sequence in mission §5 (ONLINE PREPARATION → PHYSICAL
  SESSION → ONLINE FOLLOW-UP → PRACTICAL ASSESSMENT → PROOF) becomes one
  *possible* `HybridComposition`, not a hardcoded flow — matching the
  mission's own instruction that different formations may sequence
  differently.
- **Naming collision flagged again** (from the audit): formation
  `HOS-01`'s "lieu hybride créatif" is subject-matter content (a hybrid
  *venue* concept the formation teaches about), unrelated to
  delivery-mode HYBRID. Whoever eventually assigns `HOS-01` a delivery
  mode must not infer HYBRID delivery from that text.
- This model is **not implementable today** for the same reason physical
  is blocked: it depends on `TrainingSession` existing for its physical
  steps. Proposed here as a design, not built.

## 6. Cross-cutting rules carried into the architecture

- **§6 CTA semantics** — proposed mapping (frontend copy layer, not a new
  backend concept):
  | Mode | CTA states (indicative) |
  |---|---|
  | E_LEARNING | "Découvrir" (unauth) → "Commencer" (first module) → "Continuer" (in progress) |
  | PHYSICAL | "Voir les sessions" (sessions exist) → "Choisir une session" → "Demander une inscription" — **and, honestly, "Sessions à venir bientôt" when none exist**, never a generic "Start" |
  | HYBRID | "Voir le parcours" → "Voir les étapes" |
  A single shared `formation.delivery_modes: string[]` (the mapped,
  English-taxonomy value from §1) is what the frontend switches on to
  pick the CTA set — no separate "is this hybrid" boolean needed.
- **§7 Public discovery** — the audit already found the backend
  structurally ready (`get_current_user_optional` on both formation
  read routes). Architecturally, the only proposed change is at the
  frontend route table (`frontend/src/App.js`'s `<Protected>` wrapper
  around `/formations` and `/formations/:code`) — explicitly **not**
  executed in this pass (§7 below). For PHYSICAL, "public discovery may
  show real session data if safely available" — architecturally this
  means the same unauth-preview branch in `get_formation` would, once
  `TrainingSession` exists, additionally expose upcoming sessions'
  `starts_at`/`location`/`seats_remaining` (never learner-identifying
  enrollment data) to anonymous callers — a straightforward extension of
  the existing preview branch, not a new access model.
- **§8 Monetization** — no architecture change proposed beyond what the
  audit already found: `Formation.economics.funding_options` stays
  `INTERFACE_ONLY` until real CPF/Afdas/employer integrations exist.
  `E_LEARNING_PAYMENT != PHYSICAL_TRAINING_PAYMENT` is honored by
  attaching payment/funding state to `SessionEnrollment` (physical) and,
  separately, to a not-yet-designed e-learning purchase record — the two
  must never share a status enum, since "paid" means different things
  (access to a module vs. a confirmed physical seat).
- **§11 Proof model** — direct consequence of §4/§5's models:
  e-learning proof = existing module/quiz/deliverable/mission chain;
  physical proof = `AttendanceRecord` + `AssessmentResult` +
  trainer/jury validation; hybrid proof = the union of whichever steps
  a given `HybridComposition` actually contains.
- **§12/§13 Spatial & Hero continuity** — no new spatial mechanism is
  proposed; the existing `spatial-state.js`/`motion-tokens.js`/W-FUNNEL-1
  extracted engine already models intensity as a per-screen concern, so
  the suggested intensity table (DISCOVERY=HIGH … REGISTRATION FORM=LOW)
  is a *configuration* of existing infrastructure once a future wave
  wires physical-mode screens into it — not a new capability to build.

## 7. What this document does NOT authorize

Per mission §18, this is a correction-and-preparation pass. Explicitly
**not** done, decided-to-build, or scheduled by this document:

- No `TrainingSession`/`TrainingLocation`/`SessionEnrollment`/
  `AttendanceRecord`/`AssessmentResult`/`HybridComposition` model is
  created in code. §4/§5 are proposals for a future authorized wave.
- No change to `frontend/src/App.js`'s `<Protected>` wrapper.
- No change to `catalog_cartography.py`'s `DELIVERY_FORMATS`/per-formation
  values, and no per-formation re-assessment of which modes each of the
  30 formations can really be delivered in (§1's stated prerequisite for
  ever using `delivery_formats` as capability truth) — that review needs
  Founder/operational input this pass cannot manufacture.
- No Landing/Onboarding redesign, no checkout, no fake session data, no
  FMS migration — all explicitly reiterated from mission §18.

Everything above is a proposal for the Founder to authorize, in whole or
in part, as a future W-FUNNEL-2 (or later) wave.
