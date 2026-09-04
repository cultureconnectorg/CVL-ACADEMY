# KLT-06 — Analyste Observatory / Cultural Data Analyst — Référentiel canonique + Blueprints

```
Référentiel gelé par KLT-0005 ; contexts et périmètre buildable décidés
par KLT-0008. Ce document reprend ces décisions sans les rouvrir, et
détaille les blueprints des 5 modules effectivement construits.
STRUCTURAL_STATUS = PARTIAL — 5/7 compétences construites, 2/7
(C5, C6) BLOCKED (Observatory NOT_CONNECTED). Voir modules/
MODULES_STATUS.md.
contexts = [EXTERNAL] (KLT-0008 §2). BRIDGE non retenu.
```

## Avertissement central de cette formation

`KLT-06` est la première formation Kiltikonet dont le référentiel
lui-même n'est **pas** complet à 100% des compétences nommées par le
master plan — 2 des 7 compétences identifiées (`C5`, `C6`) dépendent
d'un accès Observatory réel, qui n'existe pas dans ce repo
(`NOT_CONNECTED`, `KLT-0001` §4). Ce n'est pas une lacune cachée : c'est
une limite structurelle nommée dès `KLT-0005` et confirmée par
`KLT-0008`. Ce package couvre les 5 compétences réellement
constructibles ; il ne prétend pas couvrir les 2 autres.

## Métier cible

**Analyste Observatory / Cultural Data Analyst** — niveau `Avancé`,
priorité `P1` (`KLT-0001` §2). Pas de correspondance ROME calibrée dans
ce repo (formation `NEW`, sans legacy — contrairement à `KLT-01`→`05`).

## Responsabilités réelles (périmètre buildable)

Comprendre l'objet et la méthode d'un observatoire de données
culturelles · évaluer la provenance et la fiabilité d'un signal ·
formuler une spécification de besoin de données pour un tiers · appliquer
une éthique et une confidentialité des données communautaires · restituer
une analyse à un public non spécialiste.

**Hors périmètre de ce package** (compétences bloquées, non construites) :
construire un tableau de bord à partir de données Observatory réelles
(`C5`) ; interpréter des signaux territoriaux réels pour appuyer une
décision (`C6`).

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
| C5 | Construire un tableau de bord à partir de données Observatory réelles | M05 | `BLOCKED` — non construit |
| C6 | Interpréter des signaux territoriaux réels pour appuyer une décision | M06 | `BLOCKED` — non construit |
| C7 | Restituer une analyse à un public non spécialiste | M07 | `BUILT` |

**5/7 compétences construites.** La numérotation `M01`-`M07` de
`KLT-0005` est conservée intacte (y compris les trous `M05`/`M06`) pour
rester traçable au référentiel gelé — voir `modules/MODULES_STATUS.md`.

## Blueprints (modules construits uniquement)

| Module | WHY_THIS_MODULE_EXISTS | ASSESSED | WHAT_REAL_OUTPUT |
|---|---|---|---|
| M01 | Sans comprendre ce qu'un observatoire capte réellement, toute lecture de donnée culturelle est mal cadrée | N1 | Note de cadrage méthode |
| M02 | Une donnée dont la provenance n'est pas évaluée peut orienter une décision sur une base fausse | N1/N2 | Grille de provenance |
| M03 | Un besoin de données mal spécifié produit une réponse inexploitable pour celui qui la demande | N2 | Fiche de spécification |
| M04 | Manipuler des données sur une communauté sans cadre éthique expose à une extraction non consentie | N2 | Grille éthique/confidentialité |
| M07 | Une analyse juste mais mal restituée ne sert à personne | N2 | Support de restitution |

Cohérence transversale vérifiée : progression N1→N2 monotone sur les 5
modules construits, aucune compétence testée sans module.
