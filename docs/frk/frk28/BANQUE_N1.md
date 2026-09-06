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
