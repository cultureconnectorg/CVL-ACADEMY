# CMD-01→14 — Assessment & Rubric

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Confond deux des trois systèmes (fms-os/fms, MetaCVLN, discipline générique), ou affirme une capacité CVLN inexistante. |
| 1 | Évite ces erreurs, conception marché-générale incomplète. |
| 2 | Conception correcte pour une famille (SRE/NOC, ICS, ou KPI), sans généralisation. |
| 3 | Conception correcte + discipline des trois systèmes explicite. |
| 4 | Niveau 3 + distinction explicite et correcte avec CMD-15 (`internal/`) et runbook ICS réaliste et complet. |

**Règle éliminatoire :** affirmer qu'un système CVLN implémente un
centre de commandement opérationnel complet côté Academy, ou confondre
`fms-os/fms`'s `/os/command-center` avec `MetaCVLN`'s
`/command-center/*`.

**Seuil de passage :** ≥2.5/4.

## Compétences évaluées

| Compétence | Ce qu'elle vérifie | Niveau minimal exigé |
|---|---|---|
| Conception KPI marché-générale | Tableau de bord réaliste, métriques prédictives, pas de métrique de vanité | 2 |
| Rôles et runbook ICS | Structure de rôles correcte, séquence d'escalade cohérente | 2 |
| Discipline des trois systèmes | Ne fusionne jamais `fms-os/fms`, `MetaCVLN`, et la discipline générique | 2 (éliminatoire sinon) |
| Positionnement vs. CMD-15 | Explique correctement pourquoi CMD-01→14 reste indépendant de CMD-15 | 4 |

## Note de correction

Un candidat qui conçoit un excellent tableau de bord KPI mais échoue au
test des trois systèmes (Cas 2 de `BANQUE_N2.md`) reste plafonné à 1 —
la discipline de non-confusion prime sur la qualité de conception.
