# CVLN Academy Master — W0 Audit Report

```
DATE: this session, branch claude/cvln-academy-canonical-fms.
SCOPE: CVLN_Academy_Cartographie_2D_Master.xlsx ingestion + repo truth
audit + reconciliation matrix + master package skeleton (W0-W3, partial
W4-W5, W12-W16 registries). Full per-domain referential construction
(W6-W11) is the next wave — see 95_GAPS/GAP_REGISTER.md for sequencing.
```

## TOTAL_OBJECTS

812 (Master_Catalogue) = 437 MARKET + 220 SYSTEM_CVLN + 153
CROSS_ECOSYSTEM + 1 BRIDGE + 1 GAP, across 27 domains, plus 130
Operator_Roles, 71 Habilitations, 7 Access_Levels, 10
Missions_Pipelines, 6 Coverage_Gaps, 9 Taxonomy rows (separate sheets,
partially overlapping Master_Catalogue).

## VERIFIED / PROPOSED / MERGED / REJECTED / BLOCKED

| Status | Count | Note |
|---|---|---|
| `VERIFIED` (narrow, specific capability) | 2 | Wallet/JCC ledger (simple), `academy.certification.passed` → Brain event |
| `PARTIAL` (real repo, narrower than candidate) | 4 domains | FMS (partial), Wallet (partial), Agent Factory (partial), Good Mood/DJ Sayd (real but domain-duplicated) |
| `PROPOSED` (all rows, per source `Statut`) | 781 | Unchanged from source |
| `PARTIAL_RETRIEVAL` | 30 | CVLN Hospitality — per source's own declaration |
| `REQUIRES_RECONCILIATION` | 1 | Per source's own declaration |
| `MERGED` | 0 | No row merged in this pass — merging (Good Mood/DJ Sayd) is proposed as an action, not yet executed |
| `REJECTED` | 0 | No row rejected — every row preserved with provenance |
| `BLOCKED` (dependency) | 1 domain (Wallet/CVE cross, 9 rows) | Depends on CVE (non-existent) and advanced Wallet (non-existent) |

## EXTERNAL / INTERNAL / RESTRICTED

437 `EXTERNAL`, 162 `INTERNAL`, 64 `INTERNAL_RESTRICTED`, 25
`INTERNAL_PRIVILEGED`, 123 `BRIDGE`, 1 `TO_RECONCILE`.

## OPERATOR_ROLES / AUTHORIZATIONS / CROSS_ECOSYSTEM_PATHS

130 rôles opérateurs candidats · 71 habilitations candidates · 153
compétences cross-écosystème + 10 pipelines/missions candidats.

## FORMATIONS_BUILT / PARTIAL / PENDING

| Statut | Corpus |
|---|---|
| `FORMATIONS_BUILT` (canonical, pre-existing, confirmed intact) | KOR-01→15 (169 modules, `docs/kor/`), KLT-01→08 (`docs/klt/`), FMS-01→06 (`backend/fms_canonical/`) |
| `FORMATIONS_PARTIAL` | FMS-07→18 (4/12 grounded in `fms-os/fms`), Wallet interne (2/10 grounded) |
| `FORMATIONS_PENDING` | Les 23 autres domaines de cette cartographie — aucun référentiel W6 rédigé |

## Repos externes vérifiés

`fms-os/fms` (cloned, HEAD `70b8e03`), `gmfest972/goodmooddjsayd`
(cloned, HEAD `704ef93`) — voir `95_GAPS/REPO_TRUTH_AUDIT.md` pour le
détail complet.

## Ce que ce rapport ne fait PAS

Ne construit aucun référentiel, blueprint, module, assessment, ou
certification pour les 812 lignes candidates — conformément à la
règle §26 ("use registries and references", jamais 800+ fichiers
markdown redondants). Cette étape est le socle W0-W5/W12-W16 sur
lequel les prochaines vagues W6-W11 domaine par domaine s'appuient.

## Prochaine étape recommandée

Voir `95_GAPS/GAP_REGISTER.md` §"Séquencement recommandé" — commencer
par G1 (Good Mood/DJ Sayd) et G5 (nommer le repo FREKCORE réel), qui
débloquent respectivement 94 et 75 lignes sans nécessiter de nouveau
repo.
