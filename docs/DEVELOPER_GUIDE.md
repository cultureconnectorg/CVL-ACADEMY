# CVLN Academy — Guide développeur

Stack : **FastAPI + Motor (MongoDB)** côté backend, **React 19 (CRA via
craco) + Tailwind + shadcn/ui** côté frontend. 4 langues : FR/EN/Kreyòl/ES
(voir `docs/I18N_AUDIT_REPORT.md` pour la couverture réelle par écran —
inégale, documentée honnêtement plutôt que survendue).

## 1. Démarrer en local

```bash
# Backend
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # puis renseigner MONGO_URL / DB_NAME / JWT_SECRET au minimum
uvicorn server:app --reload --port 8000

# Frontend (autre terminal)
cd frontend
yarn install
cp .env.example .env   # REACT_APP_BACKEND_URL=http://localhost:8000
yarn start
```

Le backend seed automatiquement le catalogue (30 formations), les badges,
missions et les 6 définitions de templates au premier démarrage
(`seed.py::seed_if_empty`, `template_engine::seed_default_definitions`) —
rien à faire manuellement pour avoir des données de base.

## 2. Architecture backend

```
backend/
  server.py         # FastAPI app, middleware CORS, startup (index, seed, subscribers)
  api/               # 1 routeur FastAPI par domaine — voir §5 pour la liste
  auth.py            # hashing, JWT, refresh tokens, require_role()
  models.py          # tous les schémas Pydantic partagés (User, Formation, ...)
  db.py              # client Motor
  infra_indexes.py   # tous les index Mongo (ensure_indexes(), appelé au startup)
  badges_engine.py   # award_threshold_badges() — partagé par onboarding/quiz/missions
  lx.py, quiz.py      # logique d'apprentissage LX v2 / génération-correction de quiz
  seed*.py            # données du catalogue (30 formations, 13 pôles, 233 modules)

  fms_import/         # §3 — moteur d'import ZIP FMS
  certification/       # §4 — moteur de certification N1/N2/A01
  skills/              # Skill Engine (Skill IDs, evidence, progression)
  template_engine/     # Diagnostic/Univers/Positionnement/Storytelling/Roadmap/Dossier/Pitch
  wallet/               # grand livre JCC/tokens, passes Apple/Google Wallet

  services/
    frek_core.py        # client FrekCore (fallback local complet)
    agent_factory.py    # client Agent Factory (fallback: SDK Anthropic direct)
    ai_assistant.py      # 4 personas IA au-dessus du transport agent_factory
    notifications.py     # transport email/SMS (fallback: log + db.notification_outbox)
    events.py             # bus d'événements in-process (publish/subscribe)
    integrations/          # 9 interfaces écosystème génériques + registre de statut
```

**Convention** : chaque domaine métier non trivial vit dans son propre
package top-level (`certification/`, `skills/`, `template_engine/`,
`wallet/`, `fms_import/`) avec un `models.py` (schémas), un `service.py` ou
équivalent (logique + accès DB), et parfois un module pur sans I/O
(`scoring.py`, `export.py`, `parser.py`) — c'est ce module pur qui porte les
tests unitaires rapides (`backend/tests/test_*.py`), sans mock de base de
données.

## 3. Le moteur d'import ZIP FMS (règles 5 et 15)

