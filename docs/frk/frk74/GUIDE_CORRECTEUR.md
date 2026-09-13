# FRK-74 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier la
liste exacte des paramètres ouverts (FFT, hop size, bandes,
algorithme) et la frontière avec FRK-29/30.

## Ce que tu vérifies en priorité

1. Le candidat présente-t-il un paramètre ouvert comme verrouillé ?
   Applique la règle éliminatoire sans exception si oui.
2. La frontière avec FRK-29/30 est-elle explicite et correcte ?
3. Une proposition de compromis (fenêtre/hop size) est-elle clairement
   qualifiée de non-officielle ?

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle de traitement du
signal — seulement sur l'exactitude du statut verrouillé/ouvert
déclaré par `CE_QUI_MANQUE.md` et la frontière avec FRK-29/30.
