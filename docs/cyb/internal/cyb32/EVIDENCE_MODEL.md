# CYB-32 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE` (cohérent avec tout le corpus —
`docs/frk/frk56/REFERENTIAL.md`).

## Chaîne de preuve

- Réservation d'ID : `CYB32.SKILL.IAM_OPERATOR.L1` — réservé, non émis.
- Grounding réel : `backend/auth.py` (hachage bcrypt, JWT, rotation de
  refresh token, hachage des tokens opaques, RBAC) — cité directement,
  jamais extrapolé.
- Mapping capacité : aucune fédération SSO/MFA/coffre de secrets
  n'existe dans ce repo.
