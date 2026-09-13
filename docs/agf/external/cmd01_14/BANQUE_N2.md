# CMD-01→14 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un tableau de bord KPI SRE/NOC

Le candidat conçoit un tableau de bord KPI marché-général (santé de
parc, taux d'incidents, MTTR) sans référence à un système CVLN précis.

**Attendu :** un tableau de bord distinguant la sévérité des incidents,
le temps moyen de résolution, et une tendance dans le temps —
documenté comme discipline générale, sans présupposer un Command
Center CVLN opérationnel.

**Critère éliminatoire :** proposer une conception qui présuppose un
Command Center CVLN opérationnel existant.

## Cas 2 — Discipline des trois systèmes

Le candidat doit distinguer, sans les confondre : (a) la route `/os/
command-center` de `fms-os/fms` (tableau de bord d'opérations de
studio), (b) le vrai Command Center de `MetaCVLN`
(`/command-center/overview`/`/timeline`, couvert par CMD-15,
`internal/`, lecture seule, non opéré par cette Academy), (c) la
discipline SRE/ICS générique enseignée ici.

**Attendu :** trois paragraphes courts et distincts, un par système,
sans mélange de vocabulaire ni de capacité entre eux.

**Critère éliminatoire :** fusionner deux de ces trois systèmes, ou
affirmer qu'un système CVLN implémente une discipline SRE/ICS complète.

## Cas 3 — Runbook d'incident réaliste

Le candidat rédige un runbook ICS court pour un incident hypothétique
de type "panne de service" dans un contexte marché-général (jamais un
système CVLN précis) : déclenchement, rôles assignés (Incident
Commander, Operations Lead, Communications Lead, Scribe), séquence
d'escalade, et critère de clôture de l'incident.

**Attendu :** un runbook complet et cohérent avec la structure de
rôles ICS classique, sans référence à un système CVLN spécifique, et
sans jamais présenter ce runbook comme un processus déjà en place dans
cette Academy ou dans l'écosystème CVLN.

**Critère éliminatoire :** présenter ce runbook comme un processus
déjà opérationnel dans cette Academy ou tout autre système CVLN
observé.
