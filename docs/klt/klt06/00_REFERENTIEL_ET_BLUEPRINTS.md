# KLT-06 — Analyste Observatory / Cultural Data Analyst — Référentiel canonique + Blueprints

```
Référentiel gelé par KLT-0005 ; contexts et périmètre buildable décidés
par KLT-0008. Ce document reprend ces décisions sans les rouvrir, et
détaille les blueprints des 5 modules effectivement construits.
STRUCTURAL_STATUS = COMPLETE — 7/7 compétences construites (mise à
jour 2026-09-07 : C5/C6 reclassifiées BUILT après re-vérification du
système Observatory réel dans Kiltikonet-Aout2026). Voir modules/
MODULES_STATUS.md.
FULLY_COMPLETE = FALSE — ce champ reste distinct de STRUCTURAL_STATUS
et signifie une connexion live Academy↔Kiltikonet-Aout2026 en
production, qui n'existe toujours pas (Academy n'a aucun client ni
credentials appelant cette API). Ne jamais confondre "module construit
sur un schéma réel vérifié" et "connecté en direct à Academy" — ce champ
ne devient TRUE que le jour où un tel client réel existe, par un ticket
dédié.
contexts = [EXTERNAL] (KLT-0008 §2). BRIDGE non retenu.
```

## Avertissement central de cette formation

`KLT-06` a longtemps été la première formation Kiltikonet dont le
référentiel n'était pas complet à 100% des compétences nommées par le
master plan — 2 des 7 compétences (`C5`, `C6`) dépendaient d'un accès
Observatory dont l'existence n'avait pas été vérifiée (`NOT_CONNECTED`,
`KLT-0001` §4). **Mise à jour du 2026-09-07** : une re-vérification,
explicitement autorisée par le Founder (`docs/klt/README.md`,
`KLT_09_20_RECONCILIATION.md` §Re-vérification), a confirmé que
l'Observatory Kiltikonet est un **système réel, vérifié** dans le repo
canonique `cultureconnectorg/Kiltikonet-Aout2026` (commit `bb64ce7`) —
routes, RBAC, adaptateurs, tout existe. Ce qui reste vrai et inchangé :
**Academy n'a aucun client ni credentials appelant cette API en
direct** — la reclassification est donc `PRODUCT_CODE_REAL_VERIFIED,
NOT_CONNECTED_TO_ACADEMY_RUNTIME`, jamais une prétention de connexion
live. `C5`/`C6` sont désormais construites sur cette base réelle
vérifiée, sans jamais fabriquer une requête live qui n'existe pas.

## Métier cible

**Analyste Observatory / Cultural Data Analyst** — niveau `Avancé`,
priorité `P1` (`KLT-0001` §2). Pas de correspondance ROME calibrée dans
ce repo (formation `NEW`, sans legacy — contrairement à `KLT-01`→`05`).

## Responsabilités réelles (périmètre buildable, 7/7)

Comprendre l'objet et la méthode d'un observatoire de données
culturelles · évaluer la provenance et la fiabilité d'un signal ·
formuler une spécification de besoin de données pour un tiers · appliquer
une éthique et une confidentialité des données communautaires ·
construire un tableau de bord à partir de données Observatory réelles
(schéma réel vérifié, non connecté en direct à Academy) · interpréter des
signaux territoriaux réels pour appuyer une décision (idem) · restituer
une analyse à un public non spécialiste.

## Limites du rôle — ce que le métier n'est PAS

Reprises telles quelles de `KLT-0005` §1.4 : n'anime pas de médiation
terrain (`KLT-01`), ne gère pas de budget/projet (`KLT-02`), ne négocie
pas de partenariat institutionnel (`KLT-03`), n'a pas d'autorité de
gouvernance (`KLT-04`), n'opère pas la plateforme (`KLT-05`), ne déploie
pas d'opérateurs (`KLT-07`). Livre une analyse et une recommandation,
jamais une décision engageante.

## Publics / Contextes

`contexts = [EXTERNAL]` (`KLT-0008` §2) — e-learning disponible en canal
externe, physique `ELIGIBLE_PENDING_OFFER` (jamais réservable sans offre
réelle). `BRIDGE` non retenu (niveau `Avancé`, pas un point d'entrée du
parcours — `KILTIKONET_PROFESSIONAL_PATHWAY.md`).

## Compétences (7) et modules — statut de construction

| # | Compétence | Module | Statut |
|---|---|---|---|
| C1 | Comprendre l'objet et la méthode d'un observatoire de données culturelles | M01 | `BUILT` |
| C2 | Évaluer la provenance et la fiabilité d'un signal | M02 | `BUILT` |
| C3 | Formuler une spécification de besoin de données pour un tiers | M03 | `BUILT` |
| C4 | Éthique et confidentialité des données communautaires/culturelles | M04 | `BUILT` |
| C5 | Construire un tableau de bord à partir de données Observatory réelles | M05 | `BUILT` |
| C6 | Interpréter des signaux territoriaux réels pour appuyer une décision | M06 | `BUILT` |
| C7 | Restituer une analyse à un public non spécialiste | M07 | `BUILT` |

**7/7 compétences construites** (mise à jour 2026-09-07). La
numérotation `M01`-`M07` de `KLT-0005` est conservée intacte pour rester
traçable au référentiel gelé — voir `modules/MODULES_STATUS.md`.

## Blueprints (modules construits uniquement)

| Module | WHY_THIS_MODULE_EXISTS | ASSESSED | WHAT_REAL_OUTPUT |
|---|---|---|---|
| M01 | Sans comprendre ce qu'un observatoire capte réellement, toute lecture de donnée culturelle est mal cadrée | N1 | Note de cadrage méthode |
| M02 | Une donnée dont la provenance n'est pas évaluée peut orienter une décision sur une base fausse | N1/N2 | Grille de provenance |
| M03 | Un besoin de données mal spécifié produit une réponse inexploitable pour celui qui la demande | N2 | Fiche de spécification |
| M04 | Manipuler des données sur une communauté sans cadre éthique expose à une extraction non consentie | N2 | Grille éthique/confidentialité |
| M05 | Un(e) analyste qui ne sait pas concevoir une maquette sur le schéma réel confond conception et requête live | N2 | Maquette de tableau de bord |
| M06 | Un signal mal interprété peut orienter une décision réseau sur une base fausse | N2 | Note d'interprétation de signal |
| M07 | Une analyse juste mais mal restituée ne sert à personne | N2 | Support de restitution |

Cohérence transversale vérifiée : progression N1→N2 monotone sur les 7
modules construits, aucune compétence testée sans module.
