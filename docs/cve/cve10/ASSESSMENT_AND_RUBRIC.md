# CVE-10 — Assessment & Rubric

Structure identique à `../cve02/ASSESSMENT_AND_RUBRIC.md` (N1 40% /
N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | `MD_c` comme pool réel — ce que le spec définit (distribution) vs. laisse ouvert (valeur € de MD_c) |
| C2 | Discipline "somme nulle au sein du cycle" (§6 C1) |
| C3 | Discipline de renvoi vers CVE-09 — jamais re-dériver la formule |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente un mécanisme de fixation de MD_c, ou valide une proposition violant C1 |
| 1 | Distinction floue entre "défini" et "laissé ouvert" |
| 2 | Distinction correcte mais discipline de renvoi absente (re-dérivation) |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite §5/§6 C1 précisément, renvoie explicitement vers CVE-09 |

## Règle éliminatoire

Tout mécanisme de fixation de `MD_c` inventé, ou toute validation
d'une proposition violant C1, entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
