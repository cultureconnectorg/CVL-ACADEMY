# CVE-03 — Assessment & Rubric

Structure identique à `../cve02/ASSESSMENT_AND_RUBRIC.md` (N1 40% /
N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Formule `C_i,c` exacte, numérateur/dénominateur, fenêtre 14j |
| C2 | Dépendance en amont au Filtre de Validation (§1.1), jamais re-dérivée dans `C` |
| C3 | Discipline de périmètre — aucun modèle multi-touch nommé n'existe dans le spec figé |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente une fenêtre différente sans la qualifier de changement de paramètre, confond `C` avec `E`, ou invente un modèle multi-touch nommé |
| 1 | Formule approximative, fenêtre ou dénominateur imprécis |
| 2 | Formule correcte mais dépendance au Filtre de Validation ou discipline de périmètre absente |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite §1.1/§1.2 précisément, avec exemple numérique correct |

## Règle éliminatoire

Toute capacité inventée (modèle multi-touch nommé, fenêtre modifiée
silencieusement, confusion `C`/`E`) entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
