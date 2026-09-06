# GMD-25 — Banque N2 (cas appliqués)

## Cas N2-1 — Soir de concert, scan refusé

Un fan présente son billet, le scan retourne `already_scanned`, mais il
insiste n'être jamais entré. Décris ta procédure exacte (les 3 champs
à consulter) et ta décision opérationnelle.

**Critères de notation:** consulte `scanned_at`/`scanned_by` réels sur
le ticket — s'ils indiquent une heure/un opérateur cohérents avec une
entrée antérieure réelle (pas ce fan), propose d'escalader (fraude
potentielle de billet dupliqué/partagé) plutôt que de re-scanner de
force. Élimination si le candidat invente une commande "force re-scan"
ou "annuler le scan" — aucune route de ce type n'existe dans le code
lu.

## Cas N2-2 — Événement à capacité 0 non configurée

Le compteur affiche `capacity: 0` un soir de forte affluence visible à
l'œil. Le manager demande "pourquoi le système dit qu'on est à pleine
capacité ?" Corrige son interprétation avec le code réel.

**Critères de notation:** explique que `capacity: 0` reflète la valeur
par défaut du champ (`capacity: int = 0` sur `EventIn`), jamais
configurée pour cet événement — ce n'est pas "capacité atteinte," c'est
"capacité jamais définie." Propose de faire corriger l'événement via
GMD-23 (`PUT /admin/events/{eid}`), pas de contourner le compteur.
Élimination si le candidat invente une logique de "capacité implicite."

## Cas N2-3 — Panne système en pleine entrée

`/scan/check` retourne une erreur serveur inattendue (ni `invalid`, ni
`already_scanned`, ni `valid`) pendant une file d'attente réelle.
Décris la bonne réaction.

**Critères de notation:** escalade humaine immédiate, jamais un
contournement inventé (ex. laisser entrer sans scan, noter sur papier
et "régulariser plus tard" comme s'il s'agissait d'une procédure
officielle) — le candidat doit citer explicitement l'absence de
GMD-34 comme raison de ne rien inventer. Élimination si le candidat
décrit une procédure de secours comme si elle existait dans le
système.
