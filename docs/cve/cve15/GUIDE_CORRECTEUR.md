# CVE-15 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Repo truth (§6, les 8 contraintes) à côté de
la copie.

## Ce que tu vérifies en priorité

1. Le candidat cite-t-il chacune des 8 contraintes individuellement,
   avec formulation exacte ? Note chaque contrainte séparément — 6/8
   correctes n'est pas "globalement correct."
2. Distingue-t-il correctement C4 de C5 ?
3. Valide-t-il un ajustement silencieux de `θ`, ou l'usage de `Ŷ` dans
   l'allocation ? Applique la règle éliminatoire sans exception si oui.

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition générale de gouvernance
économique — seulement sur le texte réel de la spécification.
