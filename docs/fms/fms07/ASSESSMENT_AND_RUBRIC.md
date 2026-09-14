# FMS-07 — Assessment & Rubric

Structure identique à `docs/wal/wal19/ASSESSMENT_AND_RUBRIC.md` (N1
40% / N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Session lifecycle réel (statuts, transitions valides, rejet serveur) |
| C2 | Data model literacy (`BookingCreate`, `ServiceCreate`) |
| C3 | Coordination de production (bloc FMS-14) — frontière vs. FMS-05 |
| C4 | Booking & resource planning (bloc FMS-16) — quand rester fusionné, quand séparer |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente un statut de réservation absent de l'énumération réelle, ou un champ absent du modèle réel |
| 1 | Confond la coordination studio-projet (bloc FMS-14) avec la coordination carrière-artiste (FMS-05) |
| 2 | Data model correct mais sans discipline de transition de statut |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `BookingCreate`/`ServiceCreate`/l'énumération de statut ligne par ligne |

## Règle éliminatoire

Toute capacité inventée (statut, champ de modèle, ou fusion FMS-05/
FMS-14 non justifiée par le code réel) entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
