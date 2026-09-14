# GMD-14 — Banque N2 (cas appliqués)

## Cas N2-1 — "Paiement réussi mais commande absente" diagnostiqué au hasard

Un opérateur reçoit une plainte et propose immédiatement de
rembourser le client "par précaution," sans vérifier de preuve.
Corrige.

**Critères de notation:** cite la démarche réelle documentée par
GMD-28 — vérifier d'abord si le webhook a été déclenché et traité
(logs webhook, dashboard Stripe) avant toute action. Élimination si le
candidat valide une action (remboursement, etc.) prise sans cette
vérification.

## Cas N2-2 — Facturation sponsor multi-devise présentée comme capacité de la plateforme

Un stagiaire affirme que "la plateforme Good Mood gère la facturation
sponsor multi-devise automatiquement." Corrige.

**Critères de notation:** rappelle que ce n'est pas une capacité
documentée dans le repo réel (GMD-28 couvre le checkout Stripe
mono-devise et la réconciliation de commande) — à enseigner comme
connaissance de marché uniquement, jamais comme capacité de la
plateforme. Élimination si le candidat maintient l'affirmation.

## Cas N2-3 — Confirmation basée sur le navigateur du client

Un collègue propose de confirmer un paiement dès que le navigateur du
client affiche "merci pour votre achat," sans attendre le webhook.
Corrige.

**Critères de notation:** explique pourquoi le webhook existe
précisément pour ne pas dépendre du navigateur du client resté ouvert
— la confirmation réelle vient de `POST /stripe/webhook`, jamais de
l'état du navigateur. Élimination si le candidat valide la
confirmation côté navigateur comme suffisante.
