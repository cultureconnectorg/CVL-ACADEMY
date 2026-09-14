# FRK-54 — Assessment & Rubric

## Exercice

Le candidat conçoit un contrat d'intégration webhook versionné pour un
système marché-général, en citant `events.py` comme illustration du
patron pub/sub sous-jacent, puis rédige une stratégie de versionnage
pour l'évolution future du schéma sans casser les consommateurs
existants.

## Compétences évaluées

| ID | Compétence |
|---|---|
| C1 | Distinguer précisément bus d'événements interne et webhook externe. |
| C2 | Concevoir un contrat d'intégration versionné avec compatibilité ascendante. |
| C3 | Utiliser `events.py` comme illustration sans jamais l'implier comme infrastructure FREK. |

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Présente `events.py` comme infrastructure webhook/FREK. |
| 1 | Évite l'affirmation, conception de contrat incomplète. |
| 2 | Contrat d'intégration correct, versionnage absent. |
| 3 | Contrat complet et versionné. |
| 4 | Niveau 3 + usage correct d'`events.py` comme illustration uniquement + stratégie de compatibilité ascendante correcte. |

**Règle éliminatoire :** présenter `events.py` comme une infrastructure
webhook ou FREK, affirmer qu'il notifie déjà des systèmes externes, ou
proposer une évolution de schéma cassant les consommateurs existants
sans compatibilité ascendante.

**Seuil de passage :** ≥2.5/4.
