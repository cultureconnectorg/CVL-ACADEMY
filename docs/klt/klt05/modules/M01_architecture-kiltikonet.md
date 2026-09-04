# KLT-05 — M01 — Kiltikonet — mission, valeurs, architecture

```
MODULE_ID: KLT05-M01
COMPETENCY_ID: C1 — Comprendre l'architecture Kiltikonet (mission, valeurs, surfaces)
PREREQUISITES: Aucun
ASSESSMENT_LEVEL: N1
KILTIKONET_DEPENDENCY: Core platform — INTEGRATION_CONTRACT, non configuré (KLT-0001 §4)
ROLE_BOUNDARIES: Comprendre l'architecture ne donne aucun accès réel — OPERATOR_AUTHORIZATION = NOT_IMPLEMENTED/NOT_GRANTED
FREK_PROOF_MAPPING: FREK-WORK (signal réel, hérité de seed_modules.py:891-893)
ORIGIN: legacy M01 + master plan M01 (MERGE)
```

## Situation professionnelle

Sans comprendre l'architecture, un opérateur agit à l'aveugle sur ses
propres surfaces — il publie, modère ou répond sans savoir ce qui relève
réellement de son périmètre.

## Objectifs d'apprentissage

- Comprendre la mission et les valeurs d'une plateforme culturelle de
  type Kiltikonet.
- Identifier les grandes surfaces fonctionnelles (contenus, communauté,
  badges, support, partenariats, analytics) et leurs relations.
- Se situer soi-même comme opérateur dans cette architecture, sans
  supposer un accès qu'on n'a pas.

## Notions essentielles

Une plateforme culturelle relie plusieurs **surfaces** distinctes
(gestion de contenu, communauté, preuve de participation, support,
analytics) qui doivent rester cohérentes entre elles. Un opérateur qui ne
voit qu'une surface (ex. la publication de contenu) sans comprendre ses
liens avec les autres (ex. comment un contenu publié affecte le support
et l'analytics) opère de façon fragmentée.

## Méthode

1. Cartographier les grandes surfaces fonctionnelles d'une plateforme
   culturelle type.
2. Identifier les liens entre elles (un contenu publié génère des
   questions de support, par exemple).
3. Se positionner explicitement dans cette architecture selon son rôle
   réel.

## Exemples

Publier l'annonce de la Veillée du Tanbou (M03) génère potentiellement
des questions de support (M07) et alimente l'analytics d'engagement
(M09) — un opérateur qui ignore ce lien traite chaque surface comme
isolée.

## Cas

System map de la Veillée du Tanbou vue comme un cas d'usage plateforme
(`case/CAS_ANGLE_OPERATEUR.md`).

## Erreurs fréquentes

- Traiter chaque surface fonctionnelle comme indépendante des autres.
- Supposer un accès administrateur non réellement accordé.

## Activité

Cartographie collective des surfaces et de leurs liens à partir du cas.

## Exercice

Identifier deux surfaces dont l'action sur l'une affecte directement
l'autre.

## Livrable

System map.

## Critères de réussite

- Les surfaces principales sont identifiées et reliées correctement.
- Le candidat se positionne sans supposer un accès non réel.

## Preuve

System map, conservée dans le registre de preuves (M11) — signal
`FREK-WORK`.

## Auto-évaluation

*Ma carte reflète-t-elle les vraies relations entre surfaces, ou une
vision fragmentée ?*

## Passage au module suivant

M02 précise concrètement quels accès et rôles le candidat détient
réellement dans cette architecture.
