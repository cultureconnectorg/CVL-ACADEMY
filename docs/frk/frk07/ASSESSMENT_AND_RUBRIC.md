# FRK-07 — Assessment & Rubric

Structure identique à `../fms07/ASSESSMENT_AND_RUBRIC.md` (N1 40% /
N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Fondamentaux IAM marché-général (IdP, OAuth2/OIDC, cycle de vie des credentials) |
| C2 | Frontière vs. FRK-06 (`mint_frek_id()` ≠ IdP) |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Affirme que `mint_frek_id()` est un IdP complet ou implémente OAuth2/OIDC |
| 1 | Concepts IAM mal restitués (confond authentification et autorisation) |
| 2 | Concepts corrects mais frontière FRK-06 vague ou incomplète |
| 3 | Concepts corrects, frontière explicite, imprécision mineure tolérée |
| 4 | Architecture IAM complète correctement conçue + frontière FRK-06 précisément articulée |

## Règle éliminatoire

Toute confusion `mint_frek_id()`/IdP, ou toute attribution d'OAuth2/OIDC
à `frek_core.py`, entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
