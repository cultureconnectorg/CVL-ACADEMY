# FRK-56 — Banque N2 (cas appliqués)

## Cas N2-1 — Un nouveau domaine demande la même explication

Le domaine Good Mood a besoin d'expliquer sa propre frontière FREK.
Dois-tu re-dériver l'explication depuis zéro ?

**Critères de notation :** explique qu'il faut réutiliser le cas
FREK×KORA déjà documenté (ce cas est le "worked case" de référence),
en l'adaptant au domaine concerné, jamais en le re-dérivant depuis les
principes de base. Élimination si le candidat re-dérive tout depuis
zéro sans citer ce précédent.

## Cas N2-2 — Un jury demande pourquoi `FALSE` partout

"Pourquoi tous les KOR sont à `READY_FOR_FREK_PROOF = FALSE`, c'est un
oubli ?" Réponds avec les faits réels.

**Critères de notation :** explique que ce n'est pas un oubli — c'est
la vérité honnête : le stack `frek_signal` est utilisé mais aucune
ancre externe n'existe. Marquer `TRUE` serait une affirmation non
vérifiée. Élimination si le candidat affirme que c'est une erreur à
corriger en passant `TRUE`.

## Cas N2-3 — Confusion d'intégration

Un stagiaire affirme "le header `FREK_PROOF_MAPPING` prouve que KORA
et FREK sont techniquement intégrés." Corrige-le.

**Critères de notation :** explique que le header documente une
intention de signal (quel `VALID_SIGNALS` ce module référence), pas
une intégration technique bidirectionnelle vérifiée. Élimination si le
candidat confirme l'affirmation erronée.