**Réconcilié contre le premier ZIP FMS réel** (`FMS_Chantier_Complet_20260822.zip`,
223 fichiers, FMS-01 à FMS-06 + leurs référentiels FMS-A à FMS-F,
verrouillés) — voir `docs/FMS_IMPORT_VALIDATION_REPORT.md` pour le rapport
de validation complet. La convention initialement documentée ici
(frontmatter YAML) avait dû être inventée avant qu'aucun ZIP réel
n'existe ; elle ne correspondait à aucun des 223 fichiers réels. Ce qui
suit est la convention réelle, extraite de l'archive elle-même et de son
propre gabarit de construction (`00_GABARIT_Construction_Metier.md` dans
l'archive source — les auteurs FMS l'appellent exactement ainsi : un
squelette figé, extrait de FMS-01, appliqué à l'identique à FMS-02→06).

### Format réel

Chaque fichier est du Markdown pur (prose + tableaux Markdown pour les
champs structurés) — **aucun frontmatter**. Ce qui porte l'information de
classification est le **nom de fichier**, numéroté et systématique :

```
13_FMS01_M01_Blueprint.md                       -> blueprint, FMS-01-M01-BLUEPRINT
14_FMS01_M01_Contenu_Complet.md                  -> module,    FMS-01-M01
01_FMS-A_Referentiel_Artist_Development.md       -> referentiel (métier A -> FMS-01)
09_FMS01_Master_Module_Map.md                    -> module_map, FMS-01-MODULE-MAP
49_FMS01_A01_Grille_Certificative_V1.md          -> grille_certificative, FMS-01-A01-GRILLE-CERTIFICATIVE
00_INDEX.md / 00_GABARIT_Construction_Metier.md  -> index/gabarit (transverses, sans formation_code)
```

26 types réels sont reconnus (`FmsResourceType` dans `fms_import/models.py`
— référentiel, learning_map, module_map, cas_fil_rouge, competency_matrix,
matrice_tracabilite, infrastructure, evidence_registry, skill_ids_registry,
rubric_master, blueprint, module, cas_inedit, sujet_officiel,
grille_certificative, guide_jury, banque_n1, banque_n2,
templates_etudiants, guide_formateur, guide_correcteur, guide_candidat,
note_harmonisation, matrice_pedagogique, gabarit, index, guide), classés
par indice de nom de fichier (`FILENAME_TYPE_HINTS`). Le `formation_code`
est dérivé du nom (`FMS01` -> `FMS-01`) ou, pour un référentiel, de la
table de correspondance lettre → métier que le gabarit lui-même documente
(`FMS-A` -> `FMS-01` ... `FMS-F` -> `FMS-06`,
`METIER_LETTER_TO_FORMATION`). Le `title` est pris sur la première ligne
`# ...` du corps. Les Skill IDs mentionnés dans le corps (forme
canonique `FMS0<n>-<Bloc><n°>`, ex. `FMS01-B2`) sont indexés pour la
recherche via une simple capture de sous-chaîne littérale — jamais
inventés.

Un frontmatter YAML reste supporté s'il est présent (aucun fichier réel
n'en a besoin) — ses champs (`type:`, `code:`, `formation_code:`, ...)
gagnent alors sur l'inférence par nom de fichier, pour ne rien casser si
un futur fichier en porte un.

### Prérequis entre modules (`fms_import/module_map.py`)

Les prérequis d'un module ne sont **pas** dans le fichier du module
lui-même — ils sont déclarés dans le `Master_Module_Map.md` de son
métier, module par module. Deux mises en page réelles coexistent selon le
métier (un champ par ligne pour FMS-01/02/03, une ligne compacte par
module séparée par « · » pour FMS-04/05/06) ; `module_map.py` gère les
deux. La ligne de certification (`A0n`) n'est **jamais** interprétée comme
un prérequis de module — son champ mélange prérequis obligatoire et
modules seulement recommandés/jamais requis en prose libre, qu'aplatir en
liste déformerait la doctrine.

### Comportement du parseur (`fms_import/parser.py`)

Le parseur ne lève jamais d'exception : un fichier qu'il n'arrive pas à
classer devient un **avertissement**, pas une erreur bloquante — pour
qu'un ZIP de 200 fichiers avec 3 fichiers mal formés importe quand même les
197 autres. Seules deux choses bloquent tout l'import : une archive
corrompue, ou une archive sans aucun fichier `.md`. Sur le ZIP réel :
223/223 fichiers classifiés, 0 avertissement de parsing (détail dans
`docs/FMS_IMPORT_VALIDATION_REPORT.md`).

### Pipeline complet (`fms_import/importer.py`)

```
extraire les .md du ZIP
  → parser chaque fichier (parser.py)
  → dériver les prérequis de module depuis tout Master Module Map du lot
    (module_map.py, appliqué uniquement aux ressources de type "module")
  → valider le lot (validators.py — codes dupliqués, prérequis pendants,
    modules sans formation_code)
  → upserter chaque ressource valide dans db.fms_resources
  → (re)construire l'index de recherche texte (indexer.py)
  → produire un ImportReport (créés / types / avertissements-erreurs)
```

`POST /api/fms/import` (multipart, réservé admin) déclenche ce pipeline —
c'est le bouton "Importer un métier FMS" du CMS admin
(`frontend/src/pages/admin/AdminDashboard.js`).

### Ce que ça construit

- **Recherche** : `GET /api/fms/resources?q=...&formation_code=...&type=...`
  (index texte Mongo sur titre/corps/code).
- **Sommaire auto-généré** : `GET /api/fms/formations/{code}/navigation` —
  groupe les ressources par type, dans l'ordre conceptuel → appliqué →
  évalué (référentiel avant module avant QCM avant assessment).
- **Graphe de dépendances** : `GET /api/fms/formations/{code}/dependency-graph`
  — nœuds + arêtes de prérequis, prêt pour une vue "module map".

### Ce que ça ne fait **pas** encore

Le pipeline ne transforme pas automatiquement les ressources importées en
objets `Formation`/`Module` du catalogue public (`db.formations`) — il
construit une couche de ressources parallèle, recherchable et navigable.
Cette synthèse reste un point d'extension volontairement pas improvisé :
elle mérite qu'un humain CVLN valide le mapping exact (quel champ du
Master Module Map devient quel champ de `Module`) plutôt qu'un choix
unilatéral — voir `docs/FMS_IMPORT_VALIDATION_REPORT.md` §5.

