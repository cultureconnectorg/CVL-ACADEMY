# KOR-0003/0004 — Rapport de construction pédagogique KOR-01 & KOR-02

```
WORKSTREAM = KOR (KORA)
AUTHORIZED = TRUE ("Continue et les grands contenus doivent être
éclatés autant que nécessaire pour constituer de vraies formations
dans le temps", Founder, 2026-09-04)
SOURCE = KOR-0002 (FROZEN) — réconciliation legacy/canonique,
structures haut niveau §5.1/§5.2, cas maître §6
DB_MUTATION = FALSE (livrable entièrement documentaire)
STOP_AFTER_DELIVERY = TRUE
```

## 1. Ce qui a été construit

| Formation | Dossier | Fichiers | Modules | Compétences |
|---|---|---|---|---|
| `KOR-01` — Podcast & Audio Production | `docs/kor/kor01/` | 30 | 14 | 14/14 |
| `KOR-02` — Cultural Storytelling & Broadcasting | `docs/kor/kor02/` | 28 | 12 | 12/12 |
| **Total** | `docs/kor/` (+ `README.md`) | **59** | **26** | **26/26** |

Méthode et gabarit strictement répliqués depuis `KLT-0003`/`KLT-0004`
(Kiltikonet), eux-mêmes calqués sur la profondeur FMS : par formation,
`00_BLUEPRINTS.md`, `case/` (cas fil rouge + Case Competency Matrix),
`modules/` (une fiche par module, 13 sections chacune), `assessments/`
(N1/N2/A01/RUBRIC), `skills/` (registre + modèle de preuve),
`guides/` (candidat/correcteur/jury), `templates/`,
`CERTIFICATION_MODEL.md`, `QUALITY_GATES.md`,
`INTEGRATION_ACADEMY_PACKAGE_NOTE.md`.

## 2. Éclatement appliqué (instruction explicite du Founder)

Le legacy comptait 8 modules pour `KOR-01` et 7 pour `KOR-02` — 15 au
total. Le corpus canonique en compte 26 (14 + 12), soit **+73%**, en
faisant émerger comme modules à part entière chaque lacune identifiée
par `KOR-0002` plutôt que de les compresser dans un module existant :

| Formation | Lacune identifiée (`KOR-0002`) | Module net-new |
|---|---|---|
| `KOR-01` | Interview (absente) | `M04` |
| `KOR-01` | Mix/master (implicite) | `M08` |
| `KOR-02` | Angle (implicite) | `M03` |
| `KOR-02` | Interview (absente) | `M04` |
| `KOR-02` | Narration culturelle (implicite) | `M06` |
| `KOR-02` | Représentation (absente) | `M09` |

Chaque module conservé du legacy (`KEEP`/`EXTEND`) reste traçable à sa
justification écrite dans `KOR-0002` §2/§3 — aucune fragmentation n'a
été faite pour le seul effet du nombre : chaque module correspond à une
compétence réellement distincte, vérifiée par `00_BLUEPRINTS.md` de
chaque formation (« vérification de cohérence transversale »).

## 3. Le cas maître — continuité inter-formations réelle

*L'Antenne Lanbi* traverse les deux formations avec un seul objet
central (la valise de Man Rosa), deux angles métier distincts (production
audio pour `KOR-01`, journalisme/storytelling pour `KOR-02`) — `KOR-02`
réutilise explicitement l'audio produit par `KOR-01` comme source,
plutôt que de dupliquer l'univers. C'est la première fois que ce
schéma "un cas, plusieurs angles, un objet transmis d'une formation à
l'autre" est réalisé pour KORA — Kiltikonet partage un univers mais pas
un artefact concret transmis entre formations de cette façon.

## 4. Ce qui n'a pas été fait (rappel explicite)

- Aucun contenu pour `KOR-03`→`15` — `NEW_CANONICAL_TARGET`/
  `CURRICULUM_BUILT = FALSE` inchangé (`KOR-0002` §0).
- Aucun code touché : `backend/kor_canonical/` n'existe pas
  (`NO_RUNTIME_BINDING`) — voir `INTEGRATION_ACADEMY_PACKAGE_NOTE.md`
  de chaque formation pour ce qu'un futur branchage impliquerait.
- Aucune mutation de `seed_data.py`/`seed_modules.py` (`badge_name`,
  `contexts` inchangés) — `NO_BADGE_REASSIGNMENT`, `NO_CONTEXT_OVERRIDE`
  respectés.
- Aucune compétence `PRODUCT_DEPENDENCY`/`BLOCKED` n'a été introduite —
  confirmé pour les deux formations, à la différence de `KLT-06`/`07`/
  `08`.

## 5. Vérification structurelle avant commit

`git status --porcelain` avant commit ne montre qu'un seul chemin
nouveau : `docs/kor/` (+ ce rapport et `docs/kor/README.md`) — aucun
fichier `backend/`, `frontend/`, ou `seed_*.py` modifié. Vérifié
directement, pas déclaré.

## 6. Statut du gate

**`KOR-0003` et `KOR-0004` = `BUILT`.** `KOR-01` et `KOR-02` sont
chacune complètes pour leur périmètre propre (`QUALITY_GATES.md` de
chaque formation, tous gates au vert). `KORA` dans son ensemble reste
`FULLY_COMPLETE = FALSE` (13/15 formations non construites,
`docs/kor/README.md`).

**Prochaine étape possible, non engagée ici** : `KOR-03` (Video &
Streaming Production) suivrait la même méthode, ou un "branchage"
`backend/kor_canonical/` pourrait être construit maintenant que deux
formations existent — les deux attendent une autorisation explicite.
