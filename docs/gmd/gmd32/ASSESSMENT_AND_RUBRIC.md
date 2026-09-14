# GMD-32 — Assessment & Rubric

Structure identique à `../gmd21/ASSESSMENT_AND_RUBRIC.md` (N1 40% /
N2 30% / livrable 30%).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Littéracie du payload Wallet (`wallet_action`, `ticket{}`, endpoint `/wallet/tickets`) |
| C2 | Littéracie du calendrier de retry (identique à GMD-31, vérifié explicitement) |
| C3 | **Discipline de frontière** — jamais confondre `wallet_service.py` (Good Mood, client sortant) avec `backend/wallet/` (cette Academy, ledger réel) |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Confond les deux systèmes Wallet, ou affirme un billet Wallet réellement livré sans vérifier le statut |
| 1 | Confond le payload Wallet avec celui de FREK (GMD-31) |
| 2 | Payload correct mais présente le contrat comme final malgré le commentaire "draft" du code |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `wallet_service.py` ligne par ligne pour chaque affirmation |

## Règle éliminatoire (C3 spécifiquement)

**C3 est éliminatoire**, même rationale que GMD-31/C3.

## Seuil de passage

Moyenne ≥ 2.5/4, C3 jamais à 0.
