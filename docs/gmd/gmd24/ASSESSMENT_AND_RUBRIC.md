# GMD-24 — Assessment & Rubric

Structure identique à `../gmd21/ASSESSMENT_AND_RUBRIC.md` (N1 40% /
N2 30% / livrable 30%).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | `TicketType` field literacy, formule `remaining = quota - sold` |
| C2 | Traçage réel purchase → QR → scan-readiness |
| C3 | Carte de handoff (GMD-26 fans, GMD-28 paiement, GMD-31/32 outbox) |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente un verrou de réservation atomique au checkout, une contrainte email générique, ou un log d'audit séparé |
| 1 | Confond le check `remaining` au checkout avec l'incrément `sold` au webhook |
| 2 | Traçage correct mais sans citer l'idempotence de `_issue_tickets_for_session` |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite la ligne de code exacte pour chaque étape, y compris le `$inc` atomique |

## Règle éliminatoire

Toute capacité inventée entraîne un 0 automatique sur la compétence
concernée.

## Seuil de passage

Moyenne ≥ 2.5/4. GMD-24 est la spécialisation la plus référencée en
aval du cluster (4 dépendants) — le seuil n'est pas alourdi pour
autant, la règle reste identique aux autres formations.
