# GMD-25 — Evidence Model

## Chaîne de preuve

M1 tableau de décision (résultat → action) → M2 explication du
compteur → M3 note d'escalade explicite → correcteur → (jury si
2.0–2.5) → `GMD25.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

Le tableau M1 vérifiable contre `server.py:715-753` (les 3 vrais
résultats, les champs écrits) ; l'explication M2 du compteur citant
exactement ce que `scanned`/`issued`/`capacity` comptent ; la note M3
citant explicitement `gmd34/GAP.md` comme raison de ne jamais inventer
de procédure de secours.

## Ce qui NE compte PAS comme preuve

Une procédure de secours inventée, une commande de re-scan forcé, ou
toute affirmation non vérifiable contre le code réel.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`GMD25.SKILL.*`) est en jeu — jamais une autorisation
opérationnelle réelle d'accès porte.

## Réservation Skill ID

`GMD25.SKILL.SCAN_OUTCOMES`, `GMD25.SKILL.COUNTER_LITERACY`,
`GMD25.SKILL.ESCALATION_BOUNDARY` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.
