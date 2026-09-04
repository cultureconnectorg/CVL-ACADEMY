# KLT-0006 — KLT-07 Responsable déploiement territorial culturel — Référentiel canonique

```
WORKSTREAM = KLT
KLT-0001..0005 = FROZEN
KLT-0006 = AUTHORIZED = TRUE (ce ticket) — portée limitée au RÉFÉRENTIEL
(compétences + structure indicative), PAS aux modules — décision Founder
du 2026-09-04 ("un seul référentiel canonique d'abord").
KLT-07 MODULE CONTENT BUILD = NOT_AUTHORIZED
METHOD = AUDIT -> FRONTIÈRE KLT-04/M11 -> COMPETENCY MAP -> STRUCTURE
INDICATIVE -> TRAÇABILITÉ -> REVIEW -> FREEZE
DB_MUTATION = FALSE / RUNTIME_BINDING = FALSE / SEED_MUTATION = FALSE /
FAKE_NETWORK = FALSE
STOP_AFTER_DELIVERY = TRUE
```

## Avertissement de source — identique à `KLT-0005`

`KLT-07` n'a ni legacy ni détail module-par-module dans le master plan
tel que résumé par `KLT-0001` — seulement intitulé, type, statut `NEW`,
niveau, priorité, domaine de dépendance. La carte de compétences
ci-dessous est **`PROPOSED`**, dérivée par Claude, jamais présentée comme
extraite d'un détail source que je n'ai pas.

---

## 1. AUDIT

### 1.1 Métier cible

**Responsable déploiement territorial culturel** (`KLT-0001` §2, ligne 7)
— type `Spécialisation professionnelle`, statut `NEW`, niveau `Avancé`,
priorité `P2`, dépendance nommée : `Network / territoires / opérateurs /
licences`.

### 1.2 État réel de Network dans Academy (`OBSERVED`)

`KLT-0001` §4 : **zéro footprint** — aucune collection `territories`/
`operators`/`licenses` dans `backend/`. `NOT_CONNECTED` en Academy.
`EXTERNAL_EVIDENCE_NOT_AUDITED` externe — Network vit vraisemblablement
dans un système séparé auquel cette session n'a pas accès.

### 1.3 Frontière à examiner avant construction — `KLT-04`/M11

`KLT-04`/M11 ("Gouvernance territoriale — réseau multi-opérateurs",
lu intégralement pour ce ticket) esquisse déjà, **du point de vue d'une
association qui envisage de devenir opérateur relais**, un modèle de
coordination réseau (vs subordination) — une compétence de *conception
de gouvernance*, exercée depuis l'intérieur d'une seule structure, sur
la base d'une évaluation de sa propre maturité organisationnelle.

`KLT-07` est **structurellement différent** : c'est le rôle qui, à
l'échelle du réseau Kiltikonet dans son ensemble (pas depuis une seule
association), **exécute** le déploiement — onboarding d'opérateurs,
suivi de licences, couverture territoriale, gestion opérationnelle de la
relation avec des opérateurs déjà en place. `KLT-04`/M11 conçoit un
modèle de gouvernance vu d'une association ; `KLT-07` opère le réseau vu
du centre. **Verdict : frontière réelle et non redondante** — `KLT-04`/
M11 reste `governance model design (single-org viewpoint)`, `KLT-07`
devient `network operations (network-wide viewpoint)`. Aucune fusion ni
renommage de `KLT-04`/M11 nécessaire.

### 1.4 Limites du rôle — ce que le métier n'est PAS

- **Ne conçoit pas** de modèle de gouvernance pour une association — 
  c'est `KLT-04`/M11 (point de vue association).
- **N'anime pas** de dispositif de médiation terrain — c'est `KLT-01`.
- **Ne gère pas** de budget de projet culturel individuel — c'est
  `KLT-02`.
- **Ne mène pas** d'audit qualité/conformité réseau formel — c'est
  `KLT-08` (référentiel `KLT-0007`, distinct — voir aussi sa propre
  frontière avec `KLT-04`/M12-M13).
- **N'a pas** d'autorité de gouvernance sur le réseau lui-même — le
  déploiement exécute une politique réseau, il ne la décide pas.

### 1.5 Contexte de la formation

`PUBLIC/EXTERNAL/BRIDGE = UNRESOLVED` (`KLT-0001` §3), reporté tel quel —
non tranché par ce référentiel.

---

## 2. CARTE DE COMPÉTENCES (`PROPOSED`)

| # | Compétence | Constructible aujourd'hui ? |
|---|---|---|
| C1 | Comprendre l'écosystème territorial Kiltikonet (opérateurs, territoires, licences, couverture) | **Oui** — littératie/méthode |
| C2 | Distinguer déploiement opérationnel réseau et conception de gouvernance associative (frontière `KLT-04`/M11) | **Oui** — c'est la compétence qui pose explicitement la frontière du §1.3 |
| C3 | Structurer un processus d'onboarding d'un nouvel opérateur territorial (étapes, critères, documents) | **Oui** — méthode/processus, illustrable sans données Network réelles |
| C4 | Suivre et documenter l'état réel de couverture territoriale (licences actives, statut, capacité) | **Non** — `UNRESOLVED`, requiert un accès Network réel |
| C5 | Gérer une relation opérateur (support, remontée de besoin, tension) | **Oui** — s'appuie sur des compétences relationnelles déjà posées ailleurs dans le corpus (`KLT-01`/M05, M07), transposées au contexte opérateur |
| C6 | Évaluer la faisabilité méthodologique d'une extension territoriale (ressources, prérequis, risques) | **Oui, à un niveau méthode** — l'ancrage sur des données réelles de couverture reste bloqué (lien C4) |
| C7 | Documenter et remonter un incident de déploiement au niveau réseau (lien `KLT-08`, `KLT-04`) | **Oui** — méthode de remontée/documentation |

