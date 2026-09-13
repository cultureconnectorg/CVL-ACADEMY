# FRK-73 — Guide Candidat

## Avant de commencer

Prérequis : FRK-71. Cette formation est **formative uniquement**.
Aucune certification n'est délivrée : le contenu attend une revue par
un cryptographe réel, nommé.

## Ce que tu dois savoir faire (à titre formatif)

Tracer fidèlement la chaîne de dérivation réelle
`PUF → HKDF → DRK → AK/FK/CK` et le schéma de signature ECDSA P-256
`r||s`, et distinguer précisément conformité fonctionnelle (tests
passants) et sécurité cryptographique prouvée.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 8 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Inventer une étape de dérivation non présente dans le code réel.
Second piège : présenter des tests fonctionnels passants (FRK-75)
comme une preuve de sécurité cryptographique.

## Règle absolue

Ne jamais présenter ce code comme « audité » ou « sécurisé » sans
réserve.
