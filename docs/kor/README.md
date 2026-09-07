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
| `KOR-03→15 CONTINUOUS_BUILD` | `docs/kor/kor03/` → `kor15/` — construction pédagogique des 13 formations restantes (référentiel/modules/case/guides/skills/templates/assessments par formation) | `BUILT` |

## Formations construites

| Code | Nom | Modules | Compétences | Statut |
|---|---|---|---|---|
| `KOR-01` | Podcast & Audio Production | 14 | 14/14 | `BUILT`, `PACKAGE_COMPLETE`, aucune compétence `BLOCKED` |
| `KOR-02` | Cultural Storytelling & Broadcasting | 12 | 12/12 | `BUILT`, `PACKAGE_COMPLETE`, aucune compétence `BLOCKED` |
| `KOR-03` | Production vidéo/streaming | 11 | 11/11 | `BUILT`, `PARTIAL_PACKAGE` (structurellement 100% par `QUALITY_GATES.md`, contenu de module approfondi — 2 `Exemples` + 3 `Erreurs fréquentes` par module, profondeur alignée sur `KOR-01`/`02`) |
| `KOR-04` | Programmation éditoriale | 9 | 9/9 | `BUILT`, `PARTIAL_PACKAGE` (structurellement 100% par `QUALITY_GATES.md`, contenu de module approfondi — même traitement que `KOR-03`) |
| `KOR-05` | Opérations créateur/catalogue | 10 | 10/10 | `BUILT`, `PARTIAL_PACKAGE` (structurellement 100% par `QUALITY_GATES.md`, contenu de module approfondi — même traitement que `KOR-03`/`04`) |
| `KOR-06` | Exploitation plateforme (DSP/CDN) | 9 | 9/9 | `BUILT`, `PARTIAL_PACKAGE` (structurellement 100% par `QUALITY_GATES.md`, contenu de module approfondi — même traitement que `KOR-03`/`04`/`05` ; `KORA_PRODUCT_GAP` distinct et non affecté : DSP/CDN/monitoring réels restent `CAPABILITY_NOT_IMPLEMENTED`) |
| `KOR-07` | Droits et licences média | 9 | 9/9 | `BUILT`, `PARTIAL_PACKAGE` (structurellement 100% par `QUALITY_GATES.md`, contenu de module approfondi — même traitement que `KOR-03`→`06` ; `NEEDS_EXPERT_REVIEW = TRUE` en permanence sur tout ce corpus, discipline préservée dans l'approfondissement) |
| `KOR-08` | Métadonnées et catalogue streaming | 9 | 9/9 | `BUILT`, `PARTIAL_PACKAGE` (structurellement 100% par `QUALITY_GATES.md`, contenu de module approfondi — même traitement que `KOR-03`→`07` ; frontière LabelOS explicite préservée) |
| `KOR-09` | Développement d'audience diaspora | 11 | 11/11 | `BUILT`, `PARTIAL_PACKAGE` (structurellement 100% par `QUALITY_GATES.md`, contenu de module approfondi — même traitement que `KOR-03`→`08` ; `KORA_PRODUCT_GAP` CRM/A-B testing à grande échelle inchangé) |
| `KOR-10` | Modèle économique streaming | 10 | 10/10 | `BUILT`, `PARTIAL_PACKAGE` (structurellement 100% par `QUALITY_GATES.md`, contenu de module approfondi — même traitement que `KOR-03`→`09` ; vigilance CVE et citation Wallet/JCC réelles préservées) |
| `KOR-11`→`15` | 5 derniers angles métier KORA | variable | 100% par formation | `BUILT`, `DRAFTED` (chaque `REFERENTIAL.md` self-déclare `STATUS = PROPOSED` pour au moins un scénario de cas ; corpus le plus léger de KORA — approfondissement non encore engagé) |

**Rappel** : `BUILT` signifie que le package canonique existe et que
`QUALITY_GATES.md` de la formation rapporte 100% de couverture
structurelle réelle (aucun `ORPHAN_SKILL`/`ORPHAN_MODULE`, aucune
compétence `BLOCKED`) — cela ne signifie pas `FULLY_COMPLETE` (aucune
formation KORA n'a encore été validée par un vrai candidat) ni que
toutes les formations ont la même profondeur éditoriale par module.
Voir `docs/cvln_academy_master/99_REPORTS/W6_GLOBAL_STATUS.md` pour le
détail ligne par ligne, mis à jour à chaque approfondissement.

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
- `backend/kor_canonical/` existe et est branché au runtime Academy
  (voir `INTEGRATION_ACADEMY_PACKAGE_NOTE.md` de chaque formation) ;
  aucune mutation de `db.formations`/`seed_data.py`/`seed_modules.py`
  legacy n'a jamais été faite pour autant — le corpus canonique KORA
  reste une collection séparée (`db.kor_resources`), jamais fusionnée
  avec le contenu legacy `KOR-01`/`KOR-02` d'origine.
- `KOR-03`→`15` ont bien du contenu construit (voir tableau
  ci-dessus) — seule sa profondeur éditoriale par module varie encore
  d'une formation à l'autre.
