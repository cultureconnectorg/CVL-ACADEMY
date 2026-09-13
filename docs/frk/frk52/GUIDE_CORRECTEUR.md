# FRK-52 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier le
versionnage et la gestion d'erreur attendus, et le grounding réel de
`frek_core.py`.

## Ce que tu vérifies en priorité

1. Le design d'API propose-t-il une stratégie de versionnage réelle ?
2. La gestion d'erreur est-elle cohérente (codes sémantiques + corps
   structuré) ?
3. Affirme-t-il, explicitement ou implicitement, que `frek_core.py`
   expose une API publique ? Applique la règle éliminatoire sans
   exception si oui.

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle du design d'API —
seulement sur la pratique réelle (versionnage, gestion d'erreur) et
sur l'absence d'invention concernant `frek_core.py`.
