# FRK-20 — Assessment & Rubric

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Confond mise en cache et vérification offline-first. |
| 1 | Connaît le concept, conception dépendante du réseau. |
| 2 | Conception locale correcte, synchronisation mal gérée. |
| 3 | Flux complet et correct (local puis synchronisation différée). |
| 4 | Niveau 3 + discipline CVLN-gap explicite (`is_remote_enabled()`). |

**Règle éliminatoire :** faire dépendre la garantie de preuve d'un
appel réseau synchrone, ou affirmer qu'un système CVLN vérifie
aujourd'hui hors-ligne.

**Seuil de passage :** ≥2.5/4.
