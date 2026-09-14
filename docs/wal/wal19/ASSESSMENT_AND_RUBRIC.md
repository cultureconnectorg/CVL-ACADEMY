# WAL-19 — Assessment & Rubric

Structure identique à `docs/gmd/gmd21/ASSESSMENT_AND_RUBRIC.md` (N1
40% / N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | System map réel (modèles, fonctions, routes) |
| C2 | Data model literacy (`TransactionType`, `Currency`, absence de hold/reservation) |
| C3 | Frontière CC≠JCC et Academy-ledger≠produit-externe |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente une route de crédit direct, un transfert, ou fusionne CC/JCC ou les deux Wallet |
| 1 | Confond ce ledger avec le vrai produit externe `djsayd/CVLN-Wallet` |
| 2 | System map correct mais sans citer la distinction CC/JCC |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `models.py`/`service.py`/`api/wallet.py` ligne par ligne |

## Règle éliminatoire

Toute capacité inventée (transfert, crédit direct par route, fusion
CC/JCC ou Academy/produit externe) entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
