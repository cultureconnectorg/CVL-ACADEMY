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
| FMS | FMS-01→06 existants + FMS-07→18 candidats | `RECONCILE` — **DONE**, voir `20_EXTERNAL/FMS_07_18_RECONCILIATION.md` | Préserver les formations canoniques déjà construites — **confirmé intactes**. Réconciliation complète des 12 candidats FMS-07→18 contre les 95 modules canoniques réels (FMS-01→06) : **5 duplications détectées et refusées** (FMS-09 ≡ FMS-03 Mixage/Mastering, FMS-11 ≡ FMS-04 Direction visuelle, FMS-14 ≡ FMS-05 Coordination, FMS-08 et FMS-17 partiellement couverts) — seuls 6-7/12 candidats restent des `NEW_GAP` légitimes (FMS-07, 10, 12, 13, 15, 16, 18). |
| Blockchain internal | BCI-31→40 | `VERIFY_IMPLEMENTATION` | Candidats tant que l'implémentation réelle n'est pas vérifiée — **vérifié : aucune implémentation trouvée, reste candidat** |
| Legal/fiscal | Group / Foundation / Tokenization | `EXPERT_REVIEW` | Enseignement par juridiction avec spécialistes, aucune recette universelle |

## Gaps découverts pendant cet audit (nouveaux, non présents dans la source)

| # | Écart | Action | Priorité |
|---|---|---|---|
| G1 | **Good Mood / DJ Sayd** : la cartographie compte 94 lignes réparties sur deux domaines séparés, mais un seul repo réel (`gmfest972/goodmooddjsayd`) porte les deux. | `RECONCILE` avant tout référentiel — proposer une frontière marque (DJ Sayd = artiste) vs plateforme (Good Mood = OS événementiel), jamais deux jeux de compétences opérateur dupliqués pour le même backend. | **P0** |
| G2 | **Wallet interne (WAL-19→28)** décrit un système financier riche (holds, double-entry, cartes, marketplace/escrow, kill-switch) très au-delà du ledger simple réellement implémenté (`backend/wallet/`). | `VERIFY_IMPLEMENTATION` avant tout référentiel WAL-20/22/23/24/25/26/27/28 — construire d'abord sur ce qui existe (WAL-19 Operator, WAL-21 Ledger Operator), marquer le reste `KORA_PRODUCT_GAP`-équivalent. | P1 |
| G3 | **LabelOS** (37 lignes) n'a aucun repo identifié malgré son usage massif comme référence conceptuelle dans le code KORA (`catalog_cartography.py`, `agent_factory.py`). | `NEEDS_FOUNDER_DECISION` : soit un repo LabelOS existe et doit être nommé, soit le domaine reste `MARKET_SKILL` pur (formations métier label, sans couche interne réelle) — décision à prendre avant W6. | P1 |
| G4 | **CVLN Brain / Intelligence OS / Command Center** : la cartographie (55 lignes cumulées) suppose des capacités de raisonnement/supervision réelles ; le repo ne confirme qu'un seul point réel (l'événement `academy.certification.passed`). | `RECONCILE` : tout référentiel pour ces pôles doit citer ce point réel unique et marquer le reste `CAPABILITY_NOT_IMPLEMENTED`, comme fait pour KOR-12. | P1 |
| G5 | **FREK candidate map (FRK-01→75)** reste, par instruction explicite du Founder (§6 mission), une carte candidate — non canonique. Aucun repo FREKCORE distinct n'a été nommé/cloné dans cette session. | `NEEDS_REPO_AUDIT` : demander l'URL du repo FREKCORE réel avant tout référentiel FRK-01→75 ; en son absence, seul `services/frek_core.py` (ce repo) fait foi. | **P0** avant toute construction FREK |
| G6 | **Kiltikonet KLT-09→20** (12 lignes) suppose un repo Kiltikonet distinct (réseau, data, identité, recherche, terrain/NFC, fintech, feed, IA/Brain, sécurité, communications, opportunités, moteur intelligent) — aucun repo Kiltikonet séparé n'a été nommé/cloné. | `NEEDS_FOUNDER_DECISION` : nommer le repo Kiltikonet réel, ou traiter KLT-09→20 comme extension conceptuelle du corpus déjà construit (`docs/klt/`) sans capacité produit nouvelle. | P1 |
| G7 | **Domaines sans aucun ancrage ni repo ni mention préalable** : CVLN CyberSecure (42), Blockchain Innovations (40), Blockchain/Tokenomics (11), Tokenomics (15), Gala Cook & Food (38), Founder/CEO (12), CVLN Group (72), Fondation Cœurvolan (74) — 304 lignes au total, plus de 1/3 de la cartographie. | `NEEDS_FOUNDER_DECISION` par domaine : soit un repo/document source existe et doit être nommé, soit ces domaines attendent une revue experte (légal/fiscal, patrimoine) avant tout référentiel. | P2 (sauf CVLN Group/Fondation : `NEEDS_EXPERT_REVIEW` explicite, jamais construit sans expert réel) |

## Séquencement recommandé pour la prochaine vague (W1-W5 par domaine)

0. **FMS-07→18** — reconciliation **FAITE** (`20_EXTERNAL/FMS_07_18_RECONCILIATION.md`). Prochaine étape directe : W4 (competency map) sur les 6-7 candidats confirmés `NEW_GAP` uniquement (FMS-07, 10, 12, 13, 15, 16, 18) — jamais sur les 5 refusés.
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
