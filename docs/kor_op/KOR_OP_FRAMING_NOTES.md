# KOR-OP-01→11 — Internal Operator Framing Notes

```
STATUS = EXTEND_EXISTING for all 11 rows below — none gets a separate
formation or a separate module. Each note POINTS TO the already-built
docs/kor/korXX/ formation that already teaches this competency at
CORE_BUILD = COMPLETE (or STATUS = PROPOSED for KOR-11→15) depth, per
KORA_OP_X_RECONCILIATION.md's own verdict. Re-teaching any of this here
would violate NO_DUPLICATE_CURRICULUM.
```

Each note below is intentionally short: the internal-operator reading
of a Master 2D row is "the same competency, framed as an employed role
inside a platform" rather than "a freelance/market professional." The
underlying skill, evidence, and boundary discipline are identical to
the cited formation — only the framing sentence differs.

## KOR-OP-01 — Platform Operator

**Maps to:** `KOR-06` (Streaming Platform Operations), built on the
generic "Anba Tonèl Host" vehicle.
**Framing:** the KOR-06 competencies (availability, DSP/CDN/monitoring
literacy) *are* the Platform Operator role — read as an internal
employee of a platform rather than an external consultant. `KOR-06`'s
own `KORA_PRODUCT_GAP` (§6) already lists DSP/CDN/monitoring as
`CAPABILITY_NOT_IMPLEMENTED` — this framing does not soften that.
**No new content.**

## KOR-OP-02 — Catalog Operator

**Maps to:** `KOR-08` (Metadata & Catalog Operations).
**Framing:** `KOR-08`'s "KORA application rule" (catalog *depth* is
LabelOS's job; KORA's is streaming-application metadata only) already
defines exactly the Catalog Operator's scope of authority — no
broader claim is added by this framing.
**No new content.**

## KOR-OP-03 — Creator Operations

**Maps to:** `KOR-05` (Creator & Content Operations).
**Framing:** the internal-operator reading of `KOR-05` is the person
inside a platform who manages creator relationships and onboarding —
same competencies, employed framing.
**No new content.**

## KOR-OP-04 — Editorial Operator

**Maps to:** `KOR-04` (Editorial Programming & Curation).
**Framing:** `KOR-04`'s programmer/curator role (C1-C9) already *is*
an internal-operator role by construction — "décide ce qui est mis en
avant" presupposes a platform employing that judgment. No separate
external/internal split is needed here; `KOR-04` was already framed
internally.
**No new content.**

## KOR-OP-05 — Playback Operations

**Maps to (split by design):** `KOR-14` (Streaming Product &
Experience — player/queue/playlists) for the experience side, `KOR-06`
(availability/infra) for the infrastructure side.
**Framing:** this is the exact boundary tension already documented in
both formations' own referentials — playback *experience* (queueing,
playlists, UX) is `KOR-14`'s competency; playback *availability*
(uptime, degraded-mode handling) is `KOR-06`'s. The Playback Operations
role is explicitly **both**, never merged into one — the split is the
point, not a gap.
**No new content, on either side.**

## KOR-OP-06 — Media Ingestion & Delivery

**Maps to (split by design):** `KOR-03` (Video & Streaming Production,
ingestion side — C9 "encoder pour la livraison", C10 "publier et
contrôler la qualité") for ingestion, `KOR-06` for delivery
infrastructure.
**Framing:** an internal Media Ingestion & Delivery operator sits at
the handoff between `KOR-03`'s C9-C10 (technical readiness for
delivery) and `KOR-06`'s infra layer — the same boundary KOR-OP-12
(below) formalizes as a distinct release-coordination role, without
duplicating either side's actual technical competency.
**No new content beyond the cross-reference to `kor_op12/`.**

## KOR-OP-07 — Subscription & Entitlement

**Maps to:** `KOR-10` (Content Monetization), subscription models
taught at its M02.
**Framing:** `KOR-10`'s subscription-model competency covers the
business-model literacy; entitlement/access-control *enforcement*
logic is not built anywhere in this repo (`ACADEMY_LOCAL_EVIDENCE =
NOT_FOUND`, consistent with `KOR-10`'s own dependency check) — this
framing note does not claim otherwise.
**No new content.**

## KOR-OP-08 — Monetization Operations

**Maps to:** `KOR-10`/M08 (Wallet/JCC application to the economic
model).
**Framing:** this is the **one confirmed `KORA_CURRENT_CAPABILITY`**
in the entire 15-formation corpus — `KOR10.SKILL.C08` is grounded
directly in real, local code (`wallet/models.py`, `wallet/service.py`).
Monetization Operations *is* this competency; nothing needs building,
only the operator-role framing pointer.
**No new content — already built to full local-evidence depth.**

## KOR-OP-09 — Rights Operations

**Maps to:** `KOR-07` (Media Rights, Licensing & Distribution).
**Framing:** `KOR-07` inherits `NEEDS_EXPERT_REVIEW` from the legacy
corpus (rights/licensing content requires real legal literacy this
Academy cannot manufacture) — the Rights Operations framing inherits
the same caveat, never resolved by re-labeling the role "internal."
**No new content, same review gate.**

## KOR-OP-10 — Trust & Safety Operator

**Maps to:** `KOR-11` (Trust, Safety & Content Governance).
**Framing:** `KOR-11` is **already framed around this exact operator
role** — its case fil rouge protagonist, Widlène, *is* a Trust & Safety
coordinator at "Anba Tonèl Host." No re-framing needed; the formation
already teaches the internal-operator reading directly.
**No new content — already built as the case protagonist's role.**

## KOR-OP-11 — Data Operator

**Maps to:** `KOR-12` (Streaming Data & Cultural Intelligence).
**Framing:** `KOR-12`'s case protagonist, Fabiola, already performs
this role. `KOR-12` also carries the mandatory CVLN Brain boundary
(`academy.certification.passed` is Brain's only real touchpoint —
never inflated into "Brain feeds KORA recommendations today," which is
false in this repo) — the Data Operator framing inherits this boundary
unchanged.
**No new content — already built as the case protagonist's role.**

## Summary

| Row | Maps to | New content |
|---|---|---|
| KOR-OP-01 | KOR-06 | None |
| KOR-OP-02 | KOR-08 | None |
| KOR-OP-03 | KOR-05 | None |
| KOR-OP-04 | KOR-04 | None |
| KOR-OP-05 | KOR-14 + KOR-06 (split) | None |
| KOR-OP-06 | KOR-03 + KOR-06 (split) | None (cross-ref to KOR-OP-12) |
| KOR-OP-07 | KOR-10/M02 | None |
| KOR-OP-08 | KOR-10/M08 | None (already local-evidence complete) |
| KOR-OP-09 | KOR-07 | None (same `NEEDS_EXPERT_REVIEW` gate) |
| KOR-OP-10 | KOR-11 | None (already the case protagonist's role) |
| KOR-OP-11 | KOR-12 | None (already the case protagonist's role) |

**11/11 rows resolved as `EXTEND_EXISTING`, zero new formations, zero
new modules.** See `docs/kor_op/kor_op12/` for the one row (KOR-OP-12)
that could not be resolved this way.
