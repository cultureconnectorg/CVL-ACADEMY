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
