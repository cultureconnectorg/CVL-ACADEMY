# KLT-02 — Chef de projet culturel — Référentiel canonique + Blueprints

```
Méthode identique à KLT-01 (KLT-0003+KLT-0004), condensée ici en un seul
document car KLT-0002 a déjà tranché les questions structurelles pour
KLT-02 (STATUS=RESOLVED) : les deux blocs legacy sans case d'atterrissage
(financements DAC/CTM/OIF, communication de projet) deviennent partie du
canon — rien à re-arbitrer.
FMS_METHOD = REFERENCE, FMS_CONTENT != KLT_CONTENT.
DB_MUTATION=FALSE / RUNTIME_BINDING=FALSE / SEED_REPLACEMENT=FALSE /
CONTEXT_OVERRIDE=FALSE / FAKE_OBSERVATORY=FALSE / FAKE_KILTIKONET=FALSE
```

## Métier cible

**Chef de projet culturel** — ROME `k1808`/`e1107`, confiance marché
`high` (`external_calibration.py:396-414`). Débouchés réels : chef de
projet culturel, chargé de développement culturel, coordinateur
événement.

## Responsabilités réelles

Cadrer un projet culturel à partir d'une intention (transformer un
besoin en mandat) · construire et défendre un budget · rechercher des
financements réels (DAC/CTM/OIF/mécénat) · planifier et piloter une
équipe · communiquer sur le projet (récit, preuves) · identifier et
traiter les risques et obligations de conformité · évaluer l'impact sans
le fabriquer · faire le bilan et proposer une suite.

## Limites du rôle

**N'est pas** un médiateur qui conduit lui-même l'action de terrain de
bout en bout (`KLT-01`, dont `KLT-02` dépend en amont : prérequis `KLT-01
recommandé`) · **ne représente pas** institutionnellement Kiltikonet dans
une négociation formelle (`KLT-03`) · **n'a pas** d'autorité de
gouvernance associative (`KLT-04`) · **n'opère pas** la plateforme
Kiltikonet.fr (`KLT-05`). Peut rechercher des financements (contrairement
au médiateur `KLT-01`) mais ne signe pas de convention institutionnelle
au nom de Kiltikonet — cette limite précise distingue `KLT-02` de
`KLT-03`.

## Publics / Contextes

Public : `INTERMEDIAIRE, PROFESSIONNEL, INSTITUTIONNEL` (`catalog_
cartography.py:220`, `KEEP`). Contexts : `EXTERNAL, BRIDGE` (`:219`,
`KEEP`, aucun changement proposé pour `KLT-02` en `KLT-0002`).

## Compétences (11) et modules — correspondance LEGACY → CANON

| # | Compétence | Origine | Module |
|---|---|---|---|
| C1 | Cadrer un projet culturel (intention → mandat) | legacy M01 + master plan M01 (`MERGE`) | M01 |
| C2 | Étudier le besoin et cartographier les parties prenantes | legacy M02 + master plan M02 (`MERGE`) | M02 |
| C3 | Construire un budget culturel prévisionnel | legacy M03 + master plan M04 (`MERGE`) | M03 |
| C4 | Rechercher des financements (DAC/CTM/OIF/mécénat) | legacy M04 (`KEEP`, orphelin résolu par `KLT-0002` → canon) | M04 |
| C5 | Planifier et gérer une équipe projet | legacy M05 + master plan M03 (`MERGE`) | M05 |
| C6 | Piloter l'exécution opérationnelle | legacy M06 + master plan M06 (`MERGE`) | M06 |
| C7 | Communiquer sur un projet (récit et preuves) | legacy M07 (`KEEP`, orphelin résolu par `KLT-0002` → canon) | M07 |
| C8 | Identifier et traiter risques et conformité | master plan M05 (`BUILD_NEW`) | M08 |
| C9 | Évaluer l'impact d'un projet culturel | legacy M08 + master plan M07 (`MERGE`, `Observatory` non simulé) | M09 |
| C10 | Bilan et reconduction stratégique | legacy M09 (`KEEP`) | M10 |
| C11 | Piloter un projet sous perturbation et le défendre (synthèse) | legacy M10 + master plan M08 (`MERGE`) | M11 |

**Aucun module legacy n'est perdu, aucune compétence orpheline.**
11 modules — ni les 10 legacy tels quels, ni les 8 du master plan :
la matrice de compétences (ci-dessus) commande le nombre, pas le
tableur.

## Blueprints (résumé — WHY / COMPETENCY / ASSESSED / OUTPUT)

| Module | WHY_THIS_MODULE_EXISTS | ASSESSED | WHAT_REAL_OUTPUT |
|---|---|---|---|
| M01 | Sans mandat clair, un projet dérive dès le premier arbitrage | N1/N2 | Note de cadrage |
| M02 | Un besoin mal étudié produit un projet qui répond à la mauvaise question | N1/N2 | Étude de besoin + carte acteurs |
| M03 | Un projet sans budget chiffré n'est qu'une intention | N2 | Budget prévisionnel complet |
| M04 | La majorité des projets culturels caribéens dépendent d'un financement externe réel | N2 | Dossier de financement + 3 pistes |
| M05 | Un budget et un cadrage ne suffisent pas sans une équipe pilotée | N2 | Planning + organigramme projet |
| M06 | Le pilotage au jour le jour est distinct de la planification initiale | N2 | Tableau de bord + rythme de comité |
| M07 | Un projet non communiqué perd son financement à la reconduction | N2 | Kit de communication + plan média |
| M08 | Ignorer un risque connu jusqu'à ce qu'il survienne est la cause n°1 d'échec de projet | N2 | Registre des risques |
| M09 | Sans évaluation sourcée, l'impact d'un projet reste une affirmation non vérifiable | N2/N3 | Rapport d'évaluation d'impact |
| M10 | Un projet qui s'arrête sans bilan ne transmet rien au projet suivant | N2/N3 | Bilan + feuille de route |
| M11 | La synthèse sous contrainte réelle est ce qui distingue un chef de projet d'un exécutant | N3 (`KLT02-A01`) | Dossier + soutenance |

Cohérence transversale vérifiée : progression N1→N3 monotone, aucune
compétence testée sans module, aucune donnée Observatory simulée en M09.
