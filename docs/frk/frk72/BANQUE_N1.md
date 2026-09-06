# FRK-72 — Banque N1 (formatif)

Réserve `FRK72.SKILL.*`.

1. Décris la structure du protocole d'attestation FREK réel (283
   octets, niveaux L0/L1/L2) tel que spécifié dans
   `FREK_Attestation_Protocol_v0.1.md`.
2. Pourquoi ce protocole reste-t-il classé `ARCHITECTURE_LEVEL_2`
   comme FRK-71, plutôt que « implémenté et testé en production » ?
3. Quelle est la différence entre les niveaux L0, L1 et L2 de ce
   protocole (à un niveau conceptuel) ?
4. Pourquoi cette formation cite FRK-71 par référence plutôt que de
   redéfinir l'échelle de maturité ?

## Corrigé indicatif

1. Le protocole spécifie un format binaire fixe de 283 octets avec
   trois niveaux d'attestation croissants (L0/L1/L2), documentés dans
   le fichier réel.
2. La spécification existe et est cohérente, mais aucune preuve
   matérielle (FPGA) ni intégration production ne l'accompagne — même
   discipline de maturité que FRK-71.
3. Chaque niveau ajoute des garanties supplémentaires d'attestation
   (contenu exact réservé à la spécification, non inventé ici).
4. Réutiliser par référence évite la duplication et garde FRK-71 comme
   source unique de vérité pour l'échelle de maturité.
