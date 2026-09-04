# KLT-0007 — KLT-08 Responsable qualité, conformité & audit réseau — Référentiel canonique

```
WORKSTREAM = KLT
KLT-0001..0006 = FROZEN
KLT-0007 = AUTHORIZED = TRUE (ce ticket) — portée limitée au RÉFÉRENTIEL
(compétences + structure indicative), PAS aux modules — décision Founder
du 2026-09-04 ("un seul référentiel canonique d'abord").
KLT-08 MODULE CONTENT BUILD = NOT_AUTHORIZED
METHOD = AUDIT -> FRONTIÈRE KLT-04/M12-M13 -> COMPETENCY MAP -> STRUCTURE
INDICATIVE -> TRAÇABILITÉ -> REVIEW -> FREEZE
DB_MUTATION = FALSE / RUNTIME_BINDING = FALSE / SEED_MUTATION = FALSE /
FAKE_COMPLIANCE = FALSE
STOP_AFTER_DELIVERY = TRUE
```

## Avertissement de source — identique à `KLT-0005`/`KLT-0006`

`KLT-08` n'a ni legacy ni détail module-par-module dans le master plan
tel que résumé par `KLT-0001` — seulement intitulé, type, statut `NEW`,
niveau, priorité, domaine de dépendance. La carte de compétences
ci-dessous est **`PROPOSED`**, dérivée par Claude, jamais présentée comme
extraite d'un détail source que je n'ai pas.

---

## 1. AUDIT

### 1.1 Métier cible

**Responsable qualité, conformité & audit réseau** (`KLT-0001` §2, ligne
8) — type `Spécialisation pro/interne`, statut `NEW`, niveau `Avancé`,
priorité `P2`, dépendance nommée : `Compliance / audits / formation
opérateurs`. Seule des 3 formations planifiées dont le libellé porte
explicitement **"interne"** — signal réel retenu dans `KLT-0001` §3
(le plus net indice `INTERNAL` de tout le master plan pour ces trois
formations, sans pour autant trancher officiellement leur `contexts`).

### 1.2 État réel de Compliance dans Academy (`OBSERVED`)

`KLT-0001` §4 : Compliance et audits **n'existent pas comme donnée
structurée** dans `backend/` (confirmé aussi localement par les en-têtes
de `KLT-04`/M12 et M13, qui portent chacun `NOT_IMPLEMENTED comme donnée
structurée en Academy`). `NOT_IMPLEMENTED`, pas `NOT_CONNECTED` : la
différence est réelle — ici il n'existe même pas de système externe
identifié auquel se raccorder un jour, contrairement à Observatory ou
Network qui sont au moins nommés comme systèmes séparés potentiels.

### 1.3 Frontière à examiner avant construction — `KLT-04`/M12 et M13

Lus intégralement pour ce ticket :

