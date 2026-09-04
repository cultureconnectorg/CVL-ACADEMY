# KLT-07 — Responsable déploiement territorial culturel — Référentiel canonique + Blueprints

```
Référentiel gelé par KLT-0006 ; contexts et périmètre buildable décidés
par KLT-0008. Ce document reprend ces décisions sans les rouvrir, et
détaille les blueprints des 6 modules effectivement construits.
STRUCTURAL_STATUS = PARTIAL — 6/7 compétences construites, 1/7 (C4)
BLOCKED (Network NOT_CONNECTED). Voir modules/MODULES_STATUS.md.
contexts = [INTERNAL] (KLT-0008 §2). BRIDGE non retenu.
```

## Avertissement central de cette formation

`KLT-07` couvre 6 des 7 compétences identifiées par `KLT-0006` — seule
`C4` (suivi de couverture territoriale réelle) reste `BLOCKED`, faute
d'accès Network réel (`NOT_CONNECTED`, `KLT-0001` §4). Contrairement à
`KLT-06`, l'essentiel du métier (processus, relation, méthode
d'évaluation) ne dépend pas de données système — seul le suivi factuel
de couverture en dépend.

## Métier cible

**Responsable déploiement territorial culturel** — niveau `Avancé`,
priorité `P2` (`KLT-0001` §2). Formation `NEW`, sans legacy.

## Responsabilités réelles (périmètre buildable)

Comprendre l'écosystème territorial Kiltikonet · distinguer déploiement
opérationnel réseau et conception de gouvernance associative · structurer
l'onboarding d'un nouvel opérateur territorial · gérer une relation
opérateur au quotidien · évaluer la faisabilité méthodologique d'une
extension territoriale · documenter et remonter un incident de
déploiement.

**Hors périmètre de ce package** : suivre et documenter l'état réel de
couverture territoriale (licences actives, statut, capacité) — `C4`,
`BLOCKED`.

## Limites du rôle — ce que le métier n'est PAS

Reprises de `KLT-0006` §1.4 : ne conçoit pas de modèle de gouvernance
pour une association (`KLT-04`/M11, point de vue association — voir
§Frontière), n'anime pas de médiation terrain (`KLT-01`), ne gère pas de
budget de projet individuel (`KLT-02`), ne mène pas d'audit qualité/
conformité réseau (`KLT-08`), n'a pas d'autorité de gouvernance sur le
réseau lui-même.

## Frontière avec `KLT-04`/M11 (rappel de `KLT-0006` §1.3)

`KLT-04`/M11 esquisse un modèle de gouvernance réseau **depuis le point
de vue d'une association** qui envisage de devenir opérateur relais.
`KLT-07` opère le réseau **depuis le point de vue du centre** —
onboarding, suivi opérationnel, gestion de la relation. Les deux
formations partagent le même cas (Mémoire Vive candidate à devenir
opérateur relais) sans se dupliquer : `KLT-04`/M11 conçoit, `KLT-07`
exécute.

## Publics / Contextes

`contexts = [INTERNAL]` (`KLT-0008` §2) — e-learning en canal interne
uniquement, pas de canal externe/physique. `BRIDGE` non retenu (niveau
`Avancé`).

## Compétences (7) et modules — statut de construction

| # | Compétence | Module | Statut |
|---|---|---|---|
| C1 | Comprendre l'écosystème territorial Kiltikonet | M01 | `BUILT` |
| C2 | Distinguer déploiement opérationnel réseau et gouvernance associative | M02 | `BUILT` |
| C3 | Structurer l'onboarding d'un nouvel opérateur territorial | M03 | `BUILT` |
| C4 | Suivre l'état réel de couverture territoriale | M04 | `BLOCKED` — non construit |
| C5 | Gérer une relation opérateur au quotidien | M05 | `BUILT` |
| C6 | Évaluer la faisabilité d'une extension territoriale | M06 | `BUILT` |
| C7 | Documenter et remonter un incident de déploiement | M07 | `BUILT` |

**6/7 compétences construites.** Numérotation `KLT-0006` conservée
intacte (trou en `M04`) — voir `modules/MODULES_STATUS.md`.

## Blueprints (modules construits uniquement)

| Module | WHY_THIS_MODULE_EXISTS | ASSESSED | WHAT_REAL_OUTPUT |
|---|---|---|---|
| M01 | Sans comprendre l'écosystème territorial, un déploiement agit sans repères | N1 | Note de cadrage écosystème |
| M02 | Confondre déploiement opérationnel et conception de gouvernance produit une intrusion dans le mandat d'une association | N1 | Note de frontière |
| M03 | Un onboarding non structuré expose le réseau à des opérateurs mal préparés | N2 | Dossier d'onboarding |
| M05 | Une relation opérateur mal gérée dégrade la confiance envers le réseau | N2 | Journal de relation opérateur |
| M06 | Valider une extension sans évaluer sa faisabilité réelle expose le réseau à un échec évitable | N2 | Note de faisabilité |
| M07 | Un incident de déploiement non documenté empêche toute leçon future au niveau réseau | N2/N3 | Rapport d'incident réseau |

Cohérence transversale vérifiée : progression N1→N2/N3 monotone sur les
6 modules construits, aucune compétence testée sans module.
