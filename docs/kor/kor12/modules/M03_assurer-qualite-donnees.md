# KOR-12 — M03 — Assurer la qualité des données

```
MODULE_ID: KOR12-M03
COMPETENCY_ID: C3 — Assurer la qualité des données
PREREQUISITES: M02
ASSESSMENT_LEVEL: N2
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Des doublons sont suspectés dans les événements de *Rasin* — Fabiola
doit les détecter et les traiter avant toute interprétation, sous
peine de fausser toute analyse ultérieure.

## Objectifs d'apprentissage

- Détecter un problème de qualité de données.
- Le traiter avant toute interprétation.

## Notions essentielles

Les **problèmes typiques** incluent les doublons, les événements
manquants, l'incohérence entre seuils (un `completion` sans
`play_start` correspondant, par exemple). La **méthode de
fiabilisation** combine dédoublonnage, règles de validation, et
documentation des limites connues. Il ne faut **jamais interpréter des
données non fiabilisées** comme si elles l'étaient.

## Méthode

1. Identifier les doublons ou incohérences dans le jeu de données.
2. Appliquer une méthode de dédoublonnage et de validation.
3. Documenter les limites connues qui subsistent malgré la
   fiabilisation.

## Exemples

Un même événement `play_start` apparaît deux fois avec un horodatage
identique — identifié comme doublon technique et supprimé avant tout
calcul de métrique. À l'inverse, interpréter directement un taux de
complétion anormalement élevé comme un signal positif, sans vérifier
d'abord si des doublons de `completion` ne le gonflent pas
artificiellement, produirait une conclusion fondée sur une donnée non
fiabilisée.

## Cas

Épisode B — doublons suspectés dans les événements de *Rasin* (`case/
CASE.md`).

## Erreurs fréquentes

- Interpréter des données avant de les avoir fiabilisées.
- Corriger un doublon sans documenter la méthode ni la limite
  résiduelle.
- Ignorer une incohérence entre seuils parce qu'elle semble mineure.

## Activité

Identification des doublons ou incohérences dans le jeu de données de
l'épisode B.

## Exercice

Produire un rapport de qualité de données identifiant le problème et
sa correction.

## Livrable

Rapport de qualité (`EVIDENCE_TYPE = DATA_QUALITY_REPORT`).

## Critères de réussite

- Le problème de qualité est identifié précisément.
- La correction appliquée est documentée avec sa méthode.
- Les limites résiduelles connues sont explicitement mentionnées.

## Preuve

Rapport de qualité, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Ai-je fiabilisé les données avant de les interpréter, ou ai-je
raisonné sur des données douteuses ?*

## Passage au module suivant

Les données désormais fiabilisées permettent d'analyser le
comportement d'audience en M04.
