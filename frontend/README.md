# CVLN Academy — Frontend

Application React de CVLN Academy. Ce dossier porte l’expérience web de la plateforme : navigation, parcours apprenant, progression, Spatial Learning et surfaces utilisateur.

Pour la présentation générale du produit, l’architecture globale et les règles de preuve, consulter le [`README` racine](../README.md).

## Stack

- React 19
- Create React App via `craco`
- React Router
- Tailwind CSS + shadcn/ui
- Jest + React Testing Library
- Playwright
- PWA : manifest et service worker

## Installation

```bash
yarn install
cp .env.example .env
```

Configurer l’URL du backend pour l’environnement local :

```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

Puis démarrer l’application :

```bash
yarn start
```

Le serveur de développement utilise par défaut le port `3000`.

## Structure

```text
frontend/
├── src/
│   ├── pages/            Pages et surfaces produit
│   ├── components/       Composants applicatifs et UI
│   └── lib/              Primitives métier et expérience frontend
│       └── spatial/      Primitives Spatial Learning
├── e2e/                  Scénarios Playwright
└── playwright.config.js  Configuration E2E
```

`src/lib/` regroupe notamment les primitives liées à l’authentification, l’API, l’i18n, le lifecycle et l’expérience Spatial. `src/lib/spatial/` contient les primitives spécialisées telles que l’attention, la cadence, la topologie, la physique, l’haptique, l’audio et le frame pacing lorsque celles-ci sont utilisées par l’application.

## Développement

Avant de proposer une modification frontend, exécuter les contrôles pertinents :

```bash
# lint
npx eslint src e2e playwright.config.js

# tests unitaires
CI=true yarn test --watchAll=false

# build production
CI=true yarn build

# E2E
npx playwright test
```

Un test local réussi ne remplace pas le résultat de la CI du commit correspondant.

## Playwright

Les scénarios E2E et leurs limites de preuve sont documentés dans [`e2e/README.md`](e2e/README.md).

En CI, Chromium est installé pour Playwright. Dans un environnement local disposant déjà d’un Chromium compatible, `PLAYWRIGHT_CHROMIUM_PATH` peut être utilisé lorsque la configuration du projet le prévoit.

## Principes frontend

Le frontend doit préserver les règles produit définies par CVLN Academy sans simuler un état métier qui n’existe pas réellement. Une fixture, un mock ou une représentation visuelle ne constitue pas à elle seule une preuve de persistance backend ou d’intégration externe.

Pour Spatial Learning, les changements doivent préserver la continuité du parcours, l’accessibilité, la navigation et les états de progression réellement disponibles.

## Documentation associée

- [`../docs/DEVELOPER_GUIDE.md`](../docs/DEVELOPER_GUIDE.md) — guide développeur global
- [`../docs/ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md`](../docs/ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md) — architecture Spatial
- [`../docs/I18N_AUDIT_REPORT.md`](../docs/I18N_AUDIT_REPORT.md) — couverture multilingue observée
- [`e2e/README.md`](e2e/README.md) — validation runtime Playwright

## Règle de preuve

**Current != Target.** Une spécification, une maquette, une fixture ou un document d’audit ne doit pas être présenté comme une fonctionnalité frontend livrée sans preuve correspondante dans le code et, lorsque nécessaire, dans le runtime.