# GMD-31 — Evidence Model

## Chaîne de preuve

M1 payload annoté → M2 chronologie de retry écrite → M3 distinction
écrite explicite (Good Mood FREK vs Academy FREK) → correcteur →
(jury si 2.0–2.5) → `GMD31.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

Le payload M1 vérifiable contre `frek_service.py` (lu en entier) ; la
chronologie M2 citant les 5 backoffs exacts ; la distinction M3
écrite noir sur blanc, jamais implicite.

## Ce qui NE compte PAS comme preuve

Toute affirmation qui confond les deux systèmes FREK, ou toute route
de relance manuelle inventée.

`READY_FOR_FREK_PROOF = FALSE` (voir `../CERTIFICATION_MODEL.md`
§Evidence chain — cette formation enseigne précisément pourquoi cette
mention existe). Seule une certification interne Academy
(`GMD31.SKILL.*`) est en jeu.

## Réservation Skill ID

`GMD31.SKILL.OUTBOX_PAYLOAD`, `GMD31.SKILL.RETRY_SCHEDULE`,
`GMD31.SKILL.BOUNDARY_DISCIPLINE` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.
