# IOS-07 — Banque N1 (formatif)

Réserve `IOS07.SKILL.*`.

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
