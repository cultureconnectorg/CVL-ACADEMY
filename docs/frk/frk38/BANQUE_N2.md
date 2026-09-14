# FRK-38 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'une vérification d'intégrité post-capture

Le candidat conçoit un contrôle de détection d'altération (ex.
cohérence de compression, hash-chain) pour un actif média, en citant
FRK-36/37 par référence pour les étapes amont.

**Critère éliminatoire :** redéfinir FRK-36/37 au lieu de les citer.

**Critères de notation :** le contrôle proposé détecte réellement une
altération (pas seulement l'absence d'attestation ou de capture
authentique).

## Cas 2 — Chaîne complète

Le candidat doit expliquer pourquoi une capture authentique (FRK-36)
d'un appareil attesté (FRK-37) peut néanmoins échouer une vérification
d'intégrité (FRK-38) si elle a été altérée après capture.

**Critère éliminatoire :** affirmer qu'une des trois formations suffit
seule à garantir la confiance complète.

## Cas 3 — Détection d'une double compression

Un vérificateur reçoit une image JPEG censée être une capture directe
non retouchée. L'analyse révèle des artefacts de quantification
incohérents entre deux régions de l'image. Que conclure, et que ne
peut-on PAS conclure sans investigation supplémentaire ?

**Critères de notation :** conclut qu'une double compression a eu
lieu, signe probable d'un montage/retouche après la capture d'origine.
Ne peut PAS conclure quelle modification précise a été faite, ni qui
l'a faite — l'analyse de cohérence de compression détecte un signe
d'altération, pas son contenu ni son auteur. Élimination si le
candidat affirme pouvoir identifier la modification exacte à partir de
ce seul signal.
