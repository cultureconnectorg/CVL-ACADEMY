# KOR-12 — M07 — Détecter des tendances

```
MODULE_ID: KOR12-M07
COMPETENCY_ID: C7 — Détecter des tendances
PREREQUISITES: M06
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Sur un exercice dédié couvrant plusieurs émissions d'Anba Tonèl Host
(`KOR-06`), Fabiola doit repérer une tendance réelle sans la confondre
avec une simple fluctuation ponctuelle.

## Objectifs d'apprentissage

- Détecter une tendance réelle dans un jeu de données simulé.
- Ne pas confondre bruit et signal.

## Notions essentielles

Une **tendance** se distingue d'une **fluctuation ponctuelle** par sa
persistance sur une fenêtre d'observation suffisante. Conclure à une
tendance sur la base d'un seul pic ou d'une seule baisse confond du
bruit avec un signal réel — une **fenêtre d'observation minimale**
s'impose avant de conclure.

## Méthode

1. Observer le jeu de données sur une fenêtre suffisante, pas un seul
   point.
2. Distinguer ce qui persiste (tendance) de ce qui est ponctuel
   (bruit).
3. Justifier explicitement pourquoi le signal retenu dépasse le bruit.

## Exemples

Une hausse progressive des écoutes sur quatre semaines consécutives,
observée sur plusieurs émissions, constitue une tendance réelle. À
l'inverse, un pic d'écoute isolé sur une seule journée (coïncidant
peut-être avec un événement extérieur non documenté) serait une
fluctuation ponctuelle — la conclure comme "tendance" sans vérifier sa
persistance confondrait le bruit avec le signal.

## Cas

Exercice dédié sur un jeu de données simulé multi-émissions d'Anba
Tonèl Host (`case/CASE.md`, `KOR-06`) — non couvert par le fil rouge
central.

## Erreurs fréquentes

- Conclure à une tendance sur un seul point de donnée.
- Ignorer une fenêtre d'observation insuffisante pour appuyer la
  conclusion.
- Confondre un événement ponctuel non documenté avec une tendance de
  fond.

## Activité

Observation du jeu de données multi-émissions sur la fenêtre complète
disponible.

## Exercice

Identifier, sur le jeu fourni, une tendance réelle et une fausse
tendance (bruit), en justifiant la distinction.

## Livrable

Note de tendance (`EVIDENCE_TYPE = TREND_NOTE`).

## Critères de réussite

- La tendance identifiée persiste sur une fenêtre suffisante.
- Le bruit est explicitement distingué du signal.
- La justification de la distinction est documentée.

## Preuve

Note de tendance, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Ma tendance persiste-t-elle réellement, ou ai-je conclu sur un
signal isolé ?*

## Passage au module suivant

Ces tendances informent l'évaluation de la performance des contenus
menée en M08.
