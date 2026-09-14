# FRK-07 — Digital Identity Engineering

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Market-general IAM
(Identity & Access Management) skill, teachable independent of a real
FREKCORE repo — industry-standard knowledge (identity providers,
authentication/authorization architecture, session management). Never
a description of what `frek_core.py` implements today.

## Objectives

A candidate who completes FRK-07 can design and reason about a real
IAM (Identity & Access Management) architecture, as industry-standard
knowledge, never as a description of CVLN's current implementation:

- Explain the identity provider (IdP) role in an authentication
  architecture: authenticating a subject, issuing tokens/assertions,
  and the relying-party trust relationship — distinct from a service
  that merely generates identifiers.
- Explain the OAuth2 authorization model (resource owner, client,
  authorization server, resource server) and the OIDC identity layer
  built on top of it (ID token, UserInfo endpoint, discovery document)
  as real, named industry standards — never attributed to CVLN.
- Explain credential lifecycle management: issuance, rotation,
  revocation, and expiry — and why a system without rotation or
  revocation cannot be called a credential-management system, only an
  identifier generator.
- Explain session and token models: opaque vs. self-contained
  (JWT-style) tokens, refresh-token rotation, and the tradeoffs between
  stateful session stores and stateless bearer tokens.
- Keep the FRK-06 boundary explicit at all times: `frek_core.py`'s
  `mint_frek_id()` is a sequential counter that formats and returns an
  identifier string — it authenticates nothing, issues no token,
  manages no session, and has no revocation or rotation path. It is
  not an IdP, not an OAuth2 authorization server, and not a credential
  lifecycle system. This formation teaches the real discipline so a
  candidate can correctly place `mint_frek_id()` within it — as a
  single narrow operation, never as the whole stack.

## Modules

1. **IdP architecture fundamentals** — the identity-provider role,
   the authentication vs. authorization distinction, and the
   relying-party trust model (who trusts whom, and on what basis).
2. **OAuth2/OIDC as real industry standards** — the four OAuth2 roles,
   the authorization-code flow, and what OIDC adds on top (ID token,
   UserInfo, discovery) — taught as named external standards, never as
   a CVLN capability.
3. **Credential lifecycle management** — issuance, rotation,
   revocation, expiry; why an identifier generator without any of
   these is not a credential-management system.
4. **Boundary discipline vs. FRK-06** — `mint_frek_id()` is a narrow
   ID-minting operation (sequential counter, formatted string) inside
   a much larger discipline this formation teaches; never conflate the
   part with the whole.

## Assessment

A design exercise: candidate proposes an IAM architecture for a
hypothetical system using real industry patterns (OAuth2/OIDC roles,
credential lifecycle, session model) — graded against real standards,
never against an invented CVLN capability, and never allowed to
attribute IdP/OAuth2/OIDC behavior to `frek_core.py`.

## Evidence / certification / mission eligibility

`FRK07.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.
