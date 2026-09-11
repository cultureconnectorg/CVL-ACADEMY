# CVLN Academy — Frontend

Frontend React de CVLN Academy. Cette application porte l’expérience apprenant, le Spatial Learning, les surfaces de formation/progression, les espaces de rôle et le Legal Center.

## Stack

- React 19
- Create React App via `craco`
- Tailwind CSS + composants shadcn/ui
- React Router
- Jest / React Testing Library
- Playwright pour les parcours E2E
- PWA : manifest + service worker

## Installation

```bash
yarn install
cp .env.example .env
```

Configurer notamment :

```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

Puis :

```bash
yarn start
```

L’application de développement utilise par défaut le port 3000.

## Commandes de vérification

```bash
# lint
npx eslint src e2e playwright.config.js

# tests unitaires
CI=true yarn test --watchAll=false

# build production
CI=true yarn build

# E2E Playwright
npx playwright test
```

En CI, Chromium est installé par Playwright. Dans un environnement local/sandbox disposant déjà d’un exécutable Chromium, `PLAYWRIGHT_CHROMIUM_PATH` peut être utilisé pour fournir explicitement son chemin.

## Architecture utile

- `src/pages/` : surfaces produit et parcours
- `src/components/` : composants applicatifs et UI
- `src/lib/` : primitives d’expérience, auth, i18n, API, lifecycle et Spatial Learning
- `src/lib/spatial/` : attention, cadence, physique, topologie, haptique, audio et frame pacing
- `e2e/` : preuves runtime Playwright
- `playwright.config.js` : configuration E2E

## Spatial Learning

Le frontend conserve le contexte spatial entre certaines navigations : profondeur/scroll, focus et contexte de parcours. La roadmap expose la progression réelle et peut rendre les étapes futures comme horizon sans simuler un déblocage.

La traçabilité des 137 exigences du classeur Spatial est vérifiée depuis la racine du dépôt par :

```bash
node --test scripts/spatial-requirements.test.mjs
```

## Legal Center

Le frontend contient les surfaces publiques de documentation juridique et un gate d’acceptation pour les utilisateurs authentifiés lorsque le bundle courant n’a pas encore été accepté. Le flux prend en charge la signature au doigt/souris et transmet l’acceptation au backend pour conservation de la preuve.

Les principales surfaces associées se trouvent dans :

- `src/pages/LegalHub.jsx`
- `src/pages/LegalAcceptance.jsx`
- `src/components/LegalFooter.jsx`
- `src/components/CookieConsent.jsx`

## E2E

Consulter [`e2e/README.md`](e2e/README.md) pour le périmètre exact des scénarios Playwright et les limites de ce qu’ils prouvent.

## Documentation générale

La documentation canonique du projet commence dans [`../README.md`](../README.md) et [`../docs/DEVELOPER_GUIDE.md`](../docs/DEVELOPER_GUIDE.md).