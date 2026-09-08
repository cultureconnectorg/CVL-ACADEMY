# CVE-03 — Banque N2 (cas appliqués)

## Cas N2-1 — Demande d'élargir la fenêtre à 30 jours

Un manager demande d'étendre la fenêtre d'attribution à 30 jours "pour
une campagne spéciale," sans passer par un processus formel. Corrige.

**Critères de notation:** cite la fenêtre réelle du document figé (14
jours) et explique qu'un changement serait une vraie modification de
paramètre, soumise à la contrainte de gouvernance C7 (§6 : "∀ change
in θ, published + justified + archived") — jamais un ajustement
silencieux. Élimination si le candidat accepte le changement sans
mentionner cette exigence.

## Cas N2-2 — Confusion entre engagement et attribution

Un stagiaire affirme que `C_i,c` inclut les likes et partages, en plus
des conversions monétaires. Corrige.

**Critères de notation:** cite la formule réelle — `C_i,c` ne compte
que la valeur en € des conversions attribuées dans la fenêtre de 14
jours ; les signaux d'engagement (durée d'écoute, ré-écoute,
ajouts en playlist) relèvent de la composante `E` (§1.2), jamais de
`C`. Élimination si le candidat confond les deux composantes.

## Cas N2-3 — Modèle "dernier clic" présumé

Un collègue demande d'expliquer "le modèle d'attribution dernier
clic" du CVE. Corrige.

**Critères de notation:** répond honnêtement qu'aucun modèle nommé
(dernier clic, linéaire, dégressif) n'existe dans le document figé —
seule la formule proportionnelle sur fenêtre de 14 jours existe.
Élimination si le candidat invente un mécanisme de modèle
d'attribution non présent dans le spec.
