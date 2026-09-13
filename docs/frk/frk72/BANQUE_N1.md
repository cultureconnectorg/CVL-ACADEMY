# FRK-72 — Banque N1 (formatif)

Réserve `FRK72.SKILL.*`.

## Structure du protocole (M1)

1. Décris la structure générale du protocole d'attestation FREK réel
   (283 octets, niveaux L0/L1/L2) tel que référencé dans
   `FREK_Attestation_Protocol_v0.1.md`.
2. Quelle preuve d'ingénierie réelle accompagne cette spécification,
   au-delà du document lui-même ? (Un vérificateur de référence Python,
   `reference_verifier/`, avec 16 tests passants, des vecteurs de test
   de référence, et une vérification de signature ECDSA P-256 réelle)

## Niveaux L0/L1/L2 (M2)

3. Quelle est la différence entre les niveaux L0, L1 et L2 de ce
   protocole (à un niveau conceptuel) ?
4. Un candidat doit-il inventer le contenu exact des champs de chaque
   niveau s'il ne les connaît pas précisément ? (Non — inventer un
   contenu non vérifié est une fabrication de preuve interdite)

## Frontière de maturité héritée (M3)

5. Pourquoi ce protocole reste-t-il classé `ARCHITECTURE_LEVEL_2`
   comme FRK-71, plutôt que « implémenté et testé en production » ?
6. L'existence d'un vérificateur de référence avec 16 tests passants
   suffit-elle à revendiquer un statut matériel prouvé ? (Non — c'est
   une preuve d'ingénierie logicielle réelle, mais pas une preuve
   matérielle FPGA ni une intégration production)
7. Pourquoi cette formation cite FRK-71 par référence plutôt que de
   redéfinir l'échelle de maturité ?

## Corrigé indicatif

1. Le protocole spécifie un format binaire fixe de 283 octets avec
   trois niveaux d'attestation croissants (L0/L1/L2).
2. Un vérificateur de référence Python réel (16 tests passants,
   vecteurs de test, ECDSA P-256).
3. Chaque niveau ajoute des garanties supplémentaires d'attestation
   par rapport au précédent (contenu exact réservé à la spécification,
   non inventé ici).
4. Non — c'est une fabrication de preuve interdite.
5. La spécification existe et est cohérente, et un vérificateur de
   référence existe et passe ses tests, mais aucune preuve matérielle
   (FPGA) ni intégration production ne l'accompagne — même discipline
   de maturité que FRK-71.
6. Non — c'est une preuve d'ingénierie logicielle, pas matérielle.
7. Réutiliser par référence évite la duplication et garde FRK-71 comme
   source unique de vérité pour l'échelle de maturité.
