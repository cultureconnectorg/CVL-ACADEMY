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
5. En quoi un vecteur d'or (golden vector) diffère-t-il d'un test
   arbitraire — pourquoi sa provenance importe-t-elle pour la
   crédibilité de la preuve ?
6. Si les 16 tests échouaient tous, que cela prouverait-il — et
   inversement, que ne prouve PAS leur succès complet ?
7. Pourquoi FRK-71 est-il un prérequis logique pour FRK-75 malgré
   leur différence de sujet (architecture vs. ingénierie de
   vérificateur) ?
8. Comment un candidat démontrerait-il, sans inventer de résultat,
   qu'il comprend la différence entre « cette implémentation
   fonctionne » et « la spécification est correcte » ?

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
5. Un vecteur d'or provient d'une source de référence indépendante et
   validée ; un test arbitraire ne garantit rien sur la conformité à
   une spécification externe — c'est la provenance qui donne du poids
   à la preuve, pas le simple fait de passer.
6. Un échec complet prouverait que cette implémentation ne suit même
   pas ses propres vecteurs de référence — un signal d'alarme
   immédiat. Un succès complet ne prouve que la conformité de cette
   implémentation à ces vecteurs précis, jamais l'exhaustivité ou
   l'agnosticisme de la spécification testée.
7. FRK-71 établit la littératie architecturale du cluster FREK v3 dans
   son ensemble ; sans cette base, la place précise de
   `reference_verifier/` dans l'échelle de maturité globale resterait
   incompréhensible.
8. En rédigeant explicitement deux affirmations séparées et distinctes
   — « cette implémentation Python passe ses 16 tests » (prouvé) et
   « la spécification est démontrée correcte et implémentable
   génériquement » (non prouvé, en attente d'une implémentation
   croisée) — sans jamais fusionner les deux.
