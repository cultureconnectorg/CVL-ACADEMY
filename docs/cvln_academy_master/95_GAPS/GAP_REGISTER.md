# CVLN Academy Master — Gap Register

```
SOURCE: raw/Coverage_Gaps.csv (6 rows, from the spreadsheet itself) +
gaps derived from REPO_TRUTH_AUDIT.md. Each gap gets an explicit
ACTION so the next wave knows where to start.
```

## Gaps declared by the source spreadsheet itself (preserved verbatim)

| Domaine | Écart / dépendance | Action | Règle |
|---|---|---|---|
| CVLN Hospitality | HOS-31→50 non récupérés dans ce tour | `RECONCILE` | 50 formations comptées précédemment, 30 récupérées précisément — ne pas inventer les 20 manquants |
| KORA | 15 formations canoniques KOR-01→15 | `SEPARATE_WORKSTREAM` | Le présent classe surtout les rôles opérateurs/cross ; KOR-01→15 doit rester synchronisé avec le repo (`docs/kor/`) — **confirmé synchronisé, corpus déjà livré** |
| Kiltikonet | KLT-01→08 existants + KLT-09→20 candidats | `RECONCILE` | Préserver le corpus canonique existant, ajouter les candidats sans écraser — **confirmé : KLT-01→08 intacts, KLT-09→20 restent candidats non construits** |
| FMS | FMS-01→06 existants + FMS-07→18 candidats | `RECONCILE` — **DONE (v2)**, voir `20_EXTERNAL/FMS_07_18_RECONCILIATION.md` | Préserver les formations canoniques déjà construites — **confirmé intactes**. Réconciliation à deux dimensions (couverture curriculaire × distinction professionnelle, correction Founder appliquée — `CONTENT_OVERLAP != PROFESSIONAL_DUPLICATE`) des 12 candidats : **aucun rejeté**. FMS-08/09 deviennent des parcours de spécialisation ancrés sur FMS-03 (Recording Engineering, Mixing & Mastering — professions réelles distinctes malgré une couverture curriculaire complète/substantielle) ; FMS-14/16 fusionnent comme blocs de compétence dans FMS-07 ; FMS-17 fusionne dans FMS-18 ; FMS-11 devient un parcours hybride qui réutilise FMS-04 par référence. Résultat : 9 formations/parcours couvrant fidèlement les 12 candidats. |
| Blockchain internal | BCI-31→40 | `VERIFY_IMPLEMENTATION` | Candidats tant que l'implémentation réelle n'est pas vérifiée — **vérifié : aucune implémentation trouvée, reste candidat** |
| Legal/fiscal | Group / Foundation / Tokenization | `EXPERT_REVIEW` | Enseignement par juridiction avec spécialistes, aucune recette universelle |

## Gaps découverts pendant cet audit (nouveaux, non présents dans la source)

