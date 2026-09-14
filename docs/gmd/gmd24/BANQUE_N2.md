# GMD-24 — Banque N2 (cas appliqués)

## Cas N2-1 — Vente presque complète, plusieurs achats simultanés

Un ticket type a `quota=100`, `sold=98`. Trois acheteurs tentent
d'acheter 2 billets chacun au même instant. Explique, à partir du code
réel, ce qui doit se passer et pourquoi une architecture naïve
(vérifier `remaining` puis créer la session) pourrait échouer.

**Critères de notation:** cite que la vérification `remaining <
req.quantity` se fait **avant** la création de la session Stripe, côté
`create_checkout` — un candidat rigoureux note que ce n'est **pas**
une réservation atomique (pas de verrou/hold sur `quota` au moment du
check), donc un risque de sur-vente en cas de course existe
théoriquement si deux checkouts passent le check presque simultanément
avant qu'un paiement ne soit confirmé ; la vraie protection contre la
sur-vente définitive est l'incrément atomique `$inc` sur `sold` **au
moment du webhook**, pas au moment du checkout. Élimination si le
candidat prétend qu'il existe un verrou de réservation explicite dans
le code — il n'y en a pas, c'est une observation honnête à faire, pas
une capacité à inventer.

## Cas N2-2 — Achat sans email

Un acheteur tente un achat de billet sans fournir d'email. Que se
passe-t-il, et pourquoi ce comportement est-il différent pour un achat
merch ?

**Critères de notation:** cite `if not req.email: raise 422 "Email
required for ticket purchase"` — s'applique uniquement quand
`is_ticket` est vrai (le champ merch n'a pas cette contrainte dans le
code lu). Élimination si le candidat invente une contrainte email
générique pour tous les achats.

## Cas N2-3 — Ticket scanné réclamé comme "jamais utilisé"

Un fan prétend ne jamais avoir utilisé son billet, mais le scan indique
`already_scanned`. Décris comment tracer la vérité réelle avec les
champs disponibles.

**Critères de notation:** cite les champs `scanned_at`/`scanned_by`
posés par `scan_check` au moment du scan réel (`admin["email"]`) — un
candidat rigoureux propose de vérifier ces deux champs plutôt que de
prendre la parole du fan ou de l'opérateur pour acquis. Élimination si
le candidat invente un "log d'audit" séparé qui n'existe pas dans le
modèle réel.
