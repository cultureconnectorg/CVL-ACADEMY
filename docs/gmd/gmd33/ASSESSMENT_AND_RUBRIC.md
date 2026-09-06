# GMD-33 — Assessment & Rubric

Structure identique à `../gmd21/ASSESSMENT_AND_RUBRIC.md` (N1 40% /
N2 30% / livrable 30%).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Cycle d'auth réel (login/token/cookie/me/logout, expiration 12h) |
| C2 | Audit de frontière public/admin, les deux erreurs JWT distinctes |
| C3 | Reconnaissance d'incident (jamais de réponse inventée) — l'absence de révocation de token est LE fait structurant de cette formation |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente une route de révocation de token, un mécanisme de dérogation de rôle, ou un partage de session Academy↔Good Mood |
| 1 | Ne distingue pas les deux erreurs JWT (expired vs invalid) |
| 2 | Cycle correct mais ne cite pas l'absence réelle de révocation |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `server.py:36-70` ligne par ligne pour chaque affirmation |

## Règle éliminatoire

Toute capacité inventée (révocation, dérogation, partage de session)
entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4.

## Cycle de renouvellement

Cette formation hérite du cycle sensible à 12 mois (`ECO-042`) plutôt
que les 24 mois standard, car elle couvre l'authentification/sécurité
de session — décision déjà actée dans `../CERTIFICATION_MODEL.md`.
