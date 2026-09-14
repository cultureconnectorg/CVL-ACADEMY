# WAL-24 — Assessment & Rubric

Structure identique à `docs/wal/wal19/ASSESSMENT_AND_RUBRIC.md` (N1 40%
/ N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Littéracie de la structure des payloads Apple/Google (`passes.py`) |
| C2 | Correction du comportement HTTP réel (200 + `unsigned`, jamais 501) contre le commentaire du fichier |
| C3 | Littéracie de l'écart de signature (ce qui manque réellement par plateforme) |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Affirme qu'une carte signée/installable existe déjà, ou qu'une route renvoie une erreur 501 |
| 1 | Répète le commentaire "501" du fichier sans vérifier le comportement réel de la route |
| 2 | Comportement HTTP correct mais sans nommer les dépendances de signature manquantes |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `passes.py`/`api/wallet.py` ligne par ligne, y compris la correction 200/501 |

## Règle éliminatoire

Toute affirmation qu'une carte Apple/Google réellement signée et
installable existe aujourd'hui, ou qu'une route renvoie une erreur 501,
entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
