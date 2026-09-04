# KLT-03 — Responsable partenariats institutionnels culturels — Référentiel canonique + Blueprints

```
Méthode identique à KLT-01/02. KLT-0002 a tranché la question de scope
la plus délicate des 5 formations pour KLT-03 (STATUS=RESOLVED) :
conserver la profondeur institutionnelle spécifique legacy (OIF, UNESCO,
CARIFESTA, DAC, CTM, fonds européens) — ne PAS la remplacer par un
contenu générique. Le Master Plan structure et complète, il n'appauvrit
pas.
FMS_METHOD = REFERENCE, FMS_CONTENT != KLT_CONTENT.
```

## Avertissement spécifique à KLT-03 — `SOURCE_STATUS`

**Ce référentiel nomme des dispositifs institutionnels réels** (OIF,
UNESCO, CARIFESTA, DAC, CTM, Creative Europe, ERDF). Contrairement à
`KLT-01`/`KLT-02` (contenu essentiellement méthodologique), une partie
du contenu de `KLT-03` est **factuelle et datée par nature** (calendriers
d'appels à projets, procédures de dépôt, critères d'éligibilité) — des
faits qui évoluent réellement dans le temps, indépendamment de la
qualité de la rédaction. Chaque module institution-spécifique porte donc
un champ `SOURCE_STATUS = PEDAGOGICAL_ILLUSTRATIVE, À VÉRIFIER PAR UN
EXPERT AVANT USAGE OPÉRATIONNEL RÉEL` — ce contenu est structurellement
correct (comment naviguer ce type d'institution) mais ses détails
factuels précis n'ont pas été vérifiés contre une source institutionnelle
vivante à la date de rédaction. C'est la même discipline honnête que
`NO_FAKE_OBSERVATORY` appliquée à un risque différent : un contenu non
technique mais tout aussi susceptible d'être présenté à tort comme à
jour.

## Métier cible

**Chargé de développement culturel / partenariats** — ROME `k1808`/
`k1802`, confiance marché **medium**, avec un flag explicite dans la
source ("diplomatie culturelle à vérifier",
`external_calibration.py:415-440`) — repris ici comme signal
d'humilité à préserver, pas à effacer.

## Responsabilités réelles

Cartographier et développer une stratégie dans l'écosystème
institutionnel réel (OIF, UNESCO/CARIFESTA, DAC/CTM, fonds européens) ·
négocier une convention dans les limites de son mandat · pratiquer la
diplomatie culturelle · représenter Kiltikonet en instances · pratiquer
un lobbying éthique · rendre compte avec preuve · maintenir un
portefeuille de partenaires dans la durée.

## Limites du rôle

**Ne signe pas** un engagement financier définitif sans validation de la
gouvernance associative (`KLT-04`) · **ne gère pas** le budget opérationnel
d'un projet (`KLT-02`, en amont — prérequis `KLT-01 + KLT-02`) ·
**n'opère pas** la plateforme Kiltikonet.fr (`KLT-05`). C'est la seule
des 5 formations dont le mandat inclut explicitement la représentation
institutionnelle formelle — la limite la plus importante ici est de ne
pas engager Kiltikonet au-delà du mandat reçu, pas de ne pas représenter
du tout (contrairement à `KLT-01`/`KLT-02`).

## Publics / Contextes

Public : `AVANCE, PROFESSIONNEL, INSTITUTIONNEL` (`catalog_
cartography.py:239`, `KEEP`). Contexts : `INTERNAL, EXTERNAL, BRIDGE`
(les trois — `:238`, `KEEP`) — cohérent avec l'objectif stratégique
legacy ("positionner Kiltikonet dans le paysage institutionnel mondial",
`seed_data.py:644`, une dimension autant interne qu'externe).

## Dépendance descendante — `GRP-02`

`GRP-02` (*Cultural Economy & Strategic Partnerships*, pôle distinct)
liste `"KLT-03 recommandé"` comme prérequis (`seed_data.py:1000`). Rien
dans ce document ne modifie `KLT-03` en base — cette compatibilité est
préservée par construction (`NO_SEED_REPLACEMENT`).

## Compétences (12) et modules — correspondance LEGACY → CANON

| # | Compétence | Origine | Module |
|---|---|---|---|
| C1 | Cartographier l'écosystème institutionnel et bâtir une stratégie partenariale | legacy M01 + master plan M01+M02 (`MERGE`) | M01 |
| C2 | Naviguer l'OIF (Francophonie) | legacy M02 (`KEEP`, profondeur préservée) | M02 |
| C3 | Naviguer UNESCO et CARIFESTA | legacy M03 (`KEEP`) | M03 |
| C4 | Naviguer DAC, CTM et l'écosystème local | legacy M04 (`KEEP`) | M04 |
| C5 | Naviguer les fonds européens (Creative Europe, ERDF) | legacy M05 (`KEEP`) | M05 |
| C6 | Négocier une convention dans les limites de son mandat | master plan M04 (`BUILD_NEW`) | M06 |
| C7 | Pratiquer la diplomatie culturelle et le soft power | legacy M06 + master plan M05 (`MERGE`) | M07 |
| C8 | Représenter Kiltikonet en instances | legacy M07 (`KEEP`) | M08 |
| C9 | Pratiquer un lobbying culturel éthique | legacy M08 (`KEEP`) | M09 |
| C10 | Rendre compte et prouver l'impact partenarial | master plan M06 (`BUILD_NEW`, `Observatory` non simulé) | M10 |
| C11 | Maintenir un portefeuille de partenaires dans la durée | master plan M07 (`BUILD_NEW`, `Pro space` non simulé) | M11 |
| C12 | Mener une négociation/mission institutionnelle finale sous contrainte (synthèse) | legacy M09 + master plan M08 (`MERGE`, terminal) | M12 |

**Aucun module institution-spécifique n'est généralisé.** 12 modules —
ni les 9 legacy, ni les 8 du master plan : la matrice de compétences
commande le nombre, conformément à la règle posée dès `KLT-01`.

## Blueprints (résumé)

| Module | WHY_THIS_MODULE_EXISTS | ASSESSED | WHAT_REAL_OUTPUT |
|---|---|---|---|
| M01 | Sans cartographie ni stratégie, chaque sollicitation institutionnelle est traitée au coup par coup | N1 | Cartographie institutionnelle + note de stratégie |
| M02 | L'OIF a ses propres codes, calendriers et attentes — les ignorer disqualifie un dossier avant même sa lecture | N1/N2 | Dossier OIF-ready |
| M03 | UNESCO/CARIFESTA valorisent le patrimoine selon des logiques distinctes de l'OIF | N1/N2 | Note de positionnement patrimonial |
| M04 | DAC/CTM sont l'échelon local le plus accessible mais le plus mal connu | N2 | Dossier DAC/CTM complet |
| M05 | Les fonds européens exigent un montage de consortium que rien d'autre n'enseigne | N2 | Budget + lettre de consortium |
| M06 | Une convention mal négociée engage Kiltikonet au-delà de ce que son mandat permet | N2 | Term sheet pédagogique |
| M07 | La diplomatie culturelle n'est ni de la communication ni de la négociation formelle — un registre propre | N2 | Note de diplomatie culturelle |
| M08 | Représenter en instance sans préparation expose Kiltikonet à un mauvais positionnement public | N2 | Intervention préparée |
| M09 | Un lobbying non cadré éthiquement discrédite l'organisation qu'il sert | N2 | Plan de lobbying |
| M10 | Sans reporting sourcé, un financeur ne renouvelle pas sa confiance | N2/N3 | Rapport financeur sourcé |
| M11 | Un partenariat non entretenu se perd entre deux sollicitations | N2 | Plan relationnel |
| M12 | La synthèse sous contrainte distingue un représentant capable d'un exécutant de procédure | N3 (`KLT03-A01`) | Dossier + soutenance |

Cohérence transversale vérifiée : progression N1→N3 monotone, aucune
compétence testée sans module, `Observatory`/`Pro space` non simulés en
M10/M11, `SOURCE_STATUS` appliqué à M02-M05.
