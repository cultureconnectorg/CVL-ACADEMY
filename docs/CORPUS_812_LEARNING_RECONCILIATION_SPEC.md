# CVLN Academy — Corpus 812 → Learning Runtime Reconciliation Spec

Status: DRAFT IMPLEMENTATION SPEC
Branch: `reconcile/corpus-812-learning`
Doctrine: Evidence First · Current != Target · Human Authority

## 1. Objective

Transform the canonical 812-row Academy corpus into a governed learning catalogue without confusing catalogue presence with pedagogical completeness.

The 812 rows are the master corpus, not 812 finished courses. The implementation target is to reconcile every corpus object, classify the actual training objects, and prove which trainings are consumable end-to-end after access is granted.

## 2. Canonical sources

Primary sources:
- `CVLN_Academy_Cartographie_2D_Master.xlsx` — 812 corpus rows.
- `CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx` — economic/commercial mapping for the corpus.
- Domain learning masters (for example `CVLN_Academy_Kiltikonet_Formation_Master_Plan.xlsx`) — detailed pedagogical truth when available.

Repository runtime evidence:
- `backend/seed_data.py`
- `backend/seed_modules.py`
- `backend/catalog_cartography.py`
- `backend/pricing_catalog.py`
- `backend/api/formations.py`
- `backend/api/learning.py`
- `backend/api/quizzes.py`
- `backend/api/progression.py`
- `backend/api/certification.py`
- `backend/api/commercial_access.py`

## 3. Corpus taxonomy

Every row must be explicitly classified. The corpus currently contains training objects plus internal/operator skills, cross-ecosystem competencies, transversal objects, labs and reconciliation gaps.

A row is not promoted to a sellable or learnable training because its title exists in the corpus.

Required classification states:
- `FORMATION`
- `INTERNAL_SKILL_OPERATOR`
- `CROSS_ECOSYSTEM_COMPETENCY`
- `TRANSVERSAL`
- `CASE_LAB`
- `GAP_TO_RECONCILE`

## 4. Learning completeness contract

A training is `COMPLETE` only when all mandatory gates pass.

### Gate A — Canonical identity
- stable code
- canonical title
- domain/pole
- context/dimension
- audience
- status
- provenance to canonical workbook row

### Gate B — Pedagogical design
- objectives
- prerequisites
- outcomes/competencies
- module map
- module order and prerequisites
- duration
- delivery format
- assessment strategy
- expected evidence/deliverables

### Gate C — Learning content
For every required module:
- stable module code
- title
- learning objective
- actual lesson/content payload or explicit linked resource
- activity/practice
- deliverable/evidence
- estimated duration
- assessment mapping

A title-only module is not complete.

### Gate D — Assessment
When applicable:
- N1 knowledge checks
- N2 applied exercises/cases
- N3 professional/certifying assessment
- scoring/rubrics
- pass thresholds
- correction/jury rules

### Gate E — Commercialization/access
- canonical economic mapping
- eligible offer(s)
- public/internal access policy
- purchase/funding entitlement mapping
- post-payment access actually unlocks the intended learning object

### Gate F — Runtime
- seeded/persisted data
- API list/detail
- module retrieval
- progress persistence
- quiz/assessment state
- completion state
- certification/evidence state where applicable
- frontend discovery/detail/learning path

### Gate G — Verification
- schema validation
- unit tests
- integration tests
- entitlement tests
- learning/progression tests
- end-to-end smoke test
- CI result

## 5. Status model

Each training and module must use evidence-backed status values:
- `CANDIDATE`: exists only in canonical source / proposal.
- `MAPPED`: canonical row is mapped to a runtime identifier.
- `DESIGNED`: module/assessment plan exists but learning content is not fully implemented.
- `IMPLEMENTED`: code/data exist.
- `VERIFIED`: implementation was tested against the contract.
- `PUBLISHED`: verified object intentionally exposed to its permitted audience.
- `BLOCKED`: cannot progress because a named dependency/evidence item is missing.
- `DEPRECATED`: retained only for lineage/migration.

No automatic promotion from `CANDIDATE` to `PUBLISHED`.

## 6. Legacy reconciliation rule

Existing 30-formation runtime content is an asset, not disposable legacy.

