# GMD-14 — Guide Candidat

## Avant de commencer

Aucun prérequis.

## Ce que tu dois savoir faire

Tracer la séquence réelle checkout → Stripe → webhook → commande
(citant GMD-28), diagnostiquer une panne de paiement sur preuve
réelle, et distinguer les pratiques de marché (multi-devise,
facturation sponsor) des capacités réelles de la plateforme.

## Comment réviser

1. Lis `docs/gmd/gmd28/REFERENTIAL.md` toi-même — c'est l'exemple
   travaillé réel de cette formation.
2. Fais les 6 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Confirmer un paiement sur la base de ce qu'affiche le navigateur du
client, au lieu d'attendre la confirmation réelle du webhook.

## Règle absolue

Ne prends jamais une décision financière (remboursement, etc.) sans
preuve réelle vérifiée, et ne présente jamais une pratique de
marché-général comme une capacité réelle de la plateforme —
élimination automatique.
