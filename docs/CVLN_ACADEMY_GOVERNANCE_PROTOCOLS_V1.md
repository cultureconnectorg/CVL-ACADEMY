# CVLN Academy Governance Protocols v1

Status: IMPLEMENTED SPECIFICATION — runtime verification is tracked independently by Production Gates.
Source authority: CVLN Academy Protocols / Rules / Doctrines Integration Master V1 and Founder Decisions.
Doctrine: Current != Target · Evidence First · Human Authority · no implicit authority escalation.

This document formalises GOV-01..GOV-18. It does not claim deployment, legal effect,
external professional approval, certification, insurance coverage, or production
verification. Those claims require explicit evidence in their canonical runtime gates.

## GOV-01 — CVL Academy Authority Doctrine

Authority belongs to an identified actor acting at an explicit authority level and under
an effective policy version. Authentication or an application role is not authority by
itself. A critical decision must bind actor, action, domain, context, policy version,
policy content hash, rationale and evidence. No policy match fails closed. Academy owns
Academy operational authority; group/systemic escalation remains outside Academy and
must be routed to the appropriate CVLN authority rather than fabricated locally.

Runtime: `services/authority_policy.py`, `services/policy_registry.py`,
`services/critical_proof.py`.

## GOV-02 — Authority Policy Engine Protocol

1. Resolve authenticated actor/service identity.
2. Resolve explicit requested action and context.
3. Load one effective immutable policy version from XCP-008.
4. Evaluate ordered policy rules.
5. Produce ALLOW, DENY or ESCALATE; no match = DENY.
6. Persist the complete authority decision and decision hash.
7. Sensitive callers must consume the decision; they must not replace it with a role
   shortcut.
8. Critical approvals can be anchored through the canonical FREK proof bridge.

Runtime: `services/authority_policy.py`.

## GOV-03 — Doctrine Versioning Protocol

Doctrine, policy, protocol, rule and standard versions are immutable records. A new
version may supersede an older version explicitly; existing evidence keeps its original
version/hash. Effective dates are timezone-aware. Consumers resolve the exact effective
version and fail on hash/state mismatch. Historical versions are never silently edited.

Runtime: `services/policy_registry.py`.

## GOV-04 — Professional Case Doctrine

A professional case is the canonical boundary for external professional work. Every
expert assignment, document, decision, review, credential, cost and external action
must be reachable from an explicit case. Domain and sensitivity are case properties.
Cross-case browsing is forbidden unless a separate explicit assignment exists.

Runtime: `services/professional_governance.py`, `services/professional_workspace.py`.

## GOV-05 — Expert Isolation Doctrine

External experts receive least-privilege, case-scoped access. Expert identity is not a
normal Academy user role. Active assignment + active credential + unexpired key + exact
scope are jointly required. Assignment narrowing, key rotation, expiration and
revocation invalidate prior access. Workspaces expose only records referenced by the
assigned case.

Runtime: `services/expert_access.py`, `services/professional_workspace.py`, domain
expert workspaces.

## GOV-06 — Expert Modification Protocol

An external modification is accepted only when the expert is assigned to the case,
holds the exact write scope, the target belongs to that case/domain, required evidence
and rationale are present, and any applicable authority policy returns ALLOW. Protected
identity/lifecycle fields are not directly editable. Changes are append-only where a
correction/recommendation is safer than mutating canonical source truth.

Runtime: `services/legal_expert_ops.py`, `services/external_expert_actions.py`,
`services/external_expert_validations.py`.

## GOV-07 — Professional API Credential Policy

Professional API credentials are bearer secrets issued only against an ACTIVE expert
assignment. Raw credentials are returned once and never stored; only a SHA-256 hash is
persisted. Every key has an expiry and immutable original scope. Runtime authorization
also compares the current assignment scope, so narrowing cannot be bypassed with an old
key. Rotation revokes the old key. Revocation and expiration fail closed. Usage is
tracked and audited.

Runtime: `services/professional_governance.py`, `services/expert_access.py`.

## GOV-08 — Evidence Doctrine

Evidence is referenced, content-addressed where possible and provenance-bearing.
Evidence presence is not equivalent to external validation. Evidence can support a
claim but does not manufacture legal, regulatory, security, tax, insurance or
certification authority. Critical evidence is composed by reference instead of copied
into parallel domain stores.

