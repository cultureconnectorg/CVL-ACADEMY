# FRK-75 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier la
distinction implémentation testée/spécification prouvée et la
frontière avec FRK-13.

## Ce que tu vérifies en priorité

1. Le candidat affirme-t-il que les tests prouvent l'agnosticisme
   d'implémentation ? Applique la règle éliminatoire sans exception si
   oui.
2. Fusionne-t-il `reference_verifier/` et `issue_proof()` (FRK-13) ?
   Applique la règle éliminatoire sans exception si oui.
3. La structure du package (7 modules) est-elle citée correctement ?

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle de couverture de
tests — seulement sur la distinction correcte entre « implémentation
testée » et « spécification prouvée agnostique ».
