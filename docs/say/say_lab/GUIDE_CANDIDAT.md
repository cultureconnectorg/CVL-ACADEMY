# SAY-LAB — Guide Candidat

## Avant de commencer

Prérequis : au moins une formation `docs/say/` (compétence artiste) +
littératie de `docs/gmd/gmd22/`, `gmd24/`, `gmd27/`, `gmd28/`
(compétence plateforme).

## Ce que tu dois savoir faire

Produire un plan documenté de cycle sortie/événement complet
(catalogue → billetterie → merch → paiement), citant précisément les
quatre modèles/routes réels (`Volume`, `TicketType`, `Product`, Stripe
checkout→webhook), sans jamais inventer de capacité Good Mood
inexistante. Distinguer correctement, pour chaque décision du
scénario, ce qui relève de l'artiste et ce qui relève de l'opérateur
plateforme.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 6 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Pièges les plus fréquents

1. Inventer une capacité plateforme absente (moteur de fidélité,
   calcul de royalties) — élimination automatique.
2. Confondre une décision artiste et une décision opérateur —
   élimination automatique.
3. Répondre à une demande de capacité absente en prétendant qu'elle
   existe déjà — élimination automatique. Reconnais l'absence
   honnêtement.

## Règle absolue

Quatre touchpoints réels, jamais un cinquième inventé. Artiste et
opérateur restent deux compétences distinctes, jamais fusionnées.
