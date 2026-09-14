# BRN-15 — Assessment & Rubric

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Invente une étape de traitement, ou affirme un câblage à `/brain/ask`. |
| 1 | Évite ces erreurs, trace incomplète ou imprécise sur les fichiers réels. |
| 2 | Trace complète et correcte, discipline de touchpoint unique implicite. |
| 3 | Trace complète + discipline de touchpoint unique explicite, frontière `/brain/ask` correctement posée. |
| 4 | Niveau 3 + explique pourquoi le langage de frontière est repris verbatim de `docs/kor/kor12/` (convergence, pas re-dérivation) et situe correctement le partage de mécanisme avec IOS-07. |

**Règle éliminatoire :** inventer une étape, ou affirmer un moteur de
raisonnement/câblage à `/brain/ask`.

**Seuil de passage :** ≥2.5/4.

## Compétences évaluées

| Compétence | Ce qu'elle vérifie | Niveau minimal exigé |
|---|---|---|
| Littératie du touchpoint événementiel | Trace exacte émission → bus → relais, fichiers/lignes réels cités | 2 |
| Discipline anti-inflation | N'affirme jamais un moteur de raisonnement/contexte/mémoire | 2 (éliminatoire sinon) |
| Frontière marché | Cite `/brain/ask` honnêtement comme contexte, jamais comme câblage | 2 (éliminatoire sinon) |
| Convergence documentaire | Explique pourquoi le langage de frontière est repris verbatim plutôt que re-dérivé | 4 |
| Partage de mécanisme (IOS-07) | Situe correctement pourquoi BRN-15 et IOS-07 reposent sur le même bus `events.py` | 3 |

## Note de correction

Un candidat qui trace correctement le chemin mais hésite sur la
formulation de la discipline anti-inflation reste au niveau 2 — la
trace seule ne suffit pas au niveau 3, l'explicitation de la discipline
est requise. Un candidat qui invente ne serait-ce qu'une étape
intermédiaire (même qualifiée de "probable" ou "logique") reçoit 0,
sans exception ni charité rédactionnelle.