**Synthèse** : 6 compétences sur 7 constructibles à un niveau
référentiel/méthode ; 1 seule (`C4`) bloquée sur un accès Network réel —
un écart bien plus favorable que `KLT-06`, car le cœur de ce métier
(processus, relation, méthode d'évaluation) ne dépend pas d'une lecture
de données système comme celui de `KLT-06`. Seul le **suivi factuel de
couverture réelle** reste hors de portée.

---

## 3. STRUCTURE INDICATIVE DE MODULES (noms et compétences uniquement — contenu `À produire`, hors scope)

| Module (indicatif) | Compétence(s) | Niveau éval indicatif | Statut de construction |
|---|---|---|---|
| M01 | L'écosystème territorial Kiltikonet — opérateurs, territoires, licences | C1 | N1 | `BUILDABLE` |
| M02 | Déploiement réseau vs gouvernance associative — poser la frontière | C2 | N1 | `BUILDABLE` |
| M03 | Structurer l'onboarding d'un opérateur territorial | C3 | N2 | `BUILDABLE` |
| M04 | Suivre la couverture territoriale réelle | C4 | N2/N3 | `BLOCKED` — Network non connecté |
| M05 | Gérer la relation opérateur au quotidien | C5 | N2 | `BUILDABLE` |
| M06 | Évaluer la faisabilité d'une extension territoriale | C6 | N2 | `BUILDABLE` (ancrage données réelles bloqué) |
| M07 | Documenter et remonter un incident de déploiement | C7 | N2 | `BUILDABLE` |

Le chiffre indicatif du master plan ("8 modules") reste `UNVERIFIED` —
7 compétences réelles identifiées ici, comme pour `KLT-06`.

**Aucun contenu de module n'est écrit ici.**

---

## 4. TRAÇABILITÉ (niveau référentiel)

| Compétence | Module indicatif | Statut |
|---|---|---|
| C1 | M01 | `BUILDABLE` |
| C2 | M02 | `BUILDABLE` |
| C3 | M03 | `BUILDABLE` |
| C4 | M04 | `BLOCKED` |
| C5 | M05 | `BUILDABLE` |
| C6 | M06 | `BUILDABLE` |
| C7 | M07 | `BUILDABLE` |

**Couverture** : 7/7 compétences ont un module indicatif nommé, zéro
compétence orpheline. 6/7 réellement constructibles aujourd'hui.

## 5. Dépendances Kiltikonet (`KLT-07` scope)

| Dépendance | Modules concernés | Classification |
|---|---|---|
| Network | M04 (cœur factuel), M06 (ancrage données) | `NOT_CONNECTED` en Academy / `EXTERNAL_EVIDENCE_NOT_AUDITED` externe |
| Gouvernance (frontière `KLT-04`/M11) | M02 | `NOT_IMPLEMENTED` comme donnée structurée, traité ici comme frontière conceptuelle uniquement |
| FREK | Preuve d'apprentissage (M01-M03, M05-M07) | `ACADEMY_LOCAL_IMPLEMENTATION` — réel |

## 6. Ce qui devra être fait avant le build des modules

1. Décision Founder sur `PUBLIC/EXTERNAL/BRIDGE` (§1.5) — `UNRESOLVED`.
2. Décision Founder : construire 6/7 compétences (tout sauf `C4`) comme
   premier périmètre de `KLT-07`, en laissant `M04` explicitement `À
   produire ultérieurement` — ou attendre un accès Network réel.
3. Confirmer la frontière `KLT-04`/M11 posée en §1.3 est celle voulue
   par le Founder avant tout build.

## REVIEW

- `NO_DB_MUTATION` / `NO_RUNTIME_BINDING` / `NO_SEED_MUTATION` — aucun
  code touché.
- `NO_FAKE_NETWORK` — aucune donnée Network simulée ; `M04` explicitement
  `BLOCKED`, pas construit, pas contourné.
- `NO_KLT07_MODULE_CONTENT_BUILD` — seuls noms de modules indicatifs et
  carte de compétences produits.
- `NO_KLT04_M11_MUTATION` — `KLT-04`/M11 lu, jamais modifié.

```bash
git status --short   # expect: only this new doc
```

## FREEZE

**`KLT-07_CANONICAL_REFERENTIAL = FROZEN` (compétences + structure
indicative uniquement)**. 7/7 compétences ont un module indicatif nommé,
6/7 constructibles dès aujourd'hui. **Les modules eux-mêmes restent `À
produire`.**

`STOP = TRUE.` Build de modules `KLT-07` non commencé, en attente
d'autorisation explicite et de décision sur §1.5/§6.
