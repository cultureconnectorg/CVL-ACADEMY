# CVLN Academy — Delivery Mode Audit (E_LEARNING / PHYSICAL / HYBRID)

```
ADDENDUM (2026-09-04, ACA-0004): the "AMBIGUOUS" headline finding below
is RESOLVED. The Founder's ACA-0004 decision makes `db.formations.
contexts` (INTERNAL/EXTERNAL/BRIDGE) — not `catalog_cartography.
DELIVERY_FORMATS` — the authoritative delivery-architecture source going
forward. `delivery_formats` is left exactly as-is (untouched); it is
simply no longer read by the new derivation. See
`docs/ACADEMY_ACA0004_DELIVERY_ARCHITECTURE_TRUTH_REPORT.md` and
`backend/fms_canonical/delivery_architecture.py`. The rest of this audit
(method, other findings) remains accurate as a historical record.
```

```
MODE = AUDIT_ONLY. No product code changed to produce this document.
Every claim below cites a specific file/line read this session. Where a
keyword search returned zero real hits, that is stated explicitly as a
negative finding, not silently omitted.
STOP_AFTER_DELIVERY = TRUE. H1 = NOT_AUTHORIZED. W-FUNNEL-2 UI work not
started by this pass.
```

## Method

Repository-wide search (`grep`, `backend/` + `frontend/src/`, excluding
`node_modules`/`.venv`/`__pycache__`) for every term listed in the
mission's §14, plus direct reads of every file a hit implicated. No
concept below is classified from memory or assumption — a "MISSING"
verdict means the search ran and found nothing real, not that the
search wasn't run.

## Headline finding

**A delivery-mode taxonomy already exists in the backend — but only as
a coarse, catalog-level label, not as an operational data model.**
`backend/catalog_cartography.py:22`:

```python
DELIVERY_FORMATS = ["E_LEARNING", "PRESENTIEL", "HYBRIDE"]
DEFAULT_FORMAT = ["E_LEARNING"]
PRO_FORMAT = ["E_LEARNING", "PRESENTIEL", "HYBRIDE"]
```

This is real, typed (`FormationCartography.delivery_formats: List[str]`,
`backend/models.py:110`), and **already surfaced in the API** —
`GET /formations` includes `delivery_formats` in its summary shape
(`backend/api/formations.py:~72`), reading it straight off
`cartography.delivery_formats`. **It is `AMBIGUOUS`, not `EXISTS`
cleanly**, for four concrete reasons:

1. **Naming mismatch**: the repo says `PRESENTIEL`, the mission's
   target taxonomy says `PHYSICAL`. Semantically equivalent, not
   identical strings — a mapping decision, not a rename, per §17's
   "do not rename existing production concepts unnecessarily."
2. **Not per-formation truth, a shared constant**: every one of the 30
   real formations in `_FORMATION_CARTOGRAPHY` gets either
   `DEFAULT_FORMAT` (`["E_LEARNING"]`, 9 formations) or `PRO_FORMAT`
   (`["E_LEARNING", "PRESENTIEL", "HYBRIDE"]`, 21 formations) — the
   *same two lists*, reused wholesale. No formation has been
   individually assessed for which modes it can actually be delivered
   in; this reads as an aspirational market-positioning tag, not a
   confirmed operational capability.
3. **Zero frontend consumption**: `grep` for `delivery_format`/
   `PRESENTIEL`/`E_LEARNING`/`HYBRIDE` across `frontend/src/pages/
   Formations.js`, `FormationDetail.js`, `Onboarding.js` returns
   **zero hits**. The field is computed, typed, and shipped in the API
   response — and displayed nowhere.
4. **No operational backing whatsoever**: nothing in the repository
   models a session, a date, a location, a capacity, an attendance
   record, or an enrollment distinct from e-learning module unlock —
   see below. `PRESENTIEL`/`HYBRIDE` currently mean "this formation's
   *subject matter* could in principle be taught in person," not
   "you can actually book a real physical session of this."

## Concept-by-concept classification

