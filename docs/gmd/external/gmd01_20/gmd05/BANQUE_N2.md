# GMD-05 — Banque N2 (cas appliqués)

## Cas N2-1 — Verrou de réservation affirmé à tort

Un candidat affirme que le système "réserve" un billet dès le clic
"acheter," empêchant toute survente. Corrige.

**Critères de notation:** cite la réalité documentée par GMD-24 — la
vérification `remaining < req.quantity` a lieu avant la création de
la session Stripe, sans verrou explicite ; la vraie garantie
anti-survente est l'incrément atomique `$inc` sur `sold`, appliqué au
moment du webhook, pas du clic. Élimination si le candidat maintient
qu'un verrou de réservation existe dans le code réel.

## Cas N2-2 — Tarification dynamique présentée comme capacité de la plateforme

Un stagiaire affirme que "la plateforme Good Mood gère la tarification
dynamique automatiquement." Corrige.

**Critères de notation:** rappelle que la tarification dynamique est
une pratique de marché légitime, mais **non implémentée** dans le
repo réel audité — elle doit être enseignée comme connaissance de
marché, jamais comme capacité de la plateforme. Élimination si le
candidat maintient l'affirmation de capacité plateforme.

## Cas N2-3 — Contrainte email confondue entre billets et merch

Un collègue affirme que l'email est obligatoire pour tout achat
(billets et merch identiquement). Corrige.

**Critères de notation:** cite le fait réel documenté par GMD-24 — la
contrainte email (`422 "Email required for ticket purchase"`)
s'applique uniquement quand `is_ticket` est vrai, pas aux achats
merch. Élimination si le candidat maintient une contrainte uniforme
non fondée sur le code réel.
