# FRK-55 — Guide Candidat

## Avant de commencer

Prérequis recommandés : FRK-52, FRK-54. Apprends la synthèse de
standards transversaux (erreur, version) à travers API et événements,
en citant FRK-52/54 par référence.

## Ce que tu dois savoir faire

Concevoir une taxonomie d'erreur et un schéma de version identiques à
travers API et événements, et diagnostiquer un bug d'intégration causé
par une divergence de version.

## Comment réviser

1. Relis `docs/frk/frk52/REFERENTIAL.md` et `docs/frk/frk54/
   REFERENTIAL.md` (fondamentaux, prérequis).
2. Lis `REFERENTIAL.md` §Objectives et §Modules de cette formation.
3. Fais les 7 questions de `BANQUE_N1.md`.
4. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Proposer des schémas de version incohérents entre API et événements
sans le percevoir comme un problème — élimination automatique. Second
piège : redéfinir les fondamentaux de FRK-52 ou FRK-54 au lieu de les
citer.

## Règle absolue

Une taxonomie d'erreur et un schéma de version doivent être
identiques, quelle que soit la surface.
