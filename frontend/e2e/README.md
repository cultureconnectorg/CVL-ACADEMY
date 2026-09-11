# CVLN Academy — E2E Playwright

Ce dossier contient les scénarios Playwright destinés à vérifier les comportements frontend observables de CVLN Academy dans un navigateur.

Le rôle de cette suite est de tester des parcours et interactions runtime. Elle ne remplace ni les tests unitaires, ni les tests backend, ni une validation d’intégration réelle lorsque les dépendances sont simulées.

## Exécution

Depuis `frontend/` :

```bash
npx playwright test
```

Pour exécuter un fichier précis :

```bash
npx playwright test e2e/<spec>.spec.js
```

Pour le mode interactif lorsque l’environnement le permet :

```bash
npx playwright test --ui
```

La configuration utilisée par la suite se trouve dans [`../playwright.config.js`](../playwright.config.js).

## Navigateur

GitHub Actions installe Chromium pour les scénarios Playwright. Pour un environnement local ou sandbox disposant déjà d’un navigateur compatible, suivre la configuration définie dans `playwright.config.js` et utiliser `PLAYWRIGHT_CHROMIUM_PATH` lorsqu’elle est prise en charge.

Éviter toute dépendance à un chemin local propre à une machine dans les scénarios versionnés.

## Organisation des scénarios

Les spécifications du dossier couvrent les comportements runtime de la plateforme selon les fonctionnalités présentes dans le code, notamment :

- routage et deep links ;
- protection des routes authentifiées ;
- navigation clavier et focus ;
- préférences de réduction des animations ;
- découverte des formations ;
- parcours et navigation des modules ;
- contexte et continuité Spatial Learning ;
- progression et roadmap ;
- transitions de navigation ;
- autres parcours ajoutés au produit avec leur évolution.

Le contenu exact de `e2e/` constitue la référence pour la liste courante des scénarios ; ce README n’a pas vocation à recopier durablement chaque nom de fichier.

## Fixtures et mocks

Les fixtures permettent de rendre certains scénarios déterministes. Lorsqu’un test utilise une fixture, un mock réseau ou un état frontend simulé, son résultat prouve uniquement le comportement exercé dans ces conditions.

Il ne faut pas conclure à partir d’un scénario simulé que :

- MongoDB a réellement persisté les données ;
- le backend réel a été traversé ;
- une API ou un service CVLN externe est opérationnel ;
- une intégration tierce fonctionne en production.

Ces affirmations nécessitent des preuves d’intégration adaptées.

## CI

La suite Playwright participe aux contrôles GitHub Actions du dépôt. Le résultat de la CI du commit concerné est la référence pour savoir si la suite a réellement réussi dans l’environnement d’intégration.

Une définition de workflow présente dans le dépôt n’est pas, à elle seule, une preuve de réussite.

## Ajouter ou modifier un scénario

Un scénario E2E doit :

1. vérifier un comportement utilisateur observable ;
2. rester déterministe autant que possible ;
3. expliciter ou rendre identifiable toute dépendance simulée ;
4. éviter de masquer un défaut produit par une fixture trop permissive ;
5. échouer lorsque le comportement attendu est réellement cassé ;
6. rester cohérent avec les règles d’accessibilité et de navigation de CVLN Academy.

## Règle de preuve

**Evidence First / Current != Target.** Playwright prouve uniquement ce que le scénario exécute réellement. Les spécifications, audits, matrices Excel, mocks et fixtures restent distincts d’une preuve de fonctionnement bout en bout avec les systèmes réels.