| # | Écart | Action | Priorité |
|---|---|---|---|
| G1 | **Good Mood / DJ Sayd** : la cartographie compte 94 lignes réparties sur deux domaines séparés, mais un seul repo réel (`gmfest972/goodmooddjsayd`) porte les deux. | `RECONCILE` avant tout référentiel — proposer une frontière marque (DJ Sayd = artiste) vs plateforme (Good Mood = OS événementiel), jamais deux jeux de compétences opérateur dupliqués pour le même backend. | **P0** |
| G2 | **Wallet interne (WAL-19→28)** décrit un système financier riche (holds, double-entry, cartes, marketplace/escrow, kill-switch) très au-delà du ledger simple réellement implémenté (`backend/wallet/`). | `VERIFY_IMPLEMENTATION` avant tout référentiel WAL-20/22/23/24/25/26/27/28 — construire d'abord sur ce qui existe (WAL-19 Operator, WAL-21 Ledger Operator), marquer le reste `KORA_PRODUCT_GAP`-équivalent. | P1 |
| G3 | **LabelOS** (37 lignes) n'a aucun repo identifié malgré son usage massif comme référence conceptuelle dans le code KORA (`catalog_cartography.py`, `agent_factory.py`). | `NEEDS_FOUNDER_DECISION` : soit un repo LabelOS existe et doit être nommé, soit le domaine reste `MARKET_SKILL` pur (formations métier label, sans couche interne réelle) — décision à prendre avant W6. | P1 |
| G4 | **CVLN Brain / Intelligence OS / Command Center** : la cartographie (55 lignes cumulées) suppose des capacités de raisonnement/supervision réelles ; le repo ne confirme qu'un seul point réel (l'événement `academy.certification.passed`). | `RECONCILE` : tout référentiel pour ces pôles doit citer ce point réel unique et marquer le reste `CAPABILITY_NOT_IMPLEMENTED`, comme fait pour KOR-12. | P1 |
| G5 | **FREK candidate map (FRK-01→75)** — **RECONCILIÉ** (`20_EXTERNAL/FREK_01_75_RECONCILIATION.md`), reste une carte candidate (§6 mission), non canonique. Aucun repo FREKCORE distinct n'a été nommé/cloné. | Deep audit du seul réel (`services/frek_core.py` : mint/emit_signal 8 types/issue_proof stub UUID/resolve_stade). Réconciliation à 2 dimensions : 0/75 rejeté ; 51 `NEW_EXTERNAL`, 12 `NEW_INTERNAL`, 5 `NEW_CROSS_ECOSYSTEM` (FRK-56→60), 1 spécialisation, 3 fusions (réutilisent `AUTHORIZATION_MODEL.md`/KOR-11), **6 `NEEDS_FOUNDER_DECISION`** (FRK-48,49,50,51,70 : frontière FREK-sécurité vs domaine CyberSecure séparé ; FRK-71 v3 architecture sans roadmap visible). Majorité du domaine (`.fk`, FREKANSLA, notary, watchdog, v3) reste `BLOCKED_PRODUCT_DEPENDENCY`. | **DONE** — prochaine étape : W4 sur FRK-01, FRK-58 (mieux ancrés) en premier |
| G6 | **Kiltikonet KLT-09→20** — **RECONCILIÉ** (`30_INTERNAL/KLT_09_20_RECONCILIATION.md`). 0/12 rejeté : KLT-10 fusionne avec KLT-06, KLT-09/14 débloquent des compétences déjà nommées `BLOCKED` (KLT-07/C4, WAL-X-04), KLT-13/18 deviennent spécialisation/extension de KLT-05, KLT-17 rejoint la question CyberSecure (voir G-CyberSecure ci-dessous). | 8/12 restent `BLOCKED_PRODUCT_DEPENDENCY` (aucun repo Kiltikonet séparé nommé/cloné). Chemin non bloqué dès maintenant : **KLT-13** (spécialisation sur KLT-05/C4, précédent réel Good Mood door-scan) et **KLT-18** (extension de KLT-05/C5,C7,C9). | **DONE** — reste `NEEDS_REPO_AUDIT` pour les 8 bloqués |
| G8 | **Frontière sécurité transversale** — FRK-48/49/50/51/70 (FREK) et KLT-17 (Kiltikonet) posent la même question : la sécurité applicative de chaque produit vit-elle dans le domaine séparé "CVLN CyberSecure" (42 lignes candidates), ou par produit ? | `NEEDS_FOUNDER_DECISION` **unique**, gouvernant tous les cas futurs (Wallet, LabelOS, Good Mood inclus) — ne pas trancher au cas par cas. | P1 |
| G7 | **Domaines sans aucun ancrage ni repo ni mention préalable** : CVLN CyberSecure (42), Blockchain Innovations (40), Blockchain/Tokenomics (11), Tokenomics (15), Gala Cook & Food (38), Founder/CEO (12), CVLN Group (72), Fondation Cœurvolan (74) — 304 lignes au total, plus de 1/3 de la cartographie. | `NEEDS_FOUNDER_DECISION` par domaine : soit un repo/document source existe et doit être nommé, soit ces domaines attendent une revue experte (légal/fiscal, patrimoine) avant tout référentiel. | P2 (sauf CVLN Group/Fondation : `NEEDS_EXPERT_REVIEW` explicite, jamais construit sans expert réel) |

## Séquencement recommandé pour la prochaine vague (W1-W5 par domaine)

0. **FMS-07→18** — reconciliation **FAITE (v2, occupational distinctness)** (`20_EXTERNAL/FMS_07_18_RECONCILIATION.md`). Prochaine étape directe : W4 (competency map) sur les 9 parcours confirmés, dans l'ordre FMS-07 (ombrelle, débloque 14/16) → FMS-18 (débloque 17) → FMS-08/09 (spécialisations, ancrées sur FMS-03 déjà construit) → FMS-10/11/12/13/15.
1. **G1** (Good Mood/DJ Sayd reconciliation) — bloque toute construction sur ce repo, se résout en un ticket de décision (pas de code requis).
2. **G5** (nommer le repo FREKCORE réel) — bloque toute la carte FRK-01→75 (75 lignes, le plus gros domaine).
3. **G3 + G6** (LabelOS, Kiltikonet KLT-09→20) — décisions Founder rapides, débloquent 49 lignes.
4. **G2** (Wallet interne) — construction directe possible dès maintenant sur WAL-19/WAL-21 (réel), reste marqué gap.
5. **G4** (Brain/IOS/Command Center) — réutiliser le traitement déjà validé en KOR-12 comme modèle.
6. **G7** (CyberSecure, Blockchain, Gala, Hospitality, Founder/CEO, Group, Fondation) — nécessitent tous une décision Founder ou une revue experte avant tout travail de contenu ; aucun n'est bloquant pour les autres domaines.

`NO_BLOCKED_DOMAIN_BLOCKS_ANOTHER` — conformément à la doctrine
partial-formation déjà appliquée au corpus KOR (`CORE_BUILD=COMPLETE`
possible domaine par domaine même si un autre domaine reste
`BLOCKED_DEPENDENCY`).
