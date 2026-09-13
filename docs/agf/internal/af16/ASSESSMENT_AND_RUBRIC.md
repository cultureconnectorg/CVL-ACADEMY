# AF-16 — Assessment & Rubric

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Invente une logique de routage de persona ou une intégration à `CVLNAgentfactory`. |
| 1 | Évite l'invention, description du shim incomplète. |
| 2 | Description correcte de `chat_reply()`/`mentor_reply()`, frontière implicite. |
| 3 | Description complète + frontière `CVLNAgentfactory` explicite. |
| 4 | Niveau 3 + cite précisément les éléments réels de l'ADL comme contexte de marché seulement, et qualifie explicitement toute proposition future comme hypothétique. |

**Règle éliminatoire :** inventer un registre, un système de mission,
un rollback, ou une intégration à `CVLNAgentfactory` — y compris
présenté comme en cours de développement.

**Seuil de passage :** ≥2.5/4.

## Compétences évaluées

| Compétence | Ce qu'elle vérifie | Niveau minimal exigé |
|---|---|---|
| Littératie du shim réel | Décrit exactement `chat_reply()`/`mentor_reply()` | 2 |
| Discipline anti-invention | N'invente jamais registre/mission/rollback | 2 (éliminatoire sinon) |
| Frontière `CVLNAgentfactory` | Distingue explicitement l'échelle et l'absence d'intégration | 3 |
| Discipline de proposition hypothétique | Qualifie toute idée future comme telle, jamais comme en cours | 4 (éliminatoire si violée) |

## Note de correction

Une description exacte du shim qui omet la comparaison de marché avec
`CVLNAgentfactory` reste plafonnée à 2 — la frontière explicite est
une compétence distincte de la simple exactitude technique.
