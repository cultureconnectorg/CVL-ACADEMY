# KLT-06 — M05 — Construire un tableau de bord à partir de données Observatory réelles

```
MODULE_ID: KLT06-M05
COMPETENCY_ID: C5 — Construire un tableau de bord à partir de données Observatory réelles
PREREQUISITES: M01, M02, M03
ASSESSMENT_LEVEL: N2
KILTIKONET_DEPENDENCY: Observatory — PRODUCT_CODE_REAL_VERIFIED (`backend/routes/observatory.py`, `backend/services/observatory_adapters/*`, repo `cultureconnectorg/Kiltikonet-Aout2026`, commit `bb64ce7`, vérifié 2026-09-07) ; NOT_CONNECTED_TO_ACADEMY_RUNTIME (Academy n'a aucun client ni credentials appelant cette API) ; toute donnée affichée dans ce module reste PEDAGOGICAL_ILLUSTRATIVE, jamais une requête live.
ROLE_BOUNDARIES: Concevoir une maquette de tableau de bord sur la base du schéma réel vérifié n'équivaut jamais à une requête live sur des données réelles
FREK_PROOF_MAPPING: FREK-WORK (mapping proposé — net-new, re-vérifié 2026-09-07)
ORIGIN: PROPOSED (Claude-derived, re-verified against Kiltikonet-Aout2026 2026-09-07 — voir KLT_09_20_RECONCILIATION.md §Re-vérification)
```

## Situation professionnelle

Mémoire Vive progresse dans sa candidature d'opérateur relais (`KLT-07`).
Si cette candidature aboutit un jour, un(e) analyste Observatory devra
pouvoir construire, sur le système réel de Kiltikonet, un tableau de
bord pour son territoire. Ce système existe réellement et a été vérifié
— mais aucune donnée réelle sur Mémoire Vive n'y est encore enregistrée.
La candidate doit concevoir la maquette sans jamais prétendre interroger
des données réelles aujourd'hui.

## Objectifs d'apprentissage

- Concevoir une maquette de tableau de bord alignée sur le schéma réel
  vérifié de l'Observatory Kiltikonet (endpoints, RBAC, lineage).
- Ne jamais présenter une maquette comme une requête live sur des
  données réelles.
- Appliquer la discipline de provenance (`OBSERVED` vs `NOT_CONFIGURED`)
  déjà posée en M02, sur le système réel cette fois.

## Notions essentielles

Le système Observatory réel (`backend/routes/observatory.py`,
`services/observatory_adapters/`) expose des endpoints founder-only en
lecture seule (`/memory`, `/timeline`, `/event-types`, `/territories`,
`/actors`, `/sessions`, plus les adaptateurs badges/conversion/network/
diffusion/live/mgraph/alerts), chacun porteur d'une **lineage explicite**
(source/collection citée). Concevoir une maquette, c'est choisir quels
endpoints afficher et comment restituer leur provenance réelle
(`OBSERVED` si la collection contient des documents, `NOT_CONFIGURED`
si elle est vide ou absente) — jamais l'un pour l'autre.

## Méthode

1. Identifier, parmi les endpoints réels vérifiés, ceux pertinents pour
   un tableau de bord territorial (ex. `/territories`, `/actors`,
   l'adaptateur `network`).
2. Concevoir la maquette (zones, métriques affichées, source citée pour
   chacune).
3. Prévoir explicitement l'affichage du cas `NOT_CONFIGURED` (collection
   vide) — jamais masqué ni interprété comme un zéro réel confirmé.

## Exemples

Une maquette qui affiche "Territoires actifs — à interroger via
`/api/observatory/territories`, source `db.registrations.country`" avec
un état "donnée non encore disponible" tant que la collection est vide
respecte la discipline. À l'inverse, une maquette qui afficherait "3
territoires actifs" sans avoir réellement interrogé l'API, en inventant
un chiffre plausible, fabriquerait une donnée — une violation directe de
`NOT_CONNECTED_TO_ACADEMY_RUNTIME`. Une maquette qui refuserait
d'inclure la moindre métrique par prudence excessive ("aucune donnée
n'existe encore, inutile de concevoir quoi que ce soit") confondrait
l'absence de données aujourd'hui avec l'absence de valeur de la
conception elle-même — la maquette reste utile avant même que les
données existent.

## Cas

Maquette de tableau de bord territorial pour Mémoire Vive, dans
l'hypothèse où sa candidature d'opérateur (`KLT-07`) aboutirait
(`case/CAS_ANGLE_OBSERVATORY.md`).

## Erreurs fréquentes

- Présenter une maquette comme si elle interrogeait des données réelles
  aujourd'hui.
- Inventer un chiffre plausible au lieu de citer honnêtement l'état
  "non configuré".
- Refuser de concevoir la maquette au prétexte qu'aucune donnée n'existe
  encore.

## Activité

Repérage des endpoints réels vérifiés pertinents pour un territoire
candidat.

## Exercice

Produire la maquette de tableau de bord territorial, avec pour chaque
métrique son endpoint source et son état de provenance possible
(`OBSERVED`/`NOT_CONFIGURED`).

## Livrable

Maquette de tableau de bord (spécification + croquis, 2-3 pages).

## Critères de réussite

- Chaque métrique affichée cite son endpoint et sa collection source
  réels.
- L'état "non configuré" est prévu et jamais masqué.
- Aucune donnée n'est fabriquée pour combler une case vide.

## Preuve

Maquette de tableau de bord, conservée dans le registre de preuves —
signal `FREK-WORK`.

## Auto-évaluation

*Ma maquette cite-t-elle des endpoints et collections réels, ou ai-je
fabriqué des métriques plausibles ?*

## Passage au module suivant

M06 aborde l'interprétation d'un signal territorial réel pour appuyer
une décision — une fois la maquette de restitution posée.
