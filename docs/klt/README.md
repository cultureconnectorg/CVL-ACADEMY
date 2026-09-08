# Corpus Canonique Kiltikonet (KLT-01 → KLT-08, KLT-13, KLT-18)

```
WORKSTREAM = KLT (Kiltikonet), séparé de FMS (FMS_CLOSED = TRUE)
STATUT = 5/5 formations legacy construites au niveau industriel FMS
         (KLT-01→05, COMPLETE) + 3/3 formations NEW du premier lot
         (KLT-06→08, STRUCTURAL_STATUS = COMPLETE, 7/7 compétences
         chacune) + 2/2 formations NEW du second lot (KLT-13, KLT-18,
         construites le 2026-09-07, 5/5 compétences chacune,
         STRUCTURAL_STATUS = COMPLETE **et** FULLY_COMPLETE = TRUE —
         voir §Formations NEW du second lot).
KLT-06/07/08 FULLY_COMPLETE = FALSE malgré tout (4 compétences sur 21 —
         KLT-06/C5-C6, KLT-07/C4, KLT-08/C4 — désormais
         `BUILT_UNCONNECTED` : module et contenu réels, construits sur
         le schéma réel vérifié d'Observatory/Network dans
         `Kiltikonet-Aout2026`, mais aucune connexion live
         Academy↔Kiltikonet-Aout2026). Ce champ reste FALSE tant qu'un
         client réel n'existe pas — à ne jamais déclarer TRUE sans un
         ticket dédié qui le justifie. KLT-13/18, à l'inverse, n'ont
         aucune compétence `BUILT_UNCONNECTED` (aucune dépendance à un
         système externe non connecté) : leur `FULLY_COMPLETE = TRUE`
         se calcule honnêtement, même dérivation que KLT-01→05 — ce
         n'est jamais confondu avec un import réel en base
         (`db.formations`), qui reste `NO_RUNTIME_BINDING_YET` pour les
         10 formations sans exception.
STOP = TRUE après cette livraison — intégration runtime Academy et
tout nouveau chantier ACA restent NOT_AUTHORIZED.

FOUNDER_AUTHORIZATION_UPDATE (2026-09-07) : le Founder a explicitement
autorisé, dans le périmètre suivant seulement, de lever ce STOP :
  1. Construire KLT-06/M05-M06, KLT-07/M04, KLT-08/M04 (les 4
     compétences précédemment `BLOCKED`) — désormais buildables sur la
     base du schéma réel vérifié de `Kiltikonet-Aout2026` (voir
     `KLT_09_20_RECONCILIATION.md` §Re-vérification 2026-09-07) :
     Observatory et Network sont du **code réel vérifié** (routes,
     RBAC, collections nommées), mais **Academy n'a aucun client/
     credentials appelant cette API en direct** — le contenu enseigne
     l'architecture réelle vérifiée, jamais une intégration live
     fabriquée. **FAIT** (2026-09-07).
  2. Construire KLT-13 (Terrain Operations, Accreditation & NFC) et
     KLT-18 (Cultural Communications & Engagement Operations) comme
     nouvelles formations complètes, per les verdicts déjà posés dans
     `KLT_09_20_RECONCILIATION.md` (`SPECIALIZE_EXISTING`/
     `EXTEND_EXISTING`, ancrées sur `KLT-05`). **FAIT** (2026-09-07) —
     voir §Formations NEW du second lot.
Le reste du chantier KLT-09→20 (les 8 autres candidats, tous
`BLOCKED_PRODUCT_DEPENDENCY`) et toute intégration runtime live
Academy↔Kiltikonet-Aout2026 restent `NOT_AUTHORIZED` — ce champ ne
devient jamais `FALSE` globalement sur la seule base de ce message.
```

## Ce que contient ce corpus

**KLT-01 → KLT-05 (COMPLETE)** — 5 formations, chacune avec un package
pédagogique complet — référentiel, blueprints, cas fil rouge, modules
complets, banque N1, évaluations N2, assessment certificatif, rubric,
registre de skill IDs, evidence model, guides candidat/correcteur/jury,
templates, modèle de certification, note d'intégration, quality gates :

