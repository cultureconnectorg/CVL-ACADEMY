# KOR-12 — M02 — Construire métriques et dashboards

```
MODULE_ID: KOR12-M02
COMPETENCY_ID: C2 — Construire métriques et dashboards
PREREQUISITES: M01
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Le plan d'événements de M01 existe — reste à le traduire en dashboard
lisible pour Naïma, qui n'est pas technicienne des données.

## Objectifs d'apprentissage

- Construire un dashboard lisible à partir d'un jeu de données simulé.
- Choisir des métriques pertinentes pour une audience culturelle
  visée, pas un tableau technique brut.

## Notions essentielles

Les **métriques de base** incluent les plays, le taux de complétion, la
durée moyenne d'écoute. Le choix de **visualisation** doit s'adapter à
une audience non technique comme Naïma. Une **métrique de vanité**
(nombre brut sans contexte, comme "1000 plays" sans référence) informe
peu — chaque métrique doit être interprétable dans son contexte.

## Méthode

1. Sélectionner les métriques dérivées du plan d'événements de M01.
2. Choisir une visualisation adaptée à une audience non technique.
3. Éliminer toute métrique de vanité sans contexte interprétable.

## Exemples

Un taux de complétion par épisode, présenté avec sa tendance sur les
dernières semaines, donne à Naïma une lecture actionnable. À l'inverse,
afficher uniquement "1247 plays" sans référence (total historique ?
cette semaine ? comparé à quoi ?) serait une métrique de vanité qui
impressionne sans informer réellement la décision éditoriale de Naïma.

## Cas

Épisode A, suite — dashboard de complétion par épisode pour *Rasin*
(`case/CASE.md`).

## Erreurs fréquentes

- Présenter une métrique de vanité sans contexte interprétable.
- Choisir une visualisation trop technique pour une audience non
  spécialiste.
- Construire un dashboard déconnecté des événements réellement
  instrumentés en M01.

## Activité

Sélection des métriques dérivées du plan d'événements de M01.

## Exercice

Construire le dashboard (maquette ou tableau) sur données simulées
fournies.

## Livrable

Dashboard (`EVIDENCE_TYPE = DASHBOARD_SPEC`).

## Critères de réussite

- Les métriques choisies sont dérivées du plan d'événements réel.
- La visualisation reste lisible pour une audience non technique.
- Aucune métrique de vanité sans contexte n'apparaît.

## Preuve

Dashboard, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Mon dashboard serait-il lisible et actionnable pour Naïma, ou trop
technique ou trop creux ?*

## Passage au module suivant

Avant toute interprétation de ces métriques, leur qualité doit être
vérifiée — traité en M03.
