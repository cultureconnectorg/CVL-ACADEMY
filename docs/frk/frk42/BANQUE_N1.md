# FRK-42 — Banque N1 (formatif)

Réserve `FRK42.SKILL.*`.

## Frontière vs. FRK-20 (M1)

1. Qu'est-ce que le transport de preuve hors-ligne (déplacer des
   artefacts de preuve entre environnements déconnectés) et pourquoi
   diffère-t-il de la vérification offline (FRK-20) ?
2. FRK-20 vérifie-t-il le medium de transport ? (Non — FRK-20 vérifie
   un artefact déjà en main, sans réseau ; FRK-42 conçoit comment cet
   artefact voyage sans perdre sa vérifiabilité)

## Artefacts auto-vérifiables (M1)

3. Pourquoi un artefact de preuve doit-il rester auto-vérifiable même
   après avoir traversé un support physique déconnecté (clé USB,
   support hors-réseau) ?
4. Cite deux façons de rendre un artefact auto-vérifiable. (Signature
   détachée accompagnant l'artefact, ou signature embarquée dans la
   structure même de l'artefact)

## Défis de transport (M2)

5. Cite un défi propre au transport (vs. simplement le stockage) —
   ex. intégrité pendant le transfert, ordre de livraison.
6. Comment détecter qu'un artefact manque dans une séquence
   multi-artefacts ? (Chaînage par hash — chaque artefact référence le
   hash du précédent, une rupture de chaîne signale un manque ou un
   désordre)
7. Cite un pattern de transport réel pour un petit artefact. (QR code
   imprimé pour un JWT signé de petite taille)
8. Cite un pattern de transport à haute assurance pour environnement
   air-gap. (Transfert unidirectionnel façon data-diode)

## Discipline de gap (M3)

9. Pourquoi aucun système CVLN n'implémente aujourd'hui ce transport —
   quelle discipline CVLN-gap s'applique ? (`CAPABILITY_NOT_IMPLEMENTED`
   — discipline enseignée comme conception marché-générale)
10. Un candidat peut-il affirmer qu'un système CVLN transporte des
    preuves hors-ligne aujourd'hui ? (Non — élimination si affirmé)

## Corrigé indicatif

1. FRK-20 vérifie une preuve sans réseau ; FRK-42 conçoit comment
   déplacer physiquement cette preuve d'un environnement à un autre
   sans perdre sa vérifiabilité — problème de transport, pas de
   vérification.
2. FRK-20 vérifie un artefact déjà en main ; il ne conçoit pas le
   moyen par lequel cet artefact est arrivé là.
3. Sans auto-vérifiabilité embarquée, le transport introduit un risque
   de falsification indétectable en cours de route.
4. Signature détachée (fichier séparé accompagnant l'artefact) ou
   signature embarquée dans la structure de l'artefact lui-même.
5. Un support physique peut être altéré ou perdu en transit — le
   design doit prévoir la détection d'altération et l'ordre de
   réception de plusieurs artefacts.
6. Un chaînage par hash rend une rupture ou un désordre détectable
   sans confiance dans le medium de transport.
7. Un JWT signé encodé visuellement dans un QR code imprimé.
8. Un transfert unidirectionnel (data-diode) empêchant tout canal
   retour, adapté aux environnements air-gap à haute assurance.
9. Aucun système du dépôt ne transporte de preuve hors-ligne — la
   discipline reste enseignée comme conception marché-générale.
10. Non — c'est une élimination automatique si affirmé.
