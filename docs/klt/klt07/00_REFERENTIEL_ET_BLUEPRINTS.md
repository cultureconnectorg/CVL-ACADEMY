# KLT-07 — Responsable déploiement territorial culturel — Référentiel canonique + Blueprints

```
Référentiel gelé par KLT-0006 ; contexts et périmètre buildable décidés
par KLT-0008. Ce document reprend ces décisions sans les rouvrir, et
détaille les blueprints des 6 modules effectivement construits.
STRUCTURAL_STATUS = COMPLETE — 7/7 compétences construites (mise à jour
2026-09-07 : C4 reclassifiée BUILT après re-vérification du système
Network réel dans Kiltikonet-Aout2026). Voir modules/MODULES_STATUS.md.
FULLY_COMPLETE = FALSE — distinct de STRUCTURAL_STATUS, signifie une
connexion live Academy↔Kiltikonet-Aout2026 en production, qui n'existe
toujours pas (Academy n'a aucun client ni credentials appelant cette
API). Ne jamais confondre "module construit sur un schéma réel vérifié"
et "connecté en direct à Academy".
contexts = [INTERNAL] (KLT-0008 §2). BRIDGE non retenu.
```

## Avertissement central de cette formation

`KLT-07` a longtemps couvert 6 des 7 compétences identifiées par
`KLT-0006` — seule `C4` (suivi de couverture territoriale réelle)
restait `BLOCKED`, faute d'un accès Network dont l'existence n'avait
pas été vérifiée (`NOT_CONNECTED`, `KLT-0001` §4). **Mise à jour du
2026-09-07** : une re-vérification, explicitement autorisée par le
Founder (`docs/klt/README.md`, `KLT_09_20_RECONCILIATION.md`
§Re-vérification), a confirmé que le Network Kiltikonet est un
**système réel, vérifié** dans le repo canonique
`cultureconnectorg/Kiltikonet-Aout2026` (commit `bb64ce7`). Ce qui reste
vrai et inchangé : **Academy n'a aucun client ni credentials appelant
cette API en direct** — la reclassification est donc
`PRODUCT_CODE_REAL_VERIFIED, NOT_CONNECTED_TO_ACADEMY_RUNTIME`, jamais
une prétention de connexion live. `C4` est désormais construite sur
cette base réelle vérifiée, sans jamais fabriquer une requête live qui
n'existe pas.

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

Suivre l'état réel de couverture territoriale (schéma réel vérifié du
Network, non connecté en direct à Academy).

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
| C4 | Suivre l'état réel de couverture territoriale | M04 | `BUILT` |
| C5 | Gérer une relation opérateur au quotidien | M05 | `BUILT` |
| C6 | Évaluer la faisabilité d'une extension territoriale | M06 | `BUILT` |
| C7 | Documenter et remonter un incident de déploiement | M07 | `BUILT` |

**7/7 compétences construites** (mise à jour 2026-09-07). Numérotation
`KLT-0006` conservée intacte — voir `modules/MODULES_STATUS.md`.

## Blueprints (modules construits uniquement)

| Module | WHY_THIS_MODULE_EXISTS | ASSESSED | WHAT_REAL_OUTPUT |
|---|---|---|---|
| M01 | Sans comprendre l'écosystème territorial, un déploiement agit sans repères | N1 | Note de cadrage écosystème |
| M02 | Confondre déploiement opérationnel et conception de gouvernance produit une intrusion dans le mandat d'une association | N1 | Note de frontière |
| M03 | Un onboarding non structuré expose le réseau à des opérateurs mal préparés | N2 | Dossier d'onboarding |
| M04 | Un déploiement sans suivi de couverture réel avance à l'aveugle sur ce qui est déjà couvert | N2 | Fiche de suivi de couverture |
| M05 | Une relation opérateur mal gérée dégrade la confiance envers le réseau | N2 | Journal de relation opérateur |
| M06 | Valider une extension sans évaluer sa faisabilité réelle expose le réseau à un échec évitable | N2 | Note de faisabilité |
| M07 | Un incident de déploiement non documenté empêche toute leçon future au niveau réseau | N2/N3 | Rapport d'incident réseau |

Cohérence transversale vérifiée : progression N1→N2/N3 monotone sur les
7 modules construits, aucune compétence testée sans module.
