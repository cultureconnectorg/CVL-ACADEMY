# FRK-43 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un store-and-forward

Le candidat conçoit un mécanisme de livraison persistante avec backoff
progressif, en citant le calendrier réel de Good Mood
(`[30s, 2m, 10m, 1h, 6h]`) comme exemple travaillé.

**Critère éliminatoire :** présenter l'outbox de Good Mood comme une
infrastructure FREK.

## Cas 2 — Épuisement des tentatives

Le candidat doit concevoir le mécanisme de dead-letter déclenché après
épuisement du calendrier de retry.

**Critère éliminatoire :** ne prévoir aucun mécanisme pour l'échec
persistant.

## Cas 3 — Panne longue durée du destinataire

Un service destinataire est indisponible pendant 4 heures. Le candidat
doit tracer le comportement exact du mécanisme conçu pendant cette
panne (nombre de tentatives, espacement, moment de bascule en
dead-letter le cas échéant) en s'appuyant sur le calendrier
`[30s, 2m, 10m, 1h, 6h]`.

**Critère éliminatoire :** un comportement qui continue de solliciter
le destinataire à intervalle fixe pendant toute la panne (absence de
backoff réel).
