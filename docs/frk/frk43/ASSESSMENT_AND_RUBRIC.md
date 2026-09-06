# FRK-43 — Assessment & Rubric

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Pas de mécanisme de retry/persistance. |
| 1 | Retry à intervalle fixe, pas de backoff. |
| 2 | Backoff progressif correct, pas de dead-letter. |
| 3 | Backoff + dead-letter corrects. |
| 4 | Niveau 3 + citation correcte de l'exemple Good Mood sans le
    présenter comme infrastructure FREK. |

**Règle éliminatoire :** présenter l'outbox de Good Mood comme
infrastructure FREK, ou absence totale de mécanisme d'échec persistant.

**Seuil de passage :** ≥2.5/4.
