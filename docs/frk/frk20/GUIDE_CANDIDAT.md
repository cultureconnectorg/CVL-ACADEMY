# FRK-20 — Guide Candidat

## Avant de commencer

Aucun prérequis. Apprends les patrons de conception offline-first
(marché-général), jamais confondus avec le fallback local simple de
`frek_core.py`.

## Ce que tu dois savoir faire

Concevoir un flux store-and-forward (vérification cryptographique
locale, puis synchronisation différée) où la garantie de preuve ne
dépend jamais d'un appel réseau synchrone, et confirmer précisément la
nature de `is_remote_enabled()`.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 8 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Faire dépendre la garantie de preuve d'un appel réseau synchrone —
élimination automatique. Second piège : confondre
`is_remote_enabled()` (bascule de disponibilité réseau) avec une
vérification cryptographique offline.

## Règle absolue

Aucun système CVLN ne vérifie hors-ligne aujourd'hui.
