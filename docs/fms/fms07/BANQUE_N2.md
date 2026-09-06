# FMS-07 — Banque N2 (cas appliqués)

## Cas N2-1 — Journée de bookings à traiter

Le studio a 4 réservations en attente : une `requested` datant
d'hier, une `confirmed` pour ce matin, une `in_progress` en cours, et
une demande de passage direct de `requested` à `completed`. Traite
chacune correctement.

**Critères de notation :** reconnaît que chaque transition doit passer
par les statuts réels dans un ordre cohérent (jamais `requested` →
`completed` directement sans passer par `confirmed`/`in_progress`),
cite le rejet HTTP 400 pour tout statut invalide. Élimination si le
candidat invente un statut absent de la liste réelle ou valide un
saut de statut sans le signaler comme une anomalie à vérifier.

## Cas N2-2 — Nouveau service au catalogue

Un studio veut ajouter "Mixage express" au catalogue avec un prix et
une durée. Rédige la fiche `ServiceCreate` correspondante avec les
champs réels uniquement.

**Critères de notation :** utilise uniquement les champs réels
(`name`, `description`, `category`, `duration_hours`, `price`,
`currency`, `location`, `active`, `visible`), ne laisse pas `currency`
halluciné (le candidat doit soit préciser `"EUR"` soit expliquer que
c'est la valeur par défaut réelle). Élimination si un champ inventé
est ajouté (ex. "remise fidélité" comme champ du modèle).

## Cas N2-3 — Qui gère le planning ?

Un fondateur de petit studio demande "dois-je embaucher un
scheduler séparé du studio manager ?" Réponds avec le raisonnement du
corpus.

**Critères de notation :** explique que dans une petite/moyenne
opération, Session Management (FMS-07) et Booking & Resource Planning
(bloc FMS-16 absorbé) sont réalistement la même personne — cite que
`fms-os/fms` sert les deux depuis la même couche `/os` comme preuve —
et ne recommande un rôle séparé que pour une opération significativement
plus grande. Élimination si le candidat invente une règle de seuil
chiffrée non présente dans le corpus.
