# KLT-08 — Évaluations N2 (décision / application)

```
Situations dégradées, arbitrage requis. Couvre C2, C3, C5, C6, C7.
```

## E-N2-01 — Grille d'audit réseau construite sans héritage

**Situation** : un premier brouillon de grille d'audit réseau ignore la
méthode déjà validée en `KLT-04`/M13 et repart de zéro avec des critères
génériques.

**Décision attendue** : reprendre la grille à partir de la méthode
`KLT-04`/M13, en l'étendant explicitement au multi-opérateurs.
**Compétences testées** : C2.
**Barème** : identification de l'absence d'héritage (40%, éliminatoire
si absent), reconstruction ancrée sur `KLT-04`/M13 (40%), extension
réseau justifiée (20%).

## E-N2-02 — Tentation de lisser une disparité

**Situation** : le point ouvert sur le cumul de rôles de la trésorière
de Mémoire Vive (`KLT-04`/M02) est tentant à omettre dans la vue
consolidée, pour ne pas "plomber" une conclusion globalement positive.

**Décision attendue** : maintenir le point dans la vue consolidée,
malgré la tentation de le lisser.
**Compétences testées** : C3.
**Barème** : maintien du point dans la vue (50%, éliminatoire si
absent), formulation équilibrée (pas accusatrice) (30%), cohérence
globale de la vue préservée (20%).

## E-N2-03 — Support de formation trop générique

**Situation** : un premier support de formation opérateurs se limite à
rappeler l'obligation d'accessibilité sans expliquer comment la
documenter concrètement.

**Décision attendue** : réviser le support pour y inclure une méthode
concrète et un exemple applicable.
**Compétences testées** : C5.
**Barème** : identification de l'insuffisance (40%, éliminatoire si
absent), ajout d'une méthode concrète (40%), exemple applicable inclus
(20%).

## E-N2-04 — Recommandation formulée comme une instruction

**Situation** : le brouillon de recommandations impose directement "les
opérateurs doivent documenter systématiquement" plutôt que de le
recommander à la gouvernance réseau.

**Décision attendue** : reformuler en recommandation adressée à la
gouvernance réseau, pas en instruction directe aux opérateurs.
**Compétences testées** : C6.
**Barème** : identification du dépassement de rôle (50%, éliminatoire si
absent), reformulation correcte (30%), adressage au bon niveau (20%).

## E-N2-05 — Tentation de corriger directement une non-conformité

**Situation** : face à la non-conformité de documentation PMR, un membre
de l'équipe propose de contacter directement chaque opérateur pour
"régler ça vite" sans passer par une escalade formelle.

**Décision attendue** : refuser la correction directe, documenter et
escalader au bon niveau de gouvernance réseau.
**Compétences testées** : C7.
**Barème** : refus de la correction directe (50%, éliminatoire si
absent), documentation complète produite (30%), escalade au bon niveau
(20%).

---

**Couverture** : 5 évaluations, couvrant C2, C3, C5, C6, C7. C1 reste
testée au niveau N1 uniquement (compétence conceptuelle). C4 hors
périmètre (`BLOCKED`).
