# FRK-09 — Banque N1

## Cycle de vie (M1)

1. Quels 3 processus réels de cycle de vie d'identité sont enseignés ?
   (Émission, rotation, révocation)
2. Que se passe-t-il à l'étape d'émission ? (Création initiale de la
   credential, liaison au sujet)
3. Pourquoi rotationner une clé/credential ? (Remplacement planifié ou
   après compromission suspectée, sans casser les relations de
   confiance existantes)
4. Comment un relying party apprend-il qu'une credential est révoquée ?
   (Liste de révocation, registre de statut, ou credentials à courte
   durée de vie)
5. `mint_frek_id()` a-t-il un mécanisme de rotation/révocation ? (Non
   — aucun des trois mécanismes n'existe)

## Récupération & réconciliation (M2)

6. Cite un schéma de récupération réel. (Récupération sociale/par
   garants, ou récupération custodiale)
7. Pourquoi la conception de la récupération est-elle un compromis de
   sécurité ? (Une récupération plus facile élargit généralement la
   surface d'attaque pour une prise de contrôle de compte)
8. Que signifie la réconciliation dans ce contexte ? (Détecter et
   résoudre un désaccord entre deux systèmes sur le statut actuel
   d'une identité — p. ex. un système fait encore confiance à une
   credential révoquée)

## Frontière et discipline de gap (M3)

9. FRK-09 est spécialisation de quelle formation ? (FRK-08)
10. Un candidat peut-il affirmer qu'un FREK-ID peut être révoqué
    aujourd'hui ? (Non — élimination si affirmé)
11. Un candidat peut-il affirmer qu'un FREK-ID peut être rotationné ou
    récupéré aujourd'hui ? (Non — élimination si affirmé, pour chacun
    des trois mécanismes séparément)
