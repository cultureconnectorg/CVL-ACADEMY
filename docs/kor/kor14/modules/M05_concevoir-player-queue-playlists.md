# KOR-14 — M05 — Concevoir player, file d'attente et playlists

```
MODULE_ID: KOR14-M05
COMPETENCY_ID: C5 — Concevoir player, file d'attente et playlists
PREREQUISITES: M04
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Sur un exercice dédié à l'écoute de *Rasin* et d'autres émissions à la
suite, Djems doit concevoir player, file d'attente et playlists comme
un ensemble cohérent — pas trois écrans qui se contredisent.

## Objectifs d'apprentissage

- Concevoir une expérience de lecture cohérente entre player, file
  d'attente et playlists.
- Garantir la continuité entre les trois composants.

## Notions essentielles

Les **contrôles essentiels** du player, la **gestion de la file
d'attente** et la **création/édition de playlists** doivent former un
ensemble, pas trois écrans disjoints. La **continuité** entre les
composants signifie par exemple ne pas perdre la file d'attente en
cours en éditant une playlist en parallèle.

## Méthode

1. Définir les contrôles essentiels du player.
2. Concevoir la gestion de la file d'attente et son articulation avec
   les playlists.
3. Vérifier qu'aucune action sur un composant ne fait perdre l'état
   d'un autre.

## Exemples

Un auditeur qui édite une playlist pendant l'écoute de *Rasin*
retrouve sa file d'attente intacte au retour au player — continuité
préservée. À l'inverse, si éditer une playlist réinitialisait la file
d'attente en cours, l'auditeur perdrait sa progression d'écoute
enchaînée à cause d'une action qui semblait pourtant sans rapport avec
le player.

## Cas

Exercice dédié sur l'écoute de *Rasin* et d'autres émissions à la
suite (`case/CASE.md`) — non couvert directement par le fil rouge
central.

## Erreurs fréquentes

- Concevoir les trois composants comme des écrans disjoints sans
  continuité.
- Perdre l'état de la file d'attente lors d'une action sur les
  playlists.
- Omettre un contrôle essentiel du player (lecture, pause, avance).

## Activité

Définition des contrôles essentiels du player.

## Exercice

Produire la maquette intégrée player/queue/playlists.

## Livrable

Maquette (`EVIDENCE_TYPE = PLAYER_UX_MOCKUP`).

## Critères de réussite

- Les trois composants sont conçus comme un ensemble cohérent.
- La continuité entre eux est vérifiée explicitement.
- Les contrôles essentiels du player sont tous présents.

## Preuve

Maquette, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Une action sur un composant ferait-elle perdre l'état d'un autre, ou
ai-je vérifié la continuité entre les trois ?*

## Passage au module suivant

Si une recommandation existait un jour, son placement UX devrait être
pensé sans fabriquer l'algorithme lui-même, traité en M06.
