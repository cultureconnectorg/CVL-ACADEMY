# KOR-11 — M11 — Produire un rapport de transparence

```
MODULE_ID: KOR11-M11
COMPETENCY_ID: C11 — Produire un rapport de transparence
PREREQUISITES: M10
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune ; aucune automatisation KORA réelle n'existe ici — voir REFERENTIAL.md §6
ROLE_BOUNDARIES: interdiction explicite de présenter un processus manuel comme automatisé (`NO_FAKE_PRODUCT_CAPABILITY`)
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Anba Tonèl Host doit rendre compte de son activité de modération —
un rapport honnête doit refléter un processus entièrement manuel, sans
jamais suggérer une automatisation qui n'existe pas.

## Objectifs d'apprentissage

- Produire un rapport de transparence honnête sur l'activité de
  modération.
- Ne jamais sur-vendre une automatisation inexistante.

## Notions essentielles

Les **métriques honnêtes** incluent le volume de signalements, le
délai moyen de traitement, le taux de recours, le taux de réversion de
décision. Il est **interdit explicitement** de présenter un processus
manuel comme "alimenté par IA" ou "automatisé" (`NO_FAKE_PRODUCT_
CAPABILITY`). Un rapport de transparence ne doit jamais contenir de
données personnelles identifiables des personnes signalées.

## Méthode

1. Rassembler les métriques réelles de l'activité couverte (épisodes
   A, B, C).
2. Rédiger le rapport sans qualifier d'automatisé un processus qui ne
   l'est pas.
3. Vérifier l'absence de toute donnée personnelle identifiable.

## Exemples

Le rapport indique "3 signalements traités, délai moyen de 2 jours,
1 recours déposé, 0 réversion" — des métriques honnêtes issues d'un
traitement entièrement manuel, présenté comme tel. À l'inverse, décrire
ce même processus comme "assisté par un système de détection
intelligent" pour paraître plus abouti serait une fausse déclaration
de capacité produit, alors qu'aucun système de ce type n'existe dans ce
repo.

## Cas

Rapport de transparence trimestriel fictif pour Anba Tonèl Host,
couvrant les épisodes A/B/C (`case/CASE.md`).

## Erreurs fréquentes

- Présenter un processus manuel comme automatisé ou assisté par IA.
- Omettre une métrique défavorable (délai long, taux de réversion
  élevé) pour paraître plus performant.
- Inclure une donnée personnelle identifiable d'une personne signalée.

## Activité

Rassemblement des métriques réelles de l'activité couverte.

## Exercice

Rédiger le rapport, avec ses limites explicitement énoncées.

## Livrable

Rapport de transparence (`EVIDENCE_TYPE = TRANSPARENCY_REPORT`).

## Critères de réussite

- Les métriques rapportées sont honnêtes, y compris si défavorables.
- Aucune automatisation inexistante n'est suggérée.
- Aucune donnée personnelle identifiable n'apparaît.

## Preuve

Rapport de transparence, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Mon rapport décrit-il fidèlement un processus manuel, ou a-t-il
laissé entendre une automatisation qui n'existe pas ?*

## Passage au module suivant

Une tension plus large, entre sécurité culturelle et modération
automatisée, est arbitrée en M12.
