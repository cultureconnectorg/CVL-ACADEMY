# CVLN Academy — Funnel Gap Matrix (W-FUNNEL-0)

```
Columns exactly as specified in the mission brief §41. One row per
funnel stage. Grounded in ACADEMY_CURRENT_FUNNEL_AUDIT.md — this table
is the decision surface, that document is the evidence.
```

| STAGE | CURRENT_STATUS | CURRENT_ROUTE | CURRENT_BACKEND | CURRENT_VALUE | MISSING_VALUE | SPATIAL_STATUS | TARGET_SPATIAL_BEHAVIOR | DOMAIN_DEPENDENCY | WAVE | TEST | ROLLBACK |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Discovery | PARTIAL | `/` | none needed | Landing manifesto | Public formation preview (currently `<Protected>`-gated) | LOW (2 primitives used) | MEDIUM/HIGH, world-before-interface | Product decision: what's safe to expose pre-auth | W-FUNNEL-2 | `landing-spatial.spec.js` (extend) | Flag `ACADEMY_SPATIAL_SHELL` off → current Landing |
| Registration | EXISTS | `/` (inline) | `POST /auth/register` | Real JWT+refresh, FREK-ID mint | Distinct spatial entry moment (camera anchor into identity plane) | LOW | LOW/MEDIUM, calm, DOM-form-first | None — pure presentation | W-FUNNEL-2 | new: register→onboarding E2E (needs backend in test env) | Flag off → current inline form |
| Authentication | EXISTS core / BLOCKED_EXTERNAL (OAuth) | `/` (inline) | `auth.py`, 12 routes | login/logout/refresh/reset real | OAuth needs provider creds; 2FA has no frontend | LOW | LOW, stable, no motion while typing | OAuth: BLOCKED_EXTERNAL (env vars) | W-FUNNEL-2 (2FA UI); OAuth out of scope until creds exist | `auth-guards.spec.js` (exists) | N/A (backend unchanged) |
| Identity/FREK-ID | EXISTS | `/frek-profile` | `progression.py` | Real signals/stade/profile | Spatial continuity treatment | not scored | MEDIUM, proof-grade not gamey | None | W-FUNNEL-4 | new | Flag off → current page |
| Onboarding/Orientation | EXISTS | `/onboarding` | `onboarding.py` | 4 real inputs, real options | "World constructs around you" spatial treatment (§10) | not built | MEDIUM, each answer visibly reshapes the world | None — same payload shape | W-FUNNEL-2 | new: options + complete round-trip | Flag off → current form wizard |
| Activation | EXISTS (backend strong) | (part of onboarding response) | same as above | Real convergence payload | Dedicated FOCUS→APPROACH→CONFIRM→HORIZON moment | not built | HIGH, one strong non-gamey moment | None — payload already complete | W-FUNNEL-2 | new | Flag off → plain result render |
| First Value | PARTIAL | (same) | (same) | Same payload reused | Distinct instrumentation/moment separate from Activation | n/a | MEDIUM | None | W-FUNNEL-2 | event only | N/A |
| Dashboard/Return | EXISTS | `/dashboard` | 5 real GETs incl. `next_action` | Real aggregated summary | Personal-World layout (PRIMARY/SECONDARY/PERIPHERAL/LATENT); RETURN_TO_POSITION | not built | HIGH, exactly one PRIMARY_ATTENTION | None | W-FUNNEL-3 (shell) + W-FUNNEL-6 (return) | new | Flag `ACADEMY_SPATIAL_SHELL` off → current tile dashboard |
| Formation Discovery/Selection | EXISTS (gated) | `/formations`, `/formations/:code` | `formations.py` | Real catalog+detail | Public-safe preview variant | PARTIAL (W2-D, W4-C: ONE_DOMINANT_FOCUS partial) | HIGH | Same gate decision as Discovery | W-FUNNEL-2/3 | `formations-discovery.spec.js` (exists) | Flag off → current grid |
| Learning Path/Module | EXISTS, strongest surface | `/roadmap`, `/formations/:fc/modules/:mc` | `learning.py`, real phase state machine | Real, deeply tested | Nothing missing structurally — H0.10 intensity tiers only | REALIZED (W3-A/B/D/E, W4-C: DEPTH_IS_SEMANTIC fully realized) | HIGH (Hub/Formation) → LOW (Module reading) | None — preserve, extend intensity only | W-FUNNEL-3 | 4 real specs exist | Flag off → current (already good) behavior |
| Quiz | EXISTS | (in-module) | `quizzes.py` | Real scoring+signals+cc | Spatial: LOW/MEDIUM intensity, context-plane behind | not built | LOW/MEDIUM, world visible behind | None | W-FUNNEL-4 | `module-journey-context.spec.js` (exists) | Flag off → current modal |
| Mission/Practice | EXISTS | `/missions` + in-module | `missions.py` | Real accept/submit | Spatial: MEDIUM, task-focused context plane | not built | MEDIUM | None | W-FUNNEL-4 | new | Flag off → current page |
| Mentor Context | EXISTS, already contextual | in-module | `mentor.py` + Agent Factory | Real Claude-backed chat | Nothing missing — already meets mission §14 | REALIZED (W3-C) | MEDIUM, preserve as-is | None | N/A — preserve | `mentor-presence.spec.js` (exists) | N/A |
| Progression | EXISTS | `/frek/profile`, `/progression/summary` | `progression.py` | Real stade math | ACQUIRED/CURRENT/NEXT/HORIZON spatial layout | not built | MEDIUM/HIGH | None | W-FUNNEL-4 | new | Flag off |
| Skills | EXISTS | `/skills` | `skills.py` | Real evidence registry | Proof-grade spatial treatment (not trophy room) | not scored | MEDIUM/HIGH | None | W-FUNNEL-4 | new | Flag off |
| Badges | EXISTS | `/badges` | `badges.py` + `badges_engine.py` | Real threshold awards | Same as Skills | not scored | MEDIUM/HIGH | None | W-FUNNEL-4 | new | Flag off |
| Certification | EXISTS | `/certifications` | `certification.py`, real PDF attestation | Real rubric/attempt/grade lifecycle + one real domain event | Consequential, professional spatial treatment (no celebration) | not scored | MEDIUM/HIGH | None | W-FUNNEL-4 | new | Flag off |
| Proof/FREK Profile | EXISTS | `/frek-profile` | see Identity | Real SHA-256 evidence hashes | Spatial "past/current/next/future" framing | not scored | MEDIUM | None | W-FUNNEL-4 | new | Flag off |
| Wallet | EXISTS internal / BLOCKED_EXTERNAL passes | `/wallet` | `wallet.py` | Real JCC ledger | Apple/Google pass signing (needs certs Academy doesn't have) | not scored | MEDIUM | Pass signing: BLOCKED_EXTERNAL | Ledger UI: W-FUNNEL-5; passes: blocked | new | Flag off |
| Monetization | MISSING | none | none (data model only: `FormationEconomics`) | Pricing *data* exists | Entire transaction layer: checkout, payment processor, subscription state | n/a | LOW, trust/clarity first | **Full**: no payment backend exists — build interfaces only, mark transactions BLOCKED | W-FUNNEL-5, interface-only | new, explicitly excludes "purchase succeeds" until real | Flag `ACADEMY_LIFECYCLE_ENGINE`/commercial-state off entirely |
| Retention | PARTIAL | `/dashboard` | `learning.py`'s `next_action` (real) | Real deterministic next-action | RETURN_TO_POSITION (route/scroll/rail/camera); "continue where you were" copy | not built | MEDIUM/HIGH | None — pure frontend state | W-FUNNEL-6 | new | Flag `ACADEMY_CONTINUATION_ENGINE` off → current fresh-dashboard-every-time |
| Expansion | PARTIAL | `/roadmap`, `/dashboard` | `learning.py`'s unlock logic (real) | Real `is_unlocked`/`lock_reason` | Contextual "just became relevant" reveal moment | not built | HIGH | None — real domain truth already computed | W-FUNNEL-7 | new | Flag `ACADEMY_EXPANSION_ENGINE` off |
| Ecosystem Circulation | PARTIAL internal / INTERFACE_ONLY external | `/wallet`, `/frek-profile` | `services/integrations/registry.py` (9 systems) + FrekCore + Agent Factory | Real typed interfaces, real local fallbacks | Nothing to build until external creds exist — do not fake | HIGH (per mission) but nothing to show truthfully yet | HIGH, only when REAL | **Full**: 9/11 systems unconfigured | W-FUNNEL-7, expose only what `GET /integrations` already reports true | existing `GET /integrations` (admin) | N/A — already fails closed |
| Ecosystem Builder | MISSING as surface / PARTIAL as evidence | none | scattered (skills, certs, badges, missions, wallet) | Real evidence, no unified view | Portfolio/competency-graph/collaboration surface | n/a | HIGH, earned not decorative | Depends on which sub-capability — classify individually (see below) | FUTURE_CONTRACT — not a near-term wave | n/a yet | N/A — no code exists to roll back |

## Ecosystem Builder sub-capability classification (mission §41's per-item ask)

| Capability | Classification |
|---|---|
| Portfolio of competencies | `PARTIAL` — `db.skills`/`db.user_skills`/`db.skill_evidence` real, no unified rendering |
| Verified proofs | `IMPLEMENTABLE_NOW` — SHA-256 evidence hashing already real |
| Missions completed | `IMPLEMENTABLE_NOW` — `db.user_missions` real |
| Professional identity | `PARTIAL` — `frek_id`/`FrekProfile` real, not yet framed as a shareable professional identity |
| Network/opportunities | `REQUIRES_OTHER_CVLN_SYSTEM` — no real data source exists inside Academy |
| Economic activity | `REQUIRES_OTHER_CVLN_SYSTEM` — depends on Monetization (missing) |
| Projects | `MISSING` — no model exists |
| Collaborations | `MISSING` — no model exists |
| Credentials | `IMPLEMENTABLE_NOW` — certification attestations real |
| Ecosystem history | `PARTIAL` — `db.event_log` + `db.frek_signals` are a real, if incomplete, history substrate |

## Summary count

```
EXISTS:            14  (Registration, Authentication-core, Identity,
                        Onboarding, Activation-backend, Dashboard-data,
                        Formation Discovery/Selection, Learning Path/
                        Module, Quiz, Mission, Mentor, Progression,
                        Skills, Badges, Certification, Wallet-internal)
PARTIAL:            7  (Discovery, First Value, Retention, Expansion,
                        Ecosystem Circulation-internal, 2FA-frontend,
                        Ecosystem Builder-as-evidence)
MISSING:            2  (Monetization, Ecosystem Builder-as-surface)
BLOCKED_EXTERNAL:   3  (OAuth, Wallet passes, Ecosystem Circulation-external — 9 systems)
FUTURE_CONTRACT:    1  (Ecosystem Builder, full realization)
```
