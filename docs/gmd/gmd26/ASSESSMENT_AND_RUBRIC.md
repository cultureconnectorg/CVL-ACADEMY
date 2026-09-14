# GMD-26 — Assessment & Rubric

Structure identique à `../gmd21/ASSESSMENT_AND_RUBRIC.md` (N1 40% /
N2 30% / livrable 30%).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Littéracie du champ fan réel (`purchases`, `segments`, `cities`, `external_id`) |
| C2 | Requêtage correct — savoir ce que les champs peuvent et ne peuvent pas répondre |
| C3 | Discipline d'honnêteté des données — "non trackable" plutôt qu'un chiffre inventé |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente un champ (adresse, taux d'ouverture email, dépense moyenne) ou une règle de désambiguïsation absente du code |
| 1 | Nie l'existence des champs dérivés réels (`segments`, `total_events`) |
| 2 | Réponses correctes mais sans citer la ligne de code exacte |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `upsert_fan` (`ticketing_service.py:24-70`) précisément pour chaque réponse |

## Règle éliminatoire

Toute donnée inventée pour répondre à une question stakeholder
entraîne un 0 automatique — cette formation évalue spécifiquement la
discipline anti-`FAKE_PROOF` appliquée aux données.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
