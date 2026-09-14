# KLT-08 — Responsable qualité, conformité & audit réseau — Référentiel canonique + Blueprints

```
Référentiel gelé par KLT-0007 ; contexts et périmètre buildable décidés
par KLT-0008. Ce document reprend ces décisions sans les rouvrir, et
détaille les blueprints des 6 modules effectivement construits.
STRUCTURAL_STATUS = COMPLETE — 7/7 compétences construites (mise à jour
2026-09-07 : C4 reclassifiée BUILT après re-vérification — le Network
Kiltikonet réel porte en fait des collections de conformité réelles).
Voir modules/MODULES_STATUS.md.
FULLY_COMPLETE = FALSE — distinct de STRUCTURAL_STATUS, signifie une
connexion live Academy↔Kiltikonet-Aout2026 en production, qui n'existe
toujours pas (Academy n'a aucun client ni credentials appelant cette
API). Ne jamais confondre "module construit sur un schéma réel vérifié"
et "connecté en direct à Academy".
contexts = [INTERNAL] (KLT-0008 §2). BRIDGE non retenu.
```

## Avertissement central de cette formation

`KLT-08` a longtemps couvert 6 des 7 compétences identifiées par
`KLT-0007` — seule `C4` (suivi de conformité réseau agrégée réelle)
restait `BLOCKED`, la classification d'origine (`NOT_IMPLEMENTED`,
"aucun système externe identifié à connecter un jour") reposant sur une
recherche qui n'avait pas trouvé de système de conformité réel.
**Mise à jour du 2026-09-07** : une re-vérification, explicitement
autorisée par le Founder (`docs/klt/README.md`,
`KLT_09_20_RECONCILIATION.md` §Re-vérification), a trouvé que le
Network Kiltikonet réel (`cultureconnectorg/Kiltikonet-Aout2026`,
commit `bb64ce7`) porte bien des collections de conformité réelles
(`network_compliance_records`, `network_audits`) — la classification
d'origine ("aucun système identifié") était donc trop pessimiste, pas
fausse par excès d'optimisme. Ce qui reste vrai et inchangé : **Academy
n'a aucun client ni credentials appelant cette API en direct** — la
reclassification est donc `PRODUCT_CODE_REAL_VERIFIED,
NOT_CONNECTED_TO_ACADEMY_RUNTIME`, jamais une prétention de connexion
live. `C4` est désormais construite sur cette base réelle vérifiée,
sans jamais fabriquer une requête live qui n'existe pas.

## Métier cible

**Responsable qualité, conformité & audit réseau** — niveau `Avancé`,
priorité `P2` (`KLT-0001` §2). Formation `NEW`, sans legacy. Seule des
trois formations planifiées portant explicitement la mention "interne"
dans son libellé.

## Responsabilités réelles (périmètre buildable)

Distinguer audit d'association et audit réseau · concevoir une grille
d'audit à l'échelle réseau, héritée de la méthode `KLT-04`/M13 · consolider
des résultats d'audits individuels en une vue réseau · former des
opérateurs aux exigences de conformité · rédiger des recommandations
réseau actionnables sans dépasser le rôle d'audit · documenter et
escalader une non-conformité réseau au bon niveau de gouvernance.

Suivre l'état réel de conformité réseau agrégé (schéma réel vérifié du
Network, non connecté en direct à Academy).

## Limites du rôle — ce que le métier n'est PAS

Reprises de `KLT-0007` §1.4 : ne conduit pas l'audit d'une association
individuelle isolée en tant que tel (`KLT-04`/M13 reste la compétence de
référence, même si `KLT-08` en réutilise la méthode par héritage), ne
déploie pas d'opérateurs sur le terrain (`KLT-07`), n'a pas d'autorité de
gouvernance sur le réseau (l'audit recommande, il ne décide pas — hérité
explicitement de `KLT-04`/M13), ne gère pas de projet ni de partenariat
institutionnel individuel (`KLT-02`/`KLT-03`).

## Frontière avec `KLT-04`/M12-M13 (rappel de `KLT-0007` §1.3)

`KLT-04`/M12 (conformité) et M13 (audit de gouvernance) portent sur une
**association unique**. `KLT-08` réutilise **par héritage explicite** la
méthode d'audit de M13 (vérifier, ne pas complaire, recommander sans
décider) et l'**étend** à l'agrégation multi-opérateurs et à la formation
des opérateurs — une compétence absente de `KLT-04`. Aucune fusion ni
renommage de `KLT-04`/M12-M13.

## Publics / Contextes

`contexts = [INTERNAL]` (`KLT-0008` §2) — signal le plus net des trois
formations (libellé "pro/interne"). `BRIDGE` non retenu (niveau
`Avancé`).

## Compétences (7) et modules — statut de construction

| # | Compétence | Module | Statut |
|---|---|---|---|
| C1 | Distinguer audit d'association et audit réseau | M01 | `BUILT` |
| C2 | Concevoir une grille d'audit réseau, héritée de `KLT-04`/M13 | M02 | `BUILT` |
| C3 | Consolider des résultats d'audits individuels en une vue réseau | M03 | `BUILT` |
| C4 | Suivre l'état réel de conformité réseau agrégé | M04 | `BUILT` |
| C5 | Former des opérateurs aux exigences de conformité | M05 | `BUILT` |
| C6 | Recommander sans décider — discipline d'audit à l'échelle réseau | M06 | `BUILT` |
| C7 | Documenter et escalader une non-conformité réseau | M07 | `BUILT` |

**7/7 compétences construites** (mise à jour 2026-09-07). Numérotation
`KLT-0007` conservée intacte — voir `modules/MODULES_STATUS.md`.

## Blueprints (modules construits uniquement)

| Module | WHY_THIS_MODULE_EXISTS | ASSESSED | WHAT_REAL_OUTPUT |
|---|---|---|---|
| M01 | Confondre audit d'association et audit réseau produit une méthode mal calibrée à son objet | N1 | Note de cadrage échelle |
| M02 | Une grille d'audit réseau construite sans hériter d'une méthode déjà validée réinvente ce qui existe déjà | N2 | Grille d'audit réseau |
| M03 | Consolider sans méthode produit une vue réseau biaisée par l'opérateur le plus visible | N2 | Vue consolidée réseau |
| M04 | Une conformité réseau non suivie dans la durée laisse s'installer des dérives invisibles entre deux audits | N2 | Fiche de suivi de conformité |
| M05 | Former sans méthode produit des opérateurs qui connaissent la règle sans savoir l'appliquer | N2 | Support de formation opérateurs |
| M06 | Une recommandation qui dépasse le rôle d'audit menace la légitimité même de l'audit | N2 | Note de recommandations |
| M07 | Une non-conformité réseau non escaladée au bon niveau reste sans suite | N2/N3 | Rapport de non-conformité réseau |

Cohérence transversale vérifiée : progression N1→N2/N3 monotone sur les
7 modules construits, aucune compétence testée sans module.
