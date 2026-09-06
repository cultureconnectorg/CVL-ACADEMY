# FRK-38 — Banque N1 (formatif)

Réserve `FRK38.SKILL.*`.

1. Qu'est-ce que la vérification d'intégrité média post-capture et en
   quoi diffère-t-elle de FRK-36 (capture authentique) et FRK-37
   (attestation de source) ?
2. Cite une technique réelle de détection anti-tampering (ex. analyse
   de cohérence de compression, détection d'artefacts d'édition) et
   explique son principe.
3. Pourquoi une chaîne complète de confiance média a-t-elle besoin des
   trois formations FRK-36/37/38 ensemble, sans qu'aucune ne remplace
   les deux autres ?
4. Pourquoi cette formation cite FRK-36/37 par référence plutôt que de
   les redéfinir ?

## Corrigé indicatif

1. FRK-36 porte sur l'intégrité à l'origine, FRK-37 sur la preuve de
   la source, FRK-38 sur la vérification après coup qu'aucune
   altération n'a eu lieu — trois moments distincts de la chaîne.
2. L'analyse de cohérence de compression détecte des artefacts
   incohérents révélant une recompression après montage — principe
   réel de détection forensique d'image.
3. Une capture peut être authentique à l'origine (FRK-36), venir d'un
   appareil attesté (FRK-37), mais avoir été altérée après — seule
   FRK-38 couvre ce cas ; aucune des trois formations ne suffit seule
   pour une chaîne de confiance complète.
4. Réutiliser par référence évite la duplication et garde chaque
   formation comme source unique de vérité pour son moment de la
   chaîne.
