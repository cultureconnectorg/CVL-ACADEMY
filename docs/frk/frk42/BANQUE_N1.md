# FRK-42 — Banque N1 (formatif)

Réserve `FRK42.SKILL.*`.

1. Qu'est-ce que le transport de preuve hors-ligne (déplacer des
   artefacts de preuve entre environnements déconnectés) et pourquoi
   diffère-t-il de la vérification offline (FRK-20) ?
2. Pourquoi un artefact de preuve doit-il rester auto-vérifiable même
   après avoir traversé un support physique déconnecté (clé USB,
   support hors-réseau) ?
3. Cite un défi propre au transport (vs. simplement le stockage) —
   ex. intégrité pendant le transfert, ordre de livraison.
4. Pourquoi aucun système CVLN n'implémente aujourd'hui ce transport —
   quelle discipline CVLN-gap s'applique ?

## Corrigé indicatif

1. FRK-20 vérifie une preuve sans réseau ; FRK-42 conçoit comment
   déplacer physiquement cette preuve d'un environnement à un autre
   sans perdre sa vérifiabilité — problème de transport, pas de
   vérification.
2. Sans auto-vérifiabilité embarquée, le transport introduit un risque
   de falsification indétectable en cours de route.
3. Un support physique peut être altéré ou perdu en transit — le
   design doit prévoir la détection d'altération et éventuellement
   l'ordre de réception de plusieurs artefacts.
4. Aucun système du dépôt ne transporte de preuve hors-ligne — la
   discipline reste enseignée comme conception marché-générale.
