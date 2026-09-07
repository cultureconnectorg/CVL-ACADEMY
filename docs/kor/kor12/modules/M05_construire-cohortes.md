# KOR-12 — M05 — Construire des cohortes

```
MODULE_ID: KOR12-M05
COMPETENCY_ID: C5 — Construire des cohortes
PREREQUISITES: M04
ASSESSMENT_LEVEL: N2
KORA_DEPENDENCY: aucune ; segment géographique/diaspora rattaché à KOR-09
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Naïma veut comparer les auditeurs diaspora aux auditeurs locaux — pour
que cette comparaison soit utile, Fabiola doit construire des
cohortes pertinentes, ni trop larges ni trop fines pour l'échantillon
disponible.

## Objectifs d'apprentissage

- Construire des cohortes d'audience pertinentes pour une comparaison
  utile.
- Éviter des cohortes trop fines pour être statistiquement
  significatives.

## Notions essentielles

Les **critères de cohorte** possibles incluent la date d'acquisition,
le canal, le segment géographique/diaspora (déjà travaillé en
`KOR-09`). Une cohorte trop fine sur un petit jeu de données perd toute
signification statistique — mieux vaut deux cohortes larges
comparables que dix cohortes trop petites pour rien démontrer.

## Méthode

1. Choisir un critère de découpage pertinent pour la question posée.
2. Vérifier que chaque cohorte reste assez grande pour être
   significative sur l'échantillon disponible.
3. Documenter le critère de découpage retenu et pourquoi.

## Exemples

Deux cohortes "auditeurs diaspora" et "auditeurs locaux" (rattaché à
`KOR-09`), chacune de taille suffisante pour une comparaison
significative. À l'inverse, découper en six sous-cohortes croisant
diaspora/territoire/appareil sur un échantillon de quelques dizaines
d'auditeurs produirait des groupes trop petits pour permettre la
moindre comparaison fiable — la finesse du découpage doit rester
proportionnée à la taille réelle des données.

## Cas

Épisode C — cohorte "auditeurs diaspora" vs "auditeurs locaux",
rattaché à `KOR-09` (`case/CASE.md`).

## Erreurs fréquentes

- Découper en cohortes trop fines pour l'échantillon disponible.
- Choisir un critère de découpage sans lien avec la question posée.
- Omettre de documenter le critère retenu, rendant la comparaison
  non réexaminable.

## Activité

Choix du critère de découpage et vérification de la taille des
cohortes obtenues.

## Exercice

Construire les deux cohortes et documenter le critère de découpage.

## Livrable

Analyse de cohortes (`EVIDENCE_TYPE = COHORT_ANALYSIS`).

## Critères de réussite

- Le critère de découpage est pertinent pour la question posée.
- Chaque cohorte reste assez grande pour une comparaison significative.
- Le critère retenu est explicitement documenté.

## Preuve

Analyse de cohortes, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Mes cohortes restent-elles assez grandes pour être comparées
utilement, ou les ai-je découpées trop finement ?*

## Passage au module suivant

Ces cohortes permettent d'analyser la rétention comparative en M06.
