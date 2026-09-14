# FRK-23 — Assessment & Rubric

Grille globale unique (pas de compétences nommées séparées — un seul
critère couvre l'ensemble de l'évaluation, voir
`frk_canonical/rubric_import.py` pour la convention de parsing).

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Confond modélisation conceptuelle et format `.fk`. |
| 1 | Modèle basique, relations incomplètes. |
| 2 | Modèle complet, frontière `.fk` implicite seulement. |
| 3 | Modèle complet, frontière `.fk` explicite et correcte. |
| 4 | Niveau 3 + relations de provenance pertinentes et réutilisables. |

**Règle éliminatoire :** faire dépendre le modèle du format `.fk` non
spécifié, même par une supposition implicite sur son encodage
probable.

**Seuil de passage :** ≥2.5/4.
