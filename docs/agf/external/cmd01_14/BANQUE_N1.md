# CMD-01→14 — Banque N1 (formatif)

Réserve `CMD0114.SKILL.*`.

1. Liste les 3 familles de disciplines réelles couvertes par ce cluster
   (fondamentaux SRE/NOC, rôles et runbooks ICS, conception de
   tableaux de bord KPI).
2. Pourquoi ces disciplines sont-elles un savoir SRE/ICS réel et
   actuel, indépendant de tout "Command Center CVLN" ?
3. `fms-os/fms` expose sa propre route `/os/command-center` (un
   tableau de bord KPI d'opérations de studio). Pourquoi ce produit
   n'a-t-il aucun rapport avec un "CVLN Command Center" au sens
   opérationnel ?
4. `MetaCVLN` expose de vraies routes `/command-center/overview` et
   `/command-center/timeline` (couvertes par CMD-15, `internal/`).
   Pourquoi ce cluster (CMD-01→14) reste-t-il indépendant de
   l'existence ou non de ces routes ?

## Corrigé indicatif

1. Fondamentaux SRE/NOC (supervision de parc, alerting), rôles et
   runbooks Incident Command System (ICS), conception de tableaux de
   bord KPI marché-général.
2. Ce sont des disciplines établies de l'industrie (SRE, ICS, NOC),
   enseignables et vérifiables indépendamment de toute implémentation
   CVLN spécifique.
3. `fms-os/fms`'s `/os/command-center` est un tableau de bord
   d'opérations de studio (`projects_active`, `bookings_upcoming`,
   etc. — voir `docs/fms/fms18/REFERENTIAL.md`) : même nom, produit
   différent, jamais confondu avec un centre de commandement
   opérationnel réel.
4. Ce cluster enseigne une discipline générique de marché ; il ne
   dépend d'aucun système CVLN précis, réel ou non — contrairement à
   CMD-15 qui certifie la lecture d'un système réel spécifique
   (`MetaCVLN`).
