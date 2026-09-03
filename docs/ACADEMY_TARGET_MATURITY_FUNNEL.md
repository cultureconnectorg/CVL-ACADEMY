# CVLN Academy — Target Maturity Funnel (W-FUNNEL-0)

```
This restates the Founder's own 14-level model, grounded against what
W-FUNNEL-0 actually found real in the repository (see
ACADEMY_CURRENT_FUNNEL_AUDIT.md). It is a target, not a plan — the wave
plan lives in ACADEMY_FUNNEL_IMPLEMENTATION_PLAN.md.
```

## The loop, not a line

```
DISCOVER → IDENTIFY → ORIENT → ACTIVATE → EXPERIENCE VALUE → LEARN →
PRACTICE → PROVE → PROGRESS → EXCHANGE VALUE → RETURN → EXPAND →
PARTICIPATE → BUILD → (new need / new opportunity) ↺
```

Academy becomes: **LEARNING → ACTION → PROOF → OPPORTUNITY → LEARNING**.
A learner who reaches "Proven Professional" doesn't exit the funnel —
their next need re-enters it at Learn, Practice, or Expand, not at
Discover.

## The 14 levels, target state

| # | Level | User question it answers | Real primitive to build on (found in audit) |
|---|---|---|---|
| 0 | Discovery | "Is this relevant to me?" | Landing (W2-B); formation catalog data (currently gated — see gap matrix) |
| 1 | Identity | "Who am I inside this world?" | `frek_id`, real registration/JWT/refresh |
| 2 | Orientation | "Where am I going?" | Onboarding's 4 real inputs (lang/métier/territoire/objectif) |
| 3 | Activation | "Does Academy understand me enough to guide me?" | `onboarding_complete`'s real convergence (recommended formation + mission + badge + signals) |
| 4 | First Value | "What do I do right now, and why?" | Same activation payload, needs a distinct surfaced moment |
| 5 | Learning | recurring: discover→focus→enter→understand→act→return→continue | Formation → Roadmap → ModuleJourney (the strongest, best-tested part of the product) |
| 6 | Practice | "Can I apply this?" | Quiz, Mission, Mentor context — all real |
| 7 | Proof | "Is this recognized?" | Skills evidence, badges, certification + attestation PDF — all real, `VISUAL_CONFIRMATION_NEVER_CREATES_DOMAIN_TRUTH` already the architecture (backend is authoritative, frontend never invents state) |
| 8 | Progression | "What's next, and how far?" | `stade_progress_pct`, `progression/summary`, `is_unlocked`/`lock_reason` (VISIBILITY != ACCESS already real) |
| 9 | Monetization | "What am I exchanging, and for what?" | `FormationEconomics` data model real; transaction layer `MISSING` — build interface/state contracts only |
| 10 | Retention | "Why come back?" | `next_action` (real, deterministic) — needs `RETURN_TO_POSITION` added |
| 11 | Expansion | "What opens next, and why?" | `own_pole`/`other_poles` + unlock reasons (real) — needs a surfaced reveal moment |
| 12 | Ecosystem Circulation | "How does this connect to the wider CVLN world?" | 9 real interface-only integrations + Wallet (real internal ledger) |
| 13 | Ecosystem Builder | "What have I built, and with whom?" | Scattered real evidence (skills/certs/badges/missions/wallet) — no unified surface yet |

## Public vocabulary (mission §33 — maturity != game level)

Internal lifecycle states (see `ACADEMY_LIFECYCLE_STATE_MODEL.md`) never
appear in the UI as `LEVEL N`/`XP`/`QUEST`. The audit found **zero**
instances of this vocabulary in the current product — `W3-D`'s own
report documents finding and removing exactly one "Level N" leak
already. This is a preserved strength, not a new rule.

Approved public terms (already partially in use, per the French-first
i18n dictionary): *Découvrir, Commencer, Votre parcours, En cours, À
pratiquer, À valider, Acquis, Certifié, Prochaine étape, Opportunité,
Écosystème.*

## Non-negotiables carried forward from every prior wave

- `DOMAIN_STATE != VISUAL_STATE` — already the real architecture
  (backend authoritative for identity/progression/completion/skills/
  badges/certification/access/mission-state/economic-state/proof); no
  wave in this mission may invert that.
- The six FMS profession boundaries stay frozen; `FMS_CANONICAL_
  MIGRATION` stays its own separate, untouched workstream.
- H0.10's system architecture (spring physics, retarget-safety,
  substepping, cadence, prediction, camera-follow, transition topology,
  attention tiers, occlusion channels, environmental continuity,
  spatial audio/haptics, frame-pacing instrumentation) is the reference
  to *extract production primitives from* — never edited in place, never
  re-derived from scratch in `frontend/src`.
