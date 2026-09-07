# Rail 4 — "continue les H" : rapport de câblage de l'engin caméra

**Statut : DONE (scope volontairement resserré, écarts documentés ci-dessous).**
**Date : 2026-09-07.**
**Flag : `REACT_APP_ACADEMY_SPATIAL_CAMERA_INTENT` — défaut `false`. Aucun comportement existant ne change sans action déployeur explicite.**

## 0. Mandat reçu

> Voilà les « H » continue et donne moi une preview

Suite directe de la correction Rail 3 (§11 de `ACADEMY_RAIL3_SPATIAL_PEDAGOGICAL_WIRING_REPORT.md`), qui avait établi que le moteur caméra-follow d'H0.8 (état IDLE→INTENT→LOCKING→FOLLOWING→CROSSING→REVEALING→SETTLING→RETURNING, autofocus, mémoire de focus) n'était jamais sorti du prototype — zéro import en production. Ce rapport documente ce qui a réellement été extrait et branché cette passe, et ce qui reste délibérément non fait.

## 1. Ce qui n'existait nulle part dans le repo

Vérifié avant d'écrire une ligne : `git grep`/`find` sur tout le repo pour `cameraFollowTransition`, `CAMERA_STATE`, `spatial-console-h08.html` etc. — **zéro résultat**. Le moteur caméra-follow d'H0.8/H0.9/H0.10 n'a jamais existé ailleurs que dans les artefacts Claude (prototypes HTML autonomes, jamais commités — confirmé par le propre texte des rapports : « scratchpad only, never committed »). `W-FUNNEL-1` avait extrait `attention.js`/`physics.js`/`cadence.js`/`audio.js`/`haptics.js`/`topology.js` vers `frontend/src/lib/spatial/`, mais **pas** le moteur caméra.

Pour reprendre fidèlement ce moteur (« ne pas refaire Spatial »), j'ai relu la source réelle de l'artefact H0.10 (`https://claude.ai/code/artifact/aace6209-...`, 2232 lignes, le prototype le plus récent de la lignée H0.5→H0.10) et extrait le code JS réel — `cameraFollowTransition()`, `cameraReturnTransition()`, `makeAnchorContract()`, la state machine, le token de retarget/cancel — plutôt que de le redéfinir de mémoire ou d'improviser une nouvelle version.

## 2. Ce qui est réellement extrait — `frontend/src/lib/spatial/cameraFollow.js`

Nouveau fichier, framework-agnostic (même séparation que `physics.js` : aucune lecture/écriture DOM, l'appelant fournit les rects réels), portant verbatim :
- `CAMERA_STATES` — les 8 états nommés exacts du spec H0.8 (IDLE/INTENT/LOCKING/FOLLOWING/CROSSING/REVEALING/SETTLING/RETURNING), gelé.
- `clampPct(n)` — le garde-fou de pourcentage exact du prototype.
- `computeOriginPct(rect, containerRect)` — la math de positionnement caméra utilisée deux fois par `cameraFollowTransition` (source, puis destination).
- `computeFlightKeyframes(fromRect, toRect)` — la math `dx`/`dy`/`scale` du vol du clone (phase REVEALING du prototype).
- `createCameraToken()` — le garde de retarget/cancel (`LATEST_USER_INTENT_WINS`, jamais mis en file).

Testé : `cameraFollow.test.js`, 13 tests (états gelés, clamp aux bornes, math de vol avec cas réels, garde de token sur retargets rapides).

## 3. Ce qui est réellement branché en production — `useCameraIntent.js` + `SpatialHub.jsx`

**Le seul appelant en production** de `cameraFollow.js`. Portée, assumée et expliquée :

Le prototype suppose une SPA mono-document où `goto()` bascule simplement des sections `.view` sœurs déjà présentes dans le DOM — la phase REVEALING peut donc résoudre un vrai élément-ancre de destination de façon synchrone, une frame après `goto()`. La vraie application utilise React Router : un changement de route démonte/remonte des pages, et les pages de destination (Dashboard/Roadmap/...) chargent leurs propres données au montage avant de rendre le vrai élément-ancre. Une passation REVEALING vers une ancre inter-route, dans la même frame, n'est donc pas reproductible de façon fiable sans (a) promouvoir `Layout` en route de disposition `<Outlet/>` (déjà différé — même statut REPLACE-BLOCKED que la limite documentée d'`AcademyBackdrop.jsx`) et (b) une vraie protection contre la course de montage, ni construite ni vérifiée ici.

