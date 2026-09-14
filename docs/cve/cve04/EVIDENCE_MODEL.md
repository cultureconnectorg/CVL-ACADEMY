# CVE-04 — Evidence Model

## Chaîne de preuve

M1 formule CES annotée → M2 note sur la contrainte de poids → M3
carte de dépendances → correcteur → (jury si 2.0–2.5) →
`CVE04.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

La formule M1 correcte (6 composantes, exposant `ρ_c`) ; la note M2
citant `Σ_a w_a,c = 1` ; la carte M3 renvoyant explicitement vers
§3.2/§3.3/CVE-05 sans re-dériver leur contenu.

## Ce qui NE compte PAS comme preuve

Une composante inventée, des poids non normalisés validés, ou une
re-dérivation de N/CHL_integrated/ρ_c au lieu d'un renvoi.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`CVE04.SKILL.*`) est en jeu.

## Réservation Skill ID

`CVE04.SKILL.CES_FORMULA`, `CVE04.SKILL.WEIGHT_CONSTRAINT`,
`CVE04.SKILL.CROSS_REFERENCE_DISCIPLINE` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.
