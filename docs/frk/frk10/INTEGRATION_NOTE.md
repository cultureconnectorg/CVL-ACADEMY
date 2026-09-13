# FRK-10 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** le cadre eIDAS2 (Règlement (UE) 2024/1183), le modèle
PID/EAA/QEAA de l'EUDI Wallet, le modèle de présentation par
consentement, et le mécanisme technique SD-JWT/SD-JWT VC — tous
publics, documentés, vérifiables indépendamment de CVLN.

**Supposé :** une révision d'expert réglementaire/juridique nommé —
non effectuée, `NEEDS_EXPERT_REVIEW` ouvert. Toute implémentation CVLN
de ce cadre (wallet, émission d'attestations, vérification) — jamais
affirmée (`CAPABILITY_NOT_IMPLEMENTED`) : ce corpus enseigne un
standard externe, pas une capacité de cette Academy.

## Dépendances

- `FREK_01_75_RECONCILIATION.md`, `70_EVIDENCE/
  EVIDENCE_ARCHITECTURE.md` (réservation de Skill ID sans délivrance).
- Aucune dépendance vers `backend/services/frek_core.py` ou tout autre
  service CVLN — ce corpus ne décrit aucun système interne.

## Ce qu'une future intégration exigerait

1. Une révision par un expert réglementaire/juridique nommé, levant
   `NEEDS_EXPERT_REVIEW` — préalable absolu à toute suite.
2. Une entrée `FRK10` dans le registre de certification de cette
   Academy, seulement après (1).
3. Une rubric 0–4 par compétence écrite après (1), jamais avant.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`, `NEEDS_EXPERT_REVIEW` non résolu —
littératie approfondie à profondeur technique réelle cette passe
(cadre eIDAS2, modèle PID/EAA/QEAA, mécanisme SD-JWT). Délibérément
non promu `PACKAGE_COMPLETE` : aucune certification ne peut exister
avant révision d'expert, quelle que soit la profondeur du contenu de
littératie.
