# FRK-18 — Banque N1 (formatif)

Réserve `FRK18.SKILL.*`.

## Modèle de confiance (M1)

1. Comment OpenTimestamps ancre-t-il une preuve dans la blockchain
   Bitcoin, et pourquoi cela offre-t-il une garantie différente d'un
   horodatage RFC 3161 classique (FRK-17) ?
2. Quel est le modèle de confiance de RFC 3161 ? (Une autorité de
   confiance tierce centralisée dont la signature doit être crue)
3. Quel est le modèle de confiance d'OpenTimestamps ? (Le registre
   public et décentralisé de Bitcoin — aucune autorité tierce à
   croire)

## Mécanique d'ancrage Bitcoin (M2)

4. Qu'est-ce qu'un arbre de Merkle et pourquoi permet-il d'ancrer de
   nombreuses preuves dans une seule transaction Bitcoin ?
5. Que signifie "chemin Merkle" pour une preuve individuelle ? (La
   chaîne de hachages frères nécessaire pour reconstruire la racine
   Merkle à partir du hash de cette preuve)
6. Cite les étapes de vérification manuelle d'une preuve `.ots` sans
   outil. (Recalculer le hash local, reconstruire la racine via le
   chemin Merkle, confirmer que cette racine correspond à celle
   engagée dans la transaction Bitcoin nommée)
7. Pourquoi une preuve OpenTimestamps reste-t-elle vérifiable
   indépendamment, même si le service qui l'a émise disparaît ? (Le
   serveur calendrier n'est qu'une commodité d'agrégation ; l'ancre de
   confiance réelle est Bitcoin lui-même, public et permanent)

## Discipline CVLN-gap (M3)

8. Pourquoi aucun système CVLN n'utilise aujourd'hui OpenTimestamps —
   quelle est la discipline « CVLN-gap » à respecter en formation ?
9. La proximité conceptuelle entre `issue_proof()` et OpenTimestamps
   (tous deux produisent un artefact "preuve") justifie-t-elle une
   affirmation d'usage réel ? (Non — élimination automatique si
   affirmé)

## Corrigé indicatif

1. OpenTimestamps utilise Bitcoin comme horloge décentralisée
   publique ; RFC 3161 repose sur une autorité tierce centralisée —
   modèles de confiance différents.
2. Une autorité de confiance tierce centralisée.
3. Le registre public et décentralisé de Bitcoin.
4. Un arbre de Merkle permet d'agréger des milliers de hachages en une
   seule racine ancrée dans une transaction, réduisant le coût par
   preuve.
5. La chaîne de hachages frères nécessaire pour reconstruire la racine
   Merkle à partir du hash de cette preuve.
6. Recalcul du hash local → reconstruction de la racine via le chemin
   Merkle → confirmation contre la transaction Bitcoin nommée.
7. La preuve d'inclusion (chemin Merkle + transaction Bitcoin publique)
   se vérifie indépendamment de tout service — Bitcoin lui-même sert
   d'horloge publique permanente.
8. Le protocole est réel et enseignable, mais son usage par CVLN est
   `CAPABILITY_NOT_IMPLEMENTED` — jamais présenté comme actif.
9. Non — c'est une élimination automatique si affirmé.
