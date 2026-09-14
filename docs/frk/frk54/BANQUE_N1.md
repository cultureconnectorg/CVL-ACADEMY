# FRK-54 — Banque N1 (formatif)

Réserve `FRK54.SKILL.*`.

1. Qu'est-ce qu'un bus d'événements et en quoi diffère-t-il d'un
   webhook (push HTTP externe) ?
2. Le vrai `events.py` de cette Academy (pub/sub en-process, alimente
   `academy.certification.passed`) est cité comme exemple travaillé —
   pourquoi précise-t-on qu'il n'a aucune surface webhook/externe
   aujourd'hui ?
3. Qu'est-ce qu'un contrat d'intégration (schéma d'événement stable,
   versionné) et pourquoi est-il indispensable pour tout consommateur
   externe d'un événement ?
4. Pourquoi serait-il une erreur éliminatoire de présenter `events.py`
   comme une infrastructure FREK ?
5. Pourquoi un webhook nécessite-t-il des garanties (authentification,
   retries, ordre) qu'un bus interne en mémoire n'a pas besoin de
   fournir ?
6. Que se passe-t-il pour un consommateur externe si le schéma d'un
   événement change sans versionnage ni compatibilité ascendante ?
7. Pourquoi le fait qu'`events.py` alimente déjà
   `academy.certification.passed` en interne ne rapproche-t-il en rien
   d'une infrastructure webhook fonctionnelle ?
8. Quelle différence de fiabilité existe-t-il entre un abonné en
   mémoire qui manque une notification (perdue) et un webhook avec
   file d'attente et retries ?

## Corrigé indicatif

1. Un bus d'événements diffuse en interne (souvent en mémoire) ; un
   webhook pousse activement une notification HTTP vers un système
   externe — deux mécanismes de diffusion distincts.
2. `events.py` reste un pub/sub interne à l'Academy, sans aucune route
   HTTP externe ni contrat de webhook — il illustre le patron, pas une
   infrastructure d'intégration.
3. Un contrat d'intégration stable garantit que les consommateurs
   externes ne cassent pas silencieusement à chaque évolution du
   schéma d'événement.
4. Cela affirmerait une capacité d'intégration externe inexistante —
   contraire à la discipline `CVLN-gap`.
5. Un webhook traverse un réseau non fiable vers un système tiers —
   authentification, retries et garanties d'ordre sont nécessaires
   pour compenser cette non-fiabilité, absente d'un bus interne en
   mémoire du même processus.
6. Le consommateur externe échouerait silencieusement ou
   interpréterait mal les données — c'est exactement ce qu'un contrat
   versionné et une compatibilité ascendante préviennent.
7. Parce qu'alimenter un abonné interne ne construit aucune route
   HTTP, aucune authentification externe, aucun contrat de schéma
   publié — la distance technique jusqu'à un webhook réel reste
   entière.
8. Un abonné en mémoire perdu au redémarrage du processus perd
   silencieusement l'événement ; un webhook avec file d'attente et
   retries garantit la livraison malgré une indisponibilité
   temporaire du destinataire.
