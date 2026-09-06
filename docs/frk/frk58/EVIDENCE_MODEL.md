# FRK-58 — Evidence Model

## Chaîne de preuve

M1+M2 trace annotée du fallback et de l'émission de signal → M3
tableau des paliers → M4 note écrite sur la frontière `frek_v3` →
correcteur → (jury si 2.0–2.5) → `FRK58.SKILL.*` (réservé, non lié au
runtime).

## Ce qui compte comme preuve

Les traces M1/M2 vérifiables contre `frek_core.py` ; le tableau M3
vérifiable contre `STADE_THRESHOLDS` ; la note M4 écrite noir sur
blanc sur l'absence d'intégration observée avec `frek_v3`/FRK-71→75.

## Ce qui NE compte PAS comme preuve

Un comportement d'erreur inventé, un signal hors liste accepté, ou une
affirmation d'intégration entre `frek_core.py` et n'importe quel autre
système CVLN.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`FRK58.SKILL.*`) est en jeu.

## Réservation Skill ID

`FRK58.SKILL.FALLBACK_PATTERN`, `FRK58.SKILL.SIGNAL_VALIDATION`,
`FRK58.SKILL.PROGRESSION_TIERS`, `FRK58.SKILL.BOUNDARY_DISCIPLINE` —
réservés dans `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.