- **`KLT-04`/M12** ("Conformité et responsabilité") — conformité **d'une
  association unique** (accessibilité, fiscalité, statut bénévole),
  avec une exigence de traçabilité ("documenter, pas seulement traiter
  de fait"). Échelle : une structure.
- **`KLT-04`/M13** ("Auditer une association / audit de gouvernance") —
  méthode d'audit **d'une association unique**, avec une discipline
  explicite déjà posée : *l'audit recommande, il ne décide pas*
  (`ROLE_BOUNDARIES` de M13). Échelle : une structure.

`KLT-08` porte, par son intitulé et sa dépendance nommée ("audits /
formation opérateurs"), sur une échelle **réseau** — plusieurs
opérateurs/associations à la fois, avec une dimension supplémentaire
absente de `KLT-04` : **former les opérateurs** aux exigences (pas
seulement les auditer après coup). **Verdict : le recouvrement de
méthode est réel (même discipline d'audit — vérifier, ne pas
complaire, recommander sans décider) mais l'unité d'analyse diffère**
(une structure vs un réseau de structures) et une compétence
(formation des opérateurs) n'existe dans aucune des deux formations
`KLT-04` déjà construites. `KLT-08` **réutilise** la méthode d'audit de
`KLT-04`/M13 (héritage explicite, pas réinvention) et l'**étend** à
l'agrégation multi-structures et à la formation — il ne la réécrit pas
sous un autre nom. Aucune fusion ni renommage de `KLT-04`/M12-M13
nécessaire.

### 1.4 Limites du rôle — ce que le métier n'est PAS

- **Ne conduit pas** l'audit d'une association individuelle isolée en
  tant que tel — c'est `KLT-04`/M13 (bien que `KLT-08` en réutilise la
  méthode, à l'échelle réseau).
- **Ne déploie pas** d'opérateurs sur le terrain — c'est `KLT-07`
  (référentiel `KLT-0006`).
- **N'a pas** d'autorité de gouvernance sur le réseau — l'audit
  recommande, il ne décide pas (hérité explicitement de `KLT-04`/M13,
  appliqué à l'échelle réseau).
- **Ne gère pas** de projet ni de partenariat institutionnel individuel
  — `KLT-02`/`KLT-03`.

### 1.5 Contexte de la formation

`PUBLIC/EXTERNAL/BRIDGE = UNRESOLVED` (`KLT-0001` §3) — mais avec un
indice `INTERNAL` plus net que `KLT-06`/`07` (le libellé "pro/interne"
lui-même). Ce référentiel **ne tranche pas** : reporté `UNRESOLVED`,
avec cet indice explicitement noté pour la décision Founder à venir.

---

## 2. CARTE DE COMPÉTENCES (`PROPOSED`)

| # | Compétence | Constructible aujourd'hui ? |
|---|---|---|
| C1 | Distinguer audit d'association et audit réseau (échelle, méthode, unité d'analyse — frontière `KLT-04`/M12-M13) | **Oui** — pose explicitement la frontière du §1.3 |
| C2 | Concevoir une grille d'audit à l'échelle réseau, héritée de la méthode `KLT-04`/M13 et étendue au multi-opérateurs | **Oui** — méthode, extension documentée d'une méthode déjà réelle |
| C3 | Consolider des résultats d'audits individuels en une vue réseau | **Oui, à un niveau méthode** — l'agrégation de vraies données de conformité reste bloquée (lien C4) |
| C4 | Suivre l'état réel de conformité réseau agrégé (statut par opérateur) | **Non** — `UNRESOLVED`, `Compliance` non implémentée comme donnée structurée |
| C5 | Former des opérateurs aux exigences de conformité | **Oui** — méthode de conception de formation, compétence absente de `KLT-04`, propre à `KLT-08` |
| C6 | Rédiger des recommandations réseau actionnables sans dépasser le rôle d'audit | **Oui** — hérite directement la discipline `ROLE_BOUNDARIES` de `KLT-04`/M13, appliquée à l'échelle réseau |
| C7 | Documenter et escalader une non-conformité réseau au bon niveau de gouvernance | **Oui** — méthode, lien avec `KLT-07`/C7 (remontée d'incident) et `KLT-04`/M12 (escalade CA) |

**Synthèse** : 6 compétences sur 7 constructibles à un niveau
référentiel/méthode ; 1 seule (`C4`) bloquée — le suivi factuel agrégé de
conformité réelle, qui requiert une donnée `Compliance` structurée
inexistante aujourd'hui, pas seulement non connectée.

---

## 3. STRUCTURE INDICATIVE DE MODULES (noms et compétences uniquement — contenu `À produire`, hors scope)

| Module (indicatif) | Compétence(s) | Niveau éval indicatif | Statut de construction |
|---|---|---|---|
| M01 | Audit d'association vs audit réseau — poser la frontière et l'échelle | C1 | N1 | `BUILDABLE` |
| M02 | Concevoir une grille d'audit réseau (héritage `KLT-04`/M13) | C2 | N2 | `BUILDABLE` |
| M03 | Consolider des audits individuels en une vue réseau | C3 | N2 | `BUILDABLE` (agrégation de données réelles bloquée) |
| M04 | Suivre la conformité réseau réelle agrégée | C4 | N2/N3 | `BLOCKED` — Compliance non implémentée |
| M05 | Former des opérateurs aux exigences de conformité | C5 | N2 | `BUILDABLE` |
| M06 | Recommander sans décider — la discipline d'audit à l'échelle réseau | C6 | N2 | `BUILDABLE` |
| M07 | Documenter et escalader une non-conformité réseau | C7 | N2 | `BUILDABLE` |

Le chiffre indicatif du master plan ("8 modules") reste `UNVERIFIED` —
7 compétences réelles identifiées ici, comme pour `KLT-06`/`07`.

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

## 5. Dépendances Kiltikonet (`KLT-08` scope)

| Dépendance | Modules concernés | Classification |
|---|---|---|
| Compliance / audits | M04 (cœur factuel), M03 (agrégation de données réelles) | `NOT_IMPLEMENTED` comme donnée structurée en Academy |
| Méthode d'audit `KLT-04`/M13 | M02, M06 (héritage explicite) | `ACADEMY_LOCAL_IMPLEMENTATION` — réel, contenu existant réutilisé par référence, jamais copié |
| FREK | Preuve d'apprentissage (tous modules `BUILDABLE`) | `ACADEMY_LOCAL_IMPLEMENTATION` — réel |

## 6. Ce qui devra être fait avant le build des modules

1. Décision Founder sur `PUBLIC/EXTERNAL/BRIDGE` (§1.5) — `UNRESOLVED`,
   avec l'indice `INTERNAL` du libellé à trancher explicitement.
2. Décision Founder : construire 6/7 compétences (tout sauf `C4`) comme
   premier périmètre de `KLT-08`, en laissant `M04` explicitement `À
   produire ultérieurement`.
3. Confirmer que la frontière avec `KLT-04`/M12-M13 posée en §1.3 (héritage
   de méthode, extension d'échelle, pas de duplication) est celle voulue
   par le Founder avant tout build.

## REVIEW

- `NO_DB_MUTATION` / `NO_RUNTIME_BINDING` / `NO_SEED_MUTATION` — aucun
  code touché.
- `NO_FAKE_COMPLIANCE` — aucune donnée de conformité simulée ; `M04`
  explicitement `BLOCKED`, pas construit, pas contourné.
- `NO_KLT08_MODULE_CONTENT_BUILD` — seuls noms de modules indicatifs et
  carte de compétences produits.
- `NO_KLT04_M12_M13_MUTATION` — `KLT-04`/M12 et M13 lus, jamais modifiés,
  jamais copiés (héritage par référence uniquement).

```bash
git status --short   # expect: only this new doc
```

## FREEZE

**`KLT-08_CANONICAL_REFERENTIAL = FROZEN` (compétences + structure
indicative uniquement)**. 7/7 compétences ont un module indicatif nommé,
6/7 constructibles dès aujourd'hui. **Les modules eux-mêmes restent `À
produire`.**

`STOP = TRUE.` Build de modules `KLT-08` non commencé, en attente
d'autorisation explicite et de décision sur §1.5/§6.
