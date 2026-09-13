# FRK-43 — Assessment & Rubric

## Exercice

Le candidat conçoit un mécanisme de livraison persistante avec backoff
progressif et dead-letter, en citant le calendrier réel de Good Mood
(`[30s, 2m, 10m, 1h, 6h]`) comme exemple travaillé, puis trace le
comportement exact de son mécanisme face à une panne longue durée du
destinataire.

## Compétences évaluées

| ID | Compétence |
|---|---|
| C1 | Concevoir une persistance locale avant envoi (survie au crash du processus). |
| C2 | Concevoir un backoff progressif correct et un mécanisme de dead-letter. |
| C3 | Citer l'exemple Good Mood sans jamais le présenter comme infrastructure FREK. |

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Pas de mécanisme de retry/persistance. |
| 1 | Retry à intervalle fixe, pas de backoff. |
| 2 | Backoff progressif correct, pas de dead-letter. |
| 3 | Backoff + dead-letter corrects. |
| 4 | Niveau 3 + citation correcte de l'exemple Good Mood sans le présenter comme infrastructure FREK + trace correcte du comportement face à une panne longue durée. |

**Règle éliminatoire :** présenter l'outbox de Good Mood comme
infrastructure FREK, ou absence totale de mécanisme d'échec persistant.

**Seuil de passage :** ≥2.5/4.
