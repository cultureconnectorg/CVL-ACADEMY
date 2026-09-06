# GMD-28 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session) :** `create_checkout`
(`server.py:489-548`), `get_payment_status` (`550-570`, y compris le
gap self-heal/ticket-issuance directement lu), `stripe_webhook`
(`657-690`), `_issue_tickets_for_session` (`574-620`), `admin_orders`
(`760-763`).

**Supposé :** un lien `GMD28.SKILL.*` réel dans le runtime de cette
Academy, et l'octroi d'un accès réel au compte Stripe — aucun des deux
n'existe.

## Dépendances

- `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md` (cite déjà GMD-28 comme
  meilleur précédent de paiement réel de tout l'écosystème CVLN audité,
  y compris pour `WAL-08`), `EVIDENCE_ARCHITECTURE.md`,
  `ECONOMIC_MODEL.md`, GMD-21/24/27 (prérequis).

## Ce qu'une future intégration exigerait

1. Entrée `GMD28` dans le registre de certification.
2. Surface candidat réelle (idéalement avec un compte Stripe test
   dédié).
3. Décision Founder séparée sur le cycle de renouvellement sensible
   (recommandé 12 mois, non tranché ici).

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD28`. `FULLY_COMPLETE` non déclaré.
