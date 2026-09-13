# FRK-54 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier la
nature réelle d'`events.py` (pub/sub en-process, sans surface
webhook) et les garanties d'un contrat d'intégration versionné.

## Ce que tu vérifies en priorité

1. La copie présente-t-elle `events.py` comme une infrastructure
   webhook ou FREK ? Applique la règle éliminatoire sans exception si
   oui.
2. Le contrat d'intégration proposé est-il versionné avec une
   stratégie de compatibilité ascendante réelle ?
3. Le candidat distingue-t-il précisément bus interne et webhook
   externe, avec les garanties propres à chacun ?

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle d'architecture
événementielle — seulement sur la solidité technique réelle du
contrat proposé et l'exactitude de la frontière avec `events.py`.
