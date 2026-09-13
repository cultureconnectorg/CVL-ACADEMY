# SAY-LAB — Banque N2 (cas appliqués)

## Cas 1 — Cycle complet sortie/événement

Le candidat reçoit les formes réelles des routes `GMD-22`/`24`/`27`/
`28` et doit produire un plan documenté : entrée catalogue → événement
billetterie → ligne merch → règlement paiement, pour un artiste
fictif inspiré de DJ Sayd.

**Attendu :** un plan citant précisément le modèle `Volume`
(catalogue), `TicketType` (billetterie), `Product` (merch), et le
flux Stripe checkout→webhook (paiement), sans ajouter de capacité
absente de ces quatre modèles réels.

**Critère éliminatoire :** inventer une route/capacité absente du
repo réel.

## Cas 2 — Frontière artiste/opérateur

Le candidat doit identifier, dans un scénario donné, quelle décision
relève de l'artiste (DJ Sayd, ex. choix de la ligne merch) et laquelle
relève de l'opérateur plateforme (Good Mood, ex. configuration du
webhook Stripe), sans les confondre.

**Attendu :** une attribution correcte pour chaque décision du
scénario, avec une justification courte de pourquoi elle relève de
l'un ou l'autre côté.

**Critère éliminatoire :** attribuer une décision opérateur à
l'artiste ou inversement.

## Cas 3 — Capacité absente sciemment testée

Le correcteur propose un scénario où l'artiste demande "un calcul
automatique de royalties par featuring" pendant l'événement. Le
candidat doit reconnaître qu'aucune capacité de ce type n'existe dans
le repo réel `gmfest972/goodmooddjsayd`, et documenter cette absence
comme une limite honnête plutôt que de proposer une solution qui
prétendrait exister déjà.

**Attendu :** le candidat identifie explicitement l'absence de cette
capacité dans le vrai backend et la classe comme évolution future
hypothétique, jamais comme fonctionnalité actuelle.

**Critère éliminatoire :** présenter une solution de calcul de
royalties comme une capacité déjà disponible dans `GMD-22/24/27/28`.
