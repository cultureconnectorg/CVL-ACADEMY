# CVE-01 — Banque N2 (cas appliqués)

## Cas N2-1 — Confiance interne invoquée contre H0

Un responsable affirme qu'une mesure interne, non reproductible par un
tiers à partir des logs bruts, doit quand même compter "parce que
l'équipe la valide en interne." Corrige.

**Critères de notation:** cite H0 exactement (reproductibilité par un
tiers à partir des logs bruts d'écoute/transaction) et le principe de
clôture — toute quantité qui ne satisfait pas H0 est exclue du modèle,
sans exception pour une validation interne non vérifiable. Élimination
si le candidat accepte la mesure sur la seule base de la confiance
interne.

## Cas N2-2 — Comptage erroné des couches

Un stagiaire présente un diagramme "5 couches" en comptant la
normalisation/saturation (§2) comme une couche séparée entre Mesure et
Compréhension. Corrige.

**Critères de notation:** cite la structure réelle — 4 couches
nommées (Mesure §1 → Compréhension §3 → Prévision §4 → Allocation
§5), §2 étant une transformation appliquée aux composantes de la
Couche 1 avant leur agrégation en Couche 2 (pas une couche séparée), et
§6 (Loi Fondamentale) un programme d'optimisation qui gouverne
l'ensemble sans être lui-même une 5e couche. Élimination si le
candidat valide le comptage à 5 couches sans correction.

## Cas N2-3 — Chantier 2 présenté comme déjà réalisé

Un collègue affirme que les poids indicatifs du Trust Score
(0.4/0.3/0.2/0.1, cf. CVE-02) ont déjà été validés empiriquement par
simulation. Corrige.

**Critères de notation:** cite le statut réel du document ("chantier 1
de la feuille de route de preuve," consolidant v1.0→v1.4, chantier 2 —
simulation — non réalisé) et précise que ces valeurs sont qualifiées
d'"indicative initial calibration values," jamais de valeurs validées.
Élimination si le candidat affirme qu'une simulation a eu lieu.
