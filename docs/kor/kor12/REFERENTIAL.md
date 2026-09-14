# KOR-12 — Référentiel canonique : Streaming Data & Cultural Intelligence

```
FORMATION: KOR-12
STATUT_LEGACY: NEW
BASELINE: KOR-01/KOR-02
NEEDS_EXPERT_REVIEW: TRUE (biais algorithmiques, protection des données d'audience)
```

## 1. Contenu principal (source : KOR-0001 §3, ligne 12)

Événements de lecture · plays/completions · métriques · dashboards ·
qualité des données · comportement audience · cohortes · rétention ·
tendances · performance contenus · recommandations · biais ·
intelligence culturelle · décision éditoriale.

## 2. PROFESSIONAL_ROLE → ACTIVITIES → COMPETENCIES

**Rôle professionnel** : Analyste données streaming / intelligence
culturelle.

| Activité | Compétence |
|---|---|
| Instrumenter | C1 — Concevoir un plan d'événements de lecture (plays/completions) |
| Mesurer | C2 — Construire métriques et dashboards |
| Fiabiliser | C3 — Assurer la qualité des données |
| Comprendre l'audience | C4 — Analyser le comportement d'audience |
| Segmenter | C5 — Construire des cohortes |
| Retenir | C6 — Analyser la rétention |
| Repérer | C7 — Détecter des tendances |
| Évaluer | C8 — Évaluer la performance des contenus |
| Recommander (concept) | C9 — Comprendre les systèmes de recommandation sans en fabriquer un réel pour KORA |
| Vérifier | C10 — Identifier des biais dans les données et recommandations |
| Interpréter | C11 — Produire une intelligence culturelle à partir des données |
| Éclairer | C12 — Éclairer une décision éditoriale par la donnée, sans se substituer à `KOR-04` |
| Synthétiser | C13 — Conduire un dossier data de bout en bout |

`DEPTH_DETERMINES_MODULE_COUNT` : 13 compétences → 13 modules
(`M01`-`M13`).

## 3. Provenance des compétences

Toutes `MARKET_SKILL`. Aucune `KORA_CURRENT_CAPABILITY` — voir §6.

## 4. Vérification anti-footprint (KOR-0001 §4)

> *"Streaming data / analytics (`KOR-12`) : Zéro footprint pour des
> données de lecture réelles (plays/completions). `db.progress` existe
> mais mesure la progression pédagogique Academy, pas une consommation
> média KORA — domaine différent, à ne pas confondre."*

Confirmé de nouveau. `db.progress` (progression pédagogique Academy)
n'est **jamais** utilisé ni cité comme preuve de données de streaming
réelles dans ce document ni dans les modules.

## 5. Tensions de frontière actives

- **Métadonnées catalogue vs data streaming** (`KOR-08`/`KOR-12`,
  KOR-0002 §4) : `KOR-08` décrit l'œuvre (métadonnées descriptives),
  `KOR-12` mesure son usage (données comportementales). Un même objet
  (*Rasin*) est décrit une fois (`KOR-08`) et mesuré ici, jamais
  redécrit.
- **CVLN Brain** : le pôle réel `BRN` (`registry.py` shim, événement
  `academy.certification.passed`) existe et interfacera un jour avec
  KORA. **Ce module n'affirme jamais que Brain alimente aujourd'hui des
  recommandations KORA en temps réel** — c'est faux dans ce repo. Brain
  émet un événement de certification Academy, pas un signal de
  streaming.
- **#5 (`KOR-09`/`KOR-14`)** reposée sous l'angle rétention (C6) vs
  parcours produit (`KOR-14`).

## 6. KORA_PRODUCT_GAP

| Capacité évoquée | Statut réel |
|---|---|
| Événements de lecture réels (plays/completions) | `CAPABILITY_NOT_IMPLEMENTED` |
| Dashboards d'audience | `CAPABILITY_NOT_IMPLEMENTED` |
| Moteur de recommandation | `CAPABILITY_NOT_IMPLEMENTED` |
| Détection de biais algorithmique en production | `CAPABILITY_NOT_IMPLEMENTED` |
| Interfaçage Brain → recommandations KORA | `CAPABILITY_NOT_CONNECTED` (Brain existe pour la certification Academy, pas pour KORA) |

`NO_KORA_PRODUCT_UPGRADE`.

## 7. Cas fil rouge

Naïma (`KOR-04`, Rézo Kilti) sollicite une analyste data, **Fabiola**,
pour comprendre pourquoi *Rasin* a un fort taux de complétion mais peu
de nouveaux auditeurs — donnée simulée, jamais présentée comme réelle
télémétrie KORA.

`STATUS = PROPOSED`.
