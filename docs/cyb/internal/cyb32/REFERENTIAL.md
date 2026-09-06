# CYB-32 — Identity & Access Management Operator (internal, flagship)

## Repo truth this formation is built on

Grounded directly in `backend/auth.py` (audited this session, header
comment: "FrekID auth — JWT access tokens + rotating refresh tokens +
bcrypt"): real `bcrypt.hashpw`/`bcrypt.checkpw` password hashing
(`hash_password`/`verify_password`), real JWT access tokens
(`make_token`/`decode_token`, `JWT_ALGO = "HS256"`,
`JWT_EXPIRE_MINUTES`), real **rotating** refresh tokens
(`issue_refresh_token`/`rotate_refresh_token`/
`revoke_all_refresh_tokens`), real opaque-token hashing at rest
(`_hash_opaque_token` — "Opaque (non-JWT) tokens are stored hashed —
never plaintext at rest"), real password-reset token lifecycle
(`issue_password_reset_token`/`consume_password_reset_token`), real
email-verification token lifecycle
(`issue_email_verification_token`/`consume_email_verification_token`),
and real role-based access control (`require_role(*roles)`,
`get_current_user`/`get_current_user_optional`).

## Boundary

This is the **one** row of `CYB-31→42` (CVLN's internal security
architecture layer) grounded in real, currently-running code — per
`CYBERSECURE_BLOCKCHAIN_GALA_HOSPITALITY_LABELOS_RECONCILIATION.md`.
The other 11 rows (architecture, secrets management, API security
operations, production security operations, monitoring, vulnerability
management, incident response, audit, backup/recovery security,
release-gate security, red-team) have **no** corresponding CVLN system
to operate — declared `BLOCKED_PRODUCT_DEPENDENCY` in
`docs/cyb/BLOCKED_CANDIDATES.md`, never simulated here.

**Never inflated beyond what `backend/auth.py` actually is**: this is
a single-service JWT/bcrypt auth module with token rotation — not a
SIEM, not an identity-provider platform (no SSO/SAML/OIDC federation),
not a secrets manager. The certification below never implies operating
any of those.

## Prerequisites

None (entry point of the CyberSecure internal-operator track).

## Objectives

- Read and correctly explain the real IAM lifecycle implemented in
  `backend/auth.py`: password hashing, JWT issuance/verification,
  refresh-token rotation and revocation, hashed-at-rest opaque tokens
  (reset/verification), and role-based access control.
- Correctly state the maturity boundary: this is real, running code —
  not a mockup — but it is a single-service auth module, never an
  enterprise IAM platform (no SSO federation, no secrets vault, no
  MFA/2FA implementation observed in this file).
- Never claim CVLN operates a SOC, secrets manager, or dedicated IAM
  platform beyond this module.

## Modules

1. **Password hashing literacy** — `hash_password`/`verify_password`,
   bcrypt salting, why plaintext-at-rest is never acceptable.
2. **JWT access-token literacy** — `make_token`/`decode_token`,
   `JWT_ALGO`, `JWT_EXPIRE_MINUTES`, stateless verification tradeoffs.
3. **Refresh-token rotation literacy** — `issue_refresh_token`/
   `rotate_refresh_token`/`revoke_all_refresh_tokens`, why rotation
   defeats token replay, session-revocation-on-compromise discipline.
4. **Hashed-at-rest opaque tokens** — `_hash_opaque_token`, password-
   reset and email-verification token lifecycles, why these are never
   stored plaintext.
5. **Role-based access control** — `require_role`, `get_current_user`/
   `get_current_user_optional`, least-privilege dependency injection
   pattern in FastAPI.
6. **Maturity-boundary discipline** — this module vs. an enterprise
   IAM platform: what exists, what doesn't (SSO, MFA, secrets vault),
   never claiming the latter.

## Assessment

A code-literacy exercise: candidate is given a redacted excerpt of
`backend/auth.py`'s real functions and must correctly explain the token
lifecycle, hashing discipline, and RBAC pattern — eliminatory failure
for claiming this module is an enterprise IAM platform, a SOC, or a
secrets manager.

## Evidence / certification / mission eligibility

`CYB32.SKILL.*` Skill IDs, reserved. Mission eligibility requires
literacy of this real module — never operational access to production
auth credentials or secrets.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package (référentiel +
N1/N2 + assessment/rubric + evidence model + 3 guides + integration
note), built this pass as this wave's flagship. Never implies
`FULLY_COMPLETE` — no real candidate has been assessed yet, and this
status applies to CYB-32 alone, never to the CyberSecure corpus as a
whole (see `docs/cyb/QUALITY_GATES.md`'s canonical state line).
