# CVE-02 — Guide Candidat

## Avant de commencer

CVE-01 requis (notation, Hypothèse H0).

## Ce que tu dois savoir faire

Écrire et expliquer exactement la formule du Trust Score et les 5
composantes brutes/dérivées de la Couche 1, et savoir que le choix de
transformation de saturation (§2.1) n'est **pas encore tranché** —
jamais le présenter comme réglé.

## Comment réviser

1. Lis `KORA_CVE_Specification_Mathematique_v1.0.md` §1 et §2.1
   toi-même.
2. Fais les 14 questions de `BANQUE_N1.md`, corrige contre le texte
   réel, pas contre ta mémoire.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Traiter `L` (composante "legacy") comme un signal brut au même titre
que `S`, `E`, `F`, `C` — c'est en réalité une composante **dérivée**
de l'intégrale CHL (§3.3).

## Règle absolue

N'invente jamais une valeur fixe de `τ_fraude`, ni un choix de
transformation de saturation présenté comme définitif — élimination
automatique.
