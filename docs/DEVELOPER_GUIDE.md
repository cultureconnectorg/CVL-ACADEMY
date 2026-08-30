# CVLN Academy — Guide développeur

Stack : **FastAPI + Motor (MongoDB)** côté backend, **React 19 (CRA via
craco) + Tailwind + shadcn/ui** côté frontend. Trilingue FR/EN/Kreyòl.

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
  template_engine/     # Diagnostic/Univers/Positionnement/Storytelling/Roadmap/Dossier
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

**Aucun ZIP FMS réel n'existe encore** (il arrive après cette mission) — ce
qui suit est la convention qu'Academy définit pour ces ZIP, documentée ici
précisément pour que quiconque prépare les archives FMS-01 à FMS-06 sache
quel format produire.

### Format attendu

Chaque fichier est du Markdown avec un bloc frontmatter YAML :

```markdown
---
type: module
code: FMS-01-M03
formation_code: FMS-01
title: Poser son univers artistique
prerequisites: [FMS-01-M02]
skill_ids: [FMS.N1.B2.S3]
version: "1.0"
---
# Corps du document en Markdown...
```

`type` accepte : `referentiel`, `learning_map`, `module_map`, `blueprint`,
`module`, `qcm`, `cas_n2`, `assessment`, `template`, `guide` — la liste
exacte du brief. Si `type:` est omis, le nom de fichier est inspecté pour
un indice (`FILENAME_TYPE_HINTS` dans `fms_import/models.py` — ex. un
fichier contenant "qcm" dans son nom sera classé `qcm`). Si `code:` est
omis, il est dérivé du nom de fichier.

### Comportement du parseur (`fms_import/parser.py`)

Le parseur ne lève jamais d'exception : un fichier qu'il n'arrive pas à
classer devient un **avertissement**, pas une erreur bloquante — pour
qu'un ZIP de 200 fichiers avec 3 fichiers mal formés importe quand même les
197 autres. Seules deux choses bloquent tout l'import : une archive
corrompue, ou une archive sans aucun fichier `.md`.

### Pipeline complet (`fms_import/importer.py`)

```
extraire les .md du ZIP
  → parser chaque fichier (parser.py)
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
Faire cette synthèse sans un vrai ZIP pour valider le mapping aurait été une
supposition non vérifiable. À la réception des premiers ZIP FMS réels,
étendre `importer.py` avec une étape de synthèse `Formation` est le point
d'extension naturel.

## 4. Le moteur de certification (règle 6)

```
Rubric (par certification_code, versionnée)
  └── RubricCriterion[]  (bloc, poids, score max, skill_id optionnel)

CertificationAttempt : in_progress → submitted → graded (passed|failed)
  attempt_number permet la reprise d'examen (retake)
```

- `certification/scoring.py` — **pur, sans I/O** : score par compétence →
  score par bloc (moyenne pondérée) → score global → pass/fail contre
  `pass_threshold_pct`. Testé isolément (`tests/test_certification_scoring.py`).
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
