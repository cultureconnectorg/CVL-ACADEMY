# M01 — Concevoir un plan d'événements de lecture

```
SKILL_ID: KOR12.SKILL.C01
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
```

## Objectif
Concevoir un plan d'événements de lecture (play, seuils de progression,
complétion) pertinent pour mesurer la consommation d'un contenu
streaming.

## Contenu
- Événements typiques : `play_start`, seuils 25/50/75%, `completion`,
  `skip`, `replay`.
- Ce qu'un plan d'événements doit éviter : sur-instrumentation qui nuit
  à la vie privée, sous-instrumentation qui empêche toute analyse.
- Rappel : `db.progress` (Academy) mesure une progression pédagogique,
  jamais une consommation média — ne pas confondre les deux modèles de
  données.

## Cas fil rouge
Épisode A — concevoir le plan d'événements pour *Rasin*.

## Exercice
Rédiger le plan d'événements avec ses seuils et sa justification.

## Évaluation
N1 — `Q-N1-01`.

## Évidence
Plan d'événements (`EVIDENCE_TYPE = EVENT_PLAN`).
