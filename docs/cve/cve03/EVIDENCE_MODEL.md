# CVE-03 — Evidence Model

## Chaîne de preuve

M1 formule annotée → M2 note sur la dépendance au Filtre de
Validation → M3 note honnête de périmètre → correcteur → (jury si
2.0–2.5) → `CVE03.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

La formule M1 correcte (numérateur/dénominateur/fenêtre 14j) ; la
note M2 citant `TS_i(t_e) ≥ τ_fraude` comme dépendance amont réelle ;
la note M3 déclarant honnêtement l'absence de tout modèle multi-touch
nommé dans le spec figé.

## Ce qui NE compte PAS comme preuve

Une fenêtre modifiée sans référence à la gouvernance (C7), une
confusion entre `C` et `E`, ou un modèle multi-touch inventé.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`CVE03.SKILL.*`) est en jeu.

## Réservation Skill ID

`CVE03.SKILL.ATTRIBUTION_FORMULA`, `CVE03.SKILL.VALIDATION_FILTER_DEPENDENCY`,
`CVE03.SKILL.SCOPE_DISCIPLINE` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.
