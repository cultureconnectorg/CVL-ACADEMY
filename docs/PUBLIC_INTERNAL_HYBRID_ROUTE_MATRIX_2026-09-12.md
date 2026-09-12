# CVLN Academy — Public / Internal / Hybrid route matrix

Date: 2026-09-12

## Public entry

- `/` — public landing
- `/login` — public login entry
- `/register` — public registration entry
- `/pricing` — public pricing
- `/legal/:slug` — public legal centre

## Hybrid discovery surfaces

The same URL is used for public discovery and the authenticated member experience. Public mode never loads user-owned resources.

- `/roadmap` — public progression model / member position
- `/formations` — public published catalogue / member learning path
- `/formations/:code` — public published formation preview / member progression + commercial state
- `/missions` — public mission catalogue / member mine + accept + submit
- `/badges` — public badge catalogue / member ownership and remaining thresholds
- `/skills` — public skill registry / member evidence-derived progression
- `/certifications` — public rubrics / member attempts, scores and attestations
- `/wallet` — public wallet explanation / member balances, transactions and passes
- `/frek-profile` — public FREK model / member FREK-ID, identity and signal history

## Internal-only routes

- `/dashboard`
- `/onboarding`
- `/formations/:fc/modules/:mc`
- `/stakeholder/claim/:code`
- `/partner`
- `/institution`
- `/trainer`
- `/jury`
- `/admin`
- `/admin/stakeholders`

## Data boundary

Public surfaces may expose only catalogue, published programme, doctrine, public thresholds, public rubric/registry metadata and product explanation.

Public surfaces must not load or expose user IDs, FREK-ID values, email, balances, transaction history, payment instruments, user mission state, progression, evidence, certification attempts/scores, attestations, signal history, staff/admin data or module learning content.

## Module boundary

Formation module names, durations and deliverable labels may appear in the published formation preview. The actual module route and learning content remain authenticated and onboarding-gated.

## Guard invariants

- Anonymous visitor on a hybrid route receives `PublicDiscoveryLayout`.
- Authenticated but not onboarded user is sent to `/onboarding`.
- Authenticated onboarded user receives the existing member `Layout` behind `LegalGuard`.
- Role routes remain protected by their existing role arrays.
