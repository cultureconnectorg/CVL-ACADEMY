# FRK-26 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un graphe de provenance

Le candidat modélise la chaîne de dérivation d'un objet culturel
(source → dérivé → dérivé du dérivé) en graphe orienté acyclique
horodaté.

**Critère éliminatoire :** produire un graphe cyclique pour une chaîne
de dérivation.

**Critères de notation :** chaque arête de dérivation porte un
horodatage ; le graphe reste acyclique sur l'ensemble de la chaîne.

## Cas 2 — Discipline CVLN-gap

Le candidat doit expliquer pourquoi affirmer qu'un système CVLN
maintient « un graphe de provenance » serait faux aujourd'hui.

**Critère éliminatoire :** affirmer qu'un système CVLN implémente un
graphe de provenance réel.

## Cas 3 — Relation non-acyclique dans le même graphe

Le graphe modélisé au Cas 1 doit aussi représenter les relations
"collaborateur de" entre les créateurs des objets. Explique si cette
relation doit respecter la même contrainte d'acyclicité que les arêtes
de dérivation.

**Critères de notation :** identifie que non — "collaborateur de" n'a
pas de sens de dérivation temporelle, elle peut être symétrique ou
former un cycle (A collabore avec B qui collabore avec C qui collabore
avec A) sans incohérence logique ; seules les arêtes de dérivation
portent l'exigence d'acyclicité. Élimination si le candidat applique
la même contrainte d'acyclicité à toutes les relations sans
distinction.
