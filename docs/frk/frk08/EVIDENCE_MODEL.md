# FRK-08 — Evidence Model

## Chaîne de preuve

M1 littératie DID (non reproduite) → M2 littératie VC → M3 note de
gap CVLN explicite → correcteur → (jury si 2.0–2.5) →
`FRK08.SKILL.*` (réservé).

## Ce qui compte comme preuve

La restitution correcte du modèle DID (document, méthodes de
vérification, résolution) et du modèle VC (issuer/holder/verifier,
émission vs. présentation) ; la note de gap CVLN précisant exactement
ce qui manque à `mint_frek_id()` pour être un DID.

## Ce qui NE compte PAS comme preuve

Toute affirmation, explicite ou implicite, que `frek_core.py` est
conforme W3C DID ou VC ; une confusion entre les deux standards.

`READY_FOR_FREK_PROOF = FALSE`. Aucune éligibilité mission n'existe
encore pour cette formation.

## Réservation Skill ID

`FRK08.SKILL.DID_LITERACY`, `FRK08.SKILL.VC_LITERACY`,
`FRK08.SKILL.CVLN_GAP_DISCIPLINE` — réservés dans `70_EVIDENCE/
EVIDENCE_ARCHITECTURE.md`.
