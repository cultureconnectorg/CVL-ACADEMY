# IOS-07 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier la
frontière entre le mécanisme réel (`events.py`) et le corpus de
gouvernance externe `Cvln-ios-v.1`.

## Ce que tu vérifies en priorité

1. La description d'`events.py` est-elle exacte : en-process, pub/sub,
   aucune garantie de durabilité, aucune surface webhook ? Toute
   description distribuée ou durable est éliminatoire.
2. Le candidat affirme-t-il un câblage entre `events.py` et le corpus
   `Cvln-ios-v.1` ? Éliminatoire si oui.
3. Le candidat renvoie-t-il explicitement à FRK-54 plutôt que de
   re-décrire le mécanisme de zéro ? Absence de renvoi plafonne à 2.
4. Si un dossier FRK-54 du même candidat est disponible, ses
   descriptions techniques sont-elles cohérentes entre les deux
   formations ?

## Ce que tu ne fais pas

Tu ne notes jamais sur une impression personnelle de ce qu'une
"Intelligence OS" devrait être — seulement sur l'exactitude du
mécanisme réel et le respect strict de la frontière avec
`Cvln-ios-v.1`.

## Score

Utilise la grille 0–4 et le tableau de compétences de
`ASSESSMENT_AND_RUBRIC.md`. Le seuil de passage est ≥2.5/4.
