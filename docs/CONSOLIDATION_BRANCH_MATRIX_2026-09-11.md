# CVLN Academy — Branch Consolidation Matrix

This file tracks the non-destructive reconciliation into `gstack/consolidation-all-branches-20260911`.

Rules:
- `main` remains untouched until the consolidation branch is fully reviewed and CI-validated.
- No force-push and no branch deletion.
- A branch name is never treated as proof of recency; ancestry, head SHA, diff, tests and PR history decide.
- Superseded/withdrawn branches are preserved but not replayed into the canonical runtime.
- Descendant branches are preferred over replaying every ancestor independently when they already contain the ancestor lineage.
- Every merge into consolidation must be tied to an exact reviewed head SHA.

Initial canonical groups observed:
- final wiring/runtime readiness: integrated via `gstack/final-wiring-2026-09-11`.
- Mission 3 audit: `audit/excel-m3-strict-primary-evidence-2026-09-11` supersedes the withdrawn current-main/v2/relational-truth reports.
- stakeholder/FREK-ID: latest candidate `feat/stakeholder-portals-v1`.
- Institutional Bridge: latest candidate `feat/institutional-bridge-20260911`; older institutional aliases point at an older common SHA.
- Economy/commercial/billing: `feat/billing-invoicing-core-20260911` descends from commercial runtime, which descends from Economy 3D traceability.
- Excel runtime/production lineage: `gstack/excel-runtime-integration-20260911` descends from the large production lineage and requires conflict-aware reconciliation, not a blind merge.
- Playwright quiz→mini-mission sync: narrow test-only candidate `fix/playwright-quiz-mini-mission-sync`.

This matrix is evidence-only and does not by itself mark any unmerged branch as integrated.
