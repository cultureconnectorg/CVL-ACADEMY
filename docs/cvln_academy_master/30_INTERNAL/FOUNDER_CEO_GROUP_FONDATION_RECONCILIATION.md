# Founder/CEO, CVLN Group, Fondation Cœurvolan — Reconciliation

```
RULE APPLIED: same corrected method, with the mission's own explicit
constraint carried forward without exception: legal/fiscal/patrimoine
content NEVER gets a universal recipe. Where a candidate requires
jurisdiction-specific legal, tax, corporate, or philanthropic-
regulatory content, the verdict is NEEDS_EXPERT_REVIEW, not
NEW_EXTERNAL, however well the two-dimension method would otherwise
classify it.
```

## Repo truth

`backend/seed_modules.py`/`seed_data.py` contain two relevant legacy
formations:

| Legacy code | Title (badge) | Maps to |
|---|---|---|
| `GRP-01` | Ecosystem Entrepreneurship (badge: Ecosystem Entrepreneur) | CVLN Group |
| `GRP-02` | Cultural Economy & Strategic Partnerships (badge: Cultural Economy Strategist) | CVLN Group |
| `CIP-01` | Standardisation, archivage et gouvernance culturelle (badge: **CIP Referent**) | Likely Fondation Cœurvolan — see below |

**Code-collision warning (same pattern as `HOS-01`, already flagged in
the companion document):** Master 2D's `GRP-01` candidate
("Entrepreneurship Foundations") reuses the legacy `GRP-01` code under
a different title ("Ecosystem Entrepreneurship"). Same resolution as
elsewhere: no runtime rename here, flagged for W6.

**Entity-identity question — CLOSED, `FD-CIP-001` (Founder decision,
final).** `CIP Foundation` and `Fondation Cœurvolan` are **two distinct
objects — never to be merged.** `CIP Foundation` names, in the legacy
corpus, the standards/normalization/cultural-governance function
carried in particular by `CIP-01`; `Fondation Cœurvolan` keeps its own
separate institutional identity. Until `CIP Foundation`'s definitive
legal form is settled, use the working label **`CIP Foundation (legacy
working identity)`** — the absence of a final legal form does not
block pedagogical classification. Applied here:

- `CIP-01` stays exactly what it already is — the anchor formation for
  the standards/normalization/governance function it names — **not**
  reclassified as, merged into, or treated as a predecessor of
  Fondation Cœurvolan.
- `FDC-01→48` (Fondation Cœurvolan, all sub-blocks) build **independently**
  of `CIP-01` — no shared anchor, no cross-reuse implied by this
  decision. Any genuine content overlap between the two (heritage
  standardization touching both) is resolved the normal way, by the
  two-dimension method per row, never by an entity merger.
- `EXTERNAL_INTERNAL_CONFUSION` risk this raised is closed: the two
  remain separately named, separately tracked, in every document of
  this Master Package.

## Founder/CEO (CEO-01→12) — EXECUTIVE_ONLY

`NONE` existing coverage. All 12 are `DISTINCT_PROFESSION`/real —
founder-to-CEO transition, executive team-building, board/investor
communication, delegation, institutionalization/succession are a
well-established executive-development genre (the same territory as
YPO/Vistage-style peer-executive curricula), teachable as **market-
general leadership development without inventing jurisdiction-specific
legal or fiscal content** — none of these 12 titles require a
corporate-law or tax claim to teach honestly. `NEW_EXTERNAL` for all
12, `EXECUTIVE_ONLY` context preserved from the source (a governance
control on *who* can access the content, not a content-design
constraint).

## CVLN Group (GRP-01→72)

**GRP-01→31, 41→58 (general entrepreneurship/scale-up/M&A/strategy,
39 rows):** `NONE` coverage, `DISTINCT_PROFESSION` each — real,
standard, non-jurisdiction-specific startup-to-scale-up business
curriculum (opportunity discovery, GTM, fundraising, valuation,
M&A foundations, IP/brand/data strategy, platform strategy).
`NEW_EXTERNAL` — legitimate market-general content, buildable without
legal/fiscal invention because these topics teach *frameworks and
process*, not jurisdiction-specific rules.

**GRP-32→40 (group financial/legal structuring, 9 rows: consolidation,
treasury, transfer pricing, internal control, corporate compliance,
restructuring, international holding strategy) and GRP-11
(Entrepreneurial Legal Foundations):** these **require** real
jurisdiction-specific corporate/tax/accounting rules to teach honestly
(transfer pricing and group consolidation are meaningless without a
named tax jurisdiction; "corporate compliance" without a named
regulatory regime is empty). Per the mission's own standing rule
(§17/§18, carried through every wave of this engagement):
`NEEDS_EXPERT_REVIEW` for all 10 — never a universal recipe, must be
taught with a named jurisdiction and a real subject-matter expert
before any module is written.

