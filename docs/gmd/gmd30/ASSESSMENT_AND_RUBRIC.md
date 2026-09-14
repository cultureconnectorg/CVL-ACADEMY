# GMD-30 — Assessment & Rubric

Structure identique à `../gmd21/ASSESSMENT_AND_RUBRIC.md` (N1 40% /
N2 30% / livrable 30%).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Littéracie complète du rapport, y compris le calcul théorique de `revenue_cents` |
| C2 | Cross-check contre les données brutes, y compris les deux caps différents (2000 vs 5000) |
| C3 | Discipline de portée — ne jamais présenter `revenue_cents` comme un chiffre de paiement confirmé |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente un champ `payment_method_breakdown`, un troisième cap, ou "corrige" le calcul de revenu par une formule inventée |
| 1 | Confond `revenue_cents` avec le montant réellement encaissé |
| 2 | Cross-check correct mais sans citer les deux caps distincts |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `server.py:389-410` précisément pour chaque affirmation |

## Règle éliminatoire

Toute capacité inventée entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4.
