# GMD-28 — Assessment & Rubric

Structure identique à `../gmd21/ASSESSMENT_AND_RUBRIC.md`, adaptée à
4 modules : N1 35% / N2 30% / livrable (M1 diagramme + M3 runbook) 35%.

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Cycle de vie checkout → webhook → order |
| C2 | Littéracie webhook (signature, event type, ticket vs merch) |
| C3 | Réconciliation d'ordre + reconnaissance honnête du gap self-heal/ticket-issuance |
| C4 | Diagnostic de panne (preuve réelle Stripe, jamais de log interne inventé) |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente une route de remboursement, un paramètre de filtre serveur, ou un "log webhook" interne |
| 1 | Ne distingue pas ticket vs merch dans le webhook |
| 2 | Cycle correct mais ignore le gap self-heal/`_issue_tickets_for_session` |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite chaque ligne de code exacte, y compris le gap de réparation partielle |

## Règle éliminatoire

Cette formation manipule de l'argent réel (Stripe) — l'invention de
capacité y est jugée avec la même sévérité que partout ailleurs, sans
tolérance supplémentaire ni pénalité supplémentaire au-delà de la
règle standard.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.

## Note sur le cycle de renouvellement

Cette formation manipule de l'argent réel — une recommandation de
cycle sensible à 12 mois (`ECO-042`), alignée sur GMD-33, est notée
dans `REFERENTIAL.md` comme recommandation, pas comme décision
tranchée ici.