| Concept | Status | Evidence |
|---|---|---|
| `delivery_mode` field (exact name) | **MISSING** | Zero hits for the literal string; the real equivalent is `cartography.delivery_formats` |
| Delivery-mode taxonomy (any name) | **AMBIGUOUS** | See headline finding above |
| `modality`/`online`/`distance`/`elearning` (literal strings) | **MISSING** | Zero real hits — `E_LEARNING` is the only real spelling in use |
| `session` (training-session sense) | **MISSING** | All 17 file hits are unrelated: JWT/HTTP auth sessions (`auth.py`, `api/auth.py`), Mentor conversation sessions (`MentorConversation.session_id`, `api/mentor.py`, `MentorPanel.js`), a `physics.js` internal test-helper name collision. Zero hits describe a scheduled training session with a date/time. |
| `cohort` | **PARTIAL** (real, but not a training-session concept) | `models.py`'s real `Cohort` model (`id, org_id, name, pole, starts_at, ends_at`) — a B2B *organizational grouping* (an org's group of learners), built for `orgs.py`'s invitation flow, not a scheduled physical session. `starts_at`/`ends_at` on `Cohort` are the closest existing thing to session dates in the whole repo, but a cohort is not tied to a specific formation's physical delivery, a location, or a capacity |
| `classroom` | **MISSING** | Zero hits |
| `location` (physical-venue sense) | **MISSING** | The 3 real hits are all `window.location`/`useLocation()` (browser/router APIs) — unrelated. `User.territoire` (`martinique/guadeloupe/guyane/france/caraibe/diaspora/autre`) is a real geographic field, but it describes the *learner's* origin for onboarding personalization, not a *formation session's* venue |
| `capacity` | **MISSING** | Zero hits anywhere |
| `attendance`/`presence` (physical sense) | **MISSING** | The 4 "presence" hits are all `isPedagogicalContext`/Mentor-presence naming (W3-C's "contextual presence" doctrine) — an unrelated, already-shipped UX concept, not physical attendance |
| `inscription`/`enrollment`/`registration` (training-specific sense) | **MISSING** for training; **PARTIAL** for the general concept | Real hits are: CRA service-worker `registration` (irrelevant), `auth.py`'s account *registration* (identity, not formation enrollment), `Invitation`/`Organisation`/`Cohort` (`orgs.py`) — a real org-invite acceptance flow, structurally the closest existing pattern to "apply to join something," but built for B2B account provisioning, not per-session physical-training enrollment |
| `funding`/`cpf`/`afdas` | **PARTIAL, reference-only** | `backend/external_calibration.py:120-134`: real, named `SOURCES["cpf_eligibility"]`/`SOURCES["afdas"]` entries — each a `{label, url}` pointing at the real CPF/Afdas government pages, aggregated into `FUNDING_DEFAULT`. Consumed by `catalog_cartography.py`'s `market_evidence` field. **This is citation/calibration metadata, not a funding eligibility check or integration** — no code determines whether a specific learner is CPF/Afdas-eligible, and `Formation.economics.funding_options` is populated with the literal placeholder string `["needs_external_calibration"]` (`catalog_cartography.py:694`), never real values |
| `hybrid`/`hybride` (delivery-mode sense) | **AMBIGUOUS** — see above | Real hits also include an unrelated pedagogical concept: `HOS-01`'s "lieu hybride créatif" (hybrid *venue*, a physical/hospitality space concept for one specific formation's subject matter) — do not confuse with delivery-mode HYBRID; this is content about hybrid venues, not a hybrid delivery flow |
| `attendance != progress` distinction | **N/A — no attendance model exists to conflate** | Confirmed there is currently no risk of the mission's §10 conflation because only one of the two concepts (`ModuleProgress`) exists at all |

## Public discovery — backend is already ahead of the frontend

A genuinely important, previously-unsurfaced finding: **`GET /formations`
and `GET /formations/{code}` already support unauthenticated access,
correctly and deliberately** — `backend/api/formations.py` uses
`Depends(get_current_user_optional)` (real `Optional[User]`,
`backend/auth.py:217-226`) on both routes. For an unauthenticated
caller, `get_formation` returns the **full formation detail including
modules**, with every module marked `is_unlocked: true` — an
intentional "preview" branch (`backend/api/formations.py:93-100`), not
an accident or an oversight.

Every *mutating*/personalized learning endpoint
(`learning.py`'s phase/deliverable/mini-mission/learning-path,
`quizzes.py`'s submit, `missions.py`'s accept/submit) requires **real**
(non-optional) `get_current_user` — confirmed by grep, zero exceptions.
This means the backend **already implements exactly** the Founder's
newly-stated policy: `PUBLIC_LEARNING_ACCESS = NO` (verified: no write
path is reachable without identity) alongside real content browsable
before identity.

**The only thing currently preventing `PUBLIC_FORMATION_DISCOVERY = YES`
from being real today is `frontend/src/App.js:58-60`'s `<Protected>`
wrapper** on `/formations` and `/formations/:code` — a frontend
routing decision, not a backend capability gap. This is flagged here as
evidence for the architecture doc; **no route change is made by this
audit pass**, per this mission's own explicit "do not start broad
W-FUNNEL-2 UI work yet."

## Monetization capability classification (mission §8)

| Capability | Classification | Evidence |
|---|---|---|
| Direct payment (any modality) | **MISSING** | No payment processor, checkout, or transaction code exists anywhere (re-confirmed this session; unchanged since `ACADEMY_CURRENT_FUNNEL_AUDIT.md`) |
| Subscription | **MISSING** | No subscription model exists |
| CPF eligibility (real check) | **MISSING** | `SOURCES["cpf_eligibility"]` is a citation link, not an eligibility API call |
| Afdas funding | **MISSING** | Same — citation only |
| Employer/institutional funding | **MISSING** | No model exists; `Organisation`/`Cohort` could structurally carry a B2B billing relationship later, but nothing does today |
| `Formation.economics.funding_options` (data slot) | **INTERFACE_ONLY** | Real, typed field (`FormationEconomics.funding_options: List[str]`), populated only with the placeholder `["needs_external_calibration"]` — a real slot, no real content |
| CVLN Wallet (JCC/token ledger) | **REAL** (unrelated to tuition/funding) | Confirmed real and working (`ACADEMY_CURRENT_FUNNEL_AUDIT.md` stage 22) — badge/certification credit, not a payment or funding mechanism for enrollment |

## What this audit did NOT find (explicitly, so absence isn't assumed)

No trace of: a `TrainingSession`/`Session` model, a `Location`/`Venue`
model, a `Capacity`/seat-count field, an `Attendance`/`Absence` model,
a `Trainer`/`Facilitator` assignment distinct from the existing
`trainer` role (which gates dashboard access, not session facilitation),
a cancellation/waitlist concept, or any admin/trainer surface for
scheduling. `AdminDashboard.js`/`TrainerDashboard.js` were checked for
scheduling UI — neither contains one (their scope, per
`ACADEMY_CURRENT_FUNNEL_AUDIT.md`, is CMS content lifecycle and
correction workflows, not session logistics).

## Decision-gate inputs (answered fully in the chat response, not duplicated here)

See the chat response for the required `§16` answer block
(`E_LEARNING_SUPPORT=`, `PHYSICAL_TRAINING_SUPPORT=`, etc.) — this
document is the evidence base those answers cite.
