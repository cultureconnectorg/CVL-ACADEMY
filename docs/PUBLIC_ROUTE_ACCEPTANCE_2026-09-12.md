# Public route acceptance checklist

## Public / hybrid
- [x] `/roadmap`
- [x] `/formations`
- [x] `/formations/:code`
- [x] `/missions`
- [x] `/badges`
- [x] `/skills`
- [x] `/certifications`
- [x] `/wallet`
- [x] `/frek-profile`

## Internal-only invariants
- [x] `/dashboard`
- [x] `/onboarding`
- [x] `/formations/:fc/modules/:mc`
- [x] `/partner`
- [x] `/institution`
- [x] `/stakeholder/claim/:code`
- [x] `/trainer`
- [x] `/jury`
- [x] `/admin`
- [x] `/admin/stakeholders`

## Public data-boundary invariants
- [x] Public wallet does not load balances or transactions.
- [x] Public FREK view does not load personal identity/signals.
- [x] Public missions do not load `mine` and cannot accept/submit.
- [x] Public certifications show rubrics only, not attempts/scores/attestations.
- [x] Public skills show registry only, not evidence-derived member progression.
- [x] Public formations show published catalogue/detail only.
- [x] Public formation module list never opens protected module content directly.

CI remains the final merge gate.
