# CVLN Academy Master — Changelog

| Date/Commit | Contenu |
|---|---|
| W0 | Ingestion de `CVLN_Academy_Cartographie_2D_Master.xlsx` (812 lignes, 11 sheets) ; audit repo truth de 3 repos (CVL-ACADEMY, `fms-os/fms`, `gmfest972/goodmooddjsayd`) ; construction du Master Package `docs/cvln_academy_master/` (24 fichiers, 12 dossiers). |
| `7ef9599` | FMS-07→18 réconcilié (v2, correction Founder `CONTENT_OVERLAP != PROFESSIONAL_DUPLICATE`) — 0/12 rejeté. |
| `ff481e3` | FRK-01→75 audit + réconciliation — 0/75 rejeté. |
| `fb0c0dd` | Kiltikonet KLT-09→20 réconcilié — 0/12 rejeté. |
| `846ee42` | CVLN Wallet (WAL-01→28) + CVE (CVE-01→15) réconciliés — 0/28 rejeté, CVE `NEEDS_FOUNDER_DECISION`. |
| `1e6e9f2` | KORA interne/cross (KOR-OP-01→12, KOR-X-01→07) réconcilié — 0/19 rejeté, over-counting KOR-X détecté. |
| `580d495` | Agent Factory/AF-X/Laurentia/IOS/Brain/CMD/Intelligent Operations (109 lignes) réconcilié — 0/109 rejeté, ~90% `BLOCKED_PRODUCT_DEPENDENCY`. |
| `2494a99` | Good Mood + DJ Sayd (94 lignes) réconcilié — G1 fermé (pas de vrai doublon, DJ Sayd = 0 ligne opérateur). |
| `3fb54a4` | CyberSecure, Blockchain+Tokenomics, Gala Cook & Food, Hospitality, LabelOS, Founder/CEO, CVLN Group, Fondation Cœurvolan (372 lignes) réconciliés — G3, G7, G8 fermés ; découverte d'un corpus legacy sous-évalué au W0 (`LOS-01`, `BCH-01`, `HOS-01`, `GRP-01/02`, `CIP-01`) ; nouvelle décision Founder `G9` (identité CIP/Fondation). |
| `6ec239b` | Cross-CVLN/XCV (67 lignes) réconcilié — sur-comptage `XCV-57→66` ≡ `SYS-01→10` détecté et convergé. |
| `1331be3` | Consolidation finale des registres (rôles, habilitations, évidence, Spatial) — indexation pure, `ORPHAN_ROLE=0`, `ORPHAN_AUTHORIZATION=0` confirmés sur 130+71 lignes. |
| `fe00bb9` | Bilan final des quality gates — **812/812 lignes réconciliées**, 0 rejet, 2 décisions Founder alors résiduelles (CVE, identité CIP/Fondation). |
| Ce commit (`FD-CVE-001` + `FD-CIP-001`) | **Clôture des deux décisions Founder demandées.** CVE : source méthodologique réelle nommée (`memory/KORA_CVE_Specification_Mathematique_v1.0.md`, KORA) → statut `FORMALIZED_METHODOLOGY`/`SOURCE_OBSERVED`, `CALIBRATION_PENDING` pour les paramètres non calibrés. CIP/Fondation : deux objets distincts, jamais fusionnés — `CIP Foundation (legacy working identity)` en attendant sa forme juridique définitive. Vérification globale : 1 décision Founder distincte et pré-existante reste ouverte (`FRK-71`, jamais couverte par ces deux clôtures — voir `QUALITY_GATES.md`). `RECONCILIATION_MATRIX.md`, `GAP_REGISTER.md`, `QUALITY_GATES.md` mis à jour en conséquence. Puis lancement de **W6** (référentiels pédagogiques réels par vagues). |

## Ce que ce chantier NE fait PAS

Ne modifie aucun fichier de code, seed, ou runtime existant
(`NO_RUNTIME_BINDING`, `NO_DB_MUTATION`, `NO_SEED_MUTATION`). Ne
reconstruit aucun corpus déjà livré (KOR-01→15, KLT-01→08, FMS-01→06).

## Décisions Founder — les deux demandées sont closes

`FD-CVE-001` et `FD-CIP-001` sont désormais `CLOSED` (voir
`QUALITY_GATES.md` pour le détail). **1 décision Founder distincte
reste ouverte** — `FRK-71` (FREK v3 Architecture), jamais couverte par
ces deux clôtures et non traitée ici faute de mandat explicite ; elle
ne bloque qu'une ligne sur 812. Le chantier reste sur la discipline
`RECONCILED_NOT_BUILT` jusqu'à ce qu'un objet ait effectivement son
contenu W6 (compétences, modules, assessments, preuves, gates)
construit et vérifié — `FULLY_COMPLETE` n'est déclaré pour aucun objet
par ce seul commit.

## W6 — construction des référentiels pédagogiques réels (en cours)

Les 812 lignes réconciliées sont l'entrée canonique ; W6 ne recrée
aucune cartographie. Vagues par ordre de solidité d'ancrage : Good
Mood GMD-21→33 (meilleur cluster opérateur, code réel complet) →
FMS-07 (ombrelle) → FREK-01/58 → CyberSecure CYB-01→30 → Blockchain
BCI-01→30 (sur `BCH-01`) → CVLN Hospitality HOS-01→30 (sur legacy
`HOS-01`) → Founder/CEO CEO-01→12 → CVE-01→15 (méthodologie formalisée)
→ extension aux domaines restants. Chaque vague : compétences →
prérequis → objectifs → modules → outcomes → exercices → livrables →
assessments → rubrics → evidence → certification eligibility →
mission eligibility → internal authorization gates (si applicable),
suivie de tests, preuve, commit, push.

### Wave 1 — Good Mood internal operator corpus (`docs/gmd/`)

Premier référentiel W6 réellement construit : GMD-21→33 (13
formations, 41 modules, `MODULE_CONTENT_DRAFTED`) + GMD-34 gap
explicitement déclaré (`gmd34/GAP.md`, `BLOCKED_PRODUCT_DEPENDENCY`,
non simulé). Choisi en premier car meilleur cluster ancré du chantier
(13/14 sur code réel `gmfest972/goodmooddjsayd`). Chaque
`gmdNN/REFERENTIAL.md` couvre compétences → prérequis → objectifs →
modules → outcomes/livrables → assessment, avec doctrine de
certification/évaluation partagée (`CERTIFICATION_MODEL.md`) pour
éviter la duplication. Skill IDs `GMD21.SKILL.*` → `GMD33.SKILL.*`
réservés (`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`). `FULLY_COMPLETE`
non déclaré — aucun candidat réel évalué encore
(`docs/gmd/QUALITY_GATES.md`).
