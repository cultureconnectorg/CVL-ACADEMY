# CVE-10 — Guide Candidat

## Avant de commencer

Prérequis : `CVE-09` (la formule elle-même, pas re-dérivée ici).

## Ce que tu dois savoir faire

Expliquer ce que le spec définit (distribution de `MD_c`) vs. laisse
ouvert (valeur € réelle de `MD_c`), et démontrer que l'allocation est
à somme nulle au sein d'un cycle (C1).

## Comment réviser

1. Relis `KORA_CVE_Specification_Mathematique_v1.0.md` §5 et §6 C1
   (déjà couvert en CVE-09).
2. Fais les 5 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Re-dériver la formule UVC en détail au lieu d'y renvoyer — CVE-10
apporte l'angle politique de revenu, pas une seconde dérivation
mathématique.

## Règle absolue

N'invente jamais un mécanisme de fixation de la valeur € de `MD_c`, et
ne valide jamais une proposition qui violerait la somme nulle du
cycle — élimination automatique.
