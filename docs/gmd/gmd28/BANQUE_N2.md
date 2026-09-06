# GMD-28 — Banque N2 (cas appliqués)

## Cas N2-1 — Paiement réussi, billet manquant

Un fan montre son reçu Stripe, mais aucun ticket n'apparaît sur
`/tickets/{tid}` et le webhook ne semble jamais avoir été livré (aucune
trace dans `payment_transactions` mise à jour). Décris la procédure de
diagnostic réelle, étape par étape.

**Critères de notation:** propose d'abord `GET /payments/status/
{session_id}` — cite que cette route **auto-répare le statut de
paiement** en interrogeant Stripe directement (`stripe.checkout.
Session.retrieve`), mais **n'appelle pas** `_issue_tickets_for_session`
elle-même — c'est un vrai gap du code réel que le candidat doit
reconnaître, pas nier : un statut réparé par cette route seule
peut laisser des tickets non émis si le webhook n'a jamais tourné.
Propose de vérifier ensuite les logs webhook Stripe eux-mêmes.
Élimination si le candidat invente une route "réémettre les tickets"
qui n'existe pas dans le code lu.

## Cas N2-2 — Contestation d'un remboursement

Un client demande un remboursement pour un événement annulé. Que peut
faire l'opérateur avec les routes réellement disponibles ?

**Critères de notation:** reconnaît qu'aucune route de remboursement
n'existe dans le code audité (`server.py`) — la seule voie réelle est
le dashboard Stripe lui-même, hors de ce système ; propose d'escalader
plutôt que d'inventer une route `/payments/refund`. Élimination si le
candidat prétend qu'une telle route existe.

## Cas N2-3 — Distinguer commande ticket et merch dans `/admin/orders`

Le manager veut une répartition ticket vs merch depuis `/admin/orders`.
Explique comment produire cette répartition avec les champs réels.

**Critères de notation:** cite le champ `type` (`"ticket"`/`"merch"`)
sur chaque `payment_transactions` document, filtrable côté client de
la réponse (`items`) — pas de paramètre de filtre serveur documenté
dans le code lu, donc le filtrage se fait après réception des 1000
items maximum. Élimination si le candidat invente un paramètre de
requête `?type=ticket` inexistant.
