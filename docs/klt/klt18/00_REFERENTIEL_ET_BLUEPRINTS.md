# KLT-18 — Responsable Communications & Engagement Culturel / Cultural Communications & Engagement Operator — Référentiel canonique + Blueprints

```
Formation NEW construite le 2026-09-07, sur autorisation Founder scopée
(docs/klt/README.md §FOUNDER_AUTHORIZATION_UPDATE, KLT_09_20_
RECONCILIATION.md §KLT-18). Verdict de reconciliation : EXTEND_EXISTING/
hybride, ancrée par référence sur KLT-05/C5 (animation communauté
diaspora), C7 (support/escalades), C9 (lecture de signaux d'engagement).
Ne rouvre pas KLT-05/M05, M07, M09 ; ajoute la matière stratégique de
campagne/communication réellement nouvelle au-delà de l'animation
quotidienne, sur le même principe que FMS-04 Branding spécialisant
FMS-11 Creative Direction.
STRUCTURAL_STATUS = COMPLETE — 5/5 compétences construites.
FULLY_COMPLETE = TRUE — comme KLT-13, aucune compétence de cette
formation ne dépend d'un système externe non connecté : le registre
`skills/SKILL_ID_REGISTRY.md` ne porte aucune ligne `BLOCKED` ni
`BUILT_UNCONNECTED`, donc `fully_complete` se calcule honnêtement à
`TRUE` (même dérivation que KLT-01→05). L'import en base
`db.formations` reste `NO_RUNTIME_BINDING_YET` — voir
INTEGRATION_ACADEMY_PACKAGE_NOTE.md — mais c'est une question distincte,
jamais confondue avec `fully_complete`.
contexts = [EXTERNAL]. BRIDGE non retenu.
```

## Avertissement central de cette formation — `EXTENSION_NOT_DUPLICATION`

`KLT-18` **ne réenseigne pas** l'animation de communauté diaspora
(`KLT-05`/M05), le traitement de support (`KLT-05`/M07), ni la lecture de
signaux d'engagement (`KLT-05`/M09) — ces trois modules restent
autoritaires et sont cités par référence, jamais dupliqués. Cette
formation ajoute ce qui, dans ces trois compétences, n'est pas encore
couvert : la conception d'une **stratégie** de campagne (au-delà de
l'animation quotidienne), sa déclinaison multi-canal cohérente, la
gestion d'une communication de crise (escalade au-delà du support
individuel), et la restitution stratégique d'un bilan de campagne à un
comité ou un partenaire. Aucune compétence de cette formation ne dépend
d'un système externe non vérifié — la mesure d'impact (`C4`) s'appuie
explicitement sur les mêmes données réellement disponibles que
`KLT-05`/M09 (`Observatory` non simulé, legacy analytics autoritaire).

## Métier cible

**Responsable Communications & Engagement Culturel / Cultural
Communications & Engagement Operator** — niveau `Avancé`, priorité `P2`
(spécialisation/extension, pas un métier d'entrée). Pas de
correspondance ROME calibrée dans ce repo (formation `NEW`, sans
legacy).

## Responsabilités réelles (périmètre buildable, 5/5)

Concevoir une stratégie de communication/campagne au-delà de l'animation
quotidienne (objectifs, cibles, canaux, calendrier) · décliner une
campagne multi-canal en cohérence avec l'animation communautaire
existante, sans la dupliquer · gérer une communication de crise
(escalade au-delà du support individuel) · mesurer l'impact réel d'une
campagne à partir des signaux d'engagement réellement disponibles, sans
en fabriquer · restituer une revue de campagne à un comité ou un
partenaire.

## Limites du rôle — ce que le métier n'est PAS

N'anime pas la communauté diaspora au quotidien (`KLT-05`/M05, reste
autoritaire) — s'appuie sur cette animation, ne la remplace pas. Ne
traite pas le support individuel de premier niveau (`KLT-05`/M07) — gère
la communication de crise qui **dépasse** ce niveau. Ne lit pas les
signaux d'engagement de zéro (`KLT-05`/M09, reste autoritaire pour la
lecture quotidienne) — mobilise ces mêmes données à des fins de mesure
d'impact stratégique. N'anime pas de médiation terrain (`KLT-01`), ne
gère pas de budget (`KLT-02`), ne négocie pas de partenariat
institutionnel (`KLT-03`), n'a pas d'autorité de gouvernance (`KLT-04`).

## Publics / Contextes

`contexts = [EXTERNAL]` — e-learning disponible en canal externe,
physique `ELIGIBLE_PENDING_OFFER` (jamais réservable sans offre réelle).
`BRIDGE` non retenu (niveau `Avancé`, spécialisation, pas un point
d'entrée du parcours `KILTIKONET_PROFESSIONAL_PATHWAY.md`).

## Compétences (5) et modules — statut de construction

| # | Compétence | Module | Statut |
|---|---|---|---|
| C1 | Concevoir une stratégie de campagne/communication au-delà de l'animation quotidienne | M01 | `BUILT` |
| C2 | Décliner une campagne multi-canal en cohérence avec l'animation existante, sans la dupliquer | M02 | `BUILT` |
| C3 | Gérer une communication de crise (escalade au-delà du support individuel) | M03 | `BUILT` |
| C4 | Mesurer l'impact réel d'une campagne à partir des signaux réellement disponibles | M04 | `BUILT` |
| C5 | Restituer une revue de campagne à un comité ou un partenaire | M05 | `BUILT` |

**5/5 compétences construites.**

## Blueprints

| Module | WHY_THIS_MODULE_EXISTS | ASSESSED | WHAT_REAL_OUTPUT |
|---|---|---|---|
| M01 | Une campagne conçue sans objectifs/cibles/canaux explicites se dilue dans l'animation quotidienne sans jamais produire d'effet mesurable | N1/N2 | Plan de campagne |
| M02 | Une déclinaison multi-canal qui ignore l'animation déjà en place (`KLT-05`/M05) produit des messages contradictoires ou redondants | N2 | Déclinaison multi-canal |
| M03 | Une communication de crise traitée comme un simple ticket de support sous-estime son impact réputationnel | N2 | Plan de communication de crise |
| M04 | Mesurer l'impact d'une campagne sans donnée fiable fabrique une fausse impression de succès | N2 | Rapport d'impact de campagne |
| M05 | Une campagne réussie mais mal restituée à un comité ne permet aucune décision stratégique informée | N2 | Revue de campagne |

Cohérence transversale vérifiée : progression N1→N2 monotone sur les 5
modules construits, aucune compétence testée sans module, aucune
duplication de `KLT-05`/M05, M07, M09 (citées par référence uniquement).
