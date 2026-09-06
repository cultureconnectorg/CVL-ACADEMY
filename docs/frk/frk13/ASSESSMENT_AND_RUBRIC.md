# FRK-13 — Assessment & Rubric

Structure identique à `docs/frk/frk01/ASSESSMENT_AND_RUBRIC.md` (N1
40% / N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Concept marché du proof engine (custody/signature/horodatage) |
| C2 | Réalité de `issue_proof()` (stub UUID, remote-first) |
| C3 | Communication honnête de l'écart concept/réalité |
| C4 | Frontière avec FRK-75 (vérificateur réel distinct) |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Affirme une garantie cryptographique inexistante, ou confond avec FRK-75 |
| 1 | Dénigre le concept professionnel ou sur-vend l'implémentation |
| 2 | Réalité correcte mais communication imprécise |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `issue_proof()` ligne par ligne |

## Règle éliminatoire

Toute garantie cryptographique affirmée à tort, ou toute confusion
avec FRK-75, entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