Runtime: `services/evidence_graph.py`, `services/proof_bridge.py`.

## GOV-09 — Evidence Graph Protocol

1. Register a source node with canonical source type/id, SHA-256, provenance,
   classification where applicable, and effective access policy.
2. Link nodes only through explicit supported relations.
3. Compose consumer packs as `REFERENCE_ONLY` node references.
4. Reject missing/dangling nodes.
5. Preserve source hashes and policy versions inside every pack.
6. Run integrity gate before release.

Runtime: `services/evidence_graph.py`.

## GOV-10 — Decision Provenance Protocol

Every sensitive decision records actor, role/authority context, action, policy version,
policy hash, context hash, rationale/reason, evidence, timestamp and result. Changes to
sensitive state must additionally record before/after when applicable. Audit hashes
cover the full provenance envelope.

Runtime: `services/authority_policy.py`, `services/professional_governance.py`.

## GOV-11 — Audit Event Standard

Canonical audit fields: id, event_type, actor_id, resource_type, resource_id, payload,
before, after, reason, result, payload_hash, created_at. Audit records are append-only.
Domains extend this standard; they do not create competing audit semantics.

Runtime: `services/professional_governance.py::audit_event`.

## GOV-12 — Incident Core Doctrine

One incident id is the source of truth. Privacy, Security, Legal and Risk records are
projections of that incident and keep the canonical incident id. Severity never silently
becomes a risk score. Cross-domain projections are idempotent and evidence-bearing.
Resolution/closure requires evidence.

Runtime: `services/incident_core.py`.

## GOV-13 — Escalation Protocol

Escalation is an explicit result, not an invisible privilege jump. ALLOW executes only
within the local authorised scope. DENY blocks. ESCALATE creates/updates a governed case
or review for the required higher authority; the lower layer must not self-approve the
escalated action. R5/systemic decisions requiring group authority remain outside Academy
unless a verified CVLN authority contract is available.

Runtime: `services/authority_policy.py`, professional case/review workflow.

## GOV-14 — Human Authority Doctrine

AI may prepare, classify, route, analyse and execute pre-authorised technical work, but
AI preparation is not approval. `AI_PREPARED`, `HUMAN_REVIEW`, `CVL_APPROVED` and
`EXPERT_VALIDATED` are distinct states. Human/external authority cannot be inferred
from model output, service success or a UI role.

Runtime: `services/governance_review.py`.

## GOV-15 — Cost Avoidance Protocol

External expert cost and time are recorded per case/intervention with evidence. A cost
avoided metric may be calculated only when an explicit evidence-backed baseline hours
and baseline rate are supplied. Academy never invents market rates. Multi-currency
amounts are not summed into a false common total without an FX policy.

Runtime: `services/expert_cost_ledger.py`.

## GOV-16 — Licensing Doctrine

A license grants named Academy capabilities to a tenant. It does not grant access to
CVLN internal doctrine, implementation details, other tenants, group governance or
Founder authority. Entitlements fail closed outside their effective version/scope.

Runtime: `services/license_entitlement.py`.

## GOV-17 — Tenant Entitlement Protocol

Tenant capabilities are explicit, versioned and bound to an effective policy/entitlement
record. Every request resolves tenant + capability + status + effective version. Missing
or expired entitlement denies access. API responses expose capability outcomes, not CVLN
internal policy bodies.

Runtime: `services/license_entitlement.py`.

## GOV-18 — No-Duplicate Architecture Rule

Before a new cross-cutting component is implemented, its theme must resolve against the
locked Deduplication Map as REUSE, EXTEND, CONNECT/COMPOSE or BUILD ONCE. A conflicting
build decision fails. Canonical owners include Academy Auth/RBAC, Event Bus,
NotificationService, Integration Registry, Academy→FREK bridge, Commerce, Payments,
Wallet, Certification, Physical Delivery, Learning Runtime, existing Agent/AI
infrastructure, Governance AuditEvent, Trust/Signature, Document Registry, Incident
Core and Evidence Graph.

Runtime: `services/architecture_reuse.py`; enforced at startup and by PG-13.

## Runtime completion rule

No section in this document is sufficient evidence of completion. A capability reaches
COMPLETE only when its implementation is wired, tests pass on the exact commit, required
manual verification is recorded and the deployment/recovery path is reproducible. P0
Production Gates remain authoritative for V1 closure.
