# CVLN Academy Master — Master Index

```
SCOPE: Consolidation of CVLN_Academy_Cartographie_2D_Master.xlsx
(812 candidate rows, 11 sheets) against verified repo truth
(CVL-ACADEMY, fms-os/fms, gmfest972/goodmooddjsayd).
STATUS: W0-W3 (partial W4-W5) — see 00_GOVERNANCE/BUILD_METHOD.md.
This Master Package does NOT duplicate curriculum bodies. It indexes,
reconciles, and registers — full referential/module construction per
domain is a subsequent, separate wave (see GAP_REGISTER.md for
sequencing).
```

## Comment lire ce Master Package

| Dossier | Contenu |
|---|---|
| `00_GOVERNANCE/` | Taxonomie, niveaux d'accès, modèle d'habilitation, méthode W0-W17, quality gates — doctrine adoptée telle quelle du message Founder |
| `10_PORTFOLIO/` | Cet index, la carte de portefeuille, la matrice de contexte, la matrice de réconciliation, et `raw/` (les 11 CSV sources intacts) |
| `20_EXTERNAL/` | Index des formations `MARKET`/`EXTERNAL` candidates par domaine |
| `30_INTERNAL/` | Index des rôles/compétences `SYSTEM_CVLN`/`INTERNAL` candidats par domaine |
| `40_OPERATOR_ROLES/` | Registre des 130 rôles opérateurs candidats |
| `50_AUTHORIZATIONS/` | Registre des 71 habilitations candidates |
| `60_CROSS_ECOSYSTEM/` | Carte des 153 compétences cross-écosystème + 10 pipelines/missions |
| `70_EVIDENCE/` | Architecture d'évidence et espace de noms Skill ID proposés |
| `80_MISSIONS/` | Les 4 missions et 6 pipelines cross-CVLN de la cartographie source |
| `90_SPATIAL/` | Principes de relation spatiale (différé, `SPATIAL_INTEGRATION = LATER_PHASE`) |
| `95_GAPS/` | Audit de repo truth complet + registre des écarts/dépendances |
| `99_REPORTS/` | Rapport d'audit W0, manifeste, changelog |

## Chiffres clés (source : `raw/Master_Catalogue.csv`, 812 lignes)

| Dimension | Lignes |
|---|---|
| `MARKET` (externe) | 437 |
| `SYSTEM_CVLN` (interne) | 220 |
| `CROSS_ECOSYSTEM` | 153 |
| `BRIDGE` (isolé) | 1 |
| `GAP` (isolé) | 1 |

| Statut source | Lignes |
|---|---|
| `CANDIDATE` | 781 |
| `PARTIAL_RETRIEVAL` | 30 |
| `REQUIRES_RECONCILIATION` | 1 |

27 domaines identifiés (voir `PORTFOLIO_MAP.md` et
`RECONCILIATION_MATRIX.md` pour le détail par domaine).

## Ce que ce Master Package confirme (repo truth vérifié)

- 3 repos réels inspectés : `cultureconnectorg/CVL-ACADEMY` (ce repo),
  `fms-os/fms`, `gmfest972/goodmooddjsayd`.
- 2 capacités `CAPABILITY_ALREADY_REAL` confirmées : Wallet/JCC (simple
  ledger) et l'événement `academy.certification.passed` → CVLN Brain.
- 1 duplication de domaine détectée dans la source : Good Mood / DJ
  Sayd sont un seul repo réel, traités comme deux domaines séparés dans
  la cartographie (94 lignes à réconcilier).
- Le corpus KOR-01→15 et KLT-01→08/FMS-01→06 (déjà livrés,
  antérieurement à cette cartographie) restent la baseline de
  profondeur/qualité — jamais reconstruits par ce Master Package.
