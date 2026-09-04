# KLT-05 — Opérateur Kiltikonet / Cultural Platform Operator — Référentiel canonique + Blueprints

```
Méthode identique aux 4 formations précédentes. KLT-0002 a validé pour
KLT-05 (STATUS=RESOLVED) : upgrade majeur confirmé, ajouter identités/
accès/rôles, badges/scans/preuves, incidents/continuité. badge_name =
DISPLAY_ONLY_LEGACY. Ne pas présenter Platform Operator comme une
autorisation réelle. OPERATOR_AUTHORIZATION = NOT_IMPLEMENTED /
NOT_GRANTED.
```

## Avertissement central de cette formation — `OPERATOR_AUTHORIZATION`

`KLT-05` est la seule des cinq formations où le titre du métier lui-même
("Opérateur Kiltikonet") pourrait laisser croire qu'une certification
donne un accès réel à la plateforme Kiltikonet.fr. **Ce n'est pas le
cas.** Aucune formation Academy, KLT-05 incluse, ne délivre aujourd'hui
d'autorisation d'opérer un système réel — `OPERATOR_AUTHORIZATION =
NOT_IMPLEMENTED / NOT_GRANTED`, rappelé explicitement dans chaque module
qui pourrait laisser entendre le contraire (M02, M04, M11), dans le
guide candidat et dans le modèle de certification.

## Métier cible

**Community manager / opérateur plateforme culturelle** — ROME `e1124`/
`k1808`, confiance marché **medium** (`external_calibration.py:461-482`).

## Responsabilités réelles

Comprendre l'architecture d'une plateforme culturelle (mission, valeurs,
surfaces) · opérer dans les limites de ses identités et rôles réels ·
administrer programmes et contenus sans en fabriquer · gérer participants
et preuves de participation · animer une communauté diaspora · modérer
culturellement avec sécurité et pluralité · traiter demandes et
escalades · gérer partenariats et opérations événementielles · lire des
signaux d'engagement sans les fabriquer · réagir à un incident et assurer
la continuité.

## Limites du rôle

**Ne conduit pas** l'action de médiation de terrain (`KLT-01`) · **ne
gère pas** le budget d'un projet (`KLT-02`) · **ne représente pas**
institutionnellement Kiltikonet (`KLT-03`) · **n'a pas** d'autorité de
gouvernance associative (`KLT-04`). Et, spécifique à cette formation :
**la certification `KLT-05` ne donne, à elle seule, aucun accès
opérationnel réel à Kiltikonet.fr** — voir l'avertissement ci-dessus.

## Publics / Contextes

Public : `INTERMEDIAIRE, PROFESSIONNEL` (`catalog_cartography.py:277`,
`KEEP`). Contexts : `INTERNAL, BRIDGE` (`:276`) — **`KLT-0002` a validé
un `PROPOSE_CHANGE`** : le contenu (community management, partenariats
publics, événements IRL) lit comme externally-facing, ce qui suggère un
possible manque du contexte `EXTERNAL`. **Non appliqué ici**
(`DB_CONTEXT_MUTATION = FORBIDDEN`) — signalé pour le futur ticket de
migration dédié. `delivery_formats = DEFAULT_FORMAT` (E_LEARNING
uniquement, la seule des cinq formations sans `PRO_FORMAT`) — cohérent
avec l'absence d'infrastructure physique/hybride réelle constatée en
`KLT-0001` §4, à recroiser avec `ACA-0004` lors d'une future revue
conjointe KLT/ACA, non traitée ici.

## Compétences (11) et modules — correspondance LEGACY → CANON

| # | Compétence | Origine | Module |
|---|---|---|---|
| C1 | Comprendre l'architecture Kiltikonet (mission, valeurs, surfaces) | legacy M01 + master plan M01 (`MERGE`) | M01 |
| C2 | Opérer dans les limites de ses identités, accès et rôles (RBAC) | master plan M02 (`BUILD_NEW`) | M02 |
| C3 | Administrer programmes et contenus sans en fabriquer | legacy M04 + master plan M03 (`MERGE`) | M03 |
| C4 | Gérer participants, badges et preuves de participation (scans/NFC) | master plan M04 (`BUILD_NEW`) | M04 |
| C5 | Animer une communauté diaspora | legacy M02 (`KEEP`) | M05 |
| C6 | Modérer culturellement — sécurité et pluralité | legacy M03 (`KEEP`) | M06 |
| C7 | Traiter demandes et escalades (support) | master plan M05 (`BUILD_NEW`) | M07 |
| C8 | Gérer partenariats plateforme et opérations événementielles | legacy M06+M07 + master plan M06 (`MERGE`) | M08 |
| C9 | Lire des signaux d'engagement et rendre compte sans fabriquer | legacy M05 + master plan M07 (`MERGE`, `Observatory` non simulé, legacy reste autoritaire) | M09 |
| C10 | Réagir à un incident et assurer la continuité | master plan M08 (`BUILD_NEW`) | M10 |
| C11 | Opérer une journée complète et défendre le dossier (synthèse) | legacy M08 + master plan M09 (`MERGE`, terminal) | M11 |

**Aucun module legacy n'est perdu.** 11 modules — trois thèmes
genuinely neufs (identités/accès, badges/scans, incident/continuité),
exactement ceux que le Founder a nommés dans `KLT-0002`.

## Blueprints (résumé)

| Module | WHY_THIS_MODULE_EXISTS | ASSESSED | WHAT_REAL_OUTPUT |
|---|---|---|---|
| M01 | Sans comprendre l'architecture, un opérateur agit à l'aveugle sur ses propres surfaces | N1 | System map |
| M02 | Un opérateur qui ne connaît pas ses propres droits dépasse son mandat sans le savoir | N1/N2 | Access checklist |
| M03 | Publier sans discipline éditoriale fabrique du contenu non fiable | N2 | Plan de publication |
| M04 | Une preuve de participation mal gérée compromet toute la chaîne de confiance FREK | N2 | Runbook badge/scan |
| M05 | Une communauté diaspora a des codes propres qu'un community management générique manque | N2 | Éditorial 30 jours + KPIs |
| M06 | Une modération sans méthode devient soit laxiste soit censurante | N2 | Charte de modération |
| M07 | Un support non traité dégrade la confiance envers la plateforme | N2 | Support log |
| M08 | Un partenariat ou un événement mal préparé expose la plateforme à un incident évitable | N2 | Ops checklist + term sheet |
| M09 | Rendre compte sans donnée fiable fabrique une fausse impression de maîtrise | N2 | Rapport sourcé |
| M10 | Sans procédure d'incident, une panne devient une crise | N2/N3 | Incident report |
| M11 | La synthèse sous contrainte distingue un vrai opérateur d'un exécutant de procédure | N3 (`KLT05-A01`) | Assessment + soutenance |

Cohérence transversale vérifiée : progression N1→N3 monotone, aucune
compétence testée sans module, `Observatory` non simulé en M09.
