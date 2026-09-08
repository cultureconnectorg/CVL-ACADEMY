# CVE-07 — Banque N2 (cas appliqués)

## Cas N2-1 — Axe supplémentaire proposé

Un manager demande d'ajouter un 7e axe "popularité" au Nebula Score.
Corrige.

**Critères de notation:** cite les 6 axes réels et exhaustifs du
document (`language, territory, diaspora, generation, style,
collaboration`) — un 7e axe serait un changement réel de méthodologie,
non couvert par le spec figé, jamais à valider silencieusement.
Élimination si le candidat valide l'ajout sans le signaler comme un
changement de spécification.

## Cas N2-2 — Valeur intermédiaire de novelty inventée

Un stagiaire propose `ν_k(i,c) = 0.6` pour une catégorie "à moitié
nouvelle." Corrige.

**Critères de notation:** cite les 2 seuls points de calibration
nommés (1 = première pénétration, 0.3 = déjà atteinte) et précise
qu'aucune valeur intermédiaire n'est définie par le document — une
valeur comme 0.6 serait une invention, pas une lecture du spec.
Élimination si le candidat affirme que 0.6 est une valeur documentée.

## Cas N2-3 — Confusion entropie haute/basse

Un collègue affirme qu'une entropie `H_k` élevée signifie une
concentration forte sur peu de catégories. Corrige.

**Critères de notation:** cite la formule réelle et son interprétation
correcte — une entropie élevée signifie une répartition large sur de
nombreuses catégories (c'est l'inverse de la concentration).
Élimination si le candidat maintient l'interprétation inversée.
