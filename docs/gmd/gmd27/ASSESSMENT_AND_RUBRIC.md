# GMD-27 — Assessment & Rubric

Structure identique à `../gmd21/ASSESSMENT_AND_RUBRIC.md` (N1 40% /
N2 30% / livrable 30%).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | `Product`/`ProductIn` field literacy, distinction avec `Volume` |
| C2 | CRUD walkthrough + différence admin/public sur `active` |
| C3 | Handoff vers GMD-28 — la synchronisation Stripe réelle (`gm_` prefix) comme condition de vente |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente une route "activer le prix," confond systématiquement `Product` et `Volume`, ou invente un filtre `active` sur la route admin |
| 1 | Ne cite pas les vrais préfixes `gm_`/`gmtt_` |
| 2 | CRUD correct mais sans vérifier la synchronisation Stripe |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `_sync_stripe_item` et les préfixes exacts |

## Règle éliminatoire

Toute capacité inventée entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4.
