# CVE-08 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Repo truth (§3.3, §6) à côté de la copie.

## Ce que tu vérifies en priorité

1. Le candidat cite-t-il exactement les 2 apparitions réelles de VCF ?
2. Confirme-t-il l'absence d'équation définissante par une
   vérification explicite ?
3. Labellise-t-il toute hypothèse de travail (`VCF ≈ CVI`) comme
   `HYPOTHESIS, NOT SPEC` ? Note en conséquence si le label manque
   (pas éliminatoire en soi si le contenu reste correct).
4. Présente-t-il une équation VCF inventée comme spec réelle ?
   Applique la règle éliminatoire sans exception si oui.

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition de "ce que VCF devrait être" —
seulement sur le texte réel du document et une hypothèse correctement
labellisée.
