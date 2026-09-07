# KOR-14 — M08 — Adapter l'expérience à TV/mobile/web

```
MODULE_ID: KOR14-M08
COMPETENCY_ID: C8 — Adapter l'expérience à TV/mobile/web
PREREQUISITES: M07
ASSESSMENT_LEVEL: N2
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

L'audience diaspora accède majoritairement via mobile avec une
connexion limitée — concevoir trois expériences dupliquées pour
TV/mobile/web gaspillerait l'effort sans servir la priorité réelle.

## Objectifs d'apprentissage

- Adapter une expérience à plusieurs surfaces sans dupliquer trois
  fois le travail de conception.
- Prioriser la surface qui sert le mieux l'audience réelle.

## Notions essentielles

Chaque surface a des **contraintes propres** : la TV (distance de
lecture, télécommande), le mobile (connexion limitée, écran réduit), le
web (clavier/souris). La **priorisation** doit identifier quelle
surface sert le mieux l'audience diaspora à faible connectivité — ici,
le mobile — sans pour autant abandonner les autres surfaces.

## Méthode

1. Identifier les contraintes propres à chaque surface.
2. Prioriser la surface qui sert le mieux l'audience réelle
   (mobile, faible connectivité).
3. Adapter, sans dupliquer intégralement, l'expérience pour les autres
   surfaces.

## Exemples

La priorité mobile impose une conception économe en données (images
compressées, chargement progressif) — adaptée ensuite au web (clavier)
et à la TV (grands boutons, navigation télécommande) sans repartir de
zéro. À l'inverse, concevoir d'abord pour le web puis "adapter" au
mobile en réduisant simplement la taille des éléments ignorerait la
contrainte de connectivité réelle, la plus critique pour l'audience
diaspora visée.

## Cas

Épisode C, suite — priorité mobile pour l'audience diaspora (`case/
CASE.md`).

## Erreurs fréquentes

- Concevoir les trois surfaces comme des travaux indépendants dupliqués.
- Prioriser une surface sans lien avec l'audience réelle.
- Ignorer la contrainte de connectivité limitée dans la conception
  mobile.

## Activité

Identification des contraintes propres à chaque surface.

## Exercice

Produire la note d'adaptation multi-surface avec priorité justifiée.

## Livrable

Note multi-surface (`EVIDENCE_TYPE = MULTI_SURFACE_ADAPTATION_NOTE`).

## Critères de réussite

- La priorité mobile est justifiée par les données réelles de
  l'audience.
- Les contraintes de chaque surface sont prises en compte.
- Le travail n'est pas dupliqué intégralement pour chaque surface.

## Preuve

Note multi-surface, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Ma priorisation reflète-t-elle la réalité de connectivité de
l'audience, ou un ordre arbitraire ?*

## Passage au module suivant

Au-delà de l'auditeur, le créateur vit aussi une expérience produit
dans l'application, conçue en M09.
