# KOR-14 — M11 — Analyser des analytics produit

```
MODULE_ID: KOR14-M11
COMPETENCY_ID: C11 — Analyser des analytics produit (distinct de KOR-12)
PREREQUISITES: M10
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune ; distinct des données de streaming (KOR-12)
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Au-delà des tests qualitatifs (M10), Djems doit analyser les métriques
d'usage du nouveau parcours — sans refaire l'analyse de données de
streaming déjà couverte par `KOR-12`.

## Objectifs d'apprentissage

- Analyser des métriques produit (usage de fonctionnalités, taux de
  complétion d'un parcours).
- Distinguer l'analytics produit de l'analyse de données de streaming
  (`KOR-12`).

## Notions essentielles

Les **analytics produit** répondent à "l'interface est-elle utilisée
correctement ?" — distincts des **données de streaming** (`KOR-12`, "le
contenu performe-t-il ?"). Les métriques typiques incluent le taux de
complétion d'un parcours, le taux d'abandon à une étape précise de
l'interface.

## Méthode

1. Identifier les métriques d'usage pertinentes pour le nouveau
   parcours (pas de performance de contenu).
2. Analyser le taux d'abandon à chaque étape de l'interface.
3. Vérifier que l'analyse ne glisse pas vers l'analyse de contenu de
   `KOR-12`.

## Exemples

L'analyse révèle un taux d'abandon élevé à l'étape "recherche" du
nouveau parcours — un signal produit (l'interface pose problème à cette
étape), pas un signal sur la qualité du contenu *Rasin* lui-même. À
l'inverse, interpréter ce même taux d'abandon comme "le contenu de
Rasin n'intéresse pas assez" confondrait un problème d'interface (M03,
`KOR-14`) avec une question de performance de contenu qui relève de
`KOR-12`.

## Cas

Analyse simulée du taux d'abandon dans le nouveau parcours de
découverte (`case/CASE.md`).

## Erreurs fréquentes

- Confondre un problème d'interface avec une question de performance
  de contenu (`KOR-12`).
- Analyser un taux d'abandon sans identifier à quelle étape il se
  produit.
- Ignorer une métrique d'usage pourtant disponible et pertinente.

## Activité

Identification des métriques d'usage pertinentes pour le nouveau
parcours.

## Exercice

Produire la note d'analytics produit.

## Livrable

Note d'analytics (`EVIDENCE_TYPE = PRODUCT_ANALYTICS_NOTE`).

## Critères de réussite

- L'analyse porte sur l'usage de l'interface, pas la performance de
  contenu.
- Le taux d'abandon est situé précisément à une étape.
- La distinction avec `KOR-12` est respectée.

## Preuve

Note d'analytics, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Mon analyse porte-t-elle sur l'usage de l'interface, ou ai-je glissé
vers une analyse de contenu qui relève de `KOR-12` ?*

## Passage au module suivant

Un problème d'interface peut aussi surgir brutalement sous forme
d'incident, traité en M12.
