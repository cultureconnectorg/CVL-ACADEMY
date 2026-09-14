# FRK-38 — Banque N1 (formatif)

Réserve `FRK38.SKILL.*`.

## Les trois moments de la chaîne (M3)

1. Qu'est-ce que la vérification d'intégrité média post-capture et en
   quoi diffère-t-elle de FRK-36 (capture authentique) et FRK-37
   (attestation de source) ?
2. Pourquoi cette formation cite FRK-36/37 par référence plutôt que de
   les redéfinir ?

## Techniques de détection anti-tampering (M2)

3. Cite une technique réelle de détection anti-tampering (ex. analyse
   de cohérence de compression) et explique son principe.
4. Que révèle une incohérence de compression (double compression) ?
   (Des artefacts de quantification incohérents entre régions,
   typiques d'une ré-sauvegarde après montage)
5. Cite une deuxième technique réelle. (Détection d'artefacts d'édition
   — discontinuités de bruit, incohérences d'éclairage/ombre, ou
   rupture de chaîne de hash incrémentale)

## Chaîne complète (M1/M3)

6. Pourquoi une chaîne complète de confiance média a-t-elle besoin des
   trois formations FRK-36/37/38 ensemble, sans qu'aucune ne remplace
   les deux autres ?
7. Une capture authentique d'un appareil attesté peut-elle échouer une
   vérification d'intégrité ? (Oui — si elle a été altérée après
   capture ; c'est exactement ce que FRK-38 couvre)
8. Une seule des trois formations suffit-elle à garantir la confiance
   complète ? (Non — élimination automatique si affirmé)

## Corrigé indicatif

1. FRK-36 porte sur l'intégrité à l'origine, FRK-37 sur la preuve de
   la source, FRK-38 sur la vérification après coup qu'aucune
   altération n'a eu lieu — trois moments distincts de la chaîne.
2. Réutiliser par référence évite la duplication et garde chaque
   formation comme source unique de vérité pour son moment de la
   chaîne.
3. L'analyse de cohérence de compression détecte des artefacts
   incohérents révélant une recompression après montage.
4. Des artefacts de quantification incohérents entre régions.
5. Détection d'artefacts d'édition (discontinuités de bruit,
   incohérences d'éclairage, rupture de chaîne de hash).
6. Une capture peut être authentique à l'origine (FRK-36), venir d'un
   appareil attesté (FRK-37), mais avoir été altérée après — seule
   FRK-38 couvre ce cas ; aucune des trois formations ne suffit seule
   pour une chaîne de confiance complète.
7. Oui.
8. Non — élimination automatique.