| Formation | Dossier | Modules | Documents |
|---|---|---|---|
| KLT-01 — Médiateur culturel | `klt01/` | 11 | 27 |
| KLT-02 — Chef de projet culturel | `klt02/` | 11 | 27 |
| KLT-03 — Responsable partenariats institutionnels culturels | `klt03/` | 12 | 28 |
| KLT-04 — Gouvernance des organisations et réseaux culturels | `klt04/` | 14 | 30 |
| KLT-05 — Opérateur Kiltikonet / Cultural Platform Operator | `klt05/` | 11 | 27 |

**139 documents pédagogiques**, plus les 4 documents de gouvernance du
workstream (racine `docs/`) : `KILTIKONET_KLT0001_CANONICAL_EDUCATION_
MAP.md`, `KILTIKONET_KLT0002_LEGACY_CANONICAL_RECONCILIATION.md`,
`KILTIKONET_KLT0003_KLT01_CANONICAL_REFERENTIAL.md`,
`KILTIKONET_KLT0004_KLT01_PEDAGOGICAL_BUILD_REPORT.md`.

**KLT-06 → KLT-08 (STRUCTURAL_STATUS = COMPLETE)** — 3 formations `NEW`
(sans legacy). Mise à jour 2026-09-07 : après re-vérification
Founder-autorisée, l'Observatory et le Network Kiltikonet se sont
révélés être du code réel vérifié (routes, RBAC, collections nommées)
dans `cultureconnectorg/Kiltikonet-Aout2026` — les 4 compétences
autrefois `BLOCKED` ont donc été construites sur ce schéma réel,
reclassifiées `BUILT_UNCONNECTED` (module et contenu réels, mais aucune
connexion live Academy↔Kiltikonet-Aout2026) :

| Formation | Dossier | Référentiel | Modules construits | Compétences `BUILT_UNCONNECTED` | Documents |
|---|---|---|---|---|---|
| KLT-06 — Analyste Observatory / Cultural Data Analyst | `klt06/` | `KILTIKONET_KLT0005_...` | 7/7 | 2 (C5, C6 — Observatory) | 24 |
| KLT-07 — Responsable déploiement territorial culturel | `klt07/` | `KILTIKONET_KLT0006_...` | 7/7 | 1 (C4 — Network) | 24 |
| KLT-08 — Responsable qualité, conformité & audit réseau | `klt08/` | `KILTIKONET_KLT0007_...` | 7/7 | 1 (C4 — Network/Compliance) | 24 |

**72 documents** supplémentaires (21 modules construits + support
complet par formation), plus 4 documents de décision (`KILTIKONET_
KLT0005`→`KLT0008_...md`, racine `docs/`). **Aucune de ces trois
formations n'a de badge** — formations `NEW`, sans équivalent legacy.
Voir chaque `CERTIFICATION_MODEL.md` : certification **complète** (7/7),
mais jamais une preuve de connexion live Academy↔Kiltikonet-Aout2026.

**Profondeur de module approfondie (17/17 modules originellement
construits)** — même traitement que `KOR-03`→`15` : chaque module déjà
`BUILT` est passé de 1 à 2 exemples contrastés et de 2 à 3 erreurs
fréquentes documentées. Les 4 modules ajoutés le 2026-09-07 (`KLT-06`/
M05-M06, `KLT-07`/M04, `KLT-08`/M04) portent nativement ce même format
dès leur écriture. Aucune connexion live n'est jamais fabriquée —
conformément à `NO_FAKE_LIVE_CONNECTION` (renommé depuis
`NO_FAKE_OBSERVATORY`/`NO_FAKE_NETWORK`/`NO_FAKE_COMPLIANCE`) : le
schéma réel vérifié est enseigné comme architecture citable, jamais
comme une requête live qu'Academy peut faire aujourd'hui.

