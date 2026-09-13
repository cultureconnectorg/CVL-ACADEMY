# FRK-52 — Guide Candidat

## Avant de commencer

Aucun prérequis. Apprends l'ingénierie d'API marché-générale (REST,
versionnage, gestion d'erreur). Règle absolue : `frek_core.py` n'expose
aucune API publique aujourd'hui — client Python interne uniquement
(`FrekCoreClient`).

## Ce que tu dois savoir faire

Concevoir une API REST avec une stratégie de versionnage explicite et
une gestion d'erreur cohérente (codes HTTP sémantiques + corps
structuré), et confirmer précisément la nature interne de
`frek_core.py`.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 7 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Affirmer que `frek_core.py` expose une API publique ou REST —
élimination automatique. Second piège : proposer une API sans
stratégie de versionnage.

## Règle absolue

`frek_core.py` n'expose aucune API publique aujourd'hui.
