# KOR-05 — M08 — Suivre un workflow éditorial et un catalogue

```
MODULE_ID: KOR05-M08
COMPETENCY_ID: C8 — Suivre un workflow éditorial et un catalogue
PREREQUISITES: M07
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune (buildable à échelle réduite ; un vrai catalogue à l'échelle d'une plateforme relèverait d'un système KORA non existant)
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: FREK-WORK
ORIGIN: net-new
```

## Situation professionnelle

Sans vue d'ensemble, Kessy risque d'oublier où en est chaque contenu
(en attente, contrôlé, publié) — avec seulement deux créateurs
aujourd'hui, mais le principe doit tenir même si le nombre augmente.

## Objectifs d'apprentissage

- Construire un registre de suivi simple (tableur) qui reste à jour.
- Reconnaître les limites d'une méthode manuelle à grande échelle,
  sans fabriquer une fausse solution technique.

## Notions essentielles

Un **registre de catalogue** manuel (tableur) suffit à l'échelle de
deux créateurs. À plus grande échelle, un système dédié serait
nécessaire — **cette limite doit être reconnue explicitement**, pas
comblée par une capacité KORA qui n'existe pas (`PRODUCT_DEPENDENCY =
DEFERRED` au-delà de cette échelle).

## Méthode

1. Construire un registre simple (créateur, contenu, statut, date).
2. Le maintenir à jour à chaque étape du flux (M03-M07).
3. Documenter explicitement la limite d'échelle de cette méthode.

## Exemples

Le registre indique "Rasin ép.0 — publié — 04/09" et "Kajou Studio
ép.1 — en contrôle qualité — 10/09" — à jour et lisible en un coup
d'œil pour deux créateurs. À l'inverse, mettre à jour le registre
seulement en fin de semaine plutôt qu'à chaque étape franchie
laisserait un état affiché périmé pendant plusieurs jours — un
registre n'est utile que s'il reflète l'état réel au moment où on le
consulte.

## Cas

Le registre porte sur les deux créateurs réels du cas (`case/
CASE.md`).

## Erreurs fréquentes

- Laisser le registre se désynchroniser de la réalité.
- Prétendre qu'une méthode manuelle tiendrait à grande échelle sans le
  dire.
- Mettre à jour le registre par lot en fin de semaine plutôt qu'à
  chaque étape franchie, le laissant afficher un état périmé une
  bonne partie du temps.

## Activité

Construction du registre initial.

## Exercice

Maintenir le registre à jour sur l'ensemble du cas.

## Livrable

Registre de catalogue à jour + note sur sa limite d'échelle.

## Critères de réussite

- Le registre reflète l'état réel de chaque contenu.
- La limite d'échelle de la méthode est explicitement reconnue.

## Preuve

Registre + note, signal `FREK-WORK`.

## Auto-évaluation

*Mon registre est-il à jour, ou ai-je laissé un écart avec la
réalité ?*

## Passage au module suivant

Ce registre est la base du reporting produit lors de l'incident traité
en M09.
