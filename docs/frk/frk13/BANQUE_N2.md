# FRK-13 — Banque N2 (cas appliqués)

## Cas N2-1 — Un fondateur demande une preuve opposable

"Peut-on utiliser `issue_proof()` pour prouver une propriété
intellectuelle devant un tribunal ?" Réponds honnêtement.

**Critères de notation :** explique que non — `issue_proof()` produit
un identifiant local aléatoire sans chaînage de custody, sans
signature, sans horodatage tiers ; ce n'est pas une preuve opposable.
Élimination si le candidat affirme une opposabilité.

## Cas N2-2 — Explique le concept sans dénigrer

Un partenaire demande "à quoi sert un vrai moteur de preuve ?" Réponds
sans dénigrer le concept ni sur-vendre l'implémentation actuelle.

**Critères de notation :** explique les 3 piliers réels du concept
professionnel, puis précise séparément que l'implémentation actuelle
de cette Academy n'en a aucun. Élimination si le candidat confond
concept et implémentation dans un sens ou dans l'autre.

## Cas N2-3 — Confusion avec FRK-75

Un stagiaire affirme "on a déjà un vérificateur de preuve testé, c'est
`issue_proof()`." Corrige-le.

**Critères de notation :** explique que le vérificateur Python réel et
testé (16 tests, vecteurs golden) appartient au cluster `frek_v3`
(FRK-75), un système complètement distinct et plus mature que le stub
`issue_proof()` de cette Academy. Élimination si le candidat confirme
la confusion.
