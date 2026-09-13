# AF-04→15 — Assessment & Rubric

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Affirme qu'`agent_factory.py` implémente une des 12 disciplines. |
| 1 | Évite l'affirmation, conception marché-générale incomplète. |
| 2 | Conception correcte pour une discipline, sans généralisation. |
| 3 | Conception correcte + discipline CVLN-gap explicite et systématique. |
| 4 | Niveau 3 + littératie couvrant plusieurs des 12 disciplines de manière cohérente, et cite honnêtement le contexte de marché externe (ex. `CVLNAgentfactory`) sans jamais le présenter comme opéré par cette Academy. |

**Règle éliminatoire :** affirmer qu'un système CVLN implémente l'une
des 12 disciplines — y compris sous forme d'intention future non
observée dans le dépôt.

**Seuil de passage :** ≥2.5/4.

## Compétences évaluées

| Compétence | Ce qu'elle vérifie | Niveau minimal exigé |
|---|---|---|
| Conception marché-générale | Produit une architecture réaliste pour au moins une discipline | 2 |
| Discipline CVLN-gap | N'affirme jamais qu'`agent_factory.py` implémente une discipline | 2 (éliminatoire sinon) |
| Distinction inter-disciplines | Distingue précisément des disciplines proches (ex. sécurité vs. sûreté, outils vs. orchestration) | 3 |
| Littératie transversale | Couvre plusieurs des 12 disciplines de manière cohérente | 4 |
| Frontière de contexte de marché | Cite honnêtement un système externe réel sans l'attribuer à cette Academy | 4 (éliminatoire si violée) |

## Note de correction

Une conception techniquement excellente pour une seule discipline mais
qui échoue au test CVLN-gap (Cas 2 de `BANQUE_N2.md`) reste plafonnée
à 1 — la discipline anti-inflation prime sur la qualité de conception.