**Donc** : seules les phases INTENT→LOCKING→FOLLOWING sont branchées, sur une portée intégralement page-même (jamais de dépendance à un élément de la page de destination) :

- À l'activation d'un nœud `SpatialHub` (clic/Entrée), avant `navigate()` :
  1. `INTENT` — un clone du texte du nœud est créé.
  2. `LOCKING` — le clone est positionné exactement sur le nœud réel (`getBoundingClientRect()` réel).
  3. `FOLLOWING` — une vraie animation Web Animations API (`Element.animate()`, 260ms, `cubic-bezier(.16,1,.3,1)` — la même courbe qu'H0.8) grossit et efface le clone ; **`navigate()` est appelé pendant le vol**, exactement le timing du prototype (`goto()` appelé avant la fin de `clone.animate().onfinish`).
- `prefers-reduced-motion` court-circuite entièrement le vol — navigation instantanée, même comportement que la propre branche reduced-motion du prototype.
- Gaté par `SPATIAL_CAMERA_INTENT` (nouveau flag, défaut `false`).

**Explicitement non branché** : `CROSSING`/`REVEALING`/`SETTLING`/`RETURNING`, `makeAnchorContract` complet (champs de destination), `cameraReturnTransition` (résolution d'ancre de retour), l'autofocus engine complet (chaîne de priorité, fenêtre de suppression, PREFOCUS, centrage de zone focale), la mémoire de focus (offset de rail + origine caméra persistée entre sections). Tout cela reste extrait fidèlement dans les artefacts source mais **non porté** — nécessite la restructuration `App.js` évoquée ci-dessus.

## 4. Preuve en direct

Backend `MOCK_DB=1`, utilisateur réel onboardé sur KOR (`next_action` = KOR-01), flags `SPATIAL_HUB_ENABLED`/`SPATIAL_AUDIO`/`SPATIAL_HAPTICS`/`SPATIAL_CAMERA_INTENT` activés :

1. Dashboard, état initial : le nœud d'intention réel (KOR-01) au premier plan.
2. Clic sur ce nœud → un élément `data-testid="camera-intent-clone"` existe réellement dans le DOM pendant le vol (vérifié programmatiquement, `count() > 0`), superposé à la page suivante pendant qu'elle se charge — confirmant que `navigate()` est bien appelé mid-flight, pas après.
3. Navigation réelle confirmée : `page.url()` = `/formations/KOR-01`.
4. Page d'atterrissage, en vitesse réelle (1200ms après arrivée) : rendu propre, complet, aucun artefact visuel résiduel — l'apparence "délavée" observée dans une capture intermédiaire de test s'est révélée être un artefact du script de capture lui-même (un monkey-patch de `Element.prototype.animate` ralentissant *toutes* les animations WAAPI de la page, pas seulement celle du clone) — reproduit et confirmé non présent à vitesse réelle avant d'écrire ce rapport.

## 5. Vérification technique

- Jest : **160/160** (13 nouveaux pour `cameraFollow.js`, reste inchangé).
- ESLint : propre.
- Build production : OK.
- Playwright e2e : **73/73** — zéro régression, flag off.
- Backend : non touché cette passe.

## 6. Fichiers touchés

Nouveaux : `frontend/src/lib/spatial/cameraFollow.js`, `frontend/src/lib/spatial/cameraFollow.test.js`, `frontend/src/lib/useCameraIntent.js`.
Modifiés : `frontend/src/components/SpatialHub.jsx`, `frontend/src/lib/featureFlags.js`, `frontend/src/lib/featureFlags.test.js`, `frontend/.env.example`.
Backend : aucun fichier touché.

## 7. Explicitement hors périmètre (assumé, pas oublié)

- Autofocus engine complet (chaîne de priorité, suppression, PREFOCUS, centrage de zone focale) — non porté.
- Mémoire de focus inter-section (offset de rail + origine caméra) — non porté.
- Passation caméra inter-route réelle (phases CROSSING/REVEALING/SETTLING vers un vrai élément de destination) — bloqué par l'architecture de routage actuelle, nécessite la restructuration `App.js` en `<Outlet/>` déjà différée.
- `cameraReturnTransition` (retour Module→Roadmap/Dashboard réversant la même ancre) — non porté, même blocage.
- Roadmap/Missions/Badges/FrekProfile/ModuleJourney — le camera-intent flight n'est câblé que sur `SpatialHub` (Dashboard) cette passe.

Ces items restent dans le plan H1/`SPATIAL_H1_INTEGRATION_PLAN.md` pour une prochaine passe.
