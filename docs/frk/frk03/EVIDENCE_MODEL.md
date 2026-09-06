# FRK-03 — Evidence Model

## Chaîne de preuve

M1 lecture de header annotée → M2 tableau des effets de bord réels →
M3+M4 notes écrites sur le best-effort et `READY_FOR_FREK_PROOF` →
correcteur → (jury si 2.0–2.5) → `FRK03.SKILL.*` (réservé, non lié au
runtime).

## Ce qui compte comme preuve

La lecture M1 vérifiable contre un header réel `docs/kor/`; le tableau
M2 vérifiable contre `frek_core.py` ; les notes M3/M4 écrites noir sur
blanc, jamais implicites.

## Ce qui NE compte PAS comme preuve

Une ancre externe inventée, ou une affirmation `READY_FOR_FREK_PROOF =
TRUE` non justifiée par un fait réel.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`FRK03.SKILL.*`) est en jeu.

## Réservation Skill ID

`FRK03.SKILL.HEADER_LITERACY`, `FRK03.SKILL.SIDE_EFFECT_OPERATION`,
`FRK03.SKILL.PROOF_DISCIPLINE` — réservés dans `70_EVIDENCE/
EVIDENCE_ARCHITECTURE.md`.
