# FRK-20 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier le
patron store-and-forward et la nature réelle de
`is_remote_enabled()`.

## Ce que tu vérifies en priorité

1. La garantie de preuve dépend-elle, explicitement ou implicitement,
   d'un appel réseau synchrone ? Applique la règle éliminatoire sans
   exception si oui.
2. Le candidat confond-il `is_remote_enabled()` avec une vérification
   cryptographique offline ? Applique la règle éliminatoire sans
   exception si oui.
3. La vérification locale est-elle complète et autosuffisante avant
   toute synchronisation ?

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle des systèmes
offline-first — seulement sur la solidité réelle du flux local et sur
l'exactitude de la nature de `is_remote_enabled()`.
