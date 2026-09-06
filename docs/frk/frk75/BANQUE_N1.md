# FRK-75 — Banque N1 (formatif)

Réserve `FRK75.SKILL.*`.

1. Cite les 7 modules réels du package `reference_verifier/` et
   explique pourquoi cette formation est qualifiée de « mieux
   ancrée » du cluster FRK-71→75.
2. Que prouvent réellement les 16 tests unitaires contre des vecteurs
   d'or (golden vectors) — et que ne prouvent-ils PAS ?
3. Pourquoi une implémentation Rust croisée est-elle nommée par le
   corpus lui-même comme étape suivante nécessaire, plutôt qu'un
   « nice-to-have » ?
4. Pourquoi cette formation ne doit-elle jamais être confondue avec
   FRK-13 (stub `issue_proof()` de l'Academy) ?

## Corrigé indicatif

1. `frek_constants.py`, `frek_types.py`, `frek_crypto.py`,
   `frek_parser.py`, `frek_registry.py`, `frek_verifier.py`,
   `frek_device_sim.py` — package réel, structuré, testé ; c'est le
   seul du cluster avec du code fonctionnel et testé, pas seulement de
   la documentation.
2. Les tests prouvent que cette implémentation Python particulière
   produit les résultats attendus sur des vecteurs connus — ils ne
   prouvent PAS que la spécification elle-même est correcte
   indépendamment de l'implémentation.
3. Une seule implémentation ne peut jamais prouver qu'une spécification
   est correctement définie et implémentable de façon générique — une
   seconde implémentation indépendante (Rust) est le test réel
   d'agnosticisme de la spec.
4. FRK-13 enseigne le stub réel et limité de l'Academy
   (`issue_proof()`, UUID sans garantie) ; FRK-75 enseigne une
   ingénierie de vérificateur bien plus mature et testée dans
   `frek_v3/` — deux réalités techniques très différentes, jamais
   fusionnées.
