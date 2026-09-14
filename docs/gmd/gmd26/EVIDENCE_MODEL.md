# GMD-26 — Evidence Model

## Chaîne de preuve

M1 tableau de champs → M2 réponses tracées aux champs réels (ou
explicitement signalées "non trackable") → M3 cas d'honnêteté des
données → correcteur → (jury si 2.0–2.5) → `GMD26.SKILL.*` (réservé,
non lié au runtime).

## Ce qui compte comme preuve

Le tableau M1 vérifiable contre `ticketing_service.py:24-70` ; chaque
réponse M2 tracée à un champ réel nommé, ou explicitement marquée
non-trackable ; le cas M3 correctement refusé.

## Ce qui NE compte PAS comme preuve

Un chiffre ou un segment inventé que le schéma réel ne supporte pas.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`GMD26.SKILL.*`) est en jeu.

## Réservation Skill ID

`GMD26.SKILL.FAN_RECORD_LITERACY`, `GMD26.SKILL.FAN_QUERY_PRACTICE`,
`GMD26.SKILL.DATA_HONESTY` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.
