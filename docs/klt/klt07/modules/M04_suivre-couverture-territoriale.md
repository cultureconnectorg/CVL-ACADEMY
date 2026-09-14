# KLT-07 — M04 — Suivre l'état réel de couverture territoriale

```
MODULE_ID: KLT07-M04
COMPETENCY_ID: C4 — Suivre l'état réel de couverture territoriale
PREREQUISITES: M01, M03
ASSESSMENT_LEVEL: N2
KILTIKONET_DEPENDENCY: Network — PRODUCT_CODE_REAL_VERIFIED (`backend/routes/network.py`, repo `cultureconnectorg/Kiltikonet-Aout2026`, commit `bb64ce7`, vérifié 2026-09-07) ; NOT_CONNECTED_TO_ACADEMY_RUNTIME (Academy n'a aucun client ni credentials appelant cette API) ; toute donnée manipulée dans ce module reste PEDAGOGICAL_ILLUSTRATIVE.
ROLE_BOUNDARIES: Concevoir un suivi de couverture sur le schéma réel vérifié n'équivaut jamais à une requête live sur des données réelles ; le suivi ne remplace jamais une décision de gouvernance réseau (frontière M02)
FREK_PROOF_MAPPING: FREK-WORK (mapping proposé — net-new, re-vérifié 2026-09-07)
ORIGIN: PROPOSED (Claude-derived, re-verified against Kiltikonet-Aout2026 2026-09-07 — voir KLT_09_20_RECONCILIATION.md §Re-vérification)
```

## Situation professionnelle

Le dossier Mémoire Vive progresse (M01-M03). Le responsable déploiement
territorial doit maintenant suivre l'état réel de couverture du réseau
Kiltikonet (territoires, opérateurs, licences actives) — sur un système
réel et vérifié, mais dont les collections peuvent être vides tant
qu'aucune donnée n'y a été insérée, et auquel Academy n'a aucune
connexion live.

## Objectifs d'apprentissage

- Concevoir un suivi de couverture territoriale aligné sur le schéma
  réel vérifié (endpoints, RBAC, lineage).
- Distinguer un territoire "actif dans le système" (`OBSERVED`) d'un
  territoire "non encore configuré" (`NOT_CONFIGURED`).
- Respecter le RBAC territorial réel (un rôle `TERRITORY_*` ne voit que
  son propre territoire ; les rôles globaux voient l'ensemble).

## Notions essentielles

Le système Network réel (`backend/routes/network.py`) expose `/overview`
(instantané agrégé public), `/territories`, `/territories/{id}`,
`/operators`, `/licenses` — avec un RBAC réel (`require_network_read`,
scoping territorial pour les rôles `TERRITORY_*`, accès global pour
`NETWORK_GLOBAL_READ_ROLES`). Chaque réponse porte une lineage. Suivre
la couverture, c'est produire une vue honnête de ce que ce système
contient réellement aujourd'hui — souvent rien (`NOT_CONFIGURED`) — pas
une estimation.

## Méthode

1. Identifier les endpoints réels pertinents pour le suivi de couverture
   (`/territories`, `/operators`, `/licenses`, `/overview`).
2. Respecter le RBAC territorial réel (un rôle `TERRITORY_*` ne voit que
   son territoire).
3. Produire une fiche de suivi qui distingue explicitement `OBSERVED`
   de `NOT_CONFIGURED`, jamais l'un pour l'autre.

## Exemples

Une fiche qui note "territoires actifs : à interroger via
`/api/network/territories`, aucune donnée insérée à ce jour
(`NOT_CONFIGURED`)" est honnête ; une fiche qui affiche "3 territoires
actifs, dont Mémoire Vive" en l'absence de toute donnée réelle fabrique
une couverture. À l'inverse, un rôle scopé `TERRITORY_*` qui prétendrait
voir la couverture globale du réseau (au lieu de son seul territoire)
violerait le RBAC réel — le respecter n'est pas optionnel, même en
exercice.

## Cas

Fiche de suivi de couverture territoriale pour le dossier Mémoire Vive
(`case/CAS_ANGLE_DEPLOIEMENT.md`).

## Erreurs fréquentes

- Présenter une couverture fabriquée en l'absence de données réelles
  insérées.
- Confondre le rôle RBAC territorial (`TERRITORY_*`, un seul territoire)
  avec un rôle global (`NETWORK_GLOBAL_READ_ROLES`, tous les
  territoires).
- Traiter le suivi de couverture comme une décision de gouvernance
  (retour à M02) plutôt qu'un constat factuel.

## Activité

Repérage des endpoints réels et de leur scoping RBAC pertinents pour le
suivi de couverture.

## Exercice

Produire la fiche de suivi de couverture territoriale, avec état de
provenance pour chaque donnée citée.

## Livrable

Fiche de suivi de couverture (1-2 pages).

## Critères de réussite

- Chaque donnée citée précise son endpoint réel et son état de
  provenance (`OBSERVED`/`NOT_CONFIGURED`).
- Le RBAC territorial réel est respecté dans le scoping de la fiche.
- Le suivi reste un constat, jamais une décision de gouvernance.

## Preuve

Fiche de suivi, conservée dans le registre de preuves — signal
`FREK-WORK`.

## Auto-évaluation

*Ma fiche cite-t-elle honnêtement l'état réel (souvent `NOT_CONFIGURED`),
ou ai-je fabriqué une couverture plausible ?*

## Passage au module suivant

M05 aborde la gestion de la relation opérateur au quotidien — une fois
le suivi de couverture posé.
