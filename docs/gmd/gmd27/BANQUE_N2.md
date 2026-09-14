# GMD-27 — Banque N2 (cas appliqués)

## Cas N2-1 — Nouveau produit créé mais introuvable à l'achat

Un opérateur crée un t-shirt via `POST /admin/merch`, le voit apparaître
sur `GET /merch`, mais le checkout échoue avec "Price not found."
Diagnostique.

**Critères de notation:** identifie que la création `Product` seule ne
suffit pas — un prix Stripe réel doit être synchronisé via
`_sync_stripe_item` (`lookup_prefix="gm"`) avant que `lookup_key` soit
utilisable en checkout ; propose de vérifier si cette synchronisation a
réellement eu lieu plutôt que de supposer un bug ailleurs. Élimination
si le candidat invente une route "activer le prix" qui n'existe pas
dans le code lu.

## Cas N2-2 — Produit désactivé mais toujours visible côté admin

Le manager signale qu'un produit `active=False` apparaît encore dans
`GET /admin/merch`. Est-ce un bug ?

**Critères de notation:** non — `GET /admin/merch` ne filtre pas sur
`active` (contrairement à `GET /merch`, la route publique). Le
candidat doit citer cette différence de comportement exacte plutôt que
de supposer un bug. Élimination si le candidat affirme que les deux
routes filtrent identiquement.

## Cas N2-3 — Confusion Catalogue/Merch

Un nouvel opérateur confond `Volume` (GMD-22) et `Product` (GMD-27) et
tente de vendre un item de catalogue via checkout. Explique l'erreur.

**Critères de notation:** cite que `Volume` n'a ni `price_cents` ni
`lookup_key` utilisable en checkout — ce n'est structurellement pas un
objet vendable dans ce système ; jamais conflate les deux modèles même
si leurs routes CRUD admin se ressemblent.
