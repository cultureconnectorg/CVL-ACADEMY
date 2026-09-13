# FRK-28 — Banque N1 (formatif)

Réserve `FRK28.SKILL.*`.

1. Qu'est-ce qu'un registre d'événements de provenance et en quoi
   diffère-t-il structurellement d'un simple bus pub/sub interne comme
   `backend/services/events.py` (Academy) ?
2. `events.py` alimente `academy.certification.passed` en interne à
   l'Academy — pourquoi ceci n'est-il PAS un registre de provenance,
   même si les deux reposent sur un patron événementiel ?
3. Qu'apporterait un vrai registre d'événements de provenance
   (append-only, horodaté, chaîné) qu'un pub/sub en mémoire ne garantit
   pas ?
4. Pourquoi cette formation doit-elle citer `events.py` comme
   contre-exemple pédagogique, pas comme brique à étendre ?
5. En quoi consiste précisément l'append-only — pourquoi une simple
   convention documentaire ("on ne modifie pas les événements") ne
   suffit-elle pas sans mécanisme technique qui l'impose ?
6. Comment un chaînage entre événements successifs permet-il de
   détecter une suppression ou une insertion silencieuse ?
7. Un bus pub/sub en mémoire perd-il ses événements au redémarrage du
   processus — pourquoi cela suffit-il déjà à disqualifier `events.py`
   comme registre de provenance ?
8. Pourquoi la correction d'un événement erroné se fait-elle par un
   nouvel événement compensatoire plutôt que par une réécriture de
   l'événement original ?

## Corrigé indicatif

1. Un registre de provenance persiste et chaîne des événements
   probants dans le temps ; `events.py` est un bus pub/sub en mémoire,
   volatile, sans garantie de persistance ni de chaînage.
2. `events.py` notifie des abonnés internes sans laisser de trace
   append-only vérifiable — aucune garantie de provenance n'en découle.
3. L'append-only et le chaînage garantissent qu'aucun événement passé
   ne peut être modifié ou supprimé silencieusement — garanties
   absentes d'un pub/sub en mémoire.
4. Le confondre avec une brique à étendre laisserait croire qu'une
   fonctionnalité de provenance existe déjà dans l'Academy — c'est
   faux : `events.py` sert d'exemple pédagogique du patron
   événementiel, rien de plus.
5. Une convention documentaire est contournable par n'importe quel
   accès direct au stockage — seul un mécanisme technique (permissions,
   structure append-only réelle) impose la garantie de façon fiable.
6. Si un événement est retiré ou inséré, la référence au précédent
   attendu par l'événement suivant ne correspond plus — la rupture de
   chaîne est détectable mécaniquement, pas seulement documentée.
7. Oui — un système sans persistance ne peut, par construction, offrir
   aucune garantie de trace durable, condition minimale d'un registre
   de provenance.
8. Réécrire effacerait la trace de l'erreur elle-même — l'événement
   compensatoire préserve l'historique complet, y compris l'erreur et
   sa correction, ce qui est le but même d'un registre de provenance.
