# FRK-08 — Guide Candidat

## Avant de commencer

Aucun prérequis. Cette formation enseigne les standards W3C DID/VC
réels, jamais une capacité CVLN — sache dès le départ que
`mint_frek_id()` n'est pas un DID.

## Ce que tu dois savoir faire

Expliquer le modèle de document DID (identifiant, méthodes de
vérification, points de service) et le modèle Verifiable Credentials
(issuer/holder/verifier, émission vs. présentation, divulgation
sélective) — et articuler précisément le gap entre ces standards et
l'implémentation CVLN actuelle.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 11 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Affirmer, même partiellement, que `frek_core.py` implémente ou se
rapproche d'un schéma DID — ce n'est pas le cas, et l'élimination est
automatique. Second piège : confondre émission et présentation d'une
credential dans le modèle VC.

## Règle absolue

N'affirme jamais de conformité W3C DID/VC inexistante pour un système
CVLN — élimination automatique.
