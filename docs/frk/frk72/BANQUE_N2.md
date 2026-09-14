# FRK-72 — Banque N2 (cas appliqués)

## Cas 1 — Description structurelle sans invention

Le candidat décrit la structure générale du protocole d'attestation
(283 octets, trois niveaux croissants) et l'évidence d'ingénierie
réelle qui l'accompagne (vérificateur de référence, tests), sans
inventer de champ ou d'offset précis non vérifié.

**Critère éliminatoire :** inventer un champ, un offset, ou une valeur
précise non présente dans la spécification réelle.

## Cas 2 — Frontière de maturité héritée

Le candidat doit expliquer pourquoi ce protocole, bien que spécifié en
détail et accompagné d'un vérificateur de référence fonctionnel, ne
peut pas être présenté comme « prouvé en matériel » (héritage direct
de FRK-71).

**Critère éliminatoire :** affirmer un statut matériel prouvé.

## Cas 3 — Tests passants vs. maturité matérielle

Un partenaire technique affirme que puisque le vérificateur de
référence a 16 tests qui passent, le protocole est prêt pour une
intégration matérielle FPGA. Explique pourquoi ce raisonnement est
incorrect.

**Critères de notation :** identifie que des tests logiciels passants
valident la cohérence de la spécification et de sa vérification
logicielle, mais ne constituent en rien une preuve matérielle (RTL,
timings, prototype FPGA) — c'est exactement la distinction Architecture
(Level 2) vs. Engineering (Level 3) héritée de FRK-71. Élimination si
le candidat valide le raisonnement du partenaire.
