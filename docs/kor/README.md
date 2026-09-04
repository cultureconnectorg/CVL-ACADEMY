# KORA (KOR) — Corpus pédagogique canonique

```
WORKSTREAM = KOR (KORA), séparé de FMS (FMS_CLOSED = TRUE) et de KLT
(NO_CROSS-CONTAMINATION = TRUE).
FULLY_COMPLETE = FALSE — voir §Statut ci-dessous. Ne jamais lire une
absence de mention comme une complétude implicite.
```

Ce dossier rassemble le corpus pédagogique canonique de KORA, produit
selon la méthode `AUDIT → CANONICALIZE → FREEZE → BUILD → TEST → VERIFY
→ STOP` (même discipline que FMS/`fms_canonical` et Kiltikonet/
`docs/klt`).

## Généalogie des tickets

| Ticket | Contenu | Statut |
|---|---|---|
| `KOR-0001` | `docs/KORA_KOR0001_CANONICAL_EDUCATION_MAP.md` — 15 formations canoniques figées, collision legacy `KOR-01`/`02` identifiée, dépendances vérifiées | `FROZEN` |
| `KOR-0002` | `docs/KORA_KOR0002_LEGACY_CANONICAL_RECONCILIATION.md` — réconciliation élément par élément `KOR-01`/`02`, Boundary Map 13 tensions, cas maître *L'Antenne Lanbi*, structures haut niveau | `FROZEN` |
| `KOR-0003` | `docs/kor/kor01/` — construction pédagogique complète `KOR-01` (ce dossier) | `BUILT` |
| `KOR-0004` | `docs/kor/kor02/` — construction pédagogique complète `KOR-02` (ce dossier) | `BUILT` |

## Formations construites

| Code | Nom | Modules | Compétences | Statut |
|---|---|---|---|---|
| `KOR-01` | Podcast & Audio Production | 14 | 14/14 | `BUILT`, aucune compétence `BLOCKED` |
| `KOR-02` | Cultural Storytelling & Broadcasting | 12 | 12/12 | `BUILT`, aucune compétence `BLOCKED` |

## Formations non construites (rappel explicite, `KOR-0002` §0)

`KOR-03` à `KOR-15` restent `NEW_CANONICAL_TARGET` /
`CURRICULUM_BUILT = FALSE` — aucun module, aucun référentiel, aucune
compétence écrite pour elles. Elles n'apparaissent que de façon
analytique dans la Boundary Map de `KOR-0002` §4 et la traversée
conceptuelle du cas maître (`KOR-0002` §6.3), jamais comme contenu
pédagogique.

## Le cas maître — *L'Antenne Lanbi*

`KORA_CASE_UNIVERSE = SEPARATE_FROM_KILTIKONET` (décision Founder,
`KOR-0002` §0). Un seul univers, deux angles métier déjà écrits :

- `KOR-01` (`case/CAS_FIL_ROUGE.md`) — angle production audio :
  enregistrer et monter l'épisode pilote *"La valise de Man Rosa"*.
- `KOR-02` (`case/CAS_FIL_ROUGE.md`) — angle journalisme/storytelling :
  vérifier, écrire et diffuser *"La valise racontée"*, en réutilisant
  l'audio produit par `KOR-01` comme source réelle.

Les 13 autres angles métier (`KOR-03`→`15`) sont décrits en une ligne
chacun dans `KOR-0002` §6.3 — jamais construits.

## Statut — `FULLY_COMPLETE = FALSE`

`KOR-01` et `KOR-02` sont chacune complètes **pour leur périmètre
propre** (voir `QUALITY_GATES.md` de chaque formation — tous les gates
au vert, aucune compétence `BLOCKED`). Cela ne rend pas `KORA` (15
formations) `FULLY_COMPLETE` : 13 formations sur 15 restent à l'état de
cible canonique nommée, sans un seul module écrit. Toute lecture de ce
dossier qui conclurait à une complétude de `KORA` au-delà de `KOR-01`/
`KOR-02` serait une erreur — ce README l'exclut explicitement, même
principe que `docs/klt/README.md` pour Kiltikonet.

## Ce qui n'a jamais été fait par ces tickets

- Aucune mutation de `db.formations`/`seed_data.py`/`seed_modules.py`.
- Aucun renommage de badge (`Podcast Producer CVLN`, `Cultural
  Broadcaster` inchangés), aucun changement de `contexts`.
- Aucun code touché — `backend/kor_canonical/` n'existe pas encore
  (voir `INTEGRATION_ACADEMY_PACKAGE_NOTE.md` de chaque formation pour
  ce qu'un futur "branchage" impliquerait, non engagé ici).
- Aucun contenu pour `KOR-03`→`15`.
