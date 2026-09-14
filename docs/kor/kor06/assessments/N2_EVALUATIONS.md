# KOR-06 — Évaluations N2

## E-N2-01 (C3) — Anomalie hors échantillon
**Situation** : un podcast non prioritaire (rarement vérifié) devient
indisponible sans être détecté par la routine établie.
**Décision attendue** : reconnaître la limite de la routine
d'échantillonnage et l'ajuster, sans prétendre qu'elle était
infaillible.
**Barème** : reconnaissance de la limite (50%), ajustement proposé
(50%).

## E-N2-02 (C5) — Pression pour un SLA ambitieux
**Situation** : la direction d'Anba Tonèl Host demande un SLA à 99,99%
pour attirer de gros créateurs, sans investissement infrastructurel
supplémentaire.
**Décision attendue** : refuser ou alerter sur l'écart entre
l'engagement demandé et les moyens réels, plutôt que de promettre un
seuil intenable.
**Barème** : alerte documentée (60%, éliminatoire si un SLA intenable
est validé sans réserve), proposition alternative réaliste (40%).

## E-N2-03 (C6) — Cause ambiguë de l'incident
**Situation** : au début de l'incident, la cause n'est pas évidente
(pic de trafic ou panne serveur ?).
**Décision attendue** : communiquer un état provisoire honnête plutôt
que d'attendre d'avoir toutes les réponses pour informer le créateur.
**Barème** : communication provisoire honnête (50%), diagnostic
poursuivi en parallèle (50%).

## E-N2-04 (C7) — Fatigue d'alerte constatée
**Situation** : après la mise en place du monitoring, l'équipe
commence à ignorer les alertes, trop nombreuses.
**Décision attendue** : ajuster les seuils plutôt que blâmer l'équipe
pour avoir ignoré les alertes.
**Barème** : diagnostic de la fatigue d'alerte (50%), ajustement des
seuils documenté (50%).
