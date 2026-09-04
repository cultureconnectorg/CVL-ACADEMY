# KOR-01 — Note d'intégration Academy (package, pas import)

```
NO_RUNTIME_BINDING_YET. Aucun contrat d'import n'est autorisé à ce
stade. Cette note documente comment ce package SERAIT compatible avec
le moteur d'import existant, sans y toucher.
```

## Ce que ce document n'est pas

Ce n'est ni une spécification technique d'import, ni une extension de
schéma appliquée. Aucun fichier de `fms_import/`, `fms_canonical/`,
`klt_canonical/`, ou tout autre module runtime n'a été modifié pour
produire ce package (`NO_RUNTIME_BINDING`, `NO_KORA_PRODUCT_UPGRADE` —
vérifié par `git diff --stat` avant commit, voir rapport de ticket).

## Compatibilité structurelle avec les moteurs d'import existants

Le moteur `fms_import`/`fms_canonical` (et son équivalent réel
`klt_canonical`, déjà branché en runtime pour Kiltikonet) attend, pour
chaque formation, une structure documentaire par type (référentiel,
module, N1, N2, A0x, rubric, guides, templates) classée par
`resource_type` et `(formation_code, module_number)` (voir
`klt_canonical/parser.py`, précédent direct le plus proche puisqu'il
scanne déjà un dossier `docs/klt/` non zippé, comme le serait un futur
`docs/kor/`). Ce package `KOR-01` suit une structure analogue :

| Ce package | Équivalent structurel FMS/KLT |
|---|---|
| `modules/M0X_*.md` | un module par fichier |
| `assessments/N1_QUESTION_BANK.md` | banque N1 |
| `assessments/N2_EVALUATIONS.md` | évaluations N2 |
| `assessments/A01_CERTIFICATION_ASSESSMENT.md` | assessment certificatif Axx |
| `assessments/RUBRIC.md` | grille de correction |
| `skills/SKILL_ID_REGISTRY.md` | registre skill IDs |
| `skills/EVIDENCE_MODEL.md` | modèle de preuve |
| `guides/*.md` | guides candidat/correcteur/jury |
| `templates/TEMPLATES.md` | templates/livrables |
| `case/*.md` | cas fil rouge + case competency matrix |

## Précédent le plus proche : `klt_canonical`

Contrairement à FMS (import ZIP), `klt_canonical` scanne directement un
dossier `docs/klt/` déjà présent dans le repo (`provenance.py::
default_docs_dir()`), calcule `fully_complete` en direct depuis
`SKILL_ID_REGISTRY.md`, et persiste dans une collection dédiée
(`db.klt_resources`) sans jamais toucher `db.formations`. Un futur
`kor_canonical` suivrait exactement le même patron sur `docs/kor/` —
non construit par ce ticket (`NO_RUNTIME_BINDING`).

## Là où une extension de parsing serait nécessaire — `DOCUMENT_ONLY`

Le registre `skills/SKILL_ID_REGISTRY.md` de ce package utilise un
format à 5 colonnes (Skill ID/Compétence/Module/Assessment/Evidence),
**sans colonne de statut BUILT/BLOCKED** — cohérent avec le constat
`KOR-0002` §2.5 : aucune compétence `KOR-01` n'est `BLOCKED`. Un futur
parser `kor_canonical` devrait donc réutiliser la forme "5 colonnes"
déjà gérée par `klt_canonical/parser.py::parse_skill_registry` (le même
code qui gère déjà les registres KLT-01→05, également sans colonne de
statut), pas la forme "6 colonnes" utilisée pour KLT-06/07/08.

## Ce qui resterait à faire avant tout import réel (non fait ici)

- Écrire `backend/kor_canonical/` (parser, models, provenance,
  import_pipeline, read_model, progress) — mêmes garanties que
  `klt_canonical` (aucune mutation de `db.formations`/`seed_data.py`).
- Écrire le routeur API et les pages frontend sous une route additive
  (`/kora-canonical`, par analogie avec `/kiltikonet-canonical`).
- Répéter cette même construction de package pour `KOR-02` avant toute
  décision de "branchage complet" KORA — un seul formation ne
  justifie pas un moteur d'import à elle seule.

Rien de ce qui précède n'est engagé par ce ticket — c'est un futur
raisonnable, pas une promesse.
