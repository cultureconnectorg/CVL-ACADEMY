# KOR-12 — M01 — Concevoir un plan d'événements de lecture

```
MODULE_ID: KOR12-M01
COMPETENCY_ID: C1 — Concevoir un plan d'événements de lecture (plays/completions)
PREREQUISITES: Aucun
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune ; `db.progress` (Academy) mesure une progression pédagogique, jamais une consommation média — ne pas confondre
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Fabiola rejoint Naïma (`KOR-04`, Rézo Kilti) comme analyste data pour
comprendre la consommation de *Rasin* — mais aucun plan d'événements de
lecture n'existe encore pour savoir quoi mesurer.

## Objectifs d'apprentissage

- Concevoir un plan d'événements de lecture pertinent pour mesurer la
  consommation d'un contenu streaming.
- Ne jamais confondre ce modèle de données avec `db.progress`
  (progression pédagogique Academy).

## Notions essentielles

Les **événements typiques** de lecture incluent `play_start`, des
seuils de progression (25/50/75%), `completion`, `skip`, `replay`. Un
bon plan d'événements évite deux excès : la **sur-instrumentation** qui
nuit à la vie privée, et la **sous-instrumentation** qui empêche toute
analyse utile. `db.progress` mesure une progression pédagogique
Academy — un modèle de données entièrement différent, jamais à
confondre avec une consommation média KORA.

## Méthode

1. Lister les événements minimaux nécessaires pour mesurer la
   consommation de *Rasin*.
2. Vérifier que le plan n'est ni excessif (vie privée) ni insuffisant
   (analyse impossible).
3. Documenter explicitement la distinction avec `db.progress`.

## Exemples

Un plan couvrant `play_start`, les seuils 25/50/75%, `completion` et
`skip` permet de mesurer la consommation réelle sans excès. À
l'inverse, un plan qui ajouterait un événement par seconde de lecture
ou capturerait la position exacte du curseur en continu constituerait
une sur-instrumentation inutile à la vie privée, sans gain d'analyse
proportionné.

## Cas

Épisode A — concevoir le plan d'événements pour *Rasin* (`case/
CASE.md`).

## Erreurs fréquentes

- Sous-instrumenter au point de ne pouvoir mesurer aucun comportement
  utile.
- Sur-instrumenter au détriment de la vie privée sans gain d'analyse
  proportionné.
- Confondre le plan d'événements de lecture avec `db.progress`
  (progression pédagogique Academy).

## Activité

Recensement des événements minimaux nécessaires pour *Rasin*.

## Exercice

Rédiger le plan d'événements avec ses seuils et sa justification.

## Livrable

Plan d'événements (`EVIDENCE_TYPE = EVENT_PLAN`).

## Critères de réussite

- Le plan couvre les événements essentiels sans excès ni manque.
- La distinction avec `db.progress` est explicite.
- Chaque événement retenu est justifié par un besoin d'analyse réel.

## Preuve

Plan d'événements, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Mon plan d'événements est-il proportionné, ou ai-je sur- ou
sous-instrumenté ?*

## Passage au module suivant

Ce plan d'événements alimente les métriques et dashboards construits
en M02.
