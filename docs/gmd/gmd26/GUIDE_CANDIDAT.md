# GMD-26 — Guide Candidat

## Avant de commencer

GMD-21 requis.

## Ce que tu dois savoir faire

Lire un vrai enregistrement fan (`ticketing_service.py:24-70`),
répondre correctement aux questions qu'il peut answer (VIP, ville) et
refuser honnêtement celles qu'il ne peut pas (dépense moyenne, taux
d'ouverture email) — sans jamais inventer un chiffre.

## Comment réviser

1. Lis `ticketing_service.py` lignes 24-70 toi-même.
2. Fais les 9 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`, en particulier N2-3.

## Piège le plus fréquent

Croire que le fan record ne contient que des données brutes — il
contient en réalité des champs dérivés réels (`segments`,
`total_events`, `cities`), calculés à chaque achat. Le piège inverse
existe aussi : croire qu'il contient plus qu'il ne contient réellement
(dépense, ouverture email).

## Règle absolue

N'invente jamais un chiffre ou un champ absent du schéma réel —
élimination automatique.
