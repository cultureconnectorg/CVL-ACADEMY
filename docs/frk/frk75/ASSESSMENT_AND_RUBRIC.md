# FRK-75 — Assessment & Rubric

## Exercice

Le candidat lit une sortie de test réelle (16/16 tests passants contre
vecteurs d'or), énonce précisément ce qui est prouvé vs. non prouvé,
distingue `reference_verifier/` de `issue_proof()` (FRK-13), puis
analyse un scénario hypothétique d'échec d'implémentation croisée
Rust.

## Compétences évaluées

| ID | Compétence |
|---|---|
| C1 | Citer la structure du package `reference_verifier/` (7 modules). |
| C2 | Distinguer précisément « implémentation testée » et « spécification prouvée agnostique ». |
| C3 | Maintenir la frontière permanente avec FRK-13. |

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Affirme que les tests prouvent l'agnosticisme d'implémentation. |
| 1 | Distingue en théorie, structure du package mal citée. |
| 2 | Structure du package correcte (7 modules), limitation implicite. |
| 3 | Structure correcte + limitation d'implémentation unique explicite. |
| 4 | Niveau 3 + frontière FRK-13 explicite et correcte + analyse correcte du scénario d'échec croisé. |

**Règle éliminatoire :** affirmer que les 16 tests prouvent
l'agnosticisme d'implémentation de la spécification, ou fusionner avec
FRK-13.

**Seuil de passage :** ≥2.5/4.
