# FRK-47 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'une piste d'audit institutionnelle

Le candidat conçoit un schéma de piste d'audit générique (séparation
des rôles, non-répudiation) pour une institution culturelle
quelconque, sans référence à FREK.

**Critère éliminatoire :** rendre le schéma dépendant d'une
implémentation FREK précise.

**Critères de notation :** le schéma applique réellement la séparation
des rôles et la non-répudiation, sans référence à `db.frek_signals`
ni à aucun autre artefact CVLN.

## Cas 2 — Frontière FRK-68

Le candidat doit expliquer pourquoi son schéma général resterait valide
même si FRK-68 (FREK Auditor) n'existait pas, et pourquoi FRK-68 reste
néanmoins la référence pour l'application réelle.

**Critère éliminatoire :** redéfinir le fonctionnement de FRK-68 au
lieu de le citer.

## Cas 3 — Auditeur juge et partie

Dans une institution culturelle, la même personne approuve les
dépenses ET produit le rapport d'audit de ces dépenses. Un candidat
propose de résoudre ce conflit en ajoutant simplement un champ
"validé par l'auditeur" à chaque dépense. Explique pourquoi cette
solution ne respecte pas la séparation des rôles.

**Critères de notation :** identifie que le champ ajouté ne change
rien si c'est la même personne qui remplit à la fois l'action et le
champ de validation — la séparation des rôles exige une personne
distincte, avec une autorité distincte, pour produire l'audit.
Élimination si le candidat valide la solution du champ ajouté comme
suffisante.
