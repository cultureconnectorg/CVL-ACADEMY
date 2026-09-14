# CVE-15 — Banque N2 (cas appliqués)

## Cas N2-1 — Ajustement silencieux de paramètre

Un ingénieur ajuste `τ_fraude` en production sans documentation ni
annonce, "parce que c'est un petit changement." Corrige.

**Critères de notation:** cite C7 exactement ("∀ change in θ,
published + justified + archived") — aucun changement de `θ`, même
mineur, n'est exempté de cette discipline. Élimination si le candidat
valide l'ajustement silencieux.

## Cas N2-2 — Prévision utilisée pour l'allocation

Un manager propose d'utiliser `Ŷ_i(t+Δ)` (la classification
prospective de la Couche 3) pour ajuster directement l'allocation
`UVC_i,c` d'un cycle, "pour anticiper les tendances." Corrige.

**Critères de notation:** cite C8 et §4 (`Ŷ_i(t+Δ) ∉
inputs(Allocation)` / `∉ inputs(UVC)`) — c'est une séparation
structurelle explicite, jamais une simple recommandation. Élimination
si le candidat valide l'utilisation de `Ŷ` dans l'allocation.

## Cas N2-3 — Confusion entre deux contraintes

Un stagiaire confond C4 (plancher de diversité culturelle) avec C5
(neutralité culturelle). Corrige.

**Critères de notation:** cite précisément chaque contrainte avec sa
formulation exacte — C4 (`H_diversity(catalog,c) ≥ diversity_floor`,
diversité du catalogue) et C5 (égalité d'UVC espéré à CVI égal,
indépendamment de la culture, une garantie individuelle) sont
distinctes. Élimination si les deux restent confondues après
correction.
