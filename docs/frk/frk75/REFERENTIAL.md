# FRK-75 — FREK Reference Verifier Engineering

## Repo truth this formation is built on

Grounded in `frek_v3/reference_verifier/` — un package Python réel et
structuré (`frek_constants.py`, `frek_types.py`, `frek_crypto.py`,
`frek_parser.py`, `frek_registry.py`, `frek_verifier.py`,
`frek_device_sim.py`) avec **16 tests unitaires passants contre des
vecteurs d'or (golden vectors)** — déjà audité cette session,
`REPO_REGISTRY.md`. **Le mieux ancré du cluster FRK-71→75.**

Per `FREK_01_75_RECONCILIATION.md` : coverage `SUBSTANTIAL — SOURCE_
OBSERVED, real working code`, distinctness `DISTINCT_PROFESSION`,
action `NEW_EXTERNAL`. Le contrepartie vérificateur de FRK-13 (Proof
Engine) — séquencée après elle.

## Prerequisites

FRK-71, FRK-13 (recommandé).

## Objectives

Un candidat qui complète FRK-75 sait lire et interpréter précisément
une vraie sortie de tests contre un package fonctionnel réel, sans
jamais sur-généraliser ce qu'ils prouvent :

- Enseigner la pratique réelle d'ingénierie de vérificateur de
  référence en utilisant ce package Python authentiquement
  fonctionnel et testé comme exemple travaillé.
- Citer les 7 modules réels du package `reference_verifier/` et
  expliquer pourquoi cette formation est qualifiée de « mieux
  ancrée » du cluster FRK-71→75 : c'est le seul avec du code
  fonctionnel et testé, pas seulement de la documentation.
- Expliquer précisément ce que les 16 tests unitaires contre des
  vecteurs d'or prouvent réellement (que cette implémentation Python
  particulière produit les résultats attendus sur des vecteurs
  connus) et ce qu'ils ne prouvent PAS (que la spécification
  elle-même est correcte indépendamment de l'implémentation).
- Porter la **limitation d'implémentation unique** honnêtement
  disclosée par le corpus lui-même : une implémentation Rust croisée
  est explicitement nommée comme étape suivante nécessaire pour
  prouver que la *spécification* (pas seulement ce code Python) est
  correcte — enseigner cette limitation explicitement, **ne jamais
  impliquer que le protocole est prouvé implementation-agnostic
  aujourd'hui**.
- Expliquer précisément pourquoi une seule implémentation ne peut
  jamais prouver qu'une spécification est correctement définie et
  implémentable de façon générique — une seconde implémentation
  indépendante (Rust) est le test réel d'agnosticisme de la
  spécification.
- Frontière explicite vis-à-vis de FRK-13 : FRK-13 enseigne la réalité
  du stub `issue_proof()` propre à cette Academy (UUID sans garantie) ;
  FRK-75 enseigne cette ingénierie de vérificateur séparée, plus
  mature, réelle, du cluster `frek_v3/` — jamais fusionnées, deux
  réalités techniques très différentes.
- Expliquer précisément pourquoi affirmer que les tests prouvent
  l'agnosticisme d'implémentation de la spécification serait une
  erreur éliminatoire : cela affirmerait une garantie qui n'a pas été
  établie — seule une seconde implémentation indépendante le
  pourrait.

## Modules

1. **Littératie de la structure du package reference-verifier** (7
   modules réels).
2. **Littératie de la suite de tests à vecteurs d'or** (16 tests
   passants).
3. **Discipline de la limitation d'implémentation unique** — l'écart
   d'implémentation croisée Rust, enseigné explicitement, jamais
   lissé.

## Assessment

Un exercice d'ingénierie de vérificateur : le candidat lit une vraie
sortie de test et énonce correctement ce qui est prouvé (cette
implémentation Python passe ses propres vecteurs d'or) vs. ce qui
n'est pas encore prouvé (correction implementation-agnostic, en
attente d'une implémentation croisée Rust) — échec éliminatoire pour
toute affirmation que le protocole lui-même est prouvé.

## Evidence / mission eligibility

`FRK75.SKILL.REFERENCE_VERIFIER_ENGINEERING.L1` réservé une fois
approfondi. Aucun chemin d'éligibilité mission aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment +
rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.
