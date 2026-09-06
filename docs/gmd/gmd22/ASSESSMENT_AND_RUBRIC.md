# GMD-22 — Assessment & Rubric

Structure identique à `../gmd21/ASSESSMENT_AND_RUBRIC.md` (même
`CERTIFICATION_MODEL.md`, même barème global) :

- N1 (banque formative, `BANQUE_N1.md`) — 40%
- N2 (cas appliqués, `BANQUE_N2.md`) — 30%
- Livrable (M2 runbook exécuté/vérifié) — 30%

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | `Volume`/`VolumeIn` field literacy (required vs. optional, server- vs. client-supplied) |
| C2 | CRUD walkthrough correctness (exact route/method/verification pairing) |
| C3 | Diagnostic reasoning grounded in the real model/route definitions, not assumption |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente un champ, une route, ou un mécanisme absent du code réel (batch reorder, merge, featured flag, publish/save distinction) |
| 1 | Confond majoritairement admin et public routes, ou omet la vérification post-action |
| 2 | CRUD correct mais sans distinguer les caps (200 vs 500) ou sans vérifier via la vue publique |
| 3 | CRUD complet et vérifié, diagnostic correct, une imprécision mineure tolérée |
| 4 | Exécution complète, vérification croisée admin/public systématique, diagnostic qui cite la ligne de code exacte |

## Règle éliminatoire

Toute capacité inventée (route, champ, mécanisme de fusion/lot/
publication qui n'existe pas dans `server.py`) entraîne un **0
automatique** sur la compétence concernée, quelle que soit la qualité
par ailleurs de la copie — règle identique à GMD-21, non
proportionnelle.

## Seuil de passage

Moyenne ≥ 2.5/4 sur les 3 compétences, aucune ne pouvant être à 0 pour
cause d'élimination.
