# CMD-01→14 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un tableau de bord KPI SRE/NOC

Le candidat conçoit un tableau de bord KPI marché-général (santé de
parc, taux d'incidents, MTTR) sans référence à un système CVLN précis.

**Critère éliminatoire :** proposer une conception qui présuppose un
Command Center CVLN opérationnel existant.

## Cas 2 — Discipline des trois systèmes

Le candidat doit distinguer, sans les confondre : (a) la route `/os/
command-center` de `fms-os/fms` (tableau de bord d'opérations de
studio), (b) le vrai Command Center de `MetaCVLN`
(`/command-center/overview`/`/timeline`, couvert par CMD-15,
`internal/`, lecture seule, non opéré par cette Academy), (c) la
discipline SRE/ICS générique enseignée ici.

**Critère éliminatoire :** fusionner deux de ces trois systèmes, ou
affirmer qu'un système CVLN implémente une discipline SRE/ICS complète.
