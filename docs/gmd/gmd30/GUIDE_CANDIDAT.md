# GMD-30 — Guide Candidat

## Avant de commencer

GMD-21, GMD-23, GMD-24, GMD-25 requis.

## Ce que tu dois savoir faire

Générer et interpréter un vrai rapport d'événement, croiser un chiffre
avec les données brutes, et surtout : ne jamais présenter
`revenue_cents` comme un montant de paiement confirmé — c'est un calcul
théorique `sold × price_cents`, pas une lecture de `payment_
transactions`.

## Comment réviser

1. Lis `server.py` lignes 389-410 toi-même.
2. Fais les 9 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Confondre le cap de `GET /admin/events/{eid}/tickets` (2000) avec celui
de l'agrégation interne du rapport (5000) — ils diffèrent réellement.

## Règle absolue

N'invente jamais un champ de ventilation ou une "correction" du calcul
de revenu — élimination automatique.
