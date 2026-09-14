# FRK-07 — Guide Candidat

## Avant de commencer

Aucun prérequis. Cette formation enseigne l'IAM (Identity & Access
Management) marché-général réel, jamais une capacité CVLN — sache dès
le départ que `mint_frek_id()` (FRK-06) n'est pas un IdP.

## Ce que tu dois savoir faire

Concevoir une architecture IAM réelle (rôle IdP, modèle OAuth2/OIDC,
cycle de vie des credentials, modèle de session/token) — et articuler
précisément la frontière entre cette discipline et le minting
séquentiel étroit de FRK-06.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 11 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Affirmer, même partiellement, que `frek_core.py` implémente ou se
rapproche d'un IdP, d'OAuth2 ou d'OIDC — ce n'est pas le cas, et
l'élimination est automatique. Second piège : confondre authentification
et autorisation.

## Règle absolue

N'affirme jamais qu'un système CVLN implémente une architecture IAM
complète — `mint_frek_id()` reste un minting séquentiel étroit, pas un
IdP. Aucune confusion FRK-06/FRK-07.
