# CVLN Academy — E2E Playwright

Ce dossier contient les scénarios Playwright utilisés pour vérifier les comportements frontend observables de CVLN Academy, notamment la navigation, les guards, l’accessibilité de base et le Spatial Learning.

## Exécution

Depuis `frontend/` :

```bash
npx playwright test
```

`playwright.config.js` démarre le serveur CRA/craco sur `127.0.0.1:4173` pour les tests.

### Chromium

- **GitHub Actions** : la CI installe Chromium avec `npx playwright install --with-deps chromium` puis Playwright utilise ce navigateur.
- **Local / sandbox** : si un Chromium préinstallé doit être utilisé, fournir son chemin avec `PLAYWRIGHT_CHROMIUM_PATH`.

Il n’existe donc plus de dépendance documentaire à un chemin Chromium local codé en dur.

## Périmètre couvert

La suite contient notamment :

- `routing.spec.js` — routes canoniques, deep links et fallback ;
- `auth-guards.spec.js` — protection des routes authentifiées ;
- `reduced-motion.spec.js` — respect de `prefers-reduced-motion` ;
- `keyboard-focus.spec.js` — visibilité du focus clavier ;
- `landing-spatial.spec.js` — comportement de la landing Spatial ;
- `formations-discovery.spec.js` — découverte des formations ;
- `mentor-presence.spec.js` — présence contextuelle du mentor ;
- `module-journey-hierarchy.spec.js` — hiérarchie du parcours module ;
- `module-journey-navigation.spec.js` — navigation dans le parcours ;
- `module-journey-context.spec.js` — entrée/retour et contexte ;
- `roadmap-progression.spec.js` — progression, horizon et restauration de la position roadmap ;
- `route-transition.spec.js` — transitions entre routes.

Les scénarios authentifiés peuvent utiliser les fixtures du dossier `fixtures/` pour simuler de façon déterministe l’état frontend nécessaire. Cela ne doit pas être présenté comme une preuve d’intégration réelle avec MongoDB ou avec un backend externe lorsque le scénario n’en démarre pas un.

## CI Spatial

Le workflow `.github/workflows/spatial-excel-ci.yml` exécute la suite Playwright en plus de :

- la traçabilité des 137 exigences Spatial ;
- ESLint ;
- les tests unitaires frontend ;
- le build production ;
- les régressions backend prévues par le workflow.

## Règle de preuve

Un test Playwright prouve uniquement le comportement réellement exercé par son scénario et ses fixtures. Les documents de conception, audits et matrices de cible restent distincts du runtime. Ne pas marquer une intégration backend, une persistance réelle ou une dépendance externe comme « vérifiée E2E » si le scénario les simule ou ne les démarre pas.