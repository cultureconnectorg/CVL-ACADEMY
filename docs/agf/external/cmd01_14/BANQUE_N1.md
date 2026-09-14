# CMD-01→14 — Banque N1 (formatif)

Réserve `CMD0114.SKILL.SRE_NOC_ICS_DISCIPLINES.L1`.

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
5. Quelle est la différence entre un rôle "Incident Commander" et un
   rôle "Operations Lead" dans un ICS classique ? Pourquoi cette
   distinction de rôles importe-t-elle en situation réelle
   d'incident ?
6. Un candidat propose un tableau de bord KPI qui affiche uniquement le
   nombre total de tickets ouverts, sans distinction de gravité ni de
   tendance. Qu'est-ce qui cloche dans cette conception, du point de
   vue de la discipline enseignée ici ?
7. Pourquoi confondre `fms-os/fms`'s `/os/command-center` avec le
   Command Center réel de `MetaCVLN` est-il qualifié de
   `CROSS_DOMAIN_CONTAMINATION` plutôt qu'une simple erreur mineure de
   vocabulaire ?

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
5. L'Incident Commander a l'autorité de décision globale et coordonne
   la communication et l'escalade ; l'Operations Lead dirige
   spécifiquement les actions techniques de résolution. Séparer ces
   rôles évite qu'une seule personne soit submergée par deux
   responsabilités cognitives distinctes en pleine crise.
6. Un compteur brut sans distinction de gravité ni de tendance ne
   permet pas de prioriser — un tableau de bord KPI utile doit
   distinguer la sévérité, le temps moyen de résolution (MTTR), et
   l'évolution dans le temps, sinon c'est une métrique de vanité qui ne
   prédit rien d'utile opérationnellement.
7. Parce que ce n'est pas une simple maladresse de vocabulaire : c'est
   attribuer à un produit réel (`fms-os/fms`) des capacités
   opérationnelles d'un tout autre système réel (`MetaCVLN`) simplement
   parce qu'ils partagent un nom — ce type de confusion, si répété,
   pollue systématiquement la compréhension de chaque système par
   contamination croisée involontaire.
