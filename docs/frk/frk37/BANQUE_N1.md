# FRK-37 — Banque N1 (formatif)

Réserve `FRK37.SKILL.*`.

1. Qu'est-ce que l'attestation de source/dispositif (prouver quel
   appareil/source a produit un actif média) et en quoi diffère-t-elle
   de la capture authentique générale (FRK-36) ?
2. Pourquoi l'attestation de dispositif nécessite-t-elle une racine de
   confiance matérielle ou cryptographique (ex. clé liée à l'appareil) ?
3. Donne un exemple de mécanisme d'attestation de source (ex.
   certificat d'appareil signé) et explique ce qu'il prouve
   exactement — et ce qu'il ne prouve PAS.
4. Pourquoi cette formation cite FRK-36 par référence plutôt que de
   redéfinir la capture authentique ?

## Corrigé indicatif

1. FRK-36 couvre la capture authentique en général (intégrité dès
   l'origine) ; FRK-37 se concentre spécifiquement sur la preuve de
   quel appareil/source a produit l'actif.
2. Sans racine de confiance, n'importe quel logiciel pourrait
   prétendre être n'importe quel appareil — la confiance doit ancrer
   dans un secret matériel ou cryptographique vérifiable.
3. Un certificat d'appareil signé prouve que l'appareil possède une clé
   spécifique ; il ne prouve PAS que le contenu capturé n'a pas été
   manipulé après capture (c'est le rôle de FRK-38).
4. Réutiliser par référence évite la duplication et garde FRK-36 comme
   source unique de vérité pour la capture authentique générale.
