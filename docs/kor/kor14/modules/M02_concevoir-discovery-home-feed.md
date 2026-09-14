# KOR-14 — M02 — Concevoir discovery, home et feed

```
MODULE_ID: KOR14-M02
COMPETENCY_ID: C2 — Concevoir discovery, home et feed
PREREQUISITES: M01
ASSESSMENT_LEVEL: N2
KORA_DEPENDENCY: aucune ; curation éditoriale renvoyée à KOR-04
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

La cartographie de M01 révèle que *Rasin* est difficile à découvrir —
Djems doit concevoir une expérience de découverte qui met en avant le
contenu sans s'appuyer sur un moteur de recommandation qui n'existe
pas.

## Objectifs d'apprentissage

- Concevoir une expérience de découverte qui met en avant un contenu.
- Ne jamais dépendre d'un moteur de recommandation inexistant.

## Notions essentielles

La **mise en avant manuelle/éditoriale** (curation, renvoi `KOR-04`)
diffère de la mise en avant **algorithmique** (absente ici). Un
**home/feed** bien structuré organise le contenu en sections avec une
hiérarchie visuelle claire — sans jamais simuler un algorithme qui
n'existe pas.

## Méthode

1. Identifier les points de friction de découverte issus de M01.
2. Concevoir des sections de home/feed basées sur la curation
   éditoriale (`KOR-04`), pas sur un algorithme.
3. Justifier la hiérarchie visuelle retenue.

## Exemples

La maquette met en avant *Rasin* dans une section "Sélection de la
semaine" curée éditorialement par Naïma (`KOR-04`), avec une hiérarchie
visuelle claire. À l'inverse, présenter une section "Recommandé pour
vous" personnalisée laisserait croire à un moteur de recommandation
qui n'existe pas — toute section de mise en avant doit être
identifiable comme éditoriale, pas algorithmique.

## Cas

Épisode A, suite — maquette de home/feed mettant en avant *Rasin*
(`case/CASE.md`).

## Erreurs fréquentes

- Concevoir une section qui laisse croire à une personnalisation
  algorithmique inexistante.
- Ignorer les points de friction identifiés en M01.
- Produire une hiérarchie visuelle sans justification.

## Activité

Identification des points de friction de découverte issus de M01.

## Exercice

Produire la maquette (basse fidélité) avec justification des choix.

## Livrable

Maquette (`EVIDENCE_TYPE = DISCOVERY_UX_MOCKUP`).

## Critères de réussite

- La mise en avant est explicitement éditoriale, pas algorithmique.
- La maquette répond aux points de friction identifiés en M01.
- La hiérarchie visuelle est justifiée.

## Preuve

Maquette, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Ma maquette laisse-t-elle croire à un algorithme qui n'existe pas, ou
assume-t-elle clairement une curation éditoriale ?*

## Passage au module suivant

Au-delà de la découverte passive, la recherche active doit aussi être
conçue, traitée en M03.
