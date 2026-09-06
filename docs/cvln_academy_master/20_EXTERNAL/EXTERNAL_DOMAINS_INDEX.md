# CVLN Academy Master — External (MARKET) Domains Index

```
SOURCE: raw/External_Market.csv (437 rows). Full row-level data lives
there — this index gives per-domain status and repo-truth callouts
only, per rule §26 ("do not copy 800+ objects into markdown files").
```

## Domaines déjà canoniques (hors périmètre de cette cartographie)

| Domaine | Corpus canonique | Statut |
|---|---|---|
| KORA (KOR-01→15) | `docs/kor/` | `CORE_BUILD=COMPLETE`, 15/15 formations, Master Package livré |
| Kiltikonet (KLT-01→08) | `docs/klt/` | Construit (KLT-01→05 complet, KLT-06→08 partiel, blocages documentés) |
| FMS (FMS-01→06) | `docs/ACADEMY_FMS_CANONICAL_*`, `backend/fms_canonical/` | Déjà lié au runtime (`ACADEMY_FMS_CANONICAL_RUNTIME_BINDING_REPORT.md`) |

**Ne pas reconstruire ces trois corpus.** Toute extension (FMS-07→18,
KLT-09→20) est un ajout, jamais un remplacement.

## Domaines candidats à ancrage repo confirmé

| Domaine | Lignes candidates | Repo réel | Grounding |
|---|---|---|---|
| FMS-07→18 | 12 | `fms-os/fms` + corpus canonique FMS-01→06 | **Réconcilié** (`FMS_07_18_RECONCILIATION.md`) : 5/12 candidats dupliquent un métier canonique déjà construit (refusés), 6-7/12 sont des `NEW_GAP` réels |
| Good Mood + DJ Sayd | 94 | `gmfest972/goodmooddjsayd` | Catalogue/events/tickets/merch/orders/Stripe/FREK+Wallet outbox réels — **duplication de domaine à résoudre**, voir `95_GAPS/GAP_REGISTER.md` |
| CVLN Wallet (WAL-01→18) | 18 | `backend/wallet/` (CVL-ACADEMY) | Ledger simple réel ; holds/cartes/marketplace/FinOps du candidat = au-delà du réel actuel |
| LabelOS (LOS-01→14) | 14 | aucun | `CAPABILITY_NOT_IMPLEMENTED` |

## Domaines candidats sans ancrage repo (nécessitent W1 dédié ou décision Founder)

CVLN CyberSecure, Blockchain Innovations, Blockchain/Tokenomics,
Tokenomics, Gala Cook & Food, CVLN Hospitality (partiellement
rapatriée), CVLN Group, Fondation Cœurvolan — voir
`10_PORTFOLIO/RECONCILIATION_MATRIX.md` pour le détail par domaine et
`95_GAPS/GAP_REGISTER.md` pour la séquence d'action recommandée.

## Discipline

Aucun référentiel (W6) n'est rédigé dans ce document pour ces
domaines — cet index reste au niveau W0-W1 (audit + capability map).
