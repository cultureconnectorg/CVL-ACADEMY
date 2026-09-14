# CVLN Kiltikonet Master Package v1

```
NO_REBUILD_KLT01_05 — ce package consolide le corpus existant
(docs/klt/, 139 documents, 59 modules). Il n'en réécrit, ni n'en
duplique, aucun contenu pédagogique.
```

## Ce que ce package est

Une **consolidation canonique** du corpus Kiltikonet déjà construit
(`KLT-01` à `KLT-05`) : un index maître, une cartographie transversale
des compétences, une architecture d'évaluation et de certification
consolidée, des registres de validation, des cartes d'intégration et de
dépendances, et des quality gates — le tout navigable, auditable, prêt
pour les prochaines validations.

## Ce que ce package n'est pas

Ce n'est **pas** un nouveau corpus pédagogique. Les dossiers
`01_KLTxx.../` de ce package ne contiennent qu'un `INDEX.md` — un
pointeur structuré vers `docs/klt/kltXX/`, jamais une copie. Le contenu
pédagogique réel (référentiels, modules, cas, assessments, guides,
templates) reste à un seul endroit : `docs/klt/`.

## `STRUCTURAL_COMPLETENESS != EXTERNAL_VALIDATION` — à ne jamais perdre

Contrairement au corpus FMS de référence (223 documents réels,
rédigés par des experts terrain, intégrés par Claude sans jamais être
rédigés par lui), **ce corpus Kiltikonet a été rédigé par Claude**, à
partir du contenu legacy réel (`seed_data.py`, `seed_modules.py`,
`catalog_cartography.py`, `external_calibration.py`) et du master plan
structurel fourni par le Founder — pas à partir d'un corpus externe déjà
validé par des professionnels du terrain.

Le corpus possède une architecture industrielle comparable à FMS
(référentiels → compétences → blueprints → modules → cas →
traceability → N1 → N2 → A01 → rubrics → skill IDs → evidence models →
guides → templates → certification → quality gates → intégration
préparée) — mais **structure industrielle ne veut pas dire validation
métier externe**. Pour chaque formation, ce package distingue
explicitement six statuts (voir chaque `01_KLTxx.../INDEX.md` et
`91_VALIDATION/`) :

| Dimension | Ce qu'elle mesure |
|---|---|
| `STRUCTURAL_STATUS` | Le document est-il complet et cohérent avec ses propres quality gates ? |
| `CONTENT_STATUS` | D'où vient le contenu (legacy réel, master plan, ou généré) ? |
| `EXPERT_VALIDATION_STATUS` | Un professionnel du métier l'a-t-il relu ? |
| `FIELD_TEST_STATUS` | A-t-il été testé avec de vrais candidats/correcteurs/jurys ? |
| `ACADEMY_INTEGRATION_STATUS` | Est-il connecté au runtime Academy ? |
| `PRODUCT_INTEGRATION_STATUS` | Dépend-il d'un système Kiltikonet réel non connecté ? |

**À ce jour, pour les 5 formations : `STRUCTURAL_STATUS = COMPLETE`,
les cinq autres dimensions = non atteintes.** Voir
`91_VALIDATION/KILTIKONET_FIELD_VALIDATION_REGISTER.md`.

## Priorités de validation identifiées

- **`KLT-03`** — OIF, UNESCO, CARIFESTA, DAC, CTM, Creative Europe :
  contenu institutionnel à vérifier/sourcer/dater avant tout usage réel.
- **`KLT-04`** — droit associatif (loi 1901), fiscalité, bénévolat :
  contenu juridique nécessitant validation/actualisation.

Voir `91_VALIDATION/EXTERNAL_VALIDATION_REGISTER.md` pour le détail
élément par élément.

## Structure du package

```
docs/kiltikonet_master_package/
  00_MASTER/            — index, portfolio map, cross-KLT map, pathway,
                           assessment architecture, skill registry,
                           evidence model, certification architecture,
                           operator authorization architecture
  01_KLT01_MEDIATEUR_CULTUREL/     — pointeur vers docs/klt/klt01/
  02_KLT02_CHEF_PROJET_CULTUREL/   — pointeur vers docs/klt/klt02/
  03_KLT03_PARTENARIATS_INSTITUTIONNELS/ — pointeur vers docs/klt/klt03/
  04_KLT04_GOUVERNANCE_RESEAUX/    — pointeur vers docs/klt/klt04/
  05_KLT05_OPERATEUR_KILTIKONET/   — pointeur vers docs/klt/klt05/
  06_KLT06_PLANNED/ 07_KLT07_PLANNED/ 08_KLT08_PLANNED/ — stubs PLANNED
  90_SHARED/             — cas fil rouge, univers multi-métiers
  91_VALIDATION/          — registres de validation externe/terrain
  92_INTEGRATION/         — cartes d'intégration Academy/produit
  93_QUALITY/             — quality gates transversaux
  99_REPORTS/             — manifest, changelog
```

## Source of truth

```
KLT0001 = CANONICAL EDUCATION MAP
KLT0002 = LEGACY/CANONICAL RECONCILIATION
KLT0003 = KLT01 REFERENTIAL FREEZE
KLT0004+ = PEDAGOGICAL BUILD (KLT-01, puis KLT-02→05 en continuation
           de session)
docs/klt/ (139 documents, 59 modules) = CURRENT CONSOLIDATED
           PEDAGOGICAL CORPUS — CVLN_Kiltikonet_Canonical_Corpus_
           KLT01-05.zip en est l'export livré
Ce Master Package = CONSOLIDATION du corpus ci-dessus, jamais une
           nouvelle version
```

Si ce repo contient un jour une vérité plus récente que ce qui est cité
ici, elle doit être signalée comme divergence dans un nouveau ticket —
jamais écrasée silencieusement par une mise à jour de ce package.

## Interdictions respectées dans ce ticket

```
NO_REBUILD_KLT01_05 · NO_DUPLICATE_CURRICULUM · NO_DB_MUTATION ·
NO_RUNTIME_BINDING · NO_SEED_MUTATION · NO_ROUTE_CHANGE ·
NO_FMS_MUTATION · NO_FAKE_OBSERVATORY · NO_FAKE_KILTIKONET_FEATURE ·
NO_FAKE_FREK_PROOF · NO_RNCP_CLAIM · NO_KLT06_08_BUILD
```

Voir `docs/KILTIKONET_MASTER_PACKAGE_V1_REPORT.md` pour la vérification
détaillée de chacune.