**KLT-13 → KLT-18 (formations NEW du second lot, STRUCTURAL_STATUS =
COMPLETE et FULLY_COMPLETE = TRUE)** — 2 formations construites le
2026-09-07 sur autorisation Founder scopée, verdicts de
`KLT_09_20_RECONCILIATION.md` : `KLT-13` (`SPECIALIZE_EXISTING` sur
`KLT-05`/C4) et `KLT-18` (`EXTEND_EXISTING`/hybride sur `KLT-05`/C5,C7,C9)
— aucune des deux ne rouvre ni ne duplique `KLT-05` :

| Formation | Dossier | Compétences | Documents |
|---|---|---|---|
| KLT-13 — Responsable Accréditation Terrain / Terrain Accreditation Operator | `klt13/` | 5/5 | 21 |
| KLT-18 — Responsable Communications & Engagement Culturel | `klt18/` | 5/5 | 21 |

**42 documents** supplémentaires. Contrairement à `KLT-06`→`08`, aucune
compétence de ces deux formations ne dépend d'un système externe non
connecté (`BUILT_UNCONNECTED` n'apparaît dans aucun des deux registres) —
`FULLY_COMPLETE = TRUE` s'y calcule donc honnêtement, exactement comme
`KLT-01`→`05`. `KLT-13` étudie un précédent réel cross-écosystème (Good
Mood, système QR — `GMD-25`) sans jamais le confondre avec un système
Kiltikonet, et spécifie une extension NFC en nommant explicitement son
statut `NOT_IMPLEMENTED` (aucun système NFC réel n'existe nulle part
dans l'écosystème CVLN vérifié). `KLT-18` étend `KLT-05`/C5,C7,C9 par
référence uniquement — l'animation quotidienne, le support individuel et
la lecture de signaux d'engagement au quotidien restent enseignés dans
`KLT-05` seul. **Aucune de ces deux formations n'a de badge** — formations
`NEW`, sans équivalent legacy.

**Total : 253 documents pédagogiques** (139 + 72 + 21 + 21) sous
`docs/klt/`, plus les documents de gouvernance/décision à la racine
`docs/`.

## Un seul univers, dix angles métier

Les dix formations partagent le même cas fil rouge — **La Veillée du
Tanbou**, à *Baie-Mahault-sur-Mer* (territoire et personnes fictifs,
`CASE_STATUS = PEDAGOGICAL_SIMULATION` partout) — chacune l'abordant
sous l'angle de son métier propre : médiation directe (`KLT-01`),
pilotage de projet (`KLT-02`), partenariats institutionnels (`KLT-03`),
gouvernance associative et réseau (`KLT-04`), opération de plateforme
numérique (`KLT-05`), analyse de données (`KLT-06`), déploiement
territorial réseau (`KLT-07`), audit réseau (`KLT-08`), accréditation
terrain (`KLT-13`), communications & engagement (`KLT-18`). C'est la
doctrine posée dès `KLT-0001` : "même univers, angle métier différent."
Les angles `KLT-06`→`08` s'articulent explicitement à la suite des cinq
premiers (Mémoire Vive candidate opérateur relais en `KLT-07`, puis
auditée en `KLT-08`) plutôt que de repartir d'une situation isolée ;
`KLT-13`/`18` restent ancrées sur `KLT-05` par référence, sans jamais
dupliquer ses compétences.

## Disciplines transversales, appliquées aux dix formations

- **`LEGACY = EXISTING_EVIDENCE`** — aucun contenu legacy réel n'a été
  supprimé ; chaque formation garde sa base réelle (`KLT-0002`).
- **`FMS_METHOD = REFERENCE`, `FMS_CONTENT != KLT_CONTENT`** — même
  rigueur méthodologique que FMS, zéro contenu FMS copié.
- **`NO_FAKE_OBSERVATORY`** — chaque module qui nomme `Observatory`
  comme dépendance master-plan (M10 `KLT-01`, M09 `KLT-02`, M10 `KLT-03`,
  M09 `KLT-05`) documente explicitement son absence plutôt que de la
  simuler.
- **`badge_name = DISPLAY_ONLY_LEGACY`** partout — aucun badge n'est
  présenté comme une certification RNCP ou une autorisation réelle.
- **`OPERATOR_AUTHORIZATION = NOT_IMPLEMENTED/NOT_GRANTED`** — appliqué
  à toutes les formations, avec une rigueur maximale sur `KLT-05` où le
  risque de confusion est le plus élevé.
- **`ACADEMY_CERTIFICATION != RNCP_OR_STATE_CERTIFICATION`** — chaque
  `CERTIFICATION_MODEL.md` pose cette distinction explicitement.
- **`NO_DB_MUTATION`, `NO_RUNTIME_BINDING`, `NO_SEED_REPLACEMENT`** —
  ce corpus est entièrement documentaire ; zéro fichier de code, de seed
  ou de route touché pour le produire.
- **`NO_FAKE_LIVE_CONNECTION`** (`KLT-06`→`08`, renommé depuis
  `NO_FAKE_OBSERVATORY`/`NO_FAKE_NETWORK`/`NO_FAKE_COMPLIANCE` le
  2026-09-07) — les 4 compétences autrefois `BLOCKED` sont désormais
  construites sur le schéma réel vérifié d'Observatory/Network
  (`Kiltikonet-Aout2026`), mais aucun livrable ne prétend interroger ce
  système en direct : toute donnée manipulée reste explicitement
  `PEDAGOGICAL_ILLUSTRATIVE`.
- **`BUILT_UNCONNECTED_MISREPRESENTED = 0`** (`KLT-06`→`08`, renommé
  depuis `BLOCKED_COMPETENCY_MISREPRESENTED` le 2026-09-07) — les 4
  compétences reclassifiées (2 en `KLT-06`, 1 chacune en `KLT-07`/`08`)
  sont marquées `BUILT_UNCONNECTED` à chaque niveau (référentiel,
  registre de skills, evidence model, certification, guides), jamais
  présentées comme une connexion live qu'Academy n'a pas.
- **`METHOD_INHERITANCE = héritage explicite, jamais duplication`**
  (`KLT-08`, `KLT-18`) — la méthode d'audit `KLT-04`/M13 est réutilisée
  par référence pour `KLT-08` ; l'animation communauté/support/lecture
  de signaux de `KLT-05`/M05,M07,M09 l'est pour `KLT-18` — jamais copiée
  ni réinventée dans les deux cas.
- **`NFC_NOT_IMPLEMENTED`** (`KLT-13`) — aucun système NFC réel n'existe
  nulle part dans l'écosystème CVLN vérifié ; toute spécification NFC
  porte la mention explicite de son statut non implémenté.
- **`REAL_PRECEDENT_CITED_ACCURATELY`** (`KLT-13`) — le précédent réel
  cross-écosystème étudié (Good Mood, système QR `GMD-25`) est toujours
  attribué à sa source réelle, jamais présenté comme un système
  Kiltikonet.
- **`EXTENSION_NOT_DUPLICATION`** (`KLT-18`) — aucun module ne réenseigne
  l'animation quotidienne, le support individuel, ni la lecture de
  signaux d'engagement de `KLT-05`/M05,M07,M09, cités par référence
  uniquement.

## Comment lire une formation

Dans chaque dossier `kltXX/` :

1. `00_REFERENTIEL_ET_BLUEPRINTS.md` — métier, compétences, structure des
   modules, correspondance legacy → canon.
2. `case/` — le cas fil rouge (angle métier) + la matrice compétence ↔
   cas.
3. `modules/` — les modules complets (M01 à MXX).
4. `assessments/` — banque N1, évaluations N2, assessment certificatif,
   rubric.
5. `skills/` — registre de skill IDs, modèle de preuve.
6. `guides/` — candidat, correcteur, jury.
7. `templates/` — gabarits réutilisables.
8. `CERTIFICATION_MODEL.md`, `INTEGRATION_ACADEMY_PACKAGE_NOTE.md`,
   `QUALITY_GATES.md` — cadrage transversal de la formation.

## Provenance et limites (à lire avant toute diffusion)

Ce corpus a été **rédigé par Claude** (Sonnet 5), à partir du contenu
legacy réel déjà présent dans le repo (`seed_data.py`, `seed_modules.py`,
`catalog_cartography.py`, `external_calibration.py`) et du master plan
structurel fourni par le Founder — **pas** à partir d'un corpus externe
déjà rédigé par des experts métier, à la différence de FMS (223 documents
réels intégrés, jamais rédigés par l'IA). Le contenu est
méthodologiquement rigoureux et traçable, mais reste un contenu généré,
pas un contenu de terrain validé. En particulier :

- Le contenu institution-spécifique de `KLT-03` (OIF, UNESCO, CARIFESTA,
  DAC, CTM, Creative Europe) porte la mention `SOURCE_STATUS =
  PEDAGOGICAL_ILLUSTRATIVE` — tout fait daté (calendrier, montant,
  procédure) doit être vérifié contre une source institutionnelle
  vivante avant tout usage réel.
- Le contenu juridique/fiscal de `KLT-04` (loi 1901, fiscalité culturelle,
  droit du bénévolat) porte la même réserve.
- Aucune formation ne délivre de reconnaissance RNCP, ni d'autorisation
  opérationnelle réelle sur un système Kiltikonet — voir chaque
  `CERTIFICATION_MODEL.md`.
- `KLT-06`→`08`, `KLT-13`, `KLT-18` restent, en plus de ce qui précède,
  des formations dont la source est plus mince que `KLT-01`→`05` (aucun
  legacy, aucun détail module-par-module dans un master plan pré-existant)
  — la carte de compétences de chacune est intégralement `PROPOSED`
  (dérivée par Claude), voir chaque `00_REFERENTIEL_ET_BLUEPRINTS.md`
  §Avertissement de source. `KLT-06`→`08` sont `STRUCTURAL_STATUS =
  COMPLETE` (7/7 modules chacune) mais `FULLY_COMPLETE = FALSE` (4
  compétences `BUILT_UNCONNECTED`) — voir §Formations NEW. `KLT-13`/`18`
  sont `STRUCTURAL_STATUS = COMPLETE` **et** `FULLY_COMPLETE = TRUE` (5/5
  modules chacune, aucune dépendance externe non connectée) — voir
  §Formations NEW du second lot.

## Ce qui n'a pas été fait (hors scope, non autorisé)

Aucun import réel dans le runtime Academy (`NO_RUNTIME_BINDING_YET`,
voir chaque `INTEGRATION_ACADEMY_PACKAGE_NOTE.md`) — pour les 10
formations sans exception, `KLT-13`/`18` compris malgré leur
`FULLY_COMPLETE = TRUE`. Aucun test avec de vrais candidats/correcteurs/
jury, pour aucune des 10 formations. Les 4 compétences
`BUILT_UNCONNECTED` de `KLT-06`→`08` (`C5`/`C6` Observatory de `KLT-06`,
`C4` Network de `KLT-07`, `C4` Network/Compliance de `KLT-08`) sont
désormais construites sur le schéma réel vérifié, mais sans aucune
connexion live Academy↔Kiltikonet-Aout2026 — voir chaque
`modules/MODULES_STATUS.md`. Les 10 autres candidats de la reconciliation
`KLT-09→20` (hors `KLT-13`/`18`) ont été **fermés le 2026-09-08** à
`KLT_09_20_BLOCKED_CANDIDATES.md` (4 convergés sans fichier séparé —
KLT-09/10/14/17 — et 6 déclarés `BLOCKED_PRODUCT_DEPENDENCY` avec leur
frontière de réutilisation nommée — KLT-11/12/15/16/19/20), sans lever
`NOT_AUTHORIZED`/`STOP=TRUE` au-delà du périmètre déjà scopé par le
Founder.
