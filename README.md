# CVLN Academy

Plateforme d’apprentissage progressive du groupe CVLN : formations, missions, certifications et parcours culturels, avec une expérience **Spatial Learning** pensée comme un chemin continu plutôt qu’une suite d’écrans isolés.

Langues prévues dans l’interface : FR / EN / Kreyòl / ES. Le catalogue seedé couvre 30 formations, 13 pôles et 233 modules, avec la progression Graine → Pousse → Racine → Branches → Arbre → Forêt.

## État actuel — 11 septembre 2026

La branche `main` intègre désormais :

- le socle Spatial Learning et la continuité de contexte entre routes ;
- la vérification ligne par ligne des **137 exigences du classeur Spatial**, avec un gate CI dédié ;
- les tests frontend unitaires et Playwright utilisés par la CI Spatial ;
- le backend FastAPI/MongoDB et ses tests de régression ;
- un **Legal Center** avec CGU, règlement Academy, charte IA et politique de confidentialité ;
- un **legal gate versionné** avant les parcours apprenants concernés ;
- la signature manuscrite/souris, la preuve d’acceptation et le hash de signature ;
- le bandeau de consentement cookies et les surfaces de transparence IA ;
- les moteurs FMS import/lineage, certification, lifecycle, skills et les adaptateurs d’intégration CVLN.

> Evidence First : ce README décrit l’état présent dans `main`. Les documents d’audit ou de cible ne doivent pas être interprétés comme des fonctionnalités livrées lorsqu’ils ne sont pas reliés au runtime.

## Stack

- **Backend** : FastAPI, Motor/MongoDB, Python
- **Frontend** : React 19, Create React App via craco, Tailwind CSS, shadcn/ui
- **Tests frontend** : Jest/React Testing Library + Playwright
- **CI** : GitHub Actions, dont `.github/workflows/spatial-excel-ci.yml`
- **IA / écosystème** : adaptateurs Academy vers les services CVLN ; consulter le rapport d’intégrations pour distinguer ce qui est réellement branché de ce qui reste contractuel

## Démarrer

Voir [`docs/DEVELOPER_GUIDE.md`](docs/DEVELOPER_GUIDE.md) pour les instructions détaillées.

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# renseigner au minimum MONGO_URL / DB_NAME / JWT_SECRET
uvicorn server:app --reload --port 8000

# Frontend
cd frontend
yarn install
cp .env.example .env
# REACT_APP_BACKEND_URL=http://localhost:8000
yarn start
```

## Vérification

```bash
# 137 exigences Spatial : une vérification par ligne
node --test scripts/spatial-requirements.test.mjs

# Frontend
cd frontend
npx eslint src e2e playwright.config.js
CI=true yarn test --watchAll=false
CI=true yarn build
npx playwright test

# Backend
cd backend
black --check .
pytest tests/ -n 0 --ignore=tests/backend_test.py
```

La CI Spatial exécute aussi des contrôles `isort`, `flake8` et `mypy` sur les fichiers backend modifiés par la tranche concernée, afin de ne pas attribuer artificiellement à une modification une dette préexistante hors de son périmètre.

## Documentation principale

| Document | Rôle |
|---|---|
| [`docs/DEVELOPER_GUIDE.md`](docs/DEVELOPER_GUIDE.md) | Installation, architecture, conventions et API |
| [`docs/AUDIT_REPORT.md`](docs/AUDIT_REPORT.md) | Audit technique historique ; à lire avec la date et le commit correspondant |
| [`docs/ACADEMY_CURRENT_FUNNEL_AUDIT.md`](docs/ACADEMY_CURRENT_FUNNEL_AUDIT.md) | État observé du funnel Academy |
| [`docs/ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md`](docs/ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md) | Architecture Spatial Learning de bout en bout |
| [`docs/SPATIAL_UPGRADE_SPEC.md`](docs/SPATIAL_UPGRADE_SPEC.md) | Spécification de l’upgrade Spatial |
| [`docs/INTEGRATIONS_REPORT.md`](docs/INTEGRATIONS_REPORT.md) | Statut réel des intégrations CVLN |
| [`docs/FMS_IMPORT_VALIDATION_REPORT.md`](docs/FMS_IMPORT_VALIDATION_REPORT.md) | Validation du moteur d’import FMS |
| [`docs/I18N_AUDIT_REPORT.md`](docs/I18N_AUDIT_REPORT.md) | Couverture multilingue observée |
| [`INTEGRATION_CONTRACT.md`](INTEGRATION_CONTRACT.md) | Contrat d’intégration REST |
| [`memory/PRD.md`](memory/PRD.md) | Historique produit et décisions |
| [`frontend/e2e/README.md`](frontend/e2e/README.md) | Périmètre et exécution des tests Playwright |

## Conformité Academy

Le parcours protégé utilise un bundle juridique versionné. Les documents publics sont accessibles via le Legal Center et l’API expose les exigences/acceptations. Une évolution substantielle d’un document requis doit entraîner une nouvelle version du bundle afin que l’acceptation soit redemandée.

Les textes présents dans l’application constituent une couche technique de conformité ; ils ne remplacent pas la validation finale de l’entité juridique, de ses coordonnées, de son SIREN/SIRET, de ses responsables, de ses sous-traitants, durées de conservation et autres mentions propres à l’exploitation réelle.

## Licence

Propriété du groupe CVLN. Usage interne.