**GRP-59→72 (internal operator, CVLN's own group/holding operations,
14 rows):** `PARTIAL` (legacy `GRP-01`/`GRP-02` give a real, if
generic, "ecosystem entrepreneur" survey; nothing gives CVLN's actual
corporate/holding structure — no subsidiary registry, no intercompany
ledger, no governance-operator tooling exists in any repo audited this
session). `DISTINCT_OPERATOR_ROLE` each. `NEW_INTERNAL`, mostly
`BLOCKED_PRODUCT_DEPENDENCY` — and the same expert-review caution
applies wherever an internal row implies real legal/fiscal authority
(GRP-62 Governance Operator, GRP-64 Finance & Performance Operations,
GRP-69 Risk & Internal Control, GRP-70 Group Audit & Evidence, GRP-72
Executive Decision & Authority): these must never be built as if CVLN
Group's actual legal/governance structure already exists and is
documented here — that would be exactly the `FAKE_PRODUCT_CAPABILITY`
failure mode this Master Package exists to prevent. Flag
`NEEDS_FOUNDER_DECISION` jointly with the CIP/Fondation question above
(both touch real institutional structure, not just curriculum design).

## Fondation Cœurvolan (FDC-01→48, MEM-01→10, TRN-01→07, FDC-X-01→09)

**FDC-01→20 (heritage/memory/documentation, 20 rows) + MEM-01→10 +
TRN-01→07 (17 rows, applied heritage-collection/family-transmission
tracks):** `NONE`/`PARTIAL` (overlaps `CIP-01`'s survey content and the
already-reconciled Kiltikonet `KLT-05`/`KLT-06` heritage-adjacent
competencies — cross-reference, don't duplicate). All `DISTINCT_
PROFESSION`/`DISTINCT_SPECIALIZATION` — cultural heritage management,
oral-history collection, digital preservation, ethical
collection/consent, and family-heritage transmission are real,
recognized disciplines (aligned with France Travail's own K1602
"Conservateur du patrimoine" classification, already cited in
`backend/external_calibration.py`, confirming this is a legitimate,
externally-recognized profession, not an invented one). `NEW_EXTERNAL`
for all 37, contingent on the CIP/Fondation identity question above
(if `CIP-01` is confirmed the same entity, these become `SPECIALIZE_
EXISTING` on it instead — same mechanics, no content rewritten).

**FDC-21→35 (foundation governance/philanthropy, 15 rows: governance,
grantmaking, mécénat, fundraising, financement culturel public, impact
measurement, transparency, ethics/conflicts-of-interest):** philanthropic
and non-profit governance is a real professional field, but
grantmaking rules, public cultural-funding mechanisms, and
accountability/conflict-of-interest standards are jurisdiction- and
regulator-specific (French/Caribbean non-profit law differs sharply
from, e.g., US 501(c)(3) doctrine). Same standing rule:
`NEEDS_EXPERT_REVIEW` for all 15 — teachable only with a named
jurisdiction and a real philanthropic/legal expert, never a universal
recipe.

**FDC-36→48 (internal-restricted, 13 rows, CVLN's own foundation
operations):** `PARTIAL` if the CIP/Fondation identity question
resolves positive (`CIP-01` anchors it), else `NONE`. `DISTINCT_
OPERATOR_ROLE` each. `NEW_INTERNAL`, mostly `BLOCKED_PRODUCT_
DEPENDENCY` — no archive/grant/governance system exists in any repo
audited this session. FDC-47 (Foundation Governance Operator) and
FDC-48 (Foundation Audit & Accountability) additionally inherit the
same expert-review caution as GRP-62/69/70 above — real institutional
authority is never simulated.

**FDC-X-01→09 (cross-ecosystem, 9 rows):** `SUBSTANTIAL`/`PARTIAL` —
these are well-grounded conceptually (heritage feeding FREK provenance,
Kiltikonet's living network, KORA's cultural-memory media, FMS's music
heritage, LabelOS's catalog preservation, Good Mood/DJ Sayd's live
cultural memory, Academy's heritage-to-learning pipeline) since every
"other side" of each bridge is itself already reconciled in this Master
Package. `NEW_CROSS_ECOSYSTEM` for all 9, buildable in doctrine now
(citing each already-reconciled domain by reference), with real content
gated on the FDC-01→20 buildout above.

## Summary

| Domain | Rows | Rejected | `NEW_EXTERNAL`/buildable | `NEEDS_EXPERT_REVIEW` | `NEW_INTERNAL`/blocked | `NEEDS_FOUNDER_DECISION` |
|---|---|---|---|---|---|---|
| Founder/CEO | 12 | 0 | 12 | 0 | 0 | 0 |
| CVLN Group | 72 | 0 | 39 | 10 (GRP-11,32-40) | 14 (GRP-59-72) | 0 — institutional-authority rows stay `NEEDS_EXPERT_REVIEW`/`BLOCKED`, not Founder-pending |
| Fondation Cœurvolan | 74 | 0 | 46 (37 heritage + 9 cross) | 15 (FDC-21-35) | 13 (FDC-36-48) | 0 — `FD-CIP-001` closed |

**Zero rejections across all 158 rows. Zero open Founder decisions** —
`FD-CIP-001` closed the one genuine entity-identity question this
document raised (CIP Foundation ≠ Fondation Cœurvolan, never merged,
per Founder decision). Everything else was resolved without
escalation, consistent with the correction's instruction to decide
obvious curriculum questions directly and only raise genuine ones.

## Status

`STATUS = RECONCILED_NOT_BUILT`. No mutation of `backend/seed_data.py`
or `backend/seed_modules.py`. No legal, fiscal, or governance claim is
made anywhere in this document or asserted as buildable without a
named jurisdiction and real expert review.
