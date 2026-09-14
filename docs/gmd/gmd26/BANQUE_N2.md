# GMD-26 — Banque N2 (cas appliqués)

## Cas N2-1 — Demande de segment marketing

Le manager veut cibler "les fans VIP de Paris pour une offre
exclusive." Décris comment produire cette liste avec les champs réels,
et ce qu'il faut vérifier avant de la livrer.

**Critères de notation:** croise `segments` contient `"vip"` ET
`cities` contient `"Paris"` — note que `cities` est une liste
(un fan peut avoir acheté dans plusieurs villes, donc "de Paris" veut
dire "a au moins un achat à Paris," pas "habite à Paris" — le schéma ne
capture pas d'adresse). Élimination si le candidat invente un champ
`city_primaire`/`adresse`.

## Cas N2-2 — Deux fans, même identifiant apparent

Un correcteur remarque que `external_id` est identique pour deux
emails différents (`marie@gmail.com` et `marie@yahoo.com`). Explique
pourquoi, et quel est le risque réel.

**Critères de notation:** cite `external_id = f"gm-fan-{email.split
('@')[0]}"` — collision réelle du local-part, pas un bug caché à
inventer une explication différente ; propose de signaler ce risque
de données plutôt que de le nier ou de le "corriger" en inventant une
règle de désambiguïsation qui n'existe pas dans le code.

## Cas N2-3 — Demande de métrique non trackable

Le manager veut "le taux d'ouverture moyen des emails par fan pour
prioriser les VIP." Réponds correctement avec les champs disponibles.

**Critères de notation:** réponse correcte = "non trackable
actuellement" — aucun champ d'ouverture d'email n'existe sur `fans`
ni ailleurs dans le schéma lu. Élimination automatique si le candidat
invente un chiffre ou un champ `open_rate`.
