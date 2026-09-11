# CVLN Academy

CVLN Academy est la plateforme d’apprentissage du groupe CVLN dédiée aux compétences culturelles, créatives, techniques et entrepreneuriales. Elle réunit formations, missions, progression et certification dans une expérience pensée comme un parcours continu.

L’expérience **Spatial Learning** organise l’apprentissage comme un chemin : l’utilisateur conserve son contexte, visualise sa progression et avance de **Graine → Pousse → Racine → Branches → Arbre → Forêt**.

## Produit

CVLN Academy comprend notamment :

- un catalogue de formations organisé par pôles et modules ;
- des parcours apprenants et une progression structurée ;
- une expérience Spatial Learning ;
- des espaces adaptés aux rôles de la plateforme ;
- des mécanismes de certification et de suivi de compétences ;
- des surfaces juridiques et d’acceptation nécessaires aux parcours concernés ;
- des points d’intégration avec l’écosystème CVLN.

L’interface prévoit une expérience multilingue en **FR / EN / Kreyòl / ES**.

## Architecture

```text
CVL-ACADEMY/
├── backend/                  API FastAPI, domaine et persistance
├── frontend/                 Application React
│   └── e2e/                  Tests runtime Playwright
├── docs/                     Documentation technique, produit et audits
├── scripts/                  Outils de contrôle et de traçabilité
├── memory/                   Historique produit et décisions
└── .github/workflows/        Intégration continue
```

### Stack principale

- **Frontend** : React 19, craco, Tailwind CSS, shadcn/ui
- **Backend** : FastAPI, Python, Motor/MongoDB
- **Tests frontend** : Jest, React Testing Library, Playwright
- **Tests backend** : pytest
- **Qualité** : ESLint, Black, isort, Flake8, mypy
- **CI** : GitHub Actions

## Démarrage local

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn server:app --reload --port 8000
```

Configurer au minimum les variables attendues par l’environnement, notamment `MONGO_URL`, `DB_NAME` et `JWT_SECRET`. Ne jamais versionner de secrets réels.

### Frontend

```bash
cd frontend
yarn install
cp .env.example .env
yarn start
```

Exemple de configuration locale :

```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

Pour les instructions de développement détaillées, consulter [`docs/DEVELOPER_GUIDE.md`](docs/DEVELOPER_GUIDE.md).

## Vérification

### Frontend

```bash
cd frontend
npx eslint src e2e playwright.config.js
CI=true yarn test --watchAll=false
CI=true yarn build
npx playwright test
```

### Backend

```bash
cd backend
black --check .
pytest tests/ -n 0 --ignore=tests/backend_test.py
```

Des contrôles supplémentaires de qualité, de typage, de traçabilité et de runtime sont exécutés par les workflows GitHub Actions du dépôt. **La présence d’un test ou d’un workflow ne signifie pas qu’il est vert : le résultat GitHub Actions du commit concerné reste la preuve d’exécution.**

## Documentation

| Document | Rôle |
|---|---|
| [`docs/DEVELOPER_GUIDE.md`](docs/DEVELOPER_GUIDE.md) | Installation, architecture, conventions et API |
| [`docs/ACADEMY_CURRENT_FUNNEL_AUDIT.md`](docs/ACADEMY_CURRENT_FUNNEL_AUDIT.md) | État observé du funnel Academy |
| [`docs/ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md`](docs/ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md) | Architecture Spatial Learning |
| [`docs/SPATIAL_UPGRADE_SPEC.md`](docs/SPATIAL_UPGRADE_SPEC.md) | Spécification Spatial |
| [`docs/INTEGRATIONS_REPORT.md`](docs/INTEGRATIONS_REPORT.md) | État des intégrations CVLN |
| [`docs/FMS_IMPORT_VALIDATION_REPORT.md`](docs/FMS_IMPORT_VALIDATION_REPORT.md) | Validation du moteur d’import FMS |
| [`docs/I18N_AUDIT_REPORT.md`](docs/I18N_AUDIT_REPORT.md) | Audit de la couverture multilingue |
| [`docs/AUDIT_REPORT.md`](docs/AUDIT_REPORT.md) | Rapport d’audit daté ; ne pas le confondre avec l’état courant |
| [`INTEGRATION_CONTRACT.md`](INTEGRATION_CONTRACT.md) | Contrat d’intégration REST |
| [`frontend/README.md`](frontend/README.md) | Guide frontend |
| [`frontend/e2e/README.md`](frontend/e2e/README.md) | Guide Playwright / E2E |

## Evidence First

CVLN Academy applique les principes suivants :

- **Current != Target** : une cible ou une spécification n’est pas l’état actuel du produit ;
- **Evidence First** : une capacité est considérée comme vérifiée uniquement lorsqu’une preuve appropriée existe ;
- **Human Authority** : les décisions structurantes non décidées explicitement ne doivent pas être inventées par l’automatisation.

Les matrices Excel, rapports d’audit, résultats détaillés de CI et preuves ligne par ligne sont conservés dans leurs documents, scripts et workflows dédiés plutôt que reproduits dans ce README.

## Conformité

Les mécanismes techniques de conformité présents dans l’application ne remplacent pas la validation juridique de l’exploitation réelle. Avant mise en production, les mentions liées à l’entité exploitante, ses coordonnées, identifiants légaux, responsables, sous-traitants, traitements et durées de conservation doivent correspondre à la situation juridique effective.

Aucun secret, identifiant privé ou donnée personnelle réelle ne doit être ajouté à la documentation du dépôt.

## Licence

Propriété du groupe CVLN. Usage interne.