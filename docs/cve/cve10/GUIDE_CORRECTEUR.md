# CVE-10 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Repo truth (§5, §6 C1) et `../cve09/
REFERENTIAL.md` à côté de la copie.

## Ce que tu vérifies en priorité

1. Le candidat distingue-t-il correctement "défini" (distribution) de
   "non défini" (valeur € de `MD_c`) ?
2. Démontre-t-il la somme nulle au sein d'un cycle avec une
   illustration correcte ?
3. Re-dérive-t-il la formule UVC au lieu d'y renvoyer ? Note en
   conséquence (pas éliminatoire en soi, mais pénalisant).
4. Invente-t-il un mécanisme de fixation de `MD_c`, ou valide-t-il une
   violation de C1 ? Applique la règle éliminatoire sans exception si
   oui.

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition générale de politique de revenu
— seulement sur le texte réel de la spécification.