Le graphe de prérequis lui-même reste **partiel** pour FMS-04/05/06 : leur
Master Module Map n'exprime pas de `**Prérequis**` module par module pour
la majorité de leurs modules (constat honnête, pas corrigé — fabriquer un
ordre séquentiel implicite là où le document source ne le déclare pas
irait à l'encontre du principe "jamais fabriquer" de ce chantier).

## 4. Le moteur de certification (règle 6)

```
Rubric (par certification_code, versionnée)
  └── RubricCriterion[]  (bloc, poids, score max, skill_id optionnel,
                           is_eliminatory)
  └── cap_rules[]         (plafond de mention indépendant du score)
  └── mention_thresholds[] (bandes numériques -> mention, ex. Passable/Bien/...)

CertificationAttempt : in_progress → submitted → graded (passed|failed)
  attempt_number permet la reprise d'examen (retake)
  eliminated / eliminated_reason / mention — voir plus bas
```

Un `RubricCriterion` avec `max_score=4` **est** un critère "Rubric
Master" — la grille de certification réelle de FMS-01
(`49_FMS01_A01_Grille_Certificative_V1.md`) note chaque Skill ID officiel
de 0 à 4 ; ça rentre dans le modèle pondéré sans rien changer. Deux
comportements réels de cette grille, absents du modèle pondéré simple,
ont été ajoutés en réconciliant contre elle :

- **Critères éliminatoires** (`is_eliminatory=True`) : un score brut de 0
  sur ce critère échoue la tentative, indépendamment du score total (ex.
  FMS-01 : un niveau 0 sur un Skill ID rattaché à un "verrou doctrinal").
- **Plafonnement de mention** (`cap_rules`) : un score bas sur un critère
  précis plafonne la mention atteignable, jamais ne la relève (ex. FMS-01
  §3-4 : un niveau ≤1 sur le Skill ID de "cohérence globale" plafonne à
  "Passable" quel que soit le score par ailleurs).

- `certification/scoring.py` — **pur, sans I/O** : score par compétence →
  score par bloc (moyenne pondérée) → score global → pass/fail contre
  `pass_threshold_pct`, **et** élimination + mention (voir ci-dessus).
  Testé isolément (`tests/test_certification_scoring.py`, y compris les
  cas éliminatoires/plafond).
- `certification/service.py::grade_attempt` — orchestration : note, signe
  (hash SHA-256 sur `{attempt_id, jury_id, scores, signed_at}`), pousse les
  critères réussis vers le Skill Engine comme `evidence_type="certification"`,
  émet `FREK-CERT` et l'événement `academy.certification.passed`, crédite
  50 JCC au Wallet.
- `certification/attestation.py` — génère un vrai PDF (reportlab) avec le
  détail des scores et le hash de signature jury imprimé dessus.

## 5. Permissions (RBAC)

7 rôles (`models.Role`) : `student`, `trainer`, `corrector`, `jury`,
`admin`, `super_admin`, `founder`. `models.STAFF_ROLES` /
`models.ADMIN_ROLES` regroupent les rôles élevés. `auth.require_role(*roles)`
est une factory de dépendance FastAPI :

```python
@router.post("/rubrics")
async def create_rubric(inp: RubricInput, current: User = Depends(require_role(*ADMIN_ROLES))):
    ...
```

Table de référence (non exhaustive — voir chaque routeur dans `api/` pour le
détail exact) :

| Action | Rôles autorisés |
|---|---|
| CRUD organisations/rubriques, statut de publication | `admin`, `super_admin`, `founder` |
| Créer une invitation | `trainer` + rôles admin |
| Noter une tentative de certification | `jury`, `corrector` + rôles admin |
| Import ZIP FMS | rôles admin uniquement |
| Toutes les routes `/api/*` sauf `/auth/*`, `/formations` publiques, `/onboarding/options` | authentification requise (`get_current_user`) |

## 6. API — référence rapide

Documentation interactive complète : `GET /docs` (Swagger UI, auto-générée
par FastAPI) et `GET /openapi.json` une fois le backend lancé. 80 routes au
total, regroupées par domaine dans `api/__init__.py`.

Domaines principaux et leur préfixe :

| Préfixe | Domaine |
|---|---|
| `/api/auth` | inscription, connexion, refresh, reset mot de passe, vérif email, OAuth/2FA (prêts) |
| `/api/orgs`, `/api/invitations` | organisations, cohortes, invitations |
| `/api/formations`, `/api/modules` | catalogue + parcours LX v2 |
| `/api/formations/{fc}/modules/{mc}/quiz` | quiz |
| `/api/badges`, `/api/missions` | badges, missions |
| `/api/frek/profile`, `/api/progression/summary` | profil FREK, progression |
| `/api/mentor` | Mentor CVLN (chat IA étudiant) |
| `/api/fms` | import ZIP FMS, recherche, navigation, graphe |
| `/api/skills` | Skill Engine |
| `/api/certifications` | Certification Engine |
| `/api/templates` | Template Engine |
| `/api/assistants` | 4 personas IA (rule 12) |
| `/api/wallet` | CVLN Wallet |
| `/api/integrations` | statut des intégrations écosystème (admin) |

## 7. Qualité — commandes à lancer avant tout commit

```bash
# Backend
cd backend
black . && isort --profile black . && flake8 . && mypy --ignore-missing-imports .
pytest tests/ -n 0 --ignore=tests/backend_test.py   # suite unitaire, sans Mongo
# backend_test.py (E2E) nécessite un backend + Mongo réellement lancés :
# pytest tests/backend_test.py

# Frontend
cd frontend
npx eslint src
yarn build   # doit compiler sans warning
```

Toutes ces commandes sont vertes sur `HEAD` de cette branche — voir
`docs/AUDIT_REPORT.md` pour l'état détaillé.
