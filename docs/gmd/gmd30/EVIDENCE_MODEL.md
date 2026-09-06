# GMD-30 — Evidence Model

## Chaîne de preuve

M1 tableau de champs → M2 réconciliation manuelle exécutée → M3 note
de portée → correcteur → (jury si 2.0–2.5) → `GMD30.SKILL.*` (réservé,
non lié au runtime).

## Ce qui compte comme preuve

Le tableau M1 vérifiable contre `server.py:389-410` (le calcul exact
de `revenue_cents`, `fill_rate`, `checked_in`) ; la réconciliation M2
citant les deux caps distincts (2000 vs 5000) ; la note M3 refusant de
présenter `revenue_cents` comme un chiffre de paiement confirmé.

## Ce qui NE compte PAS comme preuve

Un champ de ventilation par mode de paiement inventé, ou une
"correction" du calcul de revenu non fondée sur le code réel.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`GMD30.SKILL.*`) est en jeu.

## Réservation Skill ID

`GMD30.SKILL.REPORT_LITERACY`, `GMD30.SKILL.CROSS_CHECK`,
`GMD30.SKILL.SCOPE_DISCIPLINE` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.
