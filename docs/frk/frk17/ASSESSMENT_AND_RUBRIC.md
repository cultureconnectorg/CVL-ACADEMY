# FRK-17 — Assessment & Rubric

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Confond horodatage local et horodatage de confiance. |
| 1 | Connaît RFC 3161 en théorie, ne sait pas vérifier un jeton. |
| 2 | Sait vérifier un jeton simplifié, structure incomplète. |
| 3 | Vérification complète et correcte. |
| 4 | Niveau 3 + distingue explicitement d'`issue_proof()` (FRK-13). |

**Règle éliminatoire :** valider un jeton sans vérification de la
signature de l'autorité, ou présenter `issue_proof()` comme équivalent.

**Seuil de passage :** ≥2.5/4.
