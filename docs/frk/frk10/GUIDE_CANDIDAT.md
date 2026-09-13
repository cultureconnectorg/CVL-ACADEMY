# FRK-10 — Guide Candidat

## Avant de commencer

Aucun prérequis. Cette formation enseigne un cadre réglementaire UE
réel (eIDAS2/EUDI Wallet/SD-JWT) — jamais comme un standard mondial,
et jamais comme une capacité que CVLN implémente aujourd'hui. Aucune
certification n'est délivrée tant que `NEEDS_EXPERT_REVIEW` reste
ouvert : tu passes une vérification de littératie, pas un examen
certifiant.

## Ce que tu dois savoir faire

Expliquer, avec la réserve de juridiction systématique :

- Le cadre eIDAS2 (Règlement (UE) 2024/1183) et l'obligation pour
  chaque État membre de fournir un EUDI Wallet.
- Le modèle de données du wallet (PID, EAA, QEAA) et le fait que le
  wallet est contrôlé par le détenteur, pas centralisé.
- Le modèle de présentation par consentement (le relying party ne
  reçoit que ce qui est demandé et consenti).
- Le fonctionnement technique de SD-JWT (disclosures hachées,
  key-binding JWT, divulgation sélective) et de SD-JWT VC.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 11 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Généraliser ce cadre hors UE sans réserve — c'est l'unique discipline
réellement vérifiée aujourd'hui, et l'élimination est automatique dès
la vérification de littératie. Second piège : décrire une divulgation
qui partage la credential entière au lieu d'une disclosure sélective.

## Règle absolue

Aucune certification n'existe pour cette formation avant révision
d'expert — ne présente jamais ta réussite à la vérification de
littératie comme une certification FRK-10.
