# GMD-24 — Guide Candidat

## Avant de commencer

GMD-21, GMD-23 requis (un événement doit exister avant de vendre des
billets).

## Ce que tu dois savoir faire

Configurer un ticket type, tracer un achat de la session Stripe
jusqu'au QR, et savoir précisément quels systèmes en aval un achat
déclenche (fans, outbox FREK/Wallet) sans jamais inventer un mécanisme
absent du code.

## Comment réviser

1. Lis `server.py` lignes 115-131, 353-394, 489-560 (checkout), 574-620
   (`_issue_tickets_for_session`), 657-716 (webhook + QR).
2. Fais les 13 questions de `BANQUE_N1.md`, corrige contre le code.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Croire que la vérification `remaining < quantity` au checkout est une
réservation atomique — ce n'est qu'un contrôle préalable ; la seule
protection définitive contre la sur-vente est l'incrément `$inc`
atomique côté webhook.

## Règle absolue

N'invente jamais un verrou de réservation, une contrainte email
générique, ou un log d'audit séparé — élimination automatique.
