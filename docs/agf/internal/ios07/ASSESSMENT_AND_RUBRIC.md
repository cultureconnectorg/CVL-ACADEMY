# IOS-07 — Assessment & Rubric

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Décrit `events.py` comme distribué, ou affirme un câblage à `Cvln-ios-v.1`. |
| 1 | Évite ces erreurs, description incomplète. |
| 2 | Description correcte, référence à FRK-54 implicite. |
| 3 | Description complète + référence à FRK-54 explicite et correcte. |
| 4 | Niveau 3 + cite correctement le statut non-`DEPLOYED_RUNTIME` de `Cvln-ios-v.1` et explique pourquoi IOS-07 existe séparément de BRN-15/FRK-54. |

**Règle éliminatoire :** décrire `events.py` comme distribué, ou
affirmer un câblage à `Cvln-ios-v.1`.

**Seuil de passage :** ≥2.5/4.

## Compétences évaluées

| Compétence | Ce qu'elle vérifie | Niveau minimal exigé |
|---|---|---|
| Littératie du mécanisme réel | Décrit `events.py` avec exactitude (en-process, non durable) | 2 |
| Discipline anti-inflation | Ne décrit jamais `events.py` comme distribué/durable | 2 (éliminatoire sinon) |
| Frontière `Cvln-ios-v.1` | N'affirme jamais un câblage au corpus externe | 2 (éliminatoire sinon) |
| Référencement croisé FRK-54 | Renvoie explicitement à FRK-54 plutôt que de re-décrire | 3 |
| Consistance inter-formations | Maintient la même description technique qu'attendue dans FRK-54/BRN-15 | 3 |
| Positionnement du domaine | Explique pourquoi IOS-07 existe séparément de BRN-15/FRK-54 | 4 |

## Note de correction

Une description techniquement correcte mais qui ne renvoie jamais à
FRK-54 plafonne à 2 — le renvoi explicite est une compétence évaluée
séparément de la simple exactitude technique. Toute incohérence
factuelle avec ce qu'un candidat aurait dû affirmer pour FRK-54 sur le
même mécanisme est un signal à vérifier avec le correcteur FRK-54 si le
dossier est disponible.
