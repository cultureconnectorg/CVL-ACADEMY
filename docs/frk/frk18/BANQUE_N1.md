# FRK-18 — Banque N1 (formatif)

Réserve `FRK18.SKILL.*`.

1. Comment OpenTimestamps ancre-t-il une preuve dans la blockchain
   Bitcoin, et pourquoi cela offre-t-il une garantie différente d'un
   horodatage RFC 3161 classique (FRK-17) ?
2. Qu'est-ce qu'un arbre de Merkle et pourquoi permet-il d'ancrer de
   nombreuses preuves dans une seule transaction Bitcoin ?
3. Pourquoi une preuve OpenTimestamps reste-t-elle vérifiable
   indépendamment, même si le service qui l'a émise disparaît ?
4. Pourquoi aucun système CVLN n'utilise aujourd'hui OpenTimestamps —
   quelle est la discipline « CVLN-gap » à respecter en formation ?

## Corrigé indicatif

1. OpenTimestamps utilise Bitcoin comme horloge décentralisée
   publique ; RFC 3161 repose sur une autorité tierce centralisée —
   modèles de confiance différents.
2. Un arbre de Merkle permet d'agréger des milliers de hachages en une
   seule racine ancrée dans une transaction, réduisant le coût par
   preuve.
3. La preuve d'inclusion (chemin Merkle + transaction Bitcoin publique)
   se vérifie indépendamment de tout service — Bitcoin lui-même sert
   d'horloge publique permanente.
4. Le protocole est réel et enseignable, mais son usage par CVLN est
   `CAPABILITY_NOT_IMPLEMENTED` — jamais présenté comme actif.
