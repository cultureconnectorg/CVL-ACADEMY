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

## Ce que cette chaîne ne prouve pas

Elle ne prouve pas que cette Academy dispose d'une plateforme IAM
d'entreprise, d'un SOC, ou d'un coffre de secrets — le module réel se
limite strictement au cycle de vie décrit (hachage, JWT, rotation,
RBAC) pour un seul service.

## Pourquoi aucune preuve mission-éligible aujourd'hui

L'éligibilité mission exigerait un accès opérationnel réel à des
identifiants ou des secrets de production — chose que cette
certification ne couvre ni n'autorise. La certification porte sur la
littératie du module réel, jamais sur un accès opérationnel.

## Conditions d'une future preuve

1. Un vrai passage vérifié par un correcteur humain sur les banques
   N1/N2.
2. Si un jour ce module évoluait vers une vraie fédération SSO/MFA ou
   un coffre de secrets, une nouvelle formation ou une révision
   explicite documenterait ce nouvel état — jamais une extension
   silencieuse du périmètre actuel de CYB-32.
