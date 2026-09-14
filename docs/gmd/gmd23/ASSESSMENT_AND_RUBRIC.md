# GMD-23 — Assessment & Rubric

Structure identique à `../gmd21/ASSESSMENT_AND_RUBRIC.md` (N1 40% /
N2 30% / livrable 30%, même `CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | `Event`/`EventIn` field literacy, notamment le state machine `status` |
| C2 | Cycle de vie complet (create → ticket-type → verify public → update → archive) |
| C3 | Protocole de handoff vers GMD-24/GMD-25, ancré sur la vraie porte `status=="on_sale"` de `payments/checkout` |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente une valeur de `status` (ex. "cancelled"), une route, ou un champ absent (ex. `visible_at`) |
| 1 | Confond la responsabilité GMD-23 (l'événement) avec GMD-24 (le ticket type) |
| 2 | Cycle correct mais sans vérifier la porte `on_sale` réelle avant la vente |
| 3 | Complet et vérifié, une imprécision mineure tolérée |
| 4 | Exécution complète, citation exacte de la ligne de code pour chaque porte d'état |

## Règle éliminatoire

Toute capacité inventée (statut, route, remboursement automatique)
entraîne un 0 automatique sur la compétence concernée — non
proportionnel à la qualité de la copie.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
