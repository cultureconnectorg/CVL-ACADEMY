# Corpus Canonique Kiltikonet (KLT-01 → KLT-08)

```
WORKSTREAM = KLT (Kiltikonet), séparé de FMS (FMS_CLOSED = TRUE)
STATUT = 5/5 formations legacy construites au niveau industriel FMS
         (KLT-01→05, COMPLETE) + 3/3 formations NEW construites au
         périmètre buildable autorisé (KLT-06→08, PARTIAL — 4
         compétences sur 21 restent BLOCKED, voir §Formations
         partielles).
STOP = TRUE après cette livraison — intégration runtime Academy et
tout nouveau chantier ACA restent NOT_AUTHORIZED.
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

**KLT-06 → KLT-08 (PARTIAL)** — 3 formations `NEW` (sans legacy),
construites sur le périmètre buildable décidé par `KLT-0008`. Chaque
formation ne couvre que ses compétences non bloquées ; les compétences
dépendant d'un système Kiltikonet non connecté (Observatory, Network,
Compliance) restent explicitement `BLOCKED`, non construites, non
simulées :

| Formation | Dossier | Référentiel | Modules construits | Compétences bloquées | Documents |
|---|---|---|---|---|---|
| KLT-06 — Analyste Observatory / Cultural Data Analyst | `klt06/` | `KILTIKONET_KLT0005_...` | 5/7 | 2 (C5, C6 — Observatory) | 22 |
| KLT-07 — Responsable déploiement territorial culturel | `klt07/` | `KILTIKONET_KLT0006_...` | 6/7 | 1 (C4 — Network) | 23 |
| KLT-08 — Responsable qualité, conformité & audit réseau | `klt08/` | `KILTIKONET_KLT0007_...` | 6/7 | 1 (C4 — Compliance) | 23 |

**68 documents** supplémentaires (17 modules construits + support
complet par formation), plus 4 documents de décision (`KILTIKONET_
KLT0005`→`KLT0008_...md`, racine `docs/`). **Aucune de ces trois
formations n'a de badge** — formations `NEW`, sans équivalent legacy.
Voir chaque `CERTIFICATION_MODEL.md` : certification **partielle**
uniquement.

**Total : 207 documents pédagogiques** (139 + 68) sous `docs/klt/`, plus
8 documents de gouvernance/décision à la racine `docs/`.

## Un seul univers, huit angles métier

Les huit formations partagent le même cas fil rouge — **La Veillée du
Tanbou**, à *Baie-Mahault-sur-Mer* (territoire et personnes fictifs,
`CASE_STATUS = PEDAGOGICAL_SIMULATION` partout) — chacune l'abordant
sous l'angle de son métier propre : médiation directe (`KLT-01`),
pilotage de projet (`KLT-02`), partenariats institutionnels (`KLT-03`),
gouvernance associative et réseau (`KLT-04`), opération de plateforme
numérique (`KLT-05`), analyse de données (`KLT-06`), déploiement
territorial réseau (`KLT-07`), audit réseau (`KLT-08`). C'est la
doctrine posée dès `KLT-0001` : "même univers, angle métier différent."
Les trois derniers angles s'articulent explicitement à la suite des cinq
premiers (Mémoire Vive candidate opérateur relais en `KLT-07`, puis
auditée en `KLT-08`) plutôt que de repartir d'une situation isolée.

## Disciplines transversales, appliquées aux huit formations

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
- **`NO_FAKE_NETWORK`, `NO_FAKE_COMPLIANCE`** (`KLT-06`→`08`) — mêmes
  disciplines que `NO_FAKE_OBSERVATORY`, appliquées à `Network`
  (`KLT-07`) et `Compliance` (`KLT-08`) : aucune donnée simulée pour
  combler une compétence bloquée.
- **`BLOCKED_COMPETENCY_MISREPRESENTED = 0`** (`KLT-06`→`08`) — les 4
  compétences bloquées (2 en `KLT-06`, 1 chacune en `KLT-07`/`08`) sont
  marquées `BLOCKED` à chaque niveau (référentiel, registre de skills,
  evidence model, certification, guides), jamais présentées comme
  couvertes.
- **`METHOD_INHERITANCE = héritage explicite, jamais duplication`**
  (`KLT-08`) — la méthode d'audit `KLT-04`/M13 est réutilisée par
  référence pour `KLT-08`, jamais copiée ni réinventée.

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
- `KLT-06`→`08` sont, en plus de ce qui précède, **structurellement
  incomplètes** (`PARTIAL`, pas `COMPLETE`) : leur source est plus mince
  que `KLT-01`→`05` (aucun legacy, aucun détail module-par-module dans
  le master plan tel que résumé par `KLT-0001`) — la carte de
  compétences de chacune est intégralement `PROPOSED` (dérivée par
  Claude), voir chaque `00_REFERENTIEL_ET_BLUEPRINTS.md` §Avertissement
  de source.

## Ce qui n'a pas été fait (hors scope, non autorisé)

Aucun import réel dans le runtime Academy (`NO_RUNTIME_BINDING_YET`,
voir chaque `INTEGRATION_ACADEMY_PACKAGE_NOTE.md`). Aucun test avec de
vrais candidats/correcteurs/jury, pour aucune des 8 formations. Les 4
compétences `BLOCKED` de `KLT-06`→`08` (`C5`/`C6` Observatory de
`KLT-06`, `C4` Network de `KLT-07`, `C4` Compliance de `KLT-08`)
restent non construites — voir chaque `modules/MODULES_STATUS.md`.