Examples:
- Kiltikonet KLT-01..KLT-05 already exist in runtime and have detailed module definitions.
- Blockchain `BCH-01` already has a detailed 8-module learning path.
- The new canonical corpus separately defines `BCI-01..BCI-30`.

Reconciliation must preserve existing useful content and establish one of:
1. exact canonical successor mapping;
2. aggregate-path mapping;
3. split/redistribution of legacy modules into canonical courses;
4. deprecated-with-lineage when genuinely superseded.

No silent deletion and no blind overwrite.

## 7. Reconciliation matrix

For every canonical training row create one machine-readable record with at least:

```text
canonical_code
canonical_title
source_workbook
source_sheet
source_row
classification
context
economic_mapping_status
legacy_runtime_code
mapping_relation
module_plan_expected
module_count_expected
module_count_implemented
content_complete
assessment_complete
entitlement_complete
api_complete
frontend_complete
runtime_verified
tests_complete
ci_status
release_status
blocking_gaps[]
evidence_refs[]
```

## 8. Runtime API requirements

Catalogue endpoints must support bounded filtering/pagination instead of assuming a 30-row dataset.

Minimum filter contract:
- domain/pole
- context
- type/classification
- release status
- public/internal visibility
- text query
- pagination (`limit`, `offset` or cursor)

Use typed request/response models and keep entitlement enforcement as explicit dependencies. Test dependency overrides independently.

## 9. Kiltikonet reconciliation

Kiltikonet must be reconciled against its domain master, not only the old seed.

The domain plan defines a full pedagogical stack including:
- métier/formation reference
- Master Learning Map
- Master Module Map
- doctrine/boundaries
- case thread
- competency traceability
- module blueprints
- complete modules
- N1/N2/N3 assessment layers
- rubrics/guides
- skill/evidence IDs
- expert video package
- Academy runtime integration
- FREK/progression/certification linkage

Existing KLT modules are retained as evidence and mapped against this target.

## 10. Blockchain reconciliation

The legacy `BCH-01 — Blockchain culturelle et tokenisation` path is not equivalent to the canonical `BCI-01..BCI-30` catalogue.

Required migration step:
- map each BCH-01 module to zero/one/many BCI canonical objects;
- retain the existing aggregate path when useful;
- do not claim BCI courses are complete until their module/content/assessment/runtime gates pass.

## 11. Acceptance criteria

The reconciliation milestone is complete only when:

1. 812/812 canonical rows have deterministic classification and provenance.
2. 100% of rows classified as `FORMATION` have a reconciliation record.
3. Every published formation has >=1 real module and no placeholder-only learning path.
4. Every published module has actual content/activity/evidence semantics, not only a title.
5. Economic offer mapping and post-payment entitlement agree with the formation exposed to the learner.
6. API and frontend consume canonical/runtime data without a second contradictory hard-coded catalogue.
7. Legacy course mappings are explicit and reversible.
8. Tests prove catalogue discovery → entitlement → learning → progression → completion for representative public and internal paths.
9. CI is green for the changed scope.
10. A generated coverage report can answer, without interpretation: `X/Y formations complete`, `X/Y modules complete`, and the blockers for every incomplete item.

## 12. Non-goals

This work must not:
- invent generic learning content merely to raise coverage numbers;
- expose internal/restricted CVLN knowledge publicly;
- infer certification or public-funding eligibility without evidence;
- overwrite richer existing modules because the newer workbook is less detailed;
- declare all 812 corpus rows to be standalone courses.

## 13. Delivery phases

### Phase 1 — Truth registry
Generate corpus → runtime reconciliation records and coverage metrics.

### Phase 2 — Legacy mapping
Map existing 30 runtime courses/modules to canonical successors, starting with Kiltikonet and Blockchain.

### Phase 3 — Learning expansion
Build missing domain-specific module plans/content using domain masters and explicit evidence.

### Phase 4 — Runtime scale
Upgrade catalogue filtering/pagination/models and ensure Mongo/API/frontend can safely carry the expanded catalogue.

### Phase 5 — Entitlement and assessment proof
Verify payment/access, progression, assessments, certification/evidence and E2E behavior.

### Phase 6 — Publish gate
Only `VERIFIED` trainings may become `PUBLISHED` for their allowed audience.
