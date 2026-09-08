# CVE-09 — Banque N2 (cas appliqués)

## Cas N2-1 — UVC présenté comme score absolu

Un stagiaire affirme qu'un `UVC_i,c` élevé signifie qu'une œuvre a
"une grande valeur culturelle intrinsèque," indépendamment des autres
œuvres du cycle. Corrige.

**Critères de notation:** cite la formule réelle
(`UVC_i,c = (CVI_i,c / Σ_j CVI_j,c) · MD_c`) — c'est une part
proportionnelle du total du cycle, jamais une valeur absolue ; la
même `CVI_i,c` produirait un `UVC_i,c` différent dans un cycle au
catalogue différent. Élimination si le candidat maintient
l'interprétation absolue.

## Cas N2-2 — Confusion entre les deux formules

Un manager demande "comment `value_UVC,c` et `UVC_i,c` sont-ils
reliés, ce sont deux calculs indépendants ?" Corrige.

**Critères de notation:** montre la dérivation algébrique — les deux
formules décrivent la même quantité (`UVC_i,c`), l'une via la part de
CVI, l'autre via le prix unitaire multiplié par le CVI de l'œuvre.
Élimination si le candidat les traite comme deux mécanismes
indépendants.

## Cas N2-3 — Violation implicite de C1

Un collègue propose une modification qui ferait que la somme des
`UVC_i,c` du cycle dépasse `MD_c`. Corrige.

**Critères de notation:** cite la contrainte C1 (§6:
`Σ_i UVC_i,c = MD_c`) comme une contrainte de budget fixe — toute
proposition qui la violerait n'est pas compatible avec le mécanisme
d'allocation réel. Élimination si le candidat valide la proposition
sans signaler la violation.
