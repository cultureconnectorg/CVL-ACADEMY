# FRK-37 — Banque N1 (formatif)

Réserve `FRK37.SKILL.*`.

## Frontière FRK-36/FRK-37 (M3)

1. Qu'est-ce que l'attestation de source/dispositif (prouver quel
   appareil/source a produit un actif média) et en quoi diffère-t-elle
   de la capture authentique générale (FRK-36) ?
2. Pourquoi cette formation cite FRK-36 par référence plutôt que de
   redéfinir la capture authentique ?

## Racine de confiance (M1)

3. Pourquoi l'attestation de dispositif nécessite-t-elle une racine de
   confiance matérielle ou cryptographique (ex. clé liée à l'appareil) ?
4. Que se passerait-il sans racine de confiance ? (N'importe quel
   logiciel pourrait prétendre être n'importe quel appareil)

## Mécanisme d'attestation (M2)

5. Donne un exemple de mécanisme d'attestation de source (ex.
   certificat d'appareil signé) et explique ce qu'il prouve
   exactement.
6. Qu'est-ce qu'un certificat d'appareil signé NE prouve PAS ? (Que le
   contenu capturé n'a pas été manipulé après capture — c'est le rôle
   de FRK-38)
7. Comment un vérificateur valide-t-il un certificat d'appareil ? (En
   vérifiant la chaîne de certificats jusqu'à une clé de fabricant/
   émetteur de confiance)

## Frontière FRK-38 (M3)

8. Une attestation de dispositif valide suffit-elle à garantir
   l'intégrité complète du média ? (Non — élimination si affirmé, c'est
   la frontière avec FRK-38)

## Corrigé indicatif

1. FRK-36 couvre la capture authentique en général (intégrité dès
   l'origine) ; FRK-37 se concentre spécifiquement sur la preuve de
   quel appareil/source a produit l'actif.
2. Réutiliser par référence évite la duplication et garde FRK-36 comme
   source unique de vérité pour la capture authentique générale.
3. Sans racine de confiance, n'importe quel logiciel pourrait
   prétendre être n'importe quel appareil — la confiance doit ancrer
   dans un secret matériel ou cryptographique vérifiable.
4. Voir 3.
5. Un certificat d'appareil signé prouve que l'appareil possède une
   clé spécifique.
6. Que le contenu capturé n'a pas été manipulé après capture.
7. En vérifiant la chaîne de certificats jusqu'à une clé de fabricant/
   émetteur de confiance.
8. Non — élimination si affirmé.
