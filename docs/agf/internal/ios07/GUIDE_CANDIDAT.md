# IOS-07 — Guide Candidat

## Avant de commencer

Aucun prérequis formel, mais si tu as déjà passé FRK-54 ou BRN-15,
relis-les d'abord — les trois formations partagent le même mécanisme
technique réel (`events.py`) sous des angles différents.

## Ce que tu dois savoir faire

Décrire précisément ce qu'`events.py` (bus pub/sub en-process réel de
cette Academy) est et n'est pas : pas de communication réseau, pas de
garantie de durabilité, pas de surface webhook. Te référer à FRK-54
pour le traitement complet du même mécanisme plutôt que de le
re-décrire de zéro. Ne jamais présenter le corpus de gouvernance réel
et externe de `Cvln-ios-v.1` (21 ADRs, 7 RFCs, constitution) comme ce
que ce bus implémente ou auquel il se connecte.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 7 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.
4. Si tu as un dossier FRK-54, vérifie que tes réponses sont
   cohérentes entre les deux formations.

## Pièges les plus fréquents

1. Décrire `events.py` comme distribué ou garantissant une livraison
   persistante — élimination automatique.
2. Affirmer un câblage entre `events.py` et le corpus `Cvln-ios-v.1` —
   élimination automatique.
3. Ne jamais renvoyer explicitement à FRK-54 — plafonne ta note même
   sans commettre d'erreur éliminatoire.

## Règle absolue

`events.py` est un bus pub/sub en mémoire, interne au processus —
jamais plus. Le vrai "Intelligence OS" de l'écosystème CVLN
(`Cvln-ios-v.1`) est un corpus de gouvernance substantiel mais
self-déclaré non `DEPLOYED_RUNTIME` — cité comme preuve d'ampleur
réelle, jamais comme ce à quoi cette Academy est connectée.
