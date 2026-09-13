# IOS-07 — Banque N1 (formatif)

Réserve `IOS07.SKILL.EVENT_BUS_OPERATOR.L1`.

1. Qu'est-ce que `events.py` réellement (en-process pub/sub) et
   pourquoi n'est-ce jamais un système distribué ?
2. Pourquoi cette formation renvoie-t-elle vers FRK-54 plutôt que de
   re-décrire le même mécanisme ?
3. Le vrai corpus de gouvernance de `Cvln-ios-v.1` (21 ADRs, 7 RFCs,
   constitution, specs de protocole, backend de contrôle de dérive)
   est cité comme preuve de l'ampleur réelle de l'écosystème — pourquoi
   ne doit-il jamais être présenté comme ce que `events.py` implémente
   ou auquel il se connecte ?
4. Pourquoi ce corpus se déclare-t-il lui-même explicitement PAS
   `DEPLOYED_RUNTIME`, et pourquoi cette précision est-elle
   déterminante pour cette formation ?
5. Quelle est la relation exacte entre IOS-07 et BRN-15 ? Les deux
   formations certifient-elles la même compétence ?
6. Un candidat affirme qu'`events.py` "garantit la livraison" des
   événements même si le processus redémarre entre-temps. Que
   réponds-tu ?
7. Pourquoi cette formation existe-t-elle comme `NEW_INTERNAL` séparée
   plutôt que d'être simplement fusionnée dans BRN-15 ou FRK-54 ?

## Corrigé indicatif

1. `events.py` est un bus pub/sub en mémoire, interne au processus de
   l'Academy — aucune communication réseau, aucune garantie de
   durabilité distribuée.
2. FRK-54 traite déjà le même mécanisme sous-jacent — le re-décrire
   dupliquerait le contenu et risquerait une divergence.
3. Aucune intégration observée ne relie `events.py` au corpus de
   gouvernance de `Cvln-ios-v.1` — les fusionner inventerait un
   câblage inexistant.
4. Cette déclaration officielle du corpus lui-même empêche toute
   inflation de son statut — enseigner honnêtement cette limite fait
   partie de la discipline `repo-truth-first`.
5. IOS-07 et BRN-15 reposent sur le même mécanisme technique
   (`events.py`), mais certifient des littératies distinctes : BRN-15
   porte sur le touchpoint unique `academy.certification.passed`
   spécifiquement, IOS-07 porte sur le bus lui-même comme mécanisme
   général et sa frontière avec le vocabulaire de marché "Intelligence
   OS".
6. Réponse éliminatoire à corriger : `events.py` ne garantit aucune
   livraison persistante — c'est un pub/sub en mémoire, tout événement
   non consommé au moment de l'émission est perdu si le processus
   s'arrête. Affirmer une garantie de durabilité invente une propriété
   absente du code réel.
7. Elle isole spécifiquement la littératie du vocabulaire "Intelligence
   OS" pour éviter deux écueils : gonfler BRN-15/FRK-54 avec un
   vocabulaire de marché qui leur est étranger, et évaluer deux fois un
   candidat sur un contenu technique identique sous un nom différent.
