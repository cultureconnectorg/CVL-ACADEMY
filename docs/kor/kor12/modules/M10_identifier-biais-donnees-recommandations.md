# M10 — Identifier des biais dans données et recommandations

```
SKILL_ID: KOR12.SKILL.C10
NEEDS_EXPERT_REVIEW: TRUE
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
```

## Objectif
Identifier des biais potentiels dans un jeu de données ou un système
de recommandation hypothétique, en particulier ceux qui
sous-représenteraient des contenus en langue créole/minoritaire.

## Contenu
- Sources de biais : échantillon non représentatif, boucle de
  rétroaction (les contenus déjà populaires sont plus recommandés,
  invisibilisant les nouveaux).
- Biais culturel spécifique : un système entraîné sur un corpus
  majoritairement non-créole sous-représenterait *Rasin* et ses
  semblables.

## Cas fil rouge
Épisode D, suite — si un système de recommandation existait un jour,
quels biais faudrait-il vérifier avant de le déployer pour *Rasin* ?

## Exercice
Produire un rapport de biais anticipés (hypothétique, explicitement
marqué comme tel).

## Évaluation
N2 — `E-N2-04`.

## Évidence
Rapport de biais (`EVIDENCE_TYPE = BIAS_ASSESSMENT_REPORT`